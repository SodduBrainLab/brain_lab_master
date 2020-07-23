import matplotlib.pyplot as plt
import numpy as np
from projects.generalize_ising_model.core import generalized_ising
from linux_comp_OG.projects.generalize_ising_model.tools.utils import *
from linux_comp_OG.projects.phi.tools.utils import *
from linux_comp_OG.Matt_Caius.CalculateTstar2 import tstars

outputPath = "D:/OneDrive/School/Research/ConnectomeOutput/FiguresNew"
networks = ["Aud", "CO", "CP", "DMN", "Dorsal", "FP", "RS", "SMHand", "SMMouth", "Ventral", "Visual"]
min_temps = [53,52,52,65,56,47,57,93,59,43,84]
no_runs = 200

phiFig, phiplots = plt.subplots(3, 4, figsize=(20,10))
phiSusFig, susplots = plt.subplots(3, 4, figsize=(20,10))
specHeatFig, heatplots = plt.subplots(3, 4, figsize=(20,10))

for network, min_temp, phiplot, susplot, heatplot in zip(networks, min_temps, phiplots.flat, susplots.flat, heatplots.flat):

    temp_range = range(min_temp, 200)

    meanPhiList = list()
    phiSusList = list()
    inputPath = "D:/OneDrive/School/Research/ConnectomeOutput/" + network

    makedir(outputPath)
    ts = np.logspace(-1, np.log10(4), num=200)
    bounds = ts[[49, 199]]

    specificHeat = np.genfromtxt(inputPath + "/heat.csv")[temp_range]
    CritTemp = to_find_critical_temperature(specificHeat, ts[temp_range])
    makedir(inputPath)

    for runNo in range(no_runs):
        file = inputPath + "/" + str(runNo + 1) + "/phi.csv"
        if file_exists(file):
            phi = np.loadtxt(file)
            meanPhiList.append(phi[0])
            phiSusList.append(phi[2])
        else:
            break

    tstar = np.mean(tstars[network])
    ind_tstar = np.abs(ts - tstar).argmin()
    print(network, ind_tstar)
    print(tstar)

    ts = ts[temp_range]

    meanPhiList = np.asarray(meanPhiList)[temp_range]
    phiSusList = np.asarray(phiSusList)[temp_range]

    PhiMax = to_find_critical_temperature(meanPhiList, ts)
    PhiSusMax = to_find_critical_temperature(phiSusList, ts)

    phiplot.scatter(ts, meanPhiList)
    phiplot.axvline(CritTemp, color='k')
    phiplot.axvline(PhiMax, color='b')
    phiplot.axvline(PhiSusMax, color='r')
    phiplot.axvline(tstar, color='g')
    phiplot.set(xlabel="Temperature", ylabel='Phi', xlim=bounds)
    phiplot.set_title(str(network))
    phiplot.semilogx()

    susplot.scatter(ts, phiSusList)
    susplot.axvline(CritTemp, color='k')
    susplot.axvline(CritTemp, color='k')
    susplot.axvline(PhiMax, color='b')
    susplot.axvline(PhiSusMax, color='r')
    susplot.axvline(tstar, color='g')
    susplot.set(xlabel='Temperature', ylabel='Susceptibility of Phi', xlim=bounds,
               ylim=[-min(phiSusList), max(phiSusList) * 1.10])
    susplot.set_title(network)
    susplot.semilogx()

    heatplot.scatter(ts, specificHeat)
    heatplot.axvline(CritTemp, color='k')
    heatplot.set(xlabel="Temperature", ylabel='Specific Heat', xlim=bounds)
    heatplot.set_title(str(network))
    heatplot.semilogx()


phiFig.delaxes(phiplots[-1,-1])
phiSusFig.delaxes(susplots[-1,-1])
specHeatFig.delaxes(heatplots[-1,-1])
phiFig.tight_layout()
phiSusFig.tight_layout()
specHeatFig.tight_layout()
phiFig.savefig(outputPath + "/" + "AllNetworkPhi.png")
phiSusFig.savefig(outputPath + "/" + "AllNetworkPhiSus.png")
specHeatFig.savefig(outputPath + "/" + "AllNetworkSpecHeat.png")