#include <iostream>
#include <memory>

#include "hermes.h"

namespace hermes {

void exampleRM() {
	// magnetic field models
	auto B = Vector3QMField(0_muG, 0_muG, 1_muG);
	auto Sun08 = std::make_shared<magneticfields::Sun08>();
	// Sun08->randomTurbulent(1337);
	auto JF12 = std::make_shared<magneticfields::JF12>();
	JF12->randomStriated(137);
	JF12->randomTurbulent(1337);
	auto PT11 = std::make_shared<magneticfields::PT11>();

	// gas models
	auto gasCordes91 = std::make_shared<ionizedgas::HII_Cordes91>();
	auto gasYMW16 = std::make_shared<ionizedgas::YMW16>();

	// integrator
	auto integrator = std::make_shared<RotationMeasureIntegrator>(JF12, gasYMW16);
	auto sun_pos = Vector3QLength(8.5_kpc, 0_kpc, 0_pc);
	integrator->setObsPosition(sun_pos);

	// skymap
	int nside = 32;
	auto skymap = std::make_shared<RotationMeasureSkymap>(nside);
	skymap->setIntegrator(integrator);
	skymap->compute();

	// save
	auto output = std::make_shared<outputs::HEALPixFormat>("!example.fits.gz");
	skymap->save(output);
}

}  // namespace hermes

int main(void) {
	hermes::exampleRM();

	return 0;
}
