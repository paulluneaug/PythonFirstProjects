def TriangePascal(n):
    etage=[1]
    liste=[]
    for i in range(n+1):
        print(etage)
        a=len(etage)
        for p in range(len(etage)):
            if p==0 or p==a:
                liste.append(etage[p])
            else:
                liste.append(etage[p]+etage[(p-1)])
        liste.append(etage[a-1])
        etage=liste.copy()
        liste=[]
TriangePascal(9)
