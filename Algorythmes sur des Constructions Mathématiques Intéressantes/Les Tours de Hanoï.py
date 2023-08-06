from copy import deepcopy
def searchx(lp,x):
    for i in range (len(lp)):
        for j in range (len(lp[i])):
            if lp[i][j]==x:
                return i

def ToursHanoi(stage):
    p1=[x for x in range (1,stage+1)]
    p2=[]
    p3=[]
    lp=[p1,p2,p3]
    lpstr=['P1','P2','P3']
    actOut=[]
    actIn=[]
    ring=[]
    for n in range (1,stage+1):
        ring+=list((n,))+ring
    if stage%2==0:
        pair=-1
    else:
        pair=1
    for x in ring:
        sx=searchx(lp,x)
        lp[sx].remove(x)
        actOut.append(lpstr[sx])
        if x%2==0:
            sx+=pair
        else:
            sx-=pair
        if sx<0:
            sx=2
        elif sx>2:
            sx=0
        lp[sx].reverse()
        lp[sx].append(x)
        lp[sx].reverse()
        actIn.append(lpstr[sx])
        printstate(stage,lp)
        #a=input()
    for k in range (len(ring)):
        print(ring[k],' | ',actOut[k],' | ',actIn[k])

def printstate(stage,lp):
    for i in range (len(lp)):
        lp[i].reverse()
        for b in range((stage)-len(lp[i])):
            lp[i].append(0)
        lp[i].reverse()

    for s in range (stage):
        for l in range (3):
            if lp[l][s]==0:
                print(stage*' ',lp[l][s],stage*' ',sep='',end='')
            else:
                print((stage-lp[l][s]+1-len(str(lp[l][s])))*' ',lp[l][s],
                    (2*lp[l][s]-1)*'-',(stage-lp[l][s]+1)*' ',sep='',end='')
            print(' ',end='')
        print('')
    for i in range(3):
        print((2*stage+1)*'=',end=' ')
    print('')

    for l in lp:
        while 0 in l:
            l.remove(0)
ToursHanoi(5)