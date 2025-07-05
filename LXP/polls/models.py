from django.db import models
from django.contrib.auth.models import User

# polls/models.py

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)  # Required
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="polls")


    def __str__(self):
        return self.title

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    options = models.JSONField()
    answer_index = models.IntegerField()

