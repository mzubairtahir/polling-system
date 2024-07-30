from django.contrib import admin
from poll.models import Vote, Poll, PollOption

# Register your models here.

admin.site.register([Vote, Poll, PollOption])
