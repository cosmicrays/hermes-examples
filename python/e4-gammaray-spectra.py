from pyhermes import *
from pyhermes.units import *

import numpy as np
import healpy
import matplotlib.pyplot as plt

name = "gammarays-1GeV-1TeV-{}-{}".format('Fornieri20', 'Remy18')

def integrate_template(integrator, nside, window):
    
    integrator.setupCacheTable(100, 100, 20)
    sun_pos = Vector3QLength(8.0*kpc, 0*pc, 0*pc)
    integrator.setSunPosition(sun_pos)

    mask = RectangularWindow(*window)
    
    skymap_range = GammaSkymapRange(nside, 1*GeV, 1*TeV, 15)
    skymap_range.setIntegrator(integrator)
    skymap_range.setMask(mask)
    
    skymap_range.compute()
    
    return skymap_range

def integrate_pizero(gas, window):
    nside = 256
    protons = cosmicrays.Dragon2D(Proton)
    heliums = cosmicrays.Dragon2D(Helium)
    integrator = PiZeroIntegrator([protons, heliums], gas, interactions.Kamae06Gamma())
    return integrate_template(integrator, nside, window)

def integrate_bremss(gas, window):
    nside = 256
    leptons = cosmicrays.Dragon2D([Electron, Positron])
    integrator = PiZeroIntegrator(leptons, gas, interactions.BremsstrahlungSimple())
    return integrate_template(integrator, nside, window)

def integrate_IC(window):
    nside = 128
    leptons = Dragon2DCRDensity([Electron, Positron])
    integrator = InverseComptonIntegrator(leptons, photonfields.ISRF(), interactions.KleinNishina())    
    return integrate_template(integrator, nside, window)

# Neutral gas contained in the so-called ring model
neutral_gas_HI = neutralgas.RingModel(neutralgas.RingType.HI)
neutral_gas_CO = neutralgas.RingModel(neutralgas.RingType.CO)

galactic_centre = {
            'label': 'GC',
            'window': ([2*deg, -2*deg], [-2*deg, 2*deg])
        }
galactic_plane = {
            'label': 'GalPlane',
            'window': ([5*deg, 0*deg], [0*deg, 180*deg])
        }

window = galactic_plane

skymap_range_pi0_HI = integrate_pizero(neutral_gas_HI, window['window'])
output_hp = outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'pi0-HI', window['label']))
skymap_range_pi0_HI.save(output_hp)

skymap_range_pi0_CO = integrate_pizero(neutral_gas_CO, window['window'])
output_hp = outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'pi0-C0', window['label']))
skymap_range_pi0_CO.save(output_hp)
