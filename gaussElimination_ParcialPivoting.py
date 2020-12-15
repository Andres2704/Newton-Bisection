import numpy as np
import pandas as pd

def gaussEliminationPivoting(A, B):
    n = len(A)
    results_perm = pd.DataFrame(columns='Pivô;Linha Pivo;Matriz A Permutada;Vetor b permutado'.split(';'))
    results_gauss = pd.DataFrame(columns='Gauss - Vetor(A); Gauss-Vetor(b)'.split(';'))
    # Accessing the lines
    for i in range(n):
        print('\n{}ª Iteraçao ----------'.format(i+1))
        # Checking which is the bigger pivot
        pivot = math.fabs(A[i][i])
        pivotLine = i
        for j in range(i+1, n):
            if math.fabs(A[j][i]) > pivot:
                pivot = math.fabs(A[j][i])
                pivotLine = j
         
        # Permuting lines
        if pivotLine != i:
            lineAux = A[i]
            A[i] = A[pivotLine]
            A[pivotLine] = lineAux
            
           # For the column matrix
            bAux = B[i]
            B[i] = B[pivotLine]
            B[pivotLine] = bAux

        A_l = A.copy()
        B_l = B.copy()
       
        results_perm.loc[i+1] = [pivot, pivotLine, np.array(A_l), np.array(B_l)]
        
        
        # Gauss elimination
        for m in range(i+1, n):
            lam = A[m][i]/A[i][i]
            for k in range(i, n):
                A[m][k] -= lam*A[i][k]
            B[m] -=  lam*B[i]
            
        results_gauss.loc[i+1] = [np.array(A), np.array(B)]
        
    
    results = pd.concat([results_perm, results_gauss], axis=1)
    results.to_excel("Output_gaussEliminationPivoting.xlsx")    
                               
    for k in range(n-1,-1,-1):
        B[k] = (B[k] - np.dot(A[k][k+1:n],B[k+1:n]))/A[k][k]
        print(B[k])
    
    print('The solution is:')
    print(B)
    
    return B, results
    
A1 = [[4,-2,1], [-2, 4, -2], [1,-2,4]]
B1 = [11,-16,17]
[B, result] = gaussEliminationPivoting(A1,B1)                               
