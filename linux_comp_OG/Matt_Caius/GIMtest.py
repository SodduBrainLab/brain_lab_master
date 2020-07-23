from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import to_normalize, to_save_results, makedir,save_file
import time

def load_matrix(file):
    import numpy as np
    import scipy.io

    extension = file.split('.')[-1]
    if str(extension) == 'csv':
        return np.genfromtxt(file,delimiter = ',')
    elif str(extension) == 'npy':
        return np.load(file)
    elif str(extension) == 'mat':
        return scipy.io.loadmat(file)
    elif str(extension) == 'npz':
        return np.load(file)

# where it will go
output_path = 'D:/OneDrive/School/Research/ConnectomeOutput/GIMTEST/NewParams'

makedir(output_path)

def PlotGIM(output_path,network,resolution = 200):
    # where data comes from
    input_path = 'D:/OneDrive/School/Research/ConnectomeData/HCP_Average/' + network

    # temporary stuff
    file_name = "/Jij_avg.csv"

    # fetch the Jij csv file
    J = to_normalize(load_matrix(input_path + file_name))

    print(J, "\n\n")

    # Ising Parameters
    temperature_parameters = (
        -1, 4, resolution)  # Temperature parameters (initial tempeture, final temperature, number of steps)
    no_simulations = 3000  # Number of simulations after thermalization
    thermalize_time = 0.5  #
    no_simulations = 4000
    thermalize_time = 0.25
    makedir(output_path+"/" + network)
    save_path = output_path+"/" + network

    start_time = time.time()

    Simulated_FC, Critical_Temperature, E, M, S, H, meanSpins, timeCourses = generalized_ising(J,
                                                                                               temperature_parameters=temperature_parameters,
                                                                                               n_time_points=no_simulations,
                                                                                               thermalize_time=thermalize_time,
                                                                                               phi_variables=True,
                                                                                               return_tc=True,
                                                                                               temperature_distribution='log',
                                                                                               type="digital")

    to_save_results(temperature_parameters, J, E, M, H, S, Simulated_FC, Critical_Temperature,
                    output_path + "/" + network + "/",temperature_distribution='log')

    final_time = time.time()
    delta_time = final_time - start_time

    del Simulated_FC, Critical_Temperature, E, M, S, H, meanSpins, timeCourses

    print(delta_time)

if __name__ == '__main__':
    parcels = ["Aud","CO","CP","DMN","Dorsal","FP","RS","SMHand","SMMouth","Ventral","Visual"]

    for parcel in parcels:
        PlotGIM(output_path, parcel)


"""
parcels = ["Aud","CO","CP","DMN","Dorsal","FP","RS","SMHand","SMMouth","Ventral","Visual"]

for parcel in parcels:
    PlotGIM(output_path, parcel)
"""
