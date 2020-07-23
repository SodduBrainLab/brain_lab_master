from linux_comp_OG.projects.generalize_ising_model.tools.utils import find_dimensionality
from linux_comp_OG.projects.phi.tools.utils import load_matrix
import numpy as np
import matplotlib.pyplot as plt

inputPath = "D:/OneDrive/School/Research/ConnectomeOutput/"
outputPath = "D:/OneDrive/School/Research/ConnectomeOutput/"

networks = ["Aud", "CO", "CP", "DMN", "Dorsal", "FP", "RS", "SMHand", "SMMouth", "Ventral", "Visual"]
dimensionality = list()
JijSum = list()

for network in networks:
    networkPath = inputPath + network

    J = load_matrix(networkPath + "/J_ij.csv")
    TCrit = np.genfromtxt(networkPath + "/ctem.csv")
    sim_FC = np.load(networkPath + "/sim_fc.npy")

    ts = np.logspace(-1,np.log10(4),num=200)

    dimensionality.append(find_dimensionality(J,sim_FC,TCrit,ts))
    JijSum.append(sum(sum(J)))

print(JijSum)

plt.bar(networks,dimensionality)
plt.xlabel("Networks")
plt.ylabel("Dimensionality")
plt.title("Dimensionality of Average Jijs for Each Network")
foo, labels = plt.xticks()
plt.setp(labels, rotation=30, horizontalalignment='right')
plt.tight_layout()
plt.savefig("D:/OneDrive/School/Research/ConnectomeOutput/FiguresNew/dimensionality.png", dpi = 1000,)
np.savetxt("D:/OneDrive/School/Research/ConnectomeOutput/Dimensionality/dimensionality.csv", dimensionality)
plt.clf()

plt.bar(networks,JijSum)
plt.xlabel("Networks")
plt.ylabel("Sum")
plt.title("Sum of Average Jijs for Each Network")
foo, labels = plt.xticks()
plt.setp(labels, rotation=30, horizontalalignment='right')
plt.tight_layout()
plt.savefig("D:/OneDrive/School/Research/ConnectomeOutput/FiguresNew/JijSum.png", dpi = 1000)
np.savetxt("D:/OneDrive/School/Research/ConnectomeOutput/Dimensionality/JijSum.csv", JijSum)
plt.clf()




