from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import to_normalize,makedir,to_save_results,file_exists
from projects.phi.tools.utils import main_tpm_branch,save_tpm,load_matrix
from projects.phi.utils import to_calculate_mean_phi
import numpy as np
import time
import pyphi
import random

# where data comes from
input_path = '/home/brainlab/Desktop/Matt/ConnectomeData/HCP_Average/CO/'
# where it will go
output_path = '/home/brainlab/Desktop/Matt/ConnectomeOutput/'

makedir(output_path)

# temporary stuff
file_name = "Jij_avg.csv"

# fetch the Jij csv file
J = to_normalize(load_matrix(input_path + file_name))

def PhiOfT(J,output_path,network,resolution = 200):
    # Ising Parameters
    temperature_parameters = (
        -1, 4, resolution)  # Temperature parameters (initial tempeture, final temperature, number of steps)
    no_simulations = 3000  # Number of simulations after thermalization
    thermalize_time = 0.5  #
    makedir(output_path+"/" + network)

    start_time = time.time()

    Simulated_FC, Critical_Temperature, E, M, S, H, meanSpins, timeCourses = generalized_ising(J,
                                                                                               temperature_parameters=temperature_parameters,
                                                                                               n_time_points=no_simulations,
                                                                                               thermalize_time=thermalize_time,
                                                                                               phi_variables=True,
                                                                                               return_tc=True,
                                                                                               temperature_distribution='log',
                                                                                               type="digital")

    final_time = time.time()
    delta_time = final_time - start_time

    to_save_results(temperature_parameters,J,E,M,H,S,Simulated_FC,Critical_Temperature,output_path + "/" + network + "/")

    print("It took " + str(delta_time) + " seconds to calculate the simulated functional connectivity matricies\n\n")

    TPMs = list()


    for T in range(timeCourses.shape[-1]):

        tpm, state_total, frequency = main_tpm_branch(np.copy(timeCourses[..., T]))

        # Normalizing respect to rows
        for div in range(len(state_total)):
            if state_total[div] != 0.0:
                tpm[div, :] /= state_total[div]

        TPMs.append(tpm)

    count = 0

    print("calculating", len(TPMs), "Phi Values\n\n")
    print(Critical_Temperature,"\n\n")

    for TPM in TPMs:
        phiOut = output_path + "/" + network + "/" + str(count + 1)
        makedir(phiOut)
        print(phiOut)
        if not file_exists(phiOut+"/TPM.csv"):
            np.savetxt(phiOut+"/TPM.csv",TPM)
            save_tpm(TPM,phiOut,count+1)
        else:
            print("This TPM is already saved")
        count += 1

    ts = np.logspace(temperature_parameters[0], np.log10(temperature_parameters[1]), num=temperature_parameters[2])
    print(temperature_parameters)

    for count in range(resolution):

        phiOut = output_path+"/" + network + "/" + str(count+1)
        makedir(phiOut)
        print(phiOut)

        if not file_exists(phiOut + "/phi.csv"):

            TPM = np.genfromtxt(phiOut + "/TPM.csv")
            tpm = pyphi.convert.to_2dimensional(pyphi.convert.state_by_state2state_by_node(TPM))

            start_time = time.time()
            meanPhi, phiSum, phiSus= to_calculate_mean_phi(tpm, meanSpins[:, count],ts[count])
            print("\n\nIt took: ", time.time() - start_time, "s to calculate one Phi Value\n")


            np.savetxt(phiOut + "/phi.csv",[meanPhi, phiSum, phiSus])
        else:
            print("this one is done")


PhiOfT(J,output_path,"COTEST",resolution=200)



