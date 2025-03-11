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


colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+7, ROOT.kViolet]
markers = [20, 21, 22, 23, 47, 34]

#! LY comparison
# Open the ROOT file in read mode
root_file_0 = ROOT.TFile("HFO0.root", "READ")
graph_LY_0 = root_file_0.Get("Integral vs VGEM")
root_file_1 = ROOT.TFile("HFO1.root", "READ")
graph_LY_1 = root_file_1.Get("Integral vs VGEM")
graph_LY_0.SetMarkerStyle(markers[0])
graph_LY_0.SetMarkerColor(colors[0])
graph_LY_1.SetMarkerStyle(markers[1])
graph_LY_1.SetMarkerColor(colors[1])


graph_LY_0.GetListOfFunctions().Remove(graph_LY_0.GetFunction("expo_fit"))
graph_LY_1.GetListOfFunctions().Remove(graph_LY_1.GetFunction("expo_fit"))


graphLY_25=read_and_create_graph("LY_HeCF4_HFO_2.5.txt",marker=markers[2],color=colors[2])
graph_LY_5=read_and_create_graph("LY_HeCF4_HFO_5.txt",marker=markers[3],color=colors[3])
graph_LY_75=read_and_create_graph("LY_HeCF4_HFO_7.5.txt",marker=markers[4],color=colors[4])
graph_LY_10=read_and_create_graph("LY_HeCF4_HFO_10.txt",marker=markers[5],color=colors[5])


mulitgraph=ROOT.TMultiGraph()
mulitgraph.Add(graph_LY_0)
mulitgraph.Add(graph_LY_1)
mulitgraph.Add(graphLY_25)
mulitgraph.Add(graph_LY_5)
mulitgraph.Add(graph_LY_75)
mulitgraph.Add(graph_LY_10)
mulitgraph.SetNameTitle("Camera_ADC vs VGEM","Camera_ADC vs VGEM")
mulitgraph.GetXaxis().SetTitle("VGEM [V]")
mulitgraph.GetYaxis().SetTitle("Camera_ADC")

range=[1E2, 3E5]
mulitgraph.GetYaxis().SetRangeUser(range[0],range[1])
mulitgraph.GetXaxis().SetRangeUser(330,520)
mulitgraph.GetXaxis().SetLimits(330,520)

pavetext = ROOT.TPaveText(0.15, 0.72, 0.5, 0.9, "NDC")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)
pavetext.AddText(f"#color[{colors[0]}]{{He/CF_{{4}}/HFO 60/40/0}}")
pavetext.AddText(f"#color[{colors[1]}]{{He/CF_{{4}}/HFO 60/40/1}}")
pavetext.AddText(f"#color[{colors[2]}]{{He/CF_{{4}}/HFO 60/40/2.5}}")
pavetext.AddText(f"#color[{colors[3]}]{{He/CF_{{4}}/HFO 60/40/5}}")
pavetext.AddText(f"#color[{colors[4]}]{{He/CF_{{4}}/HFO 60/40/7.5}}")
pavetext.AddText(f"#color[{colors[5]}]{{He/CF_{{4}}/HFO 60/40/10}}")

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
linea.SetLineColor(colors[0])
linea.SetLineStyle(2)
linea.SetLineWidth(3)
linea.Draw("same")
line1 = ROOT.TLine(470, range[0], 470, range[1])
line1.SetLineColor(colors[1])
line1.SetLineStyle(2)
line1.SetLineWidth(3)
line1.Draw("same")
line = ROOT.TLine(480, range[0], 480, range[1])
line.SetLineColor(colors[2])
line.SetLineStyle(2)
line.SetLineWidth(3)
line.Draw("same")
lineq = ROOT.TLine(500, range[0], 500, range[1])
lineq.SetLineColor(colors[3])
lineq.SetLineStyle(2)
lineq.SetLineWidth(3)
lineq.Draw("same")
line7 = ROOT.TLine(510, range[0], 510, range[1])
line7.SetLineColor(colors[4])
line7.SetLineStyle(2)
line7.SetLineWidth(3)
line7.Draw("same")
line10 = ROOT.TLine(520, range[0], 520, range[1])
line10.SetLineColor(colors[5])
line10.SetLineStyle(2)
line10.SetLineWidth(3)
line10.Draw("same")
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
graph_LY_0.SetMarkerStyle(markers[0])
graph_LY_0.SetMarkerColor(colors[0])
graph_LY_1.SetMarkerStyle(markers[1])
graph_LY_1.SetMarkerColor(colors[1])

