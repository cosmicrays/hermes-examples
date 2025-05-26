from pyhermes import *
from pyhermes.units import *

from utils import plot_spectrum

windows = {
    'GC': RectangularWindow(latitude=[2 * deg, -2 * deg], longitude=[358 * deg, 2 * deg]),
    'GalPlane': RectangularWindow(latitude=[5 * deg, 0 * deg], longitude=[0 * deg, 360 * deg]),
    'InterLatReg': RectangularWindow(latitude=[10 * deg, 5 * deg], longitude=[0 * deg, 360 * deg]),
    'LocReg': RectangularWindow(latitude=[90 * deg, 20 * deg], longitude=[0 * deg, 360 * deg])
}

def skymap_range_template(integrator, mask, nside: int):
    sun_pos = Vector3QLength(8.0 * kpc, 0 * pc, 0 * pc)
    integrator.setObsPosition(sun_pos)
    skymap_range = GammaSkymapRange(nside, TeV, PeV, 3 * 8)
    skymap_range.setIntegrator(integrator)
    skymap_range.setMask(mask)
    skymap_range.compute()
    return skymap_range

def integrate_pizero(nuclei, gas, xsecs, mask, nside: int):
    integrator = PiZeroIntegrator(nuclei, gas, xsecs)
    integrator.setupCacheTable(40, 40, 16)  # To be adjusted based on performance needs
    return skymap_range_template(integrator, mask, nside)

# Save functions for spectra

def compute_spectra(mask, nside: int = 128):
    gas_models = {
        'HI': neutralgas.RingModel(neutralgas.GasType.HI),
        'H2': neutralgas.RingModel(neutralgas.GasType.H2)
    }
    nuclei = cosmicrays.Dragon2D([Proton, Helium])
    xsecs = interactions.KelnerAharonianNeutrino()

    for name, model in gas_models.items():
        skymap = integrate_pizero(nuclei, model, xsecs, mask, nside)
        fitsname = f'!fits/Pi0-{name}-{nside}-TeV-PeV-gammaray-masked-spectrum.fits.gz'
        skymap.save(outputs.HEALPixFormat(fitsname))

if __name__ == "__main__":
    nside = 64  # HEALPix NSIDE parameter

    print(f"Computing Pion Decay spectra for nside={nside}...")
    compute_spectra(mask=windows['InterLatReg'], nside=nside)

    print(f"Plotting spectra for nside={nside}...")
    plot_spectrum(f'fits/Pi0-HI-{nside}-TeV-PeV-gammaray-masked-spectrum.fits.gz', 
                  f'Pi0-HI-InterLat-pectrum-{nside}')
    
    plot_spectrum(f'fits/Pi0-H2-{nside}-TeV-PeV-gammaray-masked-spectrum.fits.gz', 
                  f'Pi0-H2-InterLat-spectrum-{nside}')

