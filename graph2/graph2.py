
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

print(len(sys.argv))
L=int(sys.argv[1])
t=int(sys.argv[2])
p=int(sys.argv[3])

def LinearR2(col_1, col_2):
    col_1 = sm.add_constant(col_1)
    model = sm.OLS(col_2, col_1)
    results = model.fit()
    COEF = [results.params[0], results.bse[0], results.params[1], results.bse[1],results.rsquared]
    COEF =  np.array(COEF)
    return COEF

S=["$S="+sys.argv[4]+"$","$S="+sys.argv[5]+"$","$S="+sys.argv[6]+"$","$S="+sys.argv[7]+"$","$S="+sys.argv[8]+"$"]


plt.figure(figsize=(10,5))
plt.title("$Directed\; Percolation\; in\; (1+1)\; dimensions$ \n"+"$\;L="+str(L)+"\;t="+str(t)+"$",fontsize=15)
plt.xlabel(r"$time$",fontsize=15)
plt.ylabel(r"$\rho(t)$",fontsize=15)
plt.xscale("log")
plt.yscale("log")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#plt.ylim([0.1,1])
for i in range(5):
    B=pd.read_csv("./graph2/DP_OP_L"+sys.argv[1]+"T"+sys.argv[2]+"P"+sys.argv[3]+"S"+sys.argv[4+i]+".txt",delim_whitespace=True,header=None)
    eps=B[0]
    zet=B[1]
    iot=B[2]
    plt.errorbar(eps,zet,yerr=iot,label=r"$\rho(t)$"+" "+S[i])
    if i==4:
        x=np.array(eps[1:]).reshape((-1,1))
        zet=np.array(zet)
        Result=LinearR2(np.log(x),np.log(zet[1:]))
        plt.plot(x,np.e**(Result[0])*x**(Result[2]),label=r"$\rho=A*t^{\delta}$"+"\n" +"$\delta="+str(round(Result[2],3))+"\pm"+str(round(Result[3],5))+"$")
plt.legend(fontsize=12,bbox_to_anchor=(1.1,0.7))
plt.tight_layout()
plt.savefig("./graph2/graph2.png")
