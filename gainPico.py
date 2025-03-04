import ROOT
import uproot
import numpy as np
import pandas as pd
import os
import argparse
import re
import matplotlib.pyplot as plt

#meassured from Plateau
#first measuremtn
rate=12E3
err_rate=0.2E3
#second mesurement
rate=10E3
err_rate=0.2E3
n0=168
e=1.6E-19

# Set up argument parser
parser = argparse.ArgumentParser(description="Process and plot data from files.")
parser.add_argument('--plot', action='store_true', help="Activate plotting of second column data")

args = parser.parse_args()

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


def read_second_column(filename):
    # Read only the second column (index 1) from the file
    second_column = np.loadtxt(filename, usecols=1)
    return second_column

def plot_second_column(filename):
    # Load the second column from the file (index 1)
    second_column = np.loadtxt(filename, usecols=1)
    # Create an index array based on the length of the second column
    index = np.arange(len(second_column))
    
    # Plot the second column vs. the index
    plt.figure(figsize=(8, 5))
    plt.plot(index, second_column, marker='o', linestyle='-', color='b')
    plt.xlabel("Index")
    plt.ylabel("Second Column")
    plt.title("Plot of Second Column vs. Index")
    plt.grid(True)
    plt.show()

def get_vgem_number(filename):
    # Extract the number right after "VGEM" in the filename
    match = re.search(r'VGEM(\d+)', filename)
    if match:
        return int(match.group(1))
    else:
        return None

data_dir = "picoammeter_Data/"

# Iterate over each file in the specified directory if plotting is activated
if args.plot:
    for filename in os.listdir(data_dir):
        if "SOURCE" not in filename:
            continue  # Skip files that do not contain "SOURCE" in the name

        file_path = os.path.join(data_dir, filename)
        
        # Plot the data using the provided plotting function
        plot_second_column(file_path)

        print(f"File: {filename}")

def plot_tgrapherrors(gr, output_filename="output.png",setLog=False,setGrid=True, pavetext=None):
    # Create a canvas with a specified title and dimensions.
    name=gr.GetName()
    canvas = ROOT.TCanvas("canvas", name, 1000, 1000)
    canvas.SetLeftMargin(0.15)
    canvas.SetRightMargin(0.12)
    if setGrid: canvas.SetGrid()
    # Set logarithmic scale if requested.
    if setLog: canvas.SetLogy()
    
    # Set default axis titles if not already provided.
    if not gr.GetXaxis().GetTitle():
        gr.GetXaxis().SetTitle("X-axis")
    if not gr.GetYaxis().GetTitle():
        gr.GetYaxis().SetTitle("Y-axis")
    
    # Draw the graph with axis, points, and error bars.
    gr.Draw("AP")
    
    # If a latex_text is provided, create a TLatex object and draw it.
    if pavetext is not None:
        pavetext.Draw("same")

    # Update the canvas to process all drawing commands.
    canvas.Update()
    
    # Save the canvas as a PNG file.
    canvas.SaveAs(output_filename)
    
    # Optionally, you can return the canvas if further manipulation is needed.
    return canvas


file_numbers = {}
for filename in os.listdir(data_dir):
    file_path = os.path.join(data_dir, filename)

    # Get the VGEM number from the filename
    vgem_number = get_vgem_number(filename)
    if vgem_number is not None:
        # Read the second column data
        second_column = read_second_column(file_path)
        
        # Calculate the mean and standard error of the mean
        mean_value = np.mean(second_column)
        mean_error = np.std(second_column) / np.sqrt(len(second_column))
        
        # Store the results in the dictionary
        if vgem_number not in file_numbers:
            file_numbers[vgem_number] = {'BKG': [], 'SOURCE': []}
        
        if "BKG" in filename:
            file_numbers[vgem_number]['BKG'].append((mean_value, mean_error))
        elif "SOURCE" in filename:
            file_numbers[vgem_number]['SOURCE'].append((mean_value, mean_error))

# Calculate the overall mean and mean error for each VGEM number
vgem_results = {}
for vgem_number, data in file_numbers.items():
    bkg_means = [x[0] for x in data['BKG']]
    bkg_errors = [x[1] for x in data['BKG']]
    source_means = [x[0] for x in data['SOURCE']]
    source_errors = [x[1] for x in data['SOURCE']]
    
    if bkg_means:
        overall_bkg_mean = np.mean(bkg_means)
        overall_bkg_error = np.sqrt(np.sum(np.array(bkg_errors)**2)) / len(bkg_errors)
    else:
        overall_bkg_mean = None
        overall_bkg_error = None
    
    if source_means:
        overall_source_mean = np.mean(source_means)
        overall_source_error = np.sqrt(np.sum(np.array(source_errors)**2)) / len(source_errors)
    else:
        overall_source_mean = None
        overall_source_error = None
        
    vgem_results[vgem_number] = {
    'BKG_mean': overall_bkg_mean,
    'BKG_error': overall_bkg_error,
    'SOURCE_mean': overall_source_mean,
    'SOURCE_error': overall_source_error
    }

# Print the results
for vgem_number, results in vgem_results.items():
    print(f"VGEM {vgem_number}:")
    print(f"  BKG Mean: {results['BKG_mean']}, BKG Error: {results['BKG_error']}")
    print(f"  SOURCE Mean: {results['SOURCE_mean']}, SOURCE Error: {results['SOURCE_error']}")


vgem_numbers = []
net_means = []
net_errors = []

