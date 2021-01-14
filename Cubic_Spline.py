import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def solve_spline(x, y, derivatives = [], verbose = True):
    n = len(x) # Número de pontos
    assert len(y) == n, "The vectors must have the same length, please check it"
    
    a = y.copy()
    h = np.zeros(n-1)
    for i in range(n-1):
        h[i] = x[i+1] - x[i]
    
    # Matrix to solve
    A = np.zeros((n,n))
    B = np.zeros(n)
    
    # Part of fix and natural Spline
    for i in range(1,n-1):
        A[i][i-1] = h[i-1]
        A[i][i] = 2*(h[i-1] + h[i])
        A[i][i+1] = h[i]
        
        B[i] = 3*(a[i+1] - a[i])/float(h[i]) - 3*(a[i] - a[i-1])/float(h[i-1])
        
    # Part in witch depends on the type of Spline, first it will try to use the derivatives, if it does'nt run use
    # the natural spline
    try:
        df0 = derivatives[0]
        df1 = derivatives[1]
        
        A[0][0] = 2*h[0]
        A[0][1] = h[0]
        A[-1][-2] = h[-2]
        A[-1][-1] = 2*h[-2]
        
        B[0] = 3*(a[1] - a[0])/float(h[0]) - 3*df0
        B[-1] = 3*df1 - 3*(a[-1] - a[-2])/float(h[-2])
    except:
        # Natural Spline
        A[0][0] = 1
        A[-1][-1] = 1
        
    # Finding the solution
    c = np.linalg.solve(A,B)
    b = np.zeros(n-1)
    d = np.zeros(n-1)
    for i in range(n-1):
        b[i] = (a[i+1]-a[i])/float(h[i]) - h[i]*(2*c[i] + c[i+1])/3
        d[i] = (c[i+1] - c[i])/(3*h[i])
    
    data = pd.DataFrame(columns='i;x;y;h;a;b;c;d'.split(';'))
    if verbose:
        print('Spline Matrix \n')
        # Make some function do show the data
        for i in range(len(A)):
            for j in range(len(A[i])):
                print(A[i][j], end=" ")
            print("|", B[i])
            
        for i in range(n-1):
            data.loc[i] = [i, x[i], y[i], h[i], a[i], b[i], c[i], d[i]]
            
        
    coef = np.zeros((n-1, 4))
    for i in range(n-1):
        coef[i][0] = a[i]
        coef[i][1] = b[i]
        coef[i][2] = c[i]
        coef[i][3] = d[i]
    
    return coef, data


def calc_spline(x, X, coef):
    y = 0
    
    try:
        n = len(X)
        y = np.zeros(n)
        for i in range(n):
            y[i] = calc_spline(x, X[i], coef) # Controled "Recursion", it is just a beautiful way do implement
    except:
        
        # Find the position of X inside of x
        k = x.searchsorted(X)
        
        if k>0: k-=1 # Use left point
        if k == len(x): k -=1 # X[i]>x[n]
            
            
        H = X - x[k]
        ak = coef[k][0]
        bk = coef[k][1]
        ck = coef[k][2]
        dk = coef[k][3]
        
        y = ak + H*(bk + H*(ck + H*dk))
        
    return y

def generate_plot(x,y,xx=0,yy=0):
    try:
        n = len(xx)
        plt.plot(x,y,'o')
        plt.grid(linestyle='--')
        plt.plot(xx, yy, '-')
        plt.margins(0.1)
    except:
        plt.plot(x,y,'o')
        plt.grid(linestyle='--')
        plt.margins(0.1)
        

# Testing
x = np.array([0,6,10,13,17,20,28])
y = np.array([6.67, 16.11, 18.89, 15, 10.56, 9.44, 8.89])

coef, data = solve_spline(x, y, derivatives=[], verbose=False)
nn = 100*len(x)
xx = np.linspace(x[0], x[-1], nn)
yy = calc_spline(x, xx, coef)

generate_plot(x,y,xx,yy)
