#include <sstream>
#include <fstream>
#include <stdio.h>
#include <iostream>
#include <TMath.h>
#include <TH2F.h>
#include <TAxis.h>
#include <TApplication.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TGraph.h>
#include <TFile.h>
#include <TROOT.h>

using namespace std;
void GenerateTVectorshape(string namefile, vector<double>& x, vector<double>& y);

int main(int argc, char**argv)
{
  vector<double> x,y,x_new,y_new;
  string name=argv[1];
  
  GenerateTVectorshape(name,x,y);
  
  int start=150;
  int end=900;

  for(int i=start;i<=end;i=i+2)
  {
    x_new.push_back(i);
    if(i<x[0]) y_new.push_back(y[0]);
    else 
    {
      if(i>x[x.size()-1]) y_new.push_back(y[y.size()-1]);
      else
      {
        auto it=find(x.begin(),x.end(),i);
        if(it==x.end())
        {
          auto itabove = find_if(x.begin(),x.end(),[&](double x){return x>i;});
          int elabove= &*itabove - &*x.begin();
          double m=(y[elabove]-y[elabove-1])/(x[elabove]-x[elabove-1]);
          y_new.push_back(m*i-m*x[elabove]+y[elabove]);
        }
        else y_new.push_back(y[&*it-&*x.begin()]);
      } 
    }


    
  }

  ofstream scrivi("Outfile_res.txt",ios_base::trunc);
  for(int i=0;i<x_new.size();i++) scrivi<<x_new[i]<<"\t"<<y_new[i]<<endl;

  scrivi.flush();
  scrivi.close();

  return 0;
  
}

void GenerateTVectorshape(string namefile, vector<double>& x, vector<double>& y)
{
	ifstream leggi(namefile.c_str());
  double val;
  while(!leggi.eof())
	{
		leggi>>val;
    if(leggi.eof()) break;
    x.push_back(val);
    leggi>>val;
    y.push_back(val);
	}
	
	return;
}
