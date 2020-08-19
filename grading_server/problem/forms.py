#from django.forms import ValidationError
#from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, HiddenInput
from django import forms

from .models import ProblemModel


class ProblemModelForm(ModelForm):
    class Meta:
        model = ProblemModel
        fields = ['name', 'problem_statement']


class TestSuiteModelForm(forms.Form):
    suite_number = forms.IntegerField()
    description = forms.CharField(max_length = 500)

class TestPairModelForm(forms.Form):
    input_file = forms.FileField()
    output_file = forms.FileField()
