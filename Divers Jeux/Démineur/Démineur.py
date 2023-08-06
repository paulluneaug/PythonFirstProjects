import tkinter as tk
from random import randint

def play_demineur():
    """
    Ouvre une fenêtre de sélection de la difficulté composée de trois boutons
    (Facile, Moyen et Difficile) et d'une entrée pour sélectionner une taille
    et un nombre de mines personnalisés
    """
    global inp

    fen_dif=tk.Tk()
    fen_dif.title('Démineur : Difficulté')

    fra_sel_dif=tk.Frame(fen_dif,bg='black')
    fra_sel_dif.pack()

    t12='Verdana 12'
    but_easy=tk.Button(fra_sel_dif,text='Facile : 9×9, 10 Mines',font=t12,
        command=lambda a=0,eff=None:init(9,9,10))
    but_easy.pack(side=tk.TOP,padx=5,pady=5)

    but_med=tk.Button(fra_sel_dif,text='Moyen : 16×16, 40 Mines',font=t12,
        command=lambda a=0,eff=None:init(16,16,40))
    but_med.pack(side=tk.TOP,padx=5,pady=5)

    but_hard=tk.Button(fra_sel_dif,text='Dificile : 30×16, 99 Mines',font=t12,
        command=lambda a=0,eff=None:init(30,16,99))
    but_hard.pack(side=tk.TOP,padx=5,pady=5)

    lab_custom = tk.Label(fra_sel_dif)
    lab_custom.configure(text = "Personalisé (x y nb_mines) :",font=t12,
        fg='white',bg='black')
    lab_custom.pack(side=tk.TOP,padx=5,pady=5)

    inp = tk.Entry(fra_sel_dif)
    inp.bind("<Return>", custom_size)
    inp.pack(side=tk.TOP,padx=5,pady=5)

    fen_dif.mainloop()

def custom_size(event):
    """
    Récupère les valeurs entrées dans inp, les sépare et lance une partie avec
    les paramètres personnalisés, s'ils sont corrects
    """
    list_imp=inp.get().split(' ')
    if len(list_imp)==3:
        try:
            axb=int(list_imp[0])*int(list_imp[1])
            if 0.05*axb<=int(list_imp[2])<=0.95*axb and axb-15>int(list_imp[2]):
                init(int(list_imp[0]),int(list_imp[1]),int(list_imp[2]))
            else:
                print('Valeurs saisies impossibles')
        except ValueError:
            print('Valeurs saisies impossibles')
    else:
        print('Il faut remplir les 3 champs')



def init(x_ca,y_ca,nb_min):
    """
    Créé une fenètre de démineur avec les paramètres en argument et lance le jeu

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        x_ca : type=int
            Nombre de cases en largeur du canevas du jeu

        y_ca : type=int
            Nombre de cases en hauteur du canevas du jeu

        nb_min : type=int
            Nombre de cases de mines
    """
    global can,turn,x_can,y_can,nb_mine,tile_flipped,fen_main,c
    x_can,y_can,nb_mine=x_ca,y_ca,nb_min
    c=30 #Taille en pixels de chaque case
    turn,tile_flipped=0,0

    fen_main=tk.Tk()
    fen_main.title('Démineur '+str(x_can)+'×'+str(y_can)+'   '+str(nb_mine)+
        ' Mines')

    can=tk.Canvas(fen_main,width=x_can*c,height=y_can*c,bg='grey')
    can.pack()

    grid(x_can*c,y_can*c)

    can.bind('<Button-1>',left_click)
    can.bind('<Button-3>',right_click)

    fen_main.mainloop()

def init_dict(x_init,y_init):
    """
    Initialise le dictionnaire dict_state

    Arguments:
    ¯¯¯¯¯¯¯¯¯¯
        x_init : type=int
            Coordonnée x de la première case appuyée par le joueur, qui doit ne
            comporter aucune mine dans les 8 cases autour d'elle

        y_init : type=int
            Coordonnée y de la première case appuyée par le joueur, qui doit ne
            comporter aucune mine dans les 8 cases autour d'elle
    """



    #dict_state est construit de la manière suivante :
    #dict_state[(x,y)]=[n,t]

    # (x,y) : type=tuple
    #     Coordonnées de chaque case

    # n : type=int 0<=n<=9
    #     Nombre de mines dans les 8 cases autour,
    #     9 si une mine se trouve sur la case

    # t : type=int 0<=t<=2
    #     État de la case
    #       0 -> la case n'as pas encore été retournée
    #       1 -> la case est retournée
    #       2 -> un drapeau est posé sur la case


    global dict_state,nb_mines,x_can,y_can,list_d
    dict_state={}
    #Dresse la liste des tuples à ajouter à chque coordonnées pour en obtenir
    #les voisines
    list_d1=[(a,b) for a in range(-1,2) for b in range(-1,2)]

    #Dresse la liste des cases ne devant pas comporter de mines (autour du
    #premier click du joueur)
    list_ban=[(x_init+list_d1[d][0],y_init+list_d1[d][1]) for d in range(9)]

    #Dresse la liste des coordonnées des mines puis les place dans le dict_state
    list_poss_mine=[(a,b) for a in range(x_can) for b in range(y_can) if (a,b)
        not in list_ban]
    for mine in range(nb_mine):
        dict_state[list_poss_mine.pop(randint(0,len(list_poss_mine)-1))]=[9,0]

    #Compte pour chaque case le nombre de mines voisines
    #puis le place dans dict_state
    for x in range (x_can):
        for y in range (y_can):
            if not (x,y) in dict_state:
                dict_state[x,y]=[0,0]
                for d in list_d:
                    if (x+d[0],y+d[1]) in dict_state:
                        if dict_state[x+d[0],y+d[1]][0]==9:
                            dict_state[x,y][0]+=1


