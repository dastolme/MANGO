Inside Spectra/Florian there are the original corrected and calibrated spectra from Florian for all the gases

Inside Spectra there are the spectra of Florian remastered to have a point every 2 nm, and the spectra of QE of the cameras some PMTs and the trnsparency of Mylar and PMMA. For the spectra the names are coded as <gas>_<pressure>.txt, where gas can be He_CF4 or He_CF4_HFO1 etc..
The code Refine_histo was used to pass from the spectra inside Florian to the one outside.

In the rest of the folder you have a file ROOT containing the emission spectrum and the "survived" spectrum for a variety of combinations of gas, detector, window and pressure. Names are coded as Effspec_<gas>_<pressure>_<detector>_<window>.root.
The code EstimateQE starts from the spectra inside spectra and produces one of the ROOT files following what the Config.txt tells it to do. It also prints the effective QE and the survived photons per secondary electron.