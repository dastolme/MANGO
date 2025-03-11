import ROOT
import numpy as np
import uproot
import pandas as pd
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Process and plot data from files.")
parser.add_argument('--hfo_qnt', type=str, help="HFO quantity in the chamber",default=0)

args = parser.parse_args()
hfo_qnt=args.hfo_qnt

def intTOgain(integral):
    conversionFactor=0.107 #e-/count
    lightFraction=0.07# gamma/e- only visible light
    QE=0.35#QE @ effective from Giorgio's calcualtion
    #omega=9.2E-4#solid angle fraction LIME
    omega=1.16E-3#solid angle fraction QUEST MANGO
    n0=168#stima Fe55
    return (integral*conversionFactor)/(lightFraction*omega*QE*n0)

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

# Read the file into a DataFrame
df = pd.read_csv("LY_HeCF4.txt", sep="\t")
# Open the ROOT file in read mode
root_file = ROOT.TFile(f"GainPico_{hfo_qnt}.root", "READ")
# Retrieve the TGraphErrors object
graphCharge = root_file.Get("Gain vs VGEM Corrected")
# Extract X, Y, errX, and errY from the TGraphErrors object
n_points = graphCharge.GetN()
x = np.array([graphCharge.GetPointX(i) for i in range(n_points - 1)])
y = np.array([graphCharge.GetPointY(i) for i in range(n_points - 1)])
ex = np.array([graphCharge.GetErrorX(i) for i in range(n_points - 1)])
ey = np.array([graphCharge.GetErrorY(i) for i in range(n_points - 1)])


# Convert the columns "Peak", "dPeak", "Sigma", "dSigma" using the intTOgain function
df["LightGain"] = df["Peak"].apply(intTOgain)
df["LightGain_err"] = df["dPeak"].apply(intTOgain)



main_file=ROOT.TFile(f"LightChargeComparison_{hfo_qnt}.root","RECREATE")
# Create a new TGraphErrors object
graphLight = grapherr(df["VGEM"], df["LightGain"], np.ones(len(df)), df["LightGain_err"],"VGEM [V]","Light Gain",name="Light Gain vs VGEM",color=2,write=False)
expo=ROOT.TF1("expo","expo",300,430)
graphLight.Fit("expo","RQ")
graphLight.Write()

pavetext = ROOT.TPaveText(0.15, 0.8, 0.5, 0.9, "NDC")
pavetext.SetFillStyle(0)  # No fill
pavetext.SetBorderSize(0)  # No border
pavetext.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
pavetext.SetTextAlign(12)
pavetext.AddText("#color[2]{Light Gain converted}")
#pavetext.AddText("#color[4]{33M#Omega resistor VGEM corrected}")
pavetext.AddText("#color[4]{Charge Gain}")


mulitgraph=ROOT.TMultiGraph()
mulitgraph.Add(graphCharge)
mulitgraph.Add(graphLight)
mulitgraph.SetNameTitle("Gain vs VGEM","Gain vs VGEM")
mulitgraph.GetXaxis().SetTitle("VGEM [V]")
mulitgraph.GetYaxis().SetTitle("Gain")
mulitgraph.GetYaxis().SetRangeUser(5E4, 5E6)

plot_tgrapherrors(mulitgraph, f"ChargeVSLight_{hfo_qnt}.png", setLog=True, setGrid=True, pavetext=pavetext)

"""
difference=np.abs(df["LightGain"]-y)
difference_err = np.sqrt(df["LightGain_err"]**2 + ey**2)
ratio = df["LightGain"]/y
ratio_err = ratio * np.sqrt((df["LightGain_err"] / df["LightGain"])**2 + (ey / y)**2)
"""
# Create a DataFrame from the numpy arrays using the same column names for merging.
df_x = pd.DataFrame({"VGEM": np.array(x), "y": np.array(y), "ey": np.array(ey)})

# Convert the VGEM columns to the same type (e.g., float) in both DataFrames.
df["VGEM"] = df["VGEM"].astype(float)
df_x["VGEM"] = df_x["VGEM"].astype(float)

# Ensure both DataFrames are sorted by VGEM (merge_asof requires sorted data).
df = df.sort_values("VGEM")
df_x = df_x.sort_values("VGEM")

# Use merge_asof to merge the two DataFrames on VGEM,
# allowing matches within a tolerance of 1 (units of VGEM).
merged = pd.merge_asof(df, df_x, on="VGEM", tolerance=1, direction="nearest")

# Compute the desired quantities using the merged DataFrame.
difference = np.abs(merged["LightGain"] - merged["y"])
difference_err = np.sqrt(merged["LightGain_err"]**2 + merged["ey"]**2)
ratio = merged["LightGain"] / merged["y"]
ratio_err = ratio * np.sqrt(
    (merged["LightGain_err"] / merged["LightGain"])**2 +
    (merged["ey"] / merged["y"])**2
)

graphDifference = grapherr(df_x["VGEM"], difference, np.ones(len(df_x["VGEM"])), difference_err,"VGEM [V]","|Light Gain - Charge Gain|",name="|Light Gain - Charge Gain|",color=2,write=True)
graphRatio = grapherr(df_x["VGEM"], ratio, np.ones(len(df_x["VGEM"])), ratio_err,"VGEM [V]","Light Gain / Charge Gain",name="Light Gain / Charge Gain",color=2,write=True)

# Create a rectangular canvas with two pads
canvas = ROOT.TCanvas("canvas", "Difference and Ratio", 2300, 1000)
canvas.Divide(2, 1)
canvas.cd(1).SetLeftMargin(0.15)
# Draw graphDifference on the left pad
canvas.cd(1)
graphDifference.Draw("AP")

# Draw graphRatio on the right pad
canvas.cd(2)
graphRatio.Draw("AP")

# Update the canvas to process all drawing commands
canvas.Update()

# Save the canvas as a PNG file
canvas.SaveAs(f"DifferenceAndRatio_{hfo_qnt}.png")

