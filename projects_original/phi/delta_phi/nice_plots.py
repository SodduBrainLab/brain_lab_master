import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib

matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *

main_path = '/Users/npopiel/Documents/empirical_phi/Grouped Averages/stats/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis', 'Baseline']

network_names = ['Higher Rest', 'Higher Taken', 'Sensory Rest','Sensory Taken']



states = ['Awake', 'Mild', 'Deep', 'Recovery']

df = pd.read_csv(main_path+'grouped_tot_avg_phi_wide.csv')

df.state = df.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)

print(df.groupby(['group','state','task']).mean())

df.rename(columns={'avg_phi':'delta_phi','task':'task','state':'Sedation Level','group':'group','combined':'combined'},inplace=True)

sns.set(style="whitegrid", palette="pastel", color_codes=True)

sns.set_context('paper')

plt.close()
plt.figure(figsize=(16,12))

ax = sns.catplot(
    data=df,
    x='combined',
    y='delta_phi',
    hue='Sedation Level',
    kind='violin',
    aspect=3,
    height=3,
    margin_titles=False,
    alpha=0.6,
    legend_out=False)

ax.row_names = []

ax.axes.flat[0].set_xlabel('Group and Task', fontsize=16)

#ax.axes.flat[0].annotate('B',xy=(-0.4,0.705),fontsize=12,fontweight='bold')


title = r'$\langle \Phi \rangle$ modulated by Sedation Level'

ax.axes.flat[0].set_title(title, usetex=True, fontsize=14)
ax.axes.flat[0].set_ylabel(r'$\langle \Phi \rangle$   ', usetex=True, fontsize=18, rotation=0)
# axes.set_xlabel('Network', fontsize=20)
ax.axes.flat[0].set_xticklabels(network_names)
#ax.axes.flat[0].set_xticklabels(ax.axes.flat[0].get_xticklabels(), rotation=45, horizontalalignment='right')
ax.axes.flat[0].legend(loc='upper left')
plt.tight_layout()

plt.savefig(main_path+'fig.pdf')



