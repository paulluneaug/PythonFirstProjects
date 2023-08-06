def trilettres(lettres):
    liste=[]
    chain=''
    for c in lettres:
        liste+=c
    liste.sort()
    for i in liste:
        chain+=i
    print(chain)


trilettres('Console de processus distant Réinitialisée')