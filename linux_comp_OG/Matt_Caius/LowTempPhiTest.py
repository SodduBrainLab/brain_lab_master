from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import *
from projects.phi.tools.utils import *
import numpy as np
import time


#where data comes from
input_path = '/home/brainlab/Desktop/Matt/ConnectomeData/'
#where it will go
output_path = '/home/brainlab/Desktop/Matt/ConnectomeOutput/LowTemp/'

if not os._exists(output_path):
    makedir(output_path)

#temporary stuff
file_name = "collab_data.csv"

#fetch the Jij csv file
J = to_normalize(np.loadtxt(input_path + file_name))
print(input_path+file_name)


# Ising Parameters
temperature_parameters = (
    0.002, 1, 20)  # Temperature parameters (initial tempeture, final temperature, number of steps)
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

to_save_results(temperature_parameters,J,E,M,S,H,Simulated_FC,Critical_Temperature,output_path)

TPMs = list()
count = 20
for T in range(timeCourses.shape[-1]):

    tpm, state_total, frequency = main_tpm_branch(np.copy(timeCourses[..., T]))

    # Normalizing respect to rows
    for div in range(len(state_total)):
        if state_total[div] != 0.0:
            tpm[div, :] /= state_total[div]

    TPMs.append(tpm)
    # save_tpm(tpm,output_path,count)
    # print("TPM SAVED")

    count += 1