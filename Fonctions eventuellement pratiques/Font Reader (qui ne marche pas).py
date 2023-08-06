import tkinter as tk

def next_font():
    global lab,i
    fonti=list_font[i].split(' ')
    if len(fonti)==2:
        lab.configure(text=fonti[0],font=(fonti[0],fonti[1])+' 40',weight=fonti[1])
        lab.grid(column=0,row=0)
    lab.configure(text=fonti[0],font=list_font[i]+' 40')
    lab.grid(column=0,row=0)
    i+=1

file_font=open('Font.txt','r')

list_font=file_font.read().split('\n')


i=0

fen=tk.Tk()
fra=tk.Frame(fen,width=500,height=100,bg='black')
fra.pack()

lab=tk.Label(fra)
lab.grid(column=0,row=0)

but=tk.Button(fra,text='Next Font',command=next_font)
but.grid(column=0,row=1)

next_font()

fen.mainloop()





