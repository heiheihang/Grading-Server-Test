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

    def author_string(self):
        authors_names = [a.get_username() for a in self.authors.all()]
        authors_names.sort()
        num_of_authors = len(authors_names)
        if num_of_authors == 0:
            return 'None'
        elif num_of_authors == 1:
            return authors_names[0]
        else:
            return ', '.join(authors_names[:-1]) + ' and ' + authors_names[-1]


class ProblemTestSuiteModel(models.Model):
    problem = models.ForeignKey(ProblemModel, on_delete = models.CASCADE)
    suite_number = models.IntegerField(default = 0)
    description = models.TextField()

    def __str__(self):
        return (self.problem.name + ' test suite ' + str(self.suite_number))

    def get_absolute_url(self):
        return reverse('suite_detail', args=[str(self.problem.id), str(self.suite_number)])


def test_file_path(instance, filename):
    problem_id = instance.suite.problem.pk
    suite_id = instance.suite.pk
    return 'problem_' + str(problem_id) + '/' + str(suite_id) + '/'


def test_input_path(instance, filename):
    return test_file_path(instance, filename) + 'input'


def test_expect_path(instance, filename):
    return test_file_path(instance, filename) + 'expect'


class ProblemTestPairModel(models.Model):
    suite = models.ForeignKey(ProblemTestSuiteModel, on_delete=models.CASCADE)
    pair_number = models.IntegerField(default=0)
    input = models.FileField(upload_to=test_input_path)
    output = models.FileField(upload_to=test_expect_path)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return(self.suite.problem.name + ' test suite ' + str(self.suite.suite_number)
               + ' test pair ' + str(self.pair_number))
