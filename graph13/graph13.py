import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import sys
import gc
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA
sys.path.append("./")
from analyze_data import PCA_txt_

import math

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
sites=int(arg[5])
N=int(arg[6]) #200
print("This is N",N)
za=int(arg[7])
m=math.floor(dp/za)*N
print("This is m",m)
norma=10000
allsys=int(arg[8])
system=["Equilibrium","Total\;system"]
batch_sizes=int(int(arg[9])*m/100.0)
## This part of the code creates the image for the percolation:

entire_set=True
centralized=True
if allsys==0:
    centralized=False
pca,x_pca=PCA_txt_(L,t,pp,dp,sites,"/graph10/",entire_set,centralized,batch_sizes,True)
x_pca=x_pca[:,1]

##First it is required to chose the points in the graph to analyze the distribution
## As a rule of thumb let's consider four points well distributed in the sample:
Npoints=10
NofP=math.floor(dp/za)
Increment=int(NofP/Npoints)
pca_psamples=[ [x for x in np.sort(x_pca[Increment*i*N:(Increment*i+1)*N]) ] for i in range(Npoints)]

def DiaconisRule(A,N):
    A=np.array(A)
    dx=2*(A[int(3/4*len(A))]-A[int(1/4*len(A))])/N**(1/3)
    Nu=(A.max()-A.min())/dx
    if dx==0.0:
        Nu=0
    return int(Nu)

Nofpoints=[ DiaconisRule(pca_psamples[i][:],N) for i in range(Npoints)]

#dx=2*(IQ3-IQ1)/(len(x_pca)**(1/3))
#N=int((x_pca.max()-x_pca.min())/dx)
print(Nofpoints)
#Used to calculate the cumulative distribution function:
pde=[i/N for i in range(N)]     

plt.figure()
plt.title(r"$P_2 \;Cumulative\;Distribution\;Function $"+"\n"+"$L="+str(L)+"\;"+r"\tau="+str(t)+"\;N="+str(N)+"$")
plt.xlabel(r"$\langle P_2\rangle$")
plt.ylabel(r"$CDF\;(\langle P_2\rangle)$")

for i in range(Npoints):
         plt.plot(pca_psamples[i][:],pde,label="$P="+str((pp+Increment*i*za)/norma)+r"$")
plt.legend()
plt.savefig("./graph13/pde.png")

counts=[0 for i in range(Npoints)]
bins=[0 for i in range(Npoints)]

if allsys==1:
    fig, axs=plt.subplots(2)
    axs[0].set_title(r"$ P_2 \;Probability\;Density\;Function$"+"\n"+"$L="+str(L)+"\;"+"\tau="+str(t)+"\;N="+str(N)+"$")
    axs[0].set_xlabel(r"$P_2$")
    axs[1].set_ylabel(r"$PDF(P_2)$")
    axs[1].set_xlabel(r"$P_2$")
    axs[0].set_ylabel(r"$PDF(P_2)$")

    axs[0].set_yscale("log")           
    axs[0].set_ylim([0.01,1])
    axs[1].set_yscale("log")           
    axs[1].set_ylim([0.01,1])

    first_one=range(int(Npoints/2))
    second_one=range(int(Npoints/2),Npoints)
    s=0

    for i in first_one:
        counts[i],bins[i]=np.histogram(pca_psamples[i][:],bins=Nofpoints[i],density=True)
        axs[0].stairs(counts[i],bins[i],label=r"$P="+str((pp+Increment*i*za)/norma)+r"$")
    for i in second_one:
        counts[i],bins[i]=np.histogram(pca_psamples[i][:],bins=Nofpoints[i],density=True)
        axs[1].stairs(counts[i],bins[i],label=r"$P="+str((pp+Increment*i*za)/norma)+r"$")
           
    axs[0].legend()
    axs[1].legend()
else:
    plt.figure()
    plt.title(r"$ P_2 \;Probability\;Density\;Function$"+"\n"+"$L="+str(L)+"\;"+r"\tau="+str(t)+"\;N="+str(N)+"$")
    plt.xlabel(r"$P_2$")
    plt.ylabel(r"$PDF(P_2)$")
    #plt.yscale("log")
    #plt.ylim([0.01,1])
    for i in range(Npoints):
        if Nofpoints[i]!=0:
            counts[i],bins[i]=np.histogram(pca_psamples[i][:],bins=Nofpoints[i],density=True)
            plt.stairs(counts[i],bins[i],label=r"$P="+str((pp+Increment*i*za)/norma)+r"$")
plt.legend()
plt.tight_layout()
plt.savefig("./graph13/QPCD.png")


