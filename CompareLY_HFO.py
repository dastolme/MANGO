import ROOT
import numpy as np
import uproot
import pandas as pd
import re
import matplotlib.pyplot as plt

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

def read_and_create_graph(filename,marker=20,color=4):
    # Read the text file using numpy.genfromtxt with tab delimiter and header names
    data = np.genfromtxt(filename, delimiter='\t', names=True)
    
    # Extract columns: VGEM for x-values, Peak for y-values, and dPeak for y-errors.
    x = data['VGEM']
    y = data['Peak']
    ey = data['dPeak']
    
    # Create a constant error array for x (here, every point gets an error of 1)
    ex = np.ones(len(x))
    
    # Use the grapherr function to create the TGraphErrors
    g = grapherr(x, y, ex, ey, "VGEM", "Peak",markerstyle=marker, color=color,write=False)
    return g


#! LY comparison
# Open the ROOT file in read mode
root_file_0 = ROOT.TFile("HFO0.root", "READ")
graph_LY_0 = root_file_0.Get("Integral vs VGEM")
root_file_1 = ROOT.TFile("HFO1.root", "READ")
graph_LY_1 = root_file_1.Get("Integral vs VGEM")
graph_LY_0.SetMarkerStyle(20)
graph_LY_0.SetMarkerColor(2)
graph_LY_1.SetMarkerStyle(21)
graph_LY_1.SetMarkerColor(4)

graphLY_25=read_and_create_graph("LY_HeCF4_HFO_2.5.txt",marker=22,color=6)
graph_LY_5=read_and_create_graph("LY_HeCF4_HFO_5.txt",marker=23,color=9)

mulitgraph=ROOT.TMultiGraph()
mulitgraph.Add(graph_LY_0)
mulitgraph.Add(graph_LY_1)
mulitgraph.Add(graphLY_25)
mulitgraph.Add(graph_LY_5)
mulitgraph.SetNameTitle("Camera_ADC vs VGEM","Camera_ADC vs VGEM")
mulitgraph.GetXaxis().SetTitle("VGEM [V]")
mulitgraph.GetYaxis().SetTitle("Camera_ADC")

range=[1E2, 3E5]
mulitgraph.GetYaxis().SetRangeUser(range[0],range[1])
mulitgraph.GetXaxis().SetRangeUser(330,520)

pavetext = ROOT.TPaveText(0.15, 0.8, 0.5, 0.9, "NDC")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)
pavetext.AddText("#color[2]{He/CF_4/HFO 60/40/0}")
pavetext.AddText("#color[4]{He/CF_4/HFO 60/40/1}")
pavetext.AddText("#color[6]{He/CF_4/HFO 60/40/2.5}")
pavetext.AddText("#color[9]{He/CF_4/HFO 60/40/5}")

# Create a canvas with a specified title and dimensions.
name=mulitgraph.GetName()
canvas = ROOT.TCanvas("canvas", name, 1000, 1000)
canvas.SetLeftMargin(0.15)
canvas.SetRightMargin(0.12)
canvas.SetLogy()
# Draw the graph with axis, points, and error bars.
mulitgraph.Draw("AP")
# If a latex_text is provided, create a TLatex object and draw it.
pavetext.Draw("same")

linea = ROOT.TLine(460, range[0], 460, range[1])
linea.SetLineColor(2)
linea.SetLineStyle(2)
linea.SetLineWidth(3)
linea.Draw("same")
line = ROOT.TLine(480, range[0], 480, range[1])
line.SetLineColor(6)
line.SetLineStyle(2)
line.SetLineWidth(3)
line.Draw("same")
lineq = ROOT.TLine(500, range[0], 500, range[1])
lineq.SetLineColor(9)
lineq.SetLineStyle(2)
lineq.SetLineWidth(3)
lineq.Draw("same")
# Update the canvas to process all drawing commands.
canvas.SetGrid()
canvas.Update()
# Save the canvas as a PNG file.
canvas.SaveAs("HFO_LY_comparison.png")


