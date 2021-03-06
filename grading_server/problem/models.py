from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from contest.models import ContestModel
from visibility.models import VisibilityModel

from datetime import datetime

class ProblemModel(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(get_user_model())
    creation_time = models.DateTimeField(auto_now_add=True)
    problem_statement = models.TextField()
    visibility = models.OneToOneField(VisibilityModel, on_delete=models.CASCADE)
    contests = models.ManyToManyField(ContestModel)

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

    def get_new_suite_number(self):
        # should this function be here (inside this class)?
        existing_suites = ProblemTestSuiteModel.objects.filter(problem=self.pk)
        if len(existing_suites) == 0:
            return 1
        suite_numbers = [suite.suite_number for suite in existing_suites]
        suite_numbers.sort()
        return suite_numbers[-1] + 1

    def is_visible(self, user):
        if self.authors.filter(pk=user.pk).exists():
            return True
        if self.visibility.is_visible(user):
            return True
        # if user is part of an active or past contest that uses this problem
        contests = [c for c in self.contests.all() if c.contestants.filter(pk=user.pk).exists()]
        time_now = datetime.now().astimezone()
        contests = [c for c in contests if time_now >= c.start_time]
        return len(contests) > 0

class ProblemTestSuiteModel(models.Model):
    problem = models.ForeignKey(ProblemModel, on_delete = models.CASCADE)
    suite_number = models.IntegerField(default = 0)
    description = models.TextField()

    def __str__(self):
        return (self.problem.name + ' test suite ' + str(self.suite_number))

    def get_absolute_url(self):
        return reverse('suite_detail', args=[str(self.problem.id), str(self.suite_number)])

    def get_new_pair_number(self):
        # should this function be here (inside this class)?
        # suppose we had pairs #1 #3
        # next pair should be #4
        existing_pairs = ProblemTestPairModel.objects.filter(suite=self.pk)
        if len(existing_pairs) == 0:
            return 1
        test_pair_numbers = [pair.pair_number for pair in existing_pairs]
        test_pair_numbers.sort()
        return test_pair_numbers[-1] + 1

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
