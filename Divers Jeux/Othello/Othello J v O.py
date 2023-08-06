import tkinter as tk
from random import randint
import time

def play_othello_JvO():
    """
    Lance une pertie d'Othello contre l'ordinateur
    """
    global fen1,can, but_white,but_black,frame_color,lab_player_color
    global width,height,select_dif
    global dico_state,c,whoplays,pts_white,pts_black,pts_rst,global_message

    c=80 #Taille en pixels de chaque case de la grise
    width=c*8 #Largeur en pixels du canevas principal et de la grille
    height=width #Hauteur en pixels du canevas principal et de la grille

    #Dictionnaire associant à chaque coordonée des cases de la grille son état:
    #   - 0 si la case est vide
    #   - 1 si un pion blanc s'y trouve
    #   - 2 si un pion noir s'y trouve
    dico_state={}

    #Indique qui joue 3 si c'est le joueur, 4 si c'est l'ordinateur
    whoplays=randint(3,4)

    fen1=tk.Tk()
    fen1.title('Othello')

    frame_color=tk.Frame(fen1,height=50,width=width+4,bg='green',bd=2,
        relief=tk.SOLID)
    frame_color.pack_propagate(False)
    frame_color.pack(side=tk.TOP,padx=5,pady=5)

    but_white=tk.Button(frame_color,text='Choisir les Blancs',font='Times 15',
        command=white_player)
    but_white.pack(side=tk.LEFT,padx=5)

    but_black=tk.Button(frame_color,text='Choisir les Noirs',font='Times 15',
        command=black_player)
    but_black.pack(side=tk.RIGHT,padx=5)

    lab_player_color=tk.Label(frame_color,bg='green',font='Times 20')
    lab_player_color.pack()

    frame_top=tk.Frame(fen1,height=50,width=width+4,bg='black',bd=2,
        relief=tk.SOLID)
    frame_top.pack_propagate(False)
    frame_top.pack(side=tk.TOP)

    frame_top_pts=tk.Frame(fen1,height=50,width=width+4,bg='green',bd=2,
        relief=tk.SOLID)
    frame_top_pts.pack_propagate(False)
    frame_top_pts.pack(side=tk.TOP,padx=5)

    global_message=tk.Label(frame_top,fg='red',bg='black',font='Times 20')
    global_message.pack(pady=5)

    pts_white=tk.Label(frame_top_pts,bg='green',font='Times 15')
    pts_white.pack(side=tk.LEFT,padx=10)

    pts_black=tk.Label(frame_top_pts,bg='green',font='Times 15')
    pts_black.pack(side=tk.RIGHT,padx=10)

    pts_rst=tk.Label(frame_top_pts,bg='green',font='Times 15')
    pts_rst.pack(pady=10)

    can=tk.Canvas(fen1,height=height,width=width,bg='green',bd=2,
        relief=tk.SOLID)
    can.pack(side=tk.TOP)

    fen1.mainloop()

def create_frame_bottom():
    """
    Créé deux cadres en bas, un pour sélectionner la difficulté, l'autre pour
    passer son tour en cas de besoin
    """
    global select_dif,but_dif_1,but_dif_2,frame_bottom_dif,but_dif_0
    frame_bottom_dif=tk.Frame(fen1,height=100,width=width/2-5,bg='green',bd=2,
        relief=tk.SOLID)
    frame_bottom_dif.grid_propagate(False)
    frame_bottom_dif.pack_propagate(False)
    frame_bottom_dif.pack(side=tk.LEFT,padx=5,pady=5)

    frame_bottom_pass=tk.Frame(fen1,height=100,width=width/2-5,bg='green',bd=2,
        relief=tk.SOLID)
    frame_bottom_pass.grid_propagate(False)
    frame_bottom_pass.pack(side=tk.RIGHT,padx=5,pady=5)

    select_dif=tk.Label(frame_bottom_dif,bg='green',font='Times 16')
    select_dif.configure(text='Sélection de la difficulté :')
    select_dif.grid(column=0,row=0,columnspan=3)

    but_dif_0=tk.Button(frame_bottom_dif,text='Facile',font='Times 15',
        command=dif0)
    but_dif_0.grid(column=0,row=1,padx=3,pady=3)

    but_dif_1=tk.Button(frame_bottom_dif,text='Moyen',font='Times 15',
        command=dif1)
    but_dif_1.grid(column=1,row=1)

    but_dif_2=tk.Button(frame_bottom_dif,text='Difficile',font='Times 15',
        command=dif2)
    but_dif_2.grid(column=2,row=1,padx=3,pady=3)

    but_skip=tk.Button(frame_bottom_pass,text='Passer son tour',font='Times 20',
        command=skip_turn)
    but_skip.grid(column=0,row=0,padx=25,pady=15)

    can.bind('<Button-1>',click)

