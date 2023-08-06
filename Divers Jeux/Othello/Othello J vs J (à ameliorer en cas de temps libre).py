from tkinter import*


def grid():
    """Dessine la grille"""
    vx=0
    vy=0
    while vx!=width:
        can.create_line(vx,0,vx,width,width=2,fill='#000000')
        vx+=c
    while vy!=height:
        can.create_line(0,vy,height,vy,width=2,fill='#000000')
        vy+=c

def init():
    """Initialise dicostate et la grille"""
    grid()
    for dx in range(dim):
        for dy in range(dim):
            dicostate[(dx,dy)]=0
    dicostate[dim/2-1,dim/2-1]=1
    dicostate[dim/2-1,dim/2]=2
    dicostate[dim/2,dim/2-1]=2
    dicostate[dim/2,dim/2]=1


def maj():
    """Met à jour la grille"""
    global white,black,pion
    white=0
    black=0
    list_wb=['white','black']
    list_bn=['Blanc.he.s','Noir.e.s']
    for dx in range (dim):
        for dy in range (dim):
            if dicostate[dx,dy]!=0:
                if dicostate[dx,dy]==1:
                    white+=1
                elif dicostate[dx,dy]==2:
                    black+=1
                can.create_oval(dx*c+c/10,dy*c+c/10,dx*c+9*c/10,dy*c+9*c/10,
                    outline=list_wb[abs(dicostate[dx,dy]-3)-1],
                    fill=list_wb[dicostate[dx,dy]-1], width=3)
                pts_white.configure(text = ("Pions Blancs : "+str(white)))
                pts_black.configure(text = ("Pions Noirs : "+str(black)))
                pts_rst.configure(text = ("Pions Restants : "+
                    str(dim**2-(black+white))))
    if pion==dim**2 or white==pion or black==pion:
        if white>black:
            global_message.configure(text='Les Blanc.he.s ont gagné')
        elif black>white:
            global_message.configure(text='Les Noir.e.s ont gagné')
        else:
            global_message.configure(text='Égalité')
        global_message.pack()
    else:
        frame_color.configure(bg=list_wb[bw-1])
        label_whoplay.configure(bg=list_wb[bw-1],fg=list_wb[abs(bw-3)-1],
            text=("C'est aux "+list_bn[bw-1]+" de jouer"))
        label_whoplay.pack(pady=2)



