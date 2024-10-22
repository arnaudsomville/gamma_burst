"""Spectra class."""

from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import swifttools.ukssdc.data.GRB as udg
import pickle

from gamma_burst.eumerations import ObservationMode

class XRTSpectra:

    def __init__(self, grb_name: str) -> None:
        self.grb_name: str = grb_name
        self.s_data = self.recover_spectra()
        pass

    def recover_spectra(self) -> dict:
        """Recover spectra data.

        Args:
            grb_name (str): GRB's name.
        """
        home_path = Path.home().joinpath(".gamma_burst")
        if not home_path.exists():
            home_path.mkdir(parents=True, exist_ok=True)
        
        folder_path = home_path.joinpath(self.grb_name).joinpath('spectra')
        
        cache_file = folder_path / 'spectra_data.pkl'
        
        if not cache_file.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            
            spectra_data = udg.getSpectra(
                GRBName=self.grb_name,
                returnData=True,
                saveData=True,
                silent=False
            )
            
            with open(cache_file, 'wb') as f:
                pickle.dump(spectra_data, f)
        else:
            with open(cache_file, 'rb') as f:
                spectra_data = pickle.load(f)

        self.s_data = spectra_data
        return spectra_data

    def print_fields(self):
        for key in self.s_data:
            data = self.s_data[key]
            if isinstance(data, pd.DataFrame):
                print(f"Dataset {key} : {data.columns}")
            else:
                print(f"{key} : {data}")

    def plot_spectra(self, mode: ObservationMode, energy_scale : tuple[float, float], delta_e: float = 1, plot_error: bool = False):
        if mode not in [ObservationMode.PC_Mode, ObservationMode.WT_Mode]:
            raise ValueError("Mode should be ObservationMode.PC_Mode or ObservationMode.WT_Mode")
        gamma = self.s_data['interval0'][mode]['PowerLaw']['Gamma']
        obs_flux = self.s_data['interval0'][mode]['PowerLaw']['ObsFlux']

        energy = np.arange(energy_scale[0], energy_scale[1], delta_e)
        flux = [obs_flux * (energy_value/50) ** -gamma for energy_value in energy]
        
        if plot_error:
            gamma_pos_err = self.s_data['interval0'][mode]['PowerLaw']['GammaNeg'] + gamma
            gamma_neg_err = self.s_data['interval0'][mode]['PowerLaw']['GammaPos'] + gamma
            obs_flux_pos_err = self.s_data['interval0'][mode]['PowerLaw']['ObsFluxPos'] + gamma
            obs_flux_neg_err = self.s_data['interval0'][mode]['PowerLaw']['ObsFluxNeg'] + gamma

            flux_error_neg = [obs_flux_neg_err * energy_value ** gamma_neg_err for energy_value in energy]
            flux_error_pos = [obs_flux_pos_err * energy_value ** gamma_pos_err for energy_value in energy]

            error = []
            for flux_value, error_pos, error_neg in zip(flux, flux_error_pos, flux_error_neg):
                error.append(abs((error_pos+error_neg)/2-flux_value))
            plt.errorbar(energy, flux, yerr=error, fmt='o-', label=mode)
        else:
            plt.plot(energy, flux)
        plt.xlabel('Energy (kev)')
        plt.ylabel('Flux (erg/cm2/s)')
        plt.xscale('log')
        plt.yscale('log')
        plt.title(f'Flux for {self.grb_name} in {mode}')
        plt.legend()
        plt.show()
    
    def plot_spectra_band(self, alpha_PL: float, K_PL:float, alpha_CPL: float, K_CPL:float, Epeak:float, energy_scale : tuple[float, float], delta_e: float = 1):

        energy = np.arange(energy_scale[0], energy_scale[1], delta_e)
        flux_PL = [K_PL * (energy_value/50) ** alpha_PL for energy_value in energy]

        flux_CPL = [K_CPL * (energy_value/50) ** alpha_CPL*np.exp(-energy_value*(2+alpha_CPL)/Epeak) for energy_value in energy]
        
        plt.plot(energy, flux_PL, label='Power Law')
        plt.plot(energy, flux_CPL, label='Cutoff Power Law')
        plt.xlabel('Energy (kev)')
        plt.ylabel('Flux (cts/s/cm2/kev)')
        plt.xscale('log')
        plt.yscale('log')
        plt.title(f'Powerlaw modelizations for {self.grb_name}')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    spectra = XRTSpectra('GRB 101225A')
    spectra.print_fields()
    # spectra.plot_spectra(ObservationMode.WT_Mode, (1,1e4))
    spectra.plot_spectra_band(
        alpha_PL=-1.83102,
        K_PL=1.99768E-04,
        alpha_CPL=-1.44935,
        K_CPL=3.39882E-04,
        Epeak=57.0008,
        energy_scale=(0,1e4),
    )