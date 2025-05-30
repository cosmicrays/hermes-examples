from pyhermes import *
from pyhermes.units import *

import os

from utils import plot_map_mollview

def skymap_template(integrator, E_nu: float, nside: int):
    sun_pos = Vector3QLength(8.0 * kpc, 0 * pc, 0 * pc)
    integrator.setObsPosition(sun_pos)
    skymap = GammaSkymap(nside, E_nu * GeV)
    skymap.setIntegrator(integrator)
    skymap.compute()
    return skymap

def integrate_pizero(nuclei, gas, xsecs, E_nu: float = 10, nside: int = 128):
    integrator = PiZeroIntegrator(nuclei, gas, xsecs)
    integrator.setupCacheTable(40, 40, 16) # To be adjusted based on performance needs
    return skymap_template(integrator, E_nu, nside)

def compute_skymaps(E_nu: float = 10, nside: int = 128):
    if not os.path.exists('fits'):
        os.makedirs('fits')

    gas_models = {
        'HI': neutralgas.RingModel(neutralgas.GasType.HI),
        'H2': neutralgas.RingModel(neutralgas.GasType.H2)
    }
    nuclei = cosmicrays.Dragon2D([Proton, Helium])
    xsecs = interactions.KelnerAharonianNeutrino() 
    for name, model in gas_models.items():
        fitsname = f'!fits/Pi0-{name}-{nside}-{E_nu}GeV-nu-skymap.fits.gz'
        skymap = integrate_pizero(nuclei, model, xsecs, E_nu, nside)
        skymap.save(outputs.HEALPixFormat(fitsname))

if __name__ == "__main__":
    E_nu = 10  # GeV
    nside = 256  # HEALPix NSIDE parameter

    print(f"Computing Pion Decay skymaps for E_nu={E_nu} GeV and nside={nside}...")
    compute_skymaps(E_nu, nside)
    
    print(f"Plotting skymaps for E_nu={E_nu} GeV and nside={nside}...")
    plot_map_mollview(f'fits/Pi0-HI-{nside}-{E_nu}GeV-nu-skymap.fits.gz', 
                      f'Neutrino_Pi0-HI-mollview-{nside}-{E_nu}GeV', 
                      min_map=-4.0, max_map=-1.0)
    plot_map_mollview(f'fits/Pi0-H2-{nside}-{E_nu}GeV-nu-skymap.fits.gz', 
                      f'Neutrino_Pi0-H2-mollview-{nside}-{E_nu}GeV', 
                      min_map=-4.0, max_map=0.)
