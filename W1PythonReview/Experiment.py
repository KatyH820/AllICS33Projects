def f():
    prev = None
    
    def g1(x):
        nonlocal prev
        temp = prev
        prev = x+5
        return temp
    def g2(x):
        nonlocal prev
        temp = prev
        prev = 5*x
        return temp
    return g1,g2

f1,f2 = f()
f3,f4 = f()
print(f1(1))
print(f2(2))   
print(f3(5))
print(f4(6))