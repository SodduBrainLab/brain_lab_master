from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import to_normalize, to_save_results, makedir,save_file
from projects.phi.tools.utils import load_matrix, file_exists, save_tpm
from projects.phi.utils import *
import time


# where it will go
output_path = 'D:\OneDrive\School\Research\ConnectomeOutput\GIMTEST'

makedir(output_path)




def PhiOfT2(output_path,network,resolution = 200):
    # where data comes from
    input_path = 'D:/OneDrive/School/Research/ConnectomeData/'+network+"/"

    # temporary stuff
    file_name = "Jij_avg.csv"

    # fetch the Jij csv file
    J = to_normalize(load_matrix(input_path + file_name))

    print(J, "\n\n")

    # Ising Parameters
    temperature_parameters = (
        -1, 4, resolution)  # Temperature parameters (initial tempeture, final temperature, number of steps)
    # no_simulations = 3000  # Number of simulations after thermalization
    # thermalize_time = 0.5  #
    no_simulations = 4000
    thermalize_time = 0.25
    makedir(output_path+"/" + network)
    save_path = output_path+"/" + network

    if True:

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

        to_save_results(temperature_parameters, J, E, M, H, S, Simulated_FC, Critical_Temperature,
                        output_path + "/" + network + "/")

        print("It took " + str(delta_time) + " seconds to calculate the simulated functional connectivity matricies\n\n")

        save_file(meanSpins, save_path + "/", 'spin_mean')
        save_file(timeCourses, save_path + "/", 'time_course')

    ts = np.logspace(temperature_parameters[0], np.log10(temperature_parameters[1]), num=temperature_parameters[2])

    print("calculating", resolution, "Phi Values\n\n")
    print(Critical_Temperature, "\n\n")

    FPMs = list()

    count = 0



    for temp in ts:
        phiOut = output_path + "/" + network + "/" + str(count + 1)
        makedir(phiOut)
        tpm, fpm = to_estimate_tpm_from_ising_model(J, temp)
        print("tpm is: ", tpm,"\n\n")
        print("fpm is:", fpm,"\n\n")
        FPMs.append(fpm)
        save_tpm(tpm, phiOut, count + 1)
        count += 1

    count = 0

    for FPM in FPMs:
        phiOut = output_path + "/" + network + "/" + str(count + 1)
        makedir(phiOut)
        print(phiOut)

        if not file_exists(phiOut + "/phi.csv"):
            start_time = time.time()

            phi_, phiSum, phiSus = to_calculate_mean_phi(FPM, meanSpins[:, count], temp)
            print("It took,", time.time()-start_time, "to calculate phi")

            np.savetxt(phiOut + "/phi.csv", [phi_, phiSum, phiSus])

        else:
            print("This is already done")



        count += 1

parcels = ['Ventral', 'Visual']

for parcel in parcels:
    PhiOfT2(output_path, parcel)



