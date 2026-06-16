from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib import messages
from .forms import TicketForm
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Ticket, TicketStatus, TicketPriority, TicketComment, TicketHistory
from users.utils import role_required

from devices.models import Device
from wiki.models import Article
from users.models import User

class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'incidents/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['history'] = (
            self.object.history
            .select_related('changed_by')
            .order_by('-changed_by')
        )
        return context

    def dispatch(self, request, *args, **kwargs):
        role = request.session.get('role')

        if role not in ['Инженер', 'Администратор','Аудитор','Оператор']:
            return redirect('devices')
        return super().dispatch(request, *args, **kwargs)

class TicketUpdateView(UpdateView):
    model = Ticket
    template_name = 'incidents/create_ticket.html'

    form_class = TicketForm

    def form_valid(self, form):
        ticket = self.get_object()
        user = User.objects.get(id=self.request.session['user_id'])
        tracked_fields = [
            'status',
            'priority',
            'assigned_to',
            'article'
        ]
        old_values = {
            field: getattr(ticket, field)
            for field in tracked_fields
        }
        response = super().form_valid(form)

        ticket.refresh_from_db()
        for field in tracked_fields:
            old = old_values[field]
            new = getattr(ticket, field)

            if old != new:
                TicketHistory.objects.create(
                    ticket=ticket,
                    changed_by=user,
                    field_name=field,
                    old_value=str(old) if old else '',
                    new_value=str(new) if new else ''
                )
        return response

    def dispatch(self, request, *args, **kwargs):
        role = request.session.get('role')

        if role not in ['Инженер', 'Администратор']:
            return redirect('incidents')
        return super().dispatch(request, *args, **kwargs)

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = '/incidents/'
    template_name = 'incidents/ticket_delete.html'

    def dispatch(self, request, *args, **kwargs):
        role = request.session.get('role')

        if role not in ['Инженер', 'Администратор']:
            return redirect('incidents')
        return super().dispatch(request, *args, **kwargs)

@role_required(['Инженер', 'Администратор','Аудитор','Оператор'])
def incidents_list(request):
    tickets = Ticket.objects.all()
    statuses = TicketStatus.objects.all()
    priorities = TicketPriority.objects.all()
    tickets_new = Ticket.objects.filter(status__name="Новая").count()
    tickets_active = Ticket.objects.filter(status__name="В работе").count()
    tickets_solved = Ticket.objects.filter(status__name="Решена").count()
    search = request.GET.get("search")
    status_id = request.GET.get("status")
    priority_id = request.GET.get("priority")

    if search:
        tickets = tickets.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(device__inventory_number__icontains=search)
        )

    if status_id:
        tickets = tickets.filter(status_id=status_id)

    if priority_id:
        tickets = tickets.filter(priority_id=priority_id)

    return render(
        request,
        "incidents/incidents.html",
        {
            "tickets": tickets,
            "statuses": statuses,
            "priorities": priorities,
            "tickets_new": tickets_new,
            "tickets_active": tickets_active,
            "tickets_solved": tickets_solved,
        }
    )

@role_required(['Администратор','Инженер','Оператор'])
def create_ticket(request):
    error = ''
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = User.objects.get(id=request.session['user_id'])
            ticket.save()
            TicketHistory.objects.create(
                ticket=ticket,
                changed_by=User.objects.get(id=request.session['user_id']),
                field_name='create',
                old_value='',
                new_value='Заявки создана'
            )
            return redirect("incidents")
        else:
            error = 'Форма заполнена некорректно'

    form = TicketForm()

    return render(request, "incidents/create_ticket.html",{'form': form, 'error': error})