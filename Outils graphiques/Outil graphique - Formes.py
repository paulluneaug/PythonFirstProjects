import tkinter as tk

def shape_maker():
    global c,can,fen,entry_outline,entry_fill,entry_width,can_test,can_layer,scroll_y,fra_left
    c=700
    lab_font='Verdana 12'

    fen=tk.Tk()
    fen.title('Shape Maker')

    can_test=tk.Canvas(fen,width=1,height=1)
    can_test.grid(column=0,row=1)

    fra_left=tk.Frame(fen,width=c/2+20,height=c,bg='black')
    fra_left.grid_propagate(False)
    fra_left.grid(column=0,row=0)

    can_layer=tk.Canvas(fra_left,width=c/2,height=c,bg='black')
    can_layer.grid_propagate(False)
    can_layer.pack(side=tk.LEFT)

    scroll_y=tk.Scrollbar(fra_left, orient="vertical", command=can_layer.yview)
    scroll_y.pack( side = tk.RIGHT, fill = 'y' )

    can_layer.configure(yscrollcommand=scroll_y.set)

    can=tk.Canvas(fen,width=c,height=c,bg='black')
    can.grid(column=1,row=0)

    fra_right=tk.Frame(fen,width=c/2+50,height=c,bg='black')
    fra_right.grid_propagate(False)
    fra_right.grid(column=2,row=0)

    but_draw_polygon=tk.Button(fra_right,text='Polygone',font='Verdana 15',
        command=draw_polygon)
    but_draw_polygon.grid(column=0,row=0,padx=5,pady=5)

    but_draw_rectangle=tk.Button(fra_right,text='Rectangle',font='Verdana 15',
        command=draw_rectangle)
    but_draw_rectangle.grid(column=1,row=0,padx=5,pady=5)

    but_draw_oval=tk.Button(fra_right,text='Ovale',font='Verdana 15',
        command=draw_oval)
    but_draw_oval.grid(column=0,row=1,padx=5,pady=5)

    but_draw_line=tk.Button(fra_right,text='Ligne',font='Verdana 15',
        command=draw_line)
    but_draw_line.grid(column=1,row=1,padx=5,pady=5)

    fra_outline=tk.Frame(fra_right,width=c/2,height=100,bg='black')
    fra_outline.grid(column=0,row=2,columnspan=2,padx=5,pady=5)

    lab_outline=tk.Label(fra_outline,text='Outline :',font=lab_font,bg='black',
        fg='white')
    lab_outline.grid(column=0,row=0,padx=5,pady=5)

    entry_outline=tk.Entry(fra_outline)
    entry_outline.grid(column=1,row=0,padx=5,pady=5)

    but_custom_ouline=tk.Button(fra_outline,command=lambda entry=entry_outline,
        eff=None:set_custom_color(entry),
        text='Choisir une couleur personalisée')
    but_custom_ouline.grid(columnspan=2,row=1,padx=5,pady=5)


    fra_fill=tk.Frame(fra_right,width=c/2,height=100,bg='black')
    fra_fill.grid(column=0,row=3,columnspan=2,padx=5,pady=5)

    lab_fill=tk.Label(fra_fill,text='Fill :',font=lab_font,bg='black',
        fg='white')
    lab_fill.grid(column=0,row=0,padx=5,pady=5)

    entry_fill=tk.Entry(fra_fill)
    entry_fill.grid(column=1,row=0,padx=5,pady=5)

    but_custom_fill=tk.Button(fra_fill,text='Choisir une couleur personalisée',
        command=lambda entry=entry_fill,eff=None:set_custom_color(entry))
    but_custom_fill.grid(columnspan=3,row=1,padx=5,pady=5)

    fra_width=tk.Frame(fra_right,width=c/2,height=100,bg='black')
    fra_width.grid(column=0,row=4,columnspan=2,padx=5,pady=5)

    lab_width=tk.Label(fra_width,text='Border Width :',font=lab_font,bg='black',
        fg='white')
    lab_width.grid(column=0,row=0,padx=5,pady=5)

    entry_width=tk.Entry(fra_width)
    entry_width.grid(column=1,row=0,padx=5,pady=5)

    but_erease=tk.Button(fra_right,text='Effacer',font='Verdana 15',
        command=erease)
    but_erease.grid(column=0,row=5,padx=5,pady=5)

    but_done=tk.Button(fra_right,text='Terminé',font='Verdana 15',
        command=done)
    but_done.grid(column=1,row=5,padx=5,pady=5)

    init()

    fen.mainloop()

