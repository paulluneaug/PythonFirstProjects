def SuiteFibonacci(n):
    """
    Renvoie les n premiers éléments de la suite de Fibonacci

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        n : type=int  1<=n
            Nombre d'éléments de la suite que l'on souhaite récupérer

    Returns:
    ¯¯¯¯¯¯¯
        listfib : type=list
            Liste des n premiers éléments de la suite de Fibonacci
    """
    listfib=[]
    nb1=0
    nb2=1
    for i in range(n):
        listfib.append(nb2)
        nb1,nb2=nb2,nb1+nb2
    return listfib
print(SuiteFibonacci(2000))