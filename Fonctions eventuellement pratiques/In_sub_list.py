def in_sub_list(item,liste,depth=None):
    if depth==None:
        if type(liste)!=list and type(liste)!=tuple:
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
        if type(liste)!=list and type(liste)!=tuple:
            return item==liste,[]
        for i in range(len(liste)):
            is_in,path=in_sub_list(item,liste[i],depth=depth-1)
            if is_in:
                return is_in,[i]+path
            elif i==len(liste)-1:
                return False,[]
