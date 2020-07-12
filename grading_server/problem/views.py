from django.shortcuts import render
from django.shortcuts import Http404, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponseForbidden,  HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory


from .models import ProblemModel, ProblemTestModel, ProblemTestSuiteModel, ProblemTestPairModel
from .forms import ProblemModelForm, ProblemTestModelForm, TestSuiteModelForm, TestPairModelForm

# Create your views here.


def problem_view(request, problem_id):
    problem = get_object_or_404(ProblemModel, id=problem_id)
    examples = ProblemTestModel.objects.all().filter(parent=problem)
    test_suites = problem.problemtestsuitemodel_set.all()
    if request.method == 'POST':
        form = TestSuiteModelForm(request.POST)
        if(form.is_valid()):
            suite_number = len(test_suites)
            print(suite_number)
            suite_description = form.cleaned_data['test_suite_description']
            new_suite = ProblemTestSuiteModel(problem = problem, problem_suite_number = suite_number, test_suite_description = suite_description)
            new_suite.save()
            return HttpResponseRedirect('/problem')
    else:
        form = TestSuiteModelForm()

    context = {
        'problem': problem,
        'examples': examples,
        'is_author': problem.authors.filter(pk=request.user.pk).exists(),
        'form': form,
        'suites': test_suites
        }
    return render(request, 'problem/problem.html', context)
    #return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def problem_edit_view(request, problem_id):
    ProblemTestModelModelFormSet = modelformset_factory(ProblemTestModel,
                                                        form=ProblemTestModelForm, fields=['input', 'output', 'task_num', 'sub_task_num', 'error_message'], extra=1)
    problem = get_object_or_404(ProblemModel, id=problem_id)
    if not problem.authors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()
    if request.method == 'GET':
        tests = ProblemTestModel.objects.all().filter(parent__id=problem_id).distinct()
        form_set = ProblemTestModelModelFormSet(initial=tests, prefix='tests')
        return render(request, 'problem/edit.html', {'problem': ProblemModelForm(instance=problem, prefix='main'), 'tests': form_set})
    if request.method == 'POST':
        form = ProblemModelForm(request.POST or None, request.FILES or None,
                                prefix='main', instance=problem)
        form_set = ProblemTestModelModelFormSet(
            request.POST or None, request.FILES or None, prefix='tests')
        if form.is_valid():
            form.save()
            print('OK')
            # TODO: somehow output telling user form has been saved
        if form_set.is_valid():
            form_set.save(commit=False)
            clean_data = form_set.cleaned_data
            print(form_set)
            print(clean_data)
            for f in form_set:
                print(f.fields['task_num'])
                f.fields['parent'] = problem
            form_set.save()
            print('formset OK')
        else:
            print(form_set.errors)
            #clean_data = form_set.cleaned_data
            #form_set = ProblemTestModelModelFormSet(initial=clean_data)
        return render(request, 'problem/edit.html', {'problem': form, 'tests': form_set})
    return HttpResponseNotAllowed(['GET', 'POST'])


def problem_index_view(request):
    if request.method == 'GET':
        problems = ProblemModel.objects.all()
        if(len(problems) > 10):
            problems = ProblemModel.objects.all()[:10].get()
        return render(request, 'problem/index.html', {'problems': problems})
    return HttpResponseNotAllowed(['GET'])


@login_required
def problem_create_view(request):
    if request.method == 'GET':
        form = ProblemModelForm(request.GET or None)
        return render(request, 'problem/create.html', {'form': form})
    if request.method == 'POST':
        form = ProblemModelForm(request.POST or None)
        if form.is_valid():
            form = form.save()
            form.authors.add(request.user)
            form.save()
            form_id = form.id
            print(form_id)
            return redirect('/problem/'+str(form_id)+'/')
        return render(request, 'problem/create.html', {'form': form})
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def test_suite_create_view(request, problem_id, suite_id):
    if request.method == 'GET':
        form = ProblemModelForm(request.GET or None)
        return render(request, 'problem/create.html', {'form': form})
    if request.method == 'POST':
        form = ProblemModelForm(request.POST or None)
        if form.is_valid():
            form = form.save()
            form.authors.add(request.user)
            form.save()
            form_id = form.id
            print(form_id)
            return redirect('/problem/'+str(form_id)+'/')
        return render(request, 'problem/create.html', {'form': form})
    return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
def test_pair_create_view(request, problem_id, suite_id, pair_id):
    if request.method == 'GET':
        form = ProblemModelForm(request.GET or None)
        return render(request, 'problem/create.html', {'form': form})
    if request.method == 'POST':
        form = ProblemModelForm(request.POST or None)
        if form.is_valid():
            form = form.save()
            form.authors.add(request.user)
            form.save()
            form_id = form.id
            print(form_id)
            return redirect('/problem/'+str(form_id)+'/')
        return render(request, 'problem/create.html', {'form': form})
    return HttpResponseNotAllowed(['GET', 'POST'])
