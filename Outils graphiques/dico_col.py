#A servi à fabriquer les dictionnaires des palettes de couleur


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
    while len(hexa)<2:
        hexa='0'+hexa
    return hexa



list_col_m=['#000000','#993300','#333300','#003300','#003366','#000080','#333399','#333333',
          '#800000','#FF6600','#808000','#008000','#008080','#0000FF','#666699','#808080',
          '#FF0000','#FF9900','#99CC00','#339966','#33CCCC','#3366FF','#800080','#969696',
          '#FF00FF','#FFCC00','#FFFF00','#00FF00','#00FFFF','#00CCFF','#993366','#C0C0C0',
          '#FF99CC','#FFCC99','#FFFF99','#CCFFCC','#CCFFFF','#99CCFF','#CC99FF','#FFFFFF']

list_col=['#'+'00'+dec2hexa(round(a*256/20))+dec2hexa(round(a*256/20)) for a in range(20)]
for e in ['#'+dec2hexa(round(a*256/20))+'FF'+'FF' for a in range(20)]:
    list_col.append(e)



dico_col_main={}
for x in range(8):
    for y in range(5):
        dico_col_main[x,y]=list_col[x+y*8]
dico_col_main=str(dico_col_main)

listeuh=[]
for l in dico_col_main:
    listeuh.append(l)
dico_col_main=listeuh
while ' ' in dico_col_main:
    for i in range(len(dico_col_main)):
        if dico_col_main[i]==' ':
            dico_col_main.pop(i)
            break

chain=''
for le in dico_col_main:
    chain=chain+le
print(chain)