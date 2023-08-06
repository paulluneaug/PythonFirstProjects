def pgcd_euclide(a,b):
    """
    Renvoie le plus grand diviseur commun de a et b en utilisant la méthode
    d'Euclide
    """
    if a<b:
        a,b=b,a
    if b==0:
        return a
    else:
        return pgcd_euclide(a%b,b)
    
def euclide(a,b):
    """
    Renvoie le plus grand diviseur commun de a et b en utilisant la méthode
    d'Euclide et affiche dans la console les différentes étapes de cet 
    algorithme
    """
    if a<b:
        a,b=b,a
    while a%b!=0:
        print(f'{a}={b}*{a//b}+{a%b}')
        a,b=b,a%b
    
    print(f'{a}={b}*{a//b}+{a%b}')
    return b

print(euclide(14,5))