import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from projects.generalize_ising_model.core import generalized_ising
from linux_comp_OG.projects.generalize_ising_model.tools.utils import *
from linux_comp_OG.projects.phi.tools.utils import *
from linux_comp_OG.Matt_Caius.CalculateFunc_Conn import network_tstars

matplotlib.rcParams.update({'font.size': 15})

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
    ts_orig = np.logspace(-1, np.log10(4), num=200)
    bounds = ts_orig[[49, 199]]

    specificHeat = np.genfromtxt(inputPath + "/heat.csv")
    CritTemp = to_find_critical_temperature(specificHeat[temp_range], ts_orig[temp_range])
    makedir(inputPath)

    for runNo in range(no_runs):
        file = inputPath + "/" + str(runNo + 1) + "/phi.csv"
        if file_exists(file):
            phi = np.loadtxt(file)
            meanPhiList.append(phi[0])
            phiSusList.append(phi[2])
        else:
            break


    ts = ts_orig[temp_range]

    tstar = np.mean(network_tstars[network])
    tstar_std = np.std(network_tstars[network])
    Q1 = np.quantile(network_tstars[network], 0.25)
    Q2 = np.quantile(network_tstars[network], 0.75)
    print(network, Q1, Q2, tstar)
    print(network_tstars[network].transpose())
    ind_tstar = np.abs(ts - tstar).argmin()

    meanPhiList_trunc = np.asarray(meanPhiList)[temp_range]
    phiSusList_trunc = np.asarray(phiSusList)[temp_range]

    PhiMax = to_find_critical_temperature(meanPhiList_trunc, ts)
    PhiSusMax = to_find_critical_temperature(phiSusList_trunc, ts)

    phiplot.scatter(ts_orig, meanPhiList)
    phiplot.axvline(CritTemp, color='k')
    phiplot.axvline(PhiMax, color='b')
    phiplot.axvline(tstar, color='g')
    if not network == 'Ventral':
        phiplot.axvspan(Q1, Q2, alpha=0.25, color='g')
    phiplot.set(xlabel="Temperature", ylabel='Phi', xlim=bounds)
    phiplot.set_title(str(network))
    phiplot.semilogx()

    susplot.scatter(ts_orig, phiSusList)
    susplot.axvline(CritTemp, color='k')
    susplot.axvline(PhiSusMax, color='r')
    susplot.axvline(tstar, color='g')
    if not network == 'Ventral':
        susplot.axvspan(Q1, Q2, alpha=0.25, color='g')
    susplot.set(xlabel='Temperature', ylabel='Susceptibility of Phi', xlim=bounds,
               ylim=[-min(phiSusList), max(phiSusList) * 1.10])
    susplot.set_title(network)
    susplot.semilogx()
    susplot.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    heatplot.scatter(ts_orig, specificHeat)
    heatplot.axvline(CritTemp, color='k')
    heatplot.set(xlabel="Temperature", ylabel='Specific Heat', xlim=bounds)
    heatplot.set_title(str(network))
    heatplot.semilogx()


phiFig.delaxes(phiplots[-1,-1])
phiSusFig.delaxes(susplots[-1,-1])
specHeatFig.delaxes(heatplots[-1,-1])

Phi = plt.arrow(0,0, 3,1, head_width=0.2, color='b', length_includes_head=True)
Tstar = plt.arrow(0,0, 1,3, head_width=0.2, color='g', length_includes_head=True)
Critical = plt.arrow(0,0, 4,4, head_width=0.2, color='k', length_includes_head=True)
PhiSus = plt.arrow(0,0, 4,4, head_width=0.2, color='r', length_includes_head=True)

phiFig.legend([Phi, Tstar, Critical], ['Maximum Phi', 'T*', 'Critical Temperature'],loc = "lower right",fontsize = 'medium')
phiSusFig.legend([PhiSus, Tstar, Critical], ['Maximum Susceptibility of Phi', 'T*', 'Critical Temperature'],loc = "lower right",fontsize = 'medium')
specHeatFig.legend([Critical], ['Critical Temperature'],loc = "lower right",fontsize = 'medium')

phiFig.tight_layout()
phiSusFig.tight_layout()
specHeatFig.tight_layout()
phiFig.savefig(outputPath + "/" + "AllNetworkPhi.png")
phiSusFig.savefig(outputPath + "/" + "AllNetworkPhiSus.png")
specHeatFig.savefig(outputPath + "/" + "AllNetworkSpecHeat.png")