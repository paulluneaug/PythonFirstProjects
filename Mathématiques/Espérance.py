def Espérance (valeur_x,proba_px):
    E=0
    if len(valeur_x)!=len(proba_px):
        return "Valeurs impossibles"
    for i in range (len(valeur_x)):
        E=E+(valeur_x[i]*proba_px[i])
    return E
print(Espérance([4,6,8,9,11,14],[0.0625,0.25,0.25,0.125,0.25,0.0625]))