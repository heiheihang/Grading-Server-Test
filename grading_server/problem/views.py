from django.shortcuts import render
from django.shortcuts import Http404, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponseForbidden,  HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory


from .models import ProblemModel, ProblemTestSuiteModel, ProblemTestPairModel
from .forms import ProblemModelForm, TestSuiteModelForm, TestPairModelForm

# Create your views here.


def problem_view(request, problem_id):
    problem = get_object_or_404(ProblemModel, id=problem_id)
    example_suites = ProblemTestSuiteModel.objects.filter(problem=problem)
    examples = ProblemTestPairModel.objects.filter(test_suite__in=[suite.pk for suite in example_suites])
    if request.method == 'POST':
        if(form.is_valid()):
            suite_number = len(test_suites)
            #print(suite_number)
            suite_description = form.cleaned_data['test_suite_description']
            new_suite = ProblemTestSuiteModel(problem = problem, problem_suite_number = suite_number, test_suite_description = suite_description)
            new_suite.save()
            return HttpResponseRedirect(str(suite_number + 1))

    context = {
        'problem': problem,
        'is_author': problem.authors.filter(pk=request.user.pk).exists(),
        #'form': form,
        'examples': examples,
        }
    return render(request, 'problem/problem.html', context)
    #return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def problem_edit_view(request, problem_id):
    #ProblemTestModelModelFormSet = modelformset_factory(ProblemTestModel,
    #                                                    form=ProblemTestModelForm, fields=['input', 'output', 'task_num', 'sub_task_num', 'error_message'], extra=1)
    problem = get_object_or_404(ProblemModel, id=problem_id)
    test_suites = problem.problemtestsuitemodel_set.all()
    if not problem.authors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()
    if request.method == 'GET':
        #tests = ProblemTestModel.objects.all().filter(parent__id=problem_id).distinct()
        #form_set = ProblemTestModelModelFormSet(initial=tests, prefix='tests')
        test_suites = problem.problemtestsuitemodel_set.all()
        add_suite_form = TestSuiteModelForm()
        
        return render(request, 'problem/edit.html', {'problem': ProblemModelForm(instance=problem, prefix='main'), 
            'suites': test_suites,
            'add_suite_form': add_suite_form})
    if request.method == 'POST':
        form = ProblemModelForm(request.POST or None, request.FILES or None,
                                prefix='main', instance=problem)
        test_suites = problem.problemtestsuitemodel_set.all()
        add_suite_form = TestSuiteModelForm()
        #form_set = ProblemTestModelModelFormSet(
        #    request.POST or None, request.FILES or None, prefix='tests')
        if form.is_valid():
            form.save()
            print('OK')
            # TODO: somehow output telling user form has been saved
        #if form_set.is_valid():
        #    form_set.save(commit=False)
        #    clean_data = form_set.cleaned_data
        #    print(form_set)
        #    print(clean_data)
        #    for f in form_set:
        #        print(f.fields['task_num'])
        #        f.fields['parent'] = problem
        #    form_set.save()
        #    print('formset OK')
        else:
            print(form_set.errors)
            #clean_data = form_set.cleaned_data
            #form_set = ProblemTestModelModelFormSet(initial=clean_data)
        return render(request, 'problem/edit.html', {'problem': form,
            'suites': test_suites,
            'add_suite_form': add_suite_form})
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
def test_suite_detail_view(request, problem_id, suite_id):
    test_suite = get_object_or_404(ProblemTestSuiteModel, problem_suite_number=suite_id, problem__id=problem_id)
    problem = test_suite.problem
    if not problem.authors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()
    pairs = test_suite.problemtestpairmodel_set.all()
    print(test_suite)
    test_pairs = ProblemTestPairModel.objects.filter(test_suite=test_suite.pk)
    if request.method == 'POST':
        form = TestPairModelForm(request.POST, request.FILES)
        if(form.is_valid()):
            pair_number = len(pairs)
            print(suite_id)
            input_file = form.cleaned_data['input_file']
            output_file = form.cleaned_data['output_file']
            new_suite = ProblemTestPairModel(test_suite = test_suite, pair_number = pair_number, input = input_file, output = output_file)
            new_suite.save()
            return HttpResponseRedirect('/problem/' + str(problem_id))
    else:
        form = TestPairModelForm()
    context = {
        'test_suite' : test_suite,
        'problem' : problem,
        'test_pairs': test_pairs,
        'form' : form
    }
    return render(request, 'problem/test_suite_detail.html', context)

@login_required
def test_suite_create_view(request, problem_id):
    problem = get_object_or_404(ProblemModel, id=problem_id)
    if not problem.authors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()
    test_suites = ProblemTestSuiteModel.objects.filter(problem=problem)
    print(test_suites)
    test_suites_numbers = [suite.problem_suite_number for suite in test_suites]
    test_suites_numbers.sort()
    new_suite_number = test_suites_numbers[-1] + 1
    new_suite = ProblemTestSuiteModel(problem=problem, problem_suite_number=new_suite_number, test_suite_description='')
    print(new_suite)
    new_suite.save()
    return redirect(test_suite_detail_view, problem_id, new_suite_number)

@login_required
def test_suite_delete_view(request, problem_id, suite_id):
    test_suite = get_object_or_404(ProblemTestSuiteModel, problem_suite_number=suite_id, problem__id=problem_id)
    if not test_suite.problem.authors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()
    test_suite.delete()
    return redirect(problem_edit_view, problem_id)

@login_required
def test_pair_create_view(request, problem_id, suite_id):
    test_suite = get_object_or_404(ProblemTestSuiteModel, problem_suite_number=suite_id, problem__id=problem_id)
    if not test_suite.problem.authors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TestPairModelForm(request.POST or None, request.FILES or None)
        if not form.is_valid():
            return redirect(test_suite_detail_view, problem_id, suite_id)
        input_file = form.cleaned_data['input_file']
        output_file = form.cleaned_data['output_file']

        test_pairs = ProblemTestPairModel.objects.filter(test_suite=test_suite)
        test_pair_numbers = [suite.pair_number for suite in test_pairs]
        test_pair_numbers.sort()
        pair_number = test_pair_numbers[-1] + 1

        new_test_pair = ProblemTestPairModel(test_suite=test_suite, pair_number=pair_number, input=input_file, output=output_file)
        new_test_pair.save()
        return redirect(test_suite_detail_view, problem_id, suite_id)
    return HttpResponseNotAllowed(['POST'])


@login_required
def test_pair_delete_view(request, problem_id, suite_id, pair_id):
    test_pair = get_object_or_404(ProblemTestPairModel, pair_number=pair_id, test_suite__problem_suite_number=suite_id, test_suite__problem__id=problem_id)
    if not test_pair.test_suite.problem.authors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden()
    test_pair.delete()
    return redirect(test_suite_detail_view, problem_id, suite_id)
