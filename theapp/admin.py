from django.contrib import admin
from .models import Location, Event, Ticket

# Register your models here.
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Ticket)