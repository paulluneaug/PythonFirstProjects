import graphic_module as graph
import useful_module as use
from copy import deepcopy

"""
Module gérant les lasers et leurs collisions avec le joueur
"""

def update_lasers(level,can_main,c_main):
    """
    Met à jour les lasers du niveau et renvoie le niveau modifié
    
    Arguments:
    ¯¯¯¯¯¯¯¯¯
        level : type=dict
            Dictionnaire de l'état d'un niveau
            
        can_main : type=tkinter.Canvas
            Canvas sur lequel on dessine le niveau
            
        c_main : type=int
            Longueur du coté de chaque bloc
            
    Returns:
    ¯¯¯¯¯¯¯
        level : type=dict
            Dictionnaire modifié de du nouvel état du niveau
        
    """
    list_stops_laser=[['block'],['door'],['breakable-block'],['speed-up'],['bounce'],
                      ['slow-down'],['sticky'],['laser-emitter'],['on-block',True],
                      ['off-block',True],['timed-block',True],['on-off-switch'],['spike'],['button'],['on-off-door',True]]

    list_mirror_redirect=[{'up':'up','right':None,'down':'down','left':None},
                          {'up':'right','right':'up','down':'left','left':'down'},
                          {'up':None,'right':'right','down':None,'left':'left'},
                          {'up':'left','right':'down','down':'right','left':'up'}]

    level_copy=deepcopy(level)

    list_edited=[]
    list_recievers=[]
    dict_ways={'up':(0,-1),'left':(-1,0),'down':(0,1),'right':(1,0)}
    dict_w_nb={'up':2,'left':1,'down':0,'right':3}
    dict_opposite={'up':'down','left':'right','down':'up','right':'left','on':'off','off':'on'}
    list_emitters=[]

    #Supprime les lasers dans tous les blocs du niveau et 
    #regroupe dans une liste tous les emmeteurs lasers
    for k in level.keys():
        if level[k][0]=='laser-emitter':
            list_emitters.append(k)

        if level[k][0]=='laser-reciever':
            level[k][2]=[]
            list_recievers.append(k)
            list_edited.append(k)

        elif level[k][0] in ('glass','checkpoint'):
            level[k][1]=[]
            list_edited.append(k)

        elif level[k][0]=='laser-beam':
            level[k]=[None]
            list_edited.append(k)

        elif level[k][0] in ('on-block','off-block','timed-block','bg','one-way-block'):# and level[k][1]!=False:
            level[k][2]=[]
            list_edited.append(k)

        elif level[k][0]=='on-off-door':
            level[k][3]=[]
            list_edited.append(k)

        elif level[k][0]=='mirror':
            level[k][3]=4*[False]
            list_edited.append(k)

    #Calcule la nouvelle position des lasers
    for emitter in list_emitters:
        
        way=level[emitter][1]
        list_stops_laser.append(['one-way-block',dict_opposite[way]])
        way_co=dict_ways[way]
        new_co=(emitter[0]+way_co[0],emitter[1]+way_co[1])
        laser_stopped=False
        
        while new_co in level and not laser_stopped:
            for b in list_stops_laser: #Vérifie qu'aucun bloc n'arrête le laser
                if len(b)<=len(level[new_co]) and level[new_co][:len(b)]==b:
                    laser_stopped=True
                    break
            #Si ce n'est pas la cas, selon le bloc que le laser rencontre
            #il peut être redirigé, traverser le bloc ou l'activer
            if not laser_stopped:
                if level[new_co][0] in ('on-block','off-block','timed-block','one-way-block','bg'):
                    level[new_co][2].append(way)

                elif level[new_co][0] == 'on-off-door':
                    level[new_co][3].append(way)

                elif level[new_co][0] in ('glass','checkpoint','laser-beam'):
                    level[new_co][1].append(way)

                elif level[new_co][0]=='mirror':
                    level[new_co][3][dict_w_nb[way]]=True
                    way=list_mirror_redirect[level[new_co][2]][way]
                    if way==None:
                        laser_stopped=True
                        break
                    else:
                        list_stops_laser.pop(-1)
                        list_stops_laser.append(['one-way-block',dict_opposite[way]])
                        level[new_co][3][(dict_w_nb[way]+2)%4]=True
                        way_co=dict_ways[way]


                elif level[new_co][0]=='laser-reciever':
                    laser_stopped=True
                    if level[new_co][1]!=dict_opposite[way]:
                        level[new_co][2].append(dict_opposite[way])

                else:
                    level[new_co]=['laser-beam',[way]]

                if new_co not in list_edited:
                    list_edited.append(new_co)

            new_co=(new_co[0]+way_co[0],new_co[1]+way_co[1])
        list_stops_laser.pop(-1)
    
    #Pour chaque récepteur laser, vérifie s'il vient de s'activer
    #Si c'est le cas, active le bloc que le récepteur pointe
    laser_2_update=False
    for reciever in list_recievers:
        if level[reciever][2]!=[] and not level[reciever][3]:
            level[reciever][3]=True
            but_co=tuple(use.sum_vector([reciever,dict_ways[level[reciever][1]]]))
            if level[but_co][0]=='button':
                list_edited,laser_2_update,level=switch_button(level[but_co][1],list_edited,laser_2_update,level)
            if level[but_co][0]=='on-off-switch':
                list_edited,laser_2_update,level=switch_on_off(dict_opposite[level[but_co][1]],list_edited,laser_2_update,level)
            if level[but_co][0]=='mirror':
                list_edited.append(but_co)
                laser_2_update=True
                level[but_co][2]=(level[but_co][2]+1)%4

        elif level[reciever][2]==[]:
            level[reciever][3]=False

    if laser_2_update:
        update_lasers(level, can_main, c_main)
    
    #Compare l'ancien niveau et le niveau modifié 
    list_to_update=use.dict_comparator(level_copy, level, list_to_check=list_edited)
    
    #Et actualise toutes les cases modifiées
    graph.can_update(can_main, list_to_update, level, c_main)

    return level


                


