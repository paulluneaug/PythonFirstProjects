import tkinter as tk
from random import randint,random

def play2048():
    """
    Lance une parte du jeu 2048
    """
    global dim,c,can,fen

    dim=4 #désigne le nombre de cases en hauteur et en largeur du plateau
    c=600//dim #définit la taille en pixels de chaque case
    width=c*dim #désigne la taille en pixels de la fenêtre du jeu
    height=width

    #créé la fenâtre du jeu et le canvas
    fen=tk.Tk()
    fen.title('2048')

    can=tk.Canvas(fen,width=width,height=height,bg='#BBADA0')
    can.pack()
    init()

    fen.mainloop()

def init():
    """
    Foncion qui initialise les différentes variables nécéssaires au programme
    et lie les flèches directionnelles aux bonnes fonctions
    """
    global dict_state
    dict_state={} #Initialise un dictionnaire ayant pour clef les coordonnées de
                  #chaque case et pour valeur, ce qu'il y a dans la case, 0 pour
                  #une case vide et un entier naturel pour tout autre case
    for x in range(dim):
        for y in range(dim):
            dict_state[x, y] = 0

    fen.bind('<Up>',up)
    fen.bind('<Right>',right)
    fen.bind('<Down>',down)
    fen.bind('<Left>',left)
    next_move()

def next_move():
    global dict_state
    #Dresse la liste de toutes les cases vides de la grille pour y ajouter une case
    list_blank=[]
    for x in range(dim):
        for y in range(dim):
            if dict_state[x,y]==0:
                list_blank.append((x,y))

    if len(list_blank)!=0:
        #Ajoute une case 2 ou 4 sur la grille si une case est libre
        if randprob(0.8):
            add=1
        else:
            add=2
        dict_state[list_blank[randint(0,len(list_blank)-1)]]=add
        can_maj()
    else:
        #sinon bloque le jeu et indique au joueur qu'il a perdu et 'délie'
        #les flèches des différentes fonctions
        can.create_text(c*dim/2,c*dim/2,text='Perdu',font='Verdana 80')
        for key in ['<Up>','<Right>','<Down>','<Left>']:
            fen.unbind(key)

def down(event):
    """
    Sépare la grille en colonnes, en supprime les 0, compacte les colonnes
    vers le bas puis remet les colonnes compactées à leur place
    """
    for xdo in range(dim):
        list_col0=[]
        for ydo in range(dim): #Sépare la grille en colonnes en enlevant les 0
            if dict_state[xdo,dim-1-ydo]!=0:
                list_col0.append(dict_state[xdo,dim-ydo-1])

        list_col=comp_list(list_col0)#Comapcte les colonnes
        #Remet les colonnes compactées à leur place
        for ydo in range (dim):
            if len(list_col)-1>=ydo:
                dict_state[xdo,dim-1-ydo]=list_col[ydo]
            else:
                dict_state[xdo,dim-1-ydo]=0
    next_move()

def left(event):
    """
    Sépare la grille en lignes, en supprime les 0, compacte les lignes
    vers la gauche puis remet les lignes compactées à leur place
    """
    for yle in range (dim):
        list_lin0=[]
        for xle in range (dim):#Sépare la grille en lignes en enlevant les 0
            if dict_state[xle,yle]!=0:
                list_lin0.append(dict_state[xle,yle])

        list_lin=comp_list(list_lin0)#Comapcte les lignes
        #Remet les lignes compactées à leur place
        for xle in range(dim):
            if len(list_lin)-1>=xle:
                dict_state[xle,yle]=list_lin[xle]
            else:
                dict_state[xle,yle]=0
    next_move()

def up(event):
    """
    Sépare la grille en colonnes, en supprime les 0, compacte les colonnes
    vers le haut puis remet les colonnes compactées à leur place
    """
    for xup in range(dim):
        list_col0=[]
        for yup in range(dim):#Sépare la grille en colonnes en enlevant les 0
            if dict_state[xup,yup]!=0:
                list_col0.append(dict_state[xup,yup])

        list_col=comp_list(list_col0)#Comapcte les colonnes
        #Remet les colonnes compactées à leur place
        for yup in range(dim):
            if len(list_col)-1>=yup:
                dict_state[xup,yup]=list_col[yup]
            else:
                dict_state[xup,yup]=0
    next_move()

def right(event):
    """
    Sépare la grille en lignes, en supprime les 0, compacte les lignes
    vers la droite puis remet les lignes compactées à leur place
    """
    for yri in range (dim):
        list_lin0=[]
        for xri in range (dim):#Sépare la grille en lignes en enlevant les 0
            if dict_state[dim-xri-1,yri]!=0:
                list_lin0.append(dict_state[dim-xri-1,yri])

        list_lin=comp_list(list_lin0)#Comapcte les lignes
        #Remet les lignes compactées à leur place
        for xri in range(dim):
            if len(list_lin)-1>=xri:
                dict_state[dim-1-xri,yri]=list_lin[xri]
            else:
                dict_state[dim-1-xri,yri]=0
    next_move()

def comp_list(list0):
    """
    Compacte la liste en argument en regroupant les couples valeurs identiques
    voisines et en en supprimant une et en ajoutant 1 à l'autre :
        Ex: [4, 2, 2] devient [4, 3]
            [3, 2, 2, 2, 2] devient [3, 3, 3]

    Arguments:
        -list0: type=list
            Liste représentant une ligne ou une colonne à compacter

    Returns:
        -list_comp: type=list
            Liste représentant une ligne ou une colonne compactée
    """
    list_comp=[]
    compactable=True #

    if len(list0)==1: #Elimine le cas où la liste ne compte qu'un seul élément
        list_comp=list0
    else:
        for i in range(len(list0)-1):

            if list0[i]==list0[i+1] and compactable: #Teste si l'élément i de la
                list_comp.append(list0[i]+1)         #liste et son voisin sont
                compactable=False                    #les mêmes et si on peut
                                                     #les compacter
            elif compactable :
                list_comp.append(list0[i])

            else:
                compactable=True

            if i==len(list0)-2 and compactable:
                list_comp.append(list0[i+1])

    return list_comp

def randprob(prob):
    """Renvoie True selon une certaine probabilité "prob"

    Arguments:
        prob: type = float or int ; 0 <= proba <= 1
            Probabilité de retourner True

    Return:
        tf: type = bool
            True ou False selon la probabilité "prob" et un tirage aléatoire
    """
    return random()<=prob



def can_maj():
    """
    Met à jour le canvas du jeu en fonction de dict_state
    """
    global dim,list_p
    can.delete(tk.ALL)
    list_tile_col=['#CDC0B4','#EEE4DA','#EDE0C8','#F2B179','#EC8D54','#EA5937',
        '#F3D86B','#F1D04B','#E4C02A','#E2BA13','#ECC400','#F46674','#F64F60',
        '#E9443E','#72B6DB','#5EA1E5','#107BBF']
    for x in range (dim):
        for y in range(dim):
            val_dic_xy=dict_state[x,y] #créé un carré sur le canevas pour chaque
                                       #case avec la couleur correspondant au
                                       #nombre de la case
            can.create_rectangle(c*(x+0.05),c*(y+0.05),c*(x+0.95),c*(y+0.95),
                fill=list_tile_col[val_dic_xy])

            if dict_state[x,y]!=0: #créé un texte sur le canevas pour chaque
                                   #case dont la valeur n'est pas 0 indiquant
                                   #la valeur de la case
                can.create_text(c*(x+0.5),c*(y+0.5),text=str(2**val_dic_xy),
                    font='Verdana '+str(40-val_dic_xy))



play2048()