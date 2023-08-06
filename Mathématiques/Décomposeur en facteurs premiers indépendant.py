from math import sqrt


def crible_eratosthene(n):
    """
    Renvoie la liste des nombres premiers de 1 à n en utilisant la méthode du
    crible d'Ératosthène

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        n : type=int  2<=n
            Limite superieure de l'ensemble sur lequel on recherche les nombres
            premiers

    Returns:
    ¯¯¯¯¯¯¯
        list_nb_pr : type=list
            Liste des nombres premiers de 1 à n
    """
    list_n=[a for a in range(n+1)] #On dresse la liste des entiers de 1 à n
    for i in range(2,int(sqrt(n))+1): #Pour chaque élément, on remplace tous
        if list_n[i] !=0:             #ses multiples par 0
            for j in range(1,(n-i)//list_n[i]+1):
                list_n[i+j*i]=0                 #On obtient ainsi tous les
    return [b for b in list_n[2:] if b!=0] #nombres premiers de 1 à n

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
    list_nbr_pr=crible_eratosthene(nb)
    list_fact_prem=[]
    i=0
    while nb!=1 and i<len(list_nbr_pr):
        if nb%list_nbr_pr[i]==0:
            list_fact_prem.append(list_nbr_pr[i])
            nb/=list_nbr_pr[i]
            # i=0
        else:
            i+=1
    if i>=len(list_nbr_pr): #Si le nombre n'a pas de diviseur inférieur à
        return None         #2 milliards, renvoie None
    return list_fact_prem

l=decomp_fact_prem(220561420)
p=1
for a in l:
    p*=a
print(l,p)