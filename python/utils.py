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

def make_cbar() -> None:
    fig = plt.gcf()
    ax = plt.gca()
    image = ax.get_images()[0]
    cb = fig.colorbar(image, orientation='horizontal', pad=0.03, shrink=0.7, ax=ax)
    cb.ax.set_xlabel(r'log E$^2$ Flux [GeV cm$^{-2}$ sr$^{-1}$ s$^{-1}$]', fontsize=12)
    cb.ax.labelpad = 1.5
    cb.ax.tick_params('both', length=0, width=1., which='major', pad=4, bottom=True, top=True, left=True, right=True)
    cb.outline.set_linewidth(0.8)


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


def get_header_info(fits_map_filename: str) -> Tuple[int, str]:
    if not os.path.exists(fits_map_filename):
        raise FileNotFoundError(f"FITS file '{fits_map_filename}' not found.")

    h = fitsio.read_header(fits_map_filename, ext=1)
    try:
        nside = h["NSIDE"]
        process = h["PROCESS"]
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

    return nside, process


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


def savefig(plt_module, filename: str, filetype: str = 'pdf') -> None:
    output_dir = 'img'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{filename}.{filetype}')
    plt_module.savefig(output_path, dpi=300)
    logging.info("Saved %s", output_path)

