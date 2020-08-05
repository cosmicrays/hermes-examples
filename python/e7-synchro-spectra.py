from pyhermes import *
from pyhermes.units import *

name = "gammarays-1GeV-1TeV-{}-{}".format('Fornieri20', 'Remy18')

galactic_centre = {
            'label': 'GC',
            'mask': RectangularWindow(latitude=[2*deg, -2*deg], longitude=[358*deg, 2*deg])
        }
galactic_plane = {
            'label': 'GalPlane',
            'mask': RectangularWindow(latitude=[5*deg, 0*deg], longitude=[0*deg, 360*deg])
        }
intermediate_region = {
            'label': 'InterLatReg',
            'mask': RectangularWindow(latitude=[20*deg, 5*deg], longitude=[0*deg, 360*deg])
        }
local_region = {
            'label': 'LocReg',
            'mask': RectangularWindow(latitude=[90*deg, 20*deg], longitude=[0*deg, 360*deg])
        }

def skymap_range_template(integrator, nside, mask):
    sun_pos = Vector3QLength(8.0*kpc, 0*pc, 0*pc)
    integrator.setSunPosition(sun_pos)

    skymap_range = GammaSkymapRange(nside, 1*GeV, 1*TeV, 25)
    skymap_range.setIntegrator(integrator)
    skymap_range.setMask(mask)
    
    skymap_range.compute()
    
    return skymap_range

def integrate_pizero(gas, mask):
    nside = 512
    protons = cosmicrays.Dragon2D(Proton)
    heliums = cosmicrays.Dragon2D(Helium)
    integrator = PiZeroIntegrator([protons, heliums], gas, interactions.Kamae06Gamma())
    integrator.setupCacheTable(100, 100, 20)
    return skymap_range_template(integrator, nside, mask)

def integrate_bremss(gas, mask):
    nside = 512 
    leptons = cosmicrays.Dragon2D([Electron, Positron])
    integrator = BremsstrahlungIntegrator(leptons, gas, interactions.BremsstrahlungTsai74())
    integrator.setupCacheTable(100, 100, 20)
    return skymap_range_template(integrator, nside, mask)

def integrate_IC(mask):
    nside = 128
    leptons = cosmicrays.Dragon2D([Electron, Positron])
    integrator = InverseComptonIntegrator(leptons, photonfields.ISRF(), interactions.KleinNishina())    
    integrator.setupCacheTable(60, 60, 12)
    return skymap_range_template(integrator, nside, mask)

# Neutral gas contained in the so-called ring model
neutral_gas_HI = neutralgas.RingModel(neutralgas.RingType.HI)
neutral_gas_CO = neutralgas.RingModel(neutralgas.RingType.CO)

for window in [galactic_centre, galactic_plane, intermediate_region, local_region]:

    skymap_range = integrate_pizero(neutral_gas_HI, window['mask'])
    skymap_range.save(outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'pi0-HI', window['label'])))

    skymap_range = integrate_pizero(neutral_gas_CO, window['mask'])
    skymap_range.save(outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'pi0-CO', window['label'])))

    skymap_range = integrate_IC(window['mask'])
    skymap_range.save(outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'IC', window['label'])))

    skymap_range = integrate_bremss(neutral_gas_HI, window['mask'])
    skymap_range.save(output_hp = outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'brems-HI', window['label'])))

    skymap_range = integrate_bremss(neutral_gas_CO, window['mask'])
    skymap_range.save(outputs.HEALPixFormat("!fits/{}-{}-{}.fits.gz".format(name, 'brems-CO', window['label'])))
