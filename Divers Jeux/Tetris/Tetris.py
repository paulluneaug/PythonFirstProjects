import tkinter as tk
from random import randint

def tetris():
    """
    Lance une parte de Tetris

    Contrôles:
        -Les flèches de droite et de gauche pour décaler la pièce qui tombe
        -La flèche du bas pour faire tomber plus vite la pièce
        -La flèche du haut pour faire tomber completement la pièce

        -A pour échanger la pièce stockée et celle qui tombe
        -Q et D pour faire tourner la pièce qui tombe respectivement dans
         le sens anti-horaire et dans le sens horaire

        -Espace pour mettre le jeu en pause
        -M pour recommencer une partie

    """
    global x_can,y_can,c,can_inc,can_main,fen,can_store,lab_pts_int
    x_can=11 #Nombre de case de largeur du canevas
    y_can=24 #Nombre de case de hauteur du canevas
    c=500//greater(y_can,x_can) #Taille en pixels de chaque case

    fen=tk.Tk()
    fen.title('Tetris')

    fra_top=tk.Frame(fen,width=c*x_can,height=3*c+10,bg='black',relief=tk.SOLID,
        bd=2)
    fra_top.grid(column=0,row=0)
    fra_top.pack_propagate(False)

    lab_inc=tk.Label(fra_top,font='Verdana 15',fg='red',bg='black',
        text='Prochaine Pièce')
    lab_inc.grid(column=0,row=0)

    lab_store=tk.Label(fra_top,font='Verdana 15',fg='red',bg='black',
        text='Pièce Stockée')
    lab_store.grid(column=2,row=0)

    #Canevas sur lequel la pièce à venir est affichée
    can_inc=tk.Canvas(fra_top,width=5*c,height=3*c,bg='black')
    can_inc.grid(column=0,row=1)

    fra_pts=tk.Frame(fra_top,width=5*c,height=3*c,bg='black',relief=tk.SOLID,
        bd=2)
    fra_pts.grid(column=1,row=1)
    fra_pts.pack_propagate(False)

    #Canevas sur lequel le pièce stockée est affichée
    can_store=tk.Canvas(fra_top,width=5*c,height=3*c,bg='black')
    can_store.grid(column=2,row=1)

    lab_pts=tk.Label(fra_pts,font='Verdana 15',fg='red',text='Points :',
        bg='black')
    lab_pts.grid(column=0,row=0)

    lab_pts_int=tk.Label(fra_pts,font='Verdana 15',fg='red',text='0',
        bg='black')
    lab_pts_int.grid(column=0,row=1)

    can_main=tk.Canvas(fen,width=c*x_can,height=c*y_can,bg='black',bd=2,
        relief=tk.SOLID) #Canevas principal sur lequel se joue le Tetris
    can_main.grid(column=0,row=1)

    fen.bind('<Left>',left)
    fen.bind('<Right>',right)
    fen.bind('<Down>',down)
    fen.bind('<q>',rot_antihor)
    fen.bind('<d>',rot_hor)
    fen.bind('<a>',store)
    fen.bind('<Q>',rot_antihor)
    fen.bind('<D>',rot_hor)
    fen.bind('<A>',store)
    fen.bind('<space>',setpause)
    fen.bind('<m>',restart)
    fen.bind('<Up>',max_down)

    init()

    fen.mainloop()

