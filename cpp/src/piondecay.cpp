#include <iostream>
#include <memory>

#include "hermes.h"

namespace hermes {

void examplePion() {
	// cosmic ray density models
	auto simpleModel = std::make_shared<cosmicrays::SimpleCR>();
	std::vector<PID> particletypes = {Proton};
	auto dragonFilename = getDataPath("CosmicRays/Fornieri20/run2d_gamma_D03,7_delta0,45_vA13.fits.gz");
	auto dragonModel = std::make_shared<cosmicrays::Dragon2D>(dragonFilename, particletypes);

	// interaction
	auto kamae = std::make_shared<interactions::Kamae06Gamma>();

	// HI model
	auto ringModel = std::make_shared<neutralgas::RingModel>(neutralgas::GasType::HI);

	// integrator
	auto integrator = std::make_shared<PiZeroIntegrator>(dragonModel, ringModel, kamae);

	// skymap
	int nside = 32;
	auto skymap = std::make_shared<GammaSkymap>(GammaSkymap(nside, 1_GeV));
	skymap->setIntegrator(integrator);

	auto output = std::make_shared<outputs::HEALPixFormat>("!example-piondecay.fits.gz");

	skymap->compute();
	skymap->save(output);
}

}  // namespace hermes

int main(void) {
	hermes::examplePion();

	return 0;
}
