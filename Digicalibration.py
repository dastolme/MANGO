import ROOT
import numpy as np
import uproot
import pandas as pd
import re
import matplotlib.pyplot as plt

def extract_exponential_numbers(s_list):
    numbers = []
    for s in s_list:
        match = re.findall(r'[-+]?\d*\.\d+E[-+]?\d+|\d+E[-+]?\d+', s)
        if match:
            numbers.extend(match)
    return numbers

def plot_waveform(X, waveform, run, i, charge, save=False, filename=None):
    plt.clf()  # Clear the current figure
    plt.plot(X, waveform[i])
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title(f'Waveform for run {run}, event {i} charge {charge}')
    if save and filename:
        plt.savefig(filename)
    else:
        plt.show()

def fill_h(histo_name, array):
    for x in range (len(array)):
        histo_name.Fill((np.array(array[x] ,dtype="d")))
def hist(list, x_name, channels=100, linecolor=4, linewidth=4,write=True):
    array=np.array(list ,dtype="d")
    hist=ROOT.TH1D(x_name,x_name,channels,0.99*np.min(array),1.01*np.max(array))
    fill_h(hist,array)
    hist.SetLineColor(linecolor)
    hist.SetLineWidth(linewidth)
    hist.GetXaxis().SetTitle(x_name)
    hist.GetYaxis().SetTitle("Entries")
    if write==True: hist.Write()
    #hist.SetStats(False)
    hist.GetYaxis().SetMaxDigits(3);
    hist.GetXaxis().SetMaxDigits(3);
    return hist
def graph(x,y,x_string, y_string,name=None, color=4, markerstyle=22, markersize=2,write=True):
        plot = ROOT.TGraph(len(x),  np.array(x  ,dtype="d")  ,   np.array(y  ,dtype="d") )
        if name is None: plot.SetNameTitle(y_string+" vs "+x_string,y_string+" vs "+x_string)
        else: plot.SetNameTitle(name, name)
        plot.GetXaxis().SetTitle(x_string)
        plot.GetYaxis().SetTitle(y_string)
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        if write==True: plot.Write()
        return plot
def nparr(list):
    return np.array(list, dtype="d")
def grapherr(x,y,ex,ey,x_string, y_string,name=None, color=4, markerstyle=22, markersize=2,write=True):
        plot = ROOT.TGraphErrors(len(x),  np.array(x  ,dtype="d"),  np.array(y  ,dtype="d"),  np.array(ex  ,dtype="d")  ,   np.array(ey  ,dtype="d") )
        if name is None: plot.SetNameTitle(y_string+" vs "+x_string,y_string+" vs "+x_string)
        else: plot.SetNameTitle(name, name)
        plot.GetXaxis().SetTitle(x_string)
        plot.GetYaxis().SetTitle(y_string)
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        if write==True: plot.Write()
        return plot
#read runlog
df = pd.read_csv('Runs_2702.csv')

df_charge_calibration = df[df['run_description'].str.contains('Charge calibration', na=False)]
runs=df_charge_calibration["run_number"].tolist()
input_charges=extract_exponential_numbers(df_charge_calibration["run_description"])

# Open ROOT files with uproot
hists_amplitudes=[]
for run in runs:
    print(f"Processing run {run} with charge {input_charges[runs.index(run)]}")
    file_path = f'./Reco/reco_run{run}_3D.root'
    try:
        charge=input_charges[runs.index(run)]
        root_file = uproot.open(file_path)
        tree = root_file["GEM_Events"]
        pmt_fullWaveform_Y = tree["pmt_fullWaveform_Y"].array(library="np")
        dt=1.3333333333333333e-09#seconds
        X = np.arange(0, len(pmt_fullWaveform_Y[0])*dt, dt)
        #print(X, pmt_fullWaveform_Y[0])
        num_events = len(pmt_fullWaveform_Y)
        plot_waveform(X, pmt_fullWaveform_Y, run, 0,charge, save=True, filename=f'waveform_run{run}_charge_{charge}_event0.png')
        
        min_values = [np.min(event) for event in pmt_fullWaveform_Y]
        hist_temp=hist(min_values, f"Minimum Values for Run {run} charge {charge}", channels=300, linecolor=4, linewidth=4, write=False)
        mean = hist_temp.GetMean()
        sigma = hist_temp.GetStdDev()
        min_values = [value for value in min_values if (mean - 5 * sigma) <= value <= (mean + 5 * sigma)]
        hist_temp.Delete()

        hist_min_values = hist(min_values, f"Minimum Values for Run {run} charge {charge}", channels=300, linecolor=4, linewidth=4, write=False)
        hists_amplitudes.append(hist_min_values,)


    except FileNotFoundError:
        print(f"File {file_path} not found.")

main_file = ROOT.TFile("ChargeCalibration.root","RECREATE")
means, err_means = [], []
for hist in hists_amplitudes:
    minX,maxX = hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax()
    if input_charges[hists_amplitudes.index(hist)] =="1.58E-13":
        ROOT.TF1("gaus","gaus",-2200,-1000)
        hist.Fit("gaus","RQ","",-2200,-1000)
    else:
        ROOT.TF1("gaus","gaus",minX,maxX)
        hist.Fit("gaus","RQ","",minX,maxX)
    hist.Write()
    means.append(hist.GetFunction("gaus").GetParameter(1))

    err_means.append(hist.GetRMS())
    

graph1=grapherr(input_charges,means,1E-15*np.ones(len(input_charges)),err_means   ,"Charges","Mean of minimum values","Mean of minimum values vs Run number", color=4, markerstyle=22, markersize=2,write=False)

fit_func = ROOT.TF1("fit_func", "pol1", 0, 0.3E-12)
fit_func.SetParameter(0, -60)
fit_func.SetParameter(1, -1.32E+16)

canvas = ROOT.TCanvas("canvas", "Fit Canvas", 1000, 1000)
canvas.SetLeftMargin(0.15)
canvas.SetRightMargin(0.12)
graph1.GetXaxis().SetRangeUser(0, 300E-15)
graph1.Fit(fit_func, "RQ")
graph1.Draw("AP")

pave_text = ROOT.TPaveText(0.6, 0.7, 0.88, 0.9, "NDC")
pave_text.SetFillStyle(0)
pave_text.SetTextAlign(12)
pave_text.AddText(f"Fit Parameters:")
pave_text.AddText(f"Slope: {fit_func.GetParameter(1):.2e} +/- {fit_func.GetParError(1):.2e}")
pave_text.AddText(f"Intercept: {fit_func.GetParameter(0):.2e} +/- {fit_func.GetParError(0):.2e}")
pave_text.AddText(f"Chi2/NDF: {fit_func.GetChisquare() / fit_func.GetNDF():.2e}")
pave_text.Draw("same")

graph1.Write()

canvas.SaveAs("fit_graph1.png")

# Save the slope and intercept in a TTree
tree = ROOT.TTree("CalibParam", "CalibParam")
slope = np.zeros(1, dtype=float)
intercept = np.zeros(1, dtype=float)

tree.Branch("slope", slope, "slope/D")
tree.Branch("intercept", intercept, "intercept/D")

slope[0] = fit_func.GetParameter(1)
intercept[0] = fit_func.GetParameter(0)

tree.Fill()
tree.Write()

main_file.Close()