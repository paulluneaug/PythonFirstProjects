from math import sqrt

file_insert=open('Quelques nombres premiers.txt','w')

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


st=''
for a in crible_eratosthene(444):
    st+=' '+str(a)
file_insert.write(st)
file_insert.close()

