from pyhermes import *
from pyhermes.units import *

dragon2D_leptons = cosmicrays.Dragon2D([Electron, Positron])
kn_crosssection = interactions.KleinNishina()
CMB_photons = ('cmb', photonfields.CMB())
ISRF_photons = ('isrf', photonfields.ISRF())

nside = 128

for name, photonfield in (CMB_photons, ISRF_photons):
    skymap_range = GammaSkymapRange(nside, 1*GeV, 100*TeV, 20)
    skymap_range = GammaSkymapRange(nside, 1*GeV, 100*TeV, 10)
    integrator = InverseComptonIntegrator(dragon2D_leptons, photonfield, kn_crosssection)
    integrator.setupCacheTable(60, 60, 12)
    integrator.setupCacheTable(80, 80, 15)
    
    skymap_range.setIntegrator(integrator)
    skymap_range.compute()

    fname = "!fits/ic-D2-{}-skymap-nside{}.fits.gz".format(name, nside)
    skymap_range.save(outputs.HEALPixFormat(fname))
