from django.urls import path
from .views import PostListView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='posts-feed'),
    path('about/', views.about, name='posts-about'),
    path('search/', views.search, name='posts-search'),
]
