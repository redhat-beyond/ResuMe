from django.contrib import admin
from .models import Resume, Rating, Comment, Poll

admin.site.register(Resume)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Poll)
