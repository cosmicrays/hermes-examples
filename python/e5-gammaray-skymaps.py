from pyhermes import *
from pyhermes.units import *

name = "gammarays-10GeV-{}-{}".format('Fornieri20', 'Remy18')

def skymap_template(integrator, nside):
    sun_pos = Vector3QLength(8.0*kpc, 0*pc, 0*pc)
    integrator.setSunPosition(sun_pos)

    skymap = GammaSkymap(nside, 10*GeV)
    skymap.setIntegrator(integrator)
    
    skymap.compute()
    
    return skymap

def integrate_pizero(gas):
    nside = 512
    protons = cosmicrays.Dragon2D(Proton)
    heliums = cosmicrays.Dragon2D(Helium)
    integrator = PiZeroIntegrator([protons, heliums], gas, interactions.Kamae06Gamma())
    integrator.setupCacheTable(200, 200, 40)
    return skymap_template(integrator, nside)

def integrate_IC():
    nside = 128
    leptons = cosmicrays.Dragon2D([Electron, Positron])
    integrator = InverseComptonIntegrator(leptons, photonfields.ISRF(), interactions.KleinNishina())    
    integrator.setupCacheTable(60, 60, 12)
    return skymap_template(integrator, nside)

# Neutral gas contained in the so-called ring model
neutral_gas_HI = neutralgas.RingModel(neutralgas.GasType.HI)
enabled_rings = [True for i in range(12)]
enabled_rings[11] = False
neutral_gas_HI.setEnabledRings(enabled_rings)
#ring_i = 11 
#neutral_gas_HI.enableRingNo(ring_i)
neutral_gas_CO = neutralgas.RingModel(neutralgas.GasType.H2)

label = 'fullsky'
skymap = integrate_pizero(neutral_gas_HI)
skymap.save(outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'pi0-HI', label)))
#skymap.save(outputs.HEALPixFormat("!fits/{}-{}-{}-ring-{}.fits.gz".format(name, 'pi0-HI', label, ring_i)))

#skymap = integrate_pizero(neutral_gas_CO)
#skymap.save(outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'pi0-CO', label)))

#skymap = integrate_IC()
#skymap.save(outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'IC', label)))

