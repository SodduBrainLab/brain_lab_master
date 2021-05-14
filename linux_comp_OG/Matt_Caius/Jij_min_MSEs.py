from linux_comp_OG.projects.generalize_ising_model.tools.utils import to_find_critical_temperature
from projects.phi.tools.utils import load_matrix
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
import os
import string


sim_FC_source = "D:/OneDrive/School/Research/ConnectomeOutput/"
Jij_Path = "D:/OneDrive/School/Research/ConnectomeData/HCP_Average/"
networks = ["Aud","CO","CP","DMN","Dorsal","FP","RS","SMHand","SMMouth","Ventral","Visual"]

min_temps = [53,52,52,65,56,47,57,93,59,43,84]
ts = np.logspace(-1,np.log10(4),num=200)
Jij_min_MSEs = list()

for network, temp in zip(networks, min_temps):
    input_path = Jij_Path + network + "/Jij_avg.csv"
    J = load_matrix(input_path)
    MSEs = list()

    sim_FCs = np.nan_to_num(np.load(sim_FC_source + network + "/sim_fc.npy"))

    for i in range(sim_FCs.shape[-1]):
        sim_FC = sim_FCs[..., i]
        MSEs.append(mean_squared_error(np.ravel(J), np.ravel(sim_FC)))

    Jij_min_MSEs.append(to_find_critical_temperature(-np.asarray(MSEs[temp:]), np.asarray(ts[temp:])))
