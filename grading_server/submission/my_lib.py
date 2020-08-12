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
    user_in = []
    expect = []
    cont = 0
    for line in f:
        #print(line)
        if(line[0] == '='):
            for x in range(min(len(expect),len(user_in))):
                comment += "Your Output: " + user_in[x]
                comment += "Expected: " + expect[x]
            user_in = []
            expect = []
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
        elif( line[0] == '-'):
            #print("Expecting:" + line)
            #comment += "Expecting:" + line
            user_in.append(line[0:])
            #start += 1
        elif(line[0] == '+'):
            #print("Received:" + line)
            #comment += "Received:" + line
            expect.append(line[0:])
            #start -= 1
        elif(len(line) > 3 and cont == 0):
            print(list(line))
            if(line[2] == 'F' and line[3] == 'i'):
                comment += (line)
                cont = 3
        elif(cont > 0):
            print(list(line))
            comment += (line)
            cont -= 1

    print(comment)
    s.feedback = comment
    s.save()
    return
