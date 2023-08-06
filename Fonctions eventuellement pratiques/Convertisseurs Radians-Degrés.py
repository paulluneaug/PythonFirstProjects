from math import pi

def deg2rad(deg):
    """
    Convertit un angle en degrés en radians

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        deg : type=int ou float
            mesure de l'angle à convertir en degrés

    Returns:
    ¯¯¯¯¯¯¯
        rad : type=int ou float
            mesure de l'angle converti en radians

    """
    return ((deg*2*pi)/360)



def rad2deg(rad):
    """
    Convertit un angle en radians en degrés

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        rad : type=int ou float
            mesure en radians de l'angle à convertir

    Returns:
    ¯¯¯¯¯¯¯
        deg : type=int ou float
            mesure en degrés de l'angle converti

    """
    return (360*rad/(2*pi))

