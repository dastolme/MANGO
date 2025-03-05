import cygno as cy
import numpy as np
import uproot
import pandas as pd
import ROOT
import os
import argparse
from tqdm import tqdm
import awkward as ak


def filter_runlog_by_hfo_c(runlog_df, desired_c):
    """
    Filters the runlog dataframe to keep only rows that have the desired HFO 'c' quantity.
    
    Parameters:
        runlog_df (pd.DataFrame): The runlog dataframe with a 'run_description' column.
        desired_c (int or str): The desired HFO 'c' value to filter by.
        
    Returns:
        pd.DataFrame: The filtered dataframe containing only rows where the HFO 'c' value matches desired_c.
    """
    # Make a copy to avoid modifying the original dataframe
    df = runlog_df.copy()
    
    # Step 1: Extract the HFO ratio string (e.g., "a/b/c") from run_description.
    # The regex captures one or more digits, slashes, and dots immediately following "HFO" up to "- GEM".
    df['hfo_values'] = df['run_description'].str.extract(r'HFO\s+([\d/.]+)\s*- GEM', expand=False)

    # Remove rows where the pattern wasn't found
    df = df.dropna(subset=['hfo_values'])
    
    # Step 2: Split the HFO values into three separate columns.
    hfo_split = df['hfo_values'].str.split('/', expand=True)
    if hfo_split.shape[1] != 3:
        # Optionally, drop rows that do not have exactly three components.
        df = df[hfo_split.shape[1] == 3]
    
    # Convert the third component (c) to a numeric value.
    df['hfo_c'] = pd.to_numeric(hfo_split[2], errors='coerce')
    df = df.dropna(subset=['hfo_c'])
    
    # Step 3: Filter the dataframe by the desired HFO 'c' quantity.
    desired_c = pd.to_numeric(desired_c, errors='coerce')
    filtered_df = df[df['hfo_c'] == desired_c].copy()
    
    # Optionally, drop the intermediate columns if they are no longer needed.
    filtered_df = filtered_df.drop(columns=['hfo_values', 'hfo_c'])
    
    return filtered_df
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

def filter_df_by_range(df, column, lower, upper, require_all=False):
    """
    Filters a DataFrame by selecting rows where the values in the specified column
    are within the range (lower, upper). If a cell's value is a list (or an Awkward array),
    the row is kept if:
      - require_all is False (default): any numeric element is within the range.
      - require_all is True: all numeric elements are within the range.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): The name of the column to filter.
        lower (numeric): The lower bound (exclusive).
        upper (numeric): The upper bound (exclusive).
        require_all (bool): If True, require all elements in a list-like cell to be within the range.
    
    Returns:
        pd.DataFrame: A DataFrame filtered to include only rows meeting the condition.
    """
    
    def in_range(val):
        # If the value is an Awkward array, convert it to a Python list.
        if isinstance(val, ak.Array):
            try:
                val = ak.to_list(val)
            except Exception:
                return False
        
        # If the value is list-like, check its elements.
        if isinstance(val, list):
            # Filter numeric values to avoid comparison issues.
            numeric_vals = [x for x in val if isinstance(x, (int, float))]
            if not numeric_vals:
                return False
            if require_all:
                return all(x > lower and x < upper for x in numeric_vals)
            else:
                return any(x > lower and x < upper for x in numeric_vals)
        
        # Otherwise, assume it's a scalar and check directly.
        try:
            return (val > lower and val < upper)
        except Exception:
            return False
    
    mask = df[column].apply(in_range)
    return df[mask]

def get_vars(var_list, file, cuts):
    try:
        events = uproot.open(file + ":Events")
    except Exception as e:
        print("Failed to open (maybe empty)", file)
        return 0

    var_arrays = []
    for var in var_list:
        cutVAR = events.arrays([var], cuts)
        VARTemp = [next(iter(d.values())) for d in ak.to_list(cutVAR)]
        VAR = [item for sublist in VARTemp for item in sublist]
        var_arrays.append(np.array(VAR, dtype="d"))
    
    return var_arrays

