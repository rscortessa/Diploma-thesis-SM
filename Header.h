#include<iostream>
#include<vector>
#include<string>
#include<algorithm>
#include<iostream>
#include<fstream>
#include<random>

#ifndef FUNCTIONS_H
#define FUNCTIONS_H
void count(std::vector<bool> &sys, std::vector<double>& b, int time,int m, int t);
std::vector<bool>  initcond(int L,std::mt19937& e2,int N);
void evolution(std::vector<bool> &sys,double p,std::uniform_real_distribution<double>& a, std::mt19937& e2);
void print_state(std::vector<bool> &sys, std::ofstream& filename);
void print(std::vector<bool> &sys, std::ofstream& filename, int t);
void orderparameter(std::vector<double>& b,std::ofstream& filename, int t, int N);
#endif
