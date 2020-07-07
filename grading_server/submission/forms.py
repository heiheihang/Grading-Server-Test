from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

from .models import FileSubssmion


class FileSubssmionForm(ModelForm):
    class Meta:
        model = FileSubssmion
        fields = ['lang', 'file']

    def clean_file(self):
        """reject submitted file if file too large"""
        file = self.cleaned_data['file']
        if len(file) > 100000:
            raise ValidationError(_('File too large'), code='large-file')
        return file
