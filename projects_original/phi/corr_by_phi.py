import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib

matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *

main_path = '/Users/npopiel/Documents/empirical_phi/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis', 'Baseline']

network_names = ['Auditory', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Frontoparietal', 'Retrosplenial', 'SM Hand',
                 'SM Mouth', 'Visual', 'Random']



states = ['Awake', 'Mild', 'Deep', 'Recovery']

df = pd.read_csv(main_path+'tot_phi.csv')

df_corr = pd.read_csv(main_path+'tot_corr_abs.csv')

df['mod'] = np.array(df_corr.correlation)/np.array(df.phi)

df.rename(columns={'phi':'phi','task':'task','state':'Sedation Level','network':'network','mod':'mod'},inplace=True)

sns.set(style="whitegrid", palette="pastel", color_codes=True)

sns.set_context('paper')

plt.figure(figsize=(16,12))

ax = sns.catplot(
    data=df,
    x='network',
    y='mod',
    palette='Set1',
    hue='Sedation Level',
    kind='bar',
    row='task',
    aspect=3,
    height=3,
    margin_titles=False,
    alpha=0.6)

ax.row_names = []

#ax.axes.flat[0].set_ylabel(r'$\Phi$', fontsize=20)
ax.axes.flat[1].set_xlabel('Network', fontsize=20)

#ax.axes.flat[0].annotate('A',xy=(-0.4,0.82),fontsize=12,fontweight='bold')
#ax.axes.flat[1].annotate('B',xy=(-0.4,0.82),fontsize=12,fontweight='bold')

titles = [r'$\frac{\rho}{\Phi}$ modulated by Sedation Level (Rest)',r'$\frac{\rho}{\Phi}$ modulated by Sedation Level (Taken)']
for ind, axes in enumerate(ax.axes.flat):
    axes.set_title(titles[ind],usetex=True,fontsize=14)
    axes.set_ylabel(r'$\frac{\rho}{\Phi}$  ', usetex=True, fontsize=20, rotation=0)
    #axes.set_xlabel('Network', fontsize=20)
    axes.set_xticklabels(network_names)
    axes.set_xticklabels(axes.get_xticklabels(), rotation=45, horizontalalignment='right')

plt.tight_layout()
#plt.suptitle(r'$\Phi$ as a function of sedation level for RSN by Task')

plt.savefig(main_path+'fig_corr_over_phi.pdf')


