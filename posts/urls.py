from django.urls import path
from .views import PostListView, PostDetailView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='posts-feed'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='posts-detail'),
    path('about/', views.about, name='posts-about'),
    path('search/', views.search, name='posts-search'),
]
