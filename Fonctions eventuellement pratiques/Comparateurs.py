def smaller(a,b):
    """
    Fonction qui renvoie le plus petit élément entre a et b

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        a : type=int or float
        b : type=int or float

    Returns:
    ¯¯¯¯¯¯¯
        small : type=int or float
            Le plus petit élément entre a et b

    """
    if a>b:
        return b
    else:
        return a

def greater(a,b):
    """
    Fonction qui renvoie le plus grand élément entre a et b

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        a : type=int or float
        b : type=int or float

    Returns:
    ¯¯¯¯¯¯¯
        great : type=int or float
            Le plus grand élément entre a et b

    """
    if a<b:
        return b
    else:
        return a