def init():
    global list_shapes,list_default,fen
    list_shapes=[]
    list_default=['white','white',2]
    fen.bind('<z>',undo)
##    can_maj(True)



def left_click(event):
    global c,current_shape,last_co_is_temp,current_shape_type
    x_lc=event.x/c
    y_lc=event.y/c
    last_co_is_temp=False
    if current_shape[0] in ['oval','rectangle','line'] and current_shape_type!='polygon' and len(current_shape[1])==2:
        end_shape(0)
        can.unbind('<Motion>')
    elif len(current_shape[1])>0:
        current_shape[1][-1]=(x_lc,y_lc)
        can.bind('<Motion>', motion)
    else:
        current_shape[1].append((x_lc,y_lc))
        can.bind('<Motion>', motion)




def update_color_can(entry):
    global can_color,slider_b,slider_g,slider_r
    can_bg='#'+dec2hexa(slider_r.get())+dec2hexa(slider_g.get())+dec2hexa(slider_b.get())
    can_color.configure(bg=can_bg)
    can_color.after(50,lambda entry=entry,eff=None:update_color_can(entry))
    entry.delete(0,len(entry.get()))
    entry.insert(0,can_bg)


def dec2hexa(dec):
    dec=int(dec)
    n=0
    hexa=''
    listhexa='0123456789ABCDEF'
    while dec>=16**n:
        n+=1
    n-=1
    while n>=0:
        p=0
        for i in range(len(listhexa)):
            if dec>=i*16**n:
                p=i
        dec-=p*16**n
        hexa+=listhexa[p]
        n-=1
    while len(hexa)<2:
        hexa='0'+hexa
    return hexa

def end_shape(event):
    global current_shape_type,current_shape,last_co_is_temp
    if current_shape[1]!=[]:
        if last_co_is_temp:
            current_shape[1].pop()
        if current_shape_type=='polygon':
            current_shape[0]='polygon'
            next_shape_type='line'
        else:
            next_shape_type=current_shape[0]
        list_shapes.append(current_shape)

        current_shape=[next_shape_type,[],list_default[0],list_default[1],
            list_default[2]]
        can_maj(True)

        can.unbind('<Motion>')

def undo(event):
    global current_shape
    current_shape[1].pop()
    can_maj(True)


def done():
    global c,can,list_shapes
    for shape in list_shapes:
        coord=''
        for co in shape[1]:
            coord+=f'({round(co[0],4)}+x)*c,({round(co[1],4)}+y)*c,'
        if shape[0]=='line':
            outline=''
        else:
            outline=',outline="'+shape[2]+'"'
        print('can.create_'+shape[0]+'('+coord+'fill="'+shape[3]+'"'+
            outline+',width='+str(shape[4])+')')

def erease():
    global list_shapes
    list_shapes=[]
    can_maj(True)

def draw_polygon():
    global list_shapes,current_shape_type,list_default,current_shape,can
    current_shape=['line',[],list_default[0],list_default[1],list_default[2]]
    current_shape_type='polygon'
    can.bind('<Button-1>',left_click)
    can.bind('<Button-3>',end_shape)

def draw_oval():
    global list_shapes,current_shape_type,list_default,current_shape,can
    current_shape=['oval',[],list_default[0],list_default[1],list_default[2]]
    current_shape_type='oval'
    can.bind('<Button-1>',left_click)

def draw_rectangle():
    global list_shapes,current_shape_type,list_default,current_shape,can
    current_shape=['rectangle',[],list_default[0],list_default[1],list_default[2]]
    current_shape_type='rectangle'
    can.bind('<Button-1>',left_click)

def draw_line():
    global list_shapes,current_shape_type,list_default,current_shape,can
    current_shape=['line',[],list_default[0],list_default[1],list_default[2]]
    current_shape_type='line'
    can.bind('<Button-1>',left_click)


def motion(event):
    global c,current_shape,last_co_is_temp
    x_m=event.x/c
    y_m=event.y/c
    if last_co_is_temp and len(current_shape[1])>0:
        current_shape[1][-1]=(x_m,y_m)
    else:
        current_shape[1].append((x_m,y_m))
        last_co_is_temp=True
    can_maj(False)

def update_default_list():
    global entry_outline,entry_fill,entry_width,can_test
    for i in range(2):
        try:
            can_test.configure(bg=[entry_outline.get(),entry_fill.get()][i])
            list_default[i]=[entry_outline.get(),entry_fill.get()][i]
        except:
            a=0
    try:
        list_default[2]=float(entry_width.get())
    except:
        a=0

