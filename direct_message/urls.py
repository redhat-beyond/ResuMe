from django.urls import path
from .views import UsersListView, MessagesCreateView
from . import views

urlpatterns = [
    path('', UsersListView.as_view(), name='direct-message-home'),
    path('<int:user_id>/', views.chat, name='direct-message'),
    path('<int:message_receiver>/new/', MessagesCreateView.as_view(), name='direct-message-create'),
]
