# Anlysis tool for HFO test with MANGO at CERN

cuts="(sc_integral>0) & (sc_integral<300000) & (sc_width/sc_length>0.6) & (sc_width/sc_length<1) & (sc_tgausssigma>3)"

anal_GainScan_CAM.py --hfo_qnt 0 
    if int(gem)>360: limits=[0,300000]
    else: limits=[0,5000]

anal_GainScan_CAM.py --hfo_qnt 1 --voltages 390 500 --fit_range 390 420
    if int(gem)>390: limits=[4000,100000]
    else: limits=[0,10000]