def can_maj(update_can_layer):
    global c,can,current_shape,can_layer,fen,scroll_y,fra_left
    can.delete(tk.ALL)
    update_default_list()
    for j in range(3):
        current_shape[2+j]=list_default[j]
    for shape in list_shapes+[current_shape]:
        coord=''
        if len(shape[1])>=2:
            for co in shape[1]:
                coord+=str(co[0])+'*c,'+str(co[1])+'*c,'
            if shape[0]=='line':
                outline=''
            else:
                outline=',outline="'+shape[2]+'"'
            eval('can.create_'+shape[0]+'('+coord+'fill="'+shape[3]+'"'+
                outline+',width='+str(shape[4])+')')


    if update_can_layer:
        print(list_shapes)
        can_layer.destroy()

        fra_left.pack_propagate(False)
        can_layer=tk.Canvas(fra_left,width=c/2,height=c,bg='black')
        can_layer.pack_propagate(False)
        can_layer.pack()
##
##        scroll_y=tk.Scrollbar(fra_left, orient="vertical", command=can_layer.yview)
##        scroll_y.pack( side = tk.RIGHT, fill = tk.Y )

        can_layer.configure(yscrollcommand=scroll_y.set)
        scroll_y.config(command=can_layer.yview)

        len_list_shapes=len(list_shapes)

        for s in range(len_list_shapes):

            k=len_list_shapes-s-1

            fra_temp=tk.Frame(can_layer,height=80,width=c/2-40,bg='black')
            #fra_temp.grid_propagate(False)
            fra_temp.grid(column=0,row=s,padx=7,pady=5)

            if s!=0:
                but_raise=tk.Button(fra_temp,text='Lever le calque',command=lambda a=k,eff=None:raise_layer(a))
                but_raise.grid(column=0,row=0)

            but_del=tk.Button(fra_temp,text='Supprimer le calque',command=lambda b=k,eff=None:del_layer(b))
            but_del.grid(column=0,row=1)

            if s!=len_list_shapes-1:
                but_lower=tk.Button(fra_temp,text='Baisser le calque',command=lambda c=k,eff=None:lower_layer(c))
                but_lower.grid(column=0,row=2)

            can_temp=tk.Canvas(fra_temp,width=70,height=70,bg='black')
            can_temp.grid(column=1,row=0,rowspan=3)

            coord=''

            if len(list_shapes[k][1])>=2:
                for co in list_shapes[k][1]:
                    coord+=f'{co[0]}*70,{co[1]}*70,'
                if list_shapes[k][0]=='line':
                    outline=''
                else:
                    outline=',outline="'+list_shapes[k][2]+'"'
                eval('can_temp.create_'+list_shapes[k][0]+'('+coord+'fill="'+list_shapes[k][3]+'"'+
                    outline+',width='+str(list_shapes[k][4]/10)+')')


def del_layer(layer):
    print(layer)
    list_shapes.pop(layer)
    can_maj(True)

def raise_layer(layer):
    print(list_shapes)
    list_shapes[layer+1],list_shapes[layer]=list_shapes[layer],list_shapes[layer+1]
    can_maj(True)

def lower_layer(layer):
    list_shapes[layer-1],list_shapes[layer]=list_shapes[layer],list_shapes[layer-1]
    can_maj(True)




def set_custom_color(entry):
    global can_color,slider_b,slider_g,slider_r,can_c_color,i_can_c_color,c_c_color
    fen_color=tk.Tk()
    fen_color.title('Couleur personalisée')

    can_color=tk.Canvas(fen_color,height=300,width=300,bg='black')
    can_color.grid(column=0,row=0)


    fra_sliders=tk.Frame(fen_color,bg='black')
    fra_sliders.grid(column=0,row=1)

    slider_r=tk.Scale(fra_sliders,from_=255,to=0,bg='black',
        activebackground='black',fg='red',font='verdana 11',label='Red')
    slider_r.grid(column=0,row=0)

    slider_g=tk.Scale(fra_sliders,from_=255,to=0,bg='black',
        activebackground='black',fg='green',font='verdana 11',label='Green')
    slider_g.grid(column=1,row=0)

    slider_b=tk.Scale(fra_sliders,from_=255,to=0,bg='black',
        activebackground='black',fg='#019BD5',font='verdana 11',label='Blue')
    slider_b.grid(column=2,row=0)

    update_color_can(entry)

    fen_color.mainloop()


shape_maker()