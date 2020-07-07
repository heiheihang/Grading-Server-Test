from django.contrib import admin
from .models import FileSubssmion
# Register your models here.


@admin.register(FileSubssmion)
class FileSubssmionAdmin(admin.ModelAdmin):
    """custom class to display non-editable submission_time in admin page"""
    readonly_fields = ['submission_time']