def check_laser_kills(level, player):
    """
    Vérifie si un laser ou un laser dans un bloc n'est pas en collision avec 
    un joueur
    
    Arguments:
    ¯¯¯¯¯¯¯¯¯
        level : type=dict
            Dictionnaire de l'état du niveau
            
        player : type=Player
            Joueur dont on vérifie les collisions
            
    Returns:
    ¯¯¯¯¯¯¯
        killed : type=bool
            True si le joueur est touché par des lasers
            False sinon
        
            
    """
    list_kills=[['laser-beam'],['timed-block',False],['on-block',False],
                ['off-block',False]]
    
    l_col=player._list_collisions
    
    p_posx=player._position[0]-int(player._position[0])
    p_posy=player._position[1]-int(player._position[1])
    
    
    
    #Liste de tous les blocs an lien avec les lasers qui tuent le joueur
    list_kills=[['laser-beam'],['timed-block',False],['on-block',False],
                ['off-block',False],['one-way-block'],['on-off-door',False],
                ['bg'],['checkpoint']]
        
    
    l_col=player._list_collisions
    for i_k in range(len(list_kills)):
        k=list_kills[i_k]
        
        #----------Vérifie si un de ces bloc touche le haut du joueur---------#
        
        #Liste de booléens, True si dans la liste des collisions du haut 
        #du joueur, il y a le bloc k, False sinon
        l_block_top=[[reducer(block) for block in arrete] for arrete in l_col[0]]
        l_col_top=[[k == block[:len(k)] if len(block)>=len(k) else False for block in arrete] for arrete in l_block_top]

        for i_arr in range(len(l_col_top)):
            
            for i_block in range(len(l_col_top[i_arr])):
               
                if l_col_top[i_arr][i_block]:
                    block=l_block_top[i_arr][i_block]
                    
                    #Si le laser dans le bloc est horizontal, 
                    #vérifie que le joueur est assez haut pour le toucher
                    if 'right' in block[-1] or 'left' in block[-1]:
                        if 0<p_posy<0.6:
                            return True
                        
                    if 'up' in block[-1] or 'down' in block[-1]:
                        #Si le laser est vertical, mais aux extémités du joueur, 
                        #vérifie si le joueur est assez à gauche ou à droite 
                        #pour le toucher
                        if (i_arr,i_block) == (0,0):
                            if p_posx<0.6:
                                return True
                                
                        elif (i_arr,i_block) == (len(l_col_top)-1,len(l_col_top[i_arr])-1):
                            if p_posx>0.4:
                                return True
                        
                        #Sinon, tue le joueur
                        else:
                            return True
                
            
        #---------Vérifie si un de ces bloc touche la droite du joueur--------#
        
        #Liste de booléens, True si dans la liste des collisions de la droite
        #du joueur, il y a le bloc k, False sinon
        l_block_right=[[reducer(block) for block in arrete] for arrete in [l_col[y][1] for y in range(1,1+player.get_height())]]
        l_col_right=[[k == block[:len(k)] if len(block)>=len(k) else False for block in arrete] for arrete in l_block_right]
        
        for i_arr in range(len(l_col_right)):
            
            for i_block in range(len(l_col_right[i_arr])):
                
                if l_col_right[i_arr][i_block]:
                    
                    block=l_block_right[i_arr][i_block]
                    #Si le laser dans le bloc est vertical, 
                    #vérifie que le joueur est assez à droite pour le toucher
                    if 'up' in block[-1] or 'down' in block[-1]:
                        if p_posx>0.4:
                            return True
                        
                    if 'right' in block[-1] or 'left' in block[-1]:
                        #Si le laser est horizontal, mais aux extémités du joueur, 
                        #vérifie si le joueur est assez haut ou bas pour le toucher
                        if (i_arr,i_block) == (0,len(l_col_right[i_arr])-1):
                            if p_posy<0.6:
                                return True
                                
                        elif (i_arr,i_block) == (len(l_col_right)-1,0):
                            if p_posy>0.4 or p_posy==0:
                                return True
                            
                        #Sinon, tue le joueur
                        else:
                            return True
                
            
        #----------Vérifie si un de ces bloc touche le bas du joueur---------#
        
        #Liste de booléens, True si dans la liste des collisions du bas
        #du joueur, il y a le bloc k, False sinon
        l_block_down=[[reducer(block) for block in arrete] for arrete in l_col[-1]]
        l_col_down=[[k == block[:len(k)] if len(block)>=len(k) else False for block in arrete] for arrete in l_block_down]
        
        for i_arr in range(len(l_col_down)):
            
            for i_block in range(len(l_col_down[i_arr])):
                
                if l_col_down[i_arr][i_block]:
                    block=l_block_down[i_arr][i_block]
                    
                    #Si le laser dans le bloc est horizontal, 
                    #vérifie que le joueur est assez bas pour le toucher
                    if 'right' in block[-1] or 'left' in block[-1]:
                        if p_posy>0.4:
                            return True
                    
                    if 'up' in block[-1] or 'down' in block[-1]:
                        #Si le laser est vertical, mais aux extémités du joueur, 
                        #vérifie si le joueur est assez à gauche ou à droite 
                        #pour le toucher
                        if (i_arr,i_block) == (0,0):
                            if p_posx<0.6:
                                return True
                                
                        elif (i_arr,i_block) == (len(l_col_down)-1,len(l_col_down[i_arr])-1):
                            if p_posx>0.4:
                                return True
                        
                        #Sinon, tue le joueur
                        else:
                            return True
                    
            
        #---------Vérifie si un de ces bloc touche la gauche du joueur--------#
        
        #Liste de booléens, True si dans la liste des collisions de la gauche
        #du joueur, il y a le bloc k, False sinon
        l_block_left=[[reducer(block) for block in arrete] for arrete in [l_col[y][0] for y in range(1,1+player.get_height())]]
        l_col_left=[[k == block[:len(k)] if len(block)>=len(k) else False for block in arrete] for arrete in l_block_left]
        
        for i_arr in range(len(l_col_left)):
            
            for i_block in range(len(l_col_left[i_arr])):
                
                if l_col_left[i_arr][i_block]:
                    
                    block=l_block_left[i_arr][i_block]
                    #Si le laser dans le bloc est vertical, 
                    #vérifie que le joueur est assez à droite pour le toucher
                    if 'up' in block[-1] or 'down' in block[-1]:
                        if 0<p_posx<0.6:
                            return True
                        
                    if 'right' in block[-1] or 'left' in block[-1]:
                        #Si le laser est horizontal, mais aux extémités, 
                        #vérifie si le joueur est assez haut ou bas pour le toucher
                        if (i_arr,i_block) == (0,len(l_col_left[i_arr])-1):
                            if 0<p_posy<0.6:
                                return True
                                
                        elif (i_arr,i_block) == (len(l_col_left)-1,0):
                            if p_posy>0.4:
                                return True
                            
                        #Sinon, tue le joueur
                        else:
                            return True
        
    return False

