from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    creation_date = models.DateTimeField(default=timezone.now)
    message_text = models.TextField()

    def __str__(self):
        return f"Message {self.pk} by {self.sender} to {self.receiver}"
