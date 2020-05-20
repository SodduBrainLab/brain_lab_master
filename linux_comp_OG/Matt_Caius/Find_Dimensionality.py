from projects.generalize_ising_model.tools.utils import find_dimensionality
from projects.phi.tools.utils import load_matrix
import numpy as np
import matplotlib.pyplot as plt

inputPath = "/home/brainlab/Desktop/Matt/ConnectomeOutput/"
outputPath = "/home/brainlab/Desktop/Matt/ConnectomeOutput/"

networks = [
    "Dorsal",
    "Visual",
    "DMN",
    "RS",
    "FP",
    "Aud",
    "CO",
    "Ventral",
    "SMHand",
    "SMMouth"
]

dimensionality = list()

for network in networks:
    networkPath = inputPath + network

    J = load_matrix(networkPath + "/J_ij.csv")
    TCrit = np.genfromtxt(networkPath + "/ctem.csv")
    sim_FC = np.load(networkPath + "/sim_fc.npy")

    ts = np.logspace(-1,np.log10(4),num=200)

    dimensionality.append(find_dimensionality(J,sim_FC,TCrit,ts))

plt.bar(networks,dimensionality)
plt.xlabel("Networks")
plt.ylabel("Dimensionality")
plt.title("Dimensionality of Average Jijs for Each Network")
plt.xticks(rotation = "vertical")
plt.tight_layout()

plt.savefig("/home/brainlab/Desktop/Matt/ConnectomeOutput/Figures/dimensionality.png", dpi = 1000,)
plt.show()