def init():
    """
    Initialise la le dictionnaire dico_state et place les 4 poions du centre
    """
    global c_skipped,p_skipped
    for x in range(8):
        for y in range (8):
            if not (x,y) in dico_state.keys():
                dico_state[x,y]=0
    dico_state[3,3]=1
    dico_state[3,4]=2
    dico_state[4,3]=2
    dico_state[4,4]=1
    c_skipped,p_skipped=False,False
    grid()
    maj_grid()
    play()

def grid():
    """
    Dessine la grille
    """
    vx=0
    vy=0
    while vx!=width:
        can.create_line(vx,0,vx,width,width=2,fill='black')
        vx+=c
    while vy!=height:
        can.create_line(0,vy,height,vy,width=2,fill='black')
        vy+=c

def maj_grid():
    """
    Met à jour la grille du jeu pour correspondre à l'état de dico_state
    """
    global pion,p_skipped,c_skipped
    can.delete('pawn') #Supprime les pions de la grille
    white=0 #Nombre de pions blancs sur le plateau
    black=0 #Nombre de pions noirs sur le plateau
    #Pour chaque entrées de dico_state, créé un pion de la bonne couleur et compte les pions
    for x in range (8):
        for y in range (8):
            if dico_state[x,y]!=0:
                if dico_state[x,y]==1:
                    out="black"
                    fill="white"
                    white+=1
                elif dico_state[x,y]==2:
                    out="white"
                    fill="black"
                    black+=1
                can.create_oval(x*c+c/10,y*c+c/10,x*c+9*c/10,y*c+9*c/10,
                    outline=out,fill=fill, width=c/32,tag='pawn')

    pts_white.configure(text=('Points Blancs : '+str(white)))
    pts_black.configure(text=('Points Noirs : '+str(black)))
    pts_rst.configure(text=('Points restants : '+str(64-(black+white))))
    pion=black+white

    if pion==64 or white== 0 or black==0 or (p_skipped and c_skipped):
        #Si il n'y a plus de pions noirs ou blancs, ou si tout le plateau est
        #rempli, ou encore si le joueur et l'ordinateur ont passé leur tour
        #désigne un gagnant
        if white>black:
            global_message.configure(text='Les Blancs ont gagné')
        elif black>white:
            global_message.configure(text='Les Noirs ont gagné')
        else:
            global_message.configure(text='Égalité')
        global_message.pack()
        can.unbind('<Button-1>')
    else:
        p_skipped,p_skipped=False,False

