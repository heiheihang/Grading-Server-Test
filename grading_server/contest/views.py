from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseNotAllowed, HttpResponseForbidden,  HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from datetime import datetime, timezone

from .models import ContestModel
from problem.models import ProblemModel
from .forms import ContestForm, ContestCreateForm
from visibility.forms import VisibilityForm


def contest_index_view(request):
    if request.method == 'GET':
        contests = ContestModel.objects.all()
        contests = [c for c in contests if c.is_visible(request.user)]
        if(len(contests) > 10):
            contests = contests[:10]
        return render(request, 'contest/index.html', {'contests': contests})
    return HttpResponseNotAllowed(['GET'])


@login_required
def contest_create_view(request):
    if request.method == 'GET':
        form = ContestCreateForm(request.GET or None)
        return render(request, 'contest/create.html', {'form': form})
    if request.method == 'POST':
        form = ContestCreateForm(request.POST or None)
        if form.is_valid():
            # TODO: better way of doing this?
            contest = ContestModel()
            contest.name = form.cleaned_data['name']
            contest.start_time = form.cleaned_data['start_time']
            contest.end_time = form.cleaned_data['end_time']
            new_visibility = VisibilityModel(mode='PRIV')
            new_visibility.save()
            contest.visibility = new_visibility
            contest.save()
            contest.authors.add(request.user)
            contest.save()
            contest_id = contest.id
            print(contest_id)
            return redirect('/contest/'+str(contest_id)+'/')
        return render(request, 'contest/create.html', {'form': form})
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def contest_detail_view(request, contest_id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    contest = get_object_or_404(ContestModel, id=contest_id)
    if not contest.is_visible(request.user):
        return HttpResponseForbidden()
    problems = [p for p in ProblemModel.objects.all() if p.contests.filter(
        pk=contest.pk).exists()]
    if contest.authors.filter(pk=request.user.pk).exists():
        return render(request, 'contest/contest.html', {'contest': contest, 'problems': problems, 'is_author': True})
    # contestants cannot enter a contest page until contest has started
    registered = contest.contestants.filter(pk=request.user.pk).exists()
    current_time = datetime.now().astimezone()
    if not registered and current_time < contest.end_time:
        return redirect(contest_register_view, contest_id)

    if registered and current_time < contest.start_time:
        return render(request, 'contest/wait.html',
                      {'contest': contest, 'start_time': contest.start_time, 'now': datetime.now().astimezone()})

    return render(request, 'contest/contest.html', {'problems': problems, 'problems': problems})


@login_required
def contest_edit_view(request, contest_id):
    contest = get_object_or_404(ContestModel, id=contest_id)
    if not contest.authors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()
    if request.method == 'GET':
        contest_form = ContestForm(instance=contest, prefix='main')
        # we need the whitelist thing, because we can't
        # call function with arguemnt (ie use .filter(pk=#).exists()) in templates
        return render(request, 'contest/edit.html', {'contest_form': contest_form, 'visibility': contest.visibility, 'whitelist': [u.pk for u in contest.visibility.whitelist.all()]})
    elif request.method == 'POST':
        contest_form = ContestForm(
            request.POST or None, instance=contest, prefix='main')
        visibility_form = VisibilityForm(
            request.POST or None, instance=contest.visibility, prefix='vis')
        if contest_form.is_valid():
            contest_form.save()
        if visibility_form.is_valid():
            visibility_form.save()
        return render(request, 'contest/edit.html', {'contest_form': contest_form, 'visibility': contest.visibility, 'whitelist': [u.pk for u in contest.visibility.whitelist.all()]})
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def contest_register_view(request, contest_id):
    contest = get_object_or_404(ContestModel, id=contest_id)
    if not contest.is_visible(request.user):
        return HttpResponseForbidden()
    if request.method == 'GET':
        return render(request, 'contest/register.html', {'contest': contest})
    elif request.method == 'POST':
        contest.contestants.add(request.user)
        return redirect(contest_detail_view, contest_id)
    return HttpResponseNotAllowed(['GET', 'POST'])
