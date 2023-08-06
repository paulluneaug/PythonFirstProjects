def congru(a,b,n):
    """
    Vérifie si a est congru à b mudulo n, c'est à dire si ils ont le même reste
    par la division euclidienne par n

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        a : type=int
        b : type=int
        n : type=int

    Returns:
    ¯¯¯¯¯¯¯
        tf : type=bool
            True si a est congru à b modulo n
            False sinon
    """
    return (a-b)%n==0