def check(x,y,whoplays):
    """
    Vérifie si le joueur ou l'ordinateur peut poser un pion en (x,y) et si oui,
    dresse la liste des directions dans lesquelles des pions sont à retourner

    Si c'est l'ordinateur qui joue, lui renvoie les points associés

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        x : type = int
            Coordonnée x de la case à verifier

        y : type = int
            Coordonnée y de la case à verifier

        whoplays : type=int 3<=whoplays<=4
            Désigne qui joue
            3 -> le joueur
            4 -> l'ordinateur

    Return:
    ¯¯¯¯¯¯
        pts : type = int
            Point que gagnerait celui qui joue s'il place son pion ici
            -1 s'il ne peut pas jouer

        list_tf : type = list
            Liste de 8 Booléens
            True si il y a des pièces à retourner dans cette direction
            False sinon
    """
    if dico_state[x,y]==0:
        if whoplays==3:
            color=player_color
            en_color=com_color
        elif whoplays==4:
            color=com_color
            en_color=player_color

        tfN=False
        if y !=0:#Recherche de case de même couleur au Nord
            i=1
            while dico_state[x,y-i]==en_color and y-i>0:
                #Tant que les cases vers le Nord sont de la couleur
                #de l'adversaire
                i+=1
            if dico_state[x,y-i]== color and i!=1:
                #Si au bout de la lignes de cases à l'adversaire,
                #il y a une case de la couleur de celui qui joue
                tfN=True #Indique qu'il y a des cases à retourner
                         #dans cette direction


        #Et ainsi de suite pour toutes les directions

        tfNE=False
        if x!=7 and y!=0:#Recherche de case de même couleur au Nord-Est
            i=1
            while dico_state[x+i,y-i]==en_color and x+i<7 and y-i>0:
                i+=1
            if dico_state[x+i,y-i]== color and i!=1:
                tfNE=True

        tfE=False
        if x!=7:#Recherche de case de même couleur à l'Est
            i=1
            while dico_state[x+i,y]==en_color and x+i<7:
                i+=1
            if dico_state[x+i,y]== color and i!=1:
                tfE=True

        tfSE=False
        if x!=7 and y!=7:#Recherche de case de même couleur au Sud-Est
            i=1
            while dico_state[x+i,y+i]==en_color and x+i<7 and y+i<7:
                i+=1
            if dico_state[x+i,y+i]== color and i!=1:
                tfSE=True

        tfS=False
        if y!=7:#Recherche de case de même couleur au Sud
            i=1
            while dico_state[x,y+i]==en_color and y+i<7:
                i+=1
            if dico_state[x,y+i]== color and i!=1:
                tfS=True

        tfSO=False
        if x!=0 and y!=7:#Recherche de case de même couleur au Sud-Ouest
            i=1
            while dico_state[x-i,y+i]==en_color and x-i>0 and y+i<7:
                i+=1
            if dico_state[x-i,y+i]== color and i!=1:
                tfSO=True

        tfO=False
        if x!=0:#Recherche de case de même couleur à l'Ouest
            i=1
            while dico_state[x-i,y]==en_color and x-i>0:
                i+=1
            if dico_state[x-i,y]== color and i!=1:
                tfO=True

        tfNO=False
        if x!=0 and y!=0:#Recherche de case de même couleur au Nord-Ouest
            i=1
            while dico_state[x-i,y-i]==en_color and x-i>0 and y-i>0:
                i+=1
            if dico_state[x-i,y-i]== color and i!=1:
                tfNO=True

        liste_tf=[tfN,tfNE,tfE,tfSE,tfS,tfSO,tfO,tfNO]
        t=liste_tf.count(True) #Compte le nombre de directions dans lesquelles
                               #des pions sont à retourner

        if whoplays==3:
            if t==0:
                #Si il n'y a aucun pion à retourner dans toutes les directions
                #Indique au joueur que son coup est impossible
                global_message.configure(text='Coup Impossible')
            else: #Sionon, valide le coup du joueur
                global_message.configure(text='')
                maj_dico(x,y,player_color,liste_tf,False)

        elif whoplays==4:
            if t==0:         #Renvoie -1 et [] si l'ordinateur ne peut pas
                return -1,[] #jouer sur cette case

            else: #Sinon, renvoie les points gagnés et la liste des directions
                  #dans lesquelles des pions sont à retourner
                return maj_dico(x,y,com_color,liste_tf,True),liste_tf
    else:
        return -1,[]



