import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib

matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *


def percent_diff(df,n,states,network):


    diff_list = []

    for state in states:
        state_subset = df[df['state'] == state]

        taken_set = state_subset[state_subset['task'] == 'yes']
        rest_set = state_subset[state_subset['task'] == 'no']

        d_phi = np.array(taken_set.phi) - np.array(rest_set.phi)
        norm = (np.array(taken_set.phi) + np.array(rest_set.phi)) / 2

        percent_diff = 100 * d_phi / norm

        diff_list.append(percent_diff)

    state_labeler = ['Awake'] * n + ['Mild'] * n + ['Deep'] * n + ['Recovery'] * n

    network_labeler = [network] * len(state_labeler)

    return_array_diff = np.hstack(diff_list).tolist()

    return_array = np.array([return_array_diff, state_labeler, network_labeler])

    return return_array


main_path = '/Users/npopiel/Documents/empirical_phi/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis', 'Baseline']

network_names = ['Auditory', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Frontoparietal', 'Retrosplenial', 'SM Hand',
                 'SM Mouth', 'Visual', 'Random']



states = ['Awake', 'Mild', 'Deep', 'Recovery']

df = pd.read_csv(main_path+'tot_phi.csv')


labels = ['percent_diff', 'state', 'network']

diff_lst = []

for network in networks:

    n = 100 if network == 'Baseline' else 17

    df_net = df[df.network == network]

    diff_lst.append(percent_diff(df_net,n,states,network))

array_diff = np.hstack(diff_lst)

dict = {}

for ind, name in enumerate(labels):
    dict[name] = array_diff[ind]

df_diff = pd.DataFrame(dict)

df_diff["percent_diff"] = pd.to_numeric(df_diff["percent_diff"])

df.rename(columns={'percent_diff':'percent_diff','state':'Sedation Level','network':'network'},inplace=True)


sns.set(style="whitegrid", palette="pastel", color_codes=True)

sns.set_context('paper')

plt.close()
plt.figure(figsize=(16,12))

ax = sns.catplot(
    data=df_diff,
    x='network',
    y='percent_diff',
    hue='state',
    kind='bar',
    aspect=3,
    height=3,
    margin_titles=False,
    alpha=0.6,
    legend_out=False)

ax.row_names = []

ax.axes.flat[0].set_xlabel('Network', fontsize=16)

#ax.axes.flat[0].annotate('A',xy=(-0.4,0.145),fontsize=12,fontweight='bold')


title = r'$\Phi_{\%}$ modulated by Sedation Level'

ax.axes.flat[0].set_title(title, usetex=True, fontsize=14)
ax.axes.flat[0].set_ylabel(r'$\Phi_{\%}$   ', usetex=True, fontsize=18, rotation=0)
# axes.set_xlabel('Network', fontsize=20)
ax.axes.flat[0].set_xticklabels(network_names)
#ax.axes.flat[0].set_xticklabels(ax.axes.flat[0].get_xticklabels(), rotation=45, horizontalalignment='right')
ax.axes.flat[0].legend(loc='upper right')
plt.tight_layout()

plt.savefig(main_path+'fig_diff_net.pdf')



