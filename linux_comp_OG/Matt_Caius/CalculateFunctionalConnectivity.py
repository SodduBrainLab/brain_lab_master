from linux_comp_OG.projects.generalize_ising_model.tools.utils import makedir, to_find_critical_temperature
from linux_comp_OG.projects.phi.tools.utils import load_matrix
import numpy as np
import matplotlib.pyplot as plt
import os
import string
from scipy import stats
from sklearn.metrics import mean_squared_error
import pandas

time_series_Path = "D:/OneDrive/School/Research/preprocessing"
sim_FC_source = "D:/OneDrive/School/Research/ConnectomeOutput/"
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

network_tstars = dict()
ts = np.logspace(-1,np.log10(4),num=200)

for network, temp in zip(networks, min_temps):
    Norms = np.zeros([sim_FCs[network].shape[-1],1],dtype=float)
    kstest = np.zeros([sim_FCs[network].shape[-1],1],dtype=float)
    MSEs = np.zeros([sim_FCs[network].shape[-1],1],dtype=float)
    network_tstars[network] = np.zeros([no_subject, 1],dtype=float)
    subIndex = 0
    for rhoIJ in subject_rhoIJ[network]:
        path = sim_FC_source + "SimFCs_and_distances/" + str(subIndex) + "/" + network + "/"
        makedir(sim_FC_source + "SimFCs_and_distances/")
        makedir(sim_FC_source + "SimFCs_and_distances/" + str(subIndex))
        makedir(sim_FC_source + "SimFCs_and_distances/" + str(subIndex) + "/" + network)
        for i in range(sim_FCs[network].shape[-1]):
            sim_FC = sim_FCs[network][..., i]
            diff = sim_FC - rhoIJ
            Norms[i] = np.linalg.norm(diff)
            kstest[i] = stats.ks_2samp(np.ravel(sim_FC), np.ravel(rhoIJ))[0]
            MSEs[i] = mean_squared_error(np.ravel(rhoIJ),np.ravel(sim_FC))

            if __name__ == "__main__":
                plt.imshow(sim_FC)
                plt.colorbar()
                plt.savefig(path + str(i) + "_simFC.png")
                plt.clf()


        if __name__ == "__main__":
            plt.scatter(ts, Norms)
            plt.title("Froebenius Norm")
            plt.semilogx()
            plt.xlim(0.1,4)
            plt.savefig(path + "distance.png")
            plt.clf()
            plt.scatter(ts, kstest)
            plt.title("KS test")
            plt.semilogx()
            plt.xlim(0.1,4)
            plt.savefig(path + "kstest.png")
            plt.clf()
            plt.scatter(ts, MSEs)
            plt.title("Mean Squared Error")
            plt.semilogx()
            plt.xlim(0.1,4)
            plt.savefig(path + "MSEs.png")
            plt.clf()
            plt.imshow(rhoIJ)
            plt.colorbar()
            plt.savefig(path + "_rhoIJ.png")
            plt.clf()
            np.savetxt(path + "Norms.csv",Norms)
            np.savetxt(path + "Kstest.csv", kstest)
            np.savetxt(path + "MSEs.csv", MSEs)

        MSEPandas = pandas.Series(np.ravel(MSEs[range(temp,200)]))
        TsPandas = pandas.Series(ts[range(temp,200)])
        mseWindows = MSEPandas.rolling(5)
        tsWindows = TsPandas.rolling(5)
        mov_mean_norms = mseWindows.mean()
        mov_mean_temps = tsWindows.mean()
        newMSE = np.asarray(mov_mean_norms.tolist())
        newTemps = np.asarray(mov_mean_temps.tolist())
        newMSE = newMSE[~np.isnan(newMSE)]
        newTemps = newTemps[~np.isnan(newTemps)]


        if __name__ == "__main__":
            plt.scatter(newTemps, newMSE)
            plt.xlabel("Temperatures")
            plt.ylabel("MSE")
            plt.title("Smooth MSE: Subject " + str(subIndex + 1))
            plt.semilogx()
            plt.savefig(path + "SmoothMSE.png")
            plt.clf()


        network_tstars[network][subIndex] = to_find_critical_temperature(-newMSE, newTemps)
        subIndex += 1
















