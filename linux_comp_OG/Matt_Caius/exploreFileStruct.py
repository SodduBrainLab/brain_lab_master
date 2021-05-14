import numpy as np

input_path = "D:/OneDrive/School/Research/ConnectomeData/random_j/random_j/"

filename = input_path + "0_meanPhi.npz"

file = np.load(filename)

for entry in file:
    for thing in file[entry]:
        for something in file[entry][thing]:
            print(something)