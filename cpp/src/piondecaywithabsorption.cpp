#include <iostream>
#include <memory>

#include "hermes.h"

namespace hermes {

void examplePion() {
	// cosmic ray density models
	std::vector<PID> particletypes = {Proton};
	auto dragonFilename = getDataPath("CosmicRays/Fornieri20/run2d_gamma_D03,7_delta0,45_vA13.fits.gz");
	auto dragonModel = std::make_shared<cosmicrays::Dragon2D>(dragonFilename, particletypes);

    // photon background
     const auto isrf = std::make_shared<photonfields::ISRF>(photonfields::ISRF());
    
	// interaction
	auto kamae = std::make_shared<interactions::Kamae06Gamma>();

	// target gas
	auto ringModel = std::make_shared<neutralgas::RingModel>(neutralgas::GasType::HI);

    // mask
    const std::array<QAngle, 2> longitude{0_deg, 360_deg};
    const std::array<QAngle, 2> latitude{-8_deg, 8_deg};
    const auto mask = std::make_shared<RectangularWindow>(latitude, longitude);
    
	// integrator
	auto integrator = std::make_shared<PiZeroAbsorptionIntegrator>(dragonModel, ringModel, isrf, kamae);

    auto sun_pos = Vector3QLength(8.5_kpc, 0_kpc, 0_kpc);
    integrator->setObsPosition(sun_pos);
    integrator->setupCacheTable(100, 100, 50);
    
	// skymap
	int nside = 32;
	auto skymap = std::make_shared<GammaSkymap>(GammaSkymap(nside, 1_TeV));
    skymap->setMask(mask);
	skymap->setIntegrator(integrator);

	auto output = std::make_shared<outputs::HEALPixFormat>("!example-piondecaywithabsorption.fits.gz");

	skymap->compute();
	skymap->save(output);
}

}  // namespace hermes

int main(void) {
	hermes::examplePion();

	return 0;
}
