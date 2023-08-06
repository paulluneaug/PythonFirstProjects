import tkinter as tk
from random import randint
from math import cos,sin,sqrt,pi

def play_pong_JvJ():
    """
    Lance une partie de Pong, joueur contre joueur

    Contrôles:
    ¯¯¯¯¯¯¯¯¯
        -Z pour monter la barre de gauche
        -S pour descendre la barre de gauche

        -Flèche haut pour monter la barre de droire
        -Flèche bas pour descendre la barre de droire
    """
    global can,x_can,y_can,barx,bary,c_ball,fen,bar_speed,lab_pts_p1,lab_pts_p2
    fen=tk.Tk()
    fen.title('Pong JvO')

    #Taille en pixel du Canevas
    x_can=800
    y_can=500

    #Moitié de la taille en largeur et en hauteur des barres
    barx=12
    bary=55

    c_ball=10 #Rayon de la balle
    bar_speed=5 #Nombre de pixels dont les barres se déplace à chaque nouveau
                #calcul de la position de tous les éléments du jeu

    fra_pts=tk.Frame(fen,width=x_can,height=80,bg='black')
    fra_pts.grid(column=0,row=0)
    fra_pts.pack_propagate(False)

    fra_pts1=tk.Frame(fra_pts,width=x_can//2,height=80,bg='black')
    fra_pts1.grid(column=0,row=0)
    fra_pts1.pack_propagate(False)

    fra_pts2=tk.Frame(fra_pts,width=x_can//2,height=80,bg='black')
    fra_pts2.grid(column=1,row=0)
    fra_pts2.pack_propagate(False)

    lab_pts_p1=tk.Label(fra_pts1,font='System 30',fg='#6699FF',bg='black',
        text='0')
    lab_pts_p1.pack(pady=15)

    lab_pts_p2=tk.Label(fra_pts2,font='System 30',fg='#FF6633',bg='black',
        text='0')
    lab_pts_p2.pack(pady=15)

    can=tk.Canvas(fen,width=x_can,height=y_can,bg='black')
    can.grid(column=0,row=1)

    fen.bind('<z>',up_p1_press)
    fen.bind('<s>',down_p1_press)
    fen.bind('<KeyRelease-z>',up_p1_release)
    fen.bind('<KeyRelease-s>',down_p1_release)

    fen.bind('<Up>',up_p2_press)
    fen.bind('<Down>',down_p2_press)
    fen.bind('<KeyRelease-Up>',up_p2_release)
    fen.bind('<KeyRelease-Down>',down_p2_release)

    init()

    fen.mainloop()

def middle_line(n):
    """
    Dessine sur le canevas une ligne de n pointillés

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        n : type=int
            Nombre de pointillés sur la ligne centrale
    """
    global can,x_can,y_can
    for a in range(n):
        can.create_line(x_can//2,(a+0.2)*y_can//n,x_can//2,(a+0.8)*y_can//n,
            fill='white',width=5)

def init():
    """
    Initialise les valeurs néccéssaires au jeu
    """
    global bar_p1,bar_p2,x_can,y_can,pts_p1,pts_p2,up_p1,down_p1,up_p2,down_p2
    padx=40 #Espace en pixel entre les barres et les bords latéraux du canevas
    pts_p1,pts_p2=0,0 #Points de chaque joueurs
    up_p1,down_p1=False,False
    up_p2,down_p2=False,False
    bar_p1=[padx,y_can//2] #Position de la première barre
    bar_p2=[x_can-padx,y_can//2] #Position de la seconde barre
    middle_line(10)
    new_ball()
    can_maj(True,True)
    f_play()


def new_ball():
    """
    Place une nouvelle balle au centre du canevaset lui attribue un nouveau
    vecteur
    """
    global ball,vect_ball,ball_color
    default_ball_speed=5 #Norme du vecteur qui guide la balle lors de sa création
    ball=[x_can//2,y_can//2] #Coordonnées de la balle
    angle=deg2rad(randint(-45,45)+180*randint(0,1)) #Angle selon lequel la balle part
    if -pi/2<angle<pi/2:
        ball_color='#6699FF'
    else:
        ball_color='#FF6633'
    #Coordonnées du vecteur que suit la balle
    vect_ball=[cos(angle)*default_ball_speed,sin(angle)*default_ball_speed]

def can_maj(move_p1,move_p2):
    """
    Met à jour le canevas

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        move_p1 : type=bool
            True si la première barre bouge
            False sinon

        move_p2 : type=bool
            True si la seconde barre bouge
            False sinon
    """
    global ball,bar_p1,bar_p2,can,x_can,y_can,barx,bary,c_ball
    #Supprime la balle du canevas puis la redessine à la bonne place
    can.delete("ball")
    can.create_oval(ball[0]-c_ball,ball[1]-c_ball,ball[0]+c_ball,
        ball[1]+c_ball,fill=ball_color,tag="ball")

    if move_p1:             #Si la première barre doit bouger, la supprime et
        can.delete("bar1")  #la redessine au bon endroit
        can.create_rectangle(bar_p1[0]-barx,bar_p1[1]-bary,bar_p1[0]+barx,
            bar_p1[1]+bary,fill='#6699FF',tag="bar1")

    if move_p2:             #Si la première barre doit bouger, la supprime et
        can.delete("bar2")  #la redessine au bon endroit
        can.create_rectangle(bar_p2[0]-barx,bar_p2[1]-bary,bar_p2[0]+barx,
            bar_p2[1]+bary,fill='#FF6633',tag="bar2")


def up_p1_press(event):
    global up_p1
    up_p1=True

def down_p1_press(event):
    global down_p1
    down_p1=True

def up_p1_release(event):
    global up_p1
    up_p1=False

def down_p1_release(event):
    global down_p1
    down_p1=False

def up_p2_press(event):
    global up_p2
    up_p2=True

def down_p2_press(event):
    global down_p2
    down_p2=True

def up_p2_release(event):
    global up_p2
    up_p2=False

def down_p2_release(event):
    global down_p2
    down_p2=False

def f_play():
    """
    Fonction qui gère le déplacement de tous les éléments
    """
    global ball,vect_ball,fen,c_ball,bar_p1,bar_p2,barx,bary,lab_pts_p1
    global pts_p1,pts_p2,lab_pts_p2,up_p1,down_p1,up_p2,down_p2,ball_color
    ball=[ball[0]+vect_ball[0],ball[1]+vect_ball[1]]
    max_speed=12 #Vitesse maximum de la balle

    if (ball[1]<=c_ball and vect_ball[1]<0) or (vect_ball[1]>0 and ball[1]>=y_can-c_ball):
        #Vérifie si la balle ne touche pas les bord supérieurs ou inferieurs
        norm=sqrt(vect_ball[0]**2+vect_ball[1]**2) # Calcul de la norme du vecteur que suivait la balle
        if norm*1.05<max_speed:
            vect_ball[0]*=1.05
            vect_ball[1]*=1.05

        vect_ball[1]=-vect_ball[1] #Alors, inverse l'ordonnée du vecteur


    #----------------------------Collision avec les barres----------------------
    if bar_p1[1]-bary-c_ball<=ball[1]<=bar_p1[1]+bary+c_ball and ball[0]-c_ball<=bar_p1[0]+barx:
        #On vérifie si la balle ne nouche pas la barre de gauche
        xc,yc=ball[0]-c_ball,ball[1] #C est le point de collision entre la balle et la barre
        xp,yp=bar_p1[0],bar_p1[1]+(yc-bar_p1[1])*0.7 #P est un point par rapport auquel la balle va rebondir
        mult=sqrt(vect_ball[0]**2+vect_ball[1]**2) # Calcul de la norme du vecteur que suivait la balle
        if mult*1.05<max_speed:
            mult*=1.05
        mult/=sqrt((xc-xp)**2+(yc-yp)**2) # Calcul de CP
        vect_ball=[(xc-xp)*mult,(yc-yp)*mult] #Mise à jour des coordonnées du vecteur qui guide la balle
        ball_color='#6699FF'
        
    elif bar_p2[1]-bary-c_ball<=ball[1]<=bar_p2[1]+bary+c_ball and ball[0]+c_ball>=bar_p2[0]-barx:
        #On vérifie si la balle ne nouche pas la barre de droite
        xc,yc=ball[0]+c_ball,ball[1] #C est le point de collision entre la balle et la barre
        xp,yp=bar_p2[0],bar_p2[1]+(yc-bar_p2[1])*0.7 #P est un point par rapport auquel la balle va rebondir
        mult=sqrt(vect_ball[0]**2+vect_ball[1]**2) # Calcul de la norme du vecteur que suivait la balle
        if mult*1.05<max_speed:
            mult*=1.05
        mult/=sqrt((xc-xp)**2+(yc-yp)**2) # Calcul de CP
        vect_ball=[(xc-xp)*mult,(yc-yp)*mult] #Mise à jour des coordonnées du vecteur qui guide la balle
        ball_color='#FF6633'

    #---------------------Vérification de buts----------------------------------
    if 0>=ball[0]:#Vérifie si la balle est passée derrière la barre de gauche
        pts_p2+=1 #Ajoute un point au joueur
        lab_pts_p2.configure(text=str(pts_p2))
        new_ball()#Place une nouvelle balle

    elif ball[0]>=x_can:#Vérifie si la balle est passée derrière la barre de droite
        pts_p1+=1 #Ajoute un point à l'ordinateur
        lab_pts_p1.configure(text=str(pts_p1))
        new_ball()#Place une nouvelle balle


    #---------------------Déplacements de la barre gauche-----------------------
    if up_p1: #Si le joueur 1 appuie sur haut
        if bary+10<=bar_p1[1]:
            bar_p1[1]-=bar_speed #Monte la barre du joueur 1
            move_p1=True #Indique qu'il faut actualiser cette barre
        else:
            move_p1=False

    elif down_p1:#Si le joueur 1 appuie sur bas
        if bar_p1[1]<=y_can-bary-10:
            bar_p1[1]+=bar_speed #Baisse la barre du joueur 1
            move_p1=True #Indique qu'il faut actualiser cette barre
        else:
            move_p1=False
    else:
        move_p1=False

    #---------------------Déplacements de la barre droite-----------------------
    if up_p2: #Si le joueur 2 appuie sur haut
        if bary+10<=bar_p2[1]:
            bar_p2[1]-=bar_speed #Monte la barre du joueur 2
            move_p2=True #Indique qu'il faut actualiser cette barre
        else:
            move_p2=False

    elif down_p2:#Si le joueur 2 appuie sur bas
        if bar_p2[1]<=y_can-bary-10:
            bar_p2[1]+=bar_speed #Baisse la barre du joueur 2
            move_p2=True #Indique qu'il faut actualiser cette barre
        else:
            move_p2=False
    else:
        move_p2=False


    can_maj(move_p1,move_p2)
    fen.after(15,f_play)

def deg2rad(deg):
    """
    Convertit un angle en degrés en radians

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        deg : type=int ou float
            mesure de l'angle à convertir en degrés

    Returns:
    ¯¯¯¯¯¯¯
        rad : type=int ou float
            mesure de l'angle converti en radians

    """
    return (deg/360*2*3.1415926535)

play_pong_JvJ()