#include "hermes.h"

#include <iostream>
#include <memory>

namespace hermes {

void examplePion() {

	// cosmic ray density models
	auto simpleModel = std::make_shared<SimpleCRDensity>(SimpleCRDensity());
	std::vector<PID> particletypes = {Electron, Positron};
	auto dragonModel = std::make_shared<DragonCRDensity>(DragonCRDensity(
				getDataPath("DragonRuns/run_2D.fits.gz"),
				particletypes, DragonFileType::_2D)); 

	// interaction
	auto kamae = std::make_shared<Kamae06>(Kamae06());

	// HI model
	auto ringModel = std::make_shared<RingModelDensity>(RingModelDensity());
	
	// integrator
	auto intPiZero = std::make_shared<PiZeroIntegrator>(
		PiZeroIntegrator(dragonModel, ringModel, kamae));

	// skymap
	int nside = 32;
	auto skymap = std::make_shared<DiffFluxSkymap>(DiffFluxSkymap(nside, 1_GeV));
	skymap->setIntegrator(intPiZero);

	auto output = std::make_shared<FITSOutput>(FITSOutput("!example-pion.fits.gz"));
	
	skymap->compute();
	skymap->save(output);
}

} // namespace hermes

int main(void){

	hermes::examplePion();

	return 0;
}