# Set up argument parser
parser = argparse.ArgumentParser(description='Process HFO quantity.')
parser.add_argument('--hfo_qnt', type=int, required=False, help='The desired HFO quantity to filter by.',default=0)
parser.add_argument('--fit_range', type=int, nargs=2, required=False, help='The lower and upper bound of the integral fit range.',default=[300, 400])
parser.add_argument('--voltages', type=int, nargs=2, required=False, help='The lower and upper bound of the VGEM voltages to filter by.', default=[300, 500])
args = parser.parse_args()
hfo_qnt = args.hfo_qnt
fit_range = args.fit_range

runlog=cy.read_cygno_logbook(sql=True, tag='MAN', start_run=25689, end_run=100000000, verbose=False)
filtered = filter_runlog_by_hfo_c(runlog, hfo_qnt)
# Extract the number right after "- GEM" in the 'run_description' column
filtered['gem_number'] = filtered['run_description'].str.extract(r'- GEM\s*(\d+)', expand=False)
print(filtered)

# Create the Reco directory if it doesn't exist
os.makedirs('Reco', exist_ok=True)

# Generate a list of the names of the resulting ROOT files
resulting_files = []
VGEMs = filtered['gem_number'].unique()
for gem in VGEMs:
    output_file = f"Reco/HFO{hfo_qnt}_VGEM{gem}.root"
    resulting_files.append(output_file)

# Define the minimum and maximum VGEM values
min_vgem, max_vgem = args.voltages
# Filter the VGEMs to keep only those within the specified range
VGEMs = [gem for gem in VGEMs if min_vgem <= int(gem) <= max_vgem]

# Check if all reco_run files are present in the Reco directory
all_reco_files_present = all(os.path.exists(f"Reco/reco_run{run_number}_3D.root") for run_number in filtered['run_number'])
# Check if all resulting files are present in the Reco directory
all_files_present = all(os.path.exists(file) for file in resulting_files)

# If not all files are present, enter the cycle
if not all_reco_files_present and not all_files_present:
    # Iterate over the filtered dataframe and download the files
    for run_number in filtered['run_number']:
        url = f"https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/cygno-analysis/MANGO_RECO/reco_run{run_number}_3D.root"
        output_path = f"Reco/reco_run{run_number}_3D.root"
        os.system(f"wget -O {output_path} {url}")
if not all_files_present:
    for gem in VGEMs:
        output_file = f"Reco/HFO{hfo_qnt}_VGEM{gem}.root"
        input_files = " ".join(f"Reco/reco_run{run_number}_3D.root" for run_number in filtered[filtered['gem_number'] == gem]['run_number'])
        #print(f"hadd -f {output_file} {input_files}")
        os.system(f"hadd -f {output_file} {input_files}")

#! Camera analysis
cuts="(sc_integral>0) & (sc_integral<300000) & (sc_width/sc_length>0.6) & (sc_width/sc_length<1) & (sc_tgausssigma>3)"
variables=["sc_integral","sc_width/sc_length","sc_tgausssigma","sc_nhits","sc_integral/sc_nhits","sc_length","sc_width"]
# Create a nested dictionary with VGEM elements as the top-level keys.
# For each gem, initialize a dictionary for each variable #!results[gem][variable][histo/array]
results = {gem: {var: {"array": None, "histogram": None} for var in variables} for gem in VGEMs}

for gem in tqdm(VGEMs):
    variables_returned = get_vars(variables, f"Reco/HFO{hfo_qnt}_VGEM{gem}.root", cuts)
    variable_dict = dict(zip(variables, variables_returned))
    
    for var in variables:
        # Save the array for this variable and gem.
        results[gem][var]["array"] = variable_dict[var]
        results[gem][var]["histogram"] = hist(variable_dict[var],f"{var} for VGEM{gem}",channels=100,write=False)

# Create a dictionary to store analysis results for each VGEM
analysis_results = {gem: {} for gem in VGEMs}

main_file=ROOT.TFile(f"HFO{hfo_qnt}.root","RECREATE")
for var in variables: main_file.mkdir(var.replace("/","_"))

