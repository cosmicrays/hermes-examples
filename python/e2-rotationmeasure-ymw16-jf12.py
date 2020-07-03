from pyhermes import *
from pyhermes.units import *

import numpy as np
import healpy
import matplotlib.pyplot as plt

name = "rotationmeasure-{}-{}-{}".format('NE2001', 'JF12', 'fullsky')

def integrate_rotm():
    nside = 128
    gas = chargedgas.NE2001Simple()
    #gas = chargedgas.YMW16()
    mfield = magneticfields.JF12Field()

    integrator = RotationMeasureIntegrator(mfield, gas)
    sun_pos = Vector3QLength(8.5*kpc, 0*pc, 0*pc)
    integrator.setSunPosition(sun_pos)

    skymap = RotationMeasureSkymap(nside)
    skymap.setIntegrator(integrator)

    skymap.compute()

    return skymap

skymap = integrate_rotm()
skymap.save(outputs.HEALPixFormat("!fits/{}.fits.gz".format(name)))
