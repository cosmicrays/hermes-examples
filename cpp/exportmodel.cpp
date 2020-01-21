#include "hermes.h"

#include <iostream>
#include <memory>

namespace hermes {

// magnetic field models
auto WMAP07 = std::make_shared<WMAP07Field>(WMAP07Field());
auto Sun08 = std::make_shared<Sun08Field>(Sun08Field());
auto JF12 = std::make_shared<JF12Field>(JF12Field());
auto PT11 = std::make_shared<PT11Field>(PT11Field());

// gas models
auto gasCordes91 = std::make_shared<HII_Cordes91>(HII_Cordes91());
auto gasYMW16 = std::make_shared<YMW16>(YMW16());
	
// cosmic ray density models
auto simpleModel = std::make_shared<SimpleCRDensity>(SimpleCRDensity());
auto WMAP07Model = std::make_shared<WMAP07CRDensity>(WMAP07CRDensity());
auto Sun08Model = std::make_shared<Sun08CRDensity>(Sun08CRDensity());
std::vector<PID> particletypes = {Electron, Positron};
auto dragonModel = std::make_shared<Dragon2DCRDensity>(Dragon2DCRDensity(
                                getDataPath("CosmicRays/Gaggero17/run_2D.fits.gz"),
                                particletypes));

void printSpectrum() {
	
	//auto energy = std::next(dragonModel->begin());
	for(auto energy = dragonModel->begin(); energy != dragonModel->end(); ++energy) {
		Vector3QLength pos(8.3_kpc, 0, 0);
		auto density = dragonModel->getDensityPerEnergy(*energy, pos);
		std::cout << density << std::endl;
	}
}

void printGrid() {
	
	std::cout << "# X\tY\tZ\teta" << std::endl;
	auto energy = std::next(dragonModel->begin());
	//energy++;
	QLength x = 1_kpc;
	QLength y = 1_kpc;
#pragma omp critical(print)
	for (QLength x = -12_kpc; x < 12_kpc; x += 0.5_kpc)
		for (QLength y = -12_kpc; y < 12_kpc; y += 0.5_kpc)
			for (QLength z = -4_kpc; z < 4_kpc; z += 0.2_kpc) {
				Vector3QLength pos(x.getValue(), y.getValue(), z.getValue());
				auto density = dragonModel->getDensityPerEnergy(*energy, pos);
				//auto density = simpleModel->getDensityPerEnergy(*energy, pos);
				//auto density = (JF12->getField(pos)).getZ();
				//auto density = (PT11->getField(pos)).getR();
				//auto density = (testField->getField(pos)).getR();
				//if (density.getValue() == 0) continue;
				std::cout << x.getValue()/1_pc << "\t" <<
					     y.getValue()/1_pc << "\t" <<
					     z.getValue()/1_pc << "\t" <<
					     density << std::endl;
			}
}

} // namespace hermes

int main(void){

	//hermes::printSpectrum();
	hermes::printGrid();

	return 0;
}

