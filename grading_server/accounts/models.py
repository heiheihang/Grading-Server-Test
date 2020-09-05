from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# reference: https://studygyaan.com/django/how-to-signup-user-and-send-confirmation-email-in-django
class EmailVerify(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verify')
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        EmailVerify.objects.create(user=instance)
        instance.email_verify.save()