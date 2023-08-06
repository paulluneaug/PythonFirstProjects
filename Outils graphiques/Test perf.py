
import tkinter as tk
from timeit import timeit

import tkinter as tk
from math import sqrt
import mod_plat as mp
from random import randrange



class Player:
    """
    Classe créant et gérant un personnage jouable d'un platformer
    """

    def __init__(self,x,y,width=1,height=2,velocity=5):
        #Dictionnaire des différents vecteurs qui s'appliquent sur le joueur
        self._vector={'right':[0,0],'jump':[0,0],'gravity':[0,8],
                      'reaction':[0,0],'left':[0,0]}

        #Dictionnaire des intentions du joueur
        self._wanna_go={'right':False,'left':False,'up':False,'sneak':False}

        self._position=[x,y] #Coordonnées du joueur
        self._last_checkpoint=[x,y] #Coordonnées du dernier checkpoint
        
        self._max_life=5
        self._life=self._max_life

        self._velocity=velocity #Vitesse du joueur
        self._height=height #Hauteur
        self._width=width #Largeur

        self.create_list_collisions()
        
        self._can_wall_jump=False #Capacité du joueur à sauter sur les murs

        self._jump_speed=3*c_main # Vitesse de saut
        self._max_jump=1 #Nombre de saut que le joueur peut enchaîner sans
                         #toucher le sol ou un mur
        self._jump_left=self._max_jump

        self._dir=(1,0) #Direction du joueur
        self._dash_cooldown=[0,fps//1.5] #Cooldown du dash
        self._dash_lenght=[0,fps//10]#Nombre de frames pendant lesquelles 
                                    #le joueur est soumis au dash

        self._stored_vectors={'dash':[0,0]}
        self._max_height=y

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
                        if (int(self._position[0]+arrete+a),int(self._position[1]-self._height-add_top)) in level:
                            #Vérifie si le le haut du joueur est toujours dans 
                            #le niveau
                            
                            #Ajoute à une liste la case qu'il touche 
                            arrete_temp.append(level[int(self._position[0]+arrete+a),int(self._position[1]-self._height-add_top)][0])
                            
                            #Et à une autres, ses coordonnées
                            arrete_temp_coor.append([int(self._position[0]+arrete+a),int(self._position[1]-self._height-add_top)])
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
                        if (int(self._position[0]+arrete+b),int(self._position[1])) in level:
                            #Vérifie si le bas du joueur est toujours dans 
                            #le niveau
                            
                            #Ajoute à une liste la case qu'il touche 
                            arrete_temp.append(level[int(self._position[0]+arrete+b),int(self._position[1])][0])
                            
                            #Et à une autres, ses coordonnées
                            arrete_temp_coor.append([int(self._position[0]+arrete+b),int(self._position[1])])
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
                        
                            if (int(self._position[0]-add_side),int(self._position[1]-(self._height-etage+add_top)-c)) in level:
                                #Vérifie si la gauche du joueur est toujours 
                                #dans le niveau
                                
                                #Ajoute à une liste la case qu'il touche 
                                arrete_temp.append(level[int(self._position[0]-add_side),int(self._position[1]-(self._height-etage+add_top)-c)][0])
                                
                                #Et à une autres, ses coordonnées
                                arrete_temp_coor.append([int(self._position[0]-add_side),int(self._position[1]-(self._height-etage+add_top)-c)])
                            
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
                        
                            if (int(self._position[0]+arrete*list_nbr_arrete[0]),int(self._position[1]-(self._height-etage+add_top)-d)) in level:
                                #Vérifie si la droite du joueur est toujours dans 
                                #le niveau
                                
                                #Ajoute à une liste la case qu'il touche 
                                arrete_temp.append(level[int(self._position[0]+arrete*list_nbr_arrete[0]),int(self._position[1]-(self._height-etage+add_top)-d)][0])
                                
                                #Et à une autres, ses coordonnées
                                arrete_temp_coor.append([int(self._position[0]+arrete*list_nbr_arrete[0]),int(self._position[1]-(self._height-etage+add_top)-d)])
                            else: #Bloque le joueur s'il sort du niveau
                                arrete_temp.append(None)
                                arrete_temp_coor.append(None)
                        list_collisions[etage][arrete]=arrete_temp
                        list_collisions_coor[etage][arrete]=arrete_temp_coor
                        
        self._list_collisions=list_collisions
        self._list_collisions_coor=list_collisions_coor

    def respawn(self):
        """
        Fait réapparaître le joueur au dernier checkpoint, annule tous 
        les vecteurs auxquels il est soumis et lui enlève une vie
        """
        self.set_position(self._last_checkpoint)
        list_vect2keep=['gravity'] #Liste des vecteurs que l'on ne doit pas 
                                   #annuler 
        for vect in self._vector.keys():
            if vect not in list_vect2keep:
                self._vector[vect]=[0,0]
                
        self._life-=1
        if self._life==0:
            a=0 #DEATH
            
    def refill_life(self):
        self._life=self._max_life

def platformer():
    global x_can,y_can,c_main,can_main,fps,fen,player,dict_levels,nb_level_done,level
    x_can,y_can=60,30 #Nombre de cases en hauteur et largeur du canvas
    c_main=900//max(x_can,y_can) #Taille en pixels de chaque case
    nb_level_done=0
    
    dict_levels={'tutorial':['tuto0','tuto1'],
                 1:['digo','0','cbo'],
                 2:['digoestbo','one_way'],
                 '3':['test','smile']}
    level=eval(open(f'Levels/level{dict_levels[list(dict_levels.keys())[0]].pop(0)}.txt','r').read())

    fps=90 #Nombre de fois par secondes où l'état du jeu est calculé

    player=Player(0,y_can-1,width=1,height=2,velocity=c_main//3) #Création du joueur

    fen=tk.Tk()
    fen.title('Platformer')

    can_main=tk.Canvas(fen,width=x_can*c_main,height=y_can*c_main,bg='white')
    can_main.pack()
    
    can_update(['all'])

    play()

    fen.bind('<Up>',jump)

    fen.bind('<Left>',lambda x:key_press('left'))
    fen.bind('<KeyRelease-Left>',lambda x:key_release('left'))

    fen.bind('<Right>',lambda x:key_press('right'))
    fen.bind('<KeyRelease-Right>',lambda x:key_release('right'))

    fen.bind('<Down>',lambda x:key_press('sneak'))
    fen.bind('<KeyRelease-Down>',lambda x:key_release('sneak'))

    fen.bind('<d>',dash)

    fen.mainloop()




def can_update(list_to_update):
    """
    Met à jour une ou toutes les cases de la grille

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        list_to_update : type=tuple or list
            Liste du ou des éléments qu'il faut mettre à jour
                -"all" s'il faut tout mettre à jour
                -un tuple ou une liste de deux flottants pour mettre à jour 
                 une certaine case
                -"player" pour mettre à jour le sprite du joueur
    """
    for element in list_to_update: #Parcourt chaque élément à mettre à jour
    
        if element=="all": #Met à jour toutes les cases
            can_main.delete('all')
            for tile in level.keys():
                if level[tile][0] not in (None,''):
                    if len(level[tile])==1:
                        mp.draw_tile(can_main,tile[0],tile[1],level[tile][0],
                                     c_main)
                    elif level[tile][0] in ('key','door'):
                        mp.draw_tile(can_main,tile[0],tile[1],level[tile][0],
                                     c_main,channel=level[tile][1][1])
                    elif level[tile][0]=='glass':
                        mp.draw_tile(can_main,tile[0],tile[1],level[tile][0],
                                     c_main,glass_color=level[tile][1])
                    elif level[tile][0]=='one_way_block':
                        mp.draw_tile(can_main,tile[0],tile[1],level[tile][0],
                                     c_main,way=level[tile][1])
        
        elif type(element)==tuple: #Met à jour une case en particulier
            can_main.delete(f'{element[0]}/{element[1]}')
            if level[element][0] not in (None,''):
                if len(level[tile])==1:
                    mp.draw_tile(can_main,element[0],element[1],
                                 level[element][0],c_main)
                elif level[tile][0] in ('key','door'):
                    mp.draw_tile(can_main,element[0],element[1],
                                 level[element][0],c_main,
                                 channel=level[element][1][1])
                elif level[tile][0]=='glass':
                    mp.draw_tile(can_main,element[0],element[1],
                                 level[element][0],c_main,
                                 glass_color=level[tile][1])
                elif level[tile][0]=='one_way_block':
                    mp.draw_tile(can_main,element[0],element[1],
                                 level[element][0],c_main,way=level[tile][1])
                                 
                
        
        if element in ('player','all'): #Met à jour le sprite du joueur
            can_main.delete('player')
            p_pos=player.get_position()
            for x in range(player.get_width()):
                for y in range(player.get_height()):
                    can_main.create_rectangle((p_pos[0]+x)*c_main,
                                              (p_pos[1]-y)*c_main,
                                              (p_pos[0]+x+1)*c_main,
                                              (p_pos[1]-y-1)*c_main,
                                              fill='#004BFF',tag='player')
            can_main.create_oval(player.get_position()[0]*c_main-3,
                                 player.get_position()[1]*c_main-3,
                                 player.get_position()[0]*c_main+3,
                                 player.get_position()[1]*c_main+3,
                                 fill='purple',tag='player')


def play():
    """
    Boucle principale
    """

    list_blocks_stops=['block','door','breakable-block'] #Liste des blocs bloquant le joueur

    player.create_list_collisions()

    #Vérifie si le joueur a une case 'checkpoint' dans sa liste de collision
    is_on_checkpoint,check_co=mp.in_sub_list('checkpoint',player._list_collisions)

    if is_on_checkpoint: #Si oui, change les coordonnés du checkpoint du joueur
        j,k,l=tuple(check_co)
        check_co=player._list_collisions_coor[j][k][l]
        player._last_checkpoint=[check_co[0],check_co[1]+1]
    

    if player._dash_lenght[0]==player._dash_lenght[1]:
        player._vector,player._stored_vectors=player._stored_vectors,player._vector
    elif player._dash_lenght[0]==1:
        player._vector,player._stored_vectors=player._stored_vectors,player._vector

    if len(player._vector)!=1:
        if player._wanna_go['left']: #Si je joueur appuie sur la touche pour aller à gauche
            player._vector['left']=[-player._velocity,0] #
            player._dir=(-1,0) #Change sa direction
        else:
            player._vector['left']=[0,0] #Sinon, annule le vecteur de gauche
    
    
        if player._wanna_go['right']: #Si je joueur appuie sur la touche pour aller à droite
            player._vector['right']=[player._velocity,0]
            player._dir=(1,0) #Change sa direction
        else:
            player._vector['right']=[0,0] #Sinon, annule le vecteur de gauche

    if player._wanna_go['sneak']: #Si le joueur veut d'accroupir
        player._height=1 #Baisse sa hauteur à 1
        
    elif player._height!=2: #Sinon, si le joueur ne veut pas s'accroupir mais qu'il n'est pas relevé
        can_go=True
        for item in list_blocks_stops: #Vérifie au dessus de sa tête si il y a un bloc qui l'empêche de se relever
            can_go=can_go and not (True in [item in arrete for arrete in player._list_collisions[0]])
       
        list_col=player._list_collisions.copy()
        while can_go and True in ['one_way_block' in arrete for arrete in list_col[0]]:
            #Cherche toutes cases de one_way_block au dessus du joueur
            
            c,path=mp.in_sub_list('one_way_block',list_col[0])
            f,g=tuple(path)
            
            #Et vérifie leur sens pour savoir si ils bloquent le joueur
            if level[tuple(player._list_collisions_coor[0][f][g])][1]=='down':
                can_go=False    
            list_col[0][f][g]=None 
        if can_go: #Si'il n'y en a pas
            player._height=2 #Augmente sa taille à 2

    #Somme des vecteurs qui s'appliquent sur le joueur
    vect=sum_vector([vector for vector in player._vector.values()])

    #Norme de ce vecteur
    norm_vect=int(sqrt(vect[0]**2+vect[1]**2))+1
    

    step=1

    list_t2update=[] #Liste des cases à actualiser

    for n in range(0,norm_vect,step):
        
        player.create_list_collisions()
    
        list_can_go=4*[True] #Liste des directions dans lequel le joueur peut aller
        #----------------------------------------------------------------------
        if vect[1]<0: #Si vect va vers le haut 
            can_go=True
            for item in list_blocks_stops:#Vérifie s'il n'y a pas de blocs qui 
                                          #arretent le joueur au dessus de lui
                can_go=can_go and not (True in [item in arrete for arrete in player._list_collisions[0]])
                
                
            list_col=player._list_collisions.copy()
            while can_go and True in ['one_way_block' in arrete for arrete in list_col[0]]:
                #Cherche toutes cases de one_way_block au dessus du joueur
                
                c,path=mp.in_sub_list('one_way_block',list_col[0])
                f,g=tuple(path)
                
                #Et vérifie leur sens pour savoir si ils bloquent le joueur
                if level[tuple(player._list_collisions_coor[0][f][g])][1]=='down':
                    can_go=False    
                list_col[0][f][g]=None
                
            
            if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                           #pas aller plus haut 
                player._vector['jump']=sum_vector([player._vector['gravity']],multiplier=-1)
                list_can_go[0]=False #Indique qu'il ne peut pas aller en haut

            #Tant qu'il y a des blocs cassables au dessus de la tête du joueur
            while True in ['breakable-block' in arrete for arrete in player._list_collisions[0]]:
                t,b_block=mp.in_sub_list('breakable-block',player._list_collisions[0])
                
                r,s=tuple(b_block) #Récupère leurs coordonnées et les supprime
                level[tuple(player._list_collisions_coor[0][r][s])]=[None]
                
                #Ajoute ces coordonnées à la liste des cases à actualiser
                list_t2update.append(tuple(player._list_collisions_coor[0][r][s]))
                
                #Recréé la liste des collisions du joueur pour prendre en 
                #compte la disparition des blocs cassbles
                player.create_list_collisions()
                
            #S'il y a des piques au dessus du joueur, le fait réapparaître
            if True in ['spike' in arrete for arrete in player._list_collisions[0]]:
                player.respawn() 
                break
            
        #----------------------------------------------------------------------
        if vect[0]>0: #Si vect va vers la droite
            can_go=True
            for item in list_blocks_stops:#Vérifie s'il n'y a pas de blocs qui 
                                          #arretent le joueur sur da droite
                can_go=can_go and not (True in [item in player._list_collisions[y][1] for y in range(1,1+player.get_height())])
            
            
            list_col=player._list_collisions.copy()
            while can_go and True in ['one_way_block'  in list_col[y][1] for y in range(1,1+player.get_height())]:
                #Cherche toutes cases de one_way_block à droite du joueur
                
                c,path=mp.in_sub_list('one_way_block',list_col)
                f,g,h=tuple(path)
                
                #Et vérifie leur sens pour savoir si ils bloquent le joueur
                if g==1 and level[tuple(player._list_collisions_coor[f][g][h])][1]=='left':
                    can_go=False    
                list_col[f][g][h]=None
                
                
            if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                           #pas aller plus à droite en annulant ce vecteur
                player._vector[list(player._vector.keys())[0]]=[0,0]
                list_can_go[1]=False
                
                if player._can_wall_jump: #Si le joueur peut sauter des murs
                    #Remet dans son état initial le nombre de saut qu'il reste 
                    #au joueur
                    player._jump_left=player._max_jump
                
            #S'il y a des piques à droite du joueur, le fait réapparaître
            if True in ['spike' in player._list_collisions[y][1] for y in range(1,1+player.get_height())]:
                player.respawn()
                break
            
        #----------------------------------------------------------------------
        if vect[1]>0: #Si vect va vers le bas
        
            #Si je joueur et bel et bien dans un bloc de piques 
            #(et pas juste sur la case au dessus), le fait réapparaître
            if vect[1]!=0 and True in ['spike' in arrete for arrete in player._list_collisions[-1]]:
                player.respawn()
                break

            # while True in ['breakable-block' in arrete for arrete in player._list_collisions[-1]]:
            #     t,b_block=mp.in_sub_list('breakable-block',player._list_collisions[-1])
            #     r,s=tuple(b_block)
            #     level[tuple(player._list_collisions_coor[-1][r][s])]=[None]
            #     list_t2update.append(tuple(player._list_collisions_coor[-1][r][s]))
            #     player.create_list_collisions()

            can_go=True
            for item in list_blocks_stops:#Vérifie s'il n'y a pas de blocs qui 
                                          #arretent le joueur en dessous de lui
                can_go=can_go and not (True in [item in arrete for arrete in player._list_collisions[-1]])

            list_col=player._list_collisions.copy()
            while can_go and True in ['one_way_block' in arrete for arrete in list_col[-1]]:
                #Cherche toutes cases de one_way_block en dessous du joueur
                
                c,path=mp.in_sub_list('one_way_block',list_col[-1])
                f,g=tuple(path)
                
                #Et vérifie leur sens pour savoir si ils bloquent le joueur
                if level[tuple(player._list_collisions_coor[-1][f][g])][1]=='up':
                    can_go=False    
                list_col[-1][f][g]=None
                
            if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                           #pas aller plus bas en appliquant un vecteur opposé 
                           #à la gravité sur le joueur
                player._vector['reaction']=sum_vector([player._vector['gravity']],multiplier=-1)
                
                player._vector['jump']=[0,0] #Annule le vecteur saut
                
                #Remet dans son état initial le nombre de saut qu'il reste 
                #au joueur
                player._jump_left=player._max_jump
                list_can_go[2]=False
            else:
                player._vector['reaction']=[0,0]
        else:
            player._vector['reaction']=[0,0]


        #----------------------------------------------------------------------
        if vect[0]<0: #Si vect va vers la gauche

            can_go=True
            for item in list_blocks_stops:#Vérifie s'il n'y a pas de blocs qui 
                                          #arretent le joueur à gauche de lui
                can_go=can_go and not (True in [item in player._list_collisions[y][0] for y in range(1,1+player.get_height())])
            
            list_col=player._list_collisions.copy()
            while can_go and True in ['one_way_block'  in list_col[y][0] for y in range(1,1+player.get_height())]:
                #Cherche toutes cases de one_way_block à gauche du joueur
                
                c,path=mp.in_sub_list('one_way_block',list_col)
                f,g,h=tuple(path)
                
                #Et vérifie leur sens pour savoir si ils bloquent le joueur
                if g==0 and level[tuple(player._list_collisions_coor[f][g][h])][1]=='right':
                    can_go=False    
                list_col[f][g][h]=None
            
            if not can_go: #S'il y en a, fait en sorte que le joueur ne puisse
                           #pas aller plus à gauche en annulant ce vecteur
                player._vector[list(player._vector.keys())[-1]]=[0,0]
                list_can_go[3]=False
                
                if player._can_wall_jump: #Si le joueur peut sauter des murs
                    #Remet dans son état initial le nombre de saut qu'il reste 
                    #au joueur
                    player._jump_left=player._max_jump
                    
            #S'il y a des piques à gauche du joueur, le fait réapparaître
            if True in ['spike' in player._list_collisions[y][0] for y in range(1,1+player.get_height())]:
                player.respawn()
                break
            
        #----------------------------------------------------------------------

        if player.get_position()[1]<player._max_height:
            player._max_height=player.get_position()[1]
            print(y_can-1-player._max_height)

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
        
        if n%15==0:
            can_update(['player'])

    #Cherche des clefs autour du joueur
    in_l,path=mp.in_sub_list('key',player._list_collisions)

    if in_l: #S'il y en a, 
        a,b,c=tuple(path) #Récupère les coordonnées
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
    
    
    can_update(list_t2update) #Met à jour toutes les cases qu'il faut
        
    if True in ['portal-out' in player._list_collisions[y][0] for y in range(1,1+player.get_height())]:
        next_level()

    can_update(['player']) #Met à jour le sprite du joueur
    
    #Diminue le vecteur saut
    if 'jump' in player._vector:
        player._vector['jump']=sum_vector([player._vector['jump']],multiplier=0.9)
    
    if player._dash_cooldown[0]!=0:
        player._dash_cooldown[0]-=1
    if player._dash_lenght[0]!=0:
        player._dash_lenght[0]-=1
        
    fen.after(1000//fps,play)
##    fen.after(int(30),play)

def key_release(key):
    player._wanna_go[key]=False

def key_press(key):
    if not player._wanna_go[key]:
        player._wanna_go[key]=True

def jump(event):
    """
    Fait sauter le joueur
    """
    print(player._vector)
    if player._jump_left>0 and not 'dash' in player._vector:
        player._vector['jump']=[0,-player._jump_speed]
        player._jump_left-=1

def dash(event):
    if player._dash_cooldown[0]==0:
        player._dash_cooldown[0]=player._dash_cooldown[1]
        player._dash_lenght[0]=player._dash_lenght[1]
        player._vector['jump']=[0,0]
        player._stored_vectors['dash']=[player._dir[0]*3*player._velocity,player._dir[1]*3*player._velocity]

def next_level():
    global level,nb_level_done,i_level
    
    print(dict_levels)
    if dict_levels!={}:
        first_key=list(dict_levels.keys())[0]
        if type(first_key)==str:
            if dict_levels[first_key]!=[]:
                level=eval(open(f"Levels/level{dict_levels[first_key].pop(0)}.txt",'r').read())
            else:
                del dict_levels[first_key]
                first_key=list(dict_levels.keys())[0]
        if type(first_key)==int:
            if nb_level_done==5:
                nb_level_done=0
                player.refill_life()
                # del dict_levels[first_key]
                # first_key=list(dict_levels.keys())[0]
            if dict_levels[first_key]==[]:
                del dict_levels[first_key]
                next_level()
            else:
                if (len(list(dict_levels.keys()))>=2 and type(list(dict_levels.keys())[1])==str) or mp.randprob(0.8):
                    dif=first_key
                else:
                    dif=list(dict_levels.keys())[1]
                print(dict_levels)
                level_nb=randrange(len(dict_levels[dif]))
                print(dif,dict_levels[dif],level_nb)
                print([dict_levels[dif][level_nb]])
                level=eval(open(f"Levels/level{dict_levels[dif].pop(level_nb)}.txt",'r').read())
                
    
    player.set_position([0,y_can-1])
    can_update(['all'])
                
                
                
                
        
        
    
    # i_level+=1
    # level=eval(open(f'Levels/level{list_levels[i_level]}.txt','r').read())
    # player.set_position([0,y_can-1])
    # can_update(['all'])
    
    
def sum_vector(list_vector,multiplier=1,arrond=False):
    """
    Renvoie la somme de tous les vecteurs d'une liste
    
    Arguments:
    ¯¯¯¯¯¯¯¯¯
        list_vector : type=list
            Liste de listes de deux flottants
            
        multiplier : type= int or float
            Nombre par lequel on multiplie le vecteur
            
        arrond : type=int
            Si renseigné, nombre de chiffres après la virgule de l'éventuel 
            arrondi
            
    Returns:
    ¯¯¯¯¯¯¯
        vect : type=list
            Vecteur, somme de tous les vecteurs de la liste
    """
    vect=[sum([v[0] for v in list_vector])*multiplier,
          sum([v[1] for v in list_vector])*multiplier]
    if arrond==False:
        return vect
    else:
        return [round(vect[0],arrond),round(vect[1],arrond)]


# list_levels=[(eval(open('Levels/leveltruc.txt','r').read()),(0,0)),
#              (eval(open('Levels/leveltruc.txt','r').read()),(1,0)),
#              (eval(open('Levels/leveldoor2.txt','r').read()),(2,0)),
#              (eval(open('Levels/level1.txt','r').read()),(0,1)),
#              (eval(open('Levels/level1.txt','r').read()),(1,1)),
#              (eval(open('Levels/level1.txt','r').read()),(2,1))]

# x_can,y_can=30,20

# level={}

# for h in [(_,µ) for _ in range(3*x_can+3) for µ in range(2*y_can+1)]:
#     level[h]=[None]

# for b in [(_,0) for _ in range(3*x_can+3)]:
#     level[b]=['block']

# for a in [(3*x_can+d,e) for d in range(3) for e in range(2*y_can+1) if (not (d==1 and y_can-3<e<2*y_can)) and not(d==0 and y_can-2<=e<=y_can-1)]:
#     level[a]=['block']

# for l in list_levels:
#     if l[1][1]%2==0:
#         for tile in l[0].keys():
#             level[l[1][0]*x_can+tile[0],l[1][1]*y_can+tile[1]+1]=l[0][tile]

#     else:
#         for tile in l[0].keys():
#             level[l[1][0]*x_can+tile[0]+1,l[1][1]*y_can+tile[1]+1]=l[0][x_can-1-tile[0],tile[1]]

# for u in [(0,µ) for µ in range(2*y_can+1)]:
#     level[u]=['block']


# level[0,y_can-2],level[0,y_can-1]=['portal-in'],['portal-in']
# level[0,2*y_can-2],level[0,2*y_can-1]=['portal-out'],['portal-out']









#Calcul du temps d'execution de la recherche dans la Liste
temps_liste =timeit('play()', setup="from __main__ import play")
print('polygon :', temps_liste)

#can.delete(tk.ALL)
##Calcul du temps d'execution de la recherche dans le dictionnaire
#temps_dico=timeit('square()', setup="from __main__ import square")
#print('square :', temps_dico)
#
#square()

root.mainloop()