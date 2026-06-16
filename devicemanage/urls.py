"""
URL configuration for devicemanage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from devices import views as views_devices
from users import views as views_users

from devices.views import DeviceAPIView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('devices/', include('devices.urls')),
    path('', views_devices.devices_home, name='devices_home'),
    path('login/', include('users.urls')),
    path('logout/',views_users.logout, name='logout'),
    path('wiki/', include('wiki.urls')),
    path('register/', views_users.register, name='register'),
    path('api/v1/devices', DeviceAPIView.as_view()),
    path('incidents/', include('incidets.urls')),
    path('tinymce/', include('tinymce.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
