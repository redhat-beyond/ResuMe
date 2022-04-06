from django.urls import path
from . import views


urlpatterns = [
    path('', views.feed, name='posts-feed'),
    path('about/', views.about, name='posts-about'),
    path('search/', views.search, name='posts-search'),
]
