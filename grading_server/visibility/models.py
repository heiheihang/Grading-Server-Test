from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

VISIBILITY_TYPES = [('PUB', 'Public'),
                    ('TIME', 'Timed Release'),
                    ('PRIV', 'Private List')]


class VisibilityModel(models.Model):
    # This will govern who will be able to see that a model exists
    # for example, users not in a class cannot see a in-class contest exists
    # TODO: make it easy so that a visibility can be copy-pasted (copy paste list of students)
    # TODO: make it filter-base (or whatever you call it)
    #   - currently we have either a private whitelist,
    #     xor public release at time (start of class)
    #     make it so we can have the following for example:
    #       - at start of class, memebers of private whitelist
    #         (students) can see the contest
    #       - and the course has ended (one month or something)
    #         the contest will be released (public)
    #       - in other words: (time_a AND whitelist) OR (time_b)
    mode = models.CharField(
        max_length=8, choices=VISIBILITY_TYPES, default='PRI')
    # using auto_now_add will always forced to use now(), instead of being a default value
    release_time = models.DateTimeField(default=datetime.now)
    whitelist = models.ManyToManyField(get_user_model(), blank=True)

    def is_visible(self, user):
        if self.mode == 'PUB':
            return True
        elif self.mode == 'TIME':
            if datetime.utcnow() >= self.release_time:
                return True
        elif self.mode == 'PRIV':
            pass
        else:
            # in case idk
            raise NotImplementedError
        return self.whitelist.filter(pk=user.pk).exists()
