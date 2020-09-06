from django.contrib import admin
from . import models
from django.conf import settings
from django.contrib import messages
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    actions = ['refund']
    list_display = ['name', 'room', 'start_date', 'end_date', 'status']
    list_display_links = ['name']
    search_fields = ['name']

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'room', 'start_date', 'end_date')
        }),
        ('Stripe', {
            'classes': ('collapse', ),
            'fields': ('stripe_id', 'stripe_payment_intent'),
            'description': 'These fields contain information about the Stripe transaction.'
        })
    )

    def refund(self, request, queryset):
        for reservation in queryset:
            if reservation.stripe_payment_intent:
                try:
                    stripe.Refund.create(
                        payment_intent=reservation.stripe_payment_intent
                    )
                except:
                    self.message_user(request, 'There was an unexpected error. Please try again later.', level=messages.ERROR)
                reservation.delete()
                self.message_user(request, f'The reservation for {reservation.name} was refunded successfully.')


admin.site.register(models.BannedDate)
admin.site.register(models.Room)