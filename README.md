# Anlysis tool for HFO test with MANGO at CERN

## Digicalibration.py

Tool to calibrate the digitzer with calibration runs of fixed input charge

## anal_GainScan_CAM.py

tool to anlayise the light gain to 55Fe at different HFO

cuts="(sc_integral>0) & (sc_integral<300000) & (sc_width/sc_length>0.6) & (sc_width/sc_length<1) & (sc_tgausssigma>3)"

anal_GainScan_CAM.py --hfo_qnt 0 
    if int(gem)>360: limits=[0,300000]
    else: limits=[0,5000]

anal_GainScan_CAM.py --hfo_qnt 1 --voltages 390 500 --fit_range 390 420
    if int(gem)>390: limits=[4000,100000]
    else: limits=[0,10000]

## gainPico.py

tool to measure the electron gain of MANGO

## checkUniformiry.cxx

compile with g++ checkUniformity.cxx -o uniformity `root-config --cflags --libs` the run uniformity recofile.root

## chargeGainfromQUEST.py

from measurment summarized in LY_HeCF4.txt try to get the electronic gain with conversion

## CompareLY_HFO.py

makes the plot of different LY adn energy resolution measured for hte dfififerent HFO configurations

## QE_effective/Spectra/Refine_histo.cxx

compile with g++ Refine_histo.cxx -o <progname> `root-config --cflags --libs`. Runs as ./progname <path_to_spectrum> . Transforms a spectrum resampling and interpolating fixing a point every 2 nm. Output in Outfile_res.txt

## QE_effective/EstimateQE.cxx

compile with g++ EstimateQE.cxx -o <progname> `root-config --cflags --libs`. Runs as ./progname Config.txt . It starts from the spectra inside Spectra folder and produces a ROOT file containing the emission spectrum and the "survived" spectrum for a variety of combinations of gas, detector, window and pressure. The choice of parameters follows what the Config.txt tells it to do. It also prints the effective QE and the survived photons per secondary electron