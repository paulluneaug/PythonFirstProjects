def hexa2dec (hexa):
    """
    Convertit une valeure hexadécimale en décimal

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        hexa type=str ou int
            Valeu en héxadécimal à convertir
    """
    dec=0
    listhexa=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    for i in range (len(hexa)):
        for j in range (len(listhexa)):
            if hexa[(len(hexa)-1)-i]==listhexa[j]:
                dec+=j*16**i
    return dec

print(hexa2dec(''))