from .models import FileSubmission
from datetime import timedelta
from subprocess import check_output, Popen, PIPE
from django.core.files.storage import FileSystemStorage
from hashlib import md5

def process_job(submission_pk):
    #print(submission_pk)
    submission = FileSubmission.objects.get(pk=submission_pk)
    #print(submission)
    file_name = submission.file.name
    #print(file_name)
    print('./media/' + file_name)
    name_hash = md5(file_name.encode()).hexdigest()
    time = submission.submission_time + timedelta(hours=8)
    time_s = time.strftime('%Y-%m-%d-%H-%M-%S')
    print(time)
    user_id = submission.user.id
    problem_id = submission.problem.id
    submission_id = submission.pk
    with open('./media/user_{0}/{1}_{0}_{2}_report'.format(user_id, problem_id, time_s), 'w+') as f:
        output = Popen(
            ['bash', './docker/docker.sh', 'py', './media/' + file_name, './media/problem_' + str(submission.problem.pk) + '/', name_hash], stdout=f)
        fs = FileSystemStorage()
        s = './user_{0}/{1}_{0}_{2}_report'.format(user_id, problem_id, time_s)
        filename = fs.save(s,f)
        submission.report = filename
        submission.save()
