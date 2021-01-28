import numpy as np

def trapezoid4(f, a, b, eps):
    n = 1
    er = 1
    integral = []
    ER = []

    x = [a, b]
    y = list(map(f, x))        
    I = ((b-a)/2)*(y[0] + 2*sum(y[1:-1]) + y[-1])
    
    integral.append(I)
    k = 1
    while eps < er:
        n = 2**k
        h = (b-a)/n
        x = list(np.linspace(a,b,n, endpoint=False))
        x = x + [b]
        y = list(map(f, x))
        
        I = (h/2)*(y[0] + 2*sum(y[1:-1]) + y[-1])
        
        integral.append(I)
        er = abs((integral[k] - integral[k-1])/integral[k-1])
        print(er)
        ER.append(er)
        k = k+1
        
        
    return I, integral,  ER, k
    
def f(x):
    return 1/(x+2)

I, integral, ER, n = trapezoid4(f,-1,1,1.0E-6)
