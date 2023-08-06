from math import sqrt

def decomp_fact_prem(nb):
    """
    Décompose un nombre en facteurs premiers

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        nb : type=int  1<=nb
            Nombre à décomposer en facteurs premiers

    Returns:
    ¯¯¯¯¯¯¯
        list_fact_prem : type=list
            Liste des facteurs premiers de nb
    """
    file=open('Quelques nombres premiers [0;2G].txt','r')
    list_nbr_pr=file.read()[:-1].split() #Récupère la liste des nombres premiers
    list_fact_prem=[]                    #de 0 à 2 milliards
    i=0
    while nb!=1 and i<len(list_nbr_pr):
        if nb%int(list_nbr_pr[i])==0:
            list_fact_prem.append(int(list_nbr_pr[i]))
            nb/=int(list_nbr_pr[i])
            # i=0
        else:
            i+=1
    if i>=len(list_nbr_pr): #Si le nombre n'a pas de diviseur inférieur à
        return None         #2 milliards, renvoie None
    return list_fact_prem

l=decomp_fact_prem(765235230620)
p=1
for a in l:
    p*=a
print(l,p)