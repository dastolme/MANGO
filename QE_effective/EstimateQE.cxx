#include <sstream>
#include <fstream>
#include <stdio.h>
#include <iostream>
#include <algorithm>
#include <numeric>
#include <map>
#include <TH2F.h>
#include <TAxis.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TGraph.h>
#include <TFile.h>

using namespace std;
void GenerateTVectorshape(string namefile, vector<double>& x, vector<double>& y);
void Styleup(shared_ptr<TGraph> & g,string title, int color, int marker, int linestyle, int linewidth);
void ReadConfig(string name, map<string,string>& options);

int main(int argc, char**argv)
{
  if(argc!=2)
  {
    cerr<<"Error in input! Usage ./progname configfile\n";
    exit(EXIT_FAILURE);
  }

  string name=argv[1];

  map<string,string> options;
  ReadConfig(name,options);	

  vector<double> wavelength, emission_spectr_norm, emission_spectr, trans_window, optical_device, received_emission, trash;

  double transmission_lens;
  if(options["Detector"].find("PMT")!= string::npos) transmission_lens=1.;
  else transmission_lens=0.90;

  double ph_e_reg_norm=0.113;    //photons per secondary electron in the whole He:CF4 spectrum at 10000 mbar 60/40 mixture (it is 0.07 above about 320)

  GenerateTVectorshape("Spectra/He_CF4_1000.txt",wavelength,emission_spectr_norm);

  string BASE="Spectra";
  string filename=BASE+"/"+ options["Gas"] +"_"+ options["Pressure"] +".txt";
  GenerateTVectorshape(filename,wavelength,emission_spectr);

  filename = BASE+"/"+ options["Window"] +"_trans.txt";
  GenerateTVectorshape(filename,trash,trans_window);
  trash.clear();

  filename = BASE+"/"+ options["Detector"] +".txt";
  GenerateTVectorshape(filename,trash,optical_device);

  //normalise the emission spectra to 100%
  double areanorm=accumulate(emission_spectr_norm.begin(), emission_spectr_norm.end(),0.); //This area is normalisable to 0.113 ph/e
  double area=accumulate(emission_spectr.begin(), emission_spectr.end(),0.);
  transform(emission_spectr.begin(), emission_spectr.end(),emission_spectr.begin(),[&](double x){return x/area;});
  
  //Now multiply bin by bin the emission by the various transparencies and obtain the relative received spectrum
  for(int i=0;i<emission_spectr.size();i++)
  {
    received_emission.push_back(emission_spectr[i]*transmission_lens*trans_window[i]*optical_device[i]/10000.);   //divide by 100 to have the two contribution from mylar and opticaldevice in decimal percentage (like 0.5) 
  }

  double eff_QE=accumulate(received_emission.begin(),received_emission.end(),0.); 

  cout<<"Photons per secondary e with this gas "<<ph_e_reg_norm*area/areanorm<<endl;
  cout<<"Effective QE with "<<options["Detector"]<<" and "<<options["Window"]<<" window is "<<eff_QE*100<<"%"<<endl; //multiply by 100 to have the efficiency expressed like 50%
  cout<<"Total photons collected per secondary electron by "<<options["Detector"]<<" "<<eff_QE*ph_e_reg_norm*area/areanorm<<endl;

  if(options["Detector"]=="PMT_bialkali_borosilicate") options["Detector"]="PMTbi";
  filename="Effspec_"+options["Gas"]+"_"+options["Pressure"]+"_"+options["Detector"]+"_"+options["Window"]+".root";
  //auto file=shared_ptr<TFile> {TFile::Open("Pos_Oxide.root","RECREATE")};
  auto rf= shared_ptr<TFile> {TFile::Open(filename.c_str(),"RECREATE")};
  auto g1= make_shared<TGraph>(emission_spectr.size(),wavelength.data(),emission_spectr.data());
  auto g2= make_shared<TGraph>(received_emission.size(),wavelength.data(),received_emission.data());
  
  auto c1=make_shared<TCanvas>(filename.c_str(),"c1");
  Styleup(g1,";Wavelength (nm);Spectrum",kBlue,1,1,1);
  Styleup(g2,";Wavelength (nm);Spectrum",kRed,1,1,1);
  g1->Draw("apl");
  g2->Draw("samepl");

  c1->Write();

  return 0;
}

void GenerateTVectorshape(string namefile, vector<double>& x, vector<double>& y)
{
	ifstream leggi(namefile.c_str());
  if(leggi.fail())
  {
    cerr<<"File "+namefile+" does not exist\n";
    exit(EXIT_FAILURE);
  }
  double val;
  while(!leggi.eof())
	{
		leggi>>val;
    if(leggi.eof()) break;
    x.push_back(val);
    leggi>>val;
    if(val<0) val=0;
    y.push_back(val);
	}
	
	return;
}

void Styleup(shared_ptr<TGraph> & g, string title, int color, int marker, int linestyle, int linewidth)
{
  g->SetLineColor(color);
	g->SetLineStyle(linestyle);
	g->SetMarkerStyle(marker);
	g->SetMarkerColor(color);
	g->SetLineWidth(linewidth);
	
  g->GetXaxis()->SetLimits(150,1000);				
  g->GetYaxis()->SetRangeUser(0,0.02);		
  g->GetYaxis()->SetTitleSize(0.05);
  g->GetYaxis()->SetLabelSize(0.05);
  g->GetXaxis()->SetTitleSize(0.05);
  g->GetXaxis()->SetLabelSize(0.05);
  g->SetTitle(title.c_str());
  g->GetYaxis()->SetTitleOffset(1.00);

return;
}

void ReadConfigTooeasy(string name, map<string,string>& options)
{
    ifstream config(name.c_str());

    string index;
    string val;
    while(!config.eof())
    {
      config>>index;
      if(config.eof()) break;
      config>>val;
      options[index]=val;
    }
	
}

void ReadConfig(string name, map<string,string>& options)
{
    ifstream config(name.c_str());
	
    string line;
    while(getline(config,line))
    {
        line.erase(remove_if(line.begin(),line.end(),[] (char c){return isspace(c);}),line.end());
        line.erase(remove_if(line.begin(),line.end(),[] (char c){return c=='\'';}),line.end());
        if(line[0] == '#' || line.empty() || line[0] == '{' || line[0] == '}') continue;
		
        auto delim1= line.find(":");
        auto delim2= line.find(",");
        if(delim2==string::npos) delim2=line.size();
        auto index= line.substr(0,delim1);
        auto val= line.substr(delim1+1,min(delim2,line.size())-delim1-1 );
        options[index]=val;
    }
	
}