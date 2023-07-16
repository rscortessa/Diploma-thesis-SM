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

allsys=int(arg[8])
system=["Equilibrium","Total\;system"]
portion=int(arg[9])
## This part of the code creates the image for the percolation:
m=math.floor(dp/za)*N
read_portion=int(m*portion/100)
r_portion=(portion/100*N)

entire_set=True
centralized=False

if portion==100:
    entire_set=True
else:
    entire_set=False

filename="./graph3/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt"

if entire_set==True:
    files=pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8)
    if centralized==False:
        vary=np.array(files.std())
    scaler=StandardScaler()
    scaler.fit(files)
    scaled_data=scaler.transform(files)
    pca=PCA()
    pca.fit(scaled_data)
    if centralized==False:
        pca_L=np.dot(files,np.multiply(pca.components_.T,vary))
    else:
        pca_L=pca.transform(scaled_data)
    x_pca=pca_L
else:
    tracemalloc.start()
    with pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8,chunksize=read_portion) as reader:
        for chunk in reader:
            print(chunk,sys.getsizeof(chunk))
            pca.partial_fit(chunk)    
    print("PCA",sys.getsizeof(pca))

    with pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8,chunksize=read_portion) as reader:
        for chunk in reader:
            x_pca=pca.transform(chunk)
            x_pca=np.abs(x_pca[:,0])
            pca_L=np.concatenate((pca_L,x_pca),axis=0)
    x_pca=pca_L
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()

    

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



plt.figure(figsize=(8,6))
plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; the\; two \; first\; PCs$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(x_pca[:,0],x_pca[:,1],s=1,c=np.array([pp+za*int(i/N) for i in range(int(m))]),cmap="plasma",norm=cl.Normalize(vmin=pp, vmax=pp+dp),label="dataset")
plt.xlabel(r"$PC_1$",fontsize=14)
plt.ylabel(r"$PC_2$",fontsize=14)
plt.legend()
cbar = plt.colorbar(ax=plt.gca())
cbar.ax.set_title(r'$Probability \times 10^{3}$', fontsize=12)
cbar.ax.tick_params(labelsize=10)
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PCA.pdf")


PP=np.array([pp+za*int(i/N) for i in range(int(m))])

plt.figure(figsize=(8,6))
plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; the\; first\; PC$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(PP,np.abs(x_pca[:,0]),s=1,c=np.array([pp+za*int(i/N) for i in range(int(m))]),cmap="plasma",norm=cl.Normalize(vmin=pp, vmax=pp+dp),label="dataset")
plt.xlabel(r"$Probability \; p$",fontsize=14)
plt.ylabel(r"$PC_1$",fontsize=14)
plt.legend()
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PC1.pdf")


plt.figure(figsize=(8,6))
plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; the\; second\; PC$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"$",fontsize=14)
plt.scatter(PP,np.abs(x_pca[:,1]),c=np.array([pp+za*int(i/N) for i in range(int(m))]),s=1,cmap="plasma",norm=cl.Normalize(vmin=pp, vmax=pp+dp),label="dataset")
plt.xlabel(r"$Probability \; p$",fontsize=14)
plt.ylabel(r"$PC_2$",fontsize=14)
plt.legend()
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PC2.pdf")








#Principal Components
#N is the number of repetitions
#int(m/N) is the number of points with different probability
num=math.floor(dp/za)
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

write_text(np.array([C,A[:,0],B[:,0]]),"./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(za)+"Z"+str(N)+"N"+"PC1.txt")

