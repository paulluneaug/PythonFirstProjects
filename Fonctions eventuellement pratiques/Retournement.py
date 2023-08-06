def retourne_str(e):
    """
    Retourne l'élément inversé en argument : le premier terme devient
    le dernier, ect...

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        liste : type = str or int or float
            Elément qu'il faut retourner

    Returns:
    ¯¯¯¯¯¯¯
        liste_ret : type = str
            Chaîne retournée
    """
    e=str(e)
    str_ret=''
    for i in range (len(e)):
        str_ret+=e[-(i+1)]
    return str_ret


def retourne_list(liste):
    """
    Retourne la liste inversée en argument : le premier terme devient
    le dernier, ect...

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        liste : type=list or tuple
            Liste qu'il faut retourner

    Returns:
    ¯¯¯¯¯¯¯
        liste_ret : type = list
            Liste retournée

    """
    liste_ret=[]
    for i in range(len(liste)):
        liste_ret.append(liste[-(i+1)])
    return liste_ret