for gem in VGEMs:
    for var in variables:
        root_path=var.replace("/","_")
        main_file.cd(root_path)
        h=results[gem][var]["histogram"]
        h_tgasusssigma=results[gem]["sc_tgausssigma"]["histogram"]
        if var == "sc_integral":
            
            # hfo 0%
            if int(gem)>360: limits=[0,300000]
            else: limits=[0,5000]
            # hfo 1%
            #if int(gem)>390: limits=[4000,100000]
            #else: limits=[0,10000]
                
            f1=ROOT.TF1("f1","gaus",limits[0],limits[1])
            h.Fit(f1,"RQ")
            h.Write()
            analysis_results[gem].update({"mean": f1.GetParameter(1), "mean_err": f1.GetParError(1), "sigma": f1.GetParameter(2), "sigma_err": f1.GetParError(2)})

        if var=="sc_tgausssigma":
            if int(gem)>410: limits=[5,20]
            else: limits=[0,10]
                
            f1=ROOT.TF1("f1","gaus",limits[0],limits[1])
            h_tgasusssigma.Fit(f1,"RQ")
            h_tgasusssigma.Write()
            analysis_results[gem].update({"sc_tgausssigma": f1.GetParameter(1), "sc_tgausssigma_err": f1.GetParError(1)})


        else:
            h.Write()

means=[analysis_results[gem]["mean"] for gem in VGEMs]
mean_errs=10*[analysis_results[gem]["mean_err"] for gem in VGEMs]
sigmas=[analysis_results[gem]["sigma"] for gem in VGEMs]
sigma_errs=[analysis_results[gem]["sigma_err"] for gem in VGEMs]
vgem_err=[1]*len(VGEMs)
# Compute resolution and relative error
resolutions = [sigma / mean if mean != 0 else 0 for sigma, mean in zip(sigmas, means)]
resolution_errs = [(sigma / mean) * ((sigma_err / sigma) + (mean_err / mean))
    if mean != 0 and sigma != 0 else 0
    for sigma, mean, sigma_err, mean_err in zip(sigmas, means, sigma_errs, mean_errs)]

main_file.cd()
# Create and write the resolution graph
grah_res=grapherr(VGEMs, resolutions,vgem_err, resolution_errs,"VGEM [V]", "Resolution RMS (%)", name="Resolution vs VGEM",markerstyle=21,markersize=2)
graph_int=grapherr(VGEMs, means, vgem_err, mean_errs,"VGEM [V]", "Integral", name="Integral vs VGEM",markerstyle=21,write=False,markersize=2)
expo_fit=ROOT.TF1("expo_fit","expo",fit_range[0],fit_range[1])
graph_int.Fit(expo_fit,"RQ")
graph_int.Write()

fit_params = expo_fit.GetParameters()
fit_errors = expo_fit.GetParErrors()
# Create a TPaveText object to display the fit parameters.
fit_text = ROOT.TPaveText(0.15, 0.8, 0.45, 0.9, "NDC")
fit_text.SetFillStyle(0)  # No fill
fit_text.SetBorderSize(0)  # No border
fit_text.SetFillColorAlpha(ROOT.kWhite, 0)  # Fully transparent fill color
fit_text.SetTextAlign(12)
fit_text.AddText(f"[0]: {fit_params[0]:.2e} +/- {fit_errors[0]:.2e}")
fit_text.AddText(f"[1]: {fit_params[1]:.2e} +/- {fit_errors[1]:.2e}")
# Add chi2/ndf to the TPaveText object
chi2 = expo_fit.GetChisquare()
ndf = expo_fit.GetNDF()
if ndf != 0: fit_text.AddText(f"Chi2/NDF: {chi2/ndf:.2e}")

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

# Extract tgaussigma values and their errors for each VGEM
tgaussigma_values = [analysis_results[gem]["sc_tgausssigma"] for gem in VGEMs]
tgaussigma_errors = [analysis_results[gem]["sc_tgausssigma_err"] for gem in VGEMs]

# Create and write the tgaussigma graph
graph_tgaussigma = grapherr(VGEMs, tgaussigma_values, vgem_err, tgaussigma_errors, "VGEM [V]", "tgaussigma", name="tgaussigma vs VGEM", markerstyle=21, markersize=2)
graph_tgaussigma.Write()

plot_tgrapherrors(grah_res, f"HFO{hfo_qnt}_Resolution_vs_VGEM.png")
plot_tgrapherrors(graph_int, f"HFO{hfo_qnt}_Integral_vs_VGEM.png",setLog=True,pavetext=fit_text)
plot_tgrapherrors(graph_tgaussigma, f"HFO{hfo_qnt}_tgaussigma_vs_VGEM.png")