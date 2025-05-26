import os
import logging
from typing import Tuple

import fitsio
import healpy as hp
import numpy as np
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

GEV = 1.60218e-10

# def make_cbar(image, fig, ax) -> None:
#     # fig = plt.gcf()
#     # ax = plt.gca()
#     # image = ax.get_images()[0]
#     cb = fig.colorbar(image, ax=ax, orientation='horizontal', pad=0.03, shrink=0.7)
#     cb.ax.set_xlabel(r'log E$^2$ Flux [GeV cm$^{-2}$ sr$^{-1}$ s$^{-1}$]', fontsize=12)
#     cb.ax.labelpad = 1.5
#     cb.ax.tick_params('both', length=0, width=1., which='major', pad=4, bottom=True, top=True, left=True, right=True)
#     cb.outline.set_linewidth(0.8)

def get_map(fits_map_filename: str, extension_index: int = 1) -> np.ndarray:
    if not os.path.exists(fits_map_filename):
        raise FileNotFoundError(f"FITS file '{fits_map_filename}' not found.")

    h = fitsio.read_header(fits_map_filename, ext=extension_index)
    try:
        n_pixs = h["NAXIS2"]
        nside = h["NSIDE"]
    except KeyError as e:
        raise KeyError(f"Missing expected header keyword: {e}")

    if n_pixs != hp.nside2npix(nside):
        raise ValueError("Mismatch between NAXIS2 and NSIDE pixel count.")

    flux_list = []
    with fitsio.FITS(fits_map_filename) as fits:
        for i in range(n_pixs):
            flux = fits[1][i][0]
            flux_list.append(max(flux, 1e-20))

    flux_array = np.array(flux_list)
    logging.info("Read map from %.2e to %.2e with %d pixels", flux_array.min(), flux_array.max(), n_pixs)
    logging.info("Mean flux: %.2e", np.mean(flux_array))
    logging.info("Total flux: %.2e", np.sum(flux_array))

    return flux_array


def get_header_info(fits_map_filename: str) -> Tuple[int, float, str]:
    if not os.path.exists(fits_map_filename):
        raise FileNotFoundError(f"FITS file '{fits_map_filename}' not found.")

    h = fitsio.read_header(fits_map_filename, ext=1)
    try:
        nside = h["NSIDE"]
        process = h["PROCESS"]
        E_gamma = h["ENERGY"] / GEV
        units = h["TUNIT1"]
    except KeyError as e:
        raise KeyError(f"Missing expected header keyword: {e}")

    resolution = hp.nside2resol(nside, arcmin=False) * 180. / np.pi
    logging.info("filename: %s", fits_map_filename)
    logging.info("NSIDE: %d", nside)
    logging.info("approx. resolution: %.2f degree", resolution)
    logging.info("number of pixels: %d", hp.nside2npix(nside))
    logging.info("process: %s", process)
    logging.info("units: %s", units)

    return nside, E_gamma, process

def get_energy_array(fits_map_filename):
    if not os.path.exists(fits_map_filename):
        raise FileNotFoundError(f"FITS file '{fits_map_filename}' not found.")
    
    fits = fitsio.FITS(fits_map_filename)
    size = len(fits)

    logging.info("number of extensions: %d", size)
    
    E = []
    for i in range(1,size):
        h = fitsio.read_header(fits_map_filename, ext=i)
        E.append(h["ENERGY"] / GEV)

    logging.info("energy range: %3.1e - %3.1e GeV", np.min(E), np.max(E))
    return np.array(E)

def get_fullsky_flux(fits_map_filename):
    if not os.path.exists(fits_map_filename):
        raise FileNotFoundError(f"FITS file '{fits_map_filename}' not found.")
    
    logging.info(f"Reading full sky flux from {fits_map_filename}")

    h = fitsio.read_header(fits_map_filename, ext=1)
    NSIDE = h["NSIDE"]
    NPIX = hp.nside2npix(NSIDE)

    logging.info("NSIDE: %d, NPIX: %d", NSIDE, NPIX)

    fits = fitsio.FITS(fits_map_filename)
    size = len(fits)

    logging.info("number of extensions: %d", size)

    flux = []
    for imap in range(1, size):
        img = fits[imap].read()
        value = 0.
        for ipix in range(NPIX):
            if img[ipix][0] > 0:
                value += img[ipix][0]
        flux.append(value / float(NPIX))
    fits.close()

    return np.array(flux)

