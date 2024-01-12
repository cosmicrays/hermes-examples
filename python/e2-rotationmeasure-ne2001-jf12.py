from pyhermes import *
from pyhermes.units import *

import numpy as np
import healpy
import matplotlib.pyplot as plt

name = "rotationmeasure-{}-{}-{}".format('NE2001', 'JF12', 'fullsky')

def integrate_rotm():
    nside = 256
    gas = chargedgas.NE2001Simple()
    #gas = chargedgas.YMW16()
    mfield = magneticfields.JF12()
    mfield.randomTurbulent(1)
    mfield.randomStriated(1)

    integrator = RotationMeasureIntegrator(mfield, gas)
    sun_pos = Vector3QLength(8.4*kpc, 0*pc, 0*pc)
    integrator.setObsPosition(sun_pos)

    skymap = RotationMeasureSkymap(nside)
    skymap.setIntegrator(integrator)

    skymap.compute()

    return skymap

skymap = integrate_rotm()
skymap.save(outputs.HEALPixFormat("!fits/{}.fits.gz".format(name)))
