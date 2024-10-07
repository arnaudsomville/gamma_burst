from pathlib import Path
from time import sleep
import pandas as pd
import swifttools.ukssdc.data.GRB as udg
import pickle

def recover_rebinned_light_curves(
        grb_name: str,
        bin_size: float,
        min_snr: float, 
        soft_min: float, 
        soft_max: float, 
        hard_min: float, 
        hard_max: float
    ) -> dict:
    """Recover light curve data.

    Args:
        grb_name (str): GRB's name.
    """
    home_path = Path.home().joinpath(".gamma_burst")
    if not home_path.exists():
        home_path.mkdir(parents=True, exist_ok=True)
    
    folder_path = home_path.joinpath(f"rebinned_{grb_name}_{min_snr}_{soft_min}_{soft_max}_{hard_min}_{hard_max}").joinpath('light_curve')
    
    cache_file = folder_path / 'lc_data.pkl'
    
    if not cache_file.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
        job_id = udg.rebinLightCurve(
            GRBName=grb_name,
            verbose=True,
            binMeth='time',
            pcCounts=15,
            wtCounts=15,
            dynamic=True,
            pcMaxGap=bin_size,
            wtMaxGap=bin_size,
            minSNR=min_snr,
            softLo=soft_min,
            softHi=soft_max,
            hardLo=hard_min,
            hardHi=hard_max,
            wtBinTime=2.51,
            pcBinTime=0.5,
            minCounts=15,
            binFact=1.5,
            rateFact=10,
            minEnergy=soft_min,
            maxEnergy=hard_max,
            pcHRBinTime=bin_size,
            wtHRBinTime=bin_size,
            returnData=True,
            saveData=False,
            silent=False
        )
        i=0
        while not udg.rebinComplete(job_id):
            if udg.checkRebinStatus(job_id)['statusText'] not in ['Running', 'Queued', 'Complete']:
                raise ValueError(f"Error : Rebinning status {udg.checkRebinStatus(job_id)['statusText']}")
            sleep(1)
            i+=1
            print(f'Waited {i}s')
        lc_data = udg.getRebinnedLightCurve(job_id)
        if lc_data is None:
            raise ValueError("Null lc_data")
        with open(cache_file, 'wb') as f:
            pickle.dump(lc_data, f)
    else:
        with open(cache_file, 'rb') as f:
            lc_data = pickle.load(f)
        
    
    return lc_data

def recover_spectra(grb_name: str) -> dict:
    """Recover spectra data.

    Args:
        grb_name (str): GRB's name.
    """
    home_path = Path.home().joinpath(".gamma_burst")
    if not home_path.exists():
        home_path.mkdir(parents=True, exist_ok=True)
    
    folder_path = home_path.joinpath(grb_name).joinpath('spectra')
    
    cache_file = folder_path / 'spectra_data.pkl'
    
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
        
        spectra_data = udg.getSpectra(
            GRBName=grb_name,
            returnData=True,
            saveData=True,
            silent=False
        )
        
        with open(cache_file, 'wb') as f:
            pickle.dump(spectra_data, f)
    else:
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                spectra_data = pickle.load(f)
        else:
            spectra_data = udg.getSpectra(
                GRBName=grb_name,
                destDir=folder_path,
                returnData=True,
                saveData=True,
                silent=False
            )
            with open(cache_file, 'wb') as f:
                pickle.dump(spectra_data, f)
    
    return spectra_data

def print_fields(dict):
    for key in dict:
        data = dict[key]
        if isinstance(data, pd.DataFrame):
            print(f"Dataset {key} : {data.columns}")
        else:
            print(f"{key} : {data}")
