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
import importlib.util

sys.path.append("./")
from analyze_data import PCA_txt_


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
system=["Steady\;state","Full\;evolution"]
portion=int(arg[9])
normalization=10000
## This part of the code creates the image for the percolation:
m=math.floor(dp/za)*N
read_portion=int(m*portion/100)
r_portion=(portion/100*N)

entire_set=True
centralized=True

#if portion==100:
#    entire_set=True
#else:
#    entire_set=False

pca,x_pca=PCA_txt_(L,t,pp,dp,sites,"/graph3/",entire_set,centralized,read_portion,True)

    
y=pca.explained_variance_ratio_
sing=pca.singular_values_

x=[i for i in range(len(y))]
x=np.array(x)
plt.figure(figsize=(8,6))
#plt.title(r"$Explained \;Variance \;Ratio$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(x,y,s=5,label=r"$\{\tilde{\lambda}_n\}$")
plt.ylabel(r"$\tilde{\lambda}_i$",fontsize=20)
plt.xlabel(r"$Principal\;Component\;index\;i$",fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
plt.yscale("log")
plt.tight_layout()
plt.savefig("./graph3/"+system[allsys]+"Fraction_variance.png")

z=pca.components_

if allsys ==1:
    q=[i for i in range(t*L)]
else:
    q=[i for i in range(L)]

    
plt.figure(figsize=(8,6))
#plt.title(r"$Proyection \;of \;P_1\;over \;the\;total\;lattice\;sites$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(q,z[0,:],s=5,label=r"$P_1\;projection$")
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=15)
plt.tight_layout()
plt.savefig("./graph3/"+system[allsys]+"L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"PCA1_proy.png")

plt.figure(figsize=(8,6))
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
#plt.title(r"$Proyection \;of \;P_2\;over \;the\;total\;lattice\;sites$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(q,z[1,:],s=5,label=r"$P_2\;projection$")
plt.legend(fontsize=15)
plt.tight_layout()

plt.savefig("./graph3/"+system[allsys]+"L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"PCA2_proy.png")



plt.figure(figsize=(8,6))
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#plt.title(r"$Proyection \;of \;P_3\;over \;the\;total\;lattice\;sites$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(q,z[2,:],s=5,label=r"$P_3\;projection$")
plt.legend(fontsize=15)
plt.savefig("./graph3/"+system[allsys]+"L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"PCA3_proy.png")




plt.figure(figsize=(8,6))
#plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; the\; two \; first\; P.Cs$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(x_pca[:,0],x_pca[:,1],s=1,c=np.array([pp+za*int(i/N) for i in range(int(m))])/normalization,cmap="plasma",norm=cl.Normalize(vmin=pp/normalization, vmax=(pp+dp)/normalization),label="dataset")
plt.xlabel(r"$P_1$",fontsize=20)
plt.ylabel(r"$P_2$",fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=15)
cbar = plt.colorbar(ax=plt.gca())
cbar.ax.locator_params(nbins=10)
#cbar.ax.set_title(r'$Probability \times 10^{3}$', fontsize=14)
cbar.ax.tick_params(labelsize=15)
plt.tight_layout()
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PCA.png")


PP=np.array([pp+za*int(i/N) for i in range(int(m))])/normalization
pmin=pp/normalization
pmax=(pp+dp)/normalization
plt.figure(figsize=(8,6))
#plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; P_1$"+"\n"
#         +"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.scatter(PP,np.abs(x_pca[:,0]),s=1,c=PP,cmap="plasma",norm=cl.Normalize(vmin=pmin, vmax=pmax),label="dataset")
plt.xlabel(r"$Probability \; p$",fontsize=14)
plt.ylabel(r"$P1$",fontsize=14)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PC1.png")


plt.figure(figsize=(8,6))
#plt.title(r"$Projection\; of\; the \; DATA \;set\; in\; P_2$"+"\n"
#         +"$L="+str(L)+"\;"+"t="+str(t)+"$",fontsize=14)
plt.scatter(PP,np.abs(x_pca[:,1]),c=PP,s=1,cmap="plasma",norm=cl.Normalize(vmin=pmin, vmax=pmax),label="dataset")
plt.xlabel(r"$Probability \; p$",fontsize=14)
plt.ylabel(r"$P_2$",fontsize=14)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+"PC2.png")








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
#plt.title(r"$\langle P_n\rangle \; vs \;"+"p$"+"\n"+r"$L="+str(L)+r"\;"+r"t="+str(t)+r"\;"+system[allsys]+r"$",fontsize=14)
plt.xlabel(r"$Probability\;p$",fontsize=17)
plt.ylabel(r"$\langle P_n\rangle"+"\;Quantified\;Principal\;Component$",fontsize=17)
for l in range(num_pca):
    plt.errorbar(C/normalization,A[:,l],yerr=B[:,l],label=r"$\langle P_"+str(l+1)+r"\rangle$")
    plt.plot(C/normalization,A[:,l],color="black") 
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
plt.locator_params(axis='both', nbins=7)
plt.savefig("./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"PCs.png")
plt.show()
write_text(np.array([C,A[:,0],B[:,0]]),"./graph3/"+system[allsys]+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(za)+"Z"+str(N)+"N"+"PC1.txt")

