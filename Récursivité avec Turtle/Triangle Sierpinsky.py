import turtle as tur

n=8
l=2**n*(1024//2**n)

def triangle_Sierpinski(l,n):
    """
    Dessine un triangle de Sierpinski de complexité n et de longueur l
    """
    global t
    t=tur.Turtle()
    tur.setup(1.25*l,1.25*l)
    t.hideturtle()
    t.speed('fastest')
    t.penup()
    t.goto(-l/2,-l/(3.4641016151377544))
    t.pendown()

    sous_triangle(l,n)
    tur.done()

def sous_triangle(l,n):
    global t
    if n==0:
        t.begin_fill()
        for i in range(3):
            t.fd(l)
            t.left(120)
        t.end_fill()
    else:
        sous_triangle(l//2,n-1)
        t.penup()
        t.fd(l/2)
        t.pendown()
        sous_triangle(l//2,n-1)
        t.penup()
        t.left(120)
        t.forward(l/2)
        t.right(120)
        t.pendown()
        sous_triangle(l//2,n-1)
        t.penup()
        t.right(120)
        t.fd(l/2)
        t.left(120)
        t.pendown()


triangle_Sierpinski(l,n)


