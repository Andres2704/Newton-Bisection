import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def trapezio(f, a, b, I_, n):
    h = (b-a)/2.0
    if n == 1: I = (f(a)+f(b))*h
    else:
        k = 2**(n-2)
        h = (b-a)/k
        x = a + h/2
        sum_ = 0
        for i in range(k):
            sum_ = sum_ + f(x)
            x = x + h
        I = (I_ + h*sum_)/2
    return I
    
    
I_ = 0.0
I = []
ER = []
eps = 1.0e-6
a = -1.0
b = 1.0
for n in range(1,21):
    # lambda x: (funtion to analyse here)
    In = trapezio(lambda x: 1/(x+2), a, b, I_, n)
    I.append(In)
    ER.append(abs(In - I_)/In)
    if (n > 1) and (ER[n-1]) < eps: break
    I_ = In

print('Integral: ', In)
print('n =',n)

fig, ax = plt.subplots(1,2, figsize=(15,5))
ax[0].plot(ER, 'o')
ax[0].set_title('Relative error x n')
ax[1].plot(I, 'o')
ax[0].set_title('Integral x n')
plt.show()
