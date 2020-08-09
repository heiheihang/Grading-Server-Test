import datetime

def roundSeconds(dateTimeObject):
    newDateTime = dateTimeObject

    if newDateTime.microsecond >= 500000:
        newDateTime = newDateTime + datetime.timedelta(seconds=1)

    return newDateTime.replace(microsecond=0)

#take submission, generate comment for the submission if not exists
def parse_report(s):
    print(s.submission_time)
    if(s.graded == False and s.report == None):
        return
    report = s.report
    try:
        p = report.path
    except:
        return
    print(p)
    try:
        f = open(p, 'r')
    except:
        return
    start = 0
    comment = ""
    for line in f:
        if(line[0] == '=' or start == 1):
            start = 1
            print(line)
    return
