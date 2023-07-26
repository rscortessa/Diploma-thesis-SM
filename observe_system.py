import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np

def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))



arg=sys.argv
L=int(arg[1])
t=int(arg[2])
pp=int(arg[3])
N=int(arg[4])
sites=L

A=pd.read_csv("DP_L"+str(L)+"T"+str(t)+"P"+str(pp)+"S"+str(sites)+"data.txt",delim_whitespace=True,header=None)
A=np.array(A)

###Create an array of the values of rho for the steady state for different values of p.

plt.figure(figsize=(4,4))
plt.title(r"$Directed\;bond\;percolation\;at\;(1+1)\;dimension$"+"\n"+"$L="+str(L)+"\;t="+str(t)+"\;p="+str(pp)+"$")
plt.matshow(A,cmap="binary")
plt.gca().set_aspect("auto")
#plt.xlabel(r"$sites$")
#plt.ylabel(r"$time\;t$")
#plt.colorbar()
plt.savefig("DP_L"+str(L)+"T"+str(t)+"P"+str(pp)+"S"+str(sites)+".png")
