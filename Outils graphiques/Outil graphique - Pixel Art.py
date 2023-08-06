import tkinter as tk

def pixel_art_tool():
    """
    Ouvre une fenêtre qui permet de faire des Pixel Arts

    Contrôles:

        - Click gauche pour colorer un pixel
        - Ctrl + click gauche pour colorer un ensemble de pixels

        - Click droit pour effacer un pixel coloré
        - Ctrl + click droit pour effacer un ensemble de pixels colorés

        - Click molette pour récupérer la couleur d'un pixel coloré
    """
    global c,can,fen,entry_fill,can_test,x_can,y_can,can_fill,c_fill,but_en_dis_able_grid

    x_can,y_can=27,27 #Nombre de cases en largeur et en longueur du canevas

    c=500//greater(x_can,y_can) #Longueur en pixels du coté de chaque case
    c_fill=20 #Longueur en pixels du coté des carrés de la palette
    lab_font='Verdana 12'

    fen=tk.Tk()
    fen.title('Outil Pixel Art')

    #Canevas de test pour vérifier qu'une couleur est valide
    can_test=tk.Canvas(fen,width=1,height=1)
    can_test.grid(column=0,row=1)

    #Canevas principal
    can=tk.Canvas(fen,width=c*x_can,height=c*y_can,bg='black')
    can.grid(column=1,row=0)

    #Frame sur la droite du canevas principal avec la sélection des couleurs et
    #les boutons
    fra_right=tk.Frame(fen,width=c*x_can,height=c*y_can,bg='black')
    fra_right.grid_propagate(False)
    fra_right.grid(column=2,row=0)

    #Frame contenant la palette
    fra_fill=tk.Frame(fra_right,width=c*x_can/2,height=100,bg='black')
    fra_fill.grid(column=0,row=0,columnspan=2,padx=5,pady=5)

    lab_fill=tk.Label(fra_fill,text='Fill :',font=lab_font,bg='black',
        fg='white')
    lab_fill.grid(column=0,row=0,padx=5,pady=5)

    entry_fill=tk.Entry(fra_fill)
    entry_fill.grid(column=1,row=0,padx=5,pady=5)

    but_custom_fill=tk.Button(fra_fill,text='Choisir une couleur personalisée',
        command=lambda entry=entry_fill,eff=None:set_custom_color(entry))
    but_custom_fill.grid(column=0,columnspan=2,row=1,padx=5,pady=5)

    #Canevas de la palette
    can_fill=tk.Canvas(fra_fill,width=8*c_fill,height=5*c_fill)
    can_fill.grid(column=0,row=2,columnspan=2)

    #Bouttons pour changer de palette
    but_sub_i=tk.Button(fra_fill,text='◄',font=lab_font,command=lambda z=-1,
                        eff=None:change_i_fill(z))
    but_sub_i.grid(column=0,row=3)

    but_add_i=tk.Button(fra_fill,text='►',font=lab_font,command=lambda z=1,
                        eff=None:change_i_fill(z))
    but_add_i.grid(column=1,row=3)

    #Bouttons pour ajouter des lignes ou des colonnes
    but_add_row=tk.Button(fra_right,text='Ajouter une ligne',font='Verdanna 12',
        command=add_row)
    but_add_row.grid(column=0,row=1)

    but_add_col=tk.Button(fra_right,text='Ajouter une colonne',command=add_col,
                          font='Verdanna 12')
    but_add_col.grid(column=1,row=1)

    #Bouttons pour valider ou effacer
    but_done=tk.Button(fra_right,text='Valider',font='Verdanna 12',
        command=done)
    but_done.grid(column=0,row=2)

    but_erease=tk.Button(fra_right,text='Effacer',command=erease,
        font='Verdanna 12')
    but_erease.grid(column=1,row=2)

    but_en_dis_able_grid=tk.Button(fra_right,text='Désactiver la grille',
        command=en_dis_able_grid,font='Verdanna 12')
    but_en_dis_able_grid.grid(column=0,row=3,columnspan=2)


    init()
    grid(c*x_can,c*y_can,c)

    can.bind('<Button-1>',left_click)
    can.bind('<B1-Motion>',left_click)
    can.bind('<Button-2>',pick_color)
    can.bind('<Button-3>',right_click)
    can.bind('<B3-Motion>',right_click)

    can_fill.bind('<Button-1>',left_click_fill)

    fen.mainloop()

