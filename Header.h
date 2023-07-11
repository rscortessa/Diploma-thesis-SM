#include<iostream>
#include<vector>
#include<string>
#include<algorithm>
#include<iostream>
#include<fstream>
#include<random>
#include<omp.h>
#include<sstream>

#ifndef FUNCTIONS_H
#define FUNCTIONS_H
void count(std::vector<bool> &sys, std::vector<double>& b, int time,int m, int t);
std::vector<bool>  initcond(int L,std::mt19937& e2,int N);
int evolution(std::vector<bool> &sys,double p,std::uniform_real_distribution<double>& a, std::mt19937& a2, int L);
void print_state(std::vector<bool> &sys,std::stringstream &strings);
void print(std::vector<bool> &sys, std::ofstream& filename, int t);
void orderparameter(std::vector<double>& b,std::ofstream& filename, int t, int N);

#define DECLARE_VARIABLES\
    int L = std::stoi(std::string(argv[1]));\
    int t = std::stoi(std::string(argv[2]));\
    int pp = std::stoi(std::string(argv[3]));\
    int sites = std::stoi(std::string(argv[4]));\
    int N=std::stoi(std::string(argv[6]));\
    std::string dir=std::string(argv[7]);\
    double p=pp/(10000.0);\
    std::vector<bool> sys(L,0);\
    std::vector<bool> aux(L,0);\
    std::vector<double> rho(t*N,0);\

#define RANDOM\
  std::random_device rd;\
  std::mt19937 e2(rd());\
  std::uniform_real_distribution<double> dist0(0,1);\

#endif