def grid(width,height):
    """
    Dessine la grille sur le canevas

    Arguments:
    ¯¯¯¯¯¯¯¯¯¯
        width : type=int
            largeur du canevas

        height : type=int
            longueur du canevas
    """
    vx,vy=0,0
    while vx!=width:
        can.create_line(vx,0,vx,height,width=2,fill='black')
        vx+=c
    while vy!=height:
        can.create_line(0,vy,width,vy,width=2,fill='black')
        vy+=c

def left_click(event):
    """
    Retourne les cases qui doivent l'être selon où clique le joueur
    S'il a gagné ou perdu, lui indique
    """
    global dict_state,turn,x_can,y_can,list_d,nb_mine,fen_main,tile_flipped

    #Récupère les coordonnées du clique gauche du joueur
    x_lc=event.x//c
    y_lc=event.y//c

    list_2_flip=[]
    list_tile_0=[]

    #Dresse la liste des tuples à ajouter à chque coordonnées pour en obtenir
    #les voisines
    list_d=[(a,b) for a in range(-1,2) for b in range(-1,2) if (a,b)!=(0,0)]

    if turn==0: #Si c'est le premier click du joueur, initialise dict_state
        init_dict(x_lc,y_lc)
        turn=1


    if dict_state[x_lc,y_lc][1]==0: #Vérifie que le joueur ne clique pas sur une case déjà retournée ou avec un drapeau
        dic_xy=dict_state[x_lc,y_lc][0]

        if dic_xy==0:#Si le joueur tombe sur une case sans mine autour,
                     #il faut retourner toutes les cases sans mines reliées à la
                     #case cliquée par le joueur par des cases dont n=0

            list_2_flip.append((x_lc,y_lc)) #Représente la liste des cases qu'il faudra retourner
            list_tile_0.append((x_lc,y_lc)) #Représente la liste des cases dont n=0 et dont les voisines ne sont pas encore dans list_2_flip
            while list_tile_0!=[]:
                nb_del=0 #Le nombre d'éléments de list_tile_0 supprimés

                for a in range(len(list_tile_0)):#Vérifie pour chaque élément de list_tile_0
                    a_0=list_tile_0[a-nb_del]

                    for d in list_d: #Dans chacune des directions
                        x_y=(a_0[0]+d[0],a_0[1]+d[1])
                        cond_1=not x_y in list_2_flip #Que sa voisine n'est pas déjà dans list_2_flip
                        cond_2=x_y in dict_state

                        if cond_1 and cond_2:
                            if dict_state[x_y][1]==0:
                                if dict_state[x_y][0]==0: #Si en plus sa voisine a n=0, l'ajoute à list_tile_0
                                    list_tile_0.append(x_y)
                                list_2_flip.append(x_y)
                    del list_tile_0[a-nb_del]#Puis supprime l'élément de list_tile_0
                    nb_del+=1

            for b in range(len(list_2_flip)): #Toutes les cases qu'il faut retourner sont retournées et affichées
                xy=list_2_flip.pop()
                draw_tile(xy[0],xy[1],1)
                dict_state[xy][1]=1
                tile_flipped+=1

        elif dic_xy==9:#Si le joueur tombe sur une mine
            for x in range(x_can):
                for y in range(y_can):
                    if dict_state[x,y][0]==9:
                        draw_boom(x,y) #Dessine une explosion sur chacune des mines du plateau

            fen_end=tk.Tk() #Et créé une fenêtre pour lui indiquer qu'il a perdu
            fen_end.title('Défaite')

            fra_end=tk.Frame(fen_end,width=100,height=20)
            fra_end.pack()

            lab_end=tk.Label(fra_end,font='Verdana 50',text='Défaite')
            lab_end.pack(padx=10,pady=10)

        else: #Si le joueur tombe sur une case sans mine mais avec au moins une mine autour
            draw_tile(x_lc,y_lc,dict_state[x_lc,y_lc][1]) #Dessine une case sur le canevas avec un chiffre
            dict_state[x_lc,y_lc][1]=1 #Indique à dict_state que la case est retournée
            tile_flipped+=1

        if tile_flipped==(x_can*y_can)-nb_mine: #Si toutes les cases sans mines ont été retournées
            fen_end=tk.Tk() #Créé une fenêtre pour indiquer au joueur qu'il a gagné
            fen_end.title('Victoire')

            fra_end=tk.Frame(fen_end,width=100,height=20)
            fra_end.pack()

            lab_end=tk.Label(fra_end,font='Verdana 50',text='Victoire')
            lab_end.pack(padx=10,pady=10)

