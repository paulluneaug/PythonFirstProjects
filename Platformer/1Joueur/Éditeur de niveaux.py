import tkinter as tk
import graphic_module as graph
import useful_module as use
import clean_input as ci
import Platformer1Joueur as plat

class event:
    def __init__(self,delta):
        self.delta=delta


def level_editor():
    """
    Ouvre un éditeur de niveaux
    """
    global fen,can_main,x_can,y_can,c_main,dict_state,selected_tile,grid_enable

    x_can,y_can=10,5

    c_main=1200//max(x_can,y_can)

    fen=tk.Tk()
    fen.title('Editeur de niveau')

    can_main=tk.Canvas(fen,width=x_can*c_main,height=y_can*c_main,bg='white')#,relief=tk.SOLID,borderwidth=3)
    can_main.grid(column=0,row=0)

    dict_state={}

    for j in range(x_can):
        dict_state[j,-1]=['block']
        dict_state[j,y_can]=['block']

    for k in range(y_can):
        dict_state[-1,k]=['block']
        dict_state[x_can,k]=['block']

    for none_tile in [(a,b) for a in range(x_can) for b in range(y_can)]:
        dict_state[none_tile]=[None]

    for y in [0,y_can-1]: #Place les bordures en haut et en bas du niveau
        for x in range(x_can):
            dict_state[x,y]=['block']

    for x in [0,x_can-1]: #Place les bordures à gauche et à droite du niveau
        for y in [_ for _ in range(y_can)]:
            dict_state[x,y]=['block']

    #Place un checkpoint au début du niveau
    dict_state[1,y_can-2]=['checkpoint',[]]

    #Place des portails aux extrémités du niveau
    dict_state[0,y_can-2],dict_state[0,y_can-3]=['portal-in','left'],['portal-in','left']
    dict_state[x_can-1,y_can-2],dict_state[x_can-1,y_can-3]=['portal-out','right'],['portal-out','right']

    selected_tile='block'

    grid_enable=True
    use.grid(can_main,x_can*c_main,y_can*c_main,c_main)
    graph.can_update(can_main,["all"],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)


    can_main.bind('<Button-1>',left_click_main)
    can_main.bind('<Control-1>',left_click_group)
    can_main.bind('<Button-2>',pick_tile)
    can_main.bind('<Button-3>',right_click_main)
    can_main.bind('<Control-3>',right_click_group)

    can_main.bind('<B1-Motion>',left_click_main)
    can_main.bind('<B3-Motion>',right_click_main)

    fen.bind('<MouseWheel>',scroll)
    fen.bind('<Shift-MouseWheel>',shift_scroll)
    fen.bind('<Up>',lambda x,e=event(1):scroll(e))
    fen.bind('<Down>',lambda x,f=event(-1):scroll(f))
    fen.bind('<Shift-Up>',lambda x,e=event(1):shift_scroll(e))
    fen.bind('<Shift-Down>',lambda x,f=event(-1):shift_scroll(f))

    create_fra_right()

    fen.mainloop()

