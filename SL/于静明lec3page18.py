def cube_result(cube,epsilon = 1e-6):
    cube = abs(cube)
    low,high =(0,cube) if cube >=1 else (cube,1)
    while abs(high-low) > epsilon:
        guess = (low + high)/2
        if guess ** 3 < cube:
            low = guess
        else:
            high = guess
    return (low+high)/2

cube=float(input('the cube:'))
result = cube_result(cube)
if cube > 0:
    print(f'the cube root of {cube} is {result}')
else:
    print(f'the cube root of {cube} is {-result}')