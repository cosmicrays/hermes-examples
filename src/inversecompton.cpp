#include "hermes.h"

#include <iostream>
#include <memory>

namespace hermes {

void exampleIC() {

	// cosmic ray density models
	auto simpleModel = std::make_shared<SimpleCRDensity>(SimpleCRDensity());
	std::vector<PID> particletypes = {Proton};
	auto dragonModel = std::make_shared<Dragon2DCRDensity>(Dragon2DCRDensity(
				getDataPath("CosmicRays/Gaggero17/run_2D.fits.gz"),
				particletypes)); 

	// photon field
	auto cmb = std::make_shared<CMB>(CMB());
	auto isrf = std::make_shared<ISRF>(ISRF());

	// interaction
        auto kleinnishina = std::make_shared<KleinNishina>(KleinNishina());

        // integrator
        auto intIC = std::make_shared<InverseComptonIntegrator>(
                InverseComptonIntegrator(dragonModel, isrf, kleinnishina));
        
        // skymap
        int nside = 32;
        auto mask = std::make_shared<RectangularWindow>(RectangularWindow(
                        QAngle(8_deg), QAngle(-8_deg), QAngle(-80_deg), QAngle(80_deg)));
        auto skymaps = std::make_shared<DiffFluxSkymap>(DiffFluxSkymap(nside, 100_MeV));
        //auto skymaps = std::make_shared<DiffFluxSkymapRange>(DiffFluxSkymapRange(nside, 100_MeV, 300_GeV, 10));
        skymaps->setMask(mask);
        skymaps->setIntegrator(intIC);

	auto output = std::make_shared<FITSOutput>(FITSOutput("!example-ic.fits.gz"));
	
	skymaps->compute();
	skymaps->save(output);
}

} // namespace hermes

int main(void){

	hermes::exampleIC();

	return 0;
}

