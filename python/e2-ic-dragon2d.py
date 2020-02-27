from pyhermes import *
from pyhermes.units import *

import numpy as np
import healpy
import matplotlib.pyplot as plt

#dragon2D_leptons = Dragon2DCRDensity([Electron, Positron])
dragon2D_leptons = SimpleCRDensity(1*GeV, 100*TeV, 30)
kn_crosssection = KleinNishina()
CMB_photons = ('cmb', CMB())
ISRF_photons = ('isrf', ISRF())

nside = 128

for name, photonfield in (CMB_photons, ISRF_photons):
    skymap_range = GammaSkymapRange(nside, 1*GeV, 100*TeV, 20)
    integrator = InverseComptonIntegrator(dragon2D_leptons, photonfield, kn_crosssection)
    integrator.setupCacheTable(60, 60, 12)
    integrator.setupCacheTable(80, 80, 15)

    skymap_range.setIntegrator(integrator)
    skymap_range.compute()

    output = FITSOutput("!fits/ic-simple-{}-skymap-nside{}.fits.gz".format(name, nside))
    skymap_range.save(output)

    """
    skymap_data = np.array(skymap_range[0])
    Egamma = skymap_range[0].getEnergy()
    skymap_data[skymap_data != UNSEEN] *= (float(Egamma/GeV))**2
    healpy.visufunc.mollview(
        skymap_data, norm="log",
        title='IC with DRAGON2D and {}, nside={}, $E_\gamma = 10\,\mathrm{{ GeV }}$'.format(name.upper(), nside),
        unit="GeV^1 m^-2 s^-1 sr^-1", cmap='magma')

    plt.savefig('img/ic-dragon2d-{}-skymap-nside{}.png'.format(name, nside))
    """
