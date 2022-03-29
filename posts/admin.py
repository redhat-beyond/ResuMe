from django.contrib import admin
from .models import Poll
from .models import PollFile
from .models import Choice

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(PollFile)
