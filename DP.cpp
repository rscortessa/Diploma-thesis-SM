#include"Header.h"

//This file creates the evolution for the Bond percolation system, it is specified the time t,
//the lattice sites L and the probability p.




int main(int argc,char* argv[])
{
  DECLARE_VARIABLES // All the variables are declared    
  RANDOM // The random distribution function from 0 to 1 is declared 
  std::string name1,name2;
  name1=dir+"DP_L"+std::to_string(L)+"T"+std::to_string(t)+"P"+std::to_string(pp)+"S"+std::to_string(sites)+"data.txt";
  name2=dir+"DP_OP_L"+std::to_string(L)+"T"+std::to_string(t)+"P"+std::to_string(pp)+"S"+std::to_string(sites)+".txt";
  std::ofstream file1(name1), file2(name2);
  
  aux=initcond(L,e2,sites); // Initialize the first srtup 
  for(int l=0;l<N;l++) // for between different samples
    {
      RANDOM // initialize the distribution with a different seed
      sys=aux; // The initial setup is always the same 
      for(int j=0;j<t;j++)
	{
	  if(l==N-1) // The last sample is printed
	    {
	      print(sys,file1,j); // This prints to file1 the positions in space and time of the active sites
	    }
	  count(sys,rho,j,l,t); // Counts the number of active sites per time
	  evolution(sys,p,dist0,e2,L); // Evolves the system
	}
    }
      orderparameter(rho,file2,t,N); // prints to a file the density of active sites
  
  return 0;
}

