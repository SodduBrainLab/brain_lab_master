from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import *
from projects.phi.tools.utils import *
import numpy as np
import time
import pyphi

#where data comes from
input_path = '/home/brainlab/Desktop/Matt/ConnectomeData/'
#where it will go
output_path = '/home/brainlab/Desktop/Matt/ConnectomeOutput/Test_1/'

#temporary stuff
file_name = "collab_data.csv"
Output_filename = "CollabJij_"

#fetch the Jij csv file
J = to_normalize(np.loadtxt(input_path + file_name))
print(input_path+file_name)

def GIM2Phi(J,output_path,empirical_FC = [],tpmName = ''):

    # Ising Parameters
    temperature_parameters = (
    0.002, 3, 50)  # Temperature parameters (initial tempeture, final temperature, number of steps)
    no_simulations = 1200  # Number of simulations after thermalization
    thermalize_time = 0.3  #

    start_time = time.time()

    Simulated_FC, Critical_Temperature, E, M, S, H, meanSpins, timeCourses = generalized_ising(J,
                                                                                              temperature_parameters=temperature_parameters,
                                                                                              n_time_points=no_simulations,
                                                                                              thermalize_time=thermalize_time,
                                                                                              phi_variables=True,
                                                                                              return_tc=True,
                                                                                              type="digital")

    final_time = time.time()
    delta_time = final_time - start_time

    print("It took " + str(delta_time) + " seconds to calculate the simulated functional connectivity matricies\n\n")

    TPMs = list()
    for T in range(timeCourses.shape[-1]):

        tpm, state_total, frequency = main_tpm_branch(np.copy(timeCourses[..., T]))

        # Normalizing respect to rows
        for div in range(len(state_total)):
            if state_total[div] != 0.0:
                tpm[div, :] /= state_total[div]

        TPMs.append(tpm)

    tstar = Find_Tstar(TPMs,empirical_FC)
    tstarTPM = TPMs[tstar]

    # Save the tstar TPM
    save_tpm(tstarTPM,output_path,tpmName)

    # Calculate Phi

    tpm = pyphi.convert.to_2dimensional(pyphi.convert.state_by_state2state_by_node(tstarTPM))

    start_time = time.time()
    meanPhi, phiSum = to_calculate_mean_phi(tpm, meanSpins[:, tstar])

    print("It took: ", time.time() - start_time, "s")

    return meanPhi, phiSum




