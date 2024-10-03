from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
from swifttools.ukssdc import plotLightCurve
import swifttools.ukssdc.data.GRB as udg
import pickle

def recover_light_curves(grb_name: str) -> dict:
    """Recover light curve data.

    Args:
        grb_name (str): GRB's name.
    """
    home_path = Path.home().joinpath(".gamma_burst")
    if not home_path.exists():
        home_path.mkdir(parents=True, exist_ok=True)
    
    folder_path = home_path.joinpath(grb_name).joinpath('light_curve')
    
    cache_file = folder_path / 'lc_data.pkl'
    
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
        
        lc_data = udg.getLightCurves(
            GRBName=grb_name,
            returnData=True,
            saveData=True,
            silent=False
        )
        
        with open(cache_file, 'wb') as f:
            pickle.dump(lc_data, f)
    else:
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                lc_data = pickle.load(f)
        else:
            lc_data = udg.getLightCurves(
                GRBName=grb_name,
                destDir=folder_path,
                returnData=True,
                saveData=True,
                silent=False
            )
            with open(cache_file, 'wb') as f:
                pickle.dump(lc_data, f)
    
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

def plot_light_curve(grb_name: str, mode: str, time_scale : tuple[float, float]):
    
    lc_data = recover_light_curves(grb_name)[mode]
    lc_data_filtered = lc_data.loc[(lc_data['Time'] >= time_scale[0]) & (lc_data['Time'] <= time_scale[1])]
    time = lc_data_filtered['Time']
    rate = lc_data_filtered['Rate']
    error = lc_data_filtered.get('RateErr', 0)
    
    plt.plot(time, rate)
    # plt.errorbar(time, rate, yerr=error, fmt='o-', label=mode)
    plt.xlabel('Time (s)')
    plt.ylabel('Rate (cts/s)')
    plt.title(f'Light Curve for {grb_name} in {mode} mode')
    plt.legend()
    plt.show()

def print_fields(dict):
    for key in dict:
        data = dict[key]
        if isinstance(data, pd.DataFrame):
            print(f"{key} : {data.columns}")
        else:
            print(f"{key} : {data}")

if __name__ == '__main__':
    lc_dict = recover_light_curves('GRB 101225A')
    spectra_dict = recover_spectra('GRB 101225A')
    print_fields(lc_dict)
    # print(recover_spectra('GRB 101225A'))

    plot_light_curve('GRB 101225A', 'WTHard_incbad', (0, 3000))