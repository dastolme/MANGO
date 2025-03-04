//CALL: ./progname.exe <path to file>

#include <iostream>
#include <unistd.h>
#include <limits.h>
#include <sstream>
#include <fstream>
#include <chrono>
#include <string>
#include <numeric>
#include <algorithm>
#include <cmath>
#include <stdio.h>
#include <cstdlib>
#include <filesystem>
#include "TRandom3.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
#include "TH2.h"

using namespace std;

void ScIndicesElem(int nSc, UInt_t npix, float* sc_redpixID, int &nSc_red, vector<int>& B, vector<int>& E);

int main(int argc, char** argv)
{
    if(argc<2) {cerr<<"No file path!\nSuggested use: ./progname.exe <path to file"; exit(EXIT_FAILURE);}
    string nome=argv[1];

    TFile* f = TFile::Open(Form("%s",nome.c_str()),"READ");
    TTree* tree = (TTree*)f->Get("Events");

    //define variables required
    unsigned int nSc=0;
    int nSc_red=0;
    UInt_t Nredpix=0;
    int run;
    int event;

    int nmax=500000;
    int nscmax=100;
    vector<float> sc_redpixID;
    sc_redpixID.reserve(nmax);
    vector<int> XPix;
    XPix.reserve(nmax);
    vector<int> YPix;
    YPix.reserve(nmax);
    vector<float> ZPix;
    ZPix.reserve(nmax);
    vector<float> xmean;
    xmean.reserve(nscmax);
    vector<float> ymean;
    ymean.reserve(nscmax);
    vector<float> width;
    width.reserve(nscmax);
    vector<float> length;
    length.reserve(nscmax);
    vector<float> integral;
    integral.reserve(nscmax);

    //Link the variables to the tree branches
    tree->SetBranchAddress("run",&run);
    tree->SetBranchAddress("event",&event); 
    /////////////Reco variables//////////////     
    tree->SetBranchAddress("nSc",&nSc);
    tree->SetBranchAddress("sc_redpixIdx",sc_redpixID.data());
    tree->SetBranchAddress("nRedpix",&Nredpix);
    tree->SetBranchAddress("redpix_ix",XPix.data());
    tree->SetBranchAddress("redpix_iy",YPix.data());
    tree->SetBranchAddress("redpix_iz",ZPix.data());
    tree->SetBranchAddress("sc_width",width.data());
    tree->SetBranchAddress("sc_length",length.data());
    tree->SetBranchAddress("sc_integral",integral.data());
    tree->SetBranchAddress("sc_xmean",xmean.data());
    tree->SetBranchAddress("sc_ymean",ymean.data());

    /////////////////////////////////Analysis Variables ////////////////////////////////////////////////
    vector<int> BeginScPix;
    vector<int> EndScPix;

    /////////////////////////////////Histograms/////////////////////////////////////////////////////////
    int nbinsx=4096;
    int nbinsy=2304;
    TH2F* hmap_occu = new TH2F("hmap_occu","hmap_occu",nbinsx,0,nbinsx,nbinsy,0,nbinsy);
    TH2F* hmap_intensity = new TH2F("hmap_intensity","hmap_intensity",nbinsx,0,nbinsx,nbinsy,0,nbinsy);
    TH2F* hmap_5_9keV = new TH2F("hmap_5_9keV","hmap_5_9keV",nbinsx,0,nbinsx,nbinsy,0,nbinsy);

    
    TFile *fout = TFile::Open(Form("map.root"),"RECREATE");

    //Cycle on events
    cout<<"this run has "<<tree->GetEntries()<<" entries"<<endl;
    for(int k=0;k<tree->GetEntries();k++)
    {
        
        tree->GetEntry(k);
        if(k%500==0) {cout<<"getting entries..."<<endl; cout << "Nev: "<< k << "\nnSc:  " << nSc <<endl;}
        //for reduced pixels:
        ScIndicesElem(nSc,Nredpix,sc_redpixID.data(),nSc_red,BeginScPix,EndScPix);

        for(int clu=0;clu<nSc;clu++)
        {
            if(k%500==0 && clu%20==0) cout<<"Cluster "<< clu << " integral "<<integral[clu]<<endl;         

            if(sc_redpixID[clu]!=-1)
            {
                bool cut1= (integral[clu]>1100 && integral[clu]<660000);       //remove below 0.25 eV (clear noise) and above 300 keV (no need for alphas). In GIN a muon travelling 150 cm leaves about 300 keV
                bool cut2= (xmean[clu]>2000 && xmean[clu]<2060 && ymean[clu]>1700 && ymean[clu]<1880 && width[clu]/length[clu]>0.38 && width[clu]/length[clu]<0.5);  //Remove noisy hotspot side of GEM
                bool cut3= (xmean[clu]>620 && xmean[clu]<640 && ymean[clu]>1750 && ymean[clu]<1770);  //Remove hotspot 
                if(cut1 && !cut2 && !cut3)
                {
                    for(int pix=BeginScPix[clu];pix<EndScPix[clu];pix++)
                    {
                        hmap_occu->Fill(XPix[pix],YPix[pix]);
                        if(ZPix[pix]>1)  hmap_intensity->Fill(XPix[pix],YPix[pix],ZPix[pix]);
                    }
                    if(integral[clu]>11000 && integral[clu]<20000)  
                    {
                        for(int pix=BeginScPix[clu];pix<EndScPix[clu];pix++)
                        {
                           if(ZPix[pix]>0) hmap_5_9keV->Fill(XPix[pix],YPix[pix],ZPix[pix]);
                        }     
                    }
                }
            }
            
        }
        //CAREFUL: In theory the following operations (resize and clear) should be performed on every vector. This because we are writing the arrays forcefully inside the vector but the vector "doesn't know".
        //As the cycles are now though we always stop the cycles to nSc and not to size() (which does not work as the vector thinks it has size 0), so it works without
        //integral.resize(nSc);
        //integral.clear();

    }

    for(int i=1;i<nbinsx;i++)
    {
        for(int j=1;j<nbinsy;j++)
        {
            if(hmap_occu->GetBinContent(i,j)!=0)
            {
                if(hmap_occu->GetBinContent(i,j)<10)  hmap_intensity->SetBinContent(i,j,0);
                else  hmap_intensity->SetBinContent(i,j,hmap_intensity->GetBinContent(i,j)/hmap_occu->GetBinContent(i,j));
            }   
        }
    }

    hmap_occu->Write();
    hmap_intensity->Write();
    hmap_5_9keV->Write();
    fout->Flush();
    fout->Close();
    f->Close();

    return 0;
}

//Functions
void ScIndicesElem(int nSc, UInt_t npix, float* sc_redpixID, int &nSc_red, vector<int>& B, vector<int>& E)
{
  B.clear();
  E.clear();

  vector<float> sc_redpix_start;

  int parcount=0;

  for(int i=0; i<nSc; i++){
    if(sc_redpixID[i]>=0)  sc_redpix_start.push_back(sc_redpixID[i]);
  }

  nSc_red = sc_redpix_start.size();

  sc_redpix_start.push_back(npix);

  for(int i=0;i<sc_redpix_start.size()-1;i++){
    B.push_back(sc_redpix_start[i]);
    E.push_back(sc_redpix_start[i+1]);
    //std::cout<<B[i]<<" "<<E[i]<<endl;
  }

  sc_redpix_start.clear();

  return;

}