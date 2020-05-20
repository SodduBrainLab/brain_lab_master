import matplotlib.pyplot as plt
import numpy as np
from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import *
from projects.phi.tools.utils import *
from Matt_Caius.CalculateFunctionalConnectivity import network_tstars

def GenFig(network,no_runs = 200):

    meanPhiList = list()
    phiSusList = list()
    inputPath = "/home/brainlab/Desktop/Matt/ConnectomeOutput/" + network
    outputPath = "/home/brainlab/Desktop/Matt/ConnectomeOutput/Figures"
    makedir(outputPath)
    ts = np.logspace(-1,np.log10(4),num=200)

    CritTemp = np.genfromtxt(inputPath + "/ctem.csv")


    makedir(inputPath)

    for runNo in range(no_runs):
        file = inputPath + "/" + str(runNo + 1) + "/phi.csv"
        if file_exists(file):
            phi = np.loadtxt(file)
            meanPhiList.append(phi[0])
            phiSusList.append(phi[2])
        else:
            break

    meanPhiList = np.asarray(meanPhiList)
    phiSusList = np.asarray(phiSusList)


    PhiMax = to_find_critical_temperature(meanPhiList,ts)
    PhiSusMax = to_find_critical_temperature(phiSusList,ts)
    tstar = np.mean(network_tstars[network])

    fig, axs = plt.subplots(2)

    axs[0].scatter(ts, meanPhiList)
    axs[0].set_title("Mean and Susceptibility of Phi By Temperature for %s" % network)
    axs[0].axvline(CritTemp, color='k')
    axs[0].axvline(PhiMax, color='b')
    axs[0].axvline(PhiSusMax, color='r')
    axs[0].axvline(tstar, color='g')
    axs[0].set(ylabel='Phi')

    axs[1].scatter(ts, phiSusList)
    plt.ylim(-0.000001, max(phiSusList)*1.10)
    plt.axvline(CritTemp, color='k')
    axs[1].axvline(CritTemp, color='k')
    axs[1].axvline(PhiMax, color='b')
    axs[1].axvline(PhiSusMax, color='r')
    axs[1].axvline(tstar, color='g')
    axs[1].set(xlabel='Temperature', ylabel='Susceptibility of Phi')

    plt.tight_layout()

    plt.savefig(outputPath + "/" + network + ".png")


networks = ["Aud","CO","CP","DMN","Dorsal","FP","RS","SMHand","SMMouth","Ventral","Visual"]

for network in networks:
    GenFig(network)