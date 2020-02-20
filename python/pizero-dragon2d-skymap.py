from pyhermes import *

import numpy as np
import healpy
import matplotlib.pyplot as plt

dragon2D_leptons = Dragon2DCRDensity([Proton])
kamae_crosssection = Kamae06()
neutral_gas = RingModelDensity()

nside = 512
Egamma = 0.1*TeV

skymap_name = "skymap-pizero-nside{}-{}-{}-E{}".format(nside, 'dragon2d', 'remy18', '0.1TeV')

skymap = GammaSkymap(nside=nside, Egamma=Egamma)
mask = RectangularWindow(-5*deg, 5*deg, 40*deg, 95*deg);
skymap.setMask(mask)
integrator = PiZeroIntegrator(dragon2D_leptons, neutral_gas, kamae_crosssection)

integrator.setupCacheTable(100, 100, 20)

skymap.setIntegrator(integrator)
skymap.compute()

output = FITSOutput("!fits/{}.fits.gz".format(skymap_name))
skymap.save(output)

skymap_data = np.array(skymap)
skymap_data[skymap_data != UNSEEN] *= (float(Egamma)/float(GeV))**2

healpy.visufunc.mollview(
    skymap_data,
    title='$\pi^0$ with DRAGON2D and Remy18, nside={}, $E_\gamma =0.1\,\mathrm{{ TeV }}$'.format(nside),
    unit="GeV^1 m^-2 s^-1 sr^-1", cmap='magma')

plt.savefig('img/{}.png'.format(skymap_name), dpi=300)
