import numpy as np
import pyinform
from projects.phi.tools.utils import *

def binarize_tc(time_series):
    avgs = np.mean(time_series, axis=0)

    time_series_other = np.copy(time_series)
    for i in range(len(avgs)):
        time_series[np.where(time_series_other[:, i] >= avgs[i]), i] = 1
        time_series[np.where(time_series_other[:, i] < avgs[i]), i] = 0

    time_series = time_series.astype(np.int)

    markov_chain = time_series.tolist()
    return markov_chain


states = ['Awake','Mild','Deep','Recovery']
networks = ['Aud','DMN','Dorsal','Ventral','Cingulo','Fronto','Retro','SMhand','SMmouth','Vis','Baseline']

path = '/Users/npopiel/Documents/empirical_phi/time_series/'

ts_name = 'ts_all.npy'

for network in networks:
    for state in states:

        ts_all = np.squeeze(load_matrix(path+state+'/'+network+'/'+ts_name))

        num_sub = ts_all.shape[0]

        binary_tc = np.array([binarize_tc(ts_all[i,...]) for i in range(num_sub) ])


        active_info_list = []

        for sub in range(num_sub):
            active_info = pyinform.activeinfo.active_info(binary_tc[sub],k=2)
            active_info_list.append(active_info)

        print(ts_all.shape)