from django.forms import ModelForm, HiddenInput
from django import forms
from .models import ContestModel
from django.contrib.auth import get_user_model
#from django.utils.translation import ugettext_lazy as _

from datetime import datetime


class ContestForm(forms.ModelForm):
    class Meta:
        model = ContestModel
        fields = ['name', 'authors', 'start_time', 'end_time']
        widgets = {
            # TODO: investigate using flatpickr.js
            # reference: https://stackoverflow.com/questions/60128838/django-datetimeinput-type-datetime-local-not-saving-to-database
            'start_time': forms.DateTimeInput(attrs={'type': 'select', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time > end_time:
            msg = "contest end time must be later than start time."
            self.add_error('start_time', msg)
            self.add_error('end_time', msg)


class ContestCreateForm(forms.ModelForm):
    class Meta:
        model = ContestModel
        fields = ['name', 'start_time', 'end_time']
