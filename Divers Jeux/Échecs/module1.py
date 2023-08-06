def poss(whoplay):
    dico_poss={}
    for x in range (8):
        for y in range (8):
            if dico_state[x,y][0]==whoplay:
                piece=dico_state[x,y][1]
                if piece=='pion':
                    liste_poss=pion(whoplay,x,y)
                elif piece=='tour':
                    liste_poss=tour(whoplay,x,y)
                elif piece=='cavalier':
                    liste_poss=cavalier(whoplay,x,y)
                elif piece=='fou':
                    liste_poss=fou(whoplay,x,y)
                elif piece=='reine':
                    liste_poss=reine(whoplay,x,y)
                elif piece=='roi':
                    liste_poss=roi(whoplay,x,y)
                dico_poss[x,y]=liste_poss

