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
#include <TGraphErrors.h>
#include <TFile.h>

using namespace std;
void GenerateTVectorshape(string namefile, vector<double>& x, vector<double>& y);
template <typename T> void Styleup(shared_ptr<T> & g,string title, int color, int marker, int linestyle, int linewidth, double xmin=0, double xmax=5, double ymin=0, double ymax=5);
void ReadConfig(string name, map<string,string>& options);

int main(int argc, char**argv)
{

  vector<double> mass, xsection, xsection_HFO1, xsection_HFO2, xsection_H2O, xsection_SD, xsection_HFO1_SD, xsection_HFO2_SD, xsection_H2O_SD, mass_area, area_plot, mass_area_SD, area_plot_SD, trash;

  GenerateTVectorshape("Limits/SI/TableLim_HFO0.tsv",mass,xsection);
  GenerateTVectorshape("Limits/SI/TableLim_HFO1.tsv",trash,xsection_HFO1);
  GenerateTVectorshape("Limits/SI/TableLim_HFO2_5.tsv",trash,xsection_HFO2);
  GenerateTVectorshape("Limits/SI/TableLim_H2O_2permill.tsv",trash,xsection_H2O);
  GenerateTVectorshape("Limits/SD/TableLim_HFO0.tsv",trash,xsection_SD);
  GenerateTVectorshape("Limits/SD/TableLim_HFO1.tsv",trash,xsection_HFO1_SD);
  GenerateTVectorshape("Limits/SD/TableLim_HFO2_5.tsv",trash,xsection_HFO2_SD);
  GenerateTVectorshape("Limits/SD/TableLim_H2O_2permill.tsv",trash,xsection_H2O_SD);
  //for color area plot
  GenerateTVectorshape("Limits/SI/TableLim_HFO0.tsv",mass_area,area_plot);
  GenerateTVectorshape("Limits/SI/TableLim_HFO1.tsv",mass_area,area_plot);
  GenerateTVectorshape("Limits/SD/TableLim_HFO0.tsv",mass_area_SD,area_plot_SD);
  GenerateTVectorshape("Limits/SD/TableLim_HFO1.tsv",mass_area_SD,area_plot_SD);

  mass_area.erase(std::remove_if(mass_area.begin(), mass_area.end(), [&](const double& x) {
    return area_plot[&x-&*mass_area.begin()] > 9.9e-31;}), mass_area.end());
  mass_area_SD.erase(std::remove_if(mass_area_SD.begin(), mass_area_SD.end(), [&](const double& x) {
    return area_plot_SD[&x-&*mass_area_SD.begin()] > 9.9e-31;}), mass_area_SD.end());
  area_plot.erase(std::remove_if(area_plot.begin(), area_plot.end(), [&](const double& x) {
    return area_plot[&x-&*area_plot.begin()] > 9.9e-31;}), area_plot.end());
  area_plot_SD.erase(std::remove_if(area_plot_SD.begin(), area_plot_SD.end(), [&](const double& x) {
      return area_plot_SD[&x-&*area_plot_SD.begin()] > 9.9e-31;}), area_plot_SD.end());

  //Limit plot
  auto g_HFO0_SI= make_shared<TGraph>(mass.size(),mass.data(),xsection.data());
  auto g_HFO1_SI= make_shared<TGraph>(mass.size(),mass.data(),xsection_HFO1.data());
  auto g_HFO2_SI= make_shared<TGraph>(mass.size(),mass.data(),xsection_HFO2.data());
  auto g_H2O_SI= make_shared<TGraph>(mass.size(),mass.data(),xsection_H2O.data());
  auto g_HFO0_SD= make_shared<TGraph>(mass.size(),mass.data(),xsection_SD.data());
  auto g_HFO1_SD= make_shared<TGraph>(mass.size(),mass.data(),xsection_HFO1_SD.data());
  auto g_HFO2_SD= make_shared<TGraph>(mass.size(),mass.data(),xsection_HFO2_SD.data());
  auto g_H2O_SD= make_shared<TGraph>(mass.size(),mass.data(),xsection_H2O_SD.data());
  auto g_area= make_shared<TGraph>(mass_area.size(),mass_area.data(),area_plot.data());
  auto g_area_SD= make_shared<TGraph>(mass_area_SD.size(),mass_area_SD.data(),area_plot_SD.data());
  Styleup<TGraph>(g_HFO0_SI,"He:CF4;DM Mass (GeV/c^{2});SI cross section (cm^{2})",kBlack,1,1,2, 0.2,500,1e-48,5e-31);
  Styleup<TGraph>(g_HFO1_SI,"He:CF4:HFO  1%",kBlue,1,1,2);
  Styleup<TGraph>(g_HFO2_SI,"He:CF4:HFO  2.5%",kRed,1,1,2);
  Styleup<TGraph>(g_H2O_SI,"He:CF4:H2O  0.2%",kMagenta,1,1,2);
  Styleup<TGraph>(g_HFO0_SD,"He:CF4;DM Mass (GeV/c^{2});SD proton-cross section (cm^{2})",kBlack,1,1,2,0.2,500,1e-48,5e-31);
  Styleup<TGraph>(g_HFO1_SD,"He:CF4:HFO  1%",kBlue,1,1,2);
  Styleup<TGraph>(g_HFO2_SD,"He:CF4:HFO  2.5%",kRed,1,1,2);
  Styleup<TGraph>(g_H2O_SD,"He:CF4:H2O  0.2%",kMagenta,1,1,2);
  Styleup<TGraph>(g_area,"Area diff",kYellow-8,1,1,1);
  Styleup<TGraph>(g_area_SD,"Area diff",kYellow-8,1,1,1);
  g_area->SetFillColor(kYellow-8);
  g_area_SD->SetFillColor(kYellow-8);
  g_area_SD->SetFillColorAlpha(kYellow-8, 0.15);

  auto rf=shared_ptr<TFile> {TFile::Open("Limits_file.root", "RECREATE")};
  auto c1=make_shared<TCanvas>("Limits_SI","Limits_SI");
  c1->SetLogy();
  c1->SetLogx();
  c1->SetGridx();
  c1->SetGridy();
  g_HFO0_SI->Draw("al");
  g_HFO1_SI->Draw("samel");
  g_HFO2_SI->Draw("samel");
  g_H2O_SI->Draw("samel");
  //g_area->Draw("sameLF2");
  char name[50];
  TLegend* fleg0=new TLegend(0.6,0.9,0.9,0.65);
  sprintf(name,"He:CF4");
  fleg0->AddEntry(g_HFO0_SI->GetName(),name,"l");
  sprintf(name,"He:CF4:HFO 1%");
  fleg0->AddEntry(g_HFO1_SI->GetName(),name,"l");
  sprintf(name,"He:CF4:HFO 2.5%");
  fleg0->AddEntry(g_HFO2_SI->GetName(),name,"l");
  sprintf(name,"He:CF4:H2O 0.2%");
  fleg0->AddEntry(g_H2O_SI->GetName(),name,"l");
  fleg0->Draw("SAME");
  c1->Write();

  auto c2=make_shared<TCanvas>("Limits_SD","Limits_SD");
  c2->SetLogy();
  c2->SetLogx();
  c2->SetGridx();
  c2->SetGridy();
  g_HFO0_SD->Draw("al");
  g_HFO1_SD->Draw("samel");
  g_HFO2_SD->Draw("samel");
  g_H2O_SD->Draw("samel");
  //g_area_SD->Draw("sameLF2");
  TLegend* fleg1=new TLegend(0.6,0.9,0.9,0.65);
  sprintf(name,"He:CF4");
  fleg1->AddEntry(g_HFO0_SD->GetName(),name,"l");
  sprintf(name,"He:CF4:HFO 1%");
  fleg1->AddEntry(g_HFO1_SD->GetName(),name,"l");
  sprintf(name,"He:CF4:HFO 2.5%");
  fleg1->AddEntry(g_HFO2_SD->GetName(),name,"l");
  sprintf(name,"He:CF4:H2O 0.2%");
  fleg1->AddEntry(g_H2O_SD->GetName(),name,"l");
  fleg1->Draw("SAME");
  c2->Write();

  ///////////Now analysis on area
  vector<double> HFOperc({1,2.5});
  vector<double> H2Operc({0.2});
  vector<double> HFOpercThr({0,1,2.5});
  vector<double> Thresholds({0.5,1.12,4.45});
  vector<double> extraarea, extraareaH2O, extraarea_SD, extraareaH2O_SD, extraarea_1GeV, extraareaH2O_1GeV, extraarea_SD_1GeV, extraareaH2O_SD_1GeV;
  double sum_HF1=0.;
  double sum_HF2=0.;
  double sum_H2O=0.;
  double sum_HF1_SD=0.;
  double sum_HF2_SD=0.;
  double sum_H2O_SD=0.;
  double sum_HF1_1GeV=0.;
  double sum_HF2_1GeV=0.;
  double sum_H2O_1GeV=0.;
  double sum_HF1_SD_1GeV=0.;
  double sum_HF2_SD_1GeV=0.;
  double sum_H2O_SD_1GeV=0.;

  double maxlim=1e-30;
  double mass1= 1;  //1 GeV
  auto itabove = find_if(mass.begin(),mass.end(),[&](double x){return x>mass1;});
  int elabove= &*itabove - &*mass.begin();

  for(int i=1;i<xsection.size();i++)
  {
    double deltam=log10(mass[i])-log10(mass[i-1]);
    sum_HF1+=deltam * (log10(xsection[i])-log10(xsection_HFO1[i]));
    sum_HF2+=deltam * (log10(xsection[i])-log10(xsection_HFO2[i]));
    sum_H2O+=deltam * (log10(xsection[i])-log10(xsection_H2O[i]));

    sum_HF1_SD+=deltam * (log10(xsection_SD[i])-log10(xsection_HFO1_SD[i]));
    sum_HF2_SD+=deltam * (log10(xsection_SD[i])-log10(xsection_HFO2_SD[i]));
    sum_H2O_SD+=deltam * (log10(xsection_SD[i])-log10(xsection_H2O_SD[i]));

    if(i==elabove)
    {
      sum_HF1_1GeV=sum_HF1;
      sum_HF2_1GeV=sum_HF2;
      sum_H2O_1GeV=sum_H2O;
      sum_HF1_SD_1GeV=sum_HF1_SD;
      sum_HF2_SD_1GeV=sum_HF2_SD;
      sum_H2O_SD_1GeV=sum_H2O_SD;
    }  
  }

  extraarea.push_back(sum_HF1);
  extraarea.push_back(sum_HF2);
  extraareaH2O.push_back(sum_H2O);
  extraarea_SD.push_back(sum_HF1_SD);
  extraarea_SD.push_back(sum_HF2_SD);
  extraareaH2O_SD.push_back(sum_H2O_SD);
  extraarea_1GeV.push_back(sum_HF1_1GeV);
  extraarea_1GeV.push_back(sum_HF2_1GeV);
  extraareaH2O_1GeV.push_back(sum_H2O_1GeV);
  extraarea_SD_1GeV.push_back(sum_HF1_SD_1GeV);
  extraarea_SD_1GeV.push_back(sum_HF2_SD_1GeV);
  extraareaH2O_SD_1GeV.push_back(sum_H2O_SD_1GeV);

  //GenerateTGraph
  auto g_ar_HFO=make_shared<TGraph>(HFOperc.size(),HFOperc.data(),extraarea.data());
  auto g_ar_H2O=make_shared<TGraph>(H2Operc.size(),H2Operc.data(),extraareaH2O.data());
  auto g_ar_HFO_SD=make_shared<TGraph>(HFOperc.size(),HFOperc.data(),extraarea_SD.data());
  auto g_ar_H2O_SD=make_shared<TGraph>(H2Operc.size(),H2Operc.data(),extraareaH2O_SD.data());
  auto g_ar_HFO_1GeV=make_shared<TGraph>(HFOperc.size(),HFOperc.data(),extraarea_1GeV.data());
  auto g_ar_H2O_1GeV=make_shared<TGraph>(H2Operc.size(),H2Operc.data(),extraareaH2O_1GeV.data());
  auto g_ar_HFO_SD_1GeV=make_shared<TGraph>(HFOperc.size(),HFOperc.data(),extraarea_SD_1GeV.data());
  auto g_ar_H2O_SD_1GeV=make_shared<TGraph>(H2Operc.size(),H2Operc.data(),extraareaH2O_SD_1GeV.data());

  auto g_Thres=make_shared<TGraph>(HFOpercThr.size(),HFOpercThr.data(),Thresholds.data());

  Styleup<TGraph>(g_ar_HFO,";H-gas percentage (%);Limit area gained (Log(#frac{GeV}{c^{2}})*Log(cm^{2}) )",kRed,20,1,1,-0.1,5,-120,10);
  Styleup<TGraph>(g_ar_H2O,"a",kBlue,21,1,1);
  Styleup<TGraph>(g_ar_HFO_SD,";H-gas percentage (%);Limit area gained (Log(#frac{GeV}{c^{2}})*Log(cm^{2}) )",kRed,20,1,1,-0.1,5,-120,10);
  Styleup<TGraph>(g_ar_H2O_SD,"b",kBlue,21,1,1);
  Styleup<TGraph>(g_ar_HFO_1GeV,"c",kOrange+7,22,9,1);
  Styleup<TGraph>(g_ar_H2O_1GeV,"aa",kGreen-2,23,9,1);
  Styleup<TGraph>(g_ar_HFO_SD_1GeV,"d",kOrange+7,22,9,1);
  Styleup<TGraph>(g_ar_H2O_SD_1GeV,"bb",kGreen-2,23,9,1);

  Styleup(g_Thres,";H-gas percentage (%);Threshold (keV)",kBlack,23,1,1,0,5,0,10);


  auto c3=make_shared<TCanvas>("Areagain_SI","Areagain_SI");
  g_ar_HFO->Draw("apl");
  g_ar_H2O->Draw("samepl");
  g_ar_HFO_1GeV->Draw("samepl");
  g_ar_H2O_1GeV->Draw("samepl");
  TLegend* fleg2=new TLegend(0.6,0.9,0.9,0.65);
  sprintf(name,"HFO addition until 8 GeV");
  fleg2->AddEntry(g_ar_HFO->GetName(),name,"pl");
  sprintf(name,"H20 until 8 GeV");
  fleg2->AddEntry(g_ar_H2O->GetName(),name,"lp");
  sprintf(name,"HFO addition until 1 GeV");
  fleg2->AddEntry(g_ar_HFO_1GeV->GetName(),name,"pl");
  sprintf(name,"H20 until 1 GeV");
  fleg2->AddEntry(g_ar_H2O_1GeV->GetName(),name,"pl");
  fleg2->Draw("SAME");
  c3->Write();

  auto c4=make_shared<TCanvas>("Areagain_SD","Areagain_SD");
  g_ar_HFO_SD->Draw("apl");
  g_ar_H2O_SD->Draw("samepl");
  g_ar_HFO_SD_1GeV->Draw("samepl");
  g_ar_H2O_SD_1GeV->Draw("samepl");
  TLegend* fleg3=new TLegend(0.6,0.9,0.9,0.65);
  sprintf(name,"HFO addition until 8 GeV");
  fleg3->AddEntry(g_ar_HFO_SD->GetName(),name,"pl");
  sprintf(name,"H20 until 8 GeV");
  fleg3->AddEntry(g_ar_H2O_SD->GetName(),name,"lp");
  sprintf(name,"HFO addition until 1 GeV");
  fleg3->AddEntry(g_ar_HFO_SD_1GeV->GetName(),name,"pl");
  sprintf(name,"H20 until 1 GeV");
  fleg3->AddEntry(g_ar_H2O_SD_1GeV->GetName(),name,"pl");
  fleg3->Draw("SAME");
  c4->Write();

  auto c5=make_shared<TCanvas>("Thresholds","Thresholds");
  g_Thres->Draw("apl");
  c5->Write();



  rf->Flush();
  rf->Close();

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

template <typename T> void Styleup(shared_ptr<T> & g, string title, int color, int marker, int linestyle, int linewidth, double xmin, double xmax, double ymin, double ymax)
{
  g->SetLineColor(color);
	g->SetLineStyle(linestyle);
	g->SetMarkerStyle(marker);
  g->SetMarkerSize(1.8);
	g->SetMarkerColor(color);
	g->SetLineWidth(linewidth);
  g->SetName(title.c_str());
	
  g->GetXaxis()->SetLimits(xmin,xmax);				
  g->GetYaxis()->SetRangeUser(ymin,ymax);		
  g->GetYaxis()->SetTitleSize(0.05);
  g->GetYaxis()->SetLabelSize(0.05);
  g->GetXaxis()->SetTitleSize(0.05);
  g->GetXaxis()->SetLabelSize(0.05);
  g->SetTitle(title.c_str());
  g->GetYaxis()->SetTitleOffset(1.00);

return;
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