graphLY_25=read_and_create_graph_resolution("LY_HeCF4_HFO_2.5.txt",marker=markers[2],color=colors[2])
graph_LY_5=read_and_create_graph_resolution("LY_HeCF4_HFO_5.txt",marker=markers[3],color=colors[3])
graph_LY_75=read_and_create_graph_resolution("LY_HeCF4_HFO_7.5.txt",marker=markers[4],color=colors[4])
graph_LY_10=read_and_create_graph_resolution("LY_HeCF4_HFO_10.txt",marker=markers[5],color=colors[5])

mulitgraph=ROOT.TMultiGraph()
mulitgraph.Add(graph_LY_0)
mulitgraph.Add(graph_LY_1)
mulitgraph.Add(graphLY_25)
mulitgraph.Add(graph_LY_5)
mulitgraph.Add(graph_LY_75)
mulitgraph.Add(graph_LY_10)
mulitgraph.SetNameTitle("Camera RMS Energy Resolution vs VGEM","Camera RMS Energy Resolution vs VGEM")
mulitgraph.GetXaxis().SetTitle("VGEM [V]")
mulitgraph.GetYaxis().SetTitle("Camera RMS Energy Resolution")

range=[0, 0.5]
mulitgraph.GetYaxis().SetRangeUser(range[0],range[1])
mulitgraph.GetXaxis().SetRangeUser(355,520)
mulitgraph.GetXaxis().SetLimits(355,525)

pavetext = ROOT.TPaveText(0.15, 0.8, 0.5, 0.9, "NDC")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)
pavetext.AddText(f"#color[{colors[0]}]{{He/CF_{{4}}/HFO 60/40/0}}")
pavetext.AddText(f"#color[{colors[1]}]{{He/CF_{{4}}/HFO 60/40/1}}")
pavetext.AddText(f"#color[{colors[2]}]{{He/CF_{{4}}/HFO 60/40/2.5}}")
pavetext.AddText(f"#color[{colors[3]}]{{He/CF_{{4}}/HFO 60/40/5}}")
pavetext.AddText(f"#color[{colors[4]}]{{He/CF_{{4}}/HFO 60/40/7.5}}")
pavetext.AddText(f"#color[{colors[5]}]{{He/CF_{{4}}/HFO 60/40/10}}")

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
linea.SetLineColor(colors[0])
linea.SetLineStyle(2)
linea.SetLineWidth(3)
linea.Draw("same")
line1 = ROOT.TLine(470, range[0], 470, range[1])
line1.SetLineColor(colors[1])
line1.SetLineStyle(2)
line1.SetLineWidth(3)
line1.Draw("same")
line = ROOT.TLine(480, range[0], 480, range[1])
line.SetLineColor(colors[2])
line.SetLineStyle(2)
line.SetLineWidth(3)
line.Draw("same")
lineq = ROOT.TLine(500, range[0], 500, range[1])
lineq.SetLineColor(colors[3])
lineq.SetLineStyle(2)
lineq.SetLineWidth(3)
lineq.Draw("same")
line7 = ROOT.TLine(510, range[0], 510, range[1])
line7.SetLineColor(colors[4])
line7.SetLineStyle(2)
line7.SetLineWidth(3)
line7.Draw("same")
line10 = ROOT.TLine(520, range[0], 520, range[1])
line10.SetLineColor(colors[5])
line10.SetLineStyle(2)
line10.SetLineWidth(3)
line10.Draw("same")
# Update the canvas to process all drawing commands.
canvas.SetGrid()
canvas.Update()
# Save the canvas as a PNG file.
canvas.SaveAs("HFO_Resolution_comparison.png")



