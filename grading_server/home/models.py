from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    elo = models.IntegerField()
    profile_picture = models.ImageField(upload_to = 'users_profile_pic')

    def get_absolute_url(self):
        return reverse('user_view', args=[str(self.user.id)])
