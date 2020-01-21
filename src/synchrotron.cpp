#include "hermes.h"

#include <iostream>
#include <memory>

namespace hermes {

void exampleSynchro() {

	// magnetic field models
	auto B = Vector3QMField(0_muG, 0_muG, 1_muG);
	auto ufield = std::make_shared<UniformMagneticField>(UniformMagneticField(B));
	auto JF12 = std::make_shared<JF12Field>(JF12Field());
	JF12->randomStriated(137);
	JF12->randomTurbulent(1337);
	auto PT11 = std::make_shared<PT11Field>(PT11Field());
	auto WMAP07 = std::make_shared<WMAP07Field>(WMAP07Field());
	auto Sun08 = std::make_shared<Sun08Field>(Sun08Field());
	
	// cosmic ray density models
	auto simpleModel = std::make_shared<SimpleCRDensity>(SimpleCRDensity());
	auto WMAP07Model = std::make_shared<WMAP07CRDensity>(WMAP07CRDensity());
	auto Sun08Model = std::make_shared<Sun08CRDensity>(Sun08CRDensity());
	
	std::vector<PID> particletypes = {Electron, Positron};
	auto dragonModel = std::make_shared<Dragon2DCRDensity>(Dragon2DCRDensity(
				getDataPath("CosmicRays/Gaggero17/run_2D.fits.gz"),
				particletypes)); 
	
	// integrator
	auto intSynchro = std::make_shared<SynchroIntegrator>(SynchroIntegrator(ufield, dragonModel));

	// skymap
	int nside = 32;
        //auto mask = std::make_shared<RectangularWindow>(RectangularWindow(
        //                QAngle(45_deg), QAngle(10_deg), QAngle(40_deg), QAngle(340_deg)));
	//auto skymaps = std::make_shared<RadioSkymapRange>(RadioSkymapRange(nside, 10_MHz, 100_GHz, 20));
	auto skymaps = std::make_shared<RadioSkymap>(RadioSkymap(nside, 408_MHz));
	//skymaps->setMask(mask);
	skymaps->setIntegrator(intSynchro);

	auto output = std::make_shared<FITSOutput>(FITSOutput("!example-synchro.fits.gz"));
	
	//auto energy = std::next(dragonModel->begin());
	/*for(auto energy = dragonModel->begin(); energy != dragonModel->end(); ++energy) {
		Vector3QLength pos(8.19_kpc, 0, 0.097_kpc);
		auto density = dragonModel->getDensityPerEnergy(*energy, pos);
		std::cout << *energy << " " << density << std::endl;
	}*/
	
	skymaps->compute();
	skymaps->save(output);
}

} // namespace hermes

int main(void){

	hermes::exampleSynchro();

	return 0;
}

