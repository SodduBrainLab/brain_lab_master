import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib

matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *

main_path = '/Users/npopiel/Documents/empirical_phi/delta_phi/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis', 'Baseline']

network_names = ['Auditory', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Frontoparietal', 'Retrosplenial', 'SM Hand',
                 'SM Mouth', 'Visual', 'Random']



states = ['Awake', 'Mild', 'Deep', 'Recovery']

df = pd.read_csv(main_path+'delta_phi.csv')

new_df = df[df.task == 'yes']
new_df.drop(columns=['mean','std','task'])

delta_taken = np.array(df[df.task == 'yes']['std'])
delta_rest = np.array(df[df.task == 'no']['std'])

ratio = delta_taken / delta_rest

new_df['delta_taken'] = delta_taken
new_df['delta_rest'] = delta_rest

new_df['delta_taken_over_rest'] = ratio

new_df['avg_rest'] = np.array(df[df.task == 'no']['mean'])
new_df['avg_taken'] = np.array(df[df.task == 'yes']['mean'])

new_df['diff'] = delta_taken-delta_rest
new_df['percent_diff'] = 100 * (delta_taken-delta_rest)/((delta_taken+delta_rest)/2)

sns.set(style="whitegrid", palette="pastel", color_codes=True)

sns.set_context('paper')

plt.figure(figsize=(16,12))

sns.catplot(
    data=new_df,
    x='network',
    y='percent_diff',
    palette='Set1',
    kind='bar',
    hue='state',
    aspect=3,
    height=3,
    margin_titles=False,
    alpha=0.6)



plt.savefig(main_path+'fig_ratio.pdf')

'''

ax.row_names = []

#ax.axes.flat[0].set_ylabel(r'$\Phi$', fontsize=20)
ax.axes.flat[1].set_xlabel('Network', fontsize=20)

ax.axes.flat[0].annotate('A',xy=(-0.4,0.82),fontsize=12,fontweight='bold')
ax.axes.flat[1].annotate('B',xy=(-0.4,0.82),fontsize=12,fontweight='bold')

titles = [r'$\Phi$ modulated by Sedation Level (Rest)',r'$\Phi$ modulated by Sedation Level (Taken)']
for ind, axes in enumerate(ax.axes.flat):
    axes.set_title(titles[ind],usetex=True,fontsize=14)
    axes.set_ylabel(r'$\Phi$  ', usetex=True, fontsize=20, rotation=0)
    #axes.set_xlabel('Network', fontsize=20)
    axes.set_xticklabels(network_names)
    axes.set_xticklabels(axes.get_xticklabels(), rotation=45, horizontalalignment='right')

plt.tight_layout()
#plt.suptitle(r'$\Phi$ as a function of sedation level for RSN by Task')

plt.savefig(main_path+'fig_diff.pdf')



'''