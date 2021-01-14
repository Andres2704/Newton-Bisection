'''
    p = evalPoly(a,xData,x).
    Evaluates Newton’s polynomial p at x. The coefficient
    vector {a} can be computed by the function
    ’coeffts’.
    
    a = coeffs(xData,yData).
    Computes the coefficients of Newton’s polynomial.
'''
from sympy import *
import numpy as np
def coeffs(xData, yData):
    m = len(xData)
    a = yData.copy()
    for k in range(1, m):
        a[k:m] = (a[k:m] - a[k-1])/(xData[k:m] - xData[k-1])
    
    return a

def generatePoly(a, xData):
    x = Symbol('x')
    y = [a[0]]
    aux = 1
    n = len(x_dados)
    for i in range(1,n):
        for j in range(0, i):
            aux = aux*(x-x_dados[j])
        aux = aux*a[i]
        y.append(aux)
        aux = 1
    y = sum(y)
    return y
        
def evalPoly(a, xData, x):
    n = len(xData) - 1 # Degree of polynomial
    p = a[n]
    for k in range(1, n+1):
        p = a[n-k] + (x - xData[n-k])*p
    
    return p
    
    
 # Testing
 
 x_dados = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6]  #valores de x
y_dados = [np.exp(1), np.exp(1.2), np.exp(1.4), np.exp(1.6), np.exp(1.8), np.exp(2), np.exp(2.2), np.exp(2.4), np.exp(2.6)]  
x = 1.435

a = coeffs(np.array(x_dados), np.array(y_dados))
p = evalPoly(a, np.array(x_dados), x)
y = generatePoly(a, x_dados)