def read_and_create_graph_tgaus(filename,marker=20,color=4):
    # Read the text file using numpy.genfromtxt with tab delimiter and header names
    data = np.genfromtxt(filename, delimiter='\t', names=True)
    
    # Extract columns: VGEM for x-values, Peak for y-values, and dPeak for y-errors.
    x = data['VGEM']
    y = data['gaus']
    ey = data['dgaus']
    # Create a constant error array for x (here, every point gets an error of 1)
    ex = np.ones(len(x))
    
    # Use the grapherr function to create the TGraphErrors
    g = grapherr(x, y, ex, ey, "VGEM", "Resolution",markerstyle=marker, color=color,write=False)
    return g

#! tgaussigma comparison
# Open the ROOT file in read mode
root_file_0 = ROOT.TFile("HFO0.root", "READ")
graph_LY_0 = root_file_0.Get("tgaussigma vs VGEM")
root_file_1 = ROOT.TFile("HFO1.root", "READ")
graph_LY_1 = root_file_1.Get("tgaussigma vs VGEM")
graph_LY_0.SetMarkerStyle(markers[0])
graph_LY_0.SetMarkerColor(colors[0])
graph_LY_1.SetMarkerStyle(markers[1])
graph_LY_1.SetMarkerColor(colors[1])

graphLY_25=read_and_create_graph_tgaus("LY_HeCF4_HFO_2.5.txt",marker=markers[2],color=colors[2])
graph_LY_5=read_and_create_graph_tgaus("LY_HeCF4_HFO_5.txt",marker=markers[3],color=colors[3])
graph_LY_75=read_and_create_graph_tgaus("LY_HeCF4_HFO_7.5.txt",marker=markers[4],color=colors[4])
graph_LY_10=read_and_create_graph_tgaus("LY_HeCF4_HFO_10.txt",marker=markers[5],color=colors[5])

mulitgraph=ROOT.TMultiGraph()
mulitgraph.Add(graph_LY_0)
mulitgraph.Add(graph_LY_1)
mulitgraph.Add(graphLY_25)
mulitgraph.Add(graph_LY_5)
mulitgraph.Add(graph_LY_75)
mulitgraph.Add(graph_LY_10)
mulitgraph.SetNameTitle("Camera RMS Energy Resolution vs VGEM","Camera RMS Energy Resolution vs VGEM")
mulitgraph.GetXaxis().SetTitle("VGEM [V]")
mulitgraph.GetYaxis().SetTitle("Camera RMS Energy Resolution")

range=[2, 12]
mulitgraph.GetYaxis().SetRangeUser(range[0],range[1])
mulitgraph.GetXaxis().SetRangeUser(340,520)
mulitgraph.GetXaxis().SetLimits(340,520)

pavetext = ROOT.TPaveText(0.15, 0.8, 0.5, 0.9, "NDC")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)
pavetext.AddText(f"#color[{colors[0]}]{{He/CF_{{4}}/HFO 60/40/0}}")
pavetext.AddText(f"#color[{colors[1]}]{{He/CF_{{4}}/HFO 60/40/1}}")
pavetext.AddText(f"#color[{colors[2]}]{{He/CF_{{4}}/HFO 60/40/2.5}}")
pavetext.AddText(f"#color[{colors[3]}]{{He/CF_{{4}}/HFO 60/40/5}}")
pavetext.AddText(f"#color[{colors[4]}]{{He/CF_{{4}}/HFO 60/40/7.5}}")
pavetext.AddText(f"#color[{colors[5]}]{{He/CF_{{4}}/HFO 60/40/10}}")

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
linea.SetLineColor(colors[0])
linea.SetLineStyle(2)
linea.SetLineWidth(3)
linea.Draw("same")
line1 = ROOT.TLine(470, range[0], 470, range[1])
line1.SetLineColor(colors[1])
line1.SetLineStyle(2)
line1.SetLineWidth(3)
line1.Draw("same")
line = ROOT.TLine(480, range[0], 480, range[1])
line.SetLineColor(colors[2])
line.SetLineStyle(2)
line.SetLineWidth(3)
line.Draw("same")
lineq = ROOT.TLine(500, range[0], 500, range[1])
lineq.SetLineColor(colors[3])
lineq.SetLineStyle(2)
lineq.SetLineWidth(3)
lineq.Draw("same")
line7 = ROOT.TLine(510, range[0], 510, range[1])
line7.SetLineColor(colors[4])
line7.SetLineStyle(2)
line7.SetLineWidth(3)
line7.Draw("same")
line10 = ROOT.TLine(520, range[0], 520, range[1])
line10.SetLineColor(colors[5])
line10.SetLineStyle(2)
line10.SetLineWidth(3)
line10.Draw("same")
# Update the canvas to process all drawing commands.
canvas.SetGrid()
canvas.Update()
# Save the canvas as a PNG file.
canvas.SaveAs("HFO_tgaussigma_comparison.png")



