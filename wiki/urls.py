from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.wiki_view, name = 'wiki'),
    path('add/', views.add_article, name = 'add_article'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name = 'detail_article'),
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name = 'update_article'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name = 'delete_article'),
    path('<int:pk>/history/',views.article_history, name = 'article_history'),
    path('history/<int:pk>/', views.article_version, name = 'article_version'),
]