import logging
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
import fitsio
import numpy as np
from utils import savefig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_header(fits_map_filename):
    header = fitsio.read_header(fits_map_filename, ext=0)
    logging.debug(f"Header: {header}")
    return header

def get_img(fits_map_filename, imap):
    with fitsio.FITS(fits_map_filename, iter_row_buffer=100000) as fits:
        img_data = fits[0].read()
    return img_data[imap]

def prepare_axes(header, log_img):
    n_lon = header['NAXIS1']
    n_lat = header['NAXIS2']
    b = np.linspace(-90., 90., n_lat)
    l = np.linspace(-180., 180., n_lon)
    fig, ax = plt.subplots(figsize=(10, 5))
    im = ax.imshow(log_img , cmap='Blues', vmin=np.max(log_img)-2.0, vmax=np.max(log_img),
                    extent=[l[0], l[-1], b[0], b[-1]], origin='lower', aspect='auto')
    return fig, ax, im

def configure_colorbar(fig, im):
    cb = fig.colorbar(im, orientation='horizontal', pad=0.15)
    cb.ax.set_xlabel(r'log N [cm$^{-2}$]', fontsize=10)
    cb.ax.labelpad = 2
    cb.ax.tick_params(direction='in', length=0, width=1., which='major', pad=4,
                      bottom=True, top=True, left=True, right=True)
    cb.outline.set_linewidth(0.8)

def finalize_plot(ax, title, output_filename):
    ax.set_title(title, pad=5, fontsize=11)
    ax.set_xlabel(r'l [deg]')
    ax.set_ylabel(r'b [deg]')
    savefig(plt, output_filename)
    plt.close()

def plot_map(fits_map_filename, imap, output_filename, title, conversion_factor = 1.):
    header = get_header(fits_map_filename)
    img = get_img(fits_map_filename, imap)
    log_img = np.log10(conversion_factor * img + 1e-20)
    logging.info(f"Plotting {title} with vmax: {np.max(log_img):.2f}")
    fig, ax, im = prepare_axes(header, log_img)
    configure_colorbar(fig, im)
    finalize_plot(ax, title, output_filename)

if __name__ == "__main__":
    fits_map_filename = 'gas_maps/WCOrings_COGAL.fits.gz'
    logging.info(f"Processing file: {fits_map_filename}")
    X_CO = 1.8e20 # cm-2 / (K * km / s)
    for i in range(12):
        plot_map(fits_map_filename, i, f'NH2_ring_{i}', f'H2 Ring {i}', X_CO)
    logging.info("Processing complete.")

    fits_map_filename = 'gas_maps/NHrings_Ts300K.fits.gz'
    logging.info(f"Processing file: {fits_map_filename}")
    for i in range(12):
        plot_map(fits_map_filename, i, f'NHI_ring_{i}', f'HI Ring {i}')
    logging.info("Processing complete.")
