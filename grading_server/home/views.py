from django.shortcuts import Http404, redirect, get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from problem.models import ProblemModel
import datetime
from django.contrib.auth.models import User
from .models import UserProfile

def index(request):
    return render(request, "index.html")

def user_view(request, user_id):
    user_object = get_object_or_404(User, user_id)
    user_profile = user_object.userprofile

    context = {
        'user_profile' = user_profile,
        'user' = user_object
    }
