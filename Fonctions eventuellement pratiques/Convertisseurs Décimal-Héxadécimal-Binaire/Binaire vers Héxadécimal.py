def bin2hexa(bin):
    bin=str(bin)
    hexa=''
    listhexa=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    listbin=['0000','0001','0010','0011','0100','0101','0110','0111','1000',
        '1001','1010','1011','1100','1101','1110','1111']
    while len(bin)%4!=0:
        bin='0'+bin
    for i in range(len(bin)//4):
        for j in range(16):
            if bin[4*i:4*i+4]==listbin[j]:
                hexa+=listhexa[j]
    return hexa
print(bin2hexa())