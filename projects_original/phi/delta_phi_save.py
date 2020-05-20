import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib

matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *

def organize_df(df, states, n, network,task):

    state_labeler = []

    mean_state_task, std_state_task = [], []

    for state in states:
        phi_state = df[df.state == state]
        phi_net_state = phi_state[phi_state.network == network]

        phi_task_net_state = phi_net_state[phi_net_state.task == task]

        state_labeler += [state] * n

        mean_state_task.append(phi_task_net_state.mean())
        std_state_task.append(phi_task_net_state.std())

    network_labeler = [network] * len(state_labeler)

    return_array_mean_phi = np.squeeze(np.array(mean_state_task, dtype='float')).flatten('F').tolist()
    return_array_std_phi = np.squeeze(np.array(std_state_task, dtype='float')).flatten('F').tolist()

    return_array = np.array([return_array_mean_phi, return_array_std_phi, state_labeler, network_labeler])

    return return_array

main_path = '/Users/npopiel/Documents/empirical_phi/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis', 'Baseline']

network_names = ['Auditory', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Frontoparietal', 'Retrosplenial', 'SM Hand',
                 'SM Mouth', 'Visual', 'Random']

states = ['Awake', 'Mild', 'Deep', 'Recovery']

df = pd.read_csv(main_path+'tot_phi.csv')


list_rest, list_task = [], []

for network in networks:

    rest = organize_df(df,states,n=17,network=network,task='no')
    list_rest.append(rest)

    task = organize_df(df,states,17,network,'yes')
    list_task.append(task)

array_rest = np.hstack(list_rest)
array_task = np.hstack(list_task)

labels = ['mean', 'std', 'state', 'network']
#labels_std = ['std','state', 'network']

dict_rest, dict_task = {}, {}

for ind, name in enumerate(labels):

    dict_rest[name] = array_rest[ind]
    dict_task[name] = array_task[ind]

df_rest = pd.DataFrame(dict_rest)
df_task = pd.DataFrame(dict_task)

df_rest['task'] = ['no'] * df_rest['mean'].count()
df_task['task'] = ['yes'] * df_rest['mean'].count()

df2 = pd.concat([df_rest, df_task])

df2["mean"] = pd.to_numeric(df2["mean"])
df2["std"] = pd.to_numeric(df2["std"])

save_path = '/Users/npopiel/Documents/empirical_phi/delta_phi/'

df2.to_csv(save_path + 'delta_phi.csv', index=False)

