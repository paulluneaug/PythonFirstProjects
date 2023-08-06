import tkinter as tk
from random import random

def game_life():
    """
    Lance une simulation du Jeu de la Vie, de John Conway
    """
    global can,x_c,y_c,c,dico_state,sleep,fen,inp,play
    #Définit la nombre de cellules en hauteur et en largeur de la grille
    x_c,y_c=80,40

    c=500//y_c #Taille en pixels du coté de chaque cellule
    width,height=x_c*c,y_c*c
    sleep=50 #Temps en ms entre chaque calcul du prochain état de la grille
    play=False

    fen=tk.Tk()
    fen.title('Jeu de la Vie')

    can=tk.Canvas(fen,width=width,height=height,bg='#DDDDDD')
    can.pack(padx=3,pady=2)

    frame_bottom=tk.Frame(fen,width=width,height=80,bg='gray',bd=2,relief=tk.SOLID)
    frame_bottom.pack_propagate(False)
    frame_bottom.pack(pady=5)

    but_play=tk.Button(frame_bottom,text='Commencer',font='Times 13',command=begin)
    but_play.pack(side=tk.LEFT,padx=5,pady=3)

    but_pause=tk.Button(frame_bottom,text='Pause',font='Times 13',command=pause)
    but_pause.pack(side=tk.RIGHT,padx=5,pady=3)

    but_random=tk.Button(frame_bottom,
        text='Placer au hasard des cellules sur la grille',font='Times 13',
        command=create_rand)
    but_random.pack(side=tk.LEFT,padx=5,pady=3)

    but_erase=tk.Button(frame_bottom,text='Tout effacer',font='Times 13',
        command=erase)
    but_erase.pack(side=tk.RIGHT,padx=5,pady=3)

    but_canon=tk.Button(frame_bottom,text='Canon à planeur',font='Times 13',
        command=canon)
    but_canon.pack(side=tk.RIGHT,padx=5,pady=3)

    lab_speed=tk.Label(frame_bottom,text="Vitesse de l'animation (en ms)",
        bg='grey')
    lab_speed.pack(pady=2)

    inp=tk.Entry(frame_bottom,width=10,font='Times 13')
    inp.bind("<Return>",custom_speed)
    inp.pack(side=tk.BOTTOM,padx=5,pady=3)

    #Initialise le dictionnaire principal avec pour chaque cellule de la grlle
    #ses coordonnées en clef et l'état de la callule en valeur:
    # - 1 si la cellule est vivante
    # - 0 sinon
    dico_state={(tx,ty):0 for tx in range(x_c) for ty in range(y_c)}
    

    grid(width,height,c)

    can.bind('<Button-1>',left_click)
    can.bind('<Button-3>',right_click)
    can.bind('<Control-B1-Motion>',left_click)
    can.bind('<Control-B3-Motion>',right_click)
    can.bind('<space>',pause)

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
    vx,vy=1,1
    while vx<=width:
        can.create_line(vx,0,vx,height,width=1,fill='black',tag='grid')
        vx+=c
    while vy<=height:
        can.create_line(0,vy,width,vy,width=1,fill='black',tag='grid')
        vy+=c
    can.create_rectangle(2,2,width,height,width=1,outline='black',tag='grid')


def f_play():
    """
    Calcule l'état de la grille au prochain tour en :
        -tuant les cellules vivantes entourées de moins de 2 ou plus de 3
         cellules vivantes
        -faisant naître les cellules mortes entourées de 3 cellules vivantes
    """
    global play,x_c,y_c,sleep,fen
    list_d=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
    list_1=[] #Liste des coordonnées des cellules vivantes

    dico_nei={} #Dictionnaire avec pour clef les coordonnées de toutes les cases
                #ayant des cellules vivantes pour voisines et pour valeurs le
                #nombre de voisines vivantes

    if play:
        for x1 in range(x_c):
            for y1 in range(y_c):
                if dico_state[x1,y1]==1:
                    list_1.append((x1,y1)) #Dresse la liste des coordonnées
                                           #des cellules vivantes
                    dico_nei[(x1,y1)]=0

        for co in list_1: #Pour chaque cellules vivantes
            for d in list_d:
                if (co[0]+d[0],co[1]+d[1]) in dico_state: #Dans chaque direction
                    if not(co[0]+d[0],co[1]+d[1]) in dico_nei:
                        dico_nei[(co[0]+d[0],co[1]+d[1])]=0
                    dico_nei[(co[0]+d[0],co[1]+d[1])]+=1 #Ajoute 1 à la valeur dans dico_nei des coordonnées de la voisine

        for key in dico_nei.keys(): #Chaque cellule avec au moins une voisine vivante
            if dico_nei[key]==3: #Naît si elle a 3 vosines
                dico_state[key]=1
            elif dico_nei[key]<2 or dico_nei[key]>3:#Meurt si elle en a moins
                dico_state[key]=0                   #que 2 ou plus que 3

        can_maj()
        fen.after(sleep,f_play)