def maj_dico(x,y,color,liste_tf,ccheck):
    """
    Met à jour dico_state en retournant les pions qui doivent l'être

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        x : type = int
            Coordonnée x de la case à verifier

        y : type = int
            Coordonnée y de la case à verifier

        color : type=int 1<=color<=2
            Désigne la couleur de celui qui joue
            1 -> Blancs
            2 -> Noirs

        list_tf : type = list
            Liste de 8 Booléens
            True si il y a des pièces à retourner dans cette direction
            False sinon

        ccheck : type=bool
            True s'il faut renvoyer les points
            False sinon

    Return:
    ¯¯¯¯¯¯
        pts : type = int
            Point que gagnerait celui qui joue s'il place son pion ici
            -1 s'il ne peut pas jouer
    """

    global whoplays,pion
    pts=dico_val[x,y]

    #Mise à jour de dico_state pour le Nord
    if liste_tf[0]: #Si des pions sont à retourner au Nord
        j=1
        while dico_state[x,y-j]!=color: #Tant que des cases sont à retourner
            if ccheck: #Si le but est de calculer les points gagnés en jouant
                       #en (x,y)
                pts+=dico_val[x,y-j] #Ajoute au cumul de points les points
                                     #gagnés en fonction de la valeur des cases
            else: #Sinon, retourne le pion
                dico_state[x,y-j]=color
            j+=1

    #Et ainsi de suite pour toutes les directions

    #Mise à jour de dico_state pour le Nord-Est
    if liste_tf[1]:
        j=1
        while dico_state[x+j,y-j]!=color:
            if ccheck:
                pts+=dico_val[x+j,y-j]
            else:
                dico_state[x+j,y-j]=color
            j+=1

    #Mise à jour de dico_state pour l'Est
    if liste_tf[2]:
        j=1
        while dico_state[x+j,y]!=color:
            if ccheck:
                pts+=dico_val[x+j,y]
            else:
                dico_state[x+j,y]=color
            j+=1

    #Mise à jour de dico_state pour le Sud-Est
    if liste_tf[3]:
        j=1
        while dico_state[x+j,y+j]!=color:
            if ccheck:
                pts+=dico_val[x+j,y+j]
            else:
                dico_state[x+j,y+j]=color
            j+=1

    #Mise à jour de dico_state pour le Sud
    if liste_tf[4]:
        j=1
        while dico_state[x,y+j]!=color:
            if ccheck:
                pts+=dico_val[x,y+j]
            else:
                dico_state[x,y+j]=color
            j+=1

    #Mise à jour de dico_state pour le Sud-Ouest
    if liste_tf[5]:
        j=1
        while dico_state[x-j,y+j]!=color:
            if ccheck:
                pts+=dico_val[x-j,y+j]
            else:
                dico_state[x-j,y+j]=color
            j+=1

    #Mise à jour de dico_state pour l'Ouest
    if liste_tf[6]:
        j=1
        while dico_state[x-j,y]!=color:
            if ccheck:
                pts+=dico_val[x-j,y]
            else:
                dico_state[x-j,y]=color
            j+=1

    #Mise à jour de dico_state pour le Nord-Ouest
    if liste_tf[7]:
        j=1
        while dico_state[x-j,y-j]!=color:
            if ccheck:
                pts+=dico_val[x-j,y-j]
            else:
                dico_state[x-j,y-j]=color
            j+=1


    if ccheck: #Si le but était juste de calculer les points, renvoie les points
        return pts #gagnés si celui qui joue posait un pion en (x,y)
    else:
        whoplays=abs(whoplays-7)
        dico_state[x,y]=color
        maj_grid()

def play():
    """
    Fait jouer l'ordinateur
    """
    global pion,whoplays,fen1

    if pion!=64:
        if whoplays==4:

            #Dictionnaire liant à chaque coordonnée de case la valeur en points
            #que rapporterait le fait d'y poser un pion
            dico_pts={}

            for x in range (8):
                for y in range (8):
                    #Donc les points de chaque case sont évalués
                    dico_pts[x,y]=[check(x,y,4)]

            #Recherche quelle case rapporte le plus de points
            #Si il y en a plusieurs qui rapportent la même chose,
            #une au hasard est choisie
            pgkey=(0,0)
            liste_pg=[]
            for key in dico_pts.keys():
                if dico_pts[key][0][0]>dico_pts[pgkey][0][0]:
                    pgkey=key
                    liste_pg=[key]
                if dico_pts[key][0][0]==dico_pts[pgkey][0][0]:
                    liste_pg.append(key)
            if liste_pg[0] in liste_pg[1:]:
                del liste_pg[0]

            print(dico_pts[liste_pg[0]])
            if dico_pts[liste_pg[0]][0][0]!=-1:
                randkey=liste_pg[randint(0,len(liste_pg)-1)]
                cx=randkey[0]
                cy=randkey[1]
                #Valide le choix de la case en y plaçant un pion
                maj_dico(cx,cy,com_color,dico_pts[cx,cy][0][1],False)

            else: #Si aucune case ne rapporte de point,
                  #l'ordinateur ne peut pas jouer et passe son tour
                skip_turn()
        else:
            can.bind("<Button-1>",click)