def grid(width,height,c):
    """
    Dessine la grille

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        width : type = int
            Largeur du canevas sur lequel dessiner la grille

        height : type = int
            Hauteur du canevas sur lequel dessiner la grille

        c : type = int
            Taille en pixels de chaque case de la grille
    """
    vx,vy=0,0
    grid_color='#464646'
    while vx<=width:
        can.create_line(vx,0,vx,height,width=0.5,fill=grid_color,tag='grid')
        vx+=c
    while vy<=height:
        can.create_line(0,vy,width,vy,width=0.5,fill=grid_color,tag='grid')
        vy+=c

def init():
    """
    Initialise les variales
    """
    global x_can,y_can,dico_state,fill_color,i_can_fill,grid_enable
    fill_color='white' #Couleur par défaut des cases coloriées
    i_can_fill=0 #Palette affichée
    update_fill_can()
    dico_state={} #Dictionnaire de toutes les cases
    for x in range(x_can):
        for y in range(y_can):
            dico_state[x,y]=None
    grid_enable=True

def left_click(event):
    """
    Colore la case sur lequel l'utilisateur.trice clique
    """
    global c,dico_state,fill_color
    update_fill_color()
    x_lc,y_lc=event.x//c,event.y//c
    if dico_state[x_lc,y_lc]!=fill_color:#Vérifie que la case n'est pas déjà de
        dico_state[x_lc,y_lc]=fill_color #la bonne couleur pour ne pas avoir à
        can_maj((x_lc,y_lc))             #actualiser le canevas si c'est inutile

def pick_color(event):
    """
    Récupère la couleur de la case sur laquelle l'utilisateur.trice clique
    """
    global entry_fill,dico_state,c
    x_p,y_p=event.x//c,event.y//c
    if dico_state[x_p,y_p]!=None:
        entry_fill.delete(0,len(entry_fill.get()))
        entry_fill.insert(0,dico_state[x_p,y_p])


def right_click(event):
    """
    Efface la case sur lequel l'utilisateur.trice clique
    """
    global c,dico_state
    x_rc,y_rc=event.x//c,event.y//c
    if dico_state[x_rc,y_rc]!=None:
        dico_state[x_rc,y_rc]=None
        can_maj((x_rc,y_rc))

def add_col():
    """
    Ajoute une colonne au canevas principal
    """
    global x_can,y_can,can,fra_bot,c,dico_state
    for a in range(y_can):
        dico_state[x_can,a]=None
    x_can+=1
    can.configure(width=c*x_can)
    can_maj('all')


def add_row():
    """
    Ajoute une ligne au canevas principal
    """
    global x_can,y_can,can,c
    for b in range(x_can):
        dico_state[b,y_can]=None
    y_can+=1
    can.configure(height=c*y_can)
    can_maj('all')

def can_maj(co):
    """
    Met à jour la canevas principal

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        co : type=tuple ou str
            "all" si il faut mettre tout le canevas à jour

            OU

            (x,y) avec x,y les coordonnées de la case qu'il faut mettre à jour
    """
    global can,dico_state,c,x_can,y_can
    if co=='all':
        can.delete(tk.ALL)
        if grid_enable:
            grid(c*x_can,c*y_can*c,c)
        for x in range(x_can):
            for y in range(y_can):
                if dico_state[x,y]!=None:
                    can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,
                        fill=dico_state[x,y],outline=dico_state[x,y],width=0,
                        tag=f'tag{x}/{y}')

    else:
        can.delete(f'tag{co[0]}/{co[1]}') #Supprime la case aux coordonnées (co[0],co[1])
        can.create_rectangle(co[0]*c,co[1]*c,(co[0]+1)*c,(co[1]+1)*c,
            fill=dico_state[co[0],co[1]],outline=dico_state[co[0],co[1]],
            width=0,tag=f'tag{co[0]}/{co[1]}') #Puis la recréé avec la bonne couleur


