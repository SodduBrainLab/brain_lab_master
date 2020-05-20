import matplotlib.pyplot as plt
from projects.generalize_ising_model.tools.utils import to_normalize, makedir
from projects.phi.tools.utils import load_matrix

networks = ["Aud","CO","CP","DMN","Dorsal","FP","RS","SMHand","SMMouth","Ventral","Visual"]

outputPath = "/home/brainlab/Desktop/Matt/ConnectomeOutput/Jij Heatmaps"

makedir(outputPath)

fig, axs = plt.subplots(3,4)

count = 0

for ax in axs.flat:

    if count >= len(networks):
        break

    network = networks[count]
    input_path = '/home/brainlab/Desktop/Matt/ConnectomeData/HCP_Average/' + network + "/Jij_avg.csv"

    J = to_normalize(load_matrix(input_path))

    index = networks.index(network)

    heatmap = ax.imshow(J)
    ax.set_title(network)

    count += 1

fig.delaxes(axs[2,3])
plt.tight_layout()

plt.savefig("/home/brainlab/Desktop/Matt/ConnectomeOutput/Figures/Jij_Heatmaps.png", dpi = 1000)
plt.show()
