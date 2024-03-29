from pyhermes import *
from pyhermes.units import *
           
import numpy as np
import healpy
import matplotlib.pyplot as plt

def integrate_synchro(freq):
    nside = 128
    mfield = magneticfields.JF12()
    mfield.randomTurbulent(1)
    mfield.randomStriated(1)
    dragon2D_leptons = cosmicrays.Dragon2D([Electron, Positron]) 

    integrator = SynchroIntegrator(mfield, dragon2D_leptons)
    sun_pos = Vector3QLength(8.5*kpc, 0*pc, 0*pc)
    integrator.setObsPosition(sun_pos)

    skymap = RadioSkymap(nside, freq)
    skymap.setIntegrator(integrator)

    skymap.compute()

    return skymap

freq = 408*MHz
name = "synchro-{}-{}MHz-{}".format('JF12', freq/MHz, 'window')
skymap = integrate_synchro(freq)
skymap.save(outputs.HEALPixFormat("!fits/{}.fits.gz".format(name)))

freq = 23*GHz 
name = "synchro-{}-{}GHz-{}".format('JF12', freq/GHz, 'window')
skymap = integrate_synchro(freq)
skymap.save(outputs.HEALPixFormat("!fits/{}.fits.gz".format(name)))
