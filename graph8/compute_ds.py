import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures
import math
import gc

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
fr=float(arg[10])
system=["Equilibrium","Total\;system"]
#Create the scale:
scaler=StandardScaler()
# It is proccesed the data for the PCA:
# All the points with different probability need to be examined separately:

# It is created the arrays to store the information

S=[0 for i in range(waw)]
P=np.array([pp+za*i for i in range(waw)])

xx=[i for i in range(int(L*t*fr))]
for yy in range(waw): #Loop over all diferent points 
    A=pd.read_csv("./graph8/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt",delim_whitespace=True,header=None,usecols=xx,skiprows=yy*N,nrows=N)
    scaler.fit(A)
    scaled_data=scaler.transform(A)
    del A
    gc.collect()
    pca=PCA()
    pca.fit(scaled_data)
    x_pca=pca.transform(scaled_data)
    sing=np.array(pca.singular_values_)
    norm=np.sum(sing**2)
    if norm==0:
        S[yy]=0
    else:
        sing=sing**2/norm
        sing=-sing*np.log(sing)
        S[yy]=np.sum(sing)/np.log(len(pca.singular_values_))
    

#It is plotted the entropy:
# We define the points were the derivative is calculated
# These points are approximately in the region 5900-6500
PI=6200
PF=6600
indexPI=0
indexPF=0
X=np.arange(PI,PF,1)

for ii in range(len(P)):
    if P[ii]<PI:
        indexPI=ii
    if P[ii]<PF:
        indexPF=ii
        
mymodel=np.poly1d(np.polyfit(P[indexPI:indexPF],S[indexPI:indexPF],smooth))
Y=mymodel(X)
DY=mymodel.deriv(m=1)
ds=DY(X)

plt.figure(figsize=(8,6))
plt.title(r"$S(p)\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$Entropy\;S(p)$",fontsize=14)
plt.scatter(P,S,label="Entropy")
plt.plot(P,S,color="black")
plt.plot(X,Y,color="red",label="interpolation")
plt.legend()
plt.savefig("./graph8/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"S.pdf")
write_text(np.array([P,S]),"./graph8/"+str(allsys)+"_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"S.aux"+str(fr))






#It is calculated the derivative of the entropy and it is plotted as well:
XX=[]
DS=[]
for ii in range(len(X)):
    if X[ii]>=6200 and X[ii]<=6600:
        XX.append(X[ii])
        DS.append(ds[ii])
        
write_text(np.array([XX,DS]),"./graph8/"+str(allsys)+"_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"DS.aux")













