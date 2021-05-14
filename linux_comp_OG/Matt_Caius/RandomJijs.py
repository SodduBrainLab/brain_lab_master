import numpy as np
from projects.generalize_ising_model.tools.utils import to_find_critical_temperature
from projects.phi.tools.utils import load_matrix
from sklearn.metrics import mean_squared_error
from linux_comp_OG.Matt_Caius.CalculateFunctionalConnectivity import subject_rhoIJ
import time
from linux_comp_OG.projects.generalize_ising_model.core import generalized_ising
import pandas
import os
import matplotlib.pyplot as plt
import time


Random_Jijs = list()
input_path = "D:/OneDrive/School/Research/ConnectomeData/random_j/random_j/"
output_path = "D:/OneDrive/School/Research/ConnectomeData/random_j_sims/"

for i in range(159):
    data = input_path + "J_" + str(i) + ".npz"

    test = np.load(data)

    for item in test.files:
        J = test[item]
        Random_Jijs.append(J)

avg_rhoIJs = dict()



for network in subject_rhoIJ.keys():

    avg_rhoIJs[network] = np.mean(subject_rhoIJ[network], axis = 0)



def gen_sim_FCs(J):

    temperature_parameters = (
        -1, 4, 200)  # Temperature parameters (initial tempeture, final temperature, number of steps)
    no_simulations = 3000  # Number of simulations after thermalization
    thermalize_time = 0.5  #

    Simulated_FC, Critical_Temperature, E, M, S, H = generalized_ising(J,
                                                                                               temperature_parameters=temperature_parameters,
                                                                                               n_time_points=no_simulations,
                                                                                               thermalize_time=thermalize_time,
                                                                                               phi_variables=False,
                                                                                               return_tc=False,
                                                                                               temperature_distribution='log',
                                                                                               type="digital")

    del Critical_Temperature,E,M,S,H,temperature_parameters,no_simulations,thermalize_time

    return Simulated_FC

def calculate_minMSEs(sim_FCs_list, RhoIJs):
    minMSEs = dict()
    avg_minMSEs = dict()
    for network in RhoIJs:
        MSEs= list()
        minMSEs[network] = list()
        print(network)
        rhoIJ = RhoIJs[network]

        for Jij in sim_FCs_list:
            for i in range(Jij.shape[-1]):
                simFC = Jij[:, :, i]
                MSEs.append(mean_squared_error(np.ravel(rhoIJ), np.ravel(simFC)))
                del simFC

            MSEPandas = pandas.Series(np.ravel(MSEs))
            mseWindows = MSEPandas.rolling(5)
            mov_mean_norms = mseWindows.mean()
            del mseWindows
            newMSE = np.asarray(mov_mean_norms.tolist())
            newMSE = newMSE[~np.isnan(newMSE)]

            minMSEs[network].append(min(newMSE))
            print(minMSEs[network])
            del newMSE
        del rhoIJ
        avg_minMSEs[network] = np.mean(minMSEs[network])

    return avg_minMSEs

if __name__ == "__main__":

    sim_FCs_Jijs = list()
    count = 0
    for Jij in Random_Jijs:
        filename = output_path + "J_" + str(count) + ".npy"
        if not os.path.exists(filename):
            sim_FCs = gen_sim_FCs(Jij)
            np.save(filename, sim_FCs)
            del sim_FCs
        sim_FC = np.load(filename)
        plt.imshow(sim_FC[:,:,100])
        plt.colorbar()
        plt.show()
        sim_FCs_Jijs.append(np.nan_to_num(np.load(filename)))
        count += 1

    avg_minMSEs = calculate_minMSEs(sim_FCs_Jijs, avg_rhoIJs)

    print(avg_minMSEs)







