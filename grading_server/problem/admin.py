from django.contrib import admin
from .models import ProblemModel, ProblemTestModel,ProblemTestSuiteModel, ProblemTestPairModel

# Register your models here.
admin.site.register(ProblemModel)
admin.site.register(ProblemTestModel)
admin.site.register(ProblemTestSuiteModel)
admin.site.register(ProblemTestPairModel)
