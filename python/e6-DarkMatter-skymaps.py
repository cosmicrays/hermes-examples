from pyhermes import *
from pyhermes.units import *

import os

from utils import plot_map_mollview

def skymap_template(integrator, E_gamma: float, nside: int):
    sun_pos = Vector3QLength(8.0 * kpc, 0 * pc, 0 * pc)
    integrator.setObsPosition(sun_pos)
    skymap = GammaSkymap(nside, E_gamma * GeV)
    skymap.setIntegrator(integrator)
    skymap.compute()
    return skymap

def compute_skymaps(E_gamma: float = 10, nside: int = 128):
    if not os.path.exists('fits'):
        os.makedirs('fits')

    dmSpectrum = darkmatter.PPPC4DMIDSpectrum(darkmatter.Channel.W, darkmatter.Mass.m1TeV)
    dmProfile = darkmatter.NFWGProfile(gamma = 1.0, concentration = 20., M200 = 1.4 * 0.7 * 8e11 * units.sun_mass)
    integrator = DarkMatterIntegrator(dmSpectrum, dmProfile)
    skymap = skymap_template(integrator, E_gamma, nside)
    fitsname = f'!fits/DM-{nside}-{E_gamma}GeV-skymap.fits.gz'
    skymap.save(outputs.HEALPixFormat(fitsname))

if __name__ == "__main__":
    E_gamma = 100  # GeV
    nside = 512  # HEALPix NSIDE parameter

    print(f"Computing Dark Matter gamma-ray skymap for E_gamma={E_gamma} GeV and nside={nside}...")
    compute_skymaps(E_gamma, nside)
    
    print(f"Plotting skymaps for E_gamma={E_gamma} GeV and nside={nside}...")
    plot_map_mollview(f'fits/DM-{nside}-{E_gamma}GeV-skymap.fits.gz', 
                      f'DM-NFWG-mollview-{nside}-{E_gamma}GeV', 
                      min_map=-4.75, max_map=-0.75)
