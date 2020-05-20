from projects.generalize_ising_model.tools.utils import find_dimensionality
from projects.phi.tools.utils import load_matrix
import numpy as np
import matplotlib.pyplot as plt
import os
import string
from scipy import stats

time_series_Path = "/home/brainlab/Desktop/Matt/preprocessing"
sim_FC_source = "/home/brainlab/Desktop/Matt/ConnectomeOutput/"
no_subject = 20

networks = [
    "CP",
    "Ventral",
    "DMN",
    "Aud",
    "CO",
    "Dorsal",
    "SMHand",
    "Visual",
    "SMMouth",
    "FP",
    "RS"
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
        i += 1

network_tstars = dict()
ts = np.logspace(-1,np.log10(4),num=200)

for network in networks:
    ksResults = np.zeros([sim_FCs[network].shape[-1],1],dtype=float)
    network_tstars[network] = np.zeros([no_subject, 1],dtype=float)
    subIndex = 0
    for rhoIJ in subject_rhoIJ[network]:
        for i in range(sim_FCs[network].shape[-1]):
            sim_FC = sim_FCs[network][..., i]
            ksResults[i] = stats.ks_2samp(np.ravel(sim_FC), np.ravel(rhoIJ))[0]
        network_tstars[network][subIndex] = ts[np.where(ksResults == np.min(ksResults))[0]][0]
        subIndex += 1














