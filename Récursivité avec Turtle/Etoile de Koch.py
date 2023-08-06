import turtle as tur
from math import sqrt

n=4
l=3**n*(700//3**n)

def etoile_koch(l,n):
    global t
    tur.setup(1.25*l,1.25*l)
    t=tur.Turtle()
    t.hideturtle()
    t.speed('fastest')
    t.penup()
    t.goto(-l/2,l/(3.4641016151377544))
    t.pendown()
    for a in range (3):
        line(l,n)
        t.right(120)
    tur.done()

def line(l,n):
    global t
    if n==0:
        t.forward(l)
    else:
        for angle in [60,240,60]:
            line(l//3,n-1)
            t.left(angle)
        line(l//3,n-1)


etoile_koch(l,n)