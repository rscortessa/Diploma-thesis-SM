#include<iostream>
#include<vector>
#include<string>
#include<algorithm>
#include<iostream>
#include<fstream>
#include<random>

int N; //repetitions

void initcond(std::vector<bool> &sys, bool s,std::mt19937& e2);
void evolution(std::vector<bool> &sys, double p, std::uniform_real_distribution<double>& a, std::mt19937& e2);
void print_state(std::vector<bool> &sys, std::ofstream& filename);
void print(std::vector<bool> &sys, std::ofstream& filename, int t);
void count(std::vector<bool> &sys, std::vector<double>& b, int t,int m);
void orderparameter(std::vector<double>& b,std::ofstream& filename, int t);

int main(int argc,char* argv[])
{
  int L=std::stoi(std::string(argv[1]));// Lattice sites
  int t=std::stoi(std::string(argv[2])); // time steps
  int pp=std::stoi(std::string(argv[3]));
  double p=pp/(1000.0); // Probability
  N=100;

  
  std::string name,name1,name2;

  name="DP_L"+std::to_string(L)+"T"+std::to_string(t)+"P"+std::to_string(pp)+".txt";
  name1="DP_L"+std::to_string(L)+"T"+std::to_string(t)+"P"+std::to_string(pp)+"data.txt";
  name2="DP_OP_L"+std::to_string(L)+"T"+std::to_string(t)+"P"+std::to_string(pp)+".txt";

  std::ofstream file(name), file1(name1), file2(name2);

  std::vector<bool> sys(L,0);  
  std::vector<double> rho(t*N,0);

  for(int l=0;l<N;l++)
    {
        
      std::random_device rd;
      std::mt19937 e2(rd());
      std::uniform_real_distribution<double> dist0(0,1);

      
      initcond(sys,0,e2);
      for(int j=0;j<t;j++)
	{
	  if(l==N-1)
	    {
	      print_state(sys,file);
	      print(sys,file1,j);
	    }	  
	  evolution(sys,p,dist0,e2);
	  count(sys,rho,j,l);
	}
    }
      orderparameter(rho,file2,t);
  
  
  return 0;
}


void initcond(std::vector<bool> &sys, bool s,std::mt19937& e2)
{
  
  if(s==0)
    {
      std::uniform_int_distribution<> dist1(0,1);
      generate(sys.begin(),sys.end(),[&]() {return dist1(e2);});
    }
  else
    {
      int a=sys.size()/2;
      sys[a]=1;
    }
}


void evolution(std::vector<bool> &sys,double p,std::uniform_real_distribution<double>& a, std::mt19937& e2)
{
  std::vector<bool> copy;
  bool c;
  bool d;
  copy=sys;
  for(int i=0;i<sys.size();i++)
    {
      c= (copy[i-1]==1 && a(e2)<=p);
      d= (copy[i+1]==1 && a(e2)<=p);
      sys[i]= (c || d);
    }
}


void print_state(std::vector<bool> &sys, std::ofstream& filename)
{
  auto finit = [&filename](const bool& a) { filename << a << " ";};
  std::for_each(sys.begin(),sys.end(),finit);
  filename <<"\n";
}


void print(std::vector<bool> &sys, std::ofstream& filename, int t)
{
  for(int j=0;j<sys.size();j++)
    {
      if(sys[j]==1)
	{
	  filename<<j<<" "<<t<<"\n";
	}
    }
}

void count(std::vector<bool> &sys, std::vector<double>& b, int t,int m)
{
  int a=0;
  for(int i=0;i<sys.size();i++)
    {
      a=a+sys[i];
    }
  //int a=std::accumulate(sys.begin(),sys.end(),0);
  b[m*N+t]=a/(sys.size()*1.0);
  std::cout<<b[m*N+t]<<std::endl;
}

void orderparameter(std::vector<double>& b,std::ofstream& filename, int t)
{
  std::vector<double> rho(t,0);
  std::vector<double> var(t,0);
  for(int i=0;i<N;i++)
    {
      for(int j=0;j<t;j++)
	{
	  rho[j]=rho[j]+b[i*N+j]/(N*1.0);
	}
    }
  
  for(int i=0;i<N;i++)
    {
      for(int j=0;j<t;j++)
	{
	  var[j]=var[j]+std::pow(b[i*N+j]-rho[j],2);
	  if(i==N-1)
	    {
	      var[j]=std::pow(var[j]/(N*(N-1)*1.0),0.5);
	      filename<<j<<" "<<rho[j]<<" "<<var[j]<<"\n";
	    }
	} 
    }
}
