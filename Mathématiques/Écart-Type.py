from math import sqrt
def Espérance (valeur_x,proba_px):
    E=0
    if len(valeur_x)!=len(proba_px):
        return "Valeurs impossibles"
    for i in range (len(valeur_x)):
        E=E+(valeur_x[i]*proba_px[i])
    return E

def Variance(valeur_x,proba_px):
    e=Espérance(valeur_x,proba_px)
    v=0
    for i in range (len(proba_px)):
        v=v+proba_px[i]*(valeur_x[i]-e)**2
    return v

def Ecart_Type(valeur_x,proba_px):
    e_t=sqrt(Variance(valeur_x,proba_px))
    return e_t

print(Espérance([0,1,2],[7/15,7/15,1/15]))