def hexa2bin(hexa):
    bin=''
    listhexa=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    listbin=['0000','0001','0010','0011','0100','0101','0110','0111','1000',
        '1001','1010','1011','1100','1101','1110','1111']
    for i in range (len(hexa)):
        for j in range(16):
            if hexa[i]==listhexa[j]:
                bin+=listbin[j]
    while bin[0]=='0':
        bin=bin[1:]
    return bin
print(hexa2bin(''))
