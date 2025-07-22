from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'date_time', 'location', 'image', 'max_attendees', 'total_tickets', 'ticket_price']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ticket_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
        labels = {
            'title': 'Event Title',
            'description': 'Event Description',
            'category': 'Event Category',
            'date_time': 'Date and Time',
            'location': 'Event Location',
            'image': 'Event Image',
            'max_attendees': 'Maximum Attendees',
            'total_tickets': 'Total Tickets Available',
            'ticket_price': 'Ticket Price (USD)',
        }