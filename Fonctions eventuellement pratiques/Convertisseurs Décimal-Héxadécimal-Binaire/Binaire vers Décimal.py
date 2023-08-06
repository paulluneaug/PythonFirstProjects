def bin2dec(bin):
    bin=str(bin)
    dec=0
    for i in range(len(bin)):
        dec+=(int(bin[(len(bin)-1)-i])*(2**i))
    return dec

print(bin2dec(1111))