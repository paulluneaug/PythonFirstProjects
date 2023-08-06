import tkinter as tk

def play_chess_JvJ():
    """
    Lance une partie d'Échecs, joueur contre joueur
    """
    global c, width,height,dico_state,fen,frame_turn,frame_black,frame_global
    global frame_white,label_global,label_turn,can

    c=95 #Taille en pixels de chaque case

    width=8*c
    height=width
    dico_state={}

    fen=tk.Tk()
    fen.title("Échecs J v J")

    frame_turn=tk.Frame(fen,width=width,height=50,bd=2,relief=tk.SOLID)
    frame_turn.pack_propagate(False)
    frame_turn.pack(side=tk.TOP,pady=5)

    label_turn=tk.Label(frame_turn,font='Times 15')
    label_turn.pack(pady=5)

    frame_global=tk.Frame(fen,width=width,height=50,bg='black',bd=2,relief=tk.SOLID)
    frame_global.pack_propagate(False)
    frame_global.pack(side=tk.TOP)

    label_global=tk.Label(frame_global,font='Times 20',bg='black',fg='red')
    label_global.pack(pady=5)

    can=tk.Canvas(fen,width=width,height=height)
    can.pack(padx=5,pady=5)

    frame_white=tk.Canvas(fen,width=width/2-7,height=c,bg='white',bd=2,relief=tk.SOLID)
    frame_white.pack_propagate(False)
    frame_white.pack(side=tk.LEFT,padx=8)

    frame_black=tk.Canvas(fen,width=width/2-7,height=c,bg='white',bd=2,relief=tk.SOLID)
    frame_black.pack_propagate(False)
    frame_black.pack(side=tk.RIGHT,padx=8,pady=5)
    can.bind('<Button-1>',click)
    init()
    fen.mainloop()

def grid():
    """
    Dessine sur le canevas une grille de cases noires et blanches
    """
    for x in range(8):
        for y in range(8):
            if (x+y)%2==0:
                fill='white'
            else:
                fill='#656565'
            can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill=fill,width=2)
    can.create_rectangle(2,2,width+3,height+3,outline='black',width=6)

def init():
    """
    Initialise les variables néccéssaires
    """
    global list_piece,list_white_dead,list_black_dead,whoplay
    grid()
    for x in range(8):
        for y in range(8):
            if y==0:
                if x==0 or x==7:
                    dico_state[x,y]=[1,'tour']
                elif x==1 or x==6:
                    dico_state[x,y]=[1,'cavalier']
                elif x==2 or x==5:
                    dico_state[x,y]=[1,'fou']
                elif x==3:
                    dico_state[x,y]=[1,'roi']
                elif x==4:
                    dico_state[x,y]=[1,'reine']
            elif y==1:
                dico_state[x,y]=[1,'pion']
            elif y==6:
                dico_state[x,y]=[2,'pion']
            elif y==7:
                if x==0 or x==7:
                    dico_state[x,y]=[2,'tour']
                elif x==1 or x==6:
                    dico_state[x,y]=[2,'cavalier']
                elif x==2 or x==5:
                    dico_state[x,y]=[2,'fou']
                elif x==3:
                    dico_state[x,y]=[2,'roi']
                elif x==4:
                    dico_state[x,y]=[2,'reine']
            else:
                dico_state[x,y]=[0,'']

    list_piece=[0 for i in range(32)]
    list_white_dead,list_black_dead=[],[]
    whoplay=2
    next_turn()

def next_turn():
    global whoplay,x1,y1
    x1,y1=8,8
    whoplay=abs(whoplay-3)
    list_text=['Blanc.he.s','Noir.e.s']
    list_col=['white','black']
    list_mp=['pat','mat']
    label_turn.configure(text="C'est aux "+list_text[whoplay-1]+" de jouer",
        bg=list_col[whoplay-1],fg=list_col[abs(whoplay-2)])
    frame_turn.configure(bg=list_col[whoplay-1])
    dico_poss=mov_poss(whoplay)
    if len(dico_poss.keys())==0:
        if echec(whoplay,dico_state):
            morp=1
        else :
            morp=0
        label_global.configure(text=('Échec et '+list_mp[morp]))
        label_turn.configure(text=('Les '+list_text[abs(whoplay-2)]+
            ' ont gagné'),bg=list_col[abs(whoplay-2)],fg=list_col[whoplay-1])
        frame_turn.configure(bg=list_col[abs(whoplay-2)])
        can.unbind('<Button-1>')


    if echec(whoplay,dico_state) and len(dico_poss.keys())!=0:
        label_global.configure(text='Échec')
    else:
        label_global.configure(text='')
    can_maj()

