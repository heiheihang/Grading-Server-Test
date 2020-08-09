from django.shortcuts import Http404, redirect, get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect
from .models import FileSubmission
from .forms import FileSubmissionForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from problem.models import ProblemModel
import datetime

from .process_job import process_job

from . import my_lib


@login_required
def submission_view(request, problem_id):
    problem = get_object_or_404(ProblemModel, id=problem_id)
    user = request.user
    #print(request.user)
    if request.method == 'POST':
        form = FileSubmissionForm(request.POST, request.FILES)
        if form.is_valid():

            #input file handling---------------------------------------------------
            file = form.cleaned_data['file']
            # fs = FileSystemStorage()
            # time = my_lib.roundSeconds(datetime.datetime.now())
            # t = str(time.year) + '-' + str(time.month) + '-' + str(time.day) + '-' + str(time.hour) + '-' + str(time.minute) + '-' + str(time.second)
            # user_id = request.user.id
            # s = str(user_id) + '/' + str(problem_id) + "_" + str(t) + "_" + str(user_id)+".py"
            # filename = fs.save(s,file)    #file name is "problemID_Time_UserID.py"
            # print(s)
            #FileSubssmion fields information---------------------------------------
            lang = form.cleaned_data['lang']
            submission_time = my_lib.roundSeconds(datetime.datetime.now())

            graded = False

            current_submission = FileSubmission(
                file = file,
                submission_time = submission_time,
                user = user,
                graded = graded,
                problem = problem
            )
            #print(current_submission)
            current_submission.save()
            process_job(current_submission.pk)

            return HttpResponseRedirect('/submission/')
    else:
        form = FileSubmissionForm()

    previous_submissions = FileSubmission.objects.all().filter(user = user, problem = problem).order_by('-submission_time')
    if(len(previous_submissions) > 10):
        previous_submissions = previous_submissions[:10]
    for x in previous_submissions:
        my_lib.parse_report(x)
    context = {
        'form' : form,
        'problem': problem,
        'previous_submissions' : previous_submissions
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
    subs = FileSubmission.objects.all().filter(graded=False)
    a = subs[0].file.read()
    #exec(a)
    time = my_lib.roundSeconds(datetime.datetime.now())
    time = datetime.datetime.now()
    print(time)
    t = str(time.year) + '-' + str(time.month) + '-' + str(time.day) + '-' + str(time.hour) + '-' + str(time.minute) + '-' + str(time.second)
    print(t)

    context = {
        'subs': subs
    }

    return render(request, 'submission/subs.html', context=context)
