#include "hermes.h"

#include <iostream>
#include <memory>

namespace hermes {

void exampleFreeFree() {
	// gas models
	auto gasCordes91 = std::make_shared<ionizedgas::HII_Cordes91>();
    auto gasYMW16 = std::make_shared<ionizedgas::YMW16>();
	
	// integrator
    auto intFreeFree = std::make_shared<FreeFreeIntegrator>(FreeFreeIntegrator(gasYMW16));

	// skymap
	//int nside = 32;
	//auto skymaps = std::make_shared<RadioSkymapRange>(RadioSkymapRange(nside, 10_MHz, 10_GHz, 10));
    
//	skymaps->setIntegrator(intFreeFree);
//	skymaps->compute();
//
//	// save
//	auto output = std::make_shared<FITSOutput>(FITSOutput("!example-freefree.fits.gz"));
//	skymaps->save(output);
}

} // namespace hermes

int main(void){

	hermes::exampleFreeFree();

	return 0;
}

