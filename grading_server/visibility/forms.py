from django.forms import ModelForm, HiddenInput
from django import forms
from .models import VISIBILITY_TYPES, VisibilityModel
from django.utils.translation import ugettext_lazy as _

# class VisibilityForm(forms.Form):
#    mode = forms.ChoiceField(choices=VISIBILITY_TYPES,
#                             widget=forms.RadioSelect())
#    release_time = forms.DateTimeField(required=False)
#    whitelist = forms.MultipleChoiceField(choices=get_user_model())

class VisibilityForm(forms.ModelForm):
    class Meta:
        model = VisibilityModel
        fields = ['mode', 'release_time', 'whitelist']
        labels = {'mode': _('Visibility')}
