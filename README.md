# Global Sensitivity Analysis for the Program for Observation Well Representation in Fractured Aquifer Dual-continuum Simulations

***Introduction***

This repository hosts the inputs and outptus relating to the global sensitivity analysis (GSA) performed for the Program for Observation Well Representation in Fractured Aquifer Dual-continuum Simulations (POWeR-FADS), presented in Jeannot et al.(submitted). This GSA is undertaken by the method of Sobol(2001), as implemented in PESTPP-SEN (White et al., 2020), and uses 100000 uniformly distributed parameters samples. For more details, refer to Jeannot et al.(submitted).

The folders GSA_test1_sobol100000_unif and GSA_test2_sobol100000_unif refer to a GSA undertaken respectively for synthetic test cases 1 and 2, as detailed in Jeannot et al.(submitted). In each of these subfolders, the GSA can be launched by opening a linux terminal and passing the following command: ./pestpp-sen case.pst
However, please note that in practice, the costly computation time of the GSA requires to use PESTPP-SEN in parallel for achieving an acceptable computation time for this simulation. For more details on the parallel implementation of PESTPP-SEN, please refer to White et al.(2020)

***Results***

The following chart can be drawn from the outptus of the GSA :

![test](https://user-images.githubusercontent.com/67539849/197721114-3c1db629-46e2-4f72-9ece-281fc904d75f.png)

Fig 1 : Global sensitivity analysis of POWeR-FADS undertaken using the method of Sobol (2001) implemented in PESTPP-SEN (White et al., 2020), with 100000 uniformly distributed parameter samples, for (a) synthetic test case 1 and (b) synthetic test case 2. zbot_f is the altitude of lowest interception of the fracture network by the well. Ksm and Ksf are the saturated hydraulic conductivity respectively in the matrix and fracture media. αm and nm are Van Genuchten coefficients (Van Genuchten,1980) for the matrix, while αf and nf are Van Genuchten coefficients for the fracture network. ∆e is the coupling length, i.e. the width of the interface between the well and the media. Rdrill is the drill radius of the well and ωdrill is the porosity of the material used to fill the space between the tube of the well and Rdrill. ε is the convergence criterion used by POWeR-FADS. 


***Bibliography***

Jeannot, B., Schaper, L., and Habets, F., submitted. Water Level in Observation Wells Simulated from Fracture and Matrix Water Heads Outputed by Dual-continuum Hydrogeological Models : POWeR-FADS. _Water Resources research_

Sobol, I., 2001. Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates. _Mathematics and Computers in Simulation_, 55(1-3), pp.271-280.

Van Genuchten M Th, 1980. A closed-form equation for predicting the hydraulic conductivity of unsaturated soils, Soil Sci. Soc. Am., 44, 892-898

White, J.T., Hunt, R.J., Doherty, J.E., and Fienen, M.N., 2020. Approaches to highly parameterized inversion: Pest++ version 5, a software suite for parameter estimation, uncertainty analysis, management optimization and sensitivity analysis, _US Geological Survey Techniques and Methods_. 7C26, 51 p. 
