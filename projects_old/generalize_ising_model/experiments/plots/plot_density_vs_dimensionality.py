from projects.generalize_ising_model.tools.utils import to_normalize, to_save_results, correlation_function, dim, find_nearest
from os import walk
import numpy as np
import pickle
from natsort import natsorted
import matplotlib.pyplot as plt
import os
import matplotlib.patches as mpatches
from networkx.utils import *

default_size = 20
susceptibility_exp = []
dimensionality_ = []
degre_ = []
max_degre_ = []

path_simulation_output = ['/home/brainlab/Desktop/Rudas/Data/Ising/new_experiment/simulation/000_density_20']
                          #'/home/brainlab/Desktop/Rudas/Data/Ising/experiment_2/simulation/13_undirected_unweighted_0.8']
#                          '/home/brainlab/Desktop/Rudas/Data/Ising/experiment_2/simulation/3_undirected_unweighted',
#                          '/home/brainlab/Desktop/Rudas/Data/Ising/experiment_2/simulation/4_undirected_weighted']

sizes_ = np.linspace(0.05, 100, num=19).astype(np.int16)

for path in path_simulation_output:
    print(path)
    dimensionality_exp = []
    for simulation in natsorted(os.listdir(path)):

        path_simulation = path + '/' + simulation

        if os.path.isdir(path_simulation):
            print()
            print(simulation)
            print()

            pkl_file = open(path_simulation + '/parameters.pkl', 'rb')
            simulation_parameters = pickle.load(pkl_file)
            pkl_file.close()
            ts = np.linspace(simulation_parameters['temperature_parameters'][0],
                             simulation_parameters['temperature_parameters'][1],
                             simulation_parameters['temperature_parameters'][2])

            susceptibility_sim = []
            ctemp_sim = []
            dimensionality_sim = []
            for entity in natsorted(os.listdir(path_simulation)):
                path_entity = path_simulation + '/' + entity + '/'

                if os.path.isdir(path_entity):
                    #print(entity)

                    simulated_matrix = np.load(path_entity + 'sim_fc.npy')
                    J = np.loadtxt(path_entity + 'J_ij.csv', delimiter=',')
                    critical_temperature = np.loadtxt(path_entity + 'ctem.csv', delimiter=',')
                    ctemp_sim.append(critical_temperature)
                    susceptibility_sim.append(np.loadtxt(path_entity + 'susc.csv', delimiter=','))

                    c, r = correlation_function(simulated_matrix, J)

                    index_ct = find_nearest(ts, critical_temperature)
                    dimensionality = dim(c, r, index_ct)
                    if not np.isinf(r[-1]):
                        print(entity)
                        print(dimensionality)
                        dimensionality_sim.append(dimensionality)
#            if dimensionality_sim:
#                dimensionality_sim.remove(
#                    np.max(dimensionality_sim))  # Removing maximal dimensionality (Probably is other outlier)
            dimensionality_exp.append(dimensionality_sim)
    dimensionality_.append(dimensionality_exp)

fig, ax = plt.subplots(figsize=(10, 7))

colors = ['blue', 'green', 'red', 'black']
cont = 0
for exp in dimensionality_:
    new_dim = []
    new_size = []
    for dim, size in zip(exp, sizes_):
        if dim:
            new_dim.append(dim)
            new_size.append(size)

    parts = plt.violinplot(new_dim, positions=np.array(new_size)/10, showmeans=True, showmedians=False)
    for pc in parts['bodies']:
        pc.set_facecolor(colors[cont])
    cont += 1

blue_patch = mpatches.Patch(color='blue', label='Graph Size = 20')
#green_patch = mpatches.Patch(color='green', label='Graph Size = 40')
#red_patch = mpatches.Patch(color='red', label='Graph Size = 60')
# black_patch = mpatches.Patch(color='black', label='Weighted 80%')

plt.legend(handles=[blue_patch])
plt.xlabel("Graph density")
plt.ylabel("Dimensionality")

plt.xticks(np.array(new_size)/10, list(map(str, new_size)))
plt.show()