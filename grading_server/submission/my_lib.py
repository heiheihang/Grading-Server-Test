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

        if(line[0] == '='):

            if(start > 0 and start < 3):
                comment += " OK "+ '\n'
            elif(start > 2):
                comment += " WRONG"  + '\n'
            start = 1
            comment += line
            #print(line)
        elif(start == 1):
            #print("test " + line)
            comment += "test " + line
            start += 1
        elif(start > 1 and start < 5):
            start += 1
        elif(start == 5):
            #print("Expecting:" + line)
            comment += "Expecting:" + line
            start += 1
        elif(start == 6):
            #print("Received:" + line)
            comment += "Received:" + line
    print(comment)
    s.feedback = comment
    s.save()
    return
