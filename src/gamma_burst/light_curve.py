"""LightCurve class."""

from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
import swifttools.ukssdc.data.GRB as udg
import pickle

from gamma_burst.eumerations import ObservationMode
class XRTLightCurve:

    def __init__(self, grb_name: str) -> None:
        self.grb_name: str = grb_name
        self.lc_data = self.recover_light_curves()
        pass

    def recover_light_curves(self) -> dict:
        """Recover light curve data.

        Args:
            grb_name (str): GRB's name.
        """
        home_path = Path.home().joinpath(".gamma_burst")
        if not home_path.exists():
            home_path.mkdir(parents=True, exist_ok=True)
        
        folder_path = home_path.joinpath(self.grb_name).joinpath('light_curve')
        
        cache_file = folder_path / 'lc_data.pkl'
        
        if not cache_file.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            
            lc_data = udg.getLightCurves(
                GRBName=self.grb_name,
                returnData=True,
                saveData=False,
                silent=False
            )
            
            with open(cache_file, 'wb') as f:
                pickle.dump(lc_data, f)
        else:
            lc_data = udg.getLightCurves(
                GRBName=self.grb_name,
                destDir=folder_path,
                returnData=True,
                saveData=False,
                silent=False
            )
            with open(cache_file, 'wb') as f:
                pickle.dump(lc_data, f)
        self.lc_data = lc_data
        return lc_data
    
    def plot_light_curve(self, mode: ObservationMode, time_scale : tuple[float, float] = None, plot_error: bool = False):
    
        lc_data = self.lc_data[mode + '_incbad']
        lc_data_filtered = lc_data
        if time_scale is not None:
            lc_data_filtered = lc_data.loc[(lc_data['Time'] >= time_scale[0]) & (lc_data['Time'] <= time_scale[1])]
        time = lc_data_filtered['Time']
        rate = lc_data_filtered['Rate']
        
        if plot_error:
            error = lc_data_filtered.get('RateErr', 0)
            plt.errorbar(time, rate, yerr=error, fmt='o-', label=mode)
        else:
            plt.plot(time, rate)
        plt.xlabel('Time (s)')
        plt.ylabel('Rate (cts/s)')
        plt.title(f'Light Curve for {self.grb_name} in {mode}')
        plt.legend()
        plt.show()

    def plot_light_curve_HR(self, mode: ObservationMode, time_scale : tuple[float, float] = None, plot_error: bool = False):
        if mode not in [ObservationMode.PC_Mode, ObservationMode.WT_Mode]:
            raise ValueError("Mode should be ObservationMode.PC_Mode or ObservationMode.WT_Mode")
        lc_data = self.lc_data[mode + 'HR_incbad']
        lc_data_filtered = lc_data
        if time_scale is not None:
            lc_data_filtered = lc_data.loc[(lc_data['Time'] >= time_scale[0]) & (lc_data['Time'] <= time_scale[1])]
        time = lc_data_filtered['Time']
        hr = lc_data_filtered['HR']
        if plot_error:
            error = lc_data_filtered.get('RateErr', 0)
            plt.errorbar(time, hr, yerr=error, fmt='o-', label=mode)
        else:
            plt.plot(time, hr)
        plt.xlabel('Time (s)')
        plt.ylabel('HR (NU)')
        plt.title(f'Hardness Ratio for {self.grb_name} in {mode} mode')
        plt.legend()
        plt.show()
    
    def print_fields(self):
        for key in self.lc_data:
            data = self.lc_data[key]
            if isinstance(data, pd.DataFrame):
                print(f"Dataset {key} : {data.columns}")
            else:
                print(f"{key} : {data}")

if __name__ == '__main__':
    lc = XRTLightCurve('GRB 101225A')
    # lc = XRTLightCurve('GRB 081118')
    lc.plot_light_curve(ObservationMode.WT_Mode)
    lc.plot_light_curve_HR(ObservationMode.WT_Mode)

    lc.print_fields()