from django.contrib import admin
from .models import TicketStatus, TicketPriority, Ticket

admin.site.register(TicketStatus)
admin.site.register(TicketPriority)
admin.site.register(Ticket)

