from django.contrib import admin
from .models import FileSubmission
# Register your models here.


@admin.register(FileSubmission)
class FileSubmissionAdmin(admin.ModelAdmin):
    """custom class to display non-editable submission_time in admin page"""
    readonly_fields = ['submission_time']
