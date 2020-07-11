from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class ProblemModel(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(get_user_model())
    creation_time = models.DateTimeField(auto_now_add=True)
    problem_statement = models.TextField()


class ProblemTestModel(models.Model):
    parent = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)
    input = models.FileField()
    output = models.FileField()
    task_num = models.PositiveSmallIntegerField()
    sub_task_num = models.PositiveSmallIntegerField()
    error_message = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'task_num', 'sub_task_num'], name='unique task number')
        ]
