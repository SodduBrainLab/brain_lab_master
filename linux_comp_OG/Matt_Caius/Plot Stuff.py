import matplotlib.pyplot as plt
import numpy as np
from projects.generalize_ising_model.core import generalized_ising
from linux_comp_OG.projects.generalize_ising_model.tools.utils import *
from linux_comp_OG.projects.phi.tools.utils import *
from linux_comp_OG.Matt_Caius.CalculateFunctionalConnectivity import sim_FCs, subject_rhoIJ
from linux_comp_OG.Matt_Caius.CalculateTstar2 import tstars, minMSEs
import scipy.stats as stats

outputPath = "D:/OneDrive/School/Research/ConnectomeOutput/FiguresNew"
maxPhis = list()
maxSusPhis = list()
phiRatio = list()

def GenFig(network,temp_range,no_runs = 200):

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

    ts = ts[temp_range]

    meanPhiList = np.asarray(meanPhiList)[temp_range]
    phiSusList = np.asarray(phiSusList)[temp_range]


    PhiMax = to_find_critical_temperature(meanPhiList,ts)
    maxPhiValue = meanPhiList[(ts-PhiMax).argmin()]
    maxPhis.append(maxPhiValue)
    PhiSusMax = to_find_critical_temperature(phiSusList,ts)
    maxSusValue = phiSusList[(PhiSusMax - ts).argmin()]
    maxSusPhis.append(maxSusValue)
    phiRatio.append(PhiMax/maxSusValue)

    fig1, axs = plt.subplots(3)

    axs[0].scatter(ts, meanPhiList)
    axs[0].axvline(CritTemp, color='k')
    axs[0].axvline(PhiMax, color='b')
    axs[0].axvline(PhiSusMax, color='r')
    axs[0].axvline(tstar, color='g')
    axs[0].set(xlabel = "Temperature", ylabel='Phi', xlim = bounds)
    axs[0].set_title("Phi vs Temperature")
    axs[0].semilogx()

    axs[1].scatter(ts, phiSusList)
    plt.axvline(CritTemp, color='k')
    axs[1].axvline(CritTemp, color='k')
    axs[1].axvline(PhiMax, color='b')
    axs[1].axvline(PhiSusMax, color='r')
    axs[1].axvline(tstar, color='g')
    axs[1].set(xlabel='Temperature', ylabel='Susceptibility of Phi', xlim = bounds, ylim = [-min(phiSusList),max(phiSusList)*1.10])
    axs[1].set_title("Susceptibility of Phi vs Temperature")
    axs[1].semilogx()

    axs[2].scatter(ts,specificHeat)
    axs[2].axvline(CritTemp, color='k')
    axs[2].set(xlabel='Temperature', ylabel='Specific Heat', xlim = bounds)
    axs[2].set_title("Specific Heat")
    axs[2].semilogx()

    plt.tight_layout()

    plt.savefig(outputPath + "/" + network + "_phi.png")
    plt.clf()


    """
    plt.hist(network_tstars[network], bins = 20, range=[0.1,4])
    plt.xlabel("T Star")
    plt.title("Distribution of Subject T Star values")
    plt.savefig(outputPath + "/" + network + "_tstars.png")
    plt.clf()
    """

    fig, axs = plt.subplots(1, 2)
    plt.suptitle(network)
    axs[0].imshow(np.mean(subject_rhoIJ[network], axis=0))
    axs[0].set_title("Rho IJ")
    axs[1].imshow(sim_FCs[network][..., ind_tstar])
    axs[1].set_title("Simulated FC at T*")
    plt.savefig(outputPath + "/" + network + "_func_connect.png")
    plt.tight_layout()
    plt.clf()

    return tstar, CritTemp


networks = ["Aud", "CO", "CP", "DMN", "Dorsal", "FP", "RS", "SMHand", "SMMouth", "Ventral", "Visual"]

min_temps = [53,52,52,65,56,47,57,93,59,43,84]
Tstars = list()
CritTemps = list()

for network, minTemp in zip(networks, min_temps):
    ts_range = range(minTemp, 200)
    tstar, crittemp = GenFig(network, ts_range)
    Tstars.append(tstar)
    CritTemps.append(crittemp)

