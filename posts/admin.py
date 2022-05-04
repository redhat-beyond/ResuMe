from django.contrib import admin
from .models import Resume, Rating, Comment, Poll, PollFile, Choice

admin.site.register(Resume)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Poll)
admin.site.register(PollFile)
admin.site.register(Choice)
