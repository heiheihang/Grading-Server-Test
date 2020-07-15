from .models import FileSubmission

from subprocess import check_output


def process_job(submission_pk):
    print(submission_pk)
    submission = FileSubmission.objects.get(pk=submission_pk)
    print(submission)
    file_name = submission.file.name
    print(file_name)
    print('./media/' + file_name)
    output = check_output(
        ['bash', './docker/docker.sh', 'py', './media/' + file_name, './media/problem_' + str(submission.problem.pk) + '/'])
    print(output)
