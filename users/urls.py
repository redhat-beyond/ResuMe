from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='users-profile'),
    path('login/', views.login, name='users-login'),
    path('logout/', views.logout, name='users-logout'),
    path('edit-profile/', views.edit_profile, name='users-edit-profile')

]
