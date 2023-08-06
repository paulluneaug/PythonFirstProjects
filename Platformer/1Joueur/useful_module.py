from random import random

"""
Module de fonctions diverses et utiles 
"""

def search_block(block,level):
    """
    Recherche un bloc dans un niveau et renvoie la liste de toutes les 
    coordonnées de ces blocs dans le niveau
    
    Arguments:
    ¯¯¯¯¯¯¯¯¯
        block : type=str
            Bloc à rechercher dans le niveau
            
        level : type=dict
            Dictionnaire du niveau dans lequel rechercher
            
    Returns:
   ¯¯¯¯¯¯¯¯¯
       list_blocks : type=list
           Liste de toutes les coordonnées de ces blocs dans le niveau
    """
    list_blocks=[]
    for k in level.keys():
        if level[k][0]==block:
            list_blocks.append(k)
    return list_blocks

def in_sub_list(item,liste,depth=None):
    """
    Fonction qui vérifie la présence d'un élémént dans une liste et de ses
    éventuelles sous-listes

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        item : type=any
            Élément à rechercher dans la liste

        liste : type=list or tuple
            Liste dans laquelle on recherche l'item

        depth : type=int
            Si précisé, nombre de sous-liste maximum dans lequel item est
            recherché

    Returns:
    ¯¯¯¯¯¯¯
        is_in : type=bool
            - True si item est dans la liste ou une de ses sous-liste
            - False sinon

        path : type=list
            Liste des indices des différentes listes pour atteindre item dans
            la liste principale
    """
    if depth==None:
        if not (type(liste) in (tuple,list)) or item==liste or liste==[]:
            return item==liste,[]
        else:
            for i in range(len(liste)):
                is_in,path=in_sub_list(item,liste[i])
                if is_in:
                    return is_in,[i]+path
                elif i==len(liste)-1:
                    return False,[]

    elif depth==0:
        return item==liste,[]

    else:
        if not (type(liste) in (tuple,list)) or item==liste or liste==[]:
            return item==liste,[]
        for i in range(len(liste)):
            is_in,path=in_sub_list(item,liste[i],depth=depth-1)
            if is_in:
                return is_in,[i]+path
            elif i==len(liste)-1:
                return False,[]



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
    return random()<=prob


def grid(can,width,height,c):
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
    while vx<width: #Dessine les lignes verticales
        can.create_line(vx,0,vx,height,width=1,fill='black',tag='grid')
        vx+=c
    while vy<height: #Dessine les lignes horizontales
        can.create_line(0,vy,width,vy,width=1,fill='black',tag='grid')
        vy+=c
        

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
    
def dict_comparator(dict0,dict1,list_to_check=False):
    """
    Compare deux dictionnaires de taille identique et avec les même clefs et 
    renvoie la liste des clefs pour lesquelles les valeurs des dictionnaires 
    sont différentes 
    
    Arguments :
    ¯¯¯¯¯¯¯¯¯¯¯
        dict0 : type=dict
            Premier dictionnaire à comparer
        
        dict1 : type=dict
            Second dictionnaire à comparer
            
        list_to_check : type=list
            Si renseignée, liste des clefs à vérifier dans les dictionnaires
            
    Returns :
    ¯¯¯¯¯¯¯¯¯
        list_different_keys : type=list
            Liste des clefs pour lesquelles les valeurs des deux dictionnaires 
            sont différentes
    """
    list_different_keys=[]
    
    if list_to_check==False:
        domain=dict0.keys()
    else:
        domain=list_to_check
        
    for key in domain :
        if dict0[key]!=dict1[key]:
            list_different_keys.append(key)
            
    return list_different_keys

def xor(a,b):
    return (not (a) and b) or (a and not(b))
    
def clamp(value, min, max):
    if value < min :
        return min
    
    if value > max :
        return max

    return value


