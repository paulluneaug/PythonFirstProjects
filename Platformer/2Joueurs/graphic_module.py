from math import pi,cos,sin,sqrt
import useful_module as use

"""
Module gérant la partie graphique du jeu
"""

def draw_tile(can,x,y,tile_type,c,channel=0,bg_color='#FFFF5A',way='down',
              tag=None,switch_state='on',block_enable=True,laser_in=[],
              mirror_state=0,heart_color='#FF62C7'):
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
                block, spike, bounce, sticky, speed-up, slow-down, door, 
                key, bg, breakable-block, checkpoint, portal-in, 
                portal-out, one-way-block, heart, on-off-switch, on-block, 
                off-block, timed-block, laser-emitter, laser-reciever, 
                mirror, glass, button, on-off-door

        c : type=int
            Longueur en pixels de la case sur laquelle dessiner

        channel : type=int
           Si la case à dessiner est une porte ou une clef, désigne la couleur
           de celle ci
    """
    list_color_channel=['#019036','#F5E506','#592823','#91331A','#B50804',
                        '#DA7C8A','#DE5920','#055B52','#2799D7','#395499',
                        '#613E90','#1D2528','#FFB000','#0069FF','#00DD1A',
                        '#E583FF','#00FFFF','#6200FF','#0000FF','#6D4000']


    if tile_type=='block':
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='grey',outline='black',width=0,tag=f'{x}/{y}')

    elif tile_type=='spike':
        pad=0.25
        # can.create_polygon((x+0.1)*c,(y+0.1)*c,(x+0.15)*c,(y)*c,(x+0.25)*c,(y+0.1)*c,fill='red',tag=f'{x}/{y}')
        can.create_rectangle((x)*c,(y)*c,(x+1)*c,(y+1)*c,fill='red',outline='black',width=0,tag=f'{x}/{y}')
        can.create_rectangle((x+pad)*c,(y+pad)*c,(x+1-pad)*c,(y+1-pad)*c,fill='orange',outline='black',width=0,tag=f'{x}/{y}')

    elif tile_type=='bg':
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill=bg_color,outline='black',width=0,tag=f'{x}/{y}')
        if laser_in!=[]:
            draw_tile(can,x,y,'laser-beam',c,way=laser_in)

    elif tile_type=='breakable-block':
        pad=0.15
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='#FFCC00',outline='#FFCC00',width=0,tag=f'{x}/{y}')
        can.create_rectangle((x+pad)*c,y*c,(x+1-pad)*c,(y+1)*c,fill='#800000',outline='#800000',width=0,tag=f'{x}/{y}')
        can.create_rectangle(x*c,(y+pad)*c,(x+1)*c,(y+1-pad)*c,fill='#800000',outline='#800000',width=0,tag=f'{x}/{y}')
        can.create_rectangle((x+pad)*c,(y+pad)*c,(x+1-pad)*c,(y+1-pad)*c,fill='#993300',outline='#993300',width=0,tag=f'{x}/{y}')

    elif tile_type=='bounce':
        can.create_rectangle(x*c,(y+0)*c,(x+1)*c,(y+1)*c,fill='#3366FF',tag=f'{x}/{y}',width=0)
        can.create_polygon((x+0.5)*c,(y+0.1)*c,(x+0.2)*c,(y+0.4)*c,(x+0.2)*c,(y+0.55)*c,(x+0.5)*c,(y+0.25)*c,(x+0.8)*c,(y+0.55)*c,(x+0.8)*c,(y+0.4)*c,fill='#0000FF',tag=f'{x}/{y}',width=0)
        can.create_polygon((x+0.5)*c,(y+0.45)*c,(x+0.2)*c,(y+0.75)*c,(x+0.2)*c,(y+0.9)*c,(x+0.5)*c,(y+0.6)*c,(x+0.8)*c,(y+0.9)*c,(x+0.8)*c,(y+0.75)*c,fill='#0000FF',tag=f'{x}/{y}',width=0)

    elif tile_type=='speed-up':
        can.create_rectangle(x*c,(y+0)*c,(x+1)*c,(y+1)*c,fill='#99CC00',tag=f'{x}/{y}',width=0)
        can.create_polygon((x+0.55)*c,(y+0.2)*c,(x+0.7)*c,(y+0.2)*c,(x+0.9)*c,(y+0.5)*c,(x+0.7)*c,(y+0.8)*c,(x+0.55)*c,(y+0.8)*c,(x+0.75)*c,(y+0.5)*c,fill='#008000',tag=f'{x}/{y}',width=0)
        can.create_polygon((x+0.45)*c,(y+0.2)*c,(x+0.3)*c,(y+0.2)*c,(x+0.1)*c,(y+0.5)*c,(x+0.3)*c,(y+0.8)*c,(x+0.45)*c,(y+0.8)*c,(x+0.25)*c,(y+0.5)*c,fill='#008000',tag=f'{x}/{y}',width=0)

    elif tile_type=='door':
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill=list_color_channel[channel],outline='black',width=0,tag=f'{x}/{y}')
        can.create_oval((0.35+x)*c,(0.2+y)*c,(0.65+x)*c,(0.5+y)*c,fill="black",outline="black",tag=f'{x}/{y}')
        can.create_polygon((0.5+x)*c,(0.3+y)*c,(0.3+x)*c,(0.8+y)*c,(0.7+x)*c,(0.8+y)*c,fill="black",outline="black",width=2,tag=f'{x}/{y}')

    elif tile_type=='key':
        can.create_polygon((0.75+x)*c,(0.475+y)*c,(0.1+x)*c,(0.475+y)*c,(0.1+x)*c,(0.525+y)*c,(0.2+x)*c,(0.525+y)*c,(0.2+x)*c,(0.6+y)*c,(0.25+x)*c,(0.6+y)*c,(0.25+x)*c,(0.525+y)*c,(0.35+x)*c,(0.525+y)*c,(0.35+x)*c,(0.625+y)*c,(0.4+x)*c,(0.625+y)*c,(0.4+x)*c,(0.525+y)*c,(0.75+x)*c,(0.525+y)*c,fill=list_color_channel[channel],outline=list_color_channel[channel],width=2,tag=f'{x}/{y}')
        can.create_oval((0.6+x)*c,(0.35+y)*c,(0.9+x)*c,(0.65+y)*c,fill=list_color_channel[channel],outline=list_color_channel[channel],tag=f'{x}/{y}')
        can.create_oval((0.65+x)*c,(0.4+y)*c,(0.85+x)*c,(0.60+y)*c,fill="white",outline="white",tag=f'{x}/{y}')

    elif tile_type=='glass':
        if laser_in==[]:
            laser_in=[False]*4
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='#CDCDCD',width=0,tag=f'{x}/{y}')

        if laser_in!=[]:
            draw_tile(can,x,y,'laser-beam',c,way=laser_in)

    elif tile_type=='portal-in':
        if way=='left':
            can.create_rectangle(x*c,y*c,(x+0.3)*c,(y+1)*c,fill='#007AFA',tag=f'{x}/{y}',width=0)
        else:
            can.create_rectangle((x+0.7)*c,y*c,(x+1)*c,(y+1)*c,fill='#007AFA',tag=f'{x}/{y}',width=0)

    elif tile_type=='portal-out':
        if way=='left':
            can.create_rectangle(x*c,y*c,(x+0.3)*c,(y+1)*c,fill='#F6810D',tag=f'{x}/{y}',width=0)
        else:
            can.create_rectangle((x+0.7)*c,y*c,(x+1)*c,(y+1)*c,fill='#F6810D',tag=f'{x}/{y}',width=0)

    elif tile_type=='checkpoint':
        can.create_polygon(x*c+0.5*c,y*c+0.1*c,x*c+0.55*c,y*c+0.1*c,x*c+0.55*c,y*c
            +0.6*c,x*c+0.5*c,y*c+0.6*c,x*c+0.1*c,y*c+0.35*c,fill='red',
            outline='black',width=1,tag=f'{x}/{y}')
        can.create_polygon(x*c+0.55*c,y*c+0.1*c,x*c+0.6*c,y*c+0.1*c,x*c+0.6*c,
            y*c+0.8*c,x*c+0.8*c,y*c+0.8*c,x*c+0.85*c,y*c+0.88*c,x*c+0.2*c,y*c
            +0.88*c,x*c+0.25*c,y*c+0.8*c,x*c+0.5*c,y*c+0.8*c,x*c+0.5*c,y*c+0.6*c,
            x*c+0.55*c,y*c+0.6*c,fill='grey',outline='black',width=1,tag=f'{x}/{y}')

        if laser_in!=[]:
            draw_tile(can,x,y,'laser-beam',c,way=laser_in)

    elif tile_type=='one-way-block':
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='#505050',width=0,tag=f'{x}/{y}')
        if way=='down':
            can.create_rectangle((x)*c,(y+0.8)*c,(x+1)*c,(y+1)*c,fill='#B1C8D0',width=0,tag=f'{x}/{y}')
            can.create_polygon((x+0.2)*c,(y+0.2)*c,(x+0.8)*c,(y+0.2)*c,(x+0.5)*c,(y+0.65)*c,fill='#B1C8D0',width=0,tag=f'{x}/{y}')
        elif way=='up':
            can.create_rectangle((x)*c,(y)*c,(x+1)*c,(y+0.2)*c,fill='#B1C8D0',width=0,tag=f'{x}/{y}')
            can.create_polygon((x+0.2)*c,(y+0.8)*c,(x+0.8)*c,(y+0.8)*c,(x+0.5)*c,(y+0.35)*c,fill='#B1C8D0',width=0,tag=f'{x}/{y}')
        elif way=='right':
            can.create_rectangle((x+0.8)*c,(y)*c,(x+1)*c,(y+1)*c,fill='#B1C8D0',width=0,tag=f'{x}/{y}')
            can.create_polygon((x+0.2)*c,(y+0.2)*c,(x+0.65)*c,(y+0.5)*c,(x+0.2)*c,(y+0.8)*c,fill='#B1C8D0',width=0,tag=f'{x}/{y}')
        elif way=='left':
            can.create_rectangle((x)*c,(y)*c,(x+0.2)*c,(y+1)*c,fill='#B1C8D0',width=0,tag=f'{x}/{y}')
            can.create_polygon((x+0.8)*c,(y+0.8)*c,(x+0.35)*c,(y+0.5)*c,(x+0.8)*c,(y+0.2)*c,fill='#B1C8D0',width=0,tag=f'{x}/{y}')

        if laser_in!=[]:
            draw_tile(can,x,y,'laser-beam',c,way=laser_in)

    elif tile_type=='heart':
        if tag==None:
            tag=f'{x}/{y}'
        can.create_oval((x+1/6)*c,(y+1/6)*c,(x+0.52)*c,(y+0.52)*c,fill=heart_color,width=0,tag=tag)
        can.create_oval((x+0.48)*c,(y+1/6)*c,(x+5/6)*c,(y+0.52)*c,fill=heart_color,width=0,tag=tag)
        can.create_polygon((x+0.343+0.207*cos(3*pi/4))*c,(y+0.343+0.207*sin(3*pi/4))*c,(x+0.5)*c,(y+0.343)*c,(x+0.657+0.207*cos(pi/4))*c,(y+0.343+0.207*sin(pi/4))*c,(x+0.5)*c,(y+0.85)*c,fill=heart_color,width=0,tag=tag)#,outline='black')

    elif tile_type=='slow-down':
        can.create_rectangle(x*c,(y+0)*c,(x+1)*c,(y+1)*c,fill='#E600E6',tag=f'{x}/{y}',width=0)
        can.create_polygon((x+0.1)*c,(y+0.2)*c,(x+0.25)*c,(y+0.2)*c,(x+0.45)*c,(y+0.5)*c,(x+0.25)*c,(y+0.8)*c,(x+0.1)*c,(y+0.8)*c,(x+0.3)*c,(y+0.5)*c,fill='#A600A6',tag=f'{x}/{y}',width=0)
        can.create_polygon((x+0.9)*c,(y+0.2)*c,(x+0.75)*c,(y+0.2)*c,(x+0.55)*c,(y+0.5)*c,(x+0.75)*c,(y+0.8)*c,(x+0.9)*c,(y+0.8)*c,(x+0.7)*c,(y+0.5)*c,fill='#A600A6',tag=f'{x}/{y}',width=0)

    elif tile_type=='sticky':
        can.create_rectangle(x*c,(y+0)*c,(x+1)*c,(y+1)*c,fill='orange',tag=f'{x}/{y}',width=0)
        can.create_polygon((x+0.5)*c,(y+0.4)*c,(x+0.2)*c,(y+0.1)*c,(x+0.2)*c,(y+0.25)*c,(x+0.5)*c,(y+0.55)*c,(x+0.8)*c,(y+0.25)*c,(x+0.8)*c,(y+0.1)*c,fill='#FF6600',tag=f'{x}/{y}',width=0)
        can.create_polygon((x+0.5)*c,(y+0.75)*c,(x+0.2)*c,(y+0.45)*c,(x+0.2)*c,(y+0.6)*c,(x+0.5)*c,(y+0.9)*c,(x+0.8)*c,(y+0.6)*c,(x+0.8)*c,(y+0.45)*c,fill='#FF6600',tag=f'{x}/{y}',width=0)

    elif tile_type=='laser-beam':
        if 'down' in way or 'up' in way:
            # can.create_rectangle((x)*c,(y)*c,(x+1)*c,(y+1)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            # can.create_rectangle((x)*c,(y)*c,(x+1)*c,(y+1)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.3)*c,(y)*c,(x+0.7)*c,(y+1)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.4)*c,(y)*c,(x+0.6)*c,(y+1)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')
        if 'left' in way or 'right' in way:
            can.create_rectangle((x)*c,(y+0.3)*c,(x+1)*c,(y+0.7)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x)*c,(y+0.4)*c,(x+1)*c,(y+0.6)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')

    elif tile_type=='laser-emitter':
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='grey',outline='black',width=0,tag=f'{x}/{y}')
        if way=='down':
            can.create_oval((x+0.2)*c,(y+0.1)*c,(x+0.8)*c,(y+0.7)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.3)*c,(y+0.4)*c,(x+0.7)*c,(y+1)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_oval((x+0.3)*c,(y+0.2)*c,(x+0.7)*c,(y+0.6)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.4)*c,(y+0.4)*c,(x+0.6)*c,(y+1)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')

        elif way=='up':
            can.create_oval((x+0.8)*c,(y+0.9)*c,(x+0.2)*c,(y+0.3)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.7)*c,(y+0.6)*c,(x+0.3)*c,(y)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_oval((x+0.7)*c,(y+0.8)*c,(x+0.3)*c,(y+0.4)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.6)*c,(y+0.6)*c,(x+0.4)*c,(y)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')

        elif way=='right':
            can.create_oval((x+0.1)*c,(y+0.2)*c,(x+0.7)*c,(y+0.8)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.4)*c,(y+0.3)*c,(x+1)*c,(y+0.7)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_oval((x+0.2)*c,(y+0.3)*c,(x+0.6)*c,(y+0.7)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.4)*c,(y+0.4)*c,(x+1)*c,(y+0.6)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')

        elif way=='left':
            can.create_oval((x+0.9)*c,(y+0.8)*c,(x+0.3)*c,(y+0.2)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.6)*c,(y+0.7)*c,(x)*c,(y+0.3)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
            can.create_oval((x+0.8)*c,(y+0.7)*c,(x+0.4)*c,(y+0.3)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.6)*c,(y+0.6)*c,(x)*c,(y+0.4)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')

    elif tile_type=='on-off-switch':
        if switch_state=='on':
            can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='#FF4715',outline='black',width=0,tag=f'{x}/{y}')
            can.create_oval((x+0.15)*c,(y+0.3)*c,(x+0.4)*c,(y+.7)*c,fill='#FF4715',outline='white',width=1,tag=f'{x}/{y}')
            can.create_line((x+0.85)*c,(y+0.3)*c,(x+0.85)*c,(y+0.7)*c,(x+0.6)*c,(y+0.3)*c,(x+0.6)*c,(y+.7)*c,fill='white',width=1,tag=f'{x}/{y}')

        elif switch_state=='off':
            can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='#6F6FFB',outline='black',width=0,tag=f'{x}/{y}')
            can.create_oval((x+0.1)*c,(y+0.3)*c,(x+0.35)*c,(y+.7)*c,fill='#6F6FFB',outline='white',width=1,tag=f'{x}/{y}')
            can.create_line((x+0.45)*c,(y+0.7)*c,(x+0.45)*c,(y+0.5)*c,(x+0.6)*c,(y+0.5)*c,(x+0.45)*c,(y+0.5)*c,(x+0.45)*c,(y+0.3)*c,(x+0.65)*c,(y+0.3)*c,fill='white',width=1,tag=f'{x}/{y}')
            can.create_line((x+0.7)*c,(y+0.7)*c,(x+0.7)*c,(y+0.5)*c,(x+0.85)*c,(y+0.5)*c,(x+0.7)*c,(y+0.5)*c,(x+0.7)*c,(y+0.3)*c,(x+0.9)*c,(y+0.3)*c,fill='white',width=1,tag=f'{x}/{y}')

    elif tile_type in ('on-block','off-block','timed-block','on-off-door'):
        dict_col={'on-block':'#FF4715','off-block':'#6F6FFB','timed-block':'#CC99FF','on-off-door':list_color_channel[channel]}
        block_color=dict_col[tile_type]
        if block_enable:
            can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill=block_color,outline='black',width=0,tag=f'{x}/{y}')
        else:
            width=0.15
            len_corn=0.35
            for d in [(a,b) for a in range(2) for b in range(2)]:
                can.create_polygon((x+d[0])*c,(y+d[1])*c,
                                   (x+abs(d[0]-len_corn))*c,
                                   (y+d[1])*c,(x+abs(d[0]-len_corn))*c,
                                   (y+abs(d[1]-width))*c,(x+abs(d[0]-width))*c,
                                   (y+abs(d[1]-width))*c,(x+abs(d[0]-width))*c,
                                   (y+abs(d[1]-len_corn))*c,(x+d[0])*c,
                                   (y+abs(d[1]-len_corn))*c,fill=block_color,
                                   width=0,tag=f'{x}/{y}')

            if not laser_in in (False,[]):
                draw_tile(can,x,y,'laser-beam',c,way=laser_in)


        if tile_type=='timed-block':
            r=0.3
            can.create_oval((x+0.5-r)*c,(y+0.5-r)*c,(x+0.5+r)*c,(y+0.5+r)*c,outline='black',width=1,tag=f'{x}/{y}')
            can.create_line((x+0.5)*c,(y+0.5-r+0.1)*c,(x+0.5)*c,(y+0.5)*c,(x+0.5+(0.7*r)*cos(-pi/4))*c,(y+0.5+(0.7*r*sin(pi/4)))*c,fill='black',width=1,tag=f'{x}/{y}')

    elif tile_type=='mirror':
        draw_tile(can,x,y,'glass',c)
        if laser_in==[]:
            laser_in=[False]*4
        mir_out_col='#DADADA'
        mir_in_col=list_color_channel[channel]
        pad_in,pad_out=2*((0.1)**2),2*((0.05)**2)
        l_laser=[(.3,0,.7,.4),(.6,.3,1,.7),(.3,.6,.7,1),(0,.3,.4,.7)]
        
        if laser_in [0] and laser_in [2] and mirror_state==0:
            can.create_rectangle((x+.3)*c,(y+.4)*c,(x+.7)*c,(y+.6)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
        if laser_in [1] and laser_in [3] and mirror_state==2:
            can.create_rectangle((x+.4)*c,(y+.3)*c,(x+.6)*c,(y+.7)*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
        
        for i in range(4):
            if laser_in[i]:
                if i%2==0:
                    x_add,y_add=0.1,0
                else:
                    x_add,y_add=0,0.1

                l_co=l_laser[i]
                can.create_rectangle((x+l_co[0])*c,(y+l_co[1])*c,(x+l_co[2])*c,(y+l_co[3])*c,fill='#FF9AFF',width=0,tag=f'{x}/{y}')
                can.create_rectangle((x+l_co[0]+x_add)*c,(y+l_co[1]+y_add)*c,(x+l_co[2]-x_add)*c,(y+l_co[3]-y_add)*c,fill='#A12DA1',width=0,tag=f'{x}/{y}')


        if mirror_state==0:
            can.create_rectangle((x+0.35)*c,y*c,(x+0.65)*c,(y+1)*c,fill=mir_out_col,width=0,tag=f'{x}/{y}')
            can.create_rectangle((x+0.4)*c,y*c,(x+0.6)*c,(y+1)*c,fill=mir_in_col,width=0,tag=f'{x}/{y}')

        elif mirror_state==1:
            can.create_polygon((x+1-(sqrt(pad_in)+sqrt(pad_out)))*c,(y)*c,(x+1)*c,y*c,
                               (x+1)*c,(y+sqrt(pad_in)+sqrt(pad_out))*c,
                               (x+sqrt(pad_in)+sqrt(pad_out))*c,(y+1)*c,x*c,(y+1)*c,x*c,
                               (y+1-(sqrt(pad_in)+sqrt(pad_out)))*c,fill=mir_out_col,
                               width=0,tag=f'{x}/{y}')

            can.create_polygon((x+1-sqrt(pad_in))*c,(y)*c,(x+1)*c,y*c,(x+1)*c,
                               (y+sqrt(pad_in))*c,(x+sqrt(pad_in))*c,(y+1)*c,x*c,(y+1)*c,
                               x*c,(y+1-sqrt(pad_in))*c,fill=mir_in_col,width=0,
                               tag=f'{x}/{y}')

        elif mirror_state==2:
            can.create_rectangle(x*c,(y+0.35)*c,(x+1)*c,(y+0.65)*c,fill=mir_out_col,width=0,tag=f'{x}/{y}')
            can.create_rectangle(x*c,(y+0.4)*c,(x+1)*c,(y+0.6)*c,fill=mir_in_col,width=0,tag=f'{x}/{y}')

        elif mirror_state==3:
            can.create_polygon((x+sqrt(pad_in)+sqrt(pad_out))*c,(y)*c,x*c,y*c,x*c,
                               (y+sqrt(pad_in)+sqrt(pad_out))*c,
                               (x+1-(sqrt(pad_in)+sqrt(pad_out)))*c,(y+1)*c,(x+1)*c,
                               (y+1)*c,(x+1)*c,(y+1-(sqrt(pad_in)+sqrt(pad_out)))*c,
                               fill=mir_out_col,width=0,tag=f'{x}/{y}')

            can.create_polygon((x+sqrt(pad_in))*c,(y)*c,x*c,y*c,x*c,(y+sqrt(pad_in))*c,
                               (x+1-sqrt(pad_in))*c,(y+1)*c,(x+1)*c,(y+1)*c,(x+1)*c,
                               (y+1-sqrt(pad_in))*c,fill=mir_in_col,width=0,
                               tag=f'{x}/{y}')

    elif tile_type=='button':
        can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='grey',outline='black',width=0,tag=f'{x}/{y}')
        can.create_rectangle((x+0.2)*c,(y+0.3)*c,(x+0.8)*c,(y+0.7)*c,fill=list_color_channel[channel],outline='black',width=0,tag=f'{x}/{y}')

    elif tile_type=='laser-reciever':
        if laser_in==[]:
            laser_in=[]
        draw_tile(can, x, y, 'block', c)

        if laser_in==[]:
            output_col='red'
            can.create_rectangle((x+0.2)*c,(y+0.2)*c,(x+0.8)*c,(y+0.8)*c,
                                 fill='#CDCDCD',outline='#CDCDCD',width=0,
                                 tag=f'{x}/{y}')
        else:
            output_col='green'
            can.create_rectangle((x+0.2)*c,(y+0.2)*c,(x+0.8)*c,(y+0.8)*c,
                                 fill='#FF9AFF',outline='#FF9AFF',width=0,
                                 tag=f'{x}/{y}')
            can.create_rectangle((x+0.3)*c,(y+0.3)*c,(x+0.7)*c,(y+0.7)*c,
                                 fill='#A12DA1',outline='#A12DA1',width=0,
                                 tag=f'{x}/{y}')

        if way=='up':
            can.create_polygon((x+0.37)*c,(y+0.25)*c,(x+0.63)*c,(y+0.25)*c,
                               (x+0.5)*c,(y+0.05)*c,fill=output_col,
                               outline=output_col,width=0,tag=f'{x}/{y}')

        if way=='right':
            can.create_polygon((x+0.75)*c,(y+0.37)*c,(x+0.75)*c,(y+0.63)*c,
                               (x+0.95)*c,(y+0.5)*c,fill=output_col,
                               outline=output_col,width=0,tag=f'{x}/{y}')

        if way=='down':
            can.create_polygon((x+0.37)*c,(y+0.75)*c,(x+0.63)*c,(y+0.75)*c,
                               (x+0.5)*c,(y+0.95)*c,fill=output_col,
                               outline=output_col,width=0,tag=f'{x}/{y}')

        if way=='left':
            can.create_polygon((x+0.25)*c,(y+0.37)*c,(x+0.25)*c,(y+0.63)*c,
                               (x+0.05)*c,(y+0.5)*c,fill=output_col,
                               outline=output_col,width=0,tag=f'{x}/{y}')

        if 'up' in laser_in:
            can.create_rectangle((x+0.3)*c,(y+0)*c,(x+0.7)*c,(y+0.2)*c,
                                 fill='#FF9AFF',outline='#FF9AFF',width=0,
                                 tag=f'{x}/{y}')
            can.create_rectangle((x+0.4)*c,(y+0)*c,(x+0.6)*c,(y+0.3)*c,
                                 fill='#A12DA1',outline='#A12DA1',width=0,
                                 tag=f'{x}/{y}')
        elif way!='up':
            can.create_rectangle((x+0.3)*c,(y+0)*c,(x+0.7)*c,(y+0.2)*c,
                                 fill='#CDCDCD',outline='#CDCDCD',width=0,
                                 tag=f'{x}/{y}')

        if 'right' in laser_in:
            can.create_rectangle((x+0.8)*c,(y+0.3)*c,(x+1)*c,(y+0.7)*c,
                                 fill='#FF9AFF',outline='#FF9AFF',width=0,
                                 tag=f'{x}/{y}')
            can.create_rectangle((x+0.7)*c,(y+0.4)*c,(x+1)*c,(y+0.6)*c,
                                 fill='#A12DA1',outline='#A12DA1',width=0,
                                 tag=f'{x}/{y}')
        elif way!='right':
            can.create_rectangle((x+0.8)*c,(y+0.3)*c,(x+1)*c,(y+0.7)*c,
                                 fill='#CDCDCD',outline='#CDCDCD',width=0,
                                 tag=f'{x}/{y}')

        if 'down' in laser_in:
            can.create_rectangle((x+0.3)*c,(y+1)*c,(x+0.7)*c,(y+0.8)*c,
                                 fill='#FF9AFF',outline='#FF9AFF',width=0,
                                 tag=f'{x}/{y}')
            can.create_rectangle((x+0.4)*c,(y+1)*c,(x+0.6)*c,(y+0.7)*c,
                                 fill='#A12DA1',outline='#A12DA1',width=0,
                                 tag=f'{x}/{y}')
        elif way!='down':
            can.create_rectangle((x+0.3)*c,(y+1)*c,(x+0.7)*c,(y+0.8)*c,
                                 fill='#CDCDCD',outline='#CDCDCD',width=0,
                                 tag=f'{x}/{y}')

        if 'left' in laser_in:
            can.create_rectangle((x+0.2)*c,(y+0.3)*c,(x+0)*c,(y+0.7)*c,
                                 fill='#FF9AFF',outline='#FF9AFF',width=0,
                                 tag=f'{x}/{y}')
            can.create_rectangle((x+0.3)*c,(y+0.4)*c,(x+0)*c,(y+0.6)*c,
                                 fill='#A12DA1',outline='#A12DA1',width=0,
                                 tag=f'{x}/{y}')
        elif way!='left':
            can.create_rectangle((x+0.2)*c,(y+0.3)*c,(x+0)*c,(y+0.7)*c,
                                 fill='#CDCDCD',outline='#CDCDCD',width=0,
                                 tag=f'{x}/{y}')


def can_update(can,list_to_update,dico,c,grid_enable=False,x_can=0,y_can=0,list_players=None,level_name=None):
    """
    Met à jour une ou toutes les cases de la grille

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        element : type=tuple or str
            Indique quelles cases doivent être mises à jour parmi:
            -'all' pour tout mettre à jour
            -(x,y) pour mettre à jour la case en x,y
            -'player' pour mettre à jour le personnage
            -'hearts' pour mettre à jour la barre de vie du personnage

    """
    player_color=['#004BFF','red']
    for element in list_to_update:
        if element=="all": #Met à jour toutes les cases
            can.delete('all')
            if grid_enable:
                use.grid(can,x_can*c,y_can*c,c)
            for tile in dico.keys():
                if dico[tile]!=[None]:
                    if len(dico[tile])==1:
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c)
                    elif dico[tile][0]=='bg':
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,bg_color=dico[tile][1],laser_in=dico[tile][2])
                    elif dico[tile][0] in ('glass','checkpoint'):
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,laser_in=dico[tile][1])
                    elif dico[tile][0] in ('door','key','button'):
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,channel=dico[tile][1])
                    elif dico[tile][0] in ('laser-beam','laser-emitter'):
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,way=dico[tile][1])
                    elif dico[tile][0] == 'laser-reciever':
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,way=dico[tile][1],laser_in=dico[tile][2])
                    elif dico[tile][0]=='one-way-block':
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,way=dico[tile][1],laser_in=dico[tile][2])
                    elif dico[tile][0] in ('portal-in','portal-out'):
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,way=dico[tile][1])
                    elif dico[tile][0] == 'on-off-switch':
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,switch_state=dico[tile][1])
                    elif dico[tile][0] in ('on-block','off-block','timed-block'):
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,block_enable=dico[tile][1],laser_in=dico[tile][2])
                    elif dico[tile][0] == 'on-off-door':
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,block_enable=dico[tile][1],channel=dico[tile][2],laser_in=dico[tile][3])
                    elif dico[tile][0] == 'mirror':
                        draw_tile(can,tile[0],tile[1],dico[tile][0],c,channel=dico[tile][1],mirror_state=dico[tile][2],laser_in=dico[tile][3])




        elif type(element)==tuple: #Met à jour seulement la case en elementordonnées 'element'
            can.delete(f'{element[0]}/{element[1]}')
            if dico[element]!=[None]:
                if dico[element]!=[None]:
                    if len(dico[element])==1:
                        draw_tile(can,element[0],element[1],dico[element][0],c)
                    elif dico[element][0]=='bg':
                        draw_tile(can,element[0],element[1],dico[element][0],c,bg_color=dico[element][1],laser_in=dico[element][2])
                    elif dico[element][0] in ('glass','checkpoint'):
                        draw_tile(can,element[0],element[1],dico[element][0],c,laser_in=dico[element][1])
                    elif dico[element][0] in ('door','key','button'):
                        draw_tile(can,element[0],element[1],dico[element][0],c,channel=dico[element][1])
                    elif dico[element][0] in ('laser-beam','laser-emitter'):
                        draw_tile(can,element[0],element[1],dico[element][0],c,way=dico[element][1])
                    elif dico[element][0] == 'laser-reciever':
                        draw_tile(can,element[0],element[1],dico[element][0],c,way=dico[element][1],laser_in=dico[element][2])
                    elif dico[element][0]=='one-way-block':
                        draw_tile(can,element[0],element[1],dico[element][0],c,way=dico[element][1],laser_in=dico[element][2])
                    elif dico[element][0] in ('portal-in','portal-out'):
                        draw_tile(can,element[0],element[1],dico[element][0],c,way=dico[element][1])
                    elif dico[element][0] == 'on-off-switch':
                        draw_tile(can,element[0],element[1],dico[element][0],c,switch_state=dico[element][1])
                    elif dico[element][0] in ('on-block','off-block','timed-block'):
                        draw_tile(can,element[0],element[1],dico[element][0],c,block_enable=dico[element][1],laser_in=dico[element][2])
                    elif dico[element][0] == 'on-off-door':
                        draw_tile(can,element[0],element[1],dico[element][0],c,block_enable=dico[element][1],channel=dico[element][2],laser_in=dico[element][3])
                    elif dico[element][0] == 'mirror':
                        draw_tile(can,element[0],element[1],dico[element][0],c,channel=dico[element][1],mirror_state=dico[element][2],laser_in=dico[element][3])

        elif element=='player':
            for i_player in range(len(list_players)):
                player=list_players[i_player]
                can.delete(f'player{i_player}')
                p_pos=player.get_position()
                for x in range(player.get_width()):
                    for y in range(player.get_height()):
                        can.create_rectangle((p_pos[0]+x)*c,(p_pos[1]-y)*c,(p_pos[0]+x+1)*c,(p_pos[1]-y-1)*c,fill=player_color[i_player],tag=f'player{i_player}')


        elif element=='hearts':
            can.delete('hearts')
            for i_player in range(len(list_players)):
                player=list_players[i_player]
                for h in range(player._life):
                    draw_tile(can,h,i_player,'heart',c*1.5,tag='hearts',heart_color=player_color[i_player])

        elif element=='name':
            can.delete('name')
            level_name=level_name[0].upper()+level_name[1:]
            can.create_text((x_can/2)*c,c,text=level_name,fill='black',font='System 20')

