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

def percent_diff(df,n,states,network):

    diff_list = []

    for state in states:
        state_subset = df[df['state'] == state]

        taken_set = state_subset[state_subset['task'] == 'yes']
        rest_set = state_subset[state_subset['task'] == 'no']

        d_phi = np.array(taken_set.correlation) - np.array(rest_set.correlation)
        norm = (np.array(taken_set.correlation) + np.array(rest_set.correlation)) / 2

        percent_diff = 100 * d_phi / norm

        diff_list.append(percent_diff)

    state_labeler = ['Awake'] * n + ['Mild'] * n + ['Deep'] * n + ['Recovery'] * n

    network_labeler = [network] * len(state_labeler)

    return_array_diff = np.hstack(diff_list).tolist()

    return_array = np.array([return_array_diff, state_labeler, network_labeler])

    return return_array

main_path = '/Users/npopiel/Documents/empirical_phi/subject_level/correlation/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis']#, 'Baseline']

network_names = ['Auditory', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Frontoparietal', 'Retrosplenial', 'SM Hand',
                 'SM Mouth', 'Visual']#, 'Random']

states = ['Awake', 'Mild', 'Deep', 'Recovery']

df = pd.read_csv(main_path+'tot_corr_abs.csv')



diff_lst = []

groups = ['higher','sensory']

for network in networks:

    n = 17

    df_net = df[df.network == network]

    diff_lst.append(percent_diff(df_net,n,states,network=network))

array_diff = np.hstack(diff_lst)

dict = {}

labels = ['percent_diff', 'state', 'group']

for ind, name in enumerate(labels):
    dict[name] = array_diff[ind]

df_diff = pd.DataFrame(dict)

df_diff["percent_diff"] = pd.to_numeric(df_diff["percent_diff"])


df_diff.rename(columns={'percent_diff':'percent_diff','state':'Sedation Level','group':'network'},inplace=True)


sns.set(style="whitegrid", palette="pastel", color_codes=True)

sns.set_context('paper')

plt.close()
plt.figure(figsize=(16,12))

ax = sns.catplot(
    data=df_diff,
    x='network',
    y='percent_diff',
    hue='Sedation Level',
    kind='bar',
    aspect=3,
    height=3,
    margin_titles=False,
    alpha=0.6,
    legend_out=False)

ax.row_names = []

ax.axes.flat[0].set_xlabel('Network', fontsize=16)

#ax.axes.flat[0].annotate('A',xy=(-0.4,0.145),fontsize=12,fontweight='bold')


title = r'$\rho_{\%}$ modulated by Sedation Level'

ax.axes.flat[0].set_title(title, usetex=True, fontsize=14)
ax.axes.flat[0].set_ylabel(r'$\rho_{\%}$   ', usetex=True, fontsize=18, rotation=0)
# axes.set_xlabel('Network', fontsize=20)
ax.axes.flat[0].set_xticklabels(network_names)
#ax.axes.flat[0].set_xticklabels(ax.axes.flat[0].get_xticklabels(), rotation=45, horizontalalignment='right')
ax.axes.flat[0].legend(loc='upper right')
plt.tight_layout()

plt.savefig(main_path+'fig_diff_new_corr.pdf')

