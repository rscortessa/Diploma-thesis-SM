# Diploma-thesis-SM

> This is a first README, there are two files: DP.cpp, plot.py

> In order to execute the program and create the graphs use the command: make graphs
> it can be specified the length of the system L, the time t and the probability p for the evolution rule of the system.
> for example make L=100 pp=899 t=100 with executes the program with a length 100, time steps 100 and probability =0.899.

## DP.cpp
> The first file contains all the functions related to the dynamics of the model. 
> There are three files after its execution: 
> The first file contains all the information about the instantaneous states of the model: the rows indicate the position in time and the columns in the space.
> The second file contains the information of the active sites of the entire evolution specifying two coordinates (x,t). 
> The third file contains the evolution of the order parameter with time, the variables are organized as it follows: (t,p(t),error).
# plot.py
> plot.py plots the state of the system after t iterations and computes the evolution of p(t).
