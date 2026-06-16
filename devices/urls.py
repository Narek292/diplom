from django.urls import path
from . import views

urlpatterns = [
    path('', views.devices, name = 'devices'),
    path('add/', views.add_device, name = 'add_device'),
    path('<int:pk>/', views.DeviceDetailView.as_view(), name = 'device_detail'),
    path('<int:pk>/update/', views.DeviceUpdateView.as_view(), name = 'device_update'),
    path('<int:pk>/delete/', views.DeviceDeleteView.as_view(), name = 'device_delete'),
    path('logs/', views.device_logs, name = 'device_logs')
]