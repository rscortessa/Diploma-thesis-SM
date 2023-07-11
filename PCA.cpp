#include"Header.h"

//This file creates the evolution for the Bond percolation system, it is specified the time t,
//the lattice sites L and the probability p.




int main(int argc,char* argv[])
{
  DECLARE_VARIABLES // All the variables are declared    
  RANDOM // The random distribution function from 0 to 1 is declared 
  aux=initcond(L,e2,sites); // Initialize the first srtup 
  int M=std::stoi(std::string(argv[5])); // How much the probability increases in total x 10.000
  int pstep=stoi(std::string(argv[8])); // How much the probability increases for each step x 10.000
  double dp=pstep*1.0/(10000);    
  bool totalsystem=std::stoi(std::string(argv[9]));
  int Numberpics=1;
  
  std::string name;
  name=dir+"DP_L"+std::to_string(L)+"T"+std::to_string(t)+"P("+std::to_string(pp)+"-"+std::to_string(pp+M)+")"+"S"+std::to_string(sites)+".txt";
  std::ofstream file(name);
     
  
  if(totalsystem==true)
    {
      
      for(int w=0;w<M/pstep;w++)
	{
          #pragma omp parallel for private(sys)
	  for(int l=0;l<N;l++) // for between different samples
	    {
	      RANDOM
	      std::stringstream strings;
	      // initialize the distribution with a different seed
	      sys=aux; // The initial setup is always the same 
	      for(int j=0;j<t;j++)
		{
		  evolution(sys,p+dp*w,dist0,e2,L); // Evolves the system
		  print_state(sys,strings);
		}
	      #pragma omp critical
	      {
	      file<<strings.str()<<"\n";
	      }
	    }
	  
	}
    }

  else
    {
      for(int w=0;w<M/pstep;w++)
	{
	  #pragma omp parallel for private(sys)
	  for(int l=0;l<N;l++) // for between different samples
	    {
	      RANDOM // initialize the distribution with a different seed
	      sys=aux; // The initial setup is always the same 
	      std::stringstream strings;
	      for(int j=0;j<t-Numberpics;j++)
		{
		  if(evolution(sys,p+dp*w,dist0,e2,L)==0) // Evolves the system implicit in an if.
		    {
		      j=t-Numberpics-1;
		    }
		}
	      
	      for(int j=t-Numberpics;j<t;j++)
		{
		  evolution(sys,p+dp*w,dist0,e2,L); // Evolves the system
		  print_state(sys,strings);
		}

	      #pragma omp critical
	      {
	      file<<strings.str()+"\n";
	      }
	    }    
	}

    }
  
  return 0;
}

