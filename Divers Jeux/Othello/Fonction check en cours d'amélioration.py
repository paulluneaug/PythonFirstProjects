def check(x,y,whoplay):
    """
    Vérifie si le joueur ou l'ordinateur peut poser un pion en (x,y) et si oui,
    dresse la liste des directions dans lesquelles des pions sont à retourner

    Si c'est l'ordinateur qui joue, lui renvoie les points associés

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        x : type = int
            Coordonnée x de la case à verifier

        y : type = int
            Coordonnée y de la case à verifier

        whoplay : type=int 3<=whoplay<=4
            Désigne qui joue
            3 -> le joueur
            4 -> l'ordinateur

    Return:
    ¯¯¯¯¯¯
        pts : type = int
            Point que gagnerait celui qui joue s'il place son pion ici
            -1 s'il ne peut pas jouer

        list_tf : type = list
            Liste de 8 Booléens
            True si il y a des pièces à retourner dans cette direction
            False sinon

    """
    if dico_state[x,y]==0:
        if whoplay==3:
            color=player_color
            en_color=com_color
        elif whoplay==4:
            color=com_color
            en_color=player_color

        list_d=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]

        liste_tf=[False for a in range(8)]
        for direct in range(8):
            if 0<=x<=7 and 0<=y<=7:
                i=1
                evo_x,evo_y=x+list_d[direct][0]*i,y+list_d[direct][1]*i
                if (evo_x,evo_y) in dico_state.keys():
                    val_evo=dico_state[evo_x,evo_y]
                    in_dict=True
                else:
                    val_evo=0
                    in_dict=False
                if in_dict :
                    while val_evo==en_color and 0<evo_x<7 and 0<evo_y<7:
                        i+=1
                        evo_x,evo_y=x+list_d[direct][0]*i,y+list_d[direct][1]*i
                        val_evo=dico_state[evo_x,evo_y]
                        print(list_d[direct],evo_x,evo_y)
                if val_evo==color and i!=1:
                    liste_tf[direct]=True

        print(liste_tf,5*'_____________________________',sep='\n')
        t=liste_tf.count(True)
        if whoplay==3:
            if t==0:
                global_message.configure(text='Coup Impossible')
            else:
                global_message.configure(text='')
                maj_dico(x,y,player_color,liste_tf,False)
        elif whoplay==4:
            if t==0:
                return -1,[]
            else:
                return maj_dico(x,y,com_color,liste_tf,True),liste_tf
    else:
        return -1,[]