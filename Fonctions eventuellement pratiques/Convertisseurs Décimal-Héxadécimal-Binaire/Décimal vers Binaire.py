def dec2bin(dec):
    n=0
    bin=''
    while dec>=2**n:
        n+=1
    n-=1
    while n>=0:
        if dec>=2**n:
            bin+='1'
            dec-=2**n
        else:
            bin+='0'
        n-=1
    return bin
print(dec2bin())