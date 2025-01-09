x = float(input('the number you want to be opened:'))
def sqrt(x,tolerance=1e-6):
    g = x/2.0 #guess g
    while True:
        if abs(g*g-x)<tolerance:
            break
        g= (g+x/g)/2
        print
    return g

y = sqrt(x)
print(f'the number you want to be opened:{x}')
print(f'the square root is:{y}')