def right_click(event):
    """Place un drapeau ou l'enleve à l'endroit où clique le joueur"""
    global dict_state

    #Récupère les coordonnées du clique droit du joueur
    x_rc=event.x//c
    y_rc=event.y//c

    if dict_state[x_rc,y_rc][1]==0: #Si la case n'est pas retournée, dessine un drapeau sur la case
        draw_tile(x_rc,y_rc,2)
        dict_state[x_rc,y_rc][1]=2
    elif dict_state[x_rc,y_rc][1]==2: #Si un drapeau est déjà présent sur la case, le supprime
        can.create_rectangle(x_rc*c,y_rc*c,(x_rc+1)*c,(y_rc+1)*c,fill='grey',
            outline='black',width=2)
        dict_state[x_rc,y_rc][1]=0

def draw_tile(x,y,t):
    """
    Dessine une case de type t sur le canvas aux coordonnées (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯¯
        x : type=int
            Coordonnée x de la case à dessiner

        y : type=int
            Coordonnée y de la case à dessiner

        t : type=int  0<=t<=2
            Type de case
                0 -> Case non-retournée
                1 -> Case retournée
                2 -> Case avec unn drapeau
    """
    global c
    list_color=['#3366FF','#1D6404','#B0020A','#150991','#FF6B00','#007F86',
        '#C90000','#F90299']

    if t==2:#Dessine un drapeau

        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='grey',
            outline='black',width=2)

        can.create_polygon(x*c+0.5*c,y*c+0.1*c,x*c+0.55*c,y*c+0.1*c,x*c+0.55*c,
            y*c+0.6*c,x*c+0.5*c,y*c+0.6*c,x*c+0.1*c,y*c+0.35*c,fill='red',
            outline='black',width=1)

        can.create_polygon(x*c+0.55*c,y*c+0.1*c,x*c+0.6*c,y*c+0.1*c,x*c+0.6*c,
            y*c+0.8*c,x*c+0.8*c,y*c+0.8*c,x*c+0.85*c,y*c+0.88*c,x*c+0.2*c,y*c+
            0.88*c,x*c+0.25*c,y*c+0.8*c,x*c+0.5*c,y*c+0.8*c,x*c+0.5*c,y*c+0.6*c,
            x*c+0.55*c,y*c+0.6*c,fill='#515151',outline='black',width=1)

    else: #Dessine une case claire
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='#E2E2E2',
            outline='black',width=2)
        if dict_state[x,y][0]!=0: #Ajoute un texte avec le nombre de mines voisines sur la case
            can.create_text((x+0.5)*c,(y+0.5)*c,text=str(dict_state[x,y][0]),
                font='Verdana 15',fill=list_color[dict_state[x,y][0]])
        else:
            can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,
                        fill='#E2E2E2',outline='black',width=2)

def draw_boom(x,y):
    """
    Dessine une explosion aux coorndonnées (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯¯
        x : type=int
            Coordonnée x de l'explosion à dessiner

        y : type=int
            Coordonnée y de l'explosion à dessiner
    """
    global c
    can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='grey',
        outline='black',width=2)
    can.create_polygon(x*c+0.5*c,y*c+0.1*c,x*c+0.55*c,y*c+0.3*c,x*c+0.65*c,
        y*c+0.3*c,x*c+0.8*c,y*c+0.2*c,x*c+0.7*c,y*c+0.35*c,x*c+0.7*c,y*c+0.45*c,
        x*c+0.9*c,y*c+0.5*c,x*c+0.7*c,y*c+0.55*c,x*c+0.7*c,y*c+0.65*c,x*c+0.8*c,
        y*c+0.8*c,x*c+0.65*c,y*c+0.7*c,x*c+0.55*c,y*c+0.7*c,x*c+0.5*c,y*c+0.9*c,
        x*c+0.45*c,y*c+0.7*c,x*c+0.35*c,y*c+0.7*c,x*c+0.2*c,y*c+0.8*c,x*c+0.3*c,
        y*c+0.65*c,x*c+0.3*c,y*c+0.55*c,x*c+0.1*c,y*c+0.5*c,x*c+0.3*c,
        y*c+0.45*c,x*c+0.3*c,y*c+0.35*c,x*c+0.2*c,y*c+0.2*c,x*c+0.35*c,
        y*c+0.3*c,x*c+0.45*c,y*c+0.3*c,outline='red',fill='orange',width=3)



##def can_reload():
##    """
##    Supprime toutes les cases du canvas avant de les redessiner pour éviter
##    une perte de performances liée à un trop grand nombre de formes sur le
##    canvas
##    """
##    global x_can,y_can
##    can.delete(ALL)
##    grid(x_can,y_can)
##    for x in range(x_can):
##        for y in range(y_can):
##            if dict_state[x,y][1]!=0:
##                draw_tile(x,y,dict_state[x,y][1])

play_demineur()