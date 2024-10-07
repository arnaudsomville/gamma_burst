"""Spectra class."""

from pathlib import Path
from matplotlib import pyplot as plt
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
    
    def plot_light_curve_snr(self,snr: str, time_scale : tuple[float, float] = None, plot_error: bool = False):
        if snr not in self.available_SNR_data:
            raise ValueError('Wrong SNR')
        data = self.burst_analyser_data[Instrument.BAT_Sensor][snr]
        filtered_data = data['ObservedFlux']
        if time_scale is not None:
            filtered_data = data['ObservedFlux'].loc[(data['ObservedFlux']['Time'] >= time_scale[0]) & (data['ObservedFlux']['Time'] <= time_scale[1])]
        time = filtered_data['Time']
        # xrt_rate = filtered_data['XRTBand']['Flux']
        # bat_rate = filtered_data['BATBand']['Flux']
        observed_flux_rate = filtered_data['Flux']
        
        if plot_error:
            error = filtered_data.get('RateErr', 0)
            plt.figure(figsize=(10, 6))
            plt.errorbar(time, observed_flux_rate, yerr=error, fmt='o-')
        else:
            plt.figure(figsize=(10, 6))
            # plt.plot(time, xrt_rate, label='XRTBand')
            # plt.plot(time, bat_rate, label='BATBand')
            plt.plot(time, observed_flux_rate, label='ObservedFlux')

        plt.xlabel('Time (s)')
        plt.ylabel('Rate (cts/s)')
        plt.title(f'Light Curve for {self.grb_name}')
        plt.legend()
        plt.show()
    
    def plot_light_curve_binning(self,binning: str, time_scale : tuple[float, float] = None, plot_error: bool = False):
        if binning not in self.available_binning_data:
            raise ValueError('Wrong Binning')
        data = self.burst_analyser_data[Instrument.BAT_Sensor][binning]
        filtered_data = data['ObservedFlux']
        if time_scale is not None:
            filtered_data = data['ObservedFlux'].loc[(data['ObservedFlux']['Time'] >= time_scale[0]) & (data['ObservedFlux']['Time'] <= time_scale[1])]
        time = filtered_data['Time']
        # xrt_rate = filtered_data['XRTBand']['Flux'] * 0.16e4
        # bat_rate = filtered_data['BATBand']['Flux'] * 0.16e4
        observed_flux_rate = filtered_data['Flux'] * 0.16e4
        
        if plot_error:
            flux_rate_pos = filtered_data['Flux'] * 0.16e4
            flux_rate_neg = filtered_data['Flux'] * 0.16e4
            flux_rate_pos_err = flux_rate_pos - observed_flux_rate
            flux_rate_neg_err = flux_rate_neg - observed_flux_rate
            flux_rate_err = []
            for pos, neg in zip(flux_rate_pos_err, flux_rate_neg_err):
                mean_error = (pos-neg)/2
                flux_rate_err.append(mean_error)
            error = filtered_data.get('FluxErr', 0)
            plt.figure(figsize=(10, 6))
            plt.errorbar(time, observed_flux_rate, yerr=flux_rate_err, fmt='o-')
        else:
            plt.figure(figsize=(10, 6))
            # plt.plot(time, xrt_rate, label='XRTBand')
            # plt.plot(time, bat_rate, label='BATBand')
            plt.plot(time, observed_flux_rate, label='ObservedFlux')

        plt.xlabel('Time (s)')
        plt.ylabel('Rate (cts/s)')
        plt.title(f'Light Curve for {self.grb_name}')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    burst_analyser = BurstAnalyser('GRB 081118')
    burst_analyser.print_fields(Instrument.XRT_Sensor)
    print(burst_analyser.available_binning_data)
    print(burst_analyser.available_SNR_data)
    # burst_analyser.plot_light_curve_binning('TimeBins_10s', (0,60), plot_error=True)
    burst_analyser.plot_light_curve_snr('SNR6',(0,60), plot_error=False)
    burst_analyser.plot_light_curve_binning('TimeBins_64ms',(0,60), plot_error=False)
    burst_analyser.plot_light_curve_binning('TimeBins_1s',(0,60), plot_error=False)
    burst_analyser.plot_light_curve_binning('TimeBins_10s',(0,60), plot_error=False)