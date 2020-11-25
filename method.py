import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from random import *

class rootError(Exception):
    pass

class roots():
    def __init__(self, f, df, e):
        self.f = f
        self.df = df
        self.e = e
    
    def newton(self, x0, **file_name):
        fx0 = self.f(x0)
        if abs(fx0) < self.e: return x0
        k = 0
        E = 1
        
        if file_name.get('filename') == None:
            filename = 'Newton_results'
        else:
            filename = file_name.get('filename')

        results = pd.DataFrame(columns='x0 f(x)/f`(x) x1 f(x1) f`(x1) ER'.split())
        results.loc[k] = [x0, 'None', 'None', fx0, self.df(x0), 'None']
        results.to_excel(filename + ".xlsx") 

        while E > self.e:
                # Applying the method
                dx = self.f(x0)/self.df(x0)
                x1 = x0 - dx
                fx1 = self.f(x1)

                # Relative error
                E = abs((x1-x0)/x1)

                # Saving the k-th iteration result
                results.loc[k+1] = [x0, dx, x1, fx1, self.df(x1), E]
                results.to_excel(filename + ".xlsx")   

                # Change the x0 value
                x0 = x1
                k = k+1

                # Limit the while loop
                if k > 30: break

        print('The root with {} iterations is {:.9f} by the domain'.format(k, x1))
        return x1, results          
        
    def bicessao(self, x1, x2, x_apx, **file_name):
        results = pd.DataFrame(columns='a b p f(a) f(b) f(p) ER'.split())
        f1 = self.f(x1)
        if f1==0.0: return x1
        f2 = self.f(x2)
        if f2==0.0: return x2

        if f1*f2> 0.0: 
            raise rootError('Root is not bracketed, the Bolzano\'s theorem must be satisfied')        

        error = 1
        n = 0

        if file_name.get('filename') == None:
            filename = 'Bisection_results'
        else:
            filename = file_name.get('filename')
       
        
        while True:
                error = abs((x2 - x1)/x2)
                if error<self.e: break
                if n==0:
                    p = x_apx; f_p = self.f(p)
                else:
                    p = 0.5*(x1+x2); f_p = self.f(p) # Middle point

                if n==0:
                    results.loc[n] = [x1, x2, p, self.f(x1), self.f(x2), f_p, 'error']
                    results.to_excel(filename + ".xlsx")
                else:
                    results.loc[n] = [x1, x2, p, self.f(x1), self.f(x2), f_p, error]
                    results.to_excel(filename + ".xlsx")
                
                # Att the new values for bissections method
                if f1*f_p > 0.0:
                    x1 = p; 
                else:
                    x2 = p;
                n += 1

        print('The root of function f is {:.6f} with {} iterations'.format(x1, n-1))
        return p
        
    def plot(self, xi, xf):
            u = np.linspace(xi,xf,100)
            y = self.f(u)
            figure = plt.figure(figsize=(15,10))
            plt.grid(color='k', linestyle='--', alpha=0.4)
            plt.plot(u,y)
            
            
# Defining the function and their derivative
x = Symbol('x')
f = sin(x)/(x**2) - cos(x)/(x) # Funcao aqui
f_linha = lambdify(x, f.diff())
f = lambdify(x, f)

# Calling the object 

# Plot of the function
prova1 = roots(f, f_linha, 1e-4)
prova1.plot(0.1,15)

# Solving the ploblem
n = int(input('Number of intervals: '))
for i in range(n):
    I = input('{}º interval in format [a ,b] without the brackets: '.format(i+1))
    I = list(map(lambda i: float(i), I.split(',')))
    
    print(' Chose the method\n1-Newton\n2-Bisection\n')
    method = int(input('Select:'))
    
    name = input('Name for your output file? Enter for none: ')
    if name == '':
        name = None
            
    if method == 1:
        rand = I[0] + float('{:.6f}'.format(random()))
        print('\nNEWTON METHOD FOR {}º INTERVAL -------------------------'.format(i+1))
        prova1.newton(rand, filename=name)
        print('The random number for this one is {}'.format(rand))
        print('------------------------------------------------------')
        
    elif method == 2:
        rand = I[0] + float('{:.6f}'.format(random()))
        print('\nBISECTION METHOD FOR {}º INTERVAL -------------------------'.format(i+1))
        prova1.bicessao(I[0], I[1], rand, filename=name)
        print('The random number for this one is {}'.format(rand))
        print('------------------------------------------------------')
        
print('Done')