def set_custom_color(entry):
    """
    Ouvre une nouvelle fenêtre, composée d'un canevas et de 3 sliders pour
    sélectionner une couleur personalisée en paramétrant séparément le rouge,
    le vert et le bleu

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        entry : type=tkinter.Entry
            Entrée dans laquelle il faut mettre la couleur

    """
    global can_color,slider_b,slider_g,slider_r
    fen_color=tk.Tk()
    fen_color.title('Couleur personalisée')

    can_color=tk.Canvas(fen_color,height=300,width=300,bg='black')
    can_color.grid(column=0,row=0)

    fra_sliders=tk.Frame(fen_color,bg='black')
    fra_sliders.grid(column=0,row=1)

    slider_r=tk.Scale(fra_sliders,from_=255,to=0,bg='black',
        activebackground='black',fg='red',font='verdana 11',label='Red')
    slider_r.grid(column=0,row=0)

    slider_g=tk.Scale(fra_sliders,from_=255,to=0,bg='black',
        activebackground='black',fg='green',font='verdana 11',label='Green')
    slider_g.grid(column=1,row=0)

    slider_b=tk.Scale(fra_sliders,from_=255,to=0,bg='black',
        activebackground='black',fg='#019BD5',font='verdana 11',label='Blue')
    slider_b.grid(column=2,row=0)

    update_color_can(entry)

    fen_color.mainloop()

def greater(a,b):
    """
    Fonction qui renvoie le plus grand élément entre a et b

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        a : type=int or float
        b : type=int or float

    Returns:
    ¯¯¯¯¯¯¯
        great : type=int or float
            Le plus grand élément entre a et b

    """
    if a<b:
        return b
    else:
        return a

def update_fill_color():
    """
    Récupère la couleur écrite dans entry_fill, vérifie si elle est correcte
    Si oui, la fonction définit cette couleur comme couleur des nouvelles cases
    """
    global fill_color,entry_fill,can_test
    try: #Teste si on peut colorer un canevas de 1x1 pixel de ma nouvelle
        can_test.configure(bg=entry_fill.get()) #couleur
        fill_color=entry_fill.get() #Si ça ne fait pas une erreur, définit cette
                                    #couleur comme couleur des nouvelles cases
    except:
        a=0 #Sinon, ne fait rien

def update_color_can(entry):
    """
    Actualise la couleur du canevas pour sélectionner une couleur personalisée
    en fonction des 3 sliders (rouge, vert et bleu)

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        entry : type=tkinter.entry
            Entry dans laquelle la nouvelle couleur sera affichée
    """
    global can_color,slider_b,slider_g,slider_r
    #Récupère les valeurs des 3 sliders et les convertit en héxadécimal
    can_bg=f'#{dec2hexa(slider_r.get())}{dec2hexa(slider_g.get())}{dec2hexa(slider_b.get())}'

    #Applique cette nouvelle couleur au canevas
    can_color.configure(bg=can_bg)

    #Le canevas s'actualise toutes les 60 ms
    can_color.after(60,lambda entry=entry,eff=None:update_color_can(entry))

    #Met ensuite à jour l'entry passée en paramètre en rempaçant son contenu par
    #la nouvelle couleur
    entry.delete(0,len(entry.get()))
    entry.insert(0,can_bg)


def dec2hexa(dec):
    """
    Convertit une valeur décimal en hexadécimal

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        dec : type=int ou str
            Valeur décimale à convertir

    Returns:
    ¯¯¯¯¯¯¯
        hexa : type=str
            Valeur cnvertie en héxadécimal
    """
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
    while len(hexa)<2: #Allonge la longueur de hexa jusqu'à 2
        hexa='0'+hexa
    return hexa

