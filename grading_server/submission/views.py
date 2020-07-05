from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import FileSubssmion

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def submissions(request):
    subs = FileSubssmion.objects.all().filter(graded = False)

    context = {
        'subs' : subs
    }
