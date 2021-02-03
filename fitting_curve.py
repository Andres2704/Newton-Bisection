import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class adjust():
    def __init__(self):
        pass
    def linear(self, x, y, verbose=True):
        '''
        Linear regression applying least squares method
        Receive:
            x, y - Dataset
            verbose - Print each step (True or False)
        Return:
            a0 and an of y = a0 + a1*x
        '''
        n = len(x)
        assert n==len(y), "The length of x and y are differents"
        
        # Summation terms
        sx = 0
        sx2 = 0
        sy = 0
        sxy = 0
        
        for i in range(n):
            sx += x[i]
            sx2 += x[i]**2
            sy += y[i]
            sxy += y[i]*x[i]
        
        # Coefficient calc derived from leasts squares
        a0 = (sx2*sy - sxy*sx)/(n*sx2 - sx**2)
        a1 = (n*sxy -sx*sy)/(n*sx2 - sx**2)
        
        if verbose:
            print('The adjusted curve (linear regression) is: y = a0 + a1*x')
            print('a0 = ', a0)
            print('a1 = ', a1)
        
        
        return a0, a1
    
    def poly(self, x, y, d, verbose=True):
        '''
        Polynomial fitting, also with least squares method but does not use multiple linear regression method
        Receive:
            x, y - Dataset
            d    - Degree of the polynomial
            verbose - Print or not each step
        Return:
            an - The coefficients of polynomial order from 0 to d power
            matrix - Resultant matrix just before the solution takes place
        '''
        n = len(x)
        assert n==len(y), 'x and y have different length, check it'
        assert d>0, 'Please, set at least a degree of one'
        g = d+1
        
        sx = np.zeros(2*d+1)
        sxy = np.zeros(g)
        for i in range(n):
            xn = 1
            for j in range(2*d+1):
                sx[j] += xn
                if j < d+1:
                    sxy[j] += y[i]*xn
                xn *= x[i]
        
        A = np.zeros((g,g))
        B = np.zeros(g)
        for i in range(g):
            for j in range(g):
                A[i][j] = sx[i+j]
            B[i] = sxy[i]
            
        self.matrix = pd.DataFrame(A, columns=['A['+str(i)+']' for i in range(g)])
        self.matrix['B'] = B
        if verbose:
            print("------------------------------")
            print("Left hand side matrix:")
            print(self.matrix)
            
        an = np.linalg.solve(A, B)
        if verbose:
            print('\nPolynomial coefficients:')
            print('an = ', an)
            
        return an, self.matrix
    
    def exp(self, x, y, verbose=True):
        '''
        Exponential fitting (y=b*exp(ax))
        Receive:
            x, y - Dataset
            Verbose - Print or not each step
        Return: 
            a, b  - from the exponential equation
            matrix - Resulting matrix of the process
        '''
        n = len(x)
        assert n==len(y), 'x and y have different length, check it'
        
        y_b = np.log(y)
        a0, a1 = self.linear(x, y_b, verbose=False)
        b = np.exp(a0)
    
        data = np.c_[x, y, y_b]
        self.matrix = pd.DataFrame(data = data, columns='x;y;ln(y)'.split(';'))
        if verbose:
            print("------------------------------")
            print("Data:")
            print(self.matrix)

            print("\n\n------------------------------")
            print("Adjusted Coefficients:")
            print("B = ",a0)
            print("b = exp(B) = ",b)
            print("a = ",a1)
            print("------------------------------")
            print("Exponential fit: y = %.3g * exp(%.3g * x)" % (b,a1))
            
        return b, a1, self.matrix
            
    def pot(self, x, y, verbose=True):
        '''
        Power fitting (y=b*x^(a))
        Receive:
            x, y - Dataset
            Verbose - Print or not each step
        Return: 
            a, b  - from the power equation
            matrix - Resulting matrix of the process
        '''
        n = len(x)
        assert n==len(y), 'x and y have different length, check it'
        
        y_b = np.log(y)
        x_b = np.log(x)
        a0, a1 = self.linear(x_b, y_b, verbose=False)
        b = np.exp(a0)

        data = np.c_[x, y, y_b, x_b]
        self.matrix = pd.DataFrame(data = data, columns='x;y;ln(y);ln(x)'.split(';'))
        if verbose:
            print("------------------------------")
            print("Data:")
            print(self.matrix)

            print("\n\n------------------------------")
            print("Fitted coefficients:")
            print("B = ",a0)
            print("b = exp(B) = ",b)
            print("a = ",a1)
            print("------------------------------")
            print("Power fitting: y = %.3g x^%.3g" % (b,a1))
            
        return b, a1, self.matrix
            
    def to_excel(self):
        try:
            self.matrix.to_excel('Results.xlsx')
        except:
            print('Resulting matrix does not exist}')
           
           
# Example
ajuste = adjust()
x = 5*np.random.rand(10, 1)
y = 4 + 3*x**2 + np.random.rand(10, 1)

an, matrix = ajuste.poly(x, y, 2)

xx = np.linspace(min(x), max(x), 10)
yy = an[0] + an[1]*xx + an[2]*xx**2
fig, ax = plt.subplots(figsize=(10,10))
ax.scatter(x, y, label = 'Real data')
ax.plot(xx, yy, label = 'Fitted curve')
plt.legend()
