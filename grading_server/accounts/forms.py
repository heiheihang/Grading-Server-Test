from django.forms import Form, CharField, PasswordInput, EmailField, ValidationError, RegexField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class LoginForm(Form):
    username = CharField(label='username / email',
                         max_length=200, required=True)
    password = CharField(
        label='password', widget=PasswordInput(), required=True)


class RegisterForm(Form):
    username = RegexField("^[0-9A-Za-z_]+$", label='username', min_length=6,
                          max_length=100, required=True, error_messages={'invalid': 'username should only contain [0-9A-Za-z_]'})
    email = EmailField(label='email')
    password = CharField(label='password', min_length=6,
                         widget=PasswordInput(), required=True)
    password_again = CharField(label='confirm password', min_length=6,
                               widget=PasswordInput(), required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            match = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(_('This username is already in use.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValidationError(_('This email address is already in use.'))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')
        if password != password_again:
            raise ValidationError(_(
                'password confirmation does not match password'))
