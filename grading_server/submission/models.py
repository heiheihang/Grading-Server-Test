from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from problem.models import ProblemModel
from submission.choices import *

def file_submission_name(instance, filename):
    # TODO: use my_lib?
    time = instance.submission_time.strftime('%Y-%m-%d-%H-%M-%S')
    user_id = instance.user.id
    problem_id = instance.problem.id
    return 'user_{0}/{1}_{2}_{0}'.format(user_id, problem_id, time)

class FileSubmission(models.Model):
    #LANGUAGES = [('PY', 'Python 3.7')]

    file = models.FileField(upload_to=file_submission_name)
    lang = models.CharField(max_length=3, choices=LANG_CHOICES)
    submission_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    graded = models.BooleanField(default=False)
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE, default = None, blank = True, null= True)


class SubmissionReply(models.Model):
    submission = models.ForeignKey(FileSubmission, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