def create_fra_right():
    """
    Créé un cadre à droite du canvas principal avec une liste des différentes cases plaçables et une série de boutons
    """
    global but_grid,entry_channel,entry_bg_color,entry_way,c_can_right
    global can_sel_tile,entry_on_off,entry_enable,entry_mirror,entry_timed

    #Liste des différentes cases plaçables
    list_tile=['block','spike','bounce','sticky','speed-up','slow-down','door',
               'key','bg','breakable-block','checkpoint','portal-in',
               'portal-out','one-way-block','heart','on-off-switch','on-block',
               'off-block','timed-block','laser-emitter','laser-reciever',
               'mirror','glass','button','on-off-door']

    c_can_right=40 #Taille en pixels du coté de chaque canvas contenant une case
    tile_per_row=3 #Nombre de cases par ligne

    #Créé le cadre
    fra_right=tk.Frame(fen,width=450,height=y_can*c_main,bg='black')
    fra_right.grid(column=1,row=0)
    fra_right.grid_propagate(False)

    #Créé un canvas pour chaque case plaçable
    for t in range(len(list_tile)):
        can_temp=tk.Canvas(fra_right,width=c_can_right,height=c_can_right,bg='white')
        can_temp.grid(column=t%tile_per_row,row=(t//tile_per_row))

        #Dessine le type de case
        graph.draw_tile(can_temp,0,0,list_tile[t],c_can_right)

        #Permet de cliquer sur le canvas pour sélectionner la case
        can_temp.bind('<Button-1>',lambda x,new_tile=list_tile[t],eff=None : select_new_tile(new_tile))

    fra_but=tk.Frame(fra_right,bg='black')
    fra_but.grid(column=tile_per_row+1,row=0,rowspan=len(list_tile)//tile_per_row+1)

    but_grid=tk.Button(fra_but,text='Désactiver la grille',command=disable_grid)
    but_grid.pack(side='top',anchor='nw',padx=5,pady=2.5)

    but_done=tk.Button(fra_but,text='Valider',command=done)
    but_done.pack(side='top',anchor='nw',padx=5,pady=2.5)

    but_erease=tk.Button(fra_but,text='Tout supprimer',command=erease)
    but_erease.pack(side='top',anchor='nw',padx=5,pady=2.5)

    but_modif=tk.Button(fra_but,text='Modifier un niveau existant',
                        command=modif_level)
    but_modif.pack(side='top',anchor='nw',padx=5,pady=2.5)

    but_test=tk.Button(fra_but,text='Tester ce niveau',command=test_level)
    but_test.pack(side='top',anchor='nw',padx=5,pady=2.5)

    fra_channel=tk.Frame(fra_but,bg='black')
    fra_channel.pack(side='top',anchor='nw',padx=5,pady=2.5)

    lab_channel=tk.Label(fra_channel,text='Channel n° : ')
    lab_channel.grid(column=0,row=0)

    entry_channel=tk.Entry(fra_channel)
    entry_channel.grid(column=1,row=0)
    entry_channel.insert(0,'0')

    fra_bg_color=tk.Frame(fra_but,bg='black')
    fra_bg_color.pack(side='top',anchor='nw',padx=5,pady=2.5)

    lab_bg_color=tk.Label(fra_bg_color,text="Couleur de l'arrière-plan : ")
    lab_bg_color.grid(column=0,row=0)

    entry_bg_color=tk.Entry(fra_bg_color)
    entry_bg_color.grid(column=1,row=0)
    entry_bg_color.insert(0,'#FFFF5A')

    fra_way=tk.Frame(fra_but,bg='black')
    fra_way.pack(side='top',anchor='nw',padx=5,pady=2.5)

    lab_way=tk.Label(fra_way,text='Sens : ')
    lab_way.grid(column=0,row=0)

    entry_way=tk.Entry(fra_way)
    entry_way.grid(column=1,row=0)
    entry_way.insert(0,'left')

    fra_on_off=tk.Frame(fra_but,bg='black')
    fra_on_off.pack(side='top',anchor='nw',padx=5,pady=2.5)

    lab_on_off=tk.Label(fra_on_off,text='On/Off : ')
    lab_on_off.grid(column=0,row=0)

    entry_on_off=tk.Entry(fra_on_off)
    entry_on_off.grid(column=1,row=0)
    entry_on_off.insert(0,'on')

    fra_enable=tk.Frame(fra_but,bg='black')
    fra_enable.pack(side='top',anchor='nw',padx=5,pady=2.5)

    lab_enable=tk.Label(fra_enable,text='Bloc Activé : ')
    lab_enable.grid(column=0,row=0)

    entry_enable=tk.Entry(fra_enable)
    entry_enable.grid(column=1,row=0)
    entry_enable.insert(0,'True')

    fra_mirror=tk.Frame(fra_but,bg='black')
    fra_mirror.pack(side='top',anchor='nw',padx=5,pady=2.5)

    lab_mirror=tk.Label(fra_mirror,text='Position Miroir : ')
    lab_mirror.grid(column=0,row=0)

    entry_mirror=tk.Entry(fra_mirror)
    entry_mirror.grid(column=1,row=0)
    entry_mirror.insert(0,'0')

    fra_timed=tk.Frame(fra_but,bg='black')
    fra_timed.pack(side='top',anchor='nw',padx=5,pady=2.5)

    lab_timed=tk.Label(fra_timed,text='Temps de départ : ')
    lab_timed.grid(column=0,row=0)

    entry_timed=tk.Entry(fra_timed)
    entry_timed.grid(column=1,row=0)
    entry_timed.insert(0,'0')

    can_sel_tile=tk.Canvas(fra_right,width=c_can_right,height=c_can_right)
    can_sel_tile.grid(column=0,row=len(list_tile)//tile_per_row+8)

    update_sel_tile_can()

def select_new_tile(new_tile):
    """
    Sélectionne une nouvelle case à placer
    """
    global selected_tile
    selected_tile=new_tile
    update_sel_tile_can()


def disable_grid():
    """
    Désactive ou active la grille
    """
    global grid_enable
    grid_enable =not grid_enable
    if grid_enable: #Dessine la grille
        use.grid(can_main,x_can*c_main,y_can*c_main,c_main)
        but_grid.configure(text='Désactiver la grille')
    else: #Supprime la grille
        can_main.delete('grid')
        but_grid.configure(text='Activer la grille')

def done():
    """
    Exporte le niveau dans un fichier dont on choisit un nom
    """
    level_nbr=ci.clean_input('Niveau numéro : ')

    #Choisit un état des blocs on-off (soit on, soit off) en fonction des
    #interrupteurs et active ou désactive tous les blocs on-off selon l'état de
    #l'interrupteur
    on_off_channel=None
    list_on_off_not_done=[]
    for k in dict_state.keys():
        if dict_state[k][0]=='on-off-switch':
            if on_off_channel==None: #Cherche l'état à appliquer
                on_off_channel=dict_state[k][1]
                print(on_off_channel)

            dict_state[k][1]=on_off_channel


        elif dict_state[k][0] in ('on-block','off-block'):
            if on_off_channel==None:
                list_on_off_not_done.append(k)

            else:
                dict_state[k][1]=dict_state[k][0][:len(on_off_channel)]==on_off_channel

    for o in list_on_off_not_done:
        dict_state[o][1]=dict_state[o][0][:len(on_off_channel)]==on_off_channel

    #Place aussi des barrières aussi autour du niveau

    for j in range(x_can):
        dict_state[j,-1]=['block']
        dict_state[j,y_can]=['block']

    for k in range(y_can):
        dict_state[-1,k]=['block']
        dict_state[x_can,k]=['block']

    #Exporte le niveau
    file_level=open(f'Levels/{level_nbr}.txt','w',encoding='utf8')
    print(dict_state,file=file_level)



def erease():
    """
    Supprime toutes les cases de la grille et replace les bordures
    """
    global dict_state

    dict_state={}

    for none_tile in [(a,b) for a in range(x_can) for b in range(y_can)]:
        dict_state[none_tile]=[None]

    for y in [0,y_can-1]: #Place les bordures en haut et en bas du niveau
        for x in range(x_can):
            dict_state[x,y]=['block']

    for x in [0,x_can-1]: #Place les bordures à gauche et à droite du niveau
        for y in [_ for _ in range(y_can)]:
            dict_state[x,y]=['block']

    #Place un checkpoint au début du niveau
    dict_state[1,y_can-2]=['checkpoint',[]]

    #Place des portails aux extrémités du niveau
    dict_state[0,y_can-2],dict_state[0,y_can-3]=['portal-in','left'],['portal-in','left']
    dict_state[x_can-1,y_can-2],dict_state[x_can-1,y_can-3]=['portal-out','right'],['portal-out','right']

    graph.can_update(can_main,["all"],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)


def modif_level():
    """
    Récupère un niveau existant pour le modifier
    """
    global dict_state
    seek=True
    while seek:
        try :
            inp=ci.clean_input('Ouvrir le niveau : ')
            print('inp=',inp)
            dict_state=eval(open(f'Levels/{inp}.txt','r',encoding='utf8').read())
            seek=False
        except FileNotFoundError:
            print("Ce fichier n'existe pas")
    graph.can_update(can_main,["all"],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

def test_level():
    print(dict_state,file=open('Levels/temp.txt','w',encoding='utf8'))
    plat.platformer(level_n='temp')

def right_click_main(event):
    """
    Efface la case sur laquelle l'utilisat.eur.rice a cliqué
    """
    x_rc,y_rc=event.x//c_main,event.y//c_main
    if (x_rc,y_rc) in dict_state and dict_state[x_rc,y_rc]!=[None]:
        dict_state[x_rc,y_rc]=[None]
        graph.can_update(can_main,[(x_rc,y_rc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

def right_click_group(event):
    x_rc,y_rc=event.x//c_main,event.y//c_main
    clicked_tile=dict_state[x_rc,y_rc][0]

    list_2_flip=[]
    list_tile_0=[]

    #Dresse la liste des tuples à ajouter à chque coordonnées pour en obtenir
    #les voisines
    list_d=[(a,b) for a in range(-1,2) for b in range(-1,2) if (a+b)%2!=0]


    list_2_flip.append((x_rc,y_rc)) #Représente la liste des cases qu'il faudra retourner
    list_tile_0.append((x_rc,y_rc)) #Représente la liste des cases dont n=0 et dont les voisines ne sont pas encore dans list_2_flip
    while list_tile_0!=[]:
        nb_del=0 #Le nombre d'éléments de list_tile_0 supprimés

        for a in range(len(list_tile_0)):#Vérifie pour chaque élément de list_tile_0
            a_0=list_tile_0[a-nb_del]

            for d in list_d: #Dans chacune des directions
                x_y=(a_0[0]+d[0],a_0[1]+d[1])
                cond_1=not x_y in list_2_flip #Que sa voisine n'est pas déjà dans list_2_flip
                cond_2=x_y in dict_state

                if cond_1 and cond_2:
                    if dict_state[x_y][0]==clicked_tile:
                        if dict_state[x_y][0]==clicked_tile: #Si en plus sa voisine a n=0, l'ajoute à list_tile_0
                            list_tile_0.append(x_y)
                        list_2_flip.append(x_y)
            del list_tile_0[a-nb_del]#Puis supprime l'élément de list_tile_0
            nb_del+=1

    for tile in list_2_flip:
        dict_state[tile]=[None]

    graph.can_update(can_main,["all"],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)


def pick_tile(event):
    """
    Récupère la case sur laquelle on clique
    """
    global selected_tile
    selected_tile=dict_state[event.x//c_main,event.y//c_main][0]
    update_sel_tile_can()

def scroll(event):
    add=event.delta//abs(event.delta)
    list_ways=['up','right','down','left']
    if selected_tile in ('door','key','button'):
        channel=(int(entry_channel.get())+add)%20
        entry_channel.delete(0,len(entry_channel.get()))
        entry_channel.insert(0,channel)

    elif selected_tile in ('one-way-block','portal-in','portal-out','laser-beam','laser-emitter','laser-reciever'):
        way=entry_way.get()
        in_l,i=use.in_sub_list(way,list_ways)
        if in_l:
            i=i[0]
            if selected_tile in ('one-way-block','laser-beam','laser-emitter','laser-reciever'):
                s_way=list_ways[(i+add)%4]
            elif i%2==0:
                s_way=list_ways[(i+2*add+1)%4]
            else:
                s_way=list_ways[(i+2*add)%4]

        else:
            s_way='right'


        entry_way.delete(0,len(entry_way.get()))
        entry_way.insert(0,s_way)

    elif selected_tile in ('on-off-switch','on-off-block'):
        if entry_on_off.get()=='on':
            s_on_off='off'
        else:
            s_on_off='on'

        entry_on_off.delete(0,len(entry_on_off.get()))
        entry_on_off.insert(0,s_on_off)

    elif selected_tile in ('on-block','off-block','timed-block','on-off-door'):
        if entry_enable.get()=='True':
            output='False'
        else:
            output='True'
        entry_enable.delete(0,len(entry_enable.get()))
        entry_enable.insert(0,output)

    elif selected_tile == 'mirror':
        output=str((int(entry_mirror.get())+add)%4)
        entry_mirror.delete(0,len(entry_mirror.get()))
        entry_mirror.insert(0,output)




    update_sel_tile_can()

def shift_scroll(event):
    add=event.delta//abs(event.delta)
    if selected_tile in ('mirror','on-off-door'):
        channel=(int(entry_channel.get())+add)%20
        entry_channel.delete(0,len(entry_channel.get()))
        entry_channel.insert(0,channel)

    elif selected_tile == 'timed-block':
        output=str((int(entry_timed.get())+add)%60)
        entry_timed.delete(0,len(entry_timed.get()))
        entry_timed.insert(0,output)
    update_sel_tile_can()

def left_click_main(event):
    """
    Remplace la case sur laquelle l'utilisat.eur.rice a cliqué par la case
    sélectionnée
    """
    x_lc,y_lc=event.x//c_main,event.y//c_main
    if (x_lc,y_lc) in dict_state:

        #Si la case à poser est une porte ou une clef, récupère en plus son channel
        if selected_tile in ('door','key','button'):
            if dict_state[x_lc,y_lc]!=[selected_tile,int(entry_channel.get())%len(list_color_channel)]:
                dict_state[x_lc,y_lc]=[selected_tile,int(entry_channel.get())%len(list_color_channel)]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        #Si la case est un arrière plan, récupère en plus sa couleur
        elif selected_tile=='bg':
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_bg_color.get(),[]]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_bg_color.get(),[]]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile in ('glass','checkpoint'):
            if dict_state[x_lc,y_lc]!=[selected_tile,[]]:
                dict_state[x_lc,y_lc]=[selected_tile,[]]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile in ('laser-beam','laser-emitter'):
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_way.get()]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_way.get()]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile == 'laser-reciever':
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_way.get(),[],False]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_way.get(),[],False]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile=='one-way-block':
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_way.get(),[]]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_way.get(),[]]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile in ('portal-in','portal-out'):
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_way.get()]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_way.get()]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile == 'on-off-switch':
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_on_off.get()]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_on_off.get()]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile in ('on-block','off-block'):
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_enable.get()=='True',[]]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_enable.get()=='True',[]]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile=='timed-block':
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_enable.get()=='True',[],int(entry_timed.get())]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_enable.get()=='True',[],int(entry_timed.get())]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile=='on-off-door':
            if dict_state[x_lc,y_lc]!=[selected_tile,entry_enable.get()=='True',int(entry_channel.get()),[]]:
                dict_state[x_lc,y_lc]=[selected_tile,entry_enable.get()=='True',int(entry_channel.get()),[]]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

        elif selected_tile=='mirror':
            if dict_state[x_lc,y_lc]!=[selected_tile,int(entry_channel.get())%len(list_color_channel),int(entry_mirror.get())%4,[False]*4]:
                dict_state[x_lc,y_lc]=[selected_tile,int(entry_channel.get())%len(list_color_channel),int(entry_mirror.get())%4,[False]*4]
                graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)



        else:
            dict_state[x_lc,y_lc]=[selected_tile]
            graph.can_update(can_main,[(x_lc,y_lc)],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)