def reducer(block):
    dict_del={'laser-beam':2,'on-block':3,'off-block':3,'timed-block':3,
              'one-way-block':3,'on-off-door':4,'bg':3,'checkpoint':2}
    if block[0] in dict_del:
        return block[:dict_del[block[0]]]
    else:
        return [None]



def switch_button(but_channel,list_to_update,laser_2_update,level):
    """
    Change l'état des portes on-off et fait tourner les miroirs d'une certaine couleur
    
    
    """
    for key in level.keys():
        
        if len(level[key])>=2 and level[key][:2]==['mirror',but_channel]:
            level[key][2]=(level[key][2]+1)%4
            list_to_update.append(key)
            laser_2_update=True
        
        if len(level[key])>=3 and level[key][:3] in (['on-off-door',True,but_channel],['on-off-door',False,but_channel]):
            level[key][1]=not level[key][1]
            list_to_update.append(key)
            laser_2_update=True
    return list_to_update,laser_2_update,level


def switch_on_off(switch_state,list_to_update,laser_2_update,level):
    """
    Change l'état des blocs on et off ainsi que des interrupteurs on-off
    Ajoute à la liste des cases à mettre à jour les cases modifiées 
    """
    for k in level.keys():
        if level[k][0]=='on-off-switch':
            level[k][1]=switch_state
            list_to_update.append(k)
        elif level[k][0] in ('on-block','off-block'):
            level[k][1]=not level[k][1]
            list_to_update.append(k)
            laser_2_update=True
    return list_to_update,laser_2_update,level




