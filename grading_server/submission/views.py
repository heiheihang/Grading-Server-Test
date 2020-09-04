from django.shortcuts import Http404, redirect, get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed
from .models import FileSubmission
from .forms import FileSubmissionForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from problem.models import ProblemModel
from contest.models import ContestModel

from .process_job import process_job
from . import my_lib

from datetime import datetime
import django_rq


@login_required
def submission_view(request, problem_id):
    """submission page
    GET: serves webpage for user to submit a submission to a problem
    POST: handles submission - check basic validity,
        fill in implicit values (submit time, if is part of contest),
        save to database,
        and queue job to test submission
    """
    problem = get_object_or_404(ProblemModel, id=problem_id)
    user = request.user
    if not problem.is_visible(user):
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = FileSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            lang = form.cleaned_data['lang']
            submission_time = my_lib.roundSeconds(datetime.now())
            graded = False

            # find out if this submission is part of a contest
            # list of all active contests the submitter is contestant of
            contests = [c for c in problem.contests.all() if c.contestants.filter(pk=request.user.pk)]
            contests = [c for c in contests if c.is_active()]
            if len(contests) == 0:
                contest = None
            elif len(contests) == 1:
                contest = contests[0]
            else:
                # TODO: errrr...?
                # submitter is part of 2 active contests that have the same problem... wut
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
            current_submission.during_contest()
            #current_submission.check_contest()
            current_submission.save()

            django_rq.enqueue(process_job, current_submission.pk)
            #process_job(current_submission.pk)

            return HttpResponseRedirect('/submission/')
    elif request.method == 'GET':
        form = FileSubmissionForm()

        # list of previous submissions user made to the same problem
        previous_submissions = FileSubmission.objects.all().filter(user = user, problem = problem).order_by('-submission_time')
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 0
        # TODO: constant or configurable?
        SUBMISSIONS_PER_PAGE = 3
        previous_submissions = previous_submissions[page_num * SUBMISSIONS_PER_PAGE:(page_num + 1) * SUBMISSIONS_PER_PAGE]
        
        for x in previous_submissions:
            my_lib.parse_report(x)
        context = {
            'form' : form,
            'problem': problem,
            'previous_submissions' : previous_submissions
        }
        return render(request, 'submission/submission_view.html', context)
    return HttpResponseNotAllowed(['GET', 'POST'])

def problem_submission_index(request):
    """list of problems user can submit to,
    and link to submission page of those problems.
    accessed by clicking on the "submission" link on navbar"""
    problems = ProblemModel.objects.all()
    problems = [p for p in problems if p.is_visible(request.user)]

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 0
    # TODO: constant or configurable?
    PROBLEMS_PER_PAGE = 10
    problems = problems[page_num * PROBLEMS_PER_PAGE:(page_num + 1) * PROBLEMS_PER_PAGE]
    
    context = {
        'problems' : problems
    }
    return render(request, 'submission/submission_index.html', context)

def submissions(request):
    # what does this view do again?
    subs = FileSubmission.objects.all().filter(graded=False)
    a = subs[0].file.read()
    #exec(a)
    time = my_lib.roundSeconds(datetime.now())
    time = datetime.now()
    print(time)
    t = '{:%Y-%m-%d-%H-%M-%S}'.format(time)
    print(t)

    context = {
        'subs': subs
    }
    return render(request, 'submission/subs.html', context=context)