def click(event):
    """Détecte la position du clic, met à jour dicostate pour correspondre à
    l'état dans lequel il doit se trouver"""
    global bw,pion,color,white,black
    if pion!=dim**2 and white!= pion and black!=pion:
        x = int((event.x -(event.x%c))/c)
        y = int((event.y -(event.y%c))/c)
        if dicostate[x,y]==0:
            t=0
            tfN=False
            if y !=0:#Recherche de case de même couleur au Nord
                i=1
                while dicostate[x,y-i]!=bw and dicostate[x,y-i]!=0 and y-i>0:
                    i+=1
                if dicostate[x,y-i]== bw and i!=1:
                    tfN=True
                    t+=1
            tfNE=False
            if x!=dim-1 and y!=0:#Recherche de case de même couleur au Nord-Est
                i=1
                while dicostate[x+i,y-i]!=bw and dicostate[x+i,y-i]!=0 and x+i<dim-1 and y-i>0:
                    i+=1
                if dicostate[x+i,y-i]== bw and i!=1:
                    tfNE=True
                    t+=1
            tfE=False
            if x!=dim-1:#Recherche de case de même couleur à l'Est
                i=1
                while dicostate[x+i,y]!=bw and dicostate[x+i,y]!=0 and x+i<dim-1:
                    i+=1
                if dicostate[x+i,y]== bw and i!=1:
                    tfE=True
                    t+=1
            tfSE=False
            if x!=dim-1 and y!=dim-1:#Recherche de case de même couleur au Sud-Est
                i=1
                while dicostate[x+i,y+i]!=bw and dicostate[x+i,y+i]!=0 and x+i<dim-1 and y+i<dim-1:
                    i+=1
                if dicostate[x+i,y+i]== bw and i!=1:
                    tfSE=True
                    t+=1
            tfS=False
            if y!=dim-1:#Recherche de case de même couleur au Sud
                i=1
                while dicostate[x,y+i]!=bw and dicostate[x,y+i]!=0 and y+i<dim-1:
                    i+=1
                if dicostate[x,y+i]== bw and i!=1:
                    tfS=True
                    t+=1
            tfSO=False
            if x!=0 and y!=dim-1:#Recherche de case de même couleur au Sud-Ouest
                i=1
                while dicostate[x-i,y+i]!=bw and dicostate[x-i,y+i]!=0 and x-i>0 and y+i<dim-1:
                    i+=1
                if dicostate[x-i,y+i]== bw and i!=1:
                    tfSO=True
                    t+=1
            tfO=False
            if x!=0:#Recherche de case de même couleur à l'Ouest
                i=1
                while dicostate[x-i,y]!=bw and dicostate[x-i,y]!=0 and x-i>0:
                    i+=1
                if dicostate[x-i,y]== bw and i!=1:
                    tfO=True
                    t+=1
            tfNO=False
            if x!=0 and y!=0:#Recherche de case de même couleur au Nord-Ouest
                i=1
                while dicostate[x-i,y-i]!=bw and dicostate[x-i,y-i]!=0 and x-i>0 and y-i>0:
                    i+=1
                if dicostate[x-i,y-i]== bw and i!=1:
                    tfNO=True
                    t+=1
            if t!=0:
                if tfN==True:#Mise à jour de dicostate pour le Nord
                    j=1
                    while dicostate[x,y-j]!=bw:
                        dicostate[x,y-j]=bw
                        j+=1
                if tfNE==True:#Mise à jour de dicostate pour le Nord-Est
                    j=1
                    while dicostate[x+j,y-j]!=bw:
                        dicostate[x+j,y-j]=bw
                        j+=1
                if tfE==True:#Mise à jour de dicostate pour l'Est
                    j=1
                    while dicostate[x+j,y]!=bw:
                        dicostate[x+j,y]=bw
                        j+=1
                if tfSE==True:#Mise à jour de dicostate pour le Sud-Est
                    j=1
                    while dicostate[x+j,y+j]!=bw:
                        dicostate[x+j,y+j]=bw
                        j+=1
                if tfS==True:#Mise à jour de dicostate pour le Sud
                    j=1
                    while dicostate[x,y+j]!=bw:
                        dicostate[x,y+j]=bw
                        j+=1
                if tfSO==True:#Mise à jour de dicostate pour le Sud-Ouest
                    j=1
                    while dicostate[x-j,y+j]!=bw:
                        dicostate[x-j,y+j]=bw
                        j+=1
                if tfO==True:#Mise à jour de dicostate pour l'Ouest
                    j=1
                    while dicostate[x-j,y]!=bw:
                        dicostate[x-j,y]=bw
                        j+=1
                if tfNO==True:#Mise à jour de dicostate pour le Nord-Ouest
                    j=1
                    while dicostate[x-j,y-j]!=bw:
                        dicostate[x-j,y-j]=bw
                        j+=1
                dicostate[x,y]=bw
                pion+=1
                bw=abs(bw-3)
                global_message.configure(text='')
                maj()
            else:
                global_message.configure(text='Mais c mal joué wsh !')


def skip_turn():
    global bw
    bw=abs(bw-3)
    maj()


bw=2       #Indique la couleur qui commence (white->1;black->2)
if bw==1:
    color='black'
else:
    color='white'

dim=20
c=int(750/dim)      #Définition de la taille des cases
white=0
black=0
height=dim*c
width=height
fen1=Tk()
fen1.title('Othello')

frame_color=Frame(fen1,height=50,width=width+4,bd=2,relief=SOLID)
frame_color.pack_propagate(False)
frame_color.pack(side=TOP,padx=5,pady=5)

label_whoplay=Label(frame_color,font='Times 20')

frame_top=Frame(fen1,height=50,width=width+4,bg='black',bd=2,relief=SOLID)
frame_top.pack_propagate(False)
frame_top.pack(side=TOP)

frame_top_pts=Frame(fen1,height=50,width=width+4,bg='green',bd=2,relief=SOLID)
frame_top_pts.pack_propagate(False)
frame_top_pts.pack(side=TOP,padx=5)

global_message=Label(frame_top,fg='red',bg='black',font='Times 20')
global_message.pack(pady=5)

pts_white=Label(frame_top_pts,bg='green',font='Times 15')
pts_white.pack(side=LEFT,padx=10)

pts_black=Label(frame_top_pts,bg='green',font='Times 15')
pts_black.pack(side=RIGHT,padx=10)

pts_rst=Label(frame_top_pts,bg='green',font='Times 15')
pts_rst.pack(pady=10)

can=Canvas(fen1,height=height,width=width,bg='green',bd=2,relief=SOLID)
can.pack(side=TOP)


frame_bottom_pass=Frame(fen1,height=90,width=width/2-5,bg='green',bd=2,
    relief=SOLID)
frame_bottom_pass.pack_propagate(False)
frame_bottom_pass.pack(side=RIGHT,padx=5,pady=5)


but_skip=Button(frame_bottom_pass,text='Passer son tour',font='Times 20',
    command=skip_turn)
but_skip.pack(side=LEFT,padx=60)
dicostate={}
init()
pion=4
maj()
can.bind('<Button-1>',click)



fen1.mainloop()