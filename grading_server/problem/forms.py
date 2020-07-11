#from django.forms import ValidationError
#from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, HiddenInput


from .models import ProblemModel, ProblemTestModel


class ProblemModelForm(ModelForm):
    class Meta:
        model = ProblemModel
        fields = ['name', 'problem_statement']


class ProblemTestModelForm(ModelForm):
    class Meta:
        model = ProblemTestModel
        fields = ['parent', 'input', 'output', 'task_num',
                  'sub_task_num', 'error_message']
        #widgets = {'parent': HiddenInput()}