def read_and_create_graph_resolution(filename,marker=20,color=4):
    # Read the text file using numpy.genfromtxt with tab delimiter and header names
    data = np.genfromtxt(filename, delimiter='\t', names=True)
    
    # Extract columns: VGEM for x-values, Peak for y-values, and dPeak for y-errors.
    x = data['VGEM']
    ly = data['Peak']
    ely = data['dPeak']
    sigma = data['Sigma']
    esigma = data['dsigma']
    
    # Compute the resolution as sigma / ly
    y = sigma / ly
    # Propagate the errors for the resolution
    ey = y * np.sqrt((esigma / sigma) ** 2 + (ely / ly) ** 2)

    # Create a constant error array for x (here, every point gets an error of 1)
    ex = np.ones(len(x))
    
    # Use the grapherr function to create the TGraphErrors
    g = grapherr(x, y, ex, ey, "VGEM", "Resolution",markerstyle=marker, color=color,write=False)
    return g

#! Resolution comparison
# Open the ROOT file in read mode
root_file_0 = ROOT.TFile("HFO0.root", "READ")
graph_LY_0 = root_file_0.Get("Resolution vs VGEM")
root_file_1 = ROOT.TFile("HFO1.root", "READ")
graph_LY_1 = root_file_1.Get("Resolution vs VGEM")
graph_LY_0.SetMarkerStyle(20)
graph_LY_0.SetMarkerColor(2)
graph_LY_1.SetMarkerStyle(21)
graph_LY_1.SetMarkerColor(4)

graphLY_25=read_and_create_graph_resolution("LY_HeCF4_HFO_2.5.txt",marker=22,color=6)
graph_LY_5=read_and_create_graph_resolution("LY_HeCF4_HFO_5.txt",marker=23,color=9)

mulitgraph=ROOT.TMultiGraph()
mulitgraph.Add(graph_LY_0)
mulitgraph.Add(graph_LY_1)
mulitgraph.Add(graphLY_25)
mulitgraph.Add(graph_LY_5)
mulitgraph.SetNameTitle("Camera RMS Energy Resolution vs VGEM","Camera RMS Energy Resolution vs VGEM")
mulitgraph.GetXaxis().SetTitle("VGEM [V]")
mulitgraph.GetYaxis().SetTitle("Camera RMS Energy Resolution")

range=[0, 0.5]
mulitgraph.GetYaxis().SetRangeUser(range[0],range[1])
mulitgraph.GetXaxis().SetRangeUser(355,520)

pavetext = ROOT.TPaveText(0.15, 0.8, 0.5, 0.9, "NDC")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)
pavetext.AddText("#color[2]{He/CF_4/HFO 60/40/0}")
pavetext.AddText("#color[4]{He/CF_4/HFO 60/40/1}")
pavetext.AddText("#color[6]{He/CF_4/HFO 60/40/2.5}")
pavetext.AddText("#color[9]{He/CF_4/HFO 60/40/5}")

# Create a canvas with a specified title and dimensions.
name=mulitgraph.GetName()
canvas = ROOT.TCanvas("canvas", name, 1000, 1000)
canvas.SetLeftMargin(0.15)
canvas.SetRightMargin(0.12)
# Draw the graph with axis, points, and error bars.
mulitgraph.Draw("AP")
# If a latex_text is provided, create a TLatex object and draw it.
pavetext.Draw("same")

linea = ROOT.TLine(460, range[0], 460, range[1])
linea.SetLineColor(2)
linea.SetLineStyle(2)
linea.SetLineWidth(3)
linea.Draw("same")
line = ROOT.TLine(480, range[0], 480, range[1])
line.SetLineColor(6)
line.SetLineStyle(2)
line.SetLineWidth(3)
line.Draw("same")
lineq = ROOT.TLine(500, range[0], 500, range[1])
lineq.SetLineColor(9)
lineq.SetLineStyle(2)
lineq.SetLineWidth(3)
lineq.Draw("same")
# Update the canvas to process all drawing commands.
canvas.SetGrid()
canvas.Update()
# Save the canvas as a PNG file.
canvas.SaveAs("HFO_Resolution_comparison.png")
