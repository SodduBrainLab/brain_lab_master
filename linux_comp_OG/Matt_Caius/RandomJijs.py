import numpy as np
from projects.generalize_ising_model.tools.utils import to_find_critical_temperature
from projects.phi.tools.utils import load_matrix
from sklearn.metrics import mean_squared_error
from linux_comp_OG.Matt_Caius.CalculateFunctionalConnectivity import subject_rhoIJ
import time
from linux_comp_OG.projects.generalize_ising_model.core import generalized_ising
import pandas
import time, sys
from IPython.display import clear_output
import gc
import objgraph

def update_bar(progress):
    bar_length = 20
    block = int(round(bar_length * progress))
    clear_output(wait = True)
    if progress == 1:
        print("DONE")
        return None
    text = "Progress: [{0}] {1:.1f}%".format( "#" * block + "-" * (bar_length - block), progress * 100)
    print(text)


Random_Jijs = list()
input_path = "D:/OneDrive/School/Research/ConnectomeData/random_j/random_j/"

for i in range(159):
    data = input_path + "J_" + str(i) + ".npz"

    test = np.load(data)

    for item in test.files:
        J = test[item]
        Random_Jijs.append(J)

avg_rhoIJs = dict()

for network in subject_rhoIJ:
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

    print(Simulated_FC.size * Simulated_FC.itemsize)

    return Simulated_FC


def calculate_minMSEs(sim_FCs_list, RhoIJs):
    MSEs = dict()
    minMSEs = dict()
    for network in RhoIJs:
        MSEs[network] = list()
        rhoIJ = RhoIJs[network]

        for Jij in sim_FCs_list:
            for simFC in Jij:
                MSEs[network].append(mean_squared_error(np.ravel(rhoIJ), np.ravel(simFC)))
                del simFC

            MSEPandas = pandas.Series(np.ravel(MSEs[network]))
            mseWindows = MSEPandas.rolling(5)
            mov_mean_norms = mseWindows.mean()
            del mseWindows
            newMSE = np.asarray(mov_mean_norms.tolist())
            newMSE = newMSE[~np.isnan(newMSE)]

            minMSEs[network].append(min(newMSE))
            del newMSE
        del rhoIJ

    return minMSEs

if __name__ == "__main__":
    sim_FCs_list = list()

    progress = 0
    update_bar(progress)
    gc.collect()

    for Jij in Random_Jijs:
        sim_FCs_list.append(gen_sim_FCs(Jij))
        progress += 1/len(Random_Jijs)
        update_bar(progress)
        gc.collect()

    minMSEs = calculate_minMSEs(sim_FCs_list, avg_rhoIJs)

    print(minMSEs)





