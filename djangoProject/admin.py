from django.contrib import admin
from .models import Students
from .models import Polls
from .models import Sessions

admin.site.register(Students)
admin.site.register(Polls)
admin.site.register(Sessions)
