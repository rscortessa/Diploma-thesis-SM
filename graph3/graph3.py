import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import math
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

allsys=int(arg[8])
system=["Equilibrium","Total\;system"]
## This part of the code creates the image for the percolation:
#A=pd.read_csv("DP_L"+sys.argv[1]+"T"+sys.argv[2]+"P"+sys.argv[3]+"S"+sys.argv[4]+"data.txt",delim_whitespace=True,header=None)
A=pd.read_csv("./graph3/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt",delim_whitespace=True,header=None)
print(A)




scaler=StandardScaler()
scaler.fit(A)
scaled_data=scaler.transform(A)




pca=PCA()
pca.fit(scaled_data)
x_pca=pca.transform(scaled_data)


y=pca.explained_variance_ratio_
sing=pca.singular_values_

x=[i for i in range(len(y))]
x=np.array(x)
plt.figure(figsize=(8,6))
plt.title(r"$Fraction\; of\; the \; variance \;of\; the \; \;data \;set\; in\; the\; PCs$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(x,y,s=5,label="Fraction of the variance")
plt.legend()
plt.savefig("./graph3/"+system[allsys]+"Fraction_variance.png")

z=pca.components_

if allsys ==1:
    q=[i for i in range(t*L)]
else:
    q=[i for i in range(L)]

    
plt.figure(figsize=(8,6))
plt.title(r"$PCA_1\; vector\;$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(q,z[0,:],s=5,label=r"$PCA_1\;proyection$")
plt.legend()
plt.savefig("./graph3/"+system[allsys]+"L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"PCA1_proy.png")


print(len(x_pca[:,1])/N,"Let's see",dp,m*za/N)

plt.figure(figsize=(8,6))
plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; the\; two \; first\; PCs$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(x_pca[:,0],x_pca[:,1],s=1,c=np.array([pp+za*int(i/N) for i in range(int(m))]),cmap="plasma",norm=cl.Normalize(vmin=pp, vmax=pp+dp),label="dataset")
plt.xlabel(r"$PC_1$",fontsize=14)
plt.ylabel(r"$PC_2$",fontsize=14)
plt.legend()
cbar = plt.colorbar(ax=plt.gca())
minix=min(x_pca[:,0])
maxx=max(x_pca[:,0])
miniy=min(x_pca[:,1])
maxy=max(x_pca[:,1])
xo=minix+(maxx-minix)/10.0
yo=miniy+(maxy-miniy)/10.0
dx=(maxx-minix)/10.0
dy=(maxy-miniy)/10.0
#inset_axes=inset_axes(plt.gca(),width="30%",height="30%",loc="upper center")
#inset_axes.scatter(x_pca[:,0],x_pca[:,1],s=1,c=np.array([pp+za*int(i/N) for i in range(int(m))]),cmap="plasma",norm=cl.Normalize(vmin=pp, vmax=pp+dp),label="dataset")
#inset_axes.set_xlim([-20,50])
#inset_axes.set_ylim([-20,20])
cbar.ax.set_title(r'$Probability \times 10^{3}$', fontsize=12)
cbar.ax.tick_params(labelsize=10)

plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PCA.pdf")



plt.figure(figsize=(8,6))
plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; the\; first\; PC$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(np.array([pp+za*int(i/N) for i in range(int(m))]),x_pca[:,0],s=1,cmap="plasma",norm=cl.Normalize(vmin=pp, vmax=pp+dp),label="dataset")
plt.xlabel(r"$Probability \; p$",fontsize=14)
plt.ylabel(r"$PC_1$",fontsize=14)
plt.legend()
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PC1.pdf")


plt.figure(figsize=(8,6))
plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; the\; second\; PC$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"$",fontsize=14)
plt.scatter(np.array([pp+za*int(i/N) for i in range(int(m))]),x_pca[:,1],s=1,cmap="plasma",norm=cl.Normalize(vmin=pp, vmax=pp+dp),label="dataset")
plt.xlabel(r"$Probability \; p$",fontsize=14)
plt.ylabel(r"$PC_2$",fontsize=14)
plt.legend()
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PC2.pdf")








#Principal Components
#N is the number of repetitions
#int(m/N) is the number of points with different probability
num=int(m/N)
print("this is num", num)
num_pca=4
A=[[0 for i in range(num_pca)] for i in range(num)]
B=[[0 for i in range(num_pca)] for i in range(num)]
C=[pp+za*i for i in range(num)]


for l in range(num_pca):
    for j in range(num):
        D=np.array([np.abs(f) for f in x_pca[N*j:N*(j+1),l]])
        A[j][l]=np.mean(D)
        B[j][l]=np.std(D)/np.sqrt(N)

A=np.array(A)
B=np.array(B)
C=np.array(C)


plt.figure(figsize=(8,6))
plt.title(r"$|PCs|\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$|PC|$",fontsize=14)
for l in range(num_pca):
    plt.errorbar(C,A[:,l],yerr=B[:,l],label=r"$|PCA_"+str(l+1)+"|$")
    plt.plot(C,A[:,l],color="black") 
    plt.legend()
    plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"PCs.pdf")

