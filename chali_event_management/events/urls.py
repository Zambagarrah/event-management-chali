from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    RegisterEventView,
    UserDashboardView,
    export_attendees_csv,
    CalendarView,
    PurchaseTicketView,
    PaymentOptionsView,
    MpesaPaymentView,
    PaypalPaymentView,
    AirtelPaymentView
)

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/create/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('event/<int:pk>/register/', RegisterEventView.as_view(), name='event-register'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('event/<int:pk>/export/', export_attendees_csv, name='export-attendees'),
    path('calendar/', CalendarView.as_view(), name='calendar-view'),
    path('event/<int:pk>/buy/', PurchaseTicketView.as_view(), name='purchase-ticket'),
    # Payment routes
    path('event/<int:pk>/payment/', PaymentOptionsView.as_view(), name='payment-options'),
    path('payment/mpesa/<int:event_id>/', MpesaPaymentView.as_view(), name='mpesa-payment'),
    path('payment/paypal/<int:event_id>/', PaypalPaymentView.as_view(), name='paypal-payment'),
    path('payment/airtel/<int:event_id>/', AirtelPaymentView.as_view(), name='airtel-payment'),
]