#! Charge KeV comaprisons

root_file_0 = ROOT.TFile("GainPico_0.root", "READ")
graph_CK_0 = root_file_0.Get("Charge-keV vs VGEM")
graph_CK_0.SetMarkerStyle(markers[0])
graph_CK_0.SetMarkerColor(colors[0])

root_file_1 = ROOT.TFile("GainPico_1.root", "READ")
graph_CK_1 = root_file_1.Get("Charge-keV vs VGEM")
graph_CK_1.SetMarkerStyle(markers[1])
graph_CK_1.SetMarkerColor(colors[1])

root_file_25 = ROOT.TFile("GainPico_2.5.root", "READ")
graph_CK_25 = root_file_25.Get("Charge-keV vs VGEM")
graph_CK_25.SetMarkerStyle(markers[2])
graph_CK_25.SetMarkerColor(colors[2])

root_file_5 = ROOT.TFile("GainPico_5.root", "READ")
graph_CK_5 = root_file_5.Get("Charge-keV vs VGEM")
graph_CK_5.SetMarkerStyle(markers[3])
graph_CK_5.SetMarkerColor(colors[3])


mulitgraph=ROOT.TMultiGraph()
mulitgraph.Add(graph_CK_0)
mulitgraph.Add(graph_CK_1)
mulitgraph.Add(graph_CK_25)
mulitgraph.Add(graph_CK_5)
mulitgraph.SetNameTitle("Charge/keV vs VGEM","Charge/keV vs VGEM")
mulitgraph.GetXaxis().SetTitle("VGEM [V]")
mulitgraph.GetYaxis().SetTitle("Charge/keV [C/keV]")

range=[3E-13, 5E-11]
mulitgraph.GetYaxis().SetRangeUser(range[0],range[1])
mulitgraph.GetXaxis().SetRangeUser(330,500)
mulitgraph.GetXaxis().SetLimits(330,500)

pavetext = ROOT.TPaveText(0.15, 0.72, 0.5, 0.9, "NDC")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)
pavetext.AddText(f"#color[{colors[0]}]{{He/CF_{{4}}/HFO 60/40/0}}")
pavetext.AddText(f"#color[{colors[1]}]{{He/CF_{{4}}/HFO 60/40/1}}")
pavetext.AddText(f"#color[{colors[2]}]{{He/CF_{{4}}/HFO 60/40/2.5}}")
pavetext.AddText(f"#color[{colors[3]}]{{He/CF_{{4}}/HFO 60/40/5}}")

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
linea.SetLineColor(colors[0])
linea.SetLineStyle(2)
linea.SetLineWidth(3)
linea.Draw("same")
line1 = ROOT.TLine(470, range[0], 470, range[1])
line1.SetLineColor(colors[1])
line1.SetLineStyle(2)
line1.SetLineWidth(3)
line1.Draw("same")
line = ROOT.TLine(480, range[0], 480, range[1])
line.SetLineColor(colors[2])
line.SetLineStyle(2)
line.SetLineWidth(3)
line.Draw("same")
lineq = ROOT.TLine(500, range[0], 500, range[1])
lineq.SetLineColor(colors[3])
lineq.SetLineStyle(2)
lineq.SetLineWidth(3)
lineq.Draw("same")
# Update the canvas to process all drawing commands.
canvas.SetGrid()
canvas.Update()
# Save the canvas as a PNG file.
canvas.SaveAs("HFO_ChargeKeV_comparison.png")