def left_click_group(event):
    x_lc,y_lc=event.x//c_main,event.y//c_main
    clicked_tile=dict_state[x_lc,y_lc]

    list_2_flip=[]
    list_tile_0=[]

    #Dresse la liste des tuples à ajouter à chque coordonnées pour en obtenir
    #les voisines
    list_d=[(a,b) for a in range(-1,2) for b in range(-1,2) if (a+b)%2!=0]


    list_2_flip.append((x_lc,y_lc)) #Représente la liste des cases qu'il faudra retourner
    list_tile_0.append((x_lc,y_lc)) #Représente la liste des cases dont n=0 et dont les voisines ne sont pas encore dans list_2_flip
    while list_tile_0!=[]:
        nb_del=0 #Le nombre d'éléments de list_tile_0 supprimés

        for a in range(len(list_tile_0)):#Vérifie pour chaque élément de list_tile_0
            a_0=list_tile_0[a-nb_del]

            for d in list_d: #Dans chacune des directions
                x_y=(a_0[0]+d[0],a_0[1]+d[1])
                cond_1=not x_y in list_2_flip #Que sa voisine n'est pas déjà dans list_2_flip
                cond_2=x_y in dict_state

                if cond_1 and cond_2:
                    if dict_state[x_y]==clicked_tile:
                        if dict_state[x_y]==clicked_tile: #Si en plus sa voisine a n=0, l'ajoute à list_tile_0
                            list_tile_0.append(x_y)
                        list_2_flip.append(x_y)
            del list_tile_0[a-nb_del]#Puis supprime l'élément de list_tile_0
            nb_del+=1

    for tile in list_2_flip: #Parcourt toutes les cases qu'il faut changer
        #Si la case à poser est une porte ou une clef, récupère en plus son channel
        if selected_tile in ('door','key','button'):
            if dict_state[tile]!=[selected_tile,int(entry_channel.get())%len(list_color_channel)]:
                dict_state[tile]=[selected_tile,int(entry_channel.get())%len(list_color_channel)]

        #Si la case est un arrière plan, récupère en plus sa couleur
        elif selected_tile=='bg':
            if dict_state[tile]!=[selected_tile,entry_bg_color.get(),[]]:
                dict_state[tile]=[selected_tile,entry_bg_color.get(),[]]
                
        elif selected_tile in ('glass','checkpoint'):
            if dict_state[tile]!=[selected_tile,[]]:
                dict_state[tile]=[selected_tile,[]]

        elif selected_tile in ('laser-beam','laser-emitter'):
            if dict_state[tile]!=[selected_tile,entry_way.get()]:
                dict_state[tile]=[selected_tile,entry_way.get()]

        elif selected_tile == 'laser-reciever':
            if dict_state[tile]!=[selected_tile,entry_way.get(),[],False]:
                dict_state[tile]=[selected_tile,entry_way.get(),[],False]

        elif selected_tile in ('portal-in','portal-out'):
            if dict_state[tile]!=[selected_tile,entry_way.get()]:
                dict_state[tile]=[selected_tile,entry_way.get()]

        elif selected_tile == 'on-off-switch':
            if dict_state[tile]!=[selected_tile,entry_on_off.get()]:
                dict_state[tile]=[selected_tile,entry_on_off.get()]

        elif selected_tile in ('on-block','off-block'):
            if dict_state[tile]!=[selected_tile,entry_enable.get()=='True',[]]:
                dict_state[tile]=[selected_tile,entry_enable.get()=='True',[]]

        elif selected_tile=='on-off-door':
            if dict_state[tile]!=[selected_tile,entry_enable.get()=='True',int(entry_channel.get()),[]]:
                dict_state[tile]=[selected_tile,entry_enable.get()=='True',int(entry_channel.get()),[]]

        elif selected_tile=='timed-block':
            if dict_state[tile]!=[selected_tile,entry_enable.get()=='True',[],int(entry_timed.get())]:
                dict_state[tile]=[selected_tile,entry_enable.get()=='True',[],int(entry_timed.get())]

        elif selected_tile=='one-way-block':
            if dict_state[tile]!=[selected_tile,entry_way.get(),False]:
                dict_state[tile]=[selected_tile,entry_way.get(),False]

        elif selected_tile=='mirror':
            if dict_state[tile]!=[selected_tile,int(entry_channel.get())%len(list_color_channel),int(entry_mirror.get())%4,[False]*4]:
                dict_state[tile]=[selected_tile,int(entry_channel.get())%len(list_color_channel),int(entry_mirror.get())%4,[False]*4]



        else:
            dict_state[tile]=[selected_tile]

    graph.can_update(can_main,['all'],dict_state,c_main,grid_enable=grid_enable,x_can=x_can,y_can=y_can)



def update_sel_tile_can():
    can_sel_tile.delete('all')
    graph.draw_tile(can_sel_tile,0,0,selected_tile,c_can_right,
                 channel=int(entry_channel.get()),
                 bg_color=entry_bg_color.get(),way=entry_way.get(),
                 switch_state=entry_on_off.get(),mirror_state=int(entry_mirror.get()),
                 block_enable=entry_enable.get()=='True')

list_color_channel=['#019036','#F5E506','#592823','#91331A','#B50804',
                    '#DA7C8A','#DE5920','#055B52','#2799D7','#395499',
                    '#613E90','#1D2528','#FFB000','#0069FF','#00DD1A',
                    '#E583FF','#00FFFF','#6200FF','#0000FF','#6D4000']

level_editor()


