from pyhermes import *

import numpy as np
import healpy
import matplotlib.pyplot as plt

dragon2D_leptons = Dragon2DCRDensity([Electron, Proton])
kn_crosssection = KleinNishina()
CMB_photons = ('cmb', CMB())
ISRF_photons = ('isrf', ISRF())

nside = 512
Egamma = 10*GeV

for name, photonfield in (CMB_photons, ISRF_photons):
    skymap = GammaSkymap(nside=nside, Egamma=Egamma)
    integrator = InverseComptonIntegrator(dragon2D_leptons, photonfield, kn_crosssection)
    integrator.setupCacheTable(60, 60, 12)

    skymap.setIntegrator(integrator)
    skymap.compute()

    output = FITSOutput("!fits/ic-dragon2d-{}-skymap-nside{}.fits.gz".format(name, nside))
    skymap.save(output)

    skymap_data = np.array(skymap)
    skymap_data[skymap_data != UNSEEN] *= (float(Egamma)/float(GeV))**2

    healpy.visufunc.mollview(
        skymap_data, norm="log",
        title='IC with DRAGON2D and {}, nside={}, $E_\gamma = 10\,\mathrm{{ GeV }}$'.format(name.upper(), nside),
        unit="GeV^1 m^-2 s^-1 sr^-1", cmap='magma')

    plt.savefig('img/ic-dragon2d-{}-skymap-nside{}.png'.format(name, nside))
