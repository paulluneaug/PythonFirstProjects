import tkinter as tk
from random import randint

def puissance_4_jvj():
    """
    Lance une partie de Puissance 4 avec un autre joueur sur le même ordinateur
    Chaque joueur tout à tout

    Contrôles:
    ¯¯¯¯¯¯¯¯¯
        -Click gaughe sur une colonne pour y placer un pion
        -M pour recommencer une nouvelle partie
    """
    global dico_state,x_can,y_can,c,can,whoplay,lab_global,fen

    #Nombre de pions en hauteur et en largeur qu'il est possible de placer
    x_can=7
    y_can=6

    c=900//y_can #Taille de chaque case dans laquelle on peut poser un pion

    fen=tk.Tk()
    fen.title('Puissance 4 JvJ')

    fra_top_global=tk.Frame(fen,width=x_can*c,height=50,bg='black',
        relief=tk.SOLID,bd=2)
    fra_top_global.pack_propagate(False)
    fra_top_global.pack(side=tk.TOP,pady=5)

    lab_global=tk.Label(fra_top_global,font='Times 20',bg='black',fg='red')

    can=tk.Canvas(fen,width=x_can*c,height=y_can*c,bg='#5555FF',relief=tk.SOLID,
        bd=2)
    can.pack(pady=5,padx=5)

    dico_state,whoplay=init(x_can,y_can)
    can_maj()
    can.bind('<Button-1>',left_click)
    fen.mainloop()

def init(x_can,y_can):
    """
    Initialise les variables du jeu

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        x_can : type=int
            Nombre de cases en largeur du canevas

        y_can : type=int
            Nombre de cases en hauteur du canevas

    Returns:
    ¯¯¯¯¯¯¯
        dico_state : type=dict
            Dictionnaire de toutes les cases et de leur état

        whoplay : type=int
            Indique qui joue

    """
    dico_state={}
    for a in range(x_can+1):
        for b in range(y_can+1):
            dico_state[a,b]=0
    return dico_state,randint(1,2)

def can_maj():
    """
    Met à jour le canevas pour correspondre à l'état de dico_state
    """
    global dico_state,x_can,y_can,c,can
    can.delete(tk.ALL)
    list_col=['gray','yellow','red']
    for xy in dico_state.keys(): #Créé un cercle de couleur sur chaque case
        can.create_oval((xy[0]+0.15)*c,(xy[1]+0.15)*c,(xy[0]+0.85)*c,
                        (xy[1]+0.85)*c,fill=list_col[dico_state[xy]],width=2)

def left_click(event):
    """
    Place un pion de la couleur de celui qui joue dans la colonne cliquée
    """
    global c,dico_state,whoplay,lab_global,y_can
    lab_global.configure(text='')
    x_c=event.x//c
    if dico_state[x_c,0]!=0: #Indique au joueur si la colonne est pleine
        lab_global.configure(text='Cette colone est pleine')
        lab_global.pack(pady=10)
    else:
        #Place le pion au sommet de la pile de pion de la colonne
        f=0
        while dico_state[x_c,f]==0 and f<=y_can-1:
            f+=1
        dico_state[x_c,f-1]=whoplay
        next_turn(test_puissance4(x_c,f-1,whoplay))

def test_puissance4(x,y,whoplay):
    """
    Teste si l'un des deux joueur a fait un puissance 4, c'est à dire si il a
    aligné 4 pions ou plus

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        -x : type=int
            Abscisse de la case qu'il faut tester

        -y : type=int
            Ordonnée de la case qu'il faut tester

        -whoplay : type=int
            Indique qui joue
                -1 pour les jaunes
                -2 pour les rouges

    Returns:
    ¯¯¯¯¯¯¯
        tf : type=bool
            -True si un joueur a fait un puissance 4
            -False sinon

    """
    global dico_state,x_can,y_can
    list_d=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
    list_sc=[] #Liste du nombre de cases de la même couleur dans les 8directions
    for i in range(8):
        #Vérifie dans toutes les directions si il y a des pions de même couleur
        d=list_d[i]
        sc=0
        while True:
            #Tout en restant dans les limites de la grille,
            if 0<x+(1+sc)*d[0]<x_can and 0<y+(1+sc)*d[1]<y_can:
                #Compte le nombre de cases de la même couleur dans la direction
                if dico_state[x+(1+sc)*d[0],y+(1+sc)*d[1]]==whoplay:
                    sc+=1
                else:
                    break
            else:
                break
        list_sc.append(sc)
    for j in range(4):
        #Compte si l4 il y a au moins 4 cases voisines, de même couleur et
        #alignées dans les directions opposées
        if list_sc[j]+list_sc[4+j]>=3:
            return True
    return False

def next_turn(win):
    """
    Affiche quel joueur a gagné si un joueur a gagné
    Change qui joue sinon
    """
    global whoplay,fen,x_can,c,can
    list_color=[('yellow','Jaunes'),('red','Rouges')]
    can_maj()
    if win: #Si un joueur a gagné, une frame est créée en dessous du canevas
            #et la partie s'arrête
        fra_end=tk.Frame(fen,height=50,width=x_can*c,
            bg=list_color[abs(whoplay-3)-1][0],relief='solid',bd=2)
        fra_end.pack_propagate(False)
        fra_end.pack(side=tk.BOTTOM)

        lab_end=tk.Label(fra_end,font='Verdana 20',fg=list_color[whoplay-1][0],
            bg=list_color[abs(whoplay-3)-1][0],
            text='Les '+list_color[whoplay-1][1]+' ont gagné')
        lab_end.pack(padx=5,pady=5)

        can.unbind('<Button-1>')
        fen.bind('<m>',restart)

        fen.mainloop()
    #Sinon, change la personne qui joue
    whoplay=abs(whoplay-3)

def restart(event):
    """
    Recommence une partie
    """
    print('prout')
    fen.destroy()
    puissance_4_jvj()


puissance_4_jvj()