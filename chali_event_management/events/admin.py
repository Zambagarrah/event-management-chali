from django.contrib import admin
from .models import Event, Registration, Ticket
class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ('user', 'quantity', 'purchased_at')
    can_delete = False

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registered_at')
    search_fields = ('user__username', 'event__title')
    list_filter = ('registered_at',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'quantity', 'purchased_at')
    search_fields = ('user__username', 'event__title')
    list_filter = ('purchased_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'date_time', 'location',
        'ticket_price', 'total_tickets', 'max_attendees'
    )
    search_fields = ('title', 'location', 'category')
    list_filter = ('category', 'date_time')
    inlines = [TicketInline]