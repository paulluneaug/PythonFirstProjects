import tkinter as tk

def clean_input(text=''):
    """
    Ne marche pas
    """
    
    return input(text)
    global output
    fen_input=tk.Tk()
    fen_input.title('Python Input')
    
    output=''

    fra0=tk.Frame(fen_input,width=160+len(text)*9+30,height=20+40+20,bg='black')
    fra0.grid(column=0,row=0)
    fra0.grid_propagate(False)
    
    fra=tk.Frame(fra0,width=160+len(text)*9,height=20+40,bg='black')
    fra.grid(column=0,row=0,padx=15,pady=10)
    fra.grid_propagate(False)

    if text!='':        
        lab=tk.Label(fra,text=text,font='Verdana 12',fg='white',bg='black')
        lab.grid(column=0,row=0)
    
    entry=tk.Entry(fra,width=25)#, height=500)
    entry.grid(column=1,row=0,columnspan=2,pady=5)
    
    but_ok=tk.Button(fra,text='Ok',font='Verdana 12',command=lambda :destroy(fen_input,entry,True))
    but_ok.grid(column=1,row=1)
    
    but_cancel=tk.Button(fra,text='Annuler',font='Verdana 12',command=lambda :destroy(fen_input,entry,False))
    but_cancel.grid(column=2,row=1)
    
    fen_input.bind('<Return>',lambda x:destroy(fen_input,entry,True))
    
    fen_input.mainloop()
    print('o=',output)
    return output

def destroy(fen,entry,out):
    global output
    if out:
        output=entry.get()
        print(output)
    fen.destroy()
    return output


