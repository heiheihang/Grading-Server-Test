from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.


class ProblemModel(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(get_user_model())
    creation_time = models.DateTimeField(auto_now_add=True)
    problem_statement = models.TextField()

    def __str__(self):
        return self.name

    def submission_url(self):
        return reverse('submission:submission_view', args=[str(self.id)])

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

class ProblemTestSuiteModel(models.Model):
    problem = models.ForeignKey(ProblemModel, on_delete = models.CASCADE)
    problem_suite_number = models.IntegerField(default = 0)
    test_suite_description = models.TextField()

    def __str__(self):
        return (self.problem.name + ' test suite ' + str(self.problem_suite_number))

    def get_absolute_url(self):
        return reverse('suite_detail', args=[str(self.problem.id), str(self.id)])


def test_file_path(instance, filename):
    problem_id = instance.test_suite.problem.pk
    suite_id = instance.test_suite.pk
    return 'problem_' + str(problem_id) + '/' + str(suite_id) + '/'


def test_input_path(instance, filename):
    return test_file_path(instance, filename) + 'input'


def test_expect_path(instance, filename):
    return test_file_path(instance, filename) + 'expect'


class ProblemTestPairModel(models.Model):
    test_suite = models.ForeignKey(ProblemTestSuiteModel, on_delete=models.CASCADE)
    pair_number = models.IntegerField(default=0)
    input = models.FileField(upload_to=test_input_path)
    output = models.FileField(upload_to=test_expect_path)

    def __str__(self):
        return(self.test_suite.problem.name + ' test suite ' + str(self.test_suite.problem_suite_number)
               + ' test pair ' + str(self.pair_number))
