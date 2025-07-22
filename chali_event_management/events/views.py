from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Event, Registration, Ticket
from .forms import EventForm
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from collections import defaultdict
import csv
import json

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    ordering = ['date_time']

    def get_queryset(self):
        queryset = Event.objects.all().order_by('date_time')
        search_query = self.request.GET.get('search')
        category_filter = self.request.GET.get('category')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(organizer__username__icontains=search_query) |
                Q(organizer__first_name__icontains=search_query) |
                Q(organizer__last_name__icontains=search_query) |
                Q(description__icontains=search_query)
            ).distinct()
        
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = context['events']
        search_query = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')
        
        # Group events by category
        events_by_category = defaultdict(list)
        for event in events:
            events_by_category[event.get_category_display()].append(event)
        
        # Convert to regular dict and sort categories
        context['events_by_category'] = dict(events_by_category)
        context['search_query'] = search_query
        context['category_filter'] = category_filter
        context['total_events'] = events.count()
        
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='Organizer').exists() or self.request.user.is_staff

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event-list')

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer or self.request.user.is_staff

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event-list')

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer or self.request.user.is_staff

class RegisterEventView(LoginRequiredMixin, TemplateView):
    template_name = 'events/event_register.html'

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        existing_registration = Registration.objects.filter(user=request.user, event=event).first()
        existing_ticket = Ticket.objects.filter(user=request.user, event=event).first()
        
        return render(request, self.template_name, {
            'event': event, 
            'existing_registration': existing_registration,
            'existing_ticket': existing_ticket,
            'available_spots': event.max_attendees - event.registrations.count(),
            'available_tickets': event.total_tickets - event.tickets.count()
        })

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        action = request.POST.get('action')
        
        if action == 'register':
            if Registration.objects.filter(user=request.user, event=event).exists():
                message = 'You are already registered for this event'
                message_type = 'error'
            elif event.registrations.count() >= event.max_attendees:
                message = 'Event is full - no more spots available'
                message_type = 'error'
            else:
                Registration.objects.create(user=request.user, event=event)
                message = 'Registration successful!'
                message_type = 'success'
                send_mail(
                    subject='Event Registration Confirmed',
                    message=f'Hello {request.user.username}, you have successfully registered for {event.title}. See you at {event.location}!',
                    from_email='no-reply@eventmanager.com',
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
        
        return render(request, self.template_name, {
            'event': event, 
            'message': message,
            'message_type': message_type,
            'available_spots': event.max_attendees - event.registrations.count(),
            'available_tickets': event.total_tickets - event.tickets.count()
        })
   

class UserDashboardView(LoginRequiredMixin, TemplateView, ):
    template_name = 'events/dashboard.html'

    def get(self, request, *args, **kwargs):
        registrations = Registration.objects.filter(user=request.user)
        tickets = Ticket.objects.filter(user=request.user).select_related('event')
        return render(request, self.template_name, {'registrations': registrations, 'tickets': tickets})


def export_attendees_csv(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.organizer and not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)

    registrations = Registration.objects.filter(event=event)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.title}-attendees.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Registered At'])
    for reg in registrations:
        writer.writerow([reg.user.username, reg.user.email, reg.registered_at])

    return response

class CalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/calendar.html'
    context_object_name = 'events'

class PurchaseTicketView(LoginRequiredMixin, TemplateView):
    template_name = 'events/purchase_ticket.html'

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        # Check if user already has tickets for this event
        existing_ticket = Ticket.objects.filter(user=request.user, event=event).first()
        return render(request, self.template_name, {
            'event': event, 
            'existing_ticket': existing_ticket,
            'available_tickets': event.total_tickets - event.tickets.count()
        })

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if user already purchased tickets
        if Ticket.objects.filter(user=request.user, event=event).exists():
            message = 'You have already purchased tickets for this event.'
            message_type = 'error'
        elif quantity < 1:
            message = 'Invalid quantity.'
            message_type = 'error'
        elif event.tickets.count() + quantity > event.total_tickets:
            message = f'Only {event.total_tickets - event.tickets.count()} tickets available.'
            message_type = 'error'
        else:
            # Create ticket purchase
            for _ in range(quantity):
                Ticket.objects.create(user=request.user, event=event)
            
            message = f'Successfully purchased {quantity} ticket(s) for ${event.ticket_price * quantity:.2f}!'
            message_type = 'success'
            
            # Send confirmation email
            send_mail(
                subject='Ticket Purchase Confirmation',
                message=f'Hello {request.user.username}, you have successfully purchased {quantity} ticket(s) for {event.title}. Total: ${event.ticket_price * quantity:.2f}',
                from_email='no-reply@eventmanager.com',
                recipient_list=[request.user.email],
                fail_silently=True,
            )

        return render(request, self.template_name, {
            'event': event, 
            'message': message,
            'message_type': message_type,
            'available_tickets': event.total_tickets - event.tickets.count()
        })


