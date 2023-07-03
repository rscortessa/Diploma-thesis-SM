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

Id_PCA=[0 for jj in range(waw)]
P=np.array([pp+za*i for i in range(waw)])


for yy in range(waw): #Loop over all diferent points 
    A=pd.read_csv("./graph9/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt",delim_whitespace=True,header=None,skiprows=yy*N,nrows=N)
    scaler.fit(A)
    scaled_data=scaler.transform(A)
    pca=PCA()
    pca.fit(scaled_data)
    x_pca=pca.transform(scaled_data)
    sing=np.array(pca.singular_values_)
    sing=sing**2/(np.sum(sing**2))
    Id_PCA[yy]=pca.n_features_in_

#It is plotted the Id_PCA:
X=np.arange(P[0],P[len(P)-1],za/1000)
mymodel=np.poly1d(np.polyfit(P,Id_PCA,smooth))
Y=mymodel(X)
DY=mymodel.deriv(m=1)
ds=DY(X)

plt.figure(figsize=(8,6))
plt.title(r"$S(p)\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$Intrinsic\;dimension\;Id(p)$",fontsize=14)
plt.scatter(P,Id_PCA,label="Entropy")
plt.plot(P,Id_PCA,color="black")
plt.plot(X,Y,color="red",label="interpolation")
plt.legend()
plt.savefig("./graph9/"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"Id.pdf")
write_text(np.array([P,Id_PCA]),"./graph9/"+str(allsys)+"_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"Id.aux")






#It is calculated the derivative of the entropy and it is plotted as well:
XX=[]
DS=[]
for ii in range(len(X)):
    if X[ii]>=6200 and X[ii]<=6600:
        XX.append(X[ii])
        DS.append(ds[ii])
        
write_text(np.array([XX,DS]),"./graph9/"+str(allsys)+"_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"DId.aux")