def get_extension_index(fits_map_filename: str, E_gamma: float) -> int:
    with fitsio.FITS(fits_map_filename) as fits:
        size = len(fits) - 1
        logging.info("number of extensions: %d", size)

        E_min = fits[1].read_header()["ENERGY"] / GEV
        E_max = fits[size].read_header()["ENERGY"] / GEV

        if not (E_min <= E_gamma <= E_max):
            raise ValueError(f"E_gamma {E_gamma:.2e} GeV is outside the file energy range ({E_min:.2e}, {E_max:.2e})")

        for i in range(1, size):
            E_temp = fits[i].read_header()["ENERGY"] / GEV
            if E_temp > E_gamma:
                logging.info("index: %d, E_gamma: %.2e GeV", i, E_temp)
                return i

    return -1

def plot_map_mollview(
    fits_map_filename: str,
    output_filename: str,
    min_map: float = None,
    max_map: float = None
) -> None:
    """Plot HEALPix map in Mollweide projection and save to file.

    Args:
        fits_map_filename: Path to the input FITS file.
        output_filename: Name for the output image file.
        min_map: Minimum map value for color scaling.
        max_map: Maximum map value for color scaling.
    """
    try:
        fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': 'mollweide'})

        nside, E_gamma, process = get_header_info(fits_map_filename)
        flux_map = get_map(fits_map_filename, 1)
        log_map = np.log10(E_gamma * E_gamma * flux_map)

        logging.info("Map range: %.2f to %.2f, mean: %.2f", np.min(log_map), np.max(log_map), np.mean(log_map))

        # if min_map not set, use min and max of the map
        if min_map is None:
            min_map = np.min(log_map)
        if max_map is None:
            max_map = np.max(log_map)

        title = fr'{process} - NSIDE: {nside} - $E_\gamma$ : {E_gamma:.1f} GeV'
        hp.mollview(
            log_map,
            title=title,
            norm='lin',
            max=max_map,
            min=min_map,
            cmap='jet',
            cbar=True,
            format='%.2f',
            unit=r'log E$^2$ Flux [GeV cm$^{-2}$ sr$^{-1}$]'
        )
        hp.graticule()

        savefig(plt, output_filename)

    except Exception as e:
        logging.error("Failed to generate map: %s", e)
        raise

def plot_spectrum(
    fits_spectrum_filename: str, 
    output_filename: str
)-> None:
    """Plot gamma-ray spectrum from a FITS file and save to file.

    Args:
        fits_spectrum_filename: Path to the input FITS file containing the spectrum.
        output_filename: Name for the output image file.
    """
    try:
        fig, ax = plt.subplots(figsize=(10, 6))

        nside, _, process = get_header_info(fits_spectrum_filename)
        logging.info("Processing spectrum for %s at NSIDE %d", process, nside)

        E = get_energy_array(fits_spectrum_filename)
        flux = get_fullsky_flux(fits_spectrum_filename)

        logging.info("Spectrum range: %.2e to %.2e, mean: %.2e", np.min(flux), np.max(flux), np.mean(flux))

        ax.plot(E, E * E * flux, label=process)
        
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy (GeV)')
        ax.set_ylabel('E$^2$ Flux (GeV m$^{-2}$ s$^{-1}$ sr$^{-1}$)')
        #ax.set_title(f'{process} Spectrum - NSIDE: {nside}')
        ax.legend()

        savefig(plt, output_filename)

    except Exception as e:
        logging.error("Error plotting spectrum: %s", e)

def savefig(plt_module, filename: str, filetype: str = 'pdf') -> None:
    output_dir = 'img'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{filename}.{filetype}')
    plt_module.savefig(output_path, dpi=300)
    logging.info("Saved %s", output_path)