def can_maj():
    """
    Met à jour le canevas pour correspondre à l'état de dico_state
    """
    global c,dico_state,x_c,y_c,can
    can.delete('cell') #Supprime toutes les cellules
    for x_maj in range(x_c):
        for y_maj in range(y_c):
            if dico_state[x_maj,y_maj]==1:
                can.create_rectangle(x_maj*c+1,y_maj*c+1,x_maj*c+c+1,
                    y_maj*c+c+1,fill='black',tag='cell') #Affiche les cellules vivantes

def left_click(event):
    """
    Fait apparaitre une cellule là où l'utilisateur clique si il n'y en a
    pas déjà une
    """
    global c,dico_state
    x_ev=event.x//c #Récupère les coordonnées du click de l'utilisateur
    y_ev=event.y//c
    if dico_state[x_ev,y_ev]!=1:
        dico_state[x_ev,y_ev]=1
        can.create_rectangle(x_ev*c+1,y_ev*c+1,x_ev*c+c+1,y_ev*c+c+1,
            fill='black',tag='cell')

def right_click(event):
    """
    Fait diparaitre la cellule là où l'utilisateur clique si il y en a une
    """
    global c,dico_state
    x_ev=event.x//c
    y_ev=event.y//c
    if dico_state[x_ev,y_ev]!=0:
        dico_state[x_ev,y_ev]=0
        can.create_rectangle(x_ev*c+1,y_ev*c+1,x_ev*c+c+1,y_ev*c+c+1,
            fill='#DDDDDD',tag='cell')

def begin():
    """
    Lance la simulation
    """
    global play
    play=True
    f_play()

def pause():
    """
    Met en pause ou reprend la simulation
    """
    global play
    play=not play
    if play:
        f_play()

def create_rand():
    """
    Place au hasard sur le grille des cellules, selon une probabilité de 0.3
    """
    global x_c,y_c,play
    play=False
    for x2 in range(x_c):
        for y2 in range(y_c):
            if randprob(0.3):
                dico_state[x2,y2]=1
    can_maj()

def randprob(prob):
    """
    Renvoie True selon une certaine probabilité "prob"

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        prob: type = float or int ; 0 <= prob <= 1
            Probabilité de retourner True

    Return:
    ¯¯¯¯¯¯
        tf: type = bool
            True ou False selon la probabilité "prob" et un tirage aléatoire
    """
    return random()<prob

def erase():
    """
    Supprime toutes les cellules de la grille
    """
    global x_c,y_c
    pause()
    for x3 in range(x_c):
        for y3 in range(y_c):
            dico_state[x3,y3]=0
    can_maj()

def canon():
    """
    Fait apparaître un canon à planeur, une structure stable
    qui créé à intervalle régulier un planeur
    """
    global dico_state
    list_canon=[(0,5),(0,6),(1,5),(1,6),(10,5),(10,6),(10,7),(11,4),(11,8),
        (12,3),(12,9),(13,3),(13,9),(14,6),(15,4),(15,8),(16,5),(16,6),(16,7),
        (17,6),(20,3),(20,4),(20,5),(21,3),(21,4),(21,5),(22,2),(22,6),(24,1),
        (24,2),(24,6),(24,7),(34,3),(34,4),(35,3),(35,4)]
    for cell in list_canon:
        dico_state[cell]=1
    can_maj()

def custom_speed(event):
    """
    Redéfinie le temps entre chaque calcul du prochain état de la grille
    """
    global sleep
    try:
        sleep=int(inp.get())
    except ValueError:
        print('Valeur saisie impossible')

game_life()
