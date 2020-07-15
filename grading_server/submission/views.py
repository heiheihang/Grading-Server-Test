from django.shortcuts import Http404, redirect, get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect
from .models import FileSubmission
from .forms import FileSubmissionForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from problem.models import ProblemModel
import datetime

from . import my_lib


@login_required
def submission_view(request, problem_id):
    problem = get_object_or_404(ProblemModel, id=problem_id)
    print(request.user)
    if request.method == 'POST':
        form = FileSubmissionForm(request.POST)
        if form.is_valid():

            #input file handling---------------------------------------------------
            file = form.cleaned_data['file']
            fs = FileSystemStorage()
            time = roundSeconds(datetime.datetime.now())
            user_id = request.User.id
            s = str(problem_id) + "_" + str(time) + "_" + str(user_id )
            filename = fs.save(s,file)    #file name is "problemID_Time_UserID.py"

            #FileSubssmion fields information---------------------------------------
            lang = form.cleaned_data['lang']
            submission_time = time
            user = request.User
            graded = False

            current_submission = FileSubssmion(
            file = file,
            submission_time = submission_time,
            user = user,
            graded = graded,
            problem = problem)
            current_submission.save()
            return HttpResponseRedirect('/')
    else:
        form = FileSubmissionForm()
    context = {
        'form' : form
    }

    return render(request, 'submission/submission_view.html', context)

def problem_submission_index(request):
    problems = ProblemModel.objects.all()
    if(len(problems) > 100):
        problems = problems[:100]
    context = {
        'problems' : problems
    }
    return render(request, 'submission/submission_index.html', context)

def submissions(request):
    subs = FileSubssmion.objects.all().filter(graded=False)
    a = subs[0].file.read()
    exec(a)

    context = {
        'subs': subs
    }

    return render(request, 'submission/subs.html', context=context)
