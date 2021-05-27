#include <iostream>
#include <memory>

#include "hermes.h"

namespace hermes {

void exampleSynchro() {
	// magnetic field models
	auto JF12 = std::make_shared<magneticfields::JF12>();
	JF12->randomStriated(137);
	JF12->randomTurbulent(1337);
	auto PT11 = std::make_shared<magneticfields::PT11>();
	auto Sun08 = std::make_shared<magneticfields::Sun08>();

	// cosmic ray density models
	auto simpleModel = std::make_shared<cosmicrays::SimpleCR>();
	auto WMAP07Model = std::make_shared<cosmicrays::WMAP07>();
	auto Sun08Model = std::make_shared<cosmicrays::Sun08>();

	std::vector<PID> particletypes = {Electron, Positron};
	auto dragonFilename = getDataPath("CosmicRays/Fornieri20/run2d_gamma_D03,7_delta0,45_vA13.fits.gz");
	auto dragonModel = std::make_shared<cosmicrays::Dragon2D>(dragonFilename, particletypes);

	// integrator
	auto integrator = std::make_shared<SynchroIntegrator>(SynchroIntegrator(Sun08, dragonModel));

	// skymap
	int nside = 32;
	auto skymaps = std::make_shared<RadioSkymap>(RadioSkymap(nside, 408_MHz));
	skymaps->setIntegrator(integrator);

	auto output = std::make_shared<outputs::HEALPixFormat>("!example-synchro.fits.gz");

	skymaps->compute();
	skymaps->save(output);
}

}  // namespace hermes

int main(void) {
	hermes::exampleSynchro();

	return 0;
}
