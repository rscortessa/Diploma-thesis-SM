#include"Header.h"

std::vector<bool>  initcond(int L,std::mt19937& e2,int N)
{
  int i=0;
  int aux=0;
  int element=0;
  std::vector<int> a(L,0);
  std::vector<bool> b(L,0);
  std::generate(a.begin(), a.end(), [i = 0]() mutable { return i++;});
  std::uniform_int_distribution<> dist1(0,L-1);

  if(N==1)
    {
      int er=L/2.0;
	b[er]=1;
      return b;
    }
  
  for(int i=0;i<N;i++)
    {
      aux=dist1(e2)%(L-i);
      element=a[aux];
      a.erase(a.begin()+aux);
      b[element]=1;
    }
  return b;
}


int evolution(std::vector<bool> &sys,double p,std::uniform_real_distribution<double>& a, std::mt19937& a2, int L)
{
  std::vector<bool> copy;
  int sum=0;
  copy=sys;
  bool c=0;
  bool d=0;
#pragma omp parallel for reduction(+:sum) private(c,d)
  for(int i=1;i<L+1;i++)
      {
	c= (copy[i-1]==1 && a(a2)<=p);
	d= (copy[(i+1)%L]==1 && a(a2)<=p);
	sys[i%L]= (c || d);
	sum=sum+sys[i%L];
      }
 
  return sum;
}


void print_state(std::vector<bool> &sys,std::stringstream &strings)
{
  auto finit = [&strings](const bool& a) { strings << a << " ";};
  std::for_each(sys.begin(),sys.end(),finit);
}


void print(std::vector<bool> &sys, std::ofstream& filename, int t)
{
  int size=sys.size();
  for(int j=0;j<size;j++)
    {
      if(sys[j]==1)
	{
	  filename<<j<<" "<<t<<"\n";
	}
    }
}

void count(std::vector<bool> &sys, std::vector<double>& b, int time,int m, int t)
{
  int a=0;
  int size=sys.size();
  for(int i=0;i<size;i++)
    {
      a=a+sys[i];
    }
  //int a=std::accumulate(sys.begin(),sys.end(),0);
  b[m*t+time]=a/(sys.size()*1.0);
}

void orderparameter(std::vector<double>& b,std::ofstream& filename, int t, int N)
{
  std::vector<double> rho(t,0);
  std::vector<double> var(t,0);
  for(int i=0;i<N;i++)
    {
      for(int j=0;j<t;j++)
	{
	  rho[j]=rho[j]+b[i*t+j]/(N*1.0);
	}
    }
  
  for(int i=0;i<N;i++)
    {
      for(int j=0;j<t;j++)
	{
	  var[j]=var[j]+std::pow(b[i*t+j]-rho[j],2);
	  if(i==N-1)
	    {
	      var[j]=std::pow(var[j]/(N*(N-1)*1.0),0.5);
	      filename<<j<<" "<<rho[j]<<" "<<var[j]<<"\n";
	    }
	} 
    }
}
