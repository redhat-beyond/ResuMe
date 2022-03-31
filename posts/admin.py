from django.contrib import admin
from .models import Resume, Rating, Poll, PollFile, Choice

admin.site.register(Resume)
admin.site.register(Rating)
admin.site.register(Poll)
admin.site.register(PollFile)
admin.site.register(Choice)
