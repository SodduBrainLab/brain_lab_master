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

network_names = ['Higher Rest', 'Higher Taken', 'Sensory Rest','Sensory Taken']



states = ['Awake', 'Mild', 'Deep', 'Recovery']

df = pd.read_csv(main_path+'grouped_delta_phi.csv')
df2 = pd.read_csv(main_path+'grouped_mean_phi.csv')

df.state = df.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
df2.state = df2.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)


df['ratio'] = np.array(df.delta_phi)/np.array(df2.avg_phi)

df.rename(columns={'ratio':'ratio','delta_phi':'delta_phi','task':'task','state':'Sedation Level','group':'group','combined':'combined'},inplace=True)
df2.rename(columns={'avg_phi':'avg_phi','task':'task','state':'Sedation Level','group':'group','combined':'combined'},inplace=True)

sns.set(style="whitegrid", palette="pastel", color_codes=True)

sns.set_context('paper')

plt.close()
plt.figure(figsize=(16,12))

ax = sns.catplot(
    data=df,
    x='combined',
    y='ratio',
    hue='Sedation Level',
    kind='bar',
    aspect=3,
    height=3,
    margin_titles=False,
    alpha=0.6,
    legend_out=False)

ax.row_names = []

ax.axes.flat[0].set_xlabel('', fontsize=16)

#ax.axes.flat[0].annotate('A',xy=(-0.4,0.145),fontsize=12,fontweight='bold')


title = r'$\frac{\Delta \Phi}{\langle \Phi \rangle}$ modulated by Sedation Level'

ax.axes.flat[0].set_title(title, usetex=True, fontsize=14)
ax.axes.flat[0].set_ylabel(r'$\frac{\Delta \Phi}{\langle \Phi \rangle}$   ', usetex=True, fontsize=18, rotation=0)
# axes.set_xlabel('Network', fontsize=20)
#ax.axes.flat[0].set_xticklabels(network_names)
#ax.axes.flat[0].set_xticklabels(ax.axes.flat[0].get_xticklabels(), rotation=45, horizontalalignment='right')
ax.axes.flat[0].legend(loc='upper left',fontsize=6)
plt.tight_layout()

plt.savefig(main_path+'fig_ratio.pdf')



'''

for state in states:

    title = 'Phi by Network in '+ state +' Sedation Level'

    df_subset = df[df['state']==state]

    plt.figure(figsize=(16,9))

    ax = sns.barplot(x="network", y="phi", hue=index, edgecolor='0.6', data=df_subset)
    ax.set_ylabel('Phi', fontsize=20)
    ax.set_xlabel('Network', fontsize=20)
    ax.set_title(title,fontsize=24)

    ax.set_xticklabels(network_names)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    leg = ax.get_legend()
    new_title = 'Task'
    leg.set_title(new_title)
    new_labels = ['Rest', 'Taken']
    for t, l in zip(leg.texts, new_labels): t.set_text(l)
    plt.savefig(save_path+'barplot/'+state+'.pdf')
    #plt.show()
    plt.close()

'''