from datetime import datetime, time
import tkinter as tk
from math import sqrt,log
import graphic_module as graph
import laser_module as las
import useful_module as use
from random import randrange,shuffle

"""
Jeu de plateforme deux joueurs
Le but du jeu est de completer tous les tableaux en allant du portail bleu au portail orange
"""
dict_levels={'tutorial':['Zykouland','tuto 2 Jump','tuto 3 Spike','tuto5 keys','dash','discover'],
             1:['gypso','laser and receptor','le_conseil_du_vieux_sage'],
             2:['poulpidou','maze (Press R to respawn)'],
             3:['snake','Zykouland']}

class Player:
    """
    Classe créant et gérant un personnage jouable d'un platformer
    """

    def __init__(self,x,y,width=1,height=2,velocity=5):

        self._gravity=c_main//2

        #Dictionnaire des différents vecteurs qui s'appliquent sur le joueur
        self._vector={'right':[0,0],'jump':[0,0],'gravity':[0,self._gravity],
                      'reaction':[0,0],'left':[0,0]}

        #Dictionnaire des intentions du joueur
        self._wanna_go={'right':False,'left':False,'up':False,'sneak':False}

        self._position=[x,y] #Coordonnées du joueur
        self._last_checkpoint=[x,y] #Coordonnées du dernier checkpoint

        self._max_life=10
        self._life=5

        self._velocity=velocity #Vitesse du joueur
        self._speed_mult=1 #Mutiplicateur de vitesse pour si le joueur est sur
                           #une surface d'acceleration
        self._height=height #Hauteur
        self._width=width #Largeur
        self._sneak_height=height-1
        self._default_height=height

        self.create_list_collisions()

        self._can_wall_jump=False #Capacité du joueur à sauter sur les murs

        self._gravity_multiplier=0.8 #Nombre par lequel le vecteur saut est
                                     #multiplié à chaque frame

        self._jump_multiplier=1 #Multiplicateur de la hauteur du saut du joueur
                                #modifié si je joueur est sur une surface de
                                #modification de la hauteur de saut

        self._default_jump_height=5.1 #Nombre de blocs en hauteur que le joueur
                                      #peut atteindre en sautant, par défaut

        self._jump_height=self._default_jump_height
        self.calc_jump_speed(self._jump_height) # Vitesse de saut

        self._max_jump=1 #Nombre de saut que le joueur peut enchaîner sans
                         #toucher le sol ou un mur (si il peut wall jump)
        self._jump_left=self._max_jump

        self._dir=(1,0) #Direction du joueur
        self._dash_cooldown=[0,fps//1.5] #Cooldown du dash
        self._dash_lenght=[0,fps//14]#Nombre de frames pendant lesquelles
                                     #le joueur est soumis au dash

        self._stored_vectors={'dash':[0,0]}


    def __repr__(self):
        return f'Joueur de {self._width} blocs de largeur et de {self._height} blocs de hauteur et positionné en {self._position}'

    def set_position(self,new_pos):
        """
        Attribue des nouvelles coordonnées au joueur
        """
        self._position=new_pos

    def get_position(self):
        """
        Renvoie les coordonnées du joueur
        """
        return self._position

    def get_height(self):
        """
        Renvoie la hauteur du joueur
        """
        return self._height

    def get_width(self):
        """
        Renvoie la largeur du joueur
        """
        return self._width

    def create_list_collisions(self):
        """
        Créé la liste des blocs avec lesquels le joueur est en contact et une
        autre liste avec leurs coordonnées

        Cette liste se présente sous la forme de plusieurs listes, représentant
        chaque étage du joueur : un pour le dessus du joueur, un pour chaque
        case en hauteur qu'il fait et un pour le dessous du joueur

        Chacun de ces étages est composé d'une liste d'arrêtes. Les étages
        du haut et du bas contiennent autant d'arrêtes que de cases en
        largeur du joueur. Les autres en ont 2 (un pour la droite, un pour
        la gauche

        Les arrêtes sont des listes composées des cases ou des coordonnées avec
        lesquelles l'arrête est en contact
        """
        #Liste du nombre d'arrete par étage du joueur
        list_nbr_arrete=[self._width]+self._height*[2]+[self._width]

        #Listes contenant le bon nombre de sous listes, mais vides
        list_collisions=[[[] for _ in range(µ)] for µ in list_nbr_arrete]
        list_collisions_coor=[[[] for _ in range(µ)] for µ in list_nbr_arrete]

        #Si le joueur est à cheval sur 2 cases en abscisse, les arretes en haut
        #et en bas seront à cheval sur 2 cases et donc, de longueur 2
        len_arrete_top_bot=2
        add_side=0
        if self._position[0]==int(self._position[0]):
            len_arrete_top_bot=1
            add_side=1

        if self._position[0]<0:
            add_x=-1
        else:
            add_x=0

        #Si le joueur est à cheval sur 2 cases en ordonnée, les arretes à
        #gauche et à droite et en bas seront à cheval sur 2 cases et donc,
        #de longueur 2
        len_arrete_side=2
        add_top=0
        if self._position[1]==int(self._position[1]):
            len_arrete_side=1
            add_top=1


        for etage in range(len(list_collisions)): #Passe en revue chaque arrête
            for arrete in range(len(list_collisions[etage])): #de chaque étage

                if etage==0: #Pour le haut du joueur
                    arrete_temp=[]
                    arrete_temp_coor=[]
                    for a in range(len_arrete_top_bot): #Pour le nombre
                        #d'élément qu'il doit y avoir dans ces arrêtes
                        key=(int(self._position[0]+arrete+a),int(self._position[1]-self._height-add_top))
                        if key in level:
                            #Vérifie si le le haut du joueur est toujours dans
                            #le niveau

                            #Ajoute à une liste la case qu'il touche
                            arrete_temp.append(level[key])

                            #Et à une autres, ses coordonnées
                            arrete_temp_coor.append(list(key))
                        else: #Bloque le joueur s'il sort du niveau
                            arrete_temp.append('block')
                            arrete_temp_coor.append(None)

                    list_collisions[etage][arrete]=arrete_temp
                    list_collisions_coor[etage][arrete]=arrete_temp_coor

                elif etage==len(list_collisions)-1: #Pour le bas du joueur
                    arrete_temp=[]
                    arrete_temp_coor=[]
                    for b in range(len_arrete_top_bot):#Pour le nombre
                        #d'élément qu'il doit y avoir dans ces arrêtes
                        key=(int(self._position[0]+arrete+b),int(self._position[1]))
                        if key in level:
                            #Vérifie si le bas du joueur est toujours dans
                            #le niveau

                            #Ajoute à une liste la case qu'il touche
                            arrete_temp.append(level[key])

                            #Et à une autres, ses coordonnées
                            arrete_temp_coor.append(list(key))
                        else: #Bloque le joueur s'il sort du niveau
                            arrete_temp.append('block')
                            arrete_temp_coor.append(None)

                    list_collisions[etage][arrete]=arrete_temp
                    list_collisions_coor[etage][arrete]=arrete_temp_coor

                else :
                    if arrete==0: #Pour la gauche du joueur
                        arrete_temp=[]
                        arrete_temp_coor=[]
                        for c in range(len_arrete_side):#Pour le nombre
                            #d'élément qu'il doit y avoir dans ces arrêtes
                            key=(int(self._position[0]-add_side)+add_x,int(self._position[1]-(self._height-etage+add_top)-c))
                            if key in level:
                                #Vérifie si la gauche du joueur est toujours
                                #dans le niveau

                                #Ajoute à une liste la case qu'il touche
                                arrete_temp.append(level[key])

                                #Et à une autres, ses coordonnées
                                arrete_temp_coor.append(list(key))

                            else: #Bloque le joueur s'il sort du niveau
                                arrete_temp.append('block')
                                arrete_temp_coor.append(None)

                        list_collisions[etage][arrete]=arrete_temp
                        list_collisions_coor[etage][arrete]=arrete_temp_coor

                    else: #Pour la droite du joueur
                        arrete_temp=[]
                        arrete_temp_coor=[]
                        for d in range(len_arrete_side):#Pour le nombre
                            #d'élément qu'il doit y avoir dans ces arrêtes
                            key=(int(self._position[0]+arrete*list_nbr_arrete[0]),int(self._position[1]-(self._height-etage+add_top)-d))
                            if key in level:
                                #Vérifie si la droite du joueur est toujours dans
                                #le niveau

                                #Ajoute à une liste la case qu'il touche
                                arrete_temp.append(level[key])

                                #Et à une autres, ses coordonnées
                                arrete_temp_coor.append(list(key))
                            else: #Bloque le joueur s'il sort du niveau
                                arrete_temp.append(None)
                                arrete_temp_coor.append(None)

                        list_collisions[etage][arrete]=arrete_temp
                        list_collisions_coor[etage][arrete]=arrete_temp_coor

        self._list_collisions=list_collisions
        self._list_collisions_coor=list_collisions_coor

    def respawn(self):
        """
        Fait réapparaître le joueur au dernier checkpoint, annule tous les
        vecteurs auxquels il est soumis, lui enlève une vie et recharge le
        niveau au complet
        """
        global level,i_level,timed_block_cooldown
        graph.can_update(can_main, ["player"],level, c_main,list_players=list_players)
        self.set_position(self._last_checkpoint)
        list_vect2keep=['gravity'] #Liste des vecteurs que l'on ne doit pas
                                   #annuler
        for vect in self._vector.keys():
            if vect not in list_vect2keep:
                self._vector[vect]=[0,0]

        timed_block_cooldown=0

        self._life-=1
        if self._life==0:
            self.refill_life()
            i_level=i_level-i_level%5-1
            death_screen()

        else:

            level=eval(open(f'{level_name}.txt','r').read())
            level=las.update_lasers(level,can_main,c_main)
            graph.can_update(can_main,['all','name','hearts'],level,c_main,x_can=x_can,y_can=y_can,level_name=level_name,list_players=list_players)

    def refill_life(self):
        """
        Redonne de la vie au joueur
        """
        self._life=self._max_life

    def calc_jh(self,tos,grav,mult):
        """
        Calcule la hauteur d'un saut en fonction d'une vitesse initiale,
        d'un multiplicateur de saut et de la gravité

        Arguments:
        ¯¯¯¯¯¯¯¯¯
            tos : type=int or float
                Norme initiale du vecteur de saut

            grav : type=int or float
                Norme du vecteur gravité

            mult : type=float ; 0<mult<1
                Nombre par lequel le vecteur saut est multiplié à chaque frame

        Returns:
        ¯¯¯¯¯¯¯
            jh : type=int or float
                Hauteur du saut

        """
        n=int(log(grav/tos)/log(mult))+1

        jh=(tos*((mult**(n)-1)/(mult-1)))-n*grav

        return jh

    def calc_jump_speed(self,jh_wanted):
        """
        Calcule la norme initiale du vecteur saut pour une hauteur de saut
        voulue par dichotomie

        Arguments:
        ¯¯¯¯¯¯¯¯¯
            jh_wanted : type=int or float
                Hauteur de saut voulue
        """
        jh_wanted*=c_main

        #Définit les bornes de la recherche
        a,b,m=self._gravity+1,2000,1000

        #Calcule la hauteur de saut en fonction de la vitesse m
        jh_m=self.calc_jh(m,self._gravity,self._gravity_multiplier)
        while not jh_wanted-10**(-9)<=jh_m<=jh_wanted+10**(-9):
            #Applique la dichotomie

            if jh_m<jh_wanted:
                a=m
            else:
                b=m
            m=(a+b)/2
            jh_m=self.calc_jh(m,self._gravity,self._gravity_multiplier)
            
        self._jump_speed=m+1


    def set_jump_height(self,height):
        """
        Met à jour la hauteur de saut du joueur
        """
        self._jump_height=height
        self.calc_jump_speed(height)


def platformer(level_n=None,demo=False,nb_players=1):
    global x_can,y_can,c_main,can_main,fps,fen_plat,list_players,list_levels, i_level
    global level,level_name,timed_block_cooldown,list_t_blocks,img_nb,capt
    global dict_levels
    if demo:
        x_can,y_can=15,10
    else:
        x_can,y_can=60,30 #Nombre de cases en hauteur et largeur du canvas
    c_main=1300//max(x_can,y_can) #Taille en pixels de chaque case
    i_level=0 #Indice de la liste des niveaux correspondant au niveau que le joueur est en train de faire

    #Dictionnaire des niveaux, les clefs sont les difficultés et les valeurs,
    #une liste de noms de niveaux
    
    if demo:
        dict_levels={'demo':['demo1 Mouvements','demo2 Mort','demo3 OneWayBlock+R',
                             'demo4 Modificateurs de Saut et de Vitesse',
                             'demo5 Portes et Clefs','demo6 Blocs Cassables et Chronométrés',
                             'demo7 Blocs On-Off','demo8 Lasers, Miroirs et Boutons',
                             'demo9 Récepteurs Laser']}
    elif level_n=='temp':    
        dict_levels={0:['temp']}
    list_levels=dict_to_list_level(dict_levels)

    level_name=list_levels[i_level]
    level=eval(open(f'{level_name}.txt','r').read())

    img_nb=0
    capt=False

    #Recherche le portail d'entré les plus bas dans le niveau pour y faire
    #apparaître le joueur
    portal_height=0
    portal_co=None
    for k in level.keys():
        if level[k][0]=='portal-in' and portal_height<k[1]:
            portal_height=k[1]
            portal_co=[k[0],k[1]+1]


    fps=70 #Nombre de fois par secondes où l'état du jeu est calculé

    timed_block_cooldown=0
    list_t_blocks=sort_timed_blocks(level)

     #Création du joueur
    list_players=[Player(portal_co[0],portal_co[1],width=1,height=2,velocity=c_main//3) for x in range(nb_players)]

    fen_plat=tk.Tk()
    fen_plat.title('Platformer')

    can_main=tk.Canvas(fen_plat,width=x_can*c_main,height=y_can*c_main,bg='white')
    can_main.pack()

    level=las.update_lasers(level,can_main,c_main)
    graph.can_update(can_main,['all','player','hearts','name'],level,c_main,list_players=list_players,x_can=x_can,y_can=y_can,level_name=level_name)

    play()

    fen_plat.bind('<space>',lambda x:jump(0,0))
    fen_plat.bind('<Up>',lambda x:jump(0,0))

    fen_plat.bind('<Left>',lambda x:key_press('left',0))
    fen_plat.bind('<KeyRelease-Left>',lambda x:key_release('left',0))

    fen_plat.bind('<Right>',lambda x:key_press('right',0))
    fen_plat.bind('<KeyRelease-Right>',lambda x:key_release('right',0))

    fen_plat.bind('<Down>',lambda x:key_press('sneak',0))
    fen_plat.bind('<KeyRelease-Down>',lambda x:key_release('sneak',0))
    
    fen_plat.bind('<space>',lambda x:jump(0,1))
    fen_plat.bind('<z>',lambda x:jump(0,1))

    fen_plat.bind('<q>',lambda x:key_press('left',1))
    fen_plat.bind('<KeyRelease-q>',lambda x:key_release('left',1))

    fen_plat.bind('<d>',lambda x:key_press('right',1))
    fen_plat.bind('<KeyRelease-d>',lambda x:key_release('right',1))

    fen_plat.bind('<s>',lambda x:key_press('sneak',1))
    fen_plat.bind('<KeyRelease-s>',lambda x:key_release('sneak',1))

    fen_plat.bind('<!>',lambda x:dash(0,0))
    fen_plat.bind('<a>',lambda x:dash(0,1))
    fen_plat.bind('<r>',lambda x:respawn(0,0))
    fen_plat.bind('<r>',lambda x:respawn(0,1))
    fen_plat.bind('<c>',capture)

    fen_plat.protocol('WM_DELETE_WINDOW', destroy_fen)
    fen_plat.mainloop()



def play():
    """
    Boucle principale
    """
    global level,timed_block_cooldown,after_id,img_nb
    #Liste des blocs arrêtant le joueur
    list_stops=[['block'],['door'],['breakable-block'],['speed-up'],['bounce'],
                ['slow-down'],['sticky'],['laser-emitter'],['on-block',True],
                ['off-block',True],['timed-block',True],['on-off-switch'],
                ['mirror'],['glass'],['button'],['laser-reciever'],
                ['on-off-door',True]]


    frameStart = datetime.now()

    list_kills=[['spike']]


    dict_on_off={'on':'off','off':'on'}
    
    list_t2update=[] #Liste des cases à actualiser
    laser_2_update=False

    for player in list_players:
    
        player.create_list_collisions()
    
        #Vérifie si le joueur a une case 'checkpoint' dans sa liste de collision
        is_on_checkpoint,check_co=use.in_sub_list('checkpoint',player._list_collisions)
    
        if is_on_checkpoint: #Si oui, change les coordonnés du checkpoint du joueur
            j,k,l,o=tuple(check_co)
            check_co=player._list_collisions_coor[j][k][l]
            player._last_checkpoint=[check_co[0],check_co[1]+1]
    
    
    
        if player._dash_lenght[0] in (player._dash_lenght[1],1):
            player._vector,player._stored_vectors=player._stored_vectors,player._vector
    
        if len(player._vector)!=1:
            if player._wanna_go['left']: #Si je joueur appuie sur la touche pour aller à gauche
                player._vector['left']=[-player._velocity*player._speed_mult,0] #
                player._dir=(-1,0) #Change sa direction
            else:
                player._vector['left']=[0,0] #Sinon, annule le vecteur de gauche
    
    
            if player._wanna_go['right']: #Si je joueur appuie sur la touche pour aller à droite
                player._vector['right']=[player._velocity*player._speed_mult,0]
                player._dir=(1,0) #Change sa direction
            else:
                player._vector['right']=[0,0] #Sinon, annule le vecteur de gauche
    
        if player._wanna_go['sneak']: #Si le joueur veut d'accroupir
            player._height=player._sneak_height #Baisse sa hauteur à 1
            player._speed_mult=1/3
    
        elif player._height!=player._default_height: #Sinon, si le joueur ne veut pas s'accroupir mais qu'il n'est pas relevé
    
            can_go=not (True in [True in [['one-way-block','down'] == block[:2] if len(block)>=2 else False for block in arrete] for arrete in player._list_collisions[0]])
            for item in list_stops: #Vérifie au dessus de sa tête si il y a un bloc qui l'empêche de se relever
                can_go=can_go and not (True in [True in [item == block[:len(item)] for block in arrete if len(block)>=len(item)] for arrete in player._list_collisions[0]])
                if not can_go:
                    break
    
            if can_go: #Si'il n'y en a pas
                player._height=player._default_height #Augmente sa taille à 2
                player._speed_mult=1
    
        #Somme des vecteurs qui s'appliquent sur le joueur
        vect=use.sum_vector([vector for vector in player._vector.values()])
    
        #Norme de ce vecteur
        norm_vect=int(sqrt(vect[0]**2+vect[1]**2))+1
    
    
        step=1
    
    
        broke=False
    
        for n in range(0,norm_vect,step):
    
            player.create_list_collisions()
    
            list_can_go=4*[True] #Liste des directions dans lequel le joueur peut aller
            #----------------------------------------------------------------------
            if vect[1]<0: #Si vect va vers le haut
    
                list_stops.append(['one-way-block','down'])
                can_go=True
                for item in list_stops:#Vérifie s'il n'y a pas de blocs qui
                                              #arretent le joueur au dessus de lui
    
                    can_go=can_go and not (True in [True in [item == block[:len(item)] for block in arrete if len(block)>=len(item)] for arrete in player._list_collisions[0]])
    
                list_stops.pop(-1)
    
                if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                               #pas aller plus haut
                    player._vector['jump']=use.sum_vector([player._vector['gravity']],multiplier=-1)
                    list_can_go[0]=False #Indique qu'il ne peut pas aller en haut
    
    
                #Tant qu'il y a des blocs cassables au dessus de la tête du joueur
                while (True in [['breakable-block'] in arrete for arrete in player._list_collisions[0]]):
                    t,b_block=use.in_sub_list(['breakable-block'],player._list_collisions[0])
    
                    r,s=tuple(b_block) #Récupère leurs coordonnées et les supprime
                    level[tuple(player._list_collisions_coor[0][r][s])]=[None]
    
                    #Ajoute ces coordonnées à la liste des cases à actualiser
                    list_t2update.append(tuple(player._list_collisions_coor[0][r][s]))
    
                    #Recréé la liste des collisions du joueur pour prendre en
                    #compte la disparition des blocs cassbles
                    player.create_list_collisions()
                    laser_2_update=True
    
                broke=False
                #Vérifie parmi tous les blocs au dessus du personnage qui puissent le tuer
                for b in list_kills:
                    if True in [True in [b == block[:len(b)] for block in arrete if len(block)>=len(b)] for arrete in player._list_collisions[0]]:
                        player.respawn()
                        list_t2update.append('hearts')
                        broke=True
                        break
    
                if broke:
                    break
    
    
    
            #----------------------------------------------------------------------
            if vect[0]>0: #Si vect va vers la droite
                list_stops.append(['one-way-block','left'])
                can_go=True
                for item in list_stops:#Vérifie s'il n'y a pas de blocs qui
                                              #arretent le joueur au dessus de lui
                    can_go=can_go and not (True in [True in [item == block[:len(item)] for block in arrete if len(block)>=len(item)] for arrete in [player._list_collisions[y][1] for y in range(1,1+player.get_height())]])
                    if not can_go:
                        break
    
                list_stops.pop(-1)
    
                if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                               #pas aller plus haut
                    player._vector[list(player._vector.keys())[0]]=[0,0]
                    list_can_go[1]=False #Indique qu'il ne peut pas aller en haut
                    if player._can_wall_jump:
                        player._jump_left=player._max_jump
    
                broke=False
                #Vérifie parmi tous les blocs à la droite du personnage qui puissent le tuer
                for b in list_kills:
                    if True in [True in [b == block[:len(b)] for block in arrete if len(block)>=len(b)] for arrete in [player._list_collisions[y][1] for y in range(1,1+player.get_height())]]:
                        player.respawn()
                        list_t2update.append('hearts')
                        broke=True
                        break
    
                if broke:
                    break
    
    
                if True in [['portal-out','right'] in player._list_collisions[y][1] for y in range(1,1+player.get_height())] and player.get_position()[0]-int(player.get_position()[0])>0.8:
                    next_level()
    
            #----------------------------------------------------------------------
            if vect[1]>0: #Si vect va vers le bas
    
                list_stops.append(['one-way-block','up'])
                can_go=True
                for item in list_stops:#Vérifie s'il n'y a pas de blocs qui
                                              #arretent le joueur au dessus de lui
    
                    can_go=can_go and not (True in [True in [item == block[:len(item)] for block in arrete if len(block)>=len(item)] for arrete in player._list_collisions[-1]])
    
                list_stops.pop(-1)
    
                if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                               #pas aller plus haut
                    player._vector['jump']=use.sum_vector([player._vector['gravity']],multiplier=-1)
                    list_can_go[0]=False #Indique qu'il ne peut pas aller en haut
    
    
                broke=False
                #Vérifie parmi tous les blocs en dessous du personnage qui puissent le tuer
                for b in list_kills:
                    if True in [True in [b == block[:len(b)] for block in arrete if len(block)>=len(b)] for arrete in player._list_collisions[-1]]:
    
                        player.respawn()
                        list_t2update.append('hearts')
                        broke=True
                        break
    
                if broke:
                    break
    
                if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                               #pas aller plus bas en appliquant un vecteur opposé
                               #à la gravité sur le joueur
                    player._vector['reaction']=use.sum_vector([player._vector['gravity']],multiplier=-1)
    
                    player._vector['jump']=[0,0] #Annule le vecteur saut
    
                    #Remet dans son état initial le nombre de saut qu'il reste
                    #au joueur
                    player._jump_left=player._max_jump
                    list_can_go[2]=False
    
                    #Si un bloc accélérant ou déccélérant le personnage se situe en dessous de lui, applique la bonne vitesse au personnage
                    if True in [['speed-up'] in arrete for arrete in player._list_collisions[-1]]:
                        player._speed_mult=3
                    elif player._height==player._default_height:
                        player._speed_mult=1
    
                    if True in [['slow-down'] in arrete for arrete in player._list_collisions[-1]]:
                        if player._speed_mult!=3 or player._height!=player._default_height:
                            player._speed_mult=1/3
                        else :
                            player._speed_mult=1
    
                else:
                    player._vector['reaction']=[0,0]
            else:
                player._vector['reaction']=[0,0]
    
    
            #----------------------------------------------------------------------
            if vect[0]<0: #Si vect va vers la gauche
                list_stops.append(['one-way-block','right'])
                can_go=True
                for item in list_stops:#Vérifie s'il n'y a pas de blocs qui
                                              #arretent le joueur au dessus de lui
                    can_go=can_go and not (True in [True in [item == block[:len(item)] for block in arrete if len(block)>=len(item)] for arrete in [player._list_collisions[y][0] for y in range(1,1+player.get_height())]])
                    if not can_go:
                        break
    
                list_stops.pop(-1)
    
                if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                               #pas aller plus haut
                    player._vector[list(player._vector.keys())[0]]=[0,0]
                    list_can_go[1]=False #Indique qu'il ne peut pas aller en haut
                    if player._can_wall_jump:
                        player._jump_left=player._max_jump
    
                broke=False
    
                for b in list_kills:
                    if True in [True in [b == block[:len(b)] for block in arrete if len(block)>=len(b)] for arrete in [player._list_collisions[y][0] for y in range(1,1+player.get_height())]]:
    
                        player.respawn()
                        list_t2update.append('hearts')
                        broke=True
                        break
    
                if broke:
                    break
    
    
                if True in [['portal-out','right'] in player._list_collisions[y][0] for y in range(1,1+player.get_height())] and player.get_position()[0]-int(player.get_position()[0])<0.2:
                    next_level()
    
    
            #----------------------------------------------------------------------
    
            if las.check_laser_kills(level, player):
                player.respawn()
                break
    
            #Met à jour la position du joueur
            player.set_position([player.get_position()[0]+step*(vect[0]/norm_vect)/c_main,player.get_position()[1]+step*(vect[1]/norm_vect)/c_main])
    
            #Si le joueur est arreté par un bloc au dessus ou en dessous de lui,
            #on le réaligne sur la grille
            if not(list_can_go[0] and list_can_go[2]):
                player.set_position([player.get_position()[0],round(player.get_position()[1])])
    
            #Si le joueur est arreté par un bloc à gauche ou à droite de lui,
            #on le réaligne sur la grille
            if not(list_can_go[1] and list_can_go[3]):
                player.set_position([round(player.get_position()[0]),player.get_position()[1]])
    
            if n%(c_main)==0:
                graph.can_update(can_main,['player'],level,c_main,list_players=list_players)
    
        if not broke:
            #Cherche des clefs autour du joueur
            in_l,path=use.in_sub_list('key',player._list_collisions)
    
            if in_l: #S'il y en a,
                a,b,c,o=tuple(path) #Récupère les coordonnées
                key_co=tuple(player._list_collisions_coor[a][b][c])
    
                if level[key_co][0]=='key':
                    #Récupère le channel de cette clef
                    key_channel=level[key_co][1]
    
                    level[key_co]=[None] #La supprime
                    list_t2update.append(key_co)
    
                    for k in level.keys(): #Vérifie pour chaque case, si c'est une
                                           #porte avec le même channel
                        if level[k]==['door',key_channel]:
                            level[k]=[None] #Supprime ces portes
                            list_t2update.append(k)
                            laser_2_update=True
            
            if vect[1]<0:
                #Cherche des boutons au dessus du joueur
                but_in_l,path=use.in_sub_list('button',player._list_collisions[0])
                if but_in_l:
                    t,u,o=tuple(path)
                    but_co=tuple(player._list_collisions_coor[0][t][u])
    
                    list_t2update,laser_2_update,level=las.switch_button(level[but_co][1],list_t2update,laser_2_update,level)
    
                #Cherche des boutons au dessus du joueur
                switch_in_l,path=use.in_sub_list('on-off-switch',player._list_collisions[0])
    
                if switch_in_l:
                    t,u,o=tuple(path)
                    switch_co=tuple(player._list_collisions_coor[0][t][u])
    
                    list_t2update,laser_2_update,level=las.switch_on_off(dict_on_off[level[switch_co][1]],list_t2update,laser_2_update,level)
    
    
            #Recherche les coeurs autour du joueur
            in_l,path=use.in_sub_list(['heart'],player._list_collisions)
            
            if in_l and player._life<player._max_life: #S'il y en a
                a,b,c=tuple(path) #Récupère les coordonnées
                heart_co=tuple(player._list_collisions_coor[a][b][c])
    
                level[heart_co]=[None] #Le supprime
                list_t2update.append(heart_co)
                list_t2update.append('hearts')
    
                player._life+=1 #Ajoute une vie au joueur
    
   
    
        #Diminue le vecteur saut
        if 'jump' in player._vector:
            player._vector['jump']=use.sum_vector([player._vector['jump']],multiplier=player._gravity_multiplier)
    
        if player._dash_cooldown[0]!=0:
            player._dash_cooldown[0]-=1
        if player._dash_lenght[0]!=0:
            player._dash_lenght[0]-=1
 
    #Change l'état des blocs chronométrés dont la valeur interne
    #est la même que la variable qui compte le nombre de frames modulo 60
    if list_t_blocks[timed_block_cooldown]!=[]:
        for t_block in list_t_blocks[timed_block_cooldown]:
            level[t_block][1]=not level[t_block][1]
        list_t2update+=list_t_blocks[timed_block_cooldown]
        laser_2_update=True

    timed_block_cooldown=(timed_block_cooldown+1)%60

    #Met à jour les lasers si besoin
    if laser_2_update:
        level=las.update_lasers(level,can_main,c_main)

    graph.can_update(can_main,del_double(list_t2update),level,c_main,list_players=list_players) #Met à jour toutes les cases qu'il faut

    graph.can_update(can_main,['player'],level,c_main,list_players=list_players) #Met à jour le sprite du joueur
   
    if capt:
        c1,c2,c3,c4=285,40,1625,930
        # screenshot=ImageGrab.grab(bbox=(c1,c2,c3,c4))
        # screenshot.crop((left, top, right, bottom))
        # screenshot.save(f'Screenshots/screenshot{img_nb}.png','PNG')
        img_nb+=1

    after_id=fen_plat.after(int(use.clamp(((1000//fps) - ((datetime.now() - frameStart).total_seconds()*1000)), 0, (1000//fps))), play)
    # fen_plat.after(5,play)

def capture(event):
    global capt
    capt=not capt

def key_release(key,i_player):
    list_players[i_player]._wanna_go[key]=False

def key_press(key,i_player):
    if not list_players[i_player]._wanna_go[key]:
        list_players[i_player]._wanna_go[key]=True

def jump(event,i_player):
    """
    Fait sauter le joueur
    """
    player=list_players[i_player]
    if player._jump_left>0 and not 'dash' in player._vector:
        #Vérifie que le joueur n'est pas en train de s'élancer et qu'il lui reste des sauts

        i_mult=0

        #Diminue le multiplicateur de saut si le personnage est baissé
        if player._height==player._sneak_height:
            i_mult-=1
        #Ou sur une surface collante
        if True in [['sticky'] in arrete for arrete in player._list_collisions[-1]]:
            i_mult-=1
        #Mais l'augmente si la surface fait sauter plus haut
        if True in [['bounce'] in arrete for arrete in player._list_collisions[-1]]:
            i_mult+=1

        if player._jump_height!=player._default_jump_height*(2**i_mult):
            player.set_jump_height(player._default_jump_height*(2**i_mult))



        player._vector['jump']=[0,-player._jump_speed]
        player._jump_left-=1
        player._vector['reaction']=[0,0]

def dash(event,i_player):
    """
    Fait dasher le joueur
    """
    player=list_players[i_player]
    if player._dash_cooldown[0]==0 and player._height!=player._sneak_height:
        player._dash_cooldown[0]=player._dash_cooldown[1]
        player._dash_lenght[0]=player._dash_lenght[1]
        player._vector['jump']=[0,0] #Annule le vecteur saut du joueur pour éviter qu'il ne continue son saut après son dash
        player._stored_vectors['dash']=[player._dir[0]*3*player._velocity,player._dir[1]*3*player._velocity]

def respawn(event,i_player):
    list_players[i_player].respawn()

def next_level():
    """
    Passe au niveau suivant et charge le nouveau niveau
    """
    global i_level,level,level_name,list_t_blocks,timed_block_cooldown
    i_level+=1
    if i_level<=len(list_levels)-1:
        level_name=list_levels[i_level]
        level=eval(open(f"{level_name}.txt",'r').read())
        portal_height=0
        portal_co=None
        for k in level.keys():

            if level[k][0]=='portal-in' and portal_height<k[1]:
                portal_height=k[1]
                portal_co=[k[0],k[1]+1]

        timed_block_cooldown=0
        for player in list_players:
            player._last_checkpoint=portal_co
            player.set_position(portal_co)
        level=las.update_lasers(level,can_main,c_main)
        list_t_blocks=sort_timed_blocks(level)
        graph.can_update(can_main,['all','player','hearts','name'],level,c_main,list_players=list_players,x_can=x_can,y_can=y_can,level_name=level_name)


    else:
        can_main.create_text(x_can*c_main//2,y_can*c_main//2,text='Gagné',font='System 40')
        if len(list_levels)==1:
            fen_plat.destroy()


def destroy_fen():
    fen_plat.after_cancel(after_id)
    fen_plat.destroy()


def sort_timed_blocks(level):
    """
    Trie les blocs chronométrés en foncion de la frame à laquelle ils doivent
    changer d'état

    Arguments :
    ¯¯¯¯¯¯¯¯¯¯¯
        level : type=dict
            Dictionnaire de l'état d'un niveau

    Returns :
    ¯¯¯¯¯¯¯¯¯
        list_t_blocks_sorted : type=list
            Liste de 60 listes car l'état des blocs chronométrés change toutes
            les 60 frames
            La liste à l'indice i contient les coordonnées des blocs
            chronométrés qui doivent changer d'état au bout de i frames

    """
    list_t_blocks_sorted=[[] for _ in range(60)]
    for key in level.keys():
        if level[key][0]=='timed-block':
            list_t_blocks_sorted[level[key][3]].append(key)

    return list_t_blocks_sorted


def dict_to_list_level(dict_levels):
    """
    Transforme un dictionnaire de niveaux avec les difficultés en clef et la
    liste des niveaux correspondants à cette difficulté en une liste de niveau
    à proposer dans l'ordre au joueur, mélangés selon certaines règles :

        -Les niveaux ayant une difficulté sous forme de chaîne de caractère
        sont laissés à la suite tels quels

        -Si la difficulté est un entier, les niveaux sont mélangés dans cette
        difficulté et il y a une probabilité de 0.15 qu'un niveau de la
        difficulté superieure soit sélectionné sauf si cette difficulté est une
        chaîne de caractère

        -On parcourt les difficultés dans la même ordre que dans le
        dictionnaire

    Arguments :
    ¯¯¯¯¯¯¯¯¯¯¯
        dict_levels : type=dict
            Dictionnaire dont les clefs sont les difficultés et les valeurs,
            les niveaux ayant cette difficulté

    Returns :
    ¯¯¯¯¯¯¯¯¯
        list_levels : type=list
            Liste des niveaux qu'il faut présenter au joueur dans l'ordre
    """
    list_levels=[]
    while dict_levels != {}:
        first_dif=list(dict_levels.keys())[0]#Prmière difficulté du dictionnaire
        if type(first_dif)==str: #Si c'est une chaîne
            list_levels+=dict_levels[first_dif] #Ajoute toute la liste associée
            del dict_levels[first_dif] #Et supprime la clef

        elif len(list(dict_levels.keys()))>=2 and type(list(dict_levels.keys())[1])!=str and dict_levels[list(dict_levels.keys())[1]]!=[]:
            next_dif=list(dict_levels.keys())[1]
            while dict_levels[first_dif] != [] and dict_levels[next_dif] != []:
                if use.randprob(0.15):
                    list_levels.append(dict_levels[next_dif].pop(randrange(len(dict_levels[next_dif]))))
                else:
                    list_levels.append(dict_levels[first_dif].pop(randrange(len(dict_levels[first_dif]))))

            if dict_levels[first_dif]==[]:
                del dict_levels[first_dif]
            else:
                del dict_levels[next_dif]

        else:
            shuffle(dict_levels[first_dif])
            list_levels+=dict_levels[first_dif]
            del dict_levels[first_dif]

    return list_levels

def death_screen():
    # fra_death=tk.Frame(fen_plat_plat,width=x_can*c_main,height=y_can*c_main,bg='black')
    print('DEATH')
    next_level()

def del_double(list0):
    list_return=[]
    for e in list0:
        if not e in list_return:
            list_return.append(e)
    return list_return

platformer(demo=False,nb_players=2)