def done():
    """
    Valide le Pixel Art créé et met les commandes néccéssaires à sa création
    dans un fichier texte
    """
    global dico_state,c,can

    #Dresse la liste des tuples à ajouter à chque coordonnées pour en obtenir
    #les voisines
    list_d=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]

    list_gr_col=[] #Liste des couleurs des ensembles de cases collées de même couleur

    #--------Regroupe des ensembles collés de cases de la même couleur--------#

#    #Cases déjà dans un ensemble
#    list_pix_ens=[]
#
#    list_ens=[] #Liste des ensembles
#
#    for pix in dico_state.keys():
#        if pix not in list_pix_ens and dico_state[pix]!=None:
#            pix_col=dico_state[pix]
#            list_gr_col.append(pix_col)
#
#            dict_same_col={pix:[False for a in range(8)]}
#            list_same_col_2_proc=[pix]
#            list_pix_ens.append(pix)
#            while list_same_col_2_proc!=[]:
#                len_2_proc=len(list_same_col_2_proc)
#                for co in list_same_col_2_proc:
#                    for d in range (8):
#                        new_co=(co[0]+list_d[d][0],co[1]+list_d[d][1])
#                        if new_co in dico_state:
#                            if dico_state[new_co]==pix_col:
###                                print(new_co,list_same_col[a],a)
###                                print(co,list_d[d])
#                                dict_same_col[co][d]=True
#                                if new_co not in list_pix_ens:
#                                    dict_same_col[new_co]=[False for c in range(8)]
#                                    list_same_col_2_proc.append(new_co)
#                                    list_pix_ens.append(new_co)
#                    list_same_col_2_proc=list_same_col_2_proc[len_2_proc-1:]
#            list_ens.append(dict_same_col)
#
#
#    for ens in list_ens:
#        list_keys=list(ens.keys())
#
#        co=list_keys[0]






    list_pix_col=[]
    list_shapes=[]
    for pix in dico_state.keys():
        if dico_state[pix]!=None:
            if dico_state[pix] in list_pix_col:
                i=0
                while dico_state[pix]!=list_pix_col[i]:
                    i+=1
                list_shapes[i]+=[(pix[0],pix[1]),(pix[0]+1,pix[1]),(pix[0]+1,pix[1]+1),(pix[0],pix[1]+1),(pix[0],pix[1]),list_shapes[i][-1]]
            else:
                list_pix_col.append(dico_state[pix])
                list_shapes.append([(pix[0],pix[1]),(pix[0]+1,pix[1]),(pix[0]+1,pix[1]+1),(pix[0],pix[1]+1),(pix[0],pix[1])])
    file_insert=open('command.txt','w',encoding='utf8')
    for j in range(len(list_shapes)):
        str_co=''
        for int_co in list_shapes[j]:
            str_co+=f'({round(int_co[0]/(x_can),4)}+x)*c,({round(int_co[1]/(y_can),4)}+y)*c,'
        command=f'can.create_polygon({str_co}fill="{list_pix_col[j]}")\n'  #",outline="'+list_pix_col[j]+'",width=0)'
        print(command,file=file_insert)
        print(command)

    print([(key,dico_state[key]) for key in dico_state.keys() if dico_state[key]!=None],file=file_insert )



def erease():
    """
    Supprime toutes les cases colorées du canevas
    """
    global dico_state
    for key in dico_state.keys():
        dico_state[key]=None
    can_maj('all')

def en_dis_able_grid():
    """
    Désactive ou active la grille
    """
    global can,grid_enable
    grid_enable=not grid_enable
    if grid_enable:
        grid(x_can*c,y_can*c,c)
        but_en_dis_able_grid.configure(text='Désactiver la grille')
    else:
        can.delete("grid")
        but_en_dis_able_grid.configure(text='Activer la grille')



def change_i_fill(z):
    """
    Change de palette

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        z : type=int
            -1 pour afficher la palette précedente
            1 pour afficher la palette suivante
    """
    global i_can_fill
    i_can_fill=(i_can_fill+z)%len(list_col)
    update_fill_can()

