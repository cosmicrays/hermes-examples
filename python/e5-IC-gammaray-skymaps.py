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

def integrate_IC(leptons, photonfield, E_gamma: float = 10, nside: int = 128):
    integrator = InverseComptonIntegrator(leptons, photonfield, interactions.KleinNishina())
    integrator.setupCacheTable(40, 40, 16) # To be adjusted based on performance needs
    return skymap_template(integrator, E_gamma, nside)

def compute_skymaps(E_gamma: float = 10, nside: int = 128):
    if not os.path.exists('fits'):
        os.makedirs('fits')

    photonfield_models = {
        'CMB': photonfields.CMB(),
        'ISRF': photonfields.ISRF()
    }
    leptons = cosmicrays.Dragon2D([Electron, Positron])
    for name, model in photonfield_models.items():
        fitsname = f'!fits/IC-{name}-{nside}-{E_gamma}GeV-skymap.fits.gz'
        skymap = integrate_IC(leptons, model, E_gamma, nside)
        skymap.save(outputs.HEALPixFormat(fitsname))

if __name__ == "__main__":
    E_gamma = 10  # GeV
    nside = 256  # HEALPix NSIDE parameter

    print(f"Computing Inverse Compton skymaps for E_gamma={E_gamma} GeV and nside={nside}...")
    #compute_skymaps(E_gamma, nside)
    
    print(f"Plotting skymaps for E_gamma={E_gamma} GeV and nside={nside}...")
    plot_map_mollview(f'fits/IC-CMB-{nside}-{E_gamma}GeV-skymap.fits.gz', 
                      f'IC-CMB-mollview-{nside}-{E_gamma}GeV', 
                      min_map=-4.7, max_map=-3.7)
    plot_map_mollview(f'fits/IC-ISRF-{nside}-{E_gamma}GeV-skymap.fits.gz', 
                      f'IC-ISRF-mollview-{nside}-{E_gamma}GeV', 
                      min_map=-3.7, max_map=-1.7)
