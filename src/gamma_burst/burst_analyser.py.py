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
        self.available_binning_data_no_evolution = self.get_available_binning_no_evolution()
        self.available_SNR_data_no_evolution = self.get_available_SNR_no_evolution()
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
                destDir=folder_path,
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
    
    def get_available_binning_no_evolution(self)->list:
        """Print available binning. Only available for BAT."""
        binning_list = [
            key for key in self.burst_analyser_data[Instrument.BAT_Sensor_NoEvolution]['Binning']
            if 'TimeBins' in key
        ]
        return  binning_list

    def get_available_SNR_no_evolution(self)->list:
        """Print available binning. Only available for BAT."""
        binning_list = [
            key for key in self.burst_analyser_data[Instrument.BAT_Sensor_NoEvolution]['Binning']
            if 'SNR' in key
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
    
    def retrieve_time_and_count_rate_no_evolution(self, filter: str, time_scale : tuple[float, float] = None)->tuple:
        if filter not in self.available_binning_data_no_evolution:
            raise ValueError('Wrong Binning')
        
        data = self.burst_analyser_data[Instrument.BAT_Sensor_NoEvolution]
        filtered_data = data[filter]['BATBand']
        time = filtered_data['Time']
        ecf_data = data['ECFs']['ObservedFlux']
        observed_flux_rate = filtered_data['Flux'] / ecf_data

        return (time, observed_flux_rate)


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
        
        min_removed_flux_percentage = [element - min(cumulated_flux) for element in cumulated_flux]
        cumulated_flux_percentage = [element / max(min_removed_flux_percentage) for element in min_removed_flux_percentage]
        
        plt.figure(figsize=(10, 6))
        plt.plot(time, cumulated_flux_percentage)
        plt.xlabel('Time (s)')
        plt.ylabel('Percentage of cumulated flux emitted in %')
        plt.title(f'Time vs Percentage of flux emitted {filter} (max value = {cumulated_flux_value:.3e}erg cm-2 s-1) (15keV to 150keV)')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def plot_time_and_cumulated_flux_no_evolution(self, filter: str, time_scale : tuple[float, float] = None)->None:
        data = self.burst_analyser_data[Instrument.BAT_Sensor_NoEvolution][filter]
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
        
        min_removed_flux_percentage = [element - min(cumulated_flux) for element in cumulated_flux]
        cumulated_flux_percentage = [element / max(min_removed_flux_percentage) for element in min_removed_flux_percentage]
        
        plt.figure(figsize=(10, 6))
        plt.plot(time, cumulated_flux_percentage)
        plt.xlabel('Time (s)')
        plt.ylabel('Percentage of cumulated flux emitted in %')
        plt.title(f'Time vs Percentage of flux emitted {filter} (max value = {cumulated_flux_value:.3e}erg cm-2 s-1) (15keV to 150keV)')
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
        plt.title(f'Light Curve for {self.grb_name}, {snr} (15keV to 150keV) nb_data = {len(count_rate)}')
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
        plt.title(f'Light Curve for {self.grb_name}, {binning} (15keV to 150keV)')
        plt.legend()
        plt.show()
    
    def plot_light_curve_binning_no_evolution(self,binning: str):
        if binning not in self.available_binning_data_no_evolution:
            raise ValueError('Wrong Binning')
        
        data = self.burst_analyser_data[Instrument.BAT_Sensor_NoEvolution]
        filtered_data = data[binning]['BATBand']
        time = filtered_data['Time']
        ecf_data = data['ECFs']['ObservedFlux']
        observed_flux_rate = filtered_data['Flux'] / ecf_data


        plt.figure(figsize=(10, 6))
        plt.plot(time, observed_flux_rate, label=f'{binning}')
        plt.xlabel('Time (s)')
        plt.ylabel('Rate (cts/s)')
        plt.title(f'Light Curve for {self.grb_name}, {binning} (15keV to 150keV) nb_point = {len(observed_flux_rate)}')
        plt.legend()
        plt.show()
    
    def plot_light_curve_SNR_no_evolution(self,snr: str):
        if snr not in self.available_SNR_data_no_evolution:
            raise ValueError('Wrong Binning')
        
        data = self.burst_analyser_data[Instrument.BAT_Sensor_NoEvolution]
        filtered_data = data[snr]['BATBand']
        time = filtered_data['Time']
        ecf_data = data['ECFs']['ObservedFlux']
        observed_flux_rate = filtered_data['Flux'] / ecf_data


        plt.figure(figsize=(10, 6))
        plt.plot(time, observed_flux_rate, label=f'{snr}')
        plt.xlabel('Time (s)')
        plt.ylabel('Rate (cts/s)')
        plt.title(f'Light Curve for {self.grb_name}, {snr} (15keV to 150keV)')
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
        plt.title(f'HR. Mean value = {np.mean(hr)} (15keV to 150keV) nb_data = {len(hr)}')
        plt.legend()
        plt.show()
    
    def plot_light_curve_gamma(self,time_scale : tuple[float, float] = None, plot_error: bool = False):
        data = self.burst_analyser_data[Instrument.BAT_Sensor]['HRData']
        filtered_data = data
        if time_scale is not None:
            filtered_data = data.loc[(data['Time'] >= time_scale[0]) & (data['Time'] <= time_scale[1])]
        time = filtered_data['Time']
        gamma = filtered_data['Gamma']

        plt.figure(figsize=(10, 6))
        plt.plot(time, gamma, label='Gamma')
        plt.xlabel('Time (s)')
        plt.ylabel('Gamma')
        plt.title(f'Gamma. Mean value = {np.mean(gamma):.3f} (15keV to 150keV)')
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
            axs[idx].set_title(f'Light Curve for {self.grb_name}, {binning} (15keV to 150keV)')
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
            axs[idx].set_title(f'Light Curve for {self.grb_name}, {binning} (15keV to 150keV)')
            axs[idx].legend()
            axs[idx].grid(True)
        for j in range(idx + 1, len(axs)):
            fig.delaxes(axs[j])
        plt.tight_layout()
        plt.show()

    def plot_spectra(self, filter: str, energy_scale_kev: tuple[float, float], delta_e: float)->None:
        data = self.burst_analyser_data[Instrument.BAT_Sensor][filter]['BATBand']
        gamma_mean = np.mean(data['Gamma'])
        flux_mean = np.mean(data['Flux'])
        ecf_mean = np.mean(data['ECF'])
        energy = np.arange(energy_scale_kev[0], energy_scale_kev[1], delta_e)
        count = [flux_mean/ecf_mean * (energy_value/50) ** -gamma_mean for energy_value in energy]
        plt.plot(energy, count)
        plt.xlabel('Energy (kev)')
        plt.ylabel('Flux (cts/s/kev)')
        plt.xscale('log')
        plt.yscale('log')
        plt.title(f'Spectra for {self.grb_name}')
        plt.legend()
        plt.show()

def check_uniform_sampling(time, tolerance=1e-6):
    """
    Vérifie si l'échantillonnage des temps est uniforme.
    
    Args:
        time (numpy.ndarray): Array des temps.
        tolerance (float): Tolérance pour considérer l'échantillonnage comme uniforme.
        
    Returns:
        bool: True si uniforme, False sinon.
    """
    delta_ts = np.diff(time)
    return np.all(np.abs(delta_ts - delta_ts[0]) < tolerance)


def calculate_fft(time, counts):
    """
    Calcule la transformée de Fourier des comptages de photons et convertit les fréquences en énergie.
    
    Args:
        time (list or numpy.ndarray): Liste des temps.
        counts (list or numpy.ndarray): Liste des comptages de photons.
        
    Returns:
        tuple: (énergies en keV, magnitude de la FFT)
    """
    time = np.array(time)
    counts = np.array(counts)
    
    counts_uniform = counts
    delta_t = np.mean(np.diff(time))
    N = len(counts_uniform)
    fft_counts = np.fft.fft(counts_uniform)
    freqs = np.fft.fftfreq(N, d=delta_t)
    
    positive_freqs = freqs[:N//2]
    positive_fft = fft_counts[:N//2]
    
    h_keV_s = 4.135667696e-18  # keV·s
    
    energies_keV = h_keV_s * positive_freqs * 1e3
    
    magnitude = np.abs(positive_fft)
    
    return energies_keV, magnitude

def plot_fft(energies_keV, magnitude, title="Transformée de Fourier des Comptages de Photons"):
    """
    Affiche la transformée de Fourier en fonction de l'énergie.
    
    Args:
        energies_keV (numpy.ndarray): Array des énergies en keV.
        magnitude (numpy.ndarray): Array de la magnitude de la FFT.
        title (str): Titre du graphique.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(energies_keV, magnitude, color='blue')
    plt.xlabel('Énergie (keV)')
    plt.ylabel('Magnitude de la FFT')
    plt.title(title)
    plt.grid(True)
    plt.xlim(left=0)  # Limiter l'axe des x à des énergies positives
    plt.show()

if __name__ == '__main__':
    burst_analyser = BurstAnalyser('GRB 101225A')
    # burst_analyser = BurstAnalyser('GRB 210905A')
    burst_analyser.plot_light_curve_binning_no_evolution('TimeBins_64ms')
    # burst_analyser.plot_light_curve_binning_no_evolution('TimeBins_1s')
    # burst_analyser.plot_light_curve_binning_no_evolution('TimeBins_10s')

    # burst_analyser.plot_light_curve_snr('SNR4')
    # burst_analyser.plot_light_curve_snr('SNR5')
    # burst_analyser.plot_light_curve_snr('SNR7')

    # burst_analyser.plot_time_and_cumulated_flux_no_evolution('TimeBins_10s', (0, 10000))
    # burst_analyser.plot_light_curve_hr()
    # # burst_analyser.plot_time_and_cumulated_flux('SNR4')

    # # print(burst_analyser.available_binning_data)

    # burst_analyser.plot_spectra('TimeBins_10s', (0, 1e5), 10)

    time, count_rate = burst_analyser.retrieve_time_and_count_rate_no_evolution('TimeBins_64ms')
    energies_keV, magnitude = calculate_fft(time, count_rate)
    
    plot_fft(energies_keV, magnitude)
