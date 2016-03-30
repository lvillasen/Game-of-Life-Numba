# Conway's Game of Life Accelerated with Numba
# Luis Villasenor
# lvillasen@gmail.com
# 3/26/2016
# Licence: GPLv3
# Usage: python GameOfLifeNumba.py n n_iter
# where n is the board size and n_iter the number of iterations
import numpy as np
from pylab import cm as cm
import matplotlib.pyplot as plt
import numba  
import sys
@numba.autojit
def random_init(n):
    #np.random.seed(100)
    M = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            M[j,i]=np.random.randint(2)
    return M
@numba.autojit
def life_game(M,n_iter):
    nx, ny = M.shape
    for k in range(n_iter):
        C = M.copy() # copy current life grid
        for i in range(nx):
            for j in range(ny):
                if (i==0):
                    i_left=nx-1; 
                else:
                    i_left=i-1;
                if(i==nx-1):
                    i_right=0; 
                else:
                    i_right=i+1;
                if(j==0): 
                    j_down=ny-1; 
                else: 
                    j_down=j-1;
                if(j==ny-1): 
                    j_up=0; 
                else: 
                    j_up=j+1;
                count = C[i_left,j] + C[i_left,j_up] + C[i_left,j_down] \
                    + C[i,j_down] + C[i,j_up] + \
                    C[i_right,j] + C[i_right,j_up] + C[i_right,j_down] 
                if C[i, j]==1:
                    if count < 2 or count > 3:
                        M[i, j] = 0 # living cells with <2 or >3 neighbors die
                elif count == 3:
                    M[i, j] = 1 # dead cells with 3 neighbors are born
    return(M)
n=int(sys.argv[1])
n_iter=int(sys.argv[2])
m=int(sys.argv[3])
M0=random_init(n)
M=life_game(M0,n_iter)
print("%d live cells after %d iterations" %(np.sum(M),n_iter))
if m==1:
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    fig.suptitle("Conway's Game of Life Accelerated with Numba")
    while m==1:
        ax.set_title('Number of Iterations = %d'%(n_iter))
        myobj =plt.imshow(M,origin='lower',cmap='Greys',  interpolation='nearest',vmin=0, vmax=1)
        plt.draw()
        plt.pause(.01)
        n_iter+=1
        M=life_game(M,1)
