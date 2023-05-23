#include"Header.h"

//This file creates the evolution for the Bond percolation system, it is specified the time t,
//the lattice sites L and the probability p.

int main(int argc,char* argv[])
{
  int L=std::stoi(std::string(argv[1]));// Lattice sites
  int t=std::stoi(std::string(argv[2])); // time steps
  int pp=std::stoi(std::string(argv[3])); // probability*(10000) 
  int sites=std::stoi(std::string(argv[4])); // Initial Active sites
  double p=pp/(10000.0); // Probability
  int N=1000; // Number of repetitions
  
  
  std::string name,name1,name2;

  name="DP_L"+std::to_string(L)+"T"+std::to_string(t)+"P"+std::to_string(pp)+"S"+std::to_string(sites)+".txt";
  name1="DP_L"+std::to_string(L)+"T"+std::to_string(t)+"P"+std::to_string(pp)+"S"+std::to_string(sites)+"data.txt";
  name2="DP_OP_L"+std::to_string(L)+"T"+std::to_string(t)+"P"+std::to_string(pp)+"S"+std::to_string(sites)+".txt";

  std::ofstream file(name), file1(name1), file2(name2);


  std::vector<bool> sys(L,0);  
  std::vector<bool> aux(L,0);
  std::vector<double> rho(t*N,0);

  std::random_device rd;
  std::mt19937 e2(rd());
  std::uniform_real_distribution<double> dist0(0,1);      

  aux=initcond(L,e2,sites);
  
  for(int l=0;l<N;l++)
    {
        
      std::random_device rd;
      std::mt19937 e2(rd());
      std::uniform_real_distribution<double> dist0(0,1);      
      sys=aux;
      for(int j=0;j<t;j++)
	{
	  if(l==N-1)
	    {
	      print_state(sys,file);
	      print(sys,file1,j);
	    }
	  count(sys,rho,j,l,t);
	  evolution(sys,p,dist0,e2);
	  
	}
    }
      
      orderparameter(rho,file2,t,N);
  
  
  return 0;
}

