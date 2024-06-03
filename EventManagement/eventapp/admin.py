from django.contrib import admin

from .models import Event, Ticket, Venue, Attendee, Registration

# Register your models here.

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Venue)
admin.site.register(Attendee)
admin.site.register(Registration)


