from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from problem.models import ProblemModel


class FileSubssmion(models.Model):
    LANGUAGES = [('PY', 'Python 3.7')]

    file = models.FileField()
    lang = models.CharField(max_length=3, choices=LANGUAGES)
    submission_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    graded = models.BooleanField(default=False)
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE, default = None, blank = True, null= True)


class SubmissionReply(models.Model):
    submission = models.ForeignKey(FileSubssmion, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
