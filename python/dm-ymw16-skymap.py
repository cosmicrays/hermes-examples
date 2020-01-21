import numpy as np
import healpy
import matplotlib.pyplot as plt

from pyhermes import *

skymap = DMSkymap(nside=64)
gas = YMW16()
integrator = DMIntegrator(gas)
integrator.setSunPosition(Vector3QLength(8.3*kiloparsec, 0*parsec, 0*parsec))

skymap.setIntegrator(integrator)
skymap.compute()

output = FITSOutput("!fits/dm-ymw16-skymap.fits.gz")
skymap.save(output)

healpy.visufunc.mollview(
        np.log(np.array(skymap)),
        title='DM of YMW16 [pc/cm3]', cmap='magma')

plt.savefig('img/dm-ymw16-skymap.png')
