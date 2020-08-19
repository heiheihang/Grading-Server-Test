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
    visible = forms.BooleanField(required=False)
    input_file = forms.FileField()
    output_file = forms.FileField()

class TestPairModelUpdateForm(forms.Form):
    """Even if we allow updating the test file later on
    we will want to set the input/output FileField to have required=False
    but the create new test pair form (TestPairModelForm) should still require the files
    so I'm making a new form class"""
    visible = forms.BooleanField(required=False)