from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class FileSubssmion(models.Model):
    file = models.FileField()
    submission_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    graded = models.BooleanField(default = False)

class SubmissionReply(models.Model):
    submission = models.ForeignKey(FileSubssmion, on_delete = models.CASCADE)
    correct = models.BooleanField(default = False)
