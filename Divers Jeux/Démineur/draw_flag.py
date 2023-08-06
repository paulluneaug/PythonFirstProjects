from tkinter import *

def draw_flasg(x,y):
    global c
    can.create_polygon(x*c+0.5*c,y*c+0.1*c,x*c+0.55*c,y*c+0.1*c,x*c+0.55*c,y*c
        +0.6*c,x*c+0.5*c,y*c+0.6*c,x*c+0.1*c,y*c+0.35*c,fill='red',
        outline='black',width=1)
    can.create_polygon(x*c+0.55*c,y*c+0.1*c,x*c+0.6*c,y*c+0.1*c,x*c+0.6*c,
        y*c+0.8*c,x*c+0.8*c,y*c+0.8*c,x*c+0.85*c,y*c+0.88*c,x*c+0.2*c,y*c
        +0.88*c,x*c+0.25*c,y*c+0.8*c,x*c+0.5*c,y*c+0.8*c,x*c+0.5*c,y*c+0.6*c,
        x*c+0.55*c,y*c+0.6*c,fill='grey',outline='black',width=1)
    can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,outline='black',width=2)

def draw_boom(x,y):
    global c
    can.create_rectangle(x*c,y*c,(x+1)*c,(y+1)*c,fill='grey',
        outline='black',width=2)
    can.create_polygon(x*c+0.5*c,y*c+0.1*c,x*c+0.55*c,y*c+0.3*c,x*c+0.65*c,
        y*c+0.3*c,x*c+0.8*c,y*c+0.2*c,x*c+0.7*c,y*c+0.35*c,x*c+0.7*c,y*c+0.45*c,
        x*c+0.9*c,y*c+0.5*c,x*c+0.7*c,y*c+0.55*c,x*c+0.7*c,y*c+0.65*c,x*c+0.8*c,
        y*c+0.8*c,x*c+0.65*c,y*c+0.7*c,x*c+0.55*c,y*c+0.7*c,x*c+0.5*c,y*c+0.9*c,
        x*c+0.45*c,y*c+0.7*c,x*c+0.35*c,y*c+0.7*c,x*c+0.2*c,y*c+0.8*c,x*c+0.3*c,
        y*c+0.65*c,x*c+0.3*c,y*c+0.55*c,x*c+0.1*c,y*c+0.5*c,x*c+0.3*c,
        y*c+0.45*c,x*c+0.3*c,y*c+0.35*c,x*c+0.2*c,y*c+0.2*c,x*c+0.35*c,
        y*c+0.3*c,x*c+0.45*c,y*c+0.3*c,outline='red',fill='orange',width=3)


c=50
fen=Tk()
can=Canvas(fen,width=400,height=600)
can.pack()

draw_flag(0,0)
draw_flag(0,1)
draw_flag(1,0)
draw_flag(1,5)

fen.mainloop()