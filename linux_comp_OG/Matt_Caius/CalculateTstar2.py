import matplotlib.pyplot as plt
import os
import string
from scipy import stats
from sklearn.metrics import mean_squared_error
import pandas
import numpy as np
from linux_comp_OG.projects.generalize_ising_model.tools.utils import makedir, to_find_critical_temperature
from linux_comp_OG.projects.phi.tools.utils import load_matrix

time_series_Path = "D:/OneDrive/School/Research/preprocessing"
sim_FC_source = "D:/OneDrive/School/Research/ConnectomeOutput/"
outputPath = "D:/OneDrive/School/Research/ConnectomeOutput/FiguresNew/"
# sim_FC_source = "D:/OneDrive/School/Research/ConnectomeOutput/GIMTEST/NewParams/"
no_subject = 20

min_temps = [53,52,52,65,56,47,57,93,59,43,84]

networks = [
    "Aud",
    "CO",
    "CP",
    "DMN",
    "Dorsal",
    "FP",
    "RS",
    "SMHand",
    "SMMouth",
    "Ventral",
    "Visual"
]

def extract_rho(path):

    time_series = np.squeeze(load_matrix(path))

    shape_ts = time_series.shape

    assert len(shape_ts) == 2
    assert shape_ts[0] != shape_ts[1]

    if shape_ts[0]>shape_ts[1]:
        time_series=time_series.T


    rho = np.corrcoef(time_series)

    return rho

time_series_paths = list()

for root, dir, file in os.walk(time_series_Path):

    filename = str(file).strip(string.punctuation)

    if "time" in filename:
        filePath = os.path.join(root, filename)

        time_series_paths.append(filePath)



sim_FCs = dict()
subject_rhoIJ = dict()

for network in networks:
    subject_rhoIJ[network] = list()
    sim_FCs[network] = np.nan_to_num(np.load(sim_FC_source + network + "/sim_fc.npy"))


i = 0

for subject in range(no_subject):
    for network in networks:
        subject_rhoIJ[network].append(extract_rho(time_series_paths[i]))
        print(network,time_series_paths[i])
        i += 1

ts = np.logspace(-1,np.log10(4),num=200)

tstars = dict()
Norms = dict()
Kstests = dict()
MSEs = dict()
minMSEs = list()

for network, temp in zip(networks, min_temps):
    avg_rhoIJ = np.mean(subject_rhoIJ[network], axis=0)
    Norms[network] = np.zeros([sim_FCs[network].shape[-1], 1], dtype=float)
    Kstests[network] = np.zeros([sim_FCs[network].shape[-1], 1], dtype=float)
    MSEs[network] = np.zeros([sim_FCs[network].shape[-1], 1], dtype=float)


    for i in range(sim_FCs[network].shape[-1]):
        sim_FC = sim_FCs[network][..., i]
        diff = sim_FC - avg_rhoIJ
        Norms[network][i] = np.linalg.norm(diff)
        Kstests[network][i] = stats.ks_2samp(np.ravel(sim_FC), np.ravel(avg_rhoIJ))[0]
        MSEs[network][i] = mean_squared_error(np.ravel(avg_rhoIJ), np.ravel(sim_FC))

    plt.scatter(ts, Norms[network])
    plt.title("Froebenius Norm for " + network)
    plt.xlim(0.1,4)
    plt.semilogx()
    plt.savefig(outputPath + network + "_Fro.png")
    plt.clf()
    plt.scatter(ts, Kstests[network])
    plt.title("KStest for " + network)
    plt.xlim(0.1, 4)
    plt.semilogx()
    plt.savefig(outputPath + network + "_KS.png")
    plt.clf()
    plt.scatter(ts, MSEs[network])
    plt.title("MSE for " + network)
    plt.xlim(0.1, 4)
    plt.semilogx()
    plt.savefig(outputPath + network + "_MSE.png")
    plt.clf()

    MSEPandas = pandas.Series(np.ravel(MSEs[network][range(temp, 200)]))
    TsPandas = pandas.Series(ts[range(temp, 200)])
    mseWindows = MSEPandas.rolling(5)
    tsWindows = TsPandas.rolling(5)
    mov_mean_norms = mseWindows.mean()
    mov_mean_temps = tsWindows.mean()
    newMSE = np.asarray(mov_mean_norms.tolist())
    newTemps = np.asarray(mov_mean_temps.tolist())
    newMSE = newMSE[~np.isnan(newMSE)]
    newTemps = newTemps[~np.isnan(newTemps)]

    plt.scatter(newTemps, newMSE)
    plt.xlabel("Temperatures")
    plt.ylabel("MSE")
    plt.title("Smoothed out MSE for " + network)
    plt.xlim(0.1, 4)
    plt.semilogx()
    plt.savefig(outputPath + network + "_SmoothMSE.png")
    plt.clf()

    tstars[network] = to_find_critical_temperature(-newMSE, newTemps)
    minMSEs.append(min(newMSE))