def init():
    """
    Initialise les principales variales néccéssaires au jeu
    """
    global falling_piece,next_piece,n_piece,x_can,y_can,dico_state,fall_pix
    global speed,stored_piece,storable,pause,list_piece,shade_pix

    speed=500 #Temps en ms que met la pièce à tomber d'une case vers le bas

    list_piece=list_piece_main.copy()

    #Choisit la pièce qui va tomber et celle d'après
    next_piece=list_piece.pop(randint(0,len(list_piece)-1))
    falling_piece=list_piece.pop(randint(0,len(list_piece)-1))

    stored_piece,storable=[],True #Indique q'aucune pièce n'est stockée et que
                                  #la pièce qui tombe peut l'être

    #Taille du plus petit carré pouvant contenir la pièce
    n_piece=dim_piece(falling_piece[0],False)

    #Coordonnées sur le canevas principal de la case à laquelle la pièce
    #qui tombe est attachée
    fall_pix=[(x_can-n_piece)//2,-n_piece]
    shade_pix=fall_pix.copy()

    pause=False

    dico_state={} #Initialise le dictionnaire principal
    for p in [(a,b) for a in range(x_can) for b in range(-10,y_can)]:
        dico_state[p]=0

    calc_shade_pix()
    can_maj(True,False)
    chute() #Commence le jeu

def smaller(a,b):
    """
    Fonction qui renvoie le plus petit élément entre a et b

    Arguments:
        a : type=int or float
        b : type=int or float

    Returns:
        small : type=int or float
            Le plus petit élément entre a et b

    """
    if a>b:
        return b
    else:
        return a

def greater(a,b):
    """
    Fonction qui renvoie le plus grand élément entre a et b

    Arguments:
        a : type=int or float
        b : type=int or float

    Returns:
        great : type=int or float
            Le plus grand élément entre a et b

    """
    if a<b:
        return b
    else:
        return a

def dim_piece(piece,xy):
    """
    Renvoie la dimention du plus petit carré ou rectangle pouvant contenir
    la pièce
    C'est à dire la plus grande valeur parmi la différence entre la plus petite
    et la plus grande abscisse et le différence entre la plus petite et la plus
    grande ordonnée

    Arguments:
    ----------
        piece:list de tuples

        xy:bool
            True pour retourner les longueurs des cotés du plus petit rectangle
            pouvant contenir la pièce
            False pour la longeur du plus petit carré pouvant contenir la pièce

    Returns:
    --------
        dim : type=int
            Longueur du coté du plus petit carré pouvant contenir la pièce

        OU

        dim_x,dim_y : type=int
            Longueur et largeur du plus petit rectangle pouvant contenir la
            pièce
    """

    #Liste des extrèmes en abscisse et en ordonnées des cases composant la pièce
    list_ext=[[piece[0][0],piece[0][0]],[piece[0][1],piece[0][1]]]

    for pix in piece:
        #Pour chaque case de la pièce, on vérifie que son abscisse ou son
        #ordonnée n'est pas la plus grande trouvée jusqu'ici
        list_ext=[[smaller(list_ext[0][0],pix[0]),
            greater(list_ext[0][1],pix[0])],[smaller(list_ext[1][0],pix[1]),
            greater(list_ext[1][1],pix[1])]]
    if xy:
        return list_ext[0][1]-list_ext[0][0]+1,list_ext[1][1]-list_ext[1][0]+1
    else:
        return greater(list_ext[0][1]-list_ext[0][0],
                       list_ext[1][1]-list_ext[1][0])+1

def check_dir(piece_c,pix_dir,d):
    """
    Verifie si la piece en chute peut aller dans une direction

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        piece_c : type=list
            liste des coordonnées de la piece qui tombe

        pix_dir : type=list
            Liste des coordonnées du pixel directeur de la pièce

        d:tuple ou list de deux entiers entre -1 et 1
            couple de valeurs à ajourer à chaque coordonnées

    Returns:
    ¯¯¯¯¯¯¯
        tf : type=bool
            True si la pièce peut aller dans la direction
            False sinon
    """
    tf=True
    #Dresse la liste des coordonnées de chaque pixel de la pièce
    list_true_co=[(a[0]+pix_dir[0],a[1]+pix_dir[1]) for a in piece_c]

    for pix in list_true_co: #Pour chaque nouvelle coordonée
        if (pix[0]+d[0],pix[1]+d[1]) in dico_state.keys():
            if dico_state[pix[0]+d[0],pix[1]+d[1]]!=0: #On vérifie qu'il n'y a
                tf=False                         #pas déjà une pièce ou le bord
        else:
            tf=False
    return tf

def left(event):
    """
    Décale d'une case sur la gauche la pièce qui tombe
    """
    global falling_piece,fall_pix
    if check_dir(falling_piece[0],fall_pix,(-1,0)): #Vérifie qu'il n'y a aucun
        fall_pix[0]-=1                              #obstacle à gauche
        calc_shade_pix()
    can_maj(False,False)

def right(event):
    """
    Décale d'une case sur la droite la pièce qui tombe
    """
    global falling_piece,fall_pix
    if check_dir(falling_piece[0],fall_pix,(1,0)): #Vérifie qu'il n'y a aucun
        fall_pix[0]+=1                             #obstacle à droite
        calc_shade_pix()
    can_maj(False,False)

def down(event):
    """
    Fait tomber d'une case vers le bas la pièce qui tombe
    """
    global falling_piece,fall_pix
    #Vérifie si il n'y a pas de case colorée en dessous de la pièce
    if check_dir(falling_piece[0],fall_pix,(0,1)):
        fall_pix[1]+=1
        calc_shade_pix()
        can_maj(False,False)
    else: #Si il y en a une, ajoute la pièce qui tombe au dictionnaire
        insert(falling_piece)

def max_down(event):
    """
    Descend la pièce qui tombe jusqu'en bas
    """
    global fallinf_piece,fall_pix
    while check_dir(falling_piece[0],fall_pix,(0,1)): #Tant que la pièce peut
        fall_pix[1]+=1                                #descendre
    calc_shade_pix()
    insert(falling_piece) #Puis ajoute la pièce au dictionnaire

def change_piece():
    """
    Fait apparaître une nouvelle pièce
    """
    global falling_piece,next_piece,n_piece,fall_pix,storable,list_piece

    if list_piece==[]: #Reconstruit la liste des pièces disponibles si elle est
        list_piece=list_piece_main.copy() #vide

    #Place la nouvelle pièce en haut du canevas et choisit la prochaine pièce
    falling_piece=next_piece
    next_piece=list_piece.pop(randint(0,len(list_piece)-1))
    n_piece=dim_piece(falling_piece[0],False)
    fall_pix=[(x_can-n_piece)//2,-n_piece]

    storable=True #Indique qu'il est à nouveau possible de stocker la pièce

    calc_shade_pix()
    can_maj(True,False)
    checkline()

def rot_hor(event):
    """
    Fait tourner la pièce qui tombe dans le sens horaire
    """
    global falling_piece,n_piece,fall_pix
    list_hor=[]
    for pix in falling_piece[0]:
        list_hor.append((n_piece-1-pix[1],pix[0]))
    if check_dir(list_hor,fall_pix,(0,0)): #Vérifie que la pièce peut tourner
        falling_piece=[list_hor,falling_piece[1]] #sans retrer dans le décor
    calc_shade_pix()
    can_maj(False,False)

def rot_antihor(event):
    """
    Fait tourner la pièce qui tombe dans le sens anti-horaire
    """
    global falling_piece,n_piece,fall_pix
    list_antihor=[]
    for pix in falling_piece[0]:
        list_antihor.append((pix[1],n_piece-1-pix[0]))
    if check_dir(list_antihor,fall_pix,(0,0)): #Vérifie que la pièce peut tourner
        falling_piece=[list_antihor,falling_piece[1]] #sans retrer dans le décor
    calc_shade_pix()
    can_maj(False,False)

def store(event):
    """
    Échange la pièce qui tombe et la pièce stckée
    """
    global stored_piece,falling_piece,fall_pix,storable,x_can
    if storable: #Si la pièce qui tombe n'a pas déjà été stockée
        if stored_piece!=[]: #Si aucune pièce est déjà stockée
            #Échange les deux pièces
            stored_piece,falling_piece=falling_piece,stored_piece
            n_piece=dim_piece(falling_piece[0],False)
            fall_pix=[(x_can-n_piece)//2,-n_piece]
        else: #Sinon, stocke la pièce et en fait tomber une nouvelle
            stored_piece=falling_piece
            change_piece()
        storable=False
        calc_shade_pix()
        can_maj(True,True)

def can_maj(maj_can_inc,maj_can_store):
    """
    Met à jour les canevas

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        maj_can_inc : type=bool
            True s'il faut mettre à jour le canevas de la prochaine pièce
            False sinon

        maj_can_store : type=bool
            True s'il faut mettre à jour le canevas de la pièce stockée
            False sinon
    """
    global can_main,can_inc,can_store,x_can,y_can,c,falling_piece,next_piece
    global fall_pix,shade_pix

    can_main.delete(tk.ALL) #Supprime tous les éléments du canevas proncipal

    #Affiche tous les éléments fixes, les pièces déjà posées
    for x in range(x_can):
        for y in range(y_can):
            if dico_state[x,y]!=0:
                can_main.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,
                    fill=dico_state[x,y],outline='black',width=2)

    #Affiche l'ombre de la pièce qui tombe
    for pix in falling_piece[0]:
        can_main.create_rectangle((pix[0]+shade_pix[0]+0.1)*c,
                                  (pix[1]+shade_pix[1]+0.1)*c,
                                  (pix[0]+1+shade_pix[0]-0.1)*c,
                                  (pix[1]+1+shade_pix[1]-0.1)*c,
                                  fill='black',
                                  outline=falling_piece[1],width=2)

    #Affiche la pièce qui tombe
    for pix in falling_piece[0]:
        can_main.create_rectangle((pix[0]+fall_pix[0])*c,
                                  (pix[1]+fall_pix[1])*c,
                                  (pix[0]+1+fall_pix[0])*c,
                                  (pix[1]+1+fall_pix[1])*c,
                                  fill=falling_piece[1],
                                  outline='black',width=2)

    #S'il faut mettre à jour le canevas de la prochaine pièce
    if maj_can_inc:
        can_inc.delete(tk.ALL)
        n_x,n_y=dim_piece(comp(next_piece[0]),True)

        #Calcule la taille de chaque carreau pour qu'elle rentre dans le canevas
        c_t=c*smaller(smaller(5/n_x-10/(n_x*c),3/n_y-10/(n_y*c)),1)
        for pix in comp(next_piece[0]): #Et affiche la prochaine pièce
            can_inc.create_rectangle(((5*c/c_t-n_x)/2+pix[0])*c_t,
                                     ((3*c/c_t-n_y)/2+pix[1])*c_t,
                                     ((5*c/c_t-n_x)/2+pix[0]+1)*c_t,
                                     ((3*c/c_t-n_y)/2+pix[1]+1)*c_t,
                                     fill=next_piece[1],
                                     outline='black',width=2)

    #S'il faut mettre à jour le canevas de la pièce stockée
    if maj_can_store:
        can_store.delete(tk.ALL)
        n_x,n_y=dim_piece(comp(stored_piece[0]),True)

        #Calcule la taille de chaque carreau pour qu'elle rentre dans le canevas
        c_t=c*smaller(smaller(5/n_x-10/(n_x*c),3/n_y-10/(n_y*c)),1)
        for pix in comp(stored_piece[0]): #Et affiche la pièce stockée
            can_store.create_rectangle(((5*c/c_t-n_x)/2+pix[0])*c_t,
                                       ((3*c/c_t-n_y)/2+pix[1])*c_t,
                                       ((5*c/c_t-n_x)/2+pix[0]+1)*c_t,
                                       ((3*c/c_t-n_y)/2+pix[1]+1)*c_t,
                                       fill=stored_piece[1],
                                       outline='black',width=2)

def setpause(event):
    """
    Met le jeu en pause ou le reprend
    """
    global pause,can_main,x_can
    pause=not pause
    if pause:
        for key in ['<Right>','<Down>','<Left>','<q>','<d>','<a>','<Q>','<D>',
                    '<A>','<Up>']:
            fen.unbind(key) #Délie toutes les touches
        can_main.create_text(x_can//2*c,20,font='Verdanna 20',text='Pause',
            fill='red')
    else:
        fen.bind('<Left>',left)
        fen.bind('<Right>',right)
        fen.bind('<Down>',down)
        fen.bind('<Up>',max_down)
        fen.bind('<q>',rot_antihor)
        fen.bind('<d>',rot_hor)
        fen.bind('<a>',store)
        fen.bind('<Q>',rot_antihor)
        fen.bind('<D>',rot_hor)
        fen.bind('<A>',store)

        chute()

def insert(piece):
    """
    Insert la pièce qui tombe dans dico_state
    """
    global dico_state,fall_pix
    for pix in piece[0]:
        dico_state[pix[0]+fall_pix[0],pix[1]+fall_pix[1]]=piece[1]
    change_piece()

def checkline():
    """
    Vérifie chaque ligne si elle est pleine
    Supprime les lignes vides et abaisse les lignes supérieures
    """
    global x_can,y_can,dico_state,lab,lab_pts_int,speed

    #Dresse la liste des lignes pleines
    list_fill=[not(False in [dico_state[x1,y1]!=0 for x1 in range(x_can)]) for y1 in range(y_can)]

    #Met à jour les points
    pts=list_fill.count(True)**2*100+int(lab_pts_int.cget("text"))
    lab_pts_int.configure(text=str(pts))

    #Augmente la vitesse du jeu
    for h in range(list_fill.count(True)):
        if speed>100:
            speed//=1.04
            speed=int(speed)

    #Abaisse les lignes
    for a in range(y_can):
        if list_fill[a]:
            for b in range(a):
                for x1 in range(x_can):
                    dico_state[x1,a-b]=dico_state[x1,a-b-1]

    #Si une pièce dépasse du canevas, fait perdre le joueur
    if True in [dico_state[x2,-1]!=0 for x2 in range(x_can)]:
        lose()

def lose():
    """
    Fait perdre le joueur
    """
    global can_main,c

    for key in ['<Right>','<Down>','<Left>','<q>','<d>','<a>','<Q>','<D>',
                '<A>','<Up>']:
        fen.unbind(key)

    can_main.create_text((x_can/2)*c,(y_can/2)*c,font='Verdana 45',text='Perdu',
        fill='red')
    fen.mainloop()

def comp(piece):
    """
    Retourne la pièce compactée, c'est à dire chaque abscisse moins la plus
    petite abscisse et chaque ordonnée moins la plus petite ordonnée

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        piece : type=list
            liste des coordonnées de la piece

    Returns:
    ¯¯¯¯¯¯¯
        piece_comp : type=list
            liste des coordonnées de la piece compactée
    """
    sx=piece[0][0]
    sy=piece[0][1]
    for pix in piece:
        sx=smaller(sx,pix[0])
        sy=smaller(sy,pix[1])
    return [(pixel[0]-sx,pixel[1]-sy) for pixel in piece]

def calc_shade_pix():
    global shade_pix,falling_piece,fall_pix
    shade_pix=fall_pix.copy()
    while check_dir(falling_piece[0],shade_pix,(0,1)):
        shade_pix[1]+=1

def chute():
    """
    Fait descendre la pièce
    """
    global fen,speed,pause
    if not pause:
        down(0)
        can_maj(False,False)
        calc_shade_pix()
        fen.after(speed,chute)

def restart(event):
    """
    Recommence une nouvelle partie
    """
    global fen
    fen.destroy()
    tetris()


#Chaque pièce est une liste composée d'une liste de coordonnées et d'une chaine
#représentant la couleur de la pièce
list_piece_main=[[[(0,0),(0,1),(1,0),(1,1)],'#FBC200'],#| ■■
                                                       #| ■■
                 #------------------------------------
                 [[(0,0),(0,1),(1,1),(2,1)],'#0158B5'],#| ■
                                                       #| ■■■
                 #------------------------------------
                 [[(1,0),(2,0),(0,1),(1,1)],'#63BD27'],#|  ■■
                                                       #| ■■
                 #------------------------------------
                 [[(0,0),(1,0),(1,1),(2,1)],'#D61E27'],#| ■■
                                                       #|  ■■
                 #------------------------------------
                 [[(2,0),(0,1),(1,1),(2,1)],'#FC7601'],#|   ■
                                                       #| ■■■
                 #------------------------------------
                 [[(0,2),(1,2),(2,2),(3,2)],'#019BD5'],#| ■■■■
                 #------------------------------------
                 [[(1,0),(0,1),(1,1),(2,1)],'#902890'],#|  ■
                                                       #| ■■■
                 ]




tetris()