from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

from visibility.models import VisibilityModel


class ContestModel(models.Model):
    name = models.CharField(max_length=100)
    # description = models.TextField()
    authors = models.ManyToManyField(get_user_model(), related_name='author')
    # visibility only says who can see that the contest exists
    # (eg private class-only contest)
    visibility = models.OneToOneField(
        VisibilityModel, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # keeps track who joined the contest
    # contestants have access to the problems during contest, for elo calc
    contestants = models.ManyToManyField(
        get_user_model(), related_name='contestant')

    def is_visible(self, user):
        if self.authors.filter(pk=user.pk).exists():
            return True
        return self.visibility.is_visible(user)

    def is_active(self):
        time = datetime.now().astimezone()
        return time >= self.start_time and time <= self.end_time

    def author_string(self):
        # TODO: redundant code with author_string in ProblemModel
        authors_names = [a.get_username() for a in self.authors.all()]
        authors_names.sort()
        num_of_authors = len(authors_names)
        if num_of_authors == 0:
            return 'None'
        elif num_of_authors == 1:
            return authors_names[0]
        else:
            return ', '.join(authors_names[:-1]) + ' and ' + authors_names[-1]
