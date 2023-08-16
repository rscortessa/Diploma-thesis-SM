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
dp=int(arg[4])
N=int(arg[5])
zas=int(arg[6])
allsys=int(arg[7]); system=["Equilibrium","Total\;system"]
sites=L
m=int(dp/zas)

rho=[0 for i in range(m)]
p=[pp+zas*i for i in range(m)]

A=pd.read_csv("DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt",delim_whitespace=True,header=None)
A=np.array(A)

###Create an array of the values of rho for the steady state for different values of p.
for i in range(m):
    rho[i]= np.mean(np.array([ np.mean(A[j,:]) for j in range(i*N,(i+1)*N)]))


fig,ax=plt.subplots()
ax.set_title("Projection data")
ax.matshow(A,cmap="Greys")
if allsys==1:
    ax.set_aspect(L*t/(m*N))
else:
    ax.set_aspect(L/(m*N))
#plt.colorbar()
ax.set_xlabel("Sites",fontsize=15)
ax.set_ylabel("$N_{configurations}$",fontsize=15)
#ax.set_xticks(fontsize=15)
#ax.set_yticks(fontsize=15)
plt.savefig("DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".png")

plt.figure()
plt.title(r"$Steady \; value\; of \; \rho$")
plt.scatter(p,rho,label=r"$Steady \;configuration\; \rho$")
plt.legend()
plt.savefig("DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+"rho.png")


write_text(np.array([p,rho]),"rho.txt")
