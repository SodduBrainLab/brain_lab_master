import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib

matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *


def corr_load_organize(path, states, n, network):

    state_labeler, corr_list = [], []

    for state in states:

        state_path = path + state + '/' + network + '/'

        corr = np.squeeze(load_matrix(state_path + 'abs_corr.csv'))

        state_labeler += [state] * n

        #state_labeler_list.append(state_labeler)
        corr_list.append(corr)

    network_labeler = [network] * len(state_labeler)

    return_array_phi = np.squeeze(np.array(corr_list, dtype='float')).flatten('F').tolist()

    return_array = np.array([return_array_phi, state_labeler, network_labeler])

    return return_array


main_path = '/home/user/Desktop/data_phi/correlation/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis', 'Baseline']

network_names = ['Auditory', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Frontoparietal', 'Retrosplenial', 'SM Hand',
                 'SM Mouth', 'Visual', 'Baseline']

states = ['Awake', 'Mild', 'Deep', 'Recovery']
state_pos = np.arange(len(states))

labels = ['correlation', 'state', 'network']

corr_net_rest, corr_net_task = [], []

for network in networks:

    if network == 'Baseline':

        n = 100


    else:
        n = 17


    corr_rest = corr_load_organize(main_path, states, n, network)
    corr_task = corr_load_organize(main_path+'task/', states, n, network)

    corr_net_rest.append(corr_rest)
    corr_net_task.append(corr_task)

corr_array_rest = np.hstack(corr_net_rest)
corr_array_task = np.hstack(corr_net_task)


dict_rest, dict_task = {}, {}

for ind, name in enumerate(labels):
    dict_rest[name] = corr_array_rest[ind]
    dict_task[name] = corr_array_task[ind]

df_rest = pd.DataFrame(dict_rest)
df_task = pd.DataFrame(dict_task)

df_rest['task'] = ['no'] * df_rest['correlation'].count()
df_task['task'] = ['yes'] * df_rest['correlation'].count()

df = pd.concat([df_rest, df_task])

df["correlation"] = pd.to_numeric(df["correlation"])

save_path = '/home/user/Desktop/plots_phi_paper/'

df.to_csv(save_path + 'tot_corr_abs.csv', index=False)

