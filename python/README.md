# HERMES Python Example Repository

This repository contains Python scripts that generate various full-sky maps and energy spectra related to cosmic ray interactions in the Galaxy, using HERMES code

## Scripts Overview

- `e1-pi0-gammaray-skymaps.py`

    Generates a full-sky Mollweide projection map of Pion-0 decay gamma-ray intensity at a specified photon energy. The target is HI (or H2) gas, using CR nuclei distributions from DRAGON2 and Kamae06 cross-sections.

- `e2-pi0-gammaray-ring.py`
  
    Generates a full-sky Mollweide map of Pion-0 decay gamma-ray intensity at a specified photon energy, assuming HI (or H2) gas in a single ring as the target.

- `e3-pi0-neutrino-skymaps.py`

    Generates a full-sky Mollweide map of Pion-0 decay neutrino intensity at a specified neutrino energy.

- `e4-bremss-gammaray-skymaps.py`

    Generates a full-sky Mollweide map of Bremsstrahlung gamma-ray intensity at a specified photon energy, using the CR lepton distribution from DRAGON2.

- `e5-IC-gammaray-skymaps.py`

    Generates a full-sky Mollweide map of Inverse Compton gamma-ray intensity at a specified photon energy, using the CR lepton distribution from DRAGON2.

- `e6-DarkMatter-skymaps.py`

    Generates a full-sky Mollweide map of dark matter annihilation gamma-ray intensity, assuming a generalized NFW profile and a 1 TeV dark matter particle with W annihilation channel.

- `e7-gas-columndensity.py`

    Generates full-sky Cartesian maps of the gas column density for each ring (i = 0 to 11) in the CTA Ring Model.

- `e8-pi0-gammaray-spectrum.py`

    Generates the gamma-ray intensity energy spectrum of Pion-0 decay, assuming HI (or H2) as the Galactic target, using the CR nuclei distribution from the DRAGON2 provided file and Kamae06 cross-sections.

- `e9-pi0-gammaray-masked-spectrum`

    Generates the gamma-ray intensity energy spectrum of Pion-0 decay, masked on a specified latitude-longitude region.

---

### Notes

* Scripts require the DRAGON2 output files and corresponding input parameters.
* Ensure required Python packages (like `healpy`, `numpy`, etc.) are installed.
* For detailed usage of each script, please refer to the script-specific docstrings or usage examples within the scripts themselves.
