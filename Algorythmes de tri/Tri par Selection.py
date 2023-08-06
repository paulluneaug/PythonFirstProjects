def test_croissance(liste):
    for i in range(len(liste)-1):
        if liste[i]>liste[i+1]:
            return False
    return True


def tri_selection(liste):
    t=0
    while test_croissance(liste)==False:
        x=len(liste)-1
        for i in range(t,x):
            if liste[x]>liste[i]:
                x=i
        if x!=t:
            liste[t],liste[x]=liste[x],liste[t]
        t=t+1
    return liste,t

print(tri_selection([1,9,54654,-58,1,98,23,0,19,1.254,198,-36,-7821]))