def click(event):
    """
    Fait joueur le joueur là où il a cliqué
    """
    px = int(event.x//c)
    py = int(event.y//c)
    check(px,py,3)
    play()

def init_val(liste_val,dif):
    """
    Initialise le tableau des valeurs de chaque case en fonction de la
    difficulté

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        list_val : type=list
            Liste d'entiers représentant la valeur de chaque case du quart
            superieur gauche de la grille
    """
    global dico_val
    dico_val={}
    for x in range(8): #Applique le tableau de valeur de chaque case
        for y in range(8):
            if 0<=x<=3 and 0<=y<=3: #Sur le quart superieur gauche
                dico_val[x,y]=liste_val[4*x+y]
            if 0<=x<=3 and 4<=y<=7: #Sur le quart inférieur gauche
                dico_val[x,y]=liste_val[4*x+(7-y)]
            if 4<=x<=7 and 0<=y<=3: #Sur le quart superieur droit
                dico_val[x,y]=liste_val[4*(7-x)+y]
            if 4<=x<=7 and 4<=y<=7: #Sur le quart inférieur droit
                dico_val[x,y]=liste_val[4*(7-x)+(7-y)]

    select_dif.grid_forget()
    but_dif_0.grid_forget()
    but_dif_1.grid_forget()
    but_dif_2.grid_forget()

    lab_dif=tk.Label(frame_bottom_dif,font='Times 20',bg='green')
    lab_dif.configure(text=("Difficulté "+dif))
    lab_dif.pack()

def dif0():
    """
    Sélectionne la difficulté Facile
    """
    liste_val=[1,1,1,1, #Valeur des cases su coin supérieur gauche
               1,1,1,1,
               1,1,1,1,
               1,1,1,1]
    init_val(liste_val,"Facile")
    if player_color!=0:
        init()

def dif1():
    """
    Sélectionne la difficulté Moyenne
    """
    liste_val=[20,2,5,5, #Valeur des cases su coin supérieur gauche
                2,1,2,2,
                5,2,3,3,
                5,2,3,3]
    init_val(liste_val,"Moyenne")
    if player_color!=0:
        init()

def dif2():
    """
    Sélectionne la difficulté Difficile et pose un pion pour l'ordinateur dans
    chaque coin
    """
    liste_val=[100,10,25,25, #Valeur des cases su coin supérieur gauche
                10, 2,10, 5,
                25,10,15,10,
                25, 5,10,10]
    init_val(liste_val,"Difficile")
    dico_state[0,0],dico_state[7,0]=abs(player_color-3),abs(player_color-3)
    dico_state[0,7],dico_state[7,7]=abs(player_color-3),abs(player_color-3)
    pion=8
    if player_color!=0:
        init()

def skip_turn():
    """
    Passe le tour de celui qui joue
    """
    global whoplays,p_skipped,c_skipped
    if whoplays==3:
        p_skipped=True #Indique que le joueur a passé son tour
    else:
        c_skipped=True #Indique que l'ordinateur a passé son tour
    whoplays=abs(whoplays-7)
    play()

def white_player():
    """
    Sélectionne les pions blancs pour le joueur
    """
    global player_color,com_color
    player_color=1
    com_color=2

    but_white.pack_forget()
    but_black.pack_forget()
    frame_color.configure(bg='white')
    lab_player_color.configure(text='Vous êtes les Blancs',bg='white')
    lab_player_color.pack(pady=5)
    create_frame_bottom()

def black_player():
    """
    Sélectionne les pions noirs pour le joueur
    """
    global player_color,com_color
    player_color=2
    com_color=1

    but_white.pack_forget()
    but_black.pack_forget()
    frame_color.configure(bg='black')
    lab_player_color.configure(text='Vous êtes les Noirs',bg='black',fg='white')
    lab_player_color.pack(pady=5)
    create_frame_bottom()


play_othello_JvO()