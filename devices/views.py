from django.shortcuts import render, redirect
from .models import Device, DeviceType, DeviceStatus, DeviceLog
from incidets.models import Ticket
from .forms import DeviceForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.db.models import Q
from rest_framework import generics
from users.utils import role_required
from wiki.models import Article
from incidets.models import Ticket



class DeviceDetailView(DetailView):
    model = Device
    template_name = 'devices/device_detail.html'
    context_object_name = 'device'

    def dispatch(self, request, *args, **kwargs):
        role = request.session.get('role')

        if role not in ['Инженер', 'Администратор','Аудитор','Оператор']:
            return redirect('devices')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = self.object.logs.all().order_by('-created_at')
        return context

class DeviceUpdateView(UpdateView):
    model = Device
    template_name = 'devices/add_device.html'

    form_class = DeviceForm

    def dispatch(self, request, *args, **kwargs):
        role = request.session.get('role')

        if role not in ['Инженер', 'Администратор']:
            return redirect('devices')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        DeviceLog.objects.create(
            device = self.object,
            user_id = self.request.session.get('user_id'),
            action = 'update',
            description = 'Устройство было изменено'
        )
        return response

class DeviceDeleteView(DeleteView):
    model = Device
    success_url = '/devices/'
    template_name = 'devices/delete_device.html'

    def dispatch(self, request, *args, **kwargs):
        role = request.session.get('role')

        if role not in ['Инженер', 'Администратор']:
            return redirect('devices')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        DeviceLog.objects.create(
            device = self.object,
            user_id = self.request.session.get('user_id'),
            action = 'delete',
            description = 'Устройство удалено'
        )
        return super().form_valid(form)

from .serializers import DeviceSerializer



class DeviceAPIView(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

@role_required(['Оператор','Инженер','Администратор','Аудитор'])
def devices_home(request):
    devices_all = Device.objects.count()
    device_broken = Device.objects.filter(status__name='Неисправен').count()
    articles = Article.objects.all().count()
    tickets = Ticket.objects.all().count()
    devices_online = Device.objects.filter(status__name='В работе').count()
    devices_reserve = Device.objects.filter(status__name='В резерве').count()
    tickets_new = Ticket.objects.filter(status__name='Новая').count()
    tickets_work = Ticket.objects.filter(status__name='В работе').count()
    tickets_done = Ticket.objects.filter(status__name='Решена').count()
    recent_tickets = Ticket.objects.order_by('-created_at')[:5]

    return render(request,'devices/main.html',{'devices_count':devices_all,
                                               'devices_broken': device_broken,
                                               'articles_count': articles,
                                               'tickets_count': tickets,
                                               'devices_offline': devices_reserve,
                                               'devices_online': devices_online,
                                               'tickets_new': tickets_new,
                                               'tickets_work': tickets_work,
                                               'tickets_done': tickets_done,
                                               'recent_tickets': recent_tickets
                                               })

@role_required(['Оператор','Инженер','Администратор','Аудитор'])
def devices(request):
    devices = Device.objects.all()
    types = DeviceType.objects.all()
    status = DeviceStatus.objects.all()
    devices_online = Device.objects.filter(status__name='В работе').count()
    device_broken = Device.objects.filter(status__name='Неисправен').count()
    devices_offline = Device.objects.filter(status__name='В резерве').count()
    type_id = request.GET.get('type')
    if type_id:
        devices = devices.filter(type_id=type_id)

    status_id = request.GET.get('status')
    if status_id:
        devices = devices.filter(status_id=status_id)

    search = request.GET.get('search')
    if search:
        devices = devices.filter(
            Q(type__name__icontains=search)|
            Q(status__name__icontains=search)|
            Q(location__building__icontains=search)|
            Q(location__room__icontains=search)|
            Q(inventory_number__icontains=search)
        )

    return render(request,'devices/devices.html',{'devices':devices,
                                                  'types':types,
                                                  'status': status,
                                                  'devices_online': devices_online,
                                                  'devices_offline': devices_offline,
                                                  'devices_broken': device_broken
                                                  })

@role_required(['Инженер','Администратор'])
def add_device(request):
    error = ''
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save()
            DeviceLog.objects.create(
                device = device,
                user_id = request.session.get('user_id'),
                action = 'create',
                description = 'Устройство создано'
            )
            return redirect('devices')
        else:
            error = 'Форма заполнена некорректно!'



    form = DeviceForm()
    data = {
        'form':form,
        'error':error
    }



    return render(request,'devices/add_device.html',data)
@role_required(['Оператор','Инженер','Администратор','Аудитор'])
def device_logs(request):
    logs = DeviceLog.objects.select_related('device', 'user').order_by('-created_at')

    return render(request, 'devices/logs.html', {'logs':logs})