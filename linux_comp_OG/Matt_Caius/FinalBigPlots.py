import numpy as np
from projects.generalize_ising_model.core import generalized_ising
from linux_comp_OG.projects.generalize_ising_model.tools.utils import *
from linux_comp_OG.projects.phi.tools.utils import *
from linux_comp_OG.Matt_Caius.CalculateTstar2 import tstars

outputPath = "D:/OneDrive/School/Research/ConnectomeOutput/FiguresNew"
networks = ["Aud", "CO", "CP", "DMN", "Dorsal", "FP", "RS", "SMHand", "SMMouth", "Ventral", "Visual"]
min_temps = [53,52,52,65,56,47,57,93,59,43,84]
no_runs = 200