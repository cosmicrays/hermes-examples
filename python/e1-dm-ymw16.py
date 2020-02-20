from pyhermes import *
from pyhermes.units import *

import numpy as np
import healpy
import matplotlib.pyplot as plt

nside = 128
skymap_name = "skymap-dm-{}-nside{}".format('ymw16', nside)

gas = YMW16()

skymap = DMSkymap(nside)
integrator = DMIntegrator(gas)
integrator.setSunPosition(Vector3QLength(8.3*kiloparsec, 0*parsec, 0*parsec))

skymap.setIntegrator(integrator)
skymap.compute()

output = FITSOutput("!fits/{}.fits.gz".format(skymap_name))
skymap.save(output)

skymap_data = np.array(skymap) # TODO: convert units!

healpy.visufunc.mollview(
        skymap_data, norm="log",
        title='DM of YMW16 log([pc/cm3])', cmap='magma',
        coord='G', unit=skymap.getUnits())

plt.savefig('img/{}.png'.format(skymap_name), dpi=150)