def can_maj():
    can.delete(tk.ALL)
    grid()
    i=0
    for x in range(8):
        for y in range (8):
            if dico_state[x,y][0]!=0:
                val_dic_xy=dico_state[x,y]
                list_piece[i]=[tk.PhotoImage(file=(f'80-{val_dic_xy[0]}-{val_dic_xy[1]}.png')),x,y]
                i+=1
    for j in range (i):
        can.create_image(list_piece[j][1]*c+7.5,list_piece[j][2]*c+7.5,
            anchor='nw',image=list_piece[j][0])
        can.pack()
    iw=i
    for w in range(len(list_white_dead)):
        list_piece[i]=[tk.PhotoImage(file=('40-1-'+str(list_white_dead[w])+
            '.png')),w%8,w//8]
        i+=1
    frame_white.delete(tk.ALL)
    for j in range(iw,i):
        frame_white.create_image(list_piece[j][1]*50+5,list_piece[j][2]*50+10,
            anchor='nw',image=list_piece[j][0])
    ib=i
    for b in range(len(list_black_dead)):
        list_piece[i]=[tk.PhotoImage(file=('40-2-'+str(list_black_dead[b])+
            '.png')),b%8,b//8]
        i+=1
    frame_black.delete(tk.ALL)
    for j in range(ib,i):
        frame_black.create_image(list_piece[j][1]*50+5,list_piece[j][2]*50+10,
            anchor='nw',image=list_piece[j][0])
    can.pack()

def possi(dico_state,whoplay):
    dico_poss={}
    list_piece=['pion','cavalier','tour','fou','reine','roi']
    list_fonct=[pion,cavalier,tour,fou,reine,roi]
    for x in range (8):
        for y in range (8):
            if dico_state[x,y][0]==whoplay:
                for p in range (len(list_piece)):
                    if dico_state[x,y][1]==list_piece[p]:
                        dico_poss[x,y]=list_fonct[p](dico_state,whoplay,x,y)
    return dico_poss

def mov_poss(whoplay):
    """

    """
    dico_poss=possi(dico_state,whoplay)
    dico_del={}
    for key in dico_poss.keys():
        if dico_poss[key]!=[]:
            event_key=dico_poss[key]
            p=0
            for poss in event_key:
                dico_event=dico_state.copy()
                dico_event[poss[0]]=dico_event[key]
                dico_event[key]=[0,'']
                if echec(whoplay,dico_event)==1:
                    if not (key in dico_del.keys()):
                        dico_del[key]=[]
                    dico_del[key].append(p)
                p+=1
    for item_del in dico_del.keys():
        if item_del in dico_poss.keys():
            p_del=0
            for poss_del in dico_del[item_del]:
                del dico_poss[item_del][poss_del-p_del]
                p_del+=1
    list_empty=[]
    for poss in dico_poss.keys():
        if dico_poss[poss]==[]:
            list_empty.append(poss)
    for empty_key in list_empty:
        del dico_poss[empty_key]
    return dico_poss

def can_mov_poss(dico_poss,x,y):
    """
    Dessine sur le canvas toutes les cases sur lesquelles une pièce en (x,y)
    peut aller
    """
    list_col=['green','red']
    for key in dico_poss[x,y]:
        can.create_rectangle(key[0][0]*c+1,key[0][1]*c+1,(key[0][0]+1)*c-2,
            (key[0][1]+1)*c-2,outline=list_col[key[1]],width=5)
    can.create_rectangle(x*c+1,y*c+1,(x+1)*c-2,(y+1)*c-2,outline='orange',
        width=5)

def echec(whoplay,dico_state):
    """
    Renvoie True si le joueur whoplay est en échec

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        whoplay : type=int
            Indique qui joue
            -> 1 pour les blancs
            -> 1 pour les noirs

        dico_state : type=dict
            Dictionnaire de l'état de la grile

    Returns:
    ¯¯¯¯¯¯¯
        is_echec : type=bool
            True si le joueur whoplay est en échec
            False sinon
    """
    dico_event=dico_state.copy()
    dico_poss_adv=possi(dico_event,abs(whoplay-3))
    king=0
    for x in range (8):
        for y in range(8):
            if dico_event[x,y]==[whoplay,'roi']:
                king=(x,y)
                break
        if king!=0:
            break
    is_echec=False
    for key_poss in dico_poss_adv.keys():
        for item in dico_poss_adv[key_poss]:
            if item[0]==king:
                is_echec=True
    return is_echec

def pion(dico_state,whoplay,x,y):
    """
    Dresse la liste des cases accessibles par un pion en (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        dico_state : type=dict
            Dictionnaire ded l'état de la grille

        x : type=int 0<=x<=7
            Abscisse de la case sur laquelle se situe le pion

        y : type=int 0<=y<=7
            Ordonnée de la case sur laquelle se situe le pion

    Returns:
    ¯¯¯¯¯¯¯
        list_poss : type=list
            Liste des cases accessibles par un pion en (x,y)
    """
    list_poss=[]
    if whoplay==1: #Si c'est le joueur du haut qui joue
        p=1        #le pion ne peut que descendre
        lim=1
        if y==1:   #Si le pion n'a jamais bougé,
            lim=2  #il peut bouger de 2 cases

    else:          #Si c'est le joueur du bas qui joue
        p=-1       #le pion ne peut que monter
        lim=1
        if y==6:   #Si le pion n'a jamais bougé,
            lim=2  #il peut bouger de 2 cases


    for i in range(1,lim+1):                      #Vérifie qu'il n'y a personne
        if 0<=y+(p*i)<=7:                         #dans les lim cases au dessus
            if dico_state[x,y+(p*i)]==[0,'']:     #ou au dessous du pion
                list_poss.append(((x,y+(p*i)),0))
            else:
                break
    if x!=7: #Si il y a une pièce adversiare en diagonale droite du pion
        if (x+1,y+p) in dico_state and dico_state[x+1,y+p][0]==abs(whoplay-3):
            list_poss.append(((x+1,y+p),1)) #Indique qu'il peut la manger

    if x!=0: #Si il y a une pièce adversiare en diagonale gauche du pion
        if (x-1,y+p) in dico_state and dico_state[x-1,y+p][0]==abs(whoplay-3):
            list_poss.append(((x-1,y+p),1)) #Indique qu'il peut la manger
    return list_poss

def cavalier(dico_state,whoplay,x,y):
    """
    Dresse la liste des cases accessibles par un cavalier en (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        dico_state : type=dict
            Dictionnaire ded l'état de la grille

        x : type=int 0<=x<=7
            Abscisse de la case sur laquelle se situe le cavalier

        y : type=int 0<=y<=7
            Ordonnée de la case sur laquelle se situe le cavalier

    Returns:
    ¯¯¯¯¯¯¯
        list_poss : type=list
            Liste des cases accessibles par un cavalier en (x,y)
    """
    list_poss=[]
    list_cav=[c for c in range(-2,3) if c!=0]
    for c1 in list_cav:
        for c2 in list_cav:
            if (c1+c2)%2!=0:
                if 0<=x+c1<=7 and 0<=y+c2<=7:
                    if dico_state[x+c1,y+c2][0]!=whoplay:
                        if dico_state[x+c1,y+c2][0]==0:
                            list_poss.append(((x+c1,y+c2),0))
                        else:
                            list_poss.append(((x+c1,y+c2),1))
    return list_poss

def tour(dico_state,whoplay,x,y):
    """
    Dresse la liste des cases accessibles par une tour en (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        dico_state : type=dict
            Dictionnaire ded l'état de la grille

        x : type=int 0<=x<=7
            Abscisse de la case sur laquelle se situe la tour

        y : type=int 0<=y<=7
            Ordonnée de la case sur laquelle se situe la tour

    Returns:
    ¯¯¯¯¯¯¯
        list_poss : type=list
            Liste des cases accessibles par une tour en (x,y)
    """
    list_poss=[]
    list_d=[(0,-1),(1,0),(0,1),(-1,0)]
    for d in list_d:
        jx=d[0]
        jy=d[1]
        ix=jx
        iy=jy
        while 0<=x+ix<=7 and 0<=y+iy<=7:
            if dico_state[x+ix,y+iy][0]==whoplay:
                break
            elif dico_state[x+ix,y+iy][0]==0:
                list_poss.append(((x+ix,y+iy),0))
            else:
                list_poss.append(((x+ix,y+iy),1))
                break
            ix+=jx
            iy+=jy
    return list_poss

def fou(dico_state,whoplay,x,y):
    """
    Dresse la liste des cases accessibles par un fou en (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        dico_state : type=dict
            Dictionnaire ded l'état de la grille

        x : type=int 0<=x<=7
            Abscisse de la case sur laquelle se situe le fou

        y : type=int 0<=y<=7
            Ordonnée de la case sur laquelle se situe le fou

    Returns:
    ¯¯¯¯¯¯¯
        list_poss : type=list
            Liste des cases accessibles par un fou en (x,y)
    """
    list_poss=[]
    list_d=[(1,-1),(1,1),(-1,1),(-1,-1)]
    for d in list_d:
        ix=d[0]
        iy=d[1]
        while 0<=x+ix<=7 and 0<=y+iy<=7:
            if dico_state[x+ix,y+iy][0]==whoplay:
                break
            elif dico_state[x+ix,y+iy][0]==0:
                list_poss.append(((x+ix,y+iy),0))
                ix+=d[0]
                iy+=d[1]
            else:
                list_poss.append(((x+ix,y+iy),1))
                break
    return list_poss

def reine(dico_state,whoplay,x,y):
    """
    Dresse la liste des cases accessibles par une reine en (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        dico_state : type=dict
            Dictionnaire ded l'état de la grille

        x : type=int 0<=x<=7
            Abscisse de la case sur laquelle se situe la reine

        y : type=int 0<=y<=7
            Ordonnée de la case sur laquelle se situe la reine

    Returns:
    ¯¯¯¯¯¯¯
        list_poss : type=list
            Liste des cases accessibles par une reine en (x,y)
    """
    #Dresse la liste des mouvements d'un fou en (x,y)
    list_poss_fou=fou(dico_state,whoplay,x,y)

    #Dresse la liste des mouvements d'une tour en (x,y)
    list_poss=tour(dico_state,whoplay,x,y)

    for item in list_poss_fou: #Fusionne les deux listes
        list_poss.append(item)
    return list_poss

def roi(dico_state,whoplay,x,y):
    """
    Dresse la liste des cases accessibles par un roi en (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        dico_state : type=dict
            Dictionnaire ded l'état de la grille

        x : type=int 0<=x<=7
            Abscisse de la case sur laquelle se situe le roi

        y : type=int 0<=y<=7
            Ordonnée de la case sur laquelle se situe le roi

    Returns:
    ¯¯¯¯¯¯¯
        list_poss : type=list
            Liste des cases accessibles par un roi en (x,y)
    """
    list_poss=[]
    list_d=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
    for d in list_d:
        ix=d[0]
        iy=d[1]
        if 0<=x+ix<=7 and 0<=y+iy<=7:
            if dico_state[x+ix,y+iy][0]!=whoplay:
                if dico_state[x+ix,y+iy][0]==0:
                    list_poss.append(((x+ix,y+iy),0))
                else:
                    list_poss.append(((x+ix,y+iy),1))
    return list_poss


def click(event):
    global x1,y1,list_white_dead,list_black_dead,dico_poss
    cx=event.x//c
    cy=event.y//c
    can_maj()
    if dico_state[cx,cy][0]==whoplay:
        x1,y1=cx,cy
        dico_poss=mov_poss(whoplay)



    if (x1,y1) in dico_poss.keys():
        can_mov_poss(dico_poss,x1,y1)
        tf=[False,-1]
        i=0
        for mov in dico_poss[x1,y1]:
            if mov[0]==(cx,cy):
                tf=[True,i]
                break
            else:
                i+=1
        if tf!=[False,-1]:
            if dico_poss[x1,y1][tf[1]][1]==0:
                dico_state[x1,y1],dico_state[cx,cy]=dico_state[cx,cy],dico_state[x1,y1]
                x1,y1=cx,cy
                can_maj()
            else:
                if dico_state[cx,cy][0]==1:
                    list_white_dead.append(dico_state[cx,cy][1])
                else:
                    list_black_dead.append(dico_state[cx,cy][1])
                dico_state[cx,cy],dico_state[x1,y1]=dico_state[x1,y1],[0,'']

            next_turn()
            for a in range(8): #Vérifie si un pion est arrivé au bout
                if dico_state[(a,0)][1]=='pion':
                    create_fen_replace_pawn(a,0,1)
                if dico_state[(a,7)][1]=='pion':
                    create_fen_replace_pawn(a,7,1)



def create_fen_replace_pawn(x,y,color):
    """
    Créé une fenêtre de 4 boutons pour remplacer le pion arrivé au bout
    """
    global fen_new_piece
    fen_new_piece=tk.Tk()
    fen_new_piece.title('Choisir une nouvelle pièce')


    list_piece_replace=['tour','cavalier','fou','reine']

    for i in range(len(list_piece_replace)): #Créé 1 boutons pour chaque pièce
        but_piece=tk.Button(fen_new_piece,
            text=' '*((8-len(list_piece_replace[i]))//2)+
            list_piece_replace[i][0].upper()+list_piece_replace[i][1:]+
            ' '*((8-len(list_piece_replace[i]))//2),font='Times 20',
            command=lambda x=x,y=y,piece=list_piece_replace[i],
            eff=None:replace_pawn(x,y,piece))

        but_piece.grid(column=0,row=i)

    fen_new_piece.mainloop()

def replace_pawn(x,y,new_piece):
    """
    Remplace la pièce en (x,y) par une nouvelle pièce

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        x : type=int 0<=x<=7
            Abscisse de la case à remplacer

        y : type=int 0<=y<=7
            Ordonnée de la case à remplacer

        new_piece : type=str
            Nouvelle pièce à placer en (x,y)
    """
    global dico_state
    fen_new_piece.destroy()#Détruit la fenêtre de sélection de la nouvelle pièce
    dico_state[x,y][1]=new_piece
    can_maj()
    next_turn()
    next_turn()



play_chess_JvJ()


