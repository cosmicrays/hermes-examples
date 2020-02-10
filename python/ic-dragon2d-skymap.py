import numpy as np
import healpy
import matplotlib.pyplot as plt

from pyhermes import *

dragon2D_leptons = Dragon2DCRDensity()
kn_crosssection = KleinNishina()
CMB_photons = ('cmb', CMB())
ISRF_photons = ('isrf', ISRF())

Egamma = 10*GeV

for name, photonfield in (CMB_photons, ISRF_photons):
    skymap = GammaSkymap(nside=512, Egamma=Egamma)
    integrator = InverseComptonIntegrator(dragon2D_leptons, photonfield, kn_crosssection)
    integrator.initCacheTable(Egamma, 60, 60, 12)

    skymap.setIntegrator(integrator)
    skymap.compute()

    output = FITSOutput("!fits/ic-dragon2d-{}-skymap.fits.gz".format(name))
    skymap.save(output)

    healpy.visufunc.mollview(
        Egamma*2*np.array(skymap),
        title='IC with DRAGON2D and {}, nside=512, $E_\gamma = 10\,\mathrm{{ GeV }}$'.format(name.upper()),
        unit="GeV^1 m^-2 s^-1 sr^-1", cmap='magma')

    plt.savefig('img/ic-dragon2d-{}-skymap.png'.format(name))