dimensionality = np.genfromtxt("D:/OneDrive/School/Research/ConnectomeOutput/Dimensionality/dimensionality.csv")
sumJij = np.genfromtxt("D:/OneDrive/School/Research/ConnectomeOutput/Dimensionality/JijSum.csv")

def add_labels(labels,xs,ys):
    for x, y, label in zip(xs, ys, labels):
        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(10, 0),  # distance from text to points (x,y)
                     ha='right')  # horizontal alignment can be left, right or center

plt.close('all')
plt.scatter(dimensionality,Tstars)
plt.title("T* and Dimensionality")
add_labels(networks,dimensionality,Tstars)
plt.xlabel("Dimensionality")
plt.ylabel("Temperature")
plt.savefig(outputPath + "/" + "tstar_Dims.png")
plt.clf()
print(stats.pearsonr(np.asarray(dimensionality), np.asarray(Tstars)))

plt.close('all')
plt.scatter(dimensionality,CritTemps)
plt.title("Critical Temperature and Dimensionality")
add_labels(networks,dimensionality,CritTemps)
plt.xlabel("Dimensionality")
plt.ylabel("Temperature")
plt.savefig(outputPath + "/" + "Critical_Dims.png")
plt.clf()
print(stats.pearsonr(np.asarray(dimensionality), np.asarray(CritTemps)))

plt.scatter(sumJij,Tstars)
plt.title("T* vs. sum of the Jij")
add_labels(networks,sumJij,Tstars)
plt.xlabel("Sum of Jij")
plt.ylabel("Temperature")
plt.savefig(outputPath + "/" + "tstar_Jij.png")
plt.clf()
print(stats.pearsonr(np.asarray(sumJij), np.asarray(Tstars)))

plt.close('all')
plt.scatter(sumJij,CritTemps)
plt.title("Critical Temperature and sum of Jij")
add_labels(networks,sumJij,CritTemps)
plt.xlabel("Sum of Jij")
plt.ylabel("Temperature")
plt.savefig(outputPath + "/" + "Critical_Jij.png")
plt.clf()
print(stats.pearsonr(np.asarray(sumJij), np.asarray(CritTemps)))

plt.close('all')
plt.scatter(sumJij,maxPhis)
plt.title("Maximum phi and sum of Jij")
add_labels(networks,sumJij,maxPhis)
plt.xlabel("Sum of Jij")
plt.ylabel("Phi")
plt.yscale("log")
plt.savefig(outputPath + "/" + "Phi_Jij.png")
plt.clf()
print(stats.pearsonr(np.asarray(sumJij), np.asarray(maxPhis)))

plt.bar(networks,minMSEs)
plt.xlabel("Networks")
plt.ylabel("Mean Squared Error")
plt.title("Mean squared error at T* for each resting state network")
foo, labels = plt.xticks()
plt.setp(labels, rotation=30, horizontalalignment='right')
plt.tight_layout()
plt.savefig(outputPath + "/" + "minMSEs.png")
plt.clf()

plt.bar(networks, maxPhis)
plt.xlabel("Networks")
plt.ylabel("Phi")
plt.title("Maximum phi value by network")
plt.yscale("log")
foo, labels = plt.xticks()
plt.setp(labels, rotation=30, horizontalalignment='right')
plt.tight_layout()
plt.savefig(outputPath + "/" + "max_Phis.png")
plt.clf()

plt.bar(networks, maxSusPhis)
plt.xlabel("Networks")
plt.ylabel("Maximum Sus Phi")
plt.title("Maximum susceptibility of phi by network")
plt.yscale("log")
foo, labels = plt.xticks()
plt.setp(labels, rotation=30, horizontalalignment='right')
plt.tight_layout()
plt.savefig(outputPath + "/" + "max_sus_Phis.png")
plt.clf()

plt.bar(networks, phiRatio)
plt.xlabel("Networks")
plt.ylabel("Maximum Phi/ Maximum Susceptibility of Phi")
plt.yscale("log")
plt.title("Ratio between maximum phi and maximum susceptibility of phi")
foo, labels = plt.xticks()
plt.setp(labels, rotation=30, horizontalalignment='right')
plt.tight_layout()
plt.savefig(outputPath + "/" + "phi_ratios.png")
plt.clf()
