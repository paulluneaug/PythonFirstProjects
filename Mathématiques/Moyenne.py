def average(liste):
    """
    Renvoie la moyenne des éléments d'une liste
    Arguments:
    ¯¯¯¯¯¯¯¯¯
        liste type=list
            Liste d'entiers ou de flottants

    Return:
    ¯¯¯¯¯¯
        moy : type=int ou float
            Moyenne des valeurs de la liste

    """
    som=0
    for indice in range(len(liste)):
        som+=liste[indice]
    moy=som/len(liste)
    return moy