for vgem_number, results in vgem_results.items():
    if results['BKG_mean'] is not None and results['SOURCE_mean'] is not None:
        net_mean = results['SOURCE_mean'] - results['BKG_mean']
        net_error = np.sqrt(results['SOURCE_error']**2 + results['BKG_error']**2)
        
        vgem_numbers.append(vgem_number)
        net_means.append(net_mean)
        net_errors.append(net_error)

vgem_numbers = np.array(vgem_numbers)
net_means = np.array(net_means)
net_errors = np.array(net_errors)

#first measuremtn
R_protection=33E6
#second measurement
R_protection=1E6

voltage_drop=abs(R_protection*net_means)
vgem_number_corrected = (3*vgem_numbers - voltage_drop)/3

print("VGEM Numbers:", vgem_numbers)
print("Net Means:", net_means)
print("Net Errors:", net_errors)

main_file = ROOT.TFile("GainPico.root","RECREATE")
grapherr(vgem_numbers, net_means, np.zeros_like(net_means), net_errors, "VGEM [V]", "Current [A]", "Current vs VGEM ", write=True)


#! gain
# Calculate the gain from the net means
gains = abs(net_means) / (rate * e*n0)
gain_errors = gains*np.sqrt((net_errors/net_means)**2 + (err_rate/rate)**2)

gainPlot=grapherr(vgem_numbers, gains, np.ones(len(vgem_numbers)), gain_errors, "VGEM [V]", "Gain", "Gain vs VGEM", write=False,markerstyle=21)
expo=ROOT.TF1("expo","expo",300,410)
gainPlot.Fit("expo","RQ")
gainPlot.Write()

pavetext = ROOT.TPaveText(0.15, 0.7, 0.45, 0.9, "NDC")
pavetext.AddText(f"Gain = exp(A + B * VGEM)")
pavetext.AddText(f"A = {expo.GetParameter(0):.2e} +/- {expo.GetParError(0):.2e}")
pavetext.AddText(f"B = {expo.GetParameter(1):.2e} +/- {expo.GetParError(1):.2e}")
if expo.GetNDF() != 0:
    pavetext.AddText(f"Chi2/NDF: {expo.GetChisquare() / expo.GetNDF():.2e}")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)


plot_tgrapherrors(gainPlot, "GainPico_HeCF4.png", setLog=True, setGrid=True, pavetext=pavetext)

#! gain corrected

gainPlot=grapherr(vgem_number_corrected, gains, np.ones(len(vgem_numbers)), gain_errors, "VGEM corr [V]", "Gain", "Gain vs VGEM Corrected", write=False,markerstyle=21)
expo=ROOT.TF1("expo","expo",300,430)
gainPlot.Fit("expo","RQ")
gainPlot.Write()

pavetext = ROOT.TPaveText(0.15, 0.6, 0.5, 0.9, "NDC")
pavetext.AddText(f"Gain = exp(A + B * VGEM)")
pavetext.AddText(f"A = {expo.GetParameter(0):.2e} +/- {expo.GetParError(0):.2e}")
pavetext.AddText(f"B = {expo.GetParameter(1):.2e} +/- {expo.GetParError(1):.2e}")
if expo.GetNDF() != 0:
    pavetext.AddText(f"Chi2/NDF: {expo.GetChisquare() / expo.GetNDF():.2e}")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)
pavetext.AddText("#color[2]{1M#Omega resistor, no correction on VGEM}")
#pavetext.AddText("#color[4]{33M#Omega resistor VGEM corrected}")
pavetext.AddText("#color[4]{1M#Omega resistor VGEM corrected}")

#! test point
noise_mega_curr=read_second_column("picoammeter_Data/BKG_HFO_0_VGEM430_1_MOhm.txt")
source_mega_curr=read_second_column("picoammeter_Data/SOURCE_HFO_0_VGEM430_1_MOhm.txt")
new_rate=9.5E3
err_new_rate=0.5E3

# Calculate the mean and standard error of the mean
mean_noise_mega_curr = np.mean(noise_mega_curr)
mean_source_mega_curr = np.mean(source_mega_curr)
mean_noise_error = np.std(noise_mega_curr) / np.sqrt(len(noise_mega_curr))
mean_source_error = np.std(source_mega_curr) / np.sqrt(len(source_mega_curr))

# Calculate the net current and error
net_curr = mean_source_mega_curr - mean_noise_mega_curr
net_curr_error = np.sqrt(mean_source_error**2 + mean_noise_error**2)

# Calculate the gain
gain = abs(net_curr) / (new_rate * e*n0)
gain_error = gain*np.sqrt((net_curr_error/net_curr)**2 + (err_new_rate/new_rate)**2)

print("Gain 1Mega 430V: ", gain, "+/-", gain_error)

new_tgraph=grapherr([430], [gain], [1], [gain_error], "VGEM [V]", "Gain", "Gain vs VGEM no voltage drop", write=True,markerstyle=20, color=2)

mulitgraph=ROOT.TMultiGraph()

mulitgraph.Add(gainPlot)
mulitgraph.Add(new_tgraph)

mulitgraph.SetNameTitle("Gain vs VGEM","Gain vs VGEM")
mulitgraph.GetXaxis().SetTitle("VGEM [V]")
mulitgraph.GetYaxis().SetTitle("Gain")
mulitgraph.GetYaxis().SetRangeUser(1E5, 5E6)

plot_tgrapherrors(mulitgraph, "GainPico_corr_HeCF4.png", setLog=True, setGrid=True, pavetext=pavetext)
