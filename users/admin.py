from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import Group

admin.site.register(Profile)

# remove group
admin.site.unregister(Group)