# Payment Views
class PaymentOptionsView(LoginRequiredMixin, TemplateView):
    """Display payment options for ticket purchase"""
    template_name = 'events/payment_options.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=kwargs['pk'])
        quantity = int(self.request.GET.get('quantity', 1))
        total_amount = event.ticket_price * quantity
        
        context.update({
            'event': event,
            'quantity': quantity,
            'total_amount': total_amount,
        })
        return context


class MpesaPaymentView(LoginRequiredMixin, TemplateView):
    """Handle M-Pesa payment processing"""
    template_name = 'events/mpesa_payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=kwargs['event_id'])
        quantity = int(self.request.GET.get('quantity', 1))
        total_amount = event.ticket_price * quantity
        
        context.update({
            'event': event,
            'quantity': quantity,
            'total_amount': total_amount,
            'payment_method': 'M-Pesa'
        })
        return context
    
    def post(self, request, *args, **kwargs):
        """Process M-Pesa payment"""
        event = get_object_or_404(Event, pk=kwargs['event_id'])
        quantity = int(request.POST.get('quantity', 1))
        phone_number = request.POST.get('phone_number')
        
        # TODO: Integrate with M-Pesa API
        # For now, simulate successful payment
        try:
            # Create tickets for successful payment
            for _ in range(quantity):
                Ticket.objects.create(user=request.user, event=event)
            
            messages.success(request, f'M-Pesa payment successful! {quantity} ticket(s) purchased.')
            
            # Send confirmation email
            send_mail(
                subject='M-Pesa Payment Confirmation',
                message=f'Hello {request.user.username}, your M-Pesa payment of ${event.ticket_price * quantity:.2f} for {event.title} was successful.',
                from_email='no-reply@eventmanager.com',
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, 'M-Pesa payment failed. Please try again.')
            return self.get(request, *args, **kwargs)


class PaypalPaymentView(LoginRequiredMixin, TemplateView):
    """Handle PayPal payment processing"""
    template_name = 'events/paypal_payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=kwargs['event_id'])
        quantity = int(self.request.GET.get('quantity', 1))
        total_amount = event.ticket_price * quantity
        
        context.update({
            'event': event,
            'quantity': quantity,
            'total_amount': total_amount,
            'payment_method': 'PayPal'
        })
        return context
    
    def post(self, request, *args, **kwargs):
        """Process PayPal payment"""
        event = get_object_or_404(Event, pk=kwargs['event_id'])
        quantity = int(request.POST.get('quantity', 1))
        
        # TODO: Integrate with PayPal API
        # For now, simulate successful payment
        try:
            # Create tickets for successful payment
            for _ in range(quantity):
                Ticket.objects.create(user=request.user, event=event)
            
            messages.success(request, f'PayPal payment successful! {quantity} ticket(s) purchased.')
            
            # Send confirmation email
            send_mail(
                subject='PayPal Payment Confirmation',
                message=f'Hello {request.user.username}, your PayPal payment of ${event.ticket_price * quantity:.2f} for {event.title} was successful.',
                from_email='no-reply@eventmanager.com',
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, 'PayPal payment failed. Please try again.')
            return self.get(request, *args, **kwargs)


class AirtelPaymentView(LoginRequiredMixin, TemplateView):
    """Handle Airtel Money payment processing"""
    template_name = 'events/airtel_payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=kwargs['event_id'])
        quantity = int(self.request.GET.get('quantity', 1))
        total_amount = event.ticket_price * quantity
        
        context.update({
            'event': event,
            'quantity': quantity,
            'total_amount': total_amount,
            'payment_method': 'Airtel Money'
        })
        return context
    
    def post(self, request, *args, **kwargs):
        """Process Airtel Money payment"""
        event = get_object_or_404(Event, pk=kwargs['event_id'])
        quantity = int(request.POST.get('quantity', 1))
        phone_number = request.POST.get('phone_number')
        
        # TODO: Integrate with Airtel Money API
        # For now, simulate successful payment
        try:
            # Create tickets for successful payment
            for _ in range(quantity):
                Ticket.objects.create(user=request.user, event=event)
            
            messages.success(request, f'Airtel Money payment successful! {quantity} ticket(s) purchased.')
            
            # Send confirmation email
            send_mail(
                subject='Airtel Money Payment Confirmation',
                message=f'Hello {request.user.username}, your Airtel Money payment of ${event.ticket_price * quantity:.2f} for {event.title} was successful.',
                from_email='no-reply@eventmanager.com',
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, 'Airtel Money payment failed. Please try again.')
            return self.get(request, *args, **kwargs)