"""Spectra class."""

from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import swifttools.ukssdc.data.GRB as udg
import pickle

from gamma_burst.eumerations import Instrument

class BurstAnalyser:

    def __init__(self, grb_name: str) -> None:
        self.grb_name: str = grb_name
        self.burst_analyser_data = self.recover_burst_analyser_data()
        self.available_SNR_data = self.get_available_SNR()
        self.available_binning_data = self.get_available_binning()
        pass

    def recover_burst_analyser_data(self) -> dict:
        """Recover spectra data.

        Args:
            grb_name (str): GRB's name.
        """
        home_path = Path.home().joinpath(".gamma_burst")
        if not home_path.exists():
            home_path.mkdir(parents=True, exist_ok=True)
        
        folder_path = home_path.joinpath(self.grb_name).joinpath('burst_analyser')
        
        cache_file = folder_path / 'burst_analyser.pkl'
        
        if not cache_file.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            
            burst_data = udg.getBurstAnalyser(
                GRBName=self.grb_name,
                returnData=True,
                saveData=True,
                silent=False
            )
            
            with open(cache_file, 'wb') as f:
                pickle.dump(burst_data, f)
        else:
            with open(cache_file, 'rb') as f:
                burst_data = pickle.load(f)
        self.burst_analyser_data = burst_data
        return burst_data

    def print_fields(self, instrument: Instrument):
        for key in self.burst_analyser_data[instrument]:
            data = self.burst_analyser_data[instrument][key]
            if isinstance(data, pd.DataFrame):
                print(f"Dataset {key} : {data.columns}")
            else:
                print(f"{key}")
    
    def get_available_SNR(self)->list:
        """Print available binning. Only available for BAT."""
        snr_list = []
        for key in self.burst_analyser_data[Instrument.BAT_Sensor]:
            if 'SNR' in key:
                snr_list.append(key)
        return snr_list
    
    def get_available_binning(self)->list:
        """Print available binning. Only available for BAT."""
        binning_list = [
            key for key in self.burst_analyser_data[Instrument.BAT_Sensor]['Binning']
            if 'TimeBins' in key
        ]
        return  binning_list
    
    def retrieve_time_and_count_rate(self, filter: str, time_scale : tuple[float, float] = None)->tuple:
        data = self.burst_analyser_data[Instrument.BAT_Sensor][filter]
        filtered_data = data['BATBand']
        if time_scale is not None:
            filtered_data = data['BATBand'].loc[(data['BATBand']['Time'] >= time_scale[0]) & (data['BATBand']['Time'] <= time_scale[1])]
        time = filtered_data['Time']
        observed_flux_rate = filtered_data['Flux']
        ecf_data = filtered_data['ECF']

        count_rate = [flux/ecf for flux, ecf in zip(observed_flux_rate, ecf_data)]

        return (time, count_rate)

    def plot_time_and_cumulated_flux(self, filter: str, time_scale : tuple[float, float] = None)->None:
        data = self.burst_analyser_data[Instrument.BAT_Sensor][filter]
        filtered_data = data['BATBand']
        if time_scale is not None:
            filtered_data = data['BATBand'].loc[(data['BATBand']['Time'] >= time_scale[0]) & (data['BATBand']['Time'] <= time_scale[1])]
        time = filtered_data['Time']
        observed_flux_rate = filtered_data['Flux']

        cumulated_flux_value = 0
        cumulated_flux = []
        for flux_value in observed_flux_rate:
            if flux_value > 0:
                cumulated_flux_value = cumulated_flux_value + flux_value
            cumulated_flux.append(cumulated_flux_value)
        
        cumulated_flux_percentage = [element / cumulated_flux_value for element in cumulated_flux]
        plt.figure(figsize=(10, 6))
        plt.plot(time, cumulated_flux_percentage)
        plt.xlabel('Time (s)')
        plt.ylabel('Percentage of cumulated flux emitted in %')
        plt.title(f'Time vs Percentage of flux emitted (max value = {cumulated_flux_value}erg cm-2 s-1)')
        plt.legend()
        plt.grid(True)
        plt.show()

    
    def plot_light_curve_snr(self,snr: str, time_scale : tuple[float, float] = None, plot_error: bool = False):
        if snr not in self.available_SNR_data:
            raise ValueError('Wrong SNR')
        time, count_rate = self.retrieve_time_and_count_rate(snr,time_scale )
        plt.figure(figsize=(10, 6))
        plt.plot(time, count_rate, label='BATBand')
        plt.xlabel('Time (s)')
        plt.ylabel('Rate (cts/s)')
        plt.title(f'Light Curve for {self.grb_name}, {snr}')
        plt.legend()
        plt.show()
    
    
    def plot_light_curve_binning(self,binning: str, time_scale : tuple[float, float] = None, plot_error: bool = False):
        if binning not in self.available_binning_data:
            raise ValueError('Wrong Binning')
        time, count_rate = self.retrieve_time_and_count_rate(binning,time_scale )
        plt.figure(figsize=(10, 6))
        plt.plot(time, count_rate, label=f'{binning}')
        plt.xlabel('Time (s)')
        plt.ylabel('Rate (cts/s)')
        plt.title(f'Light Curve for {self.grb_name}, {binning}')
        plt.legend()
        plt.show()

    def plot_light_curve_hr(self,time_scale : tuple[float, float] = None, plot_error: bool = False):
        data = self.burst_analyser_data[Instrument.BAT_Sensor]['HRData']
        filtered_data = data
        if time_scale is not None:
            filtered_data = data.loc[(data['Time'] >= time_scale[0]) & (data['Time'] <= time_scale[1])]
        time = filtered_data['Time']
        hr = filtered_data['HR']

        plt.figure(figsize=(10, 6))
        plt.plot(time, hr, label='HR')
        plt.xlabel('Time (s)')
        plt.ylabel('Hardness Ratio')
        plt.title(f'HR. Mean value = {np.mean(hr)}')
        plt.legend()
        plt.show()
    
    def subplot_all_binning_lc(self, time_scale: tuple[float, float] = None) -> None:
        """
        Trace les light curves pour tous les types de binning disponibles dans une grille de subplots.
        
        Args:
            time_scale (tuple[float, float], optional): Intervalle de temps à tracer (start, stop).
        """
        nb_plot = len(self.available_binning_data)
        if nb_plot < 1:
            raise ValueError("No available data.")
        
        ncols = 2
        nrows = int(np.ceil(nb_plot / ncols))
        fig, axs = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows))
        axs = axs.flatten()
        for idx, binning in enumerate(self.available_binning_data):
            time, count_rate = self.retrieve_time_and_count_rate(binning, time_scale)
            axs[idx].plot(time, count_rate, 'o-', label=f'{binning}', markersize=4)
            axs[idx].set_xlabel('Time (s)')
            axs[idx].set_ylabel('Rate (cts/s)')
            axs[idx].set_title(f'Light Curve for {self.grb_name}, {binning}')
            axs[idx].legend()
            axs[idx].grid(True)
        for j in range(idx + 1, len(axs)):
            fig.delaxes(axs[j])
        plt.tight_layout()
        plt.show()
    
    def subplot_all_snr_lc(self, time_scale: tuple[float, float] = None) -> None:
        """
        Trace les light curves pour tous les types de binning disponibles dans une grille de subplots.
        
        Args:
            time_scale (tuple[float, float], optional): Intervalle de temps à tracer (start, stop).
        """
        nb_plot = len(self.available_SNR_data)
        if nb_plot < 1:
            raise ValueError("No available data.")
        
        ncols = 2
        nrows = int(np.ceil(nb_plot / ncols))
        fig, axs = plt.subplots(nrows, ncols, figsize=(10, 5 * nrows))
        axs = axs.flatten()
        for idx, binning in enumerate(self.available_SNR_data):
            time, count_rate = self.retrieve_time_and_count_rate(binning, time_scale)
            axs[idx].plot(time, count_rate, 'o-', label=f'{binning}', markersize=4)
            axs[idx].set_xlabel('Time (s)')
            axs[idx].set_ylabel('Rate (cts/s)')
            axs[idx].set_title(f'Light Curve for {self.grb_name}, {binning}')
            axs[idx].legend()
            axs[idx].grid(True)
        for j in range(idx + 1, len(axs)):
            fig.delaxes(axs[j])
        plt.tight_layout()
        plt.show()
if __name__ == '__main__':
    burst_analyser = BurstAnalyser('GRB 080623')
    # burst_analyser = BurstAnalyser('GRB 101225A')
    # burst_analyser.plot_light_curve_binning('TimeBins_10s', (0,3000), plot_error=True)
    # burst_analyser.subplot_all_binning_lc((0,1000))
    burst_analyser.plot_light_curve_hr()
    burst_analyser.subplot_all_snr_lc((0,2000))
    burst_analyser.plot_time_and_cumulated_flux('SNR5')
