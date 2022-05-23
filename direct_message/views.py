from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from users.models import User
from .models import Message


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'direct_message/main_messages.html'
    context_object_name = 'Users'

    def get_queryset(self):
        users = super(UsersListView, self).get_queryset()
        return users.exclude(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        ctx = super(UsersListView, self).get_context_data(**kwargs)
        ctx['title'] = 'Users'
        return ctx


@login_required
def chat(request, user_id):
    user = User.objects.get(pk=user_id)
    direct_messages_sender = Message.objects.filter(sender=user_id, receiver=request.user.id)
    direct_messages_receiver = Message.objects.filter(sender=request.user.id, receiver=user_id)
    direct_messages = direct_messages_sender.union(direct_messages_receiver)
    return render(request, 'direct_message/direct_message.html', {'direct_messages': direct_messages,
                                                                  'send_to': user.username})


class MessagesCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['message_text']

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = User.objects.get(pk=self.kwargs['message_receiver'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(MessagesCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'direct-message-create'
        return ctx

    def get_success_url(self):
        receiver_id = self.kwargs['message_receiver']
        return f'/direct/{receiver_id}/'
