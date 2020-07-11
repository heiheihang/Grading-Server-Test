from django.contrib import admin
from .models import ProblemModel, ProblemTestModel

# Register your models here.
admin.site.register(ProblemModel)
admin.site.register(ProblemTestModel)
