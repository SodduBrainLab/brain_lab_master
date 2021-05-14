from projects.generalize_ising_model.tools.utils import to_normalize, makedir
from projects.phi.tools.utils import load_matrix
import numpy as np
import pickle

networks = ["Aud","CO","CP","DMN","Dorsal","FP","RS","SMHand","SMMouth","Ventral","Visual"]
eigenvalues_dict = dict()
eigenvectors_dict = dict()
final = dict()


for network in networks:
    input_path = 'D:/OneDrive/School/Research/ConnectomeData/HCP_Average/' + network + "/Jij_avg.csv"
    J = load_matrix(input_path)

    eigenvalues, eigenvectors = np.linalg.eig(J)

    eigenvalues_dict[network] = eigenvalues
    eigenvectors_dict[network] = eigenvectors

final["values"] = eigenvalues_dict
final["vectors"] = eigenvectors_dict

file = open("D:/OneDrive/School/Research/ConnectomeOutput/eigen.pkl","wb")
pickle.dump(final, file)
file.close()


file_open = open("D:/OneDrive/School/Research/ConnectomeOutput/eigen.pkl","rb")

newfinal = pickle.load(file_open)
print(newfinal)


