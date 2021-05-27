#include "hermes.h"

#include <iostream>
#include <memory>

namespace hermes {

void exampleIC() {

    // cosmic ray density models
    auto simpleModel = std::make_shared<cosmicrays::SimpleCR>();
    std::vector<PID> particletypes = {Proton};
    auto dragonFilename = getDataPath("CosmicRays/Fornieri20/run2d_gamma_D03,7_delta0,45_vA13.fits.gz");
    auto dragonModel = std::make_shared<cosmicrays::Dragon2D>(dragonFilename, particletypes);

    // photon field
    auto cmb = std::make_shared<photonfields::CMB>();
    auto isrf = std::make_shared<photonfields::ISRF>();

    // interaction
    auto kleinnishina = std::make_shared<interactions::KleinNishina>();

    // integrator
    auto intIC = std::make_shared<InverseComptonIntegrator>(dragonModel, isrf, kleinnishina);

    // skymap
    int nside = 32;
    auto mask = std::make_shared<RectangularWindow>(std::array<QAngle, 2> {-8_deg, 8_deg}, std::array<QAngle, 2> {-80_deg, 80_deg});
    auto skymaps = std::make_shared<GammaSkymap>(GammaSkymap(nside, 100_MeV));
    skymaps->setMask(mask);
    skymaps->setIntegrator(intIC);

    auto output = std::make_shared<outputs::HEALPixFormat>("!example-ic.fits.gz");

    skymaps->compute();
    skymaps->save(output);
}

} // namespace hermes

int main(void){

    hermes::exampleIC();

    return 0;
}

