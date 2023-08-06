def f(a,b):
    space=len(str(max(a,b)))
    space_bars=(2+space)*'─'
    print(f'┌{space_bars}┬{space_bars}┬{space_bars}┐')
    d=b-a
    print(f'│ {(space-len(str(a)))*" "}{a} │ {(space-len(str(b)))*" "}{b} │ {(space-len(str(d)))*" "}{d} │')
    while d>0:
        b,a=a,d
        if b>a:
            d=b-a
        else:
            d=a-b
            
        print(f'│ {(space-len(str(a)))*" "}{a} │ {(space-len(str(b)))*" "}{b} │ {(space-len(str(d)))*" "}{d} │')
    print(f'└{space_bars}┴{space_bars}┴{space_bars}┘')
    return a
        

print(f(12,14))

│