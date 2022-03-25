from django.contrib import admin
from .models import userProfile
from django.contrib.auth.models import Group

admin.site.register(userProfile)

# remove group
admin.site.unregister(Group)
