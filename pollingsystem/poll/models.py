from django.db import models
from django.utils import timezone
from user.models import CustomUser, Participant

# Create your models here.


class Poll(models.Model):
    """Represents a poll having two options as choice"""

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="polls")
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    title = models.CharField(max_length=50)
    expiry_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.title} ({self.id})"


class PollOption(models.Model):
    """Represents a choice option for a Poll."""

    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="polloption/%Y/%m/&d/")
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="options")


class Vote(models.Model):
    """
    Represents a vote submitted by a participant for a specific poll option.
    """

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="votes")
    poll_option = models.ForeignKey(
        PollOption, on_delete=models.CASCADE, related_name="votes")
