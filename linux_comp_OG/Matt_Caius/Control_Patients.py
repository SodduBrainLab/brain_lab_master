import os
import csv
import numpy as np
from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import *
from projects.phi.tools.utils import *
import time

dataPath = "/home/brainlab/Desktop/Matt/ConnectomeData/Subjects"
outputPath = "/home/brainlab/Desktop/Matt/ConnectomeData/Results"

makedir(outputPath)

networks = [
    "Aud",
    "CinguloOperc",
    "CinguloParietal",
    "DMN",
    "Dorsal",
    "FrontoParietal",
    "Retrosplenial",
    "SMhand",
    "SMmouth",
    "Ventral",
    "Visual"
]

no_subjects = 20
count = 0

for network in networks:
    makedir(outputPath + "/" + network)
    for subNo in range(1, no_subjects+1):

        filepath = dataPath + "/" + "sub" + str(subNo) + "/" + network + "/Jij.csv"
        output = outputPath + "/" + network + "/" + str(subNo)

        J = to_normalize(load_matrix(filepath))

        if not os.path.exists(output):
            os.mkdir(output)



