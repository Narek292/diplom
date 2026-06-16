from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.incidents_list, name='incidents'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('<int:pk>/update/', views.TicketUpdateView.as_view(), name='update_ticket'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='detail_ticket'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='delete_ticket'),

]