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

def integrate_ring_pizero(nuclei, gas, xsecs, ring_i: int, E_gamma: float = 10, nside: int = 128):
    enabled_rings = [False for i in range(12)]
    enabled_rings[ring_i] = True
    gas.setEnabledRings(enabled_rings)
    integrator = PiZeroIntegrator(nuclei, gas, interactions.Kamae06Gamma())
    integrator.setupCacheTable(40, 40, 16) # To be adjusted based on performance needs
    return skymap_template(integrator, E_gamma, nside)

def compute_ring_skymaps(ring_i: int = 0, E_gamma: float = 10, nside: int = 128):
    if not os.path.exists('fits'):
        os.makedirs('fits')

    gas_models = {
        'HI': neutralgas.RingModel(neutralgas.GasType.HI),
        'H2': neutralgas.RingModel(neutralgas.GasType.H2)
    }
    nuclei = cosmicrays.Dragon2D([Proton, Helium])
    xsecs = interactions.Kamae06Gamma()
    for name, model in gas_models.items():
        fitsname = f'!fits/Pi0-{name}-{ring}-{nside}-{E_gamma}GeV-skymap.fits.gz'
        skymap = integrate_ring_pizero(nuclei, model, xsecs, ring_i, E_gamma, nside)
        skymap.save(outputs.HEALPixFormat(fitsname))

if __name__ == "__main__":
    E_gamma = 10  # GeV
    nside = 256  # HEALPix NSIDE parameter
    ring = 3  # Example ring index, can be changed

    print(f"Computing skymaps for E_gamma={E_gamma} GeV and nside={nside}...")
    compute_ring_skymaps(ring, E_gamma, nside)
    
    print(f"Plotting skymaps for E_gamma={E_gamma} GeV and nside={nside}...")
    plot_map_mollview(f'fits/Pi0-HI-{ring}-{nside}-{E_gamma}GeV-skymap.fits.gz', 
                      f'Pi0-HI-mollview-{ring}-{nside}-{E_gamma}GeV', 
                      min_map=-4.0, max_map=-1.0)
    plot_map_mollview(f'fits/Pi0-H2-{ring}-{nside}-{E_gamma}GeV-skymap.fits.gz', 
                      f'Pi0-H2-mollview-{ring}-{nside}-{E_gamma}GeV', 
                      min_map=-4.0, max_map=0.)