def update_fill_can():
    """
    Met à jour le canevas de la palette
    """
    global can_fill,i_can_fill,c_fill,list_col

    #Dictionnaires des différentes palettes :
    #Une palette avec un assortiment de couleurs
    dico_col_main={(0,0):'#000000',(0,1):'#800000',(0,2):'#FF0000',
                   (0,3):'#FF00FF',(0,4):'#FF99CC',(1,0):'#993300',
                   (1,1):'#FF6600',(1,2):'#FF9900',(1,3):'#FFCC00',
                   (1,4):'#FFCC99',(2,0):'#333300',(2,1):'#808000',
                   (2,2):'#99CC00',(2,3):'#FFFF00',(2,4):'#FFFF99',
                   (3,0):'#003300',(3,1):'#008000',(3,2):'#339966',
                   (3,3):'#00FF00',(3,4):'#CCFFCC',(4,0):'#003366',
                   (4,1):'#008080',(4,2):'#33CCCC',(4,3):'#00FFFF',
                   (4,4):'#CCFFFF',(5,0):'#000080',(5,1):'#0000FF',
                   (5,2):'#3366FF',(5,3):'#00CCFF',(5,4):'#99CCFF',
                   (6,0):'#333399',(6,1):'#666699',(6,2):'#800080',
                   (6,3):'#993366',(6,4):'#CC99FF',(7,0):'#333333',
                   (7,1):'#808080',(7,2):'#969696',(7,3):'#C0C0C0',
                   (7,4):'#FFFFFF'}

    #Une palette avec des nuances de noir
    dico_col_black={(0,0):'#000000',(0,1):'#333333',(0,2):'#666666',
                    (0,3):'#9A9A9A',(0,4):'#CDCDCD',(1,0):'#060606',
                    (1,1):'#3A3A3A',(1,2):'#6D6D6D',(1,3):'#A0A0A0',
                    (1,4):'#D3D3D3',(2,0):'#0D0D0D',(2,1):'#404040',
                    (2,2):'#737373',(2,3):'#A6A6A6',(2,4):'#DADADA',
                    (3,0):'#131313',(3,1):'#464646',(3,2):'#7A7A7A',
                    (3,3):'#ADADAD',(3,4):'#E0E0E0',(4,0):'#1A1A1A',
                    (4,1):'#4D4D4D',(4,2):'#808080',(4,3):'#B3B3B3',
                    (4,4):'#E6E6E6',(5,0):'#202020',(5,1):'#535353',
                    (5,2):'#868686',(5,3):'#BABABA',(5,4):'#EDEDED',
                    (6,0):'#262626',(6,1):'#5A5A5A',(6,2):'#8D8D8D',
                    (6,3):'#C0C0C0',(6,4):'#F3F3F3',(7,0):'#2D2D2D',
                    (7,1):'#606060',(7,2):'#939393',(7,3):'#C6C6C6',
                    (7,4):'#FAFAFA'}

    #Une palette avec des nuances de rouge
    dico_col_red={(0,0):'#000000',(0,1):'#660000',(0,2):'#CD0000',
                  (0,3):'#FF3333',(0,4):'#FF9A9A',(1,0):'#0D0000',
                  (1,1):'#730000',(1,2):'#DA0000',(1,3):'#FF4040',
                  (1,4):'#FFA6A6',(2,0):'#1A0000',(2,1):'#800000',
                  (2,2):'#E60000',(2,3):'#FF4D4D',(2,4):'#FFB3B3',
                  (3,0):'#260000',(3,1):'#8D0000',(3,2):'#F30000',
                  (3,3):'#FF5A5A',(3,4):'#FFC0C0',(4,0):'#330000',
                  (4,1):'#9A0000',(4,2):'#FF0000',(4,3):'#FF6666',
                  (4,4):'#FFCDCD',(5,0):'#400000',(5,1):'#A60000',
                  (5,2):'#FF0D0D',(5,3):'#FF7373',(5,4):'#FFDADA',
                  (6,0):'#4D0000',(6,1):'#B30000',(6,2):'#FF1A1A',
                  (6,3):'#FF8080',(6,4):'#FFE6E6',(7,0):'#5A0000',
                  (7,1):'#C00000',(7,2):'#FF2626',(7,3):'#FF8D8D',
                  (7,4):'#FFF3F3'}

    #Une palette avec des nuances de vert
    dico_col_green={(0,0):'#000000',(0,1):'#006600',(0,2):'#00CD00',
                    (0,3):'#33FF33',(0,4):'#9AFF9A',(1,0):'#000D00',
                    (1,1):'#007300',(1,2):'#00DA00',(1,3):'#40FF40',
                    (1,4):'#A6FFA6',(2,0):'#001A00',(2,1):'#008000',
                    (2,2):'#00E600',(2,3):'#4DFF4D',(2,4):'#B3FFB3',
                    (3,0):'#002600',(3,1):'#008D00',(3,2):'#00F300',
                    (3,3):'#5AFF5A',(3,4):'#C0FFC0',(4,0):'#003300',
                    (4,1):'#009A00',(4,2):'#00FF00',(4,3):'#66FF66',
                    (4,4):'#CDFFCD',(5,0):'#004000',(5,1):'#00A600',
                    (5,2):'#0DFF0D',(5,3):'#73FF73',(5,4):'#DAFFDA',
                    (6,0):'#004D00',(6,1):'#00B300',(6,2):'#1AFF1A',
                    (6,3):'#80FF80',(6,4):'#E6FFE6',(7,0):'#005A00',
                    (7,1):'#00C000',(7,2):'#26FF26',(7,3):'#8DFF8D',
                    (7,4):'#F3FFF3'}

    #Une palette avec des nuances de bleu
    dico_col_blue={(0,0):'#000000',(0,1):'#000066',(0,2):'#0000CD',
                   (0,3):'#3333FF',(0,4):'#9A9AFF',(1,0):'#00000D',
                   (1,1):'#000073',(1,2):'#0000DA',(1,3):'#4040FF',
                   (1,4):'#A6A6FF',(2,0):'#00001A',(2,1):'#000080',
                   (2,2):'#0000E6',(2,3):'#4D4DFF',(2,4):'#B3B3FF',
                   (3,0):'#000026',(3,1):'#00008D',(3,2):'#0000F3',
                   (3,3):'#5A5AFF',(3,4):'#C0C0FF',(4,0):'#000033',
                   (4,1):'#00009A',(4,2):'#0000FF',(4,3):'#6666FF',
                   (4,4):'#CDCDFF',(5,0):'#000040',(5,1):'#0000A6',
                   (5,2):'#0D0DFF',(5,3):'#7373FF',(5,4):'#DADAFF',
                   (6,0):'#00004D',(6,1):'#0000B3',(6,2):'#1A1AFF',
                   (6,3):'#8080FF',(6,4):'#E6E6FF',(7,0):'#00005A',
                   (7,1):'#0000C0',(7,2):'#2626FF',(7,3):'#8D8DFF',
                   (7,4):'#F3F3FF'}

    #Une palette avec des nuances de jaune
    dico_col_yellow={(0,0):'#000000',(0,1):'#666600',(0,2):'#CDCD00',
                     (0,3):'#FFFF33',(0,4):'#FFFF9A',(1,0):'#0D0D00',
                     (1,1):'#737300',(1,2):'#DADA00',(1,3):'#FFFF40',
                     (1,4):'#FFFFA6',(2,0):'#1A1A00',(2,1):'#808000',
                     (2,2):'#E6E600',(2,3):'#FFFF4D',(2,4):'#FFFFB3',
                     (3,0):'#262600',(3,1):'#8D8D00',(3,2):'#F3F300',
                     (3,3):'#FFFF5A',(3,4):'#FFFFC0',(4,0):'#333300',
                     (4,1):'#9A9A00',(4,2):'#FFFF00',(4,3):'#FFFF66',
                     (4,4):'#FFFFCD',(5,0):'#404000',(5,1):'#A6A600',
                     (5,2):'#FFFF0D',(5,3):'#FFFF73',(5,4):'#FFFFDA',
                     (6,0):'#4D4D00',(6,1):'#B3B300',(6,2):'#FFFF1A',
                     (6,3):'#FFFF80',(6,4):'#FFFFE6',(7,0):'#5A5A00',
                     (7,1):'#C0C000',(7,2):'#FFFF26',(7,3):'#FFFF8D',
                     (7,4):'#FFFFF3'}

    #Une palette avec des nuances de magenta
    dico_col_magenta={(0,0):'#000000',(0,1):'#660066',(0,2):'#CD00CD',
                      (0,3):'#FF33FF',(0,4):'#FF9AFF',(1,0):'#0D000D',
                      (1,1):'#730073',(1,2):'#DA00DA',(1,3):'#FF40FF',
                      (1,4):'#FFA6FF',(2,0):'#1A001A',(2,1):'#800080',
                      (2,2):'#E600E6',(2,3):'#FF4DFF',(2,4):'#FFB3FF',
                      (3,0):'#260026',(3,1):'#8D008D',(3,2):'#F300F3',
                      (3,3):'#FF5AFF',(3,4):'#FFC0FF',(4,0):'#330033',
                      (4,1):'#9A009A',(4,2):'#FF00FF',(4,3):'#FF66FF',
                      (4,4):'#FFCDFF',(5,0):'#400040',(5,1):'#A600A6',
                      (5,2):'#FF0DFF',(5,3):'#FF73FF',(5,4):'#FFDAFF',
                      (6,0):'#4D004D',(6,1):'#B300B3',(6,2):'#FF1AFF',
                      (6,3):'#FF80FF',(6,4):'#FFE6FF',(7,0):'#5A005A',
                      (7,1):'#C000C0',(7,2):'#FF26FF',(7,3):'#FF8DFF',
                      (7,4):'#FFF3FF'}

    #Une palette avec des nuances de cyan
    dico_col_cyan={(0,0):'#000000',(0,1):'#006666',(0,2):'#00CDCD',
                   (0,3):'#33FFFF',(0,4):'#9AFFFF',(1,0):'#000D0D',
                   (1,1):'#007373',(1,2):'#00DADA',(1,3):'#40FFFF',
                   (1,4):'#A6FFFF',(2,0):'#001A1A',(2,1):'#008080',
                   (2,2):'#00E6E6',(2,3):'#4DFFFF',(2,4):'#B3FFFF',
                   (3,0):'#002626',(3,1):'#008D8D',(3,2):'#00F3F3',
                   (3,3):'#5AFFFF',(3,4):'#C0FFFF',(4,0):'#003333',
                   (4,1):'#009A9A',(4,2):'#00FFFF',(4,3):'#66FFFF',
                   (4,4):'#CDFFFF',(5,0):'#004040',(5,1):'#00A6A6',
                   (5,2):'#0DFFFF',(5,3):'#73FFFF',(5,4):'#DAFFFF',
                   (6,0):'#004D4D',(6,1):'#00B3B3',(6,2):'#1AFFFF',
                   (6,3):'#80FFFF',(6,4):'#E6FFFF',(7,0):'#005A5A',
                   (7,1):'#00C0C0',(7,2):'#26FFFF',(7,3):'#8DFFFF',
                   (7,4):'#F3FFFF'}

    list_col=[dico_col_main,dico_col_black,dico_col_red,dico_col_green,
              dico_col_blue,dico_col_yellow,dico_col_magenta,dico_col_cyan]

    can_fill.delete(tk.ALL)
    for x in range(8):
        for y in range(5):
            can_fill.create_rectangle(x*c_fill,y*c_fill,(x+1)*c_fill,
                                      (y+1)*c_fill,
                                      fill=list_col[i_can_fill][x,y])

def left_click_fill(event):
    """
    Récupère la couleur de la palette sur laquelle l'utilisateur.trice a cliqué
    """
    global c_fill,fill,entry_fill
    x_f,y_f=event.x//c_fill,event.y//c_fill

    entry_fill.delete(0,len(entry_fill.get()))
    entry_fill.insert(0,list_col[i_can_fill][x_f,y_f])

pixel_art_tool()