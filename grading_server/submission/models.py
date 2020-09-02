from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from problem.models import ProblemModel
from submission.choices import *
from contest.models import ContestModel

def file_submission_name(instance, filename):
    # TODO: use my_lib?
    time = instance.submission_time.strftime('%Y-%m-%d-%H-%M-%S')
    user_id = instance.user.id
    problem_id = instance.problem.id
    submission_id = instance.pk
    return 'user_{0}/{1}_{0}_{2}/submission'.format(user_id, problem_id, time)

SUB_CHOICES = [
    ("1", "contest"),
    ("2", "practice"),
    ("3", "class"),
]

class FileSubmission(models.Model):
    #LANGUAGES = [('PY', 'Python 3.7')]

    file = models.FileField(upload_to=file_submission_name)
    lang = models.CharField(max_length=3, choices=LANG_CHOICES)
    submission_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    graded = models.BooleanField(default=False)
    report = models.FileField(upload_to='random/', blank = True, null = True)
    feedback = models.TextField(max_length=1000, null = True, blank= True)
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE, default = None, blank = True, null= True)
    correct = models.BooleanField(default = False)
    # users can submit to problem after contest ends (for practice)
    # so submission need to check whether it's part of a contest
    # Plus it's easier to find all submissions for a contest this way
    contest = models.ForeignKey(
        ContestModel, on_delete=models.CASCADE, default=None, blank=True, null=True)
    type = models.CharField(max_length = 10, choices = SUB_CHOICES, default = None, blank = True, null = True)

    def during_contest(self):
        if(self.contest != None):
            if(self.submission_time > self.contest.start_time and self.submission_time < self.contest.end_time):
                self.type = 1
            else:
                self.type = 2

    def check_contest(self):
        if(self.problem.contest != None):
            self.contest = self.problem.contest

class SubmissionReply(models.Model):
    submission = models.ForeignKey(FileSubmission, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
