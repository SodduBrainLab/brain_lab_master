from linux_comp_OG.projects.generalize_ising_model.tools.utils import to_normalize
from linux_comp_OG.projects.phi.tools.utils import load_matrix
import matplotlib.pyplot as plt
import numpy as np

def make_plot(network,matrix,filename,minmax):

    plt.imshow(matrix, cmap=plt.cm.Blues, vmin = minmax[0],vmax = minmax[1])
    plt.title("Element wise standard deviation of the\nJijs for the " + str(network) + " network")
    for i in range(5):
        for j in range(5):
            c = np.round(matrix[j, i],4)
            plt.text(i, j, str(c), va='center', ha='center')

    plt.savefig("D:/OneDrive/School/Research/ConnectomeOutput/FiguresNew/" + filename)
    plt.clf()


input_path = "D:/OneDrive/School/Research/ConnectomeData/Ising_HCP/"

networks = ['Aud', 'CinguloOperc', 'CinguloParietal', 'DMN', 'Dorsal', 'FrontoParietal', 'Retrosplenial', 'SMhand', 'SMmouth', 'Ventral', 'Visual']

for counter, network in enumerate(networks):
    Jijs = np.zeros([20, 5, 5], dtype=float)
    Jijs_Normalized = np.zeros([20, 5, 5], dtype=float)
    path = input_path + network
    for sub in range(20):
        J = load_matrix(path + '/Jij_Sub' + str(sub+1) + '.csv')
        J_norm = to_normalize(J)
        Jijs[sub, :, :] = J
        Jijs_Normalized[sub, :, :] = J_norm
    sigmaIJ = np.std(Jijs, axis=0)
    make_plot(network,sigmaIJ,"sigmaIjs/"+network+"_sigmaIJ.png",minmax = [0,1000])
    sigmaIJ_norm = np.std(Jijs_Normalized, axis = 0)
    make_plot(network,sigmaIJ_norm,"sigmaIjs_normalized/"+network+"_sigmaIJ.png",minmax=[0,1])