import logging

import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt

import healpy as hp
import numpy as np

from utils import savefig, make_cbar, get_map, get_header_info, get_extension_index

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def plot_map_mollview(
    fits_map_filename: str,
    output_filename: str,
    E_gamma: float,
    min_map: float,
    max_map: float
) -> None:
    """Plot HEALPix map in Mollweide projection and save to file.

    Args:
        fits_map_filename: Path to the input FITS file.
        output_filename: Name for the output image file.
        E_gamma: Energy (in GeV) to determine FITS extension.
        min_map: Minimum map value for color scaling.
        max_map: Maximum map value for color scaling.
    """
    try:
        nside, process = get_header_info(fits_map_filename)
        i_ext = get_extension_index(fits_map_filename, E_gamma)
        flux_map = get_map(fits_map_filename, i_ext)
        log_map = np.log10(E_gamma * E_gamma * flux_map)

        logging.info("Map range: %.2f to %.2f, mean: %.2f", np.min(log_map), np.max(log_map), np.mean(log_map))

        title = fr'{process} - NSIDE: {nside} - $E_\gamma$ : {E_gamma:.1f} GeV'
        hp.mollview(
            log_map,
            title=title,
            norm='lin',
            max=max_map,
            min=min_map,
            cmap='jet',
            cbar=False,
            unit=r'log E$^2$ Flux [GeV cm$^{-2}$ sr$^{-1}$ s$^{-1}$]'
        )
        hp.graticule()
        make_cbar()
        savefig(plt, output_filename)

    except Exception as e:
        logging.error("Failed to generate map: %s", e)
        raise


if __name__ == "__main__":
    plot_map_mollview('fits/ic-D2-cmb-skymap-nside128.fits.gz', 'IC-CMB-mollview-10GeV-128', 10, -2.2, -1.0)
    plot_map_mollview('fits/ic-D2-isrf-skymap-nside128.fits.gz', 'IC-ISRF-mollview-10GeV-128', 10, -1.0, 0.7)