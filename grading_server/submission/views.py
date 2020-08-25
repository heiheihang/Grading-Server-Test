from django.shortcuts import Http404, redirect, get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import FileSubmission
from .forms import FileSubmissionForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from problem.models import ProblemModel
from contest.models import ContestModel
import datetime

from .process_job import process_job

from . import my_lib

import django_rq

@login_required
def submission_view(request, problem_id):
    problem = get_object_or_404(ProblemModel, id=problem_id)
    user = request.user
    if not problem.is_visible(user):
        return HttpResponseForbidden()
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

            contests = [c for c in problem.contests.all() if c.contestants.filter(pk=request.user.pk)]
            contests = [c for c in contests if c.is_active()]
            if len(contests) == 0:
                contest = None
            elif len(contests) == 1:
                contest = contests[0]
            else:
                # errrr...?
                contest = contests[0]

            current_submission = FileSubmission(
                file = file,
                submission_time = submission_time,
                user = user,
                graded = graded,
                problem = problem,
                contest = contest
            )
            #print(current_submission)
            current_submission.save()
            django_rq.enqueue(process_job, current_submission.pk)
            #process_job(current_submission.pk)

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
    problems = [p for p in problems if p.is_visible(request.user)]
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
