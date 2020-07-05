def inp():
    return(int(input()))

def inlt():
    return(list(map(int,input().split())))

def insr():
    s = input()
    return(list(s[:len(s)]))

def s_to_int(a):
    for i in range(len(a)):
        a[i] = int(a[i])

def factors(n):
    res = []
    t = 1
    while(t*t <= n):
        if(t*t == n):
            res.append(t)
        if(n%t==0):
            res.append(t)
            res.append(n//t)
        t += 1
    res.sort()
    return res

def compact_factors(n):
    res = []

    t = 2
    while(t * t <= n):
        cnt = 0
        while(n%t == 0):
            cnt += 1
            n //= t
        if(cnt != 0):
            res.append([t,cnt])
        t += 1

    return res

def binary_search(l, target, lp, rp):
    mid = (lp+rp)//2

    if(l[mid] == target):
        return mid
    elif(l[mid] > target) :
        binary_search(l,target, lp, mid - 1)

    elif(l[mid] < target):
        binary_search(l, target, mid + 1, rp)
        
    elif(lp >= rp):
        return -1


n = inp()
print(n)