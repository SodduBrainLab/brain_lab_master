from linux_comp_OG.projects.generalize_ising_model.tools.utils import *
from linux_comp_OG.projects.phi.tools.utils import *
from linux_comp_OG.Matt_Caius.CalculateFunc_Conn import network_tstars
from scipy.stats import wilcoxon

networks = ["Aud","CO","CP","DMN","Dorsal","FP","RS","SMHand","SMMouth","Ventral","Visual"]
min_temps = [53,52,52,65,56,47,57,93,59,43,84]
no_runs = 200
median_tstars = list()
stddev_tstars = list()
pval_tstars = list()
phi_max_list = list()

for network, min_temp in zip(networks, min_temps):

    temp_range = range(min_temp, 200)
    meanPhiList = list()
    phiSusList = list()
    inputPath = "D:/OneDrive/School/Research/ConnectomeOutput/" + network
    ts = np.logspace(-1, np.log10(4), num=200)

    for runNo in range(no_runs):
        file = inputPath + "/" + str(runNo + 1) + "/phi.csv"
        if file_exists(file):
            phi = np.loadtxt(file)
            meanPhiList.append(phi[0])
            phiSusList.append(phi[2])
        else:
            break

    ts = ts[temp_range]

    meanPhiList = np.asarray(meanPhiList)[temp_range]
    phiSusList = np.asarray(phiSusList)[temp_range]

    PhiMax = to_find_critical_temperature(meanPhiList, ts)
    tstars = network_tstars[network][:,0]

    median_tstars.append(np.median(tstars))
    stddev_tstars.append(np.std(tstars))
    pval_tstars.append(wilcoxon(tstars - PhiMax)[1])
    phi_max_list.append(PhiMax)

print(median_tstars)
print(stddev_tstars)
print(phi_max_list)
print(pval_tstars)
