from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class FileSubssmion(models.Model):
    LANGUAGES = [('PY', 'Python 3.7')]

    file = models.FileField()
    lang = models.CharField(max_length=3, choices=LANGUAGES)
    submission_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    graded = models.BooleanField(default=False)


class SubmissionReply(models.Model):
    submission = models.ForeignKey(FileSubssmion, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
