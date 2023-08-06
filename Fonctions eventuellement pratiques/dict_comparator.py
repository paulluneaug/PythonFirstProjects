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
        domain=dict0
    else:
        domain=list_to_check
        
    for key in domain :
        if dict0[key]!=dict1[key]:
            list_different_keys.append(key)
            
    return list_different_keys