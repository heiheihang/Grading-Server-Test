from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from .models import FileSubssmion
from .forms import FileSubssmionForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    print(request.user)
    if request.method == 'POST':
        form = FileSubssmionForm(
            request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return HttpResponseRedirect('/')
    else:
        form = FileSubssmionForm()
    args = {}
    args['form'] = form
    return render(request, 'submission/index.html', args)


def submissions(request):
    subs = FileSubssmion.objects.all().filter(graded=False)
    a = subs[0].file.read()
    exec(a)

    context = {
        'subs': subs
    }

    return render(request, 'submission/subs.html', context=context)
