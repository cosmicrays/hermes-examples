from pyhermes import *
from pyhermes.units import *

import numpy as np
import healpy
import matplotlib.pyplot as plt

name = "dispersionmeasure-{}-{}".format('YMW16', 'fullsky')

def integrate_dispm():
    nside = 128
    gas = chargedgas.YMW16()

    integrator = DispersionMeasureIntegrator(gas)
    sun_pos = Vector3QLength(8.3*kpc, 0*pc, 0*pc)
    integrator.setObsPosition(sun_pos)

    skymap = DispersionMeasureSkymap(nside)
    skymap.setIntegrator(integrator)

    skymap.compute()

    return skymap

skymap = integrate_dispm()
skymap.save(outputs.HEALPixFormat("!fits/{}.fits.gz".format(name)))
