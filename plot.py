import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
L=int(sys.argv[1])
t=int(sys.argv[2])
pp=int(sys.argv[3])/(1000)

A=pd.read_csv("DP_L"+sys.argv[1]+"T"+sys.argv[2]+"P"+sys.argv[3]+"data.txt",delim_whitespace=True,header=None)
B=pd.read_csv("DP_OP_L"+sys.argv[1]+"T"+sys.argv[2]+"P"+sys.argv[3]+".txt",delim_whitespace=True,header=None)

x=A[0]
y=A[1]

eps=B[0]
zet=B[1]
iot=B[2]

fig, ax=plt.subplots()
plt.title("$Directed\; Percolation\; in\; (1+1)\; dimensions$ \n"+"$\;L="+str(L)+"\;t="+str(t)+"\;p="+str(pp)+"$")

ax.set_xlabel(r"$Space\; coordinate \;  x(t)$")
ax.set_ylabel(r"$time\; coordinate \; \rightarrow \;t$")
ax.set_ylim([0,t])

plt.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False,
    left=False,
    right=False,
    labelleft=False
) # labels along the bottom edge are off
#for i in range(len(x)):
#    w=np.arange(x[i]-0.5,x[i]+0.5,0.1,dtype=None)
#    z=np.arange(y[i]-0.5,y[i]+0.5,0.1,dtype=None)
#    plt.fill_between(w,z,color="blue")


ax.scatter(x,y,s=1,marker="s",color="black")
ax.set_aspect("auto")
plt.savefig("PD.png")

plt.figure()
plt.title("$Directed\; Percolation\; in\; (1+1)\; dimensions$ \n"+"$\;L="+str(L)+"\;t="+str(t)+"\;p="+str(pp)+"$")

plt.xlabel(r"$t$")
plt.ylabel(r"$\rho(t)$")
plt.errorbar(eps,zet,yerr=iot,label=r"$\rho(t)$")
plt.legend()
plt.savefig("rho.png")
