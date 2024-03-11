from django.contrib import admin

# Register your models here.
from .models import AccessToken, Ticket, DailyTicketCount

admin.site.register(AccessToken)
admin.site.register(Ticket)
admin.site.register(DailyTicketCount)