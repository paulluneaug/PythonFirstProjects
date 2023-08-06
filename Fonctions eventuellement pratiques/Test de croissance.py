def test_croissance(liste):
    """
    Teste si la liste en argument est triée par ordre croissant

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        liste : type=list
            Liste dont il faut verifier la croissance

    Returns:
    ¯¯¯¯¯¯¯
        tf : type=bool
            True si la liste est triée par ordre croissant, False sinon

    """
    tf=True
    for i in range(len(liste)-1):
        if liste[i]>liste[i+1]:
            tf=False
    return tf

def test_decroissance(liste):
    """
    Teste si la liste en argument est triée par ordre décroissant

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        liste : type=list
            Liste dont il faut verifier la décroissance

    Returns:
    ¯¯¯¯¯¯¯
        tf : type=bool
            True si la liste est triée par ordre décroissant, False sinon

    """
    tf=True
    for i in range(len(liste)-1):
        if liste[i]<liste[i+1]:
            tf=False
    return tf


