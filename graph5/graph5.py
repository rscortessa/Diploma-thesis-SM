import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import scipy.interpolate as ssc
from scipy.interpolate import splev,splrep
from scipy.interpolate import make_smoothing_spline
from scipy.interpolate import make_lsq_spline
from sklearn.preprocessing import PolynomialFeatures
import math

def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))
            

##The file has to be loaded:

arg=sys.argv # Arguments giving by console.
L=int(arg[1]) # Number of lattice sites.
t=int(arg[2]) # Number of time-steps.
pp=int(arg[3]) # Initial probability x 10.000.
dp=int(arg[4]) # Change in probability x 10.000.
sites=int(arg[5]) # Number of inital active sites.
N=int(arg[6]); print("This is N",N) # Number of repetitions for each probability.
za=int(arg[7]) # Increment in the probability for each cycle x 10.000.
m=math.floor(dp/za)*N; print("This is m",m) # Number of points of rows of the data. 
waw=int(m/N) # Number of points in the p-axis
allsys=int(arg[8])
smooth=int(arg[9])
system=["Equilibrium","Total\;system"]
#Create the scale:
scaler=StandardScaler()
# It is proccesed the data for the PCA:
# All the points with different probability need to be examined separately:

# It is created the arrays to store the information

S=[0 for i in range(waw)]
L1=[0 for i in range(waw)]
L12=[0 for i in range(waw)]
P=np.array([pp+za*i for i in range(waw)])

lamb=[]

F=np.array([0.6,0.7,0.8,0.9])
Id=[[0 for jj in range(waw)] for i in F]
Id_PCA=[0 for jj in range(waw)]

for yy in range(waw): #Loop over all diferent points 
    A=pd.read_csv("./graph5/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt",delim_whitespace=True,header=None,skiprows=yy*N,nrows=N)
    scaler.fit(A)
    scaled_data=scaler.transform(A)
    pca=PCA()
    pca.fit(scaled_data)
    x_pca=pca.transform(scaled_data)
    sing=np.array(pca.singular_values_)
    sing=sing**2/(np.sum(sing**2))
    lamb=[x for x in sing]
    sing=-sing*np.log(sing)
    S[yy]=np.sum(sing)/np.log(len(pca.singular_values_))
    #The following code computes the intrinsic dimension:
     #First, the variables are initialized:
    lamb.sort(reverse=True)
    L1[yy]=lamb[0]
    L12[yy]=lamb[0]-lamb[1]
    Id_PCA[yy]=pca.n_components_
    #For each probability and F value, the intrinsic dimension is calculated:
    for ff in range(len(F)):
        sum=0
        for i in range(len(lamb)):
            sum=sum+lamb[i]
            if sum <= F[ff]:
                continue
            else:
                Id[ff][yy]=i
                break
Id=np.array(Id)    
        

#It is plotted the entropy:
X=np.arange(P[0],P[len(P)-1],za/1000)
mymodel=np.poly1d(np.polyfit(P,S,smooth))
Y=mymodel(X)
DY=mymodel.deriv(m=1)

plt.figure(figsize=(8,6))
plt.title(r"$S(p)\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$Entropy\;S(p)$",fontsize=14)
plt.scatter(P,S,label="Entropy")
plt.plot(P,S,color="black")
plt.plot(X,Y,color="red",label="interpolation")

plt.legend()
plt.savefig("./graph5/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"S.pdf")
write_text(np.array([P,S]),"./graph5/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"S.txt")



#It is plotted the first component:

plt.figure(figsize=(8,6))
plt.title(r"$\lambda s\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$\lambda_1\; ,\lambda_1-\lambda_2$",fontsize=14)
plt.scatter(P,L1,label=r"$\lambda_1$")
plt.plot(P,L1,color="black")
plt.scatter(P,L12,label=r"$\lambda_1-\lambda_2$")
plt.plot(P,L12,color="black")
plt.legend()
plt.savefig("./graph5/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"L1.pdf")
write_text(np.array([P,L1]),"./graph5/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"L1.txt")






#It is calculated the derivative of the entropy and it is plotted as well:

ds=DY(X)
maxi=0
ii=0
for x in range(len(ds)):
    if X[x]>=6200 and X[x]<=6600:
        if maxi<ds[x]:
            maxi=ds[x]
            ii=x
            
plt.figure(figsize=(8,6))
plt.title(r"$dS/dp \; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$\frac{dS(p)}{dp}$",fontsize=14)
plt.scatter(X,ds,label=r"$\frac{dS}{dP}$")
plt.plot(X,ds,color="black")
plt.axvline(x=6447,label=r"$p_c=$"+"6447"+r"$ \times 10^{-3}$")
plt.axvline(x=X[ii],linestyle="dashed",label=r"$p_{c_{exp}}=$"+str(int(X[ii]))+r"$ \times 10^{-3}$")
plt.legend()
plt.savefig("./graph5/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"DS.pdf")
write_text(np.array([X,ds]),"./graph5/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"DS.txt")











#It is calculated the intrinsic dimension:

plt.figure(figsize=(8,6))
plt.title(r"$I_d(p)\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$I_d\; Intrinsic\; Dimension$",fontsize=14)

for ff in range(len(F)):
    plt.scatter(P,Id[ff,:],label=r"$F="+str(F[ff])+"$")
    plt.plot(P,Id[ff,:])

plt.scatter(P,Id_PCA,label=r"$PCA\;Analysis$")
plt.legend()
plt.savefig("./graph5/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"ID.pdf")
SS=[]
for ff in range(-1,len(F)):
    if ff==-1:
        SS.append(P)
    else:
        SS.append(Id[ff,:])
write_text(np.array(SS),"./graph5/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"ID.txt")




