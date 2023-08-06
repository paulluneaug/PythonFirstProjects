import tkinter as tk

def level_editor():
    """
    Ouvre un éditeur de niveaux
    """
    global fen,can_main,x_can,y_can,c_main,dict_state,selected_tile,grid_enable

    x_can,y_can=4,4

    c_main=700//max(x_can,y_can)

    fen=tk.Tk()
    fen.title('Editeur de niveau')

    can_main=tk.Canvas(fen,width=x_can*c_main,height=y_can*c_main,bg='white')#,relief=tk.SOLID,borderwidth=3)
    can_main.grid(column=0,row=0)

    dict_state={}
    for case in [(a,b) for a in range(x_can) for b in range(y_can)]:
        dict_state[case]=None
    selected_tile='block'

    grid_enable=True
    grid(can_main,x_can*c_main,y_can*c_main,c_main)
    can_update("all")

    can_main.bind('<Button-1>',left_click_main)
    can_main.bind('<Button-3>',right_click_main)
    can_main.bind('<B1-Motion>',left_click_main)
    can_main.bind('<B3-Motion>',right_click_main)

    create_fra_right()

    fen.mainloop()

def create_fra_right():
    """
    Créé un cadre à droite du canvas principal avec une liste des différentes cases plaçables et une série de boutons
    """
    global but_grid

    list_tile=['block','spike','bounce','speed up'] #Liste des différentes cases plaçables
    c_can_right=50 #Taille en pixels du coté de chaque canvas contenant une case
    tile_per_row=3 #Nombre de cases par ligne

    #Créé le cadre
    fra_right=tk.Frame(fen,width=x_can*c_main//2,height=y_can*c_main,bg='black')
    fra_right.grid(column=1,row=0)
    fra_right.grid_propagate(False)

    #Créé un canvas pour chaque case plaçable
    for t in range(len(list_tile)):
        can_temp=tk.Canvas(fra_right,width=c_can_right,height=c_can_right,bg='white')
        can_temp.grid(column=t%tile_per_row,row=(t//tile_per_row))

        #Dessine le type de case
        draw_tile(can_temp,0,0,list_tile[t],c_can_right)

        #Permet de cliquer sur le canvas pour sélectionner la case
        can_temp.bind('<Button-1>',lambda x,new_tile=list_tile[t],eff=None : select_new_tile(new_tile))


    but_grid=tk.Button(fra_right,text='Désactiver la grille',command=disable_grid)
    but_grid.grid(column=tile_per_row,row=0)

    but_done=tk.Button(fra_right,text='Valider',command=done)
    but_done.grid(column=tile_per_row,row=1)


def select_new_tile(new_tile):
    """
    Sélectionne une nouvelle case à placer
    """
    global selected_tile
    selected_tile=new_tile

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
    while vx<width:
        can.create_line(vx,0,vx,height,width=1,fill='black',tag='grid')
        vx+=c
    while vy<height:
        can.create_line(0,vy,width,vy,width=1,fill='black',tag='grid')
        vy+=c

def disable_grid():
    global grid_enable
    grid_enable =not grid_enable
    if grid_enable:
        grid(can_main,x_can*c_main,y_can*c_main,c_main)
        but_grid.configure(text='Désactiver la grille')
    else:
        can_main.delete('grid')
        but_grid.configure(text='Activer la grille')

def done():
    level_nbr=input('Niveau numéro : ')
    file_level=open(f'level{level_nbr}.txt','w',encoding='utf8')
    print(dict_state,file=file_level)


def can_update(co):
    """
    Met à jour une ou toutes les cases de la grille

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        co : type=tuple ou str
            Indique quelles cases doivent être mises à jour
            -'all'
            ou
            -(x,y)
    """
    if co=="all": #Met à jour toutes les cases
        can_main.delete(co)
        if grid_enable:
            grid(can_main,x_can*c_main,y_can*c_main,c_main)
        for tile in dict_state.keys():
            if dict_state[tile]!=None:
                draw_tile(can_main,tile[0],tile[1],dict_state[tile],c_main)

    else: #Met à jour seulement la case en coordonnées 'co'
        can_main.delete(f'{co[0]}/{co[1]}')
        if dict_state[co]!=None:
            draw_tile(can_main,co[0],co[1],dict_state[co],c_main)

def right_click_main(event):
    """
    Efface la case sur laquelle l'utilisat.eur.rice a cliqué
    """
    x_rc,y_rc=event.x//c_main,event.y//c_main
    if (x_rc,y_rc) in dict_state and dict_state[x_rc,y_rc]!=None:
        dict_state[x_rc,y_rc]=None
        can_update((x_rc,y_rc))

def left_click_main(event):
    """
    Remplace la case sur laquelle l'utilisat.eur.rice a cliqué par la case
    sélectionnée
    """
    x_lc,y_lc=event.x//c_main,event.y//c_main
    if (x_lc,y_lc) in dict_state and dict_state[x_lc,y_lc]!=selected_tile:
        dict_state[x_lc,y_lc]=selected_tile
        can_update((x_lc,y_lc))

def draw_tile(can,x,y,tile_type,c):
    """
    Dessine la case en (x,y)

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        can : type=tkinter.Canvas
            Canvas sur lequel dessiner la case

        x : type=int
            Abscisse de la case à dessiner

        y : type=int
            Ordonnée de la case à dessiner

        tile_type : type=str
            Type de case à dessiner parmi :
                block, spike, bounce, speed up

        c : type=int
            Longueur en pixels de la case sur laquelle dessiner
    """
    if tile_type=='block':
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='grey',tag=f'{x}/{y}')

    elif tile_type=='spike':
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='red',tag=f'{x}/{y}')

    elif tile_type=='bounce':
        can.create_rectangle(x*c,(y+0.85)*c,(x+1)*c,(y+1)*c,fill='blue',tag=f'{x}/{y}',width=0)

    elif tile_type=='speed up':
        can.create_rectangle(x*c,(y+0.85)*c,(x+1)*c,(y+1)*c,fill='green',tag=f'{x}/{y}',width=0)


level_editor()