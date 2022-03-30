from django.contrib import admin
from .models import Poll
from .models import PollFile
from .models import Choice
from .models import Vote

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(PollFile)
admin.site.register(Vote)
