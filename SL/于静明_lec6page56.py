def fib_efficient(n,fib_list):
    if n < len(fib_list):
        return fib_list[n]
    else:
        next = fib_efficient(n-1,fib_list) + fib_efficient(n-2,fib_list)
        fib_list.append(next)
        return next

n=int(input('please input the length of the list:'))
fib_list = [1,1]
fib_efficient(n-1,fib_list)
print(fib_list)
