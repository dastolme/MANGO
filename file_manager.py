import math
import cygno as cy
import pandas as pd
import awkward as ak
from tqdm import tqdm
import urllib3
import uproot
from concurrent.futures import ThreadPoolExecutor

class RecoRun:
    def __init__(self, type, dataframe):
        self.type = type
        self.dataframe = dataframe

class RecoRunManager:
    urllib3.disable_warnings()
    def __init__(self, run_start, run_end):
        self.runlog_df = cy.read_cygno_logbook(tag='mango', start_run=run_start,end_run=run_end)
        self.run_start = run_start
        self.run_end   = run_end

    def create_df_list(self, data_dir_path):

        param_list = ['run', 'event', 'pedestal_run', 'cmos_integral', 'cmos_mean', 'cmos_rms', 
                      'timestamp', 't_DBSCAN', 't_variables', 'lp_len', 't_pedsub', 't_saturation', 
                      't_zerosup', 't_xycut', 't_rebin', 't_medianfilter', 't_noisered', 'nSc', 
                      'sc_size', 'sc_nhits', 'sc_integral', 'sc_corrintegral', 'sc_rms', 'sc_energy', 
                      'sc_pathlength', 'sc_redpixIdx', 'nRedpix', 'redpix_ix', 'redpix_iy', 'redpix_iz', 
                      'sc_theta', 'sc_length', 'sc_width', 'sc_longrms', 'sc_latrms', 'sc_lfullrms', 
                      'sc_tfullrms', 'sc_lp0amplitude', 'sc_lp0prominence', 'sc_lp0fwhm', 'sc_lp0mean', 'sc_tp0fwhm', 
                      'sc_xmean', 'sc_ymean', 'sc_xmax', 'sc_xmin', 'sc_ymax', 'sc_ymin', 'sc_pearson', 'sc_tgaussamp',
                      'sc_tgaussmean', 'sc_tgausssigma', 'sc_tchi2', 'sc_tstatus', 'sc_lgaussamp', 'sc_lgaussmean',
                      'sc_lgausssigma', 'sc_lchi2', 'sc_lstatus']

        df_list = []

        print(f"Total runs: {self.run_end-self.run_start}")

        def read_single_file(data_dir_path, run_number):
            try:
                with uproot.open(f"{data_dir_path}reco_run{run_number}_3D.root") as root_file:
                    CMOS_root_file = root_file["Events"].arrays(param_list, library="ak")
                    df_data = ak.to_dataframe(CMOS_root_file)
                return df_data
            except FileNotFoundError as e:
                print("FileNotFound")
            except TimeoutError as e:
                print(f"Root file opening failed (run number = {run_number})")
        
        def read_many_files(run_list, data_dir_path):
            with ThreadPoolExecutor() as executor:
                df_list = list(tqdm(executor.map(read_single_file, data_dir_path, run_list, chunksize=50), total=len(run_list)))

            return df_list

        garbage_df = self.runlog_df.loc[self.runlog_df["run_description"].str.lower() == "garbage", ["run_number"]]
        run_list = [num for num in range(self.run_start,self.run_end) if garbage_df.empty or ~garbage_df.isin([num])]
        path_list = [data_dir_path for i in range(self.run_start,self.run_end)]
        df_list = read_many_files(run_list, path_list)
        
        return df_list
    
    def add_runtype_tag(self, df_list):

        run_list = []

        for df_data in tqdm(df_list):
            df = df_data[0]
            dfinfo = self.runlog_df[self.runlog_df["run_number"]==df['run'].unique()[0]].copy()
            if len(dfinfo) == 0:
                continue
            if isinstance(dfinfo["stop_time"].values[0], float):
                if math.isnan(dfinfo["stop_time"].values[0]):
                    continue

            run = {"is_pedestal": dfinfo['pedestal_run'].values[0]}
            match run:
                case {"is_pedestal": 1}:
                    run_list.append(RecoRun("pedestal", df_data))
                case {"is_pedestal": 0}:
                    run_list.append(RecoRun("data", df_data))

        return run_list
                

    def merge_and_create_hdf5(self, run_list, folder):

        run_type = ["pedestal", "data"]
        
        for type in run_type:
            store = pd.HDFStore(f"{folder}/{type}.h5", mode='w') 
            df_data_list = []   

            [df_data_list.append(run.dataframe) for run in run_list if run.type == type]
            
            if len(df_data_list) != 0:
                CMOS_df = pd.concat([dataframe for dataframe in df_data_list])
                store['CMOS'] = CMOS_df

            store.close()