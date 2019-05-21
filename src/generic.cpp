#include "hermes.h"

#include <iostream>
#include <memory>

namespace hermes {

void exampleGeneric() {

	// magnetic field models
	auto JF12 = std::make_shared<JF12Field>(JF12Field());
	//JF12->randomStriated(137);
	//JF12->randomTurbulent(1337);
	auto PT11 = std::make_shared<PT11Field>(PT11Field());
	auto WMAP07 = std::make_shared<WMAP07Field>(WMAP07Field());
	auto Sun08 = std::make_shared<Sun08Field>(Sun08Field());
	
	// cosmic ray density models
	auto simpleModel = std::make_shared<SimpleCRDensity>(SimpleCRDensity());
	auto WMAP07Model = std::make_shared<WMAP07CRDensity>(WMAP07CRDensity());
	auto Sun08Model = std::make_shared<Sun08CRDensity>(Sun08CRDensity());
	//auto dragonModel = std::make_shared<DragonCRDensity>(DragonCRDensity(
	//	getDataPath("RingModelDensity/run_2D.fits"), Electron, DragonFileType::_2D)); 
	
	// gas models
	auto gasCordes91 = std::make_shared<HII_Cordes91>(HII_Cordes91());
	auto gasYMW16 = std::make_shared<YMW16>(YMW16());
	auto ringModel = std::make_shared<RingModelDensity>(RingModelDensity());
	
	// integrator
	auto intGeneric = std::make_shared<GenericIntegrator>(
		GenericIntegrator(JF12, simpleModel, gasYMW16, ringModel));

	// skymap
	int nside = 64;
	auto skymap = std::make_shared<GenericSkymap>(GenericSkymap(nside, 10_MHz));
	skymap->setIntegrator(intGeneric);

	auto output = std::make_shared<FITSOutput>(FITSOutput("!example-generic.fits.gz"));
	
	skymap->compute();
	skymap->save(output);
}

} // namespace hermes

int main(void){

	hermes::exampleGeneric();

	return 0;
}

