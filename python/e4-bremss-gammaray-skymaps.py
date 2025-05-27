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

def integrate_bremss(leptons, gas, xsecs, E_gamma: float = 10, nside: int = 128):
    integrator = BremsstrahlungIntegrator(leptons, gas, xsecs)
    integrator.setupCacheTable(40, 40, 16) # To be adjusted based on performance needs
    return skymap_template(integrator, E_gamma, nside)

def compute_skymaps(E_gamma: float = 10, nside: int = 128):
    if not os.path.exists('fits'):
        os.makedirs('fits')

    gas_models = {
        'HI': neutralgas.RingModel(neutralgas.GasType.HI),
        'H2': neutralgas.RingModel(neutralgas.GasType.H2)
    }
    leptons = cosmicrays.Dragon2D([Electron, Positron])
    xsecs = interactions.BremsstrahlungTsai74()

    for name, model in gas_models.items():
        fitsname = f'!fits/Bremss-{name}-{nside}-{E_gamma}GeV-skymap.fits.gz'
        skymap = integrate_bremss(leptons, model, xsecs, E_gamma, nside)
        skymap.save(outputs.HEALPixFormat(fitsname))

if __name__ == "__main__":
    E_gamma = 10  # GeV
    nside = 256  # HEALPix NSIDE parameter

    print(f"Computing Bremss skymaps for E_gamma={E_gamma} GeV and nside={nside}...")
    compute_skymaps(E_gamma, nside)
    
    print(f"Plotting skymaps for E_gamma={E_gamma} GeV and nside={nside}...")
    plot_map_mollview(f'fits/Bremss-HI-{nside}-{E_gamma}GeV-skymap.fits.gz', 
                      f'Gamma-bremss-HI-mollview-{nside}-{E_gamma}GeV', 
                      min_map=-4.0, max_map=-1.0)
    plot_map_mollview(f'fits/Bremss-H2-{nside}-{E_gamma}GeV-skymap.fits.gz', 
                      f'Gamma-bremss-H2-mollview-{nside}-{E_gamma}GeV', 
                      min_map=-4.0, max_map=0.)
