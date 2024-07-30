from django.contrib import admin
from user.models import CustomUser, Participant

# Register your models here.

admin.site.register([CustomUser, Participant])