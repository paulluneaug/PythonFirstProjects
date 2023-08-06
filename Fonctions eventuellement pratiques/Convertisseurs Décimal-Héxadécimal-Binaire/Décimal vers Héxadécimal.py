def dec2hexa(dec):
    dec=int(dec)
    n=0
    hexa=''
    listhexa='0123456789ABCDEF'
    while dec>=16**n:
        n+=1
    n-=1
    while n>=0:
        p=0
        for i in range(len(listhexa)):
            if dec>=i*16**n:
                p=i
        dec-=p*16**n
        hexa+=listhexa[p]
        n-=1
    return hexa

print(dec2hexa(0))