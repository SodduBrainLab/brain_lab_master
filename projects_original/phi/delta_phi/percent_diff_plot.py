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

delta_phi_higher_order = pd.read_csv(main_path+'std_phi_higher_order3.csv',)
delta_phi_higher_order.state =  delta_phi_higher_order.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
delta_phi_higher_order.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Delta Phi'},inplace=True)
delta_phi_higher_order['group'] = ['higher']*delta_phi_higher_order['Delta Phi'].count()

avg_phi_higher_order = pd.read_csv(main_path+'mean_phi_higher_order3.csv',)
avg_phi_higher_order.state =  avg_phi_higher_order.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
avg_phi_higher_order.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Average Phi'},inplace=True)
avg_phi_higher_order['group'] = ['higher']*avg_phi_higher_order['Average Phi'].count()

delta_phi_sensory = pd.read_csv(main_path+'std_phi_sensory.csv',)
delta_phi_sensory.state =  delta_phi_sensory.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
delta_phi_sensory.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Delta Phi'},inplace=True)
delta_phi_sensory['group'] = ['sensory']*delta_phi_sensory['Delta Phi'].count()

avg_phi_sensory = pd.read_csv(main_path+'mean_phi_sensory.csv',)
avg_phi_sensory.state =  avg_phi_sensory.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
avg_phi_sensory.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Average Phi'},inplace=True)
avg_phi_sensory['group'] = ['sensory']*avg_phi_sensory['Average Phi'].count()

df_avg = pd.concat([avg_phi_sensory,avg_phi_higher_order])
df_delta = pd.concat([delta_phi_sensory,delta_phi_higher_order])

avg_taken = df_avg[df_avg.task == 'yes']
avg_rest = df_avg[df_avg.task == 'no']

avg_t_awake = avg_taken[avg_taken['Sedation Level'] == 'Awake']
avg_t_mild = avg_taken[avg_taken['Sedation Level'] == 'Mild']
avg_t_deep = avg_taken[avg_taken['Sedation Level'] == 'Deep']
avg_t_recovery = avg_taken[avg_taken['Sedation Level'] == 'Recovery']

avg_r_awake = avg_rest[avg_rest['Sedation Level'] == 'Awake']
avg_r_mild = avg_rest[avg_rest['Sedation Level'] == 'Mild']
avg_r_deep = avg_rest[avg_rest['Sedation Level'] == 'Deep']
avg_r_recovery = avg_rest[avg_rest['Sedation Level'] == 'Recovery']

d_phi_awake_higher = np.array(avg_t_awake[avg_t_awake.group == 'higher']['Average Phi'])\
                     - np.array(avg_r_awake[avg_r_awake.group == 'higher']['Average Phi'])
norm_awake_higher = (np.array(avg_t_awake[avg_t_awake.group == 'higher']['Average Phi'])\
                     + np.array(avg_r_awake[avg_r_awake.group == 'higher']['Average Phi']))/2
d_phi_mild_higher = np.array(avg_t_mild[avg_t_mild.group == 'higher']['Average Phi'])\
                     - np.array(avg_r_mild[avg_r_mild.group == 'higher']['Average Phi'])
norm_mild_higher = (np.array(avg_t_mild[avg_t_mild.group == 'higher']['Average Phi'])\
                     + np.array(avg_r_mild[avg_r_mild.group == 'higher']['Average Phi']))/2
d_phi_deep_higher = np.array(avg_t_deep[avg_t_deep.group == 'higher']['Average Phi'])\
                     - np.array(avg_r_deep[avg_r_deep.group == 'higher']['Average Phi'])
norm_deep_higher = (np.array(avg_t_deep[avg_t_deep.group == 'higher']['Average Phi'])\
                     + np.array(avg_r_deep[avg_r_deep.group == 'higher']['Average Phi']))/2
d_phi_recovery_higher = np.array(avg_t_recovery[avg_t_recovery.group == 'higher']['Average Phi'])\
                     - np.array(avg_r_recovery[avg_r_recovery.group == 'higher']['Average Phi'])
norm_recovery_higher = (np.array(avg_t_recovery[avg_t_recovery.group == 'higher']['Average Phi'])\
                     + np.array(avg_r_recovery[avg_r_recovery.group == 'higher']['Average Phi']))/2
d_phi_higher = [d_phi_awake_higher/norm_awake_higher,
                d_phi_mild_higher/norm_mild_higher,
                d_phi_deep_higher/norm_deep_higher,
                d_phi_recovery_higher/norm_recovery_higher]

d_phi_awake_sensory = np.array(avg_t_awake[avg_t_awake.group == 'sensory']['Average Phi'])\
                     - np.array(avg_r_awake[avg_r_awake.group == 'sensory']['Average Phi'])
norm_awake_sensory = (np.array(avg_t_awake[avg_t_awake.group == 'sensory']['Average Phi'])\
                     + np.array(avg_r_awake[avg_r_awake.group == 'sensory']['Average Phi']))/2
d_phi_mild_sensory = np.array(avg_t_mild[avg_t_mild.group == 'sensory']['Average Phi'])\
                     - np.array(avg_r_mild[avg_r_mild.group == 'sensory']['Average Phi'])
norm_mild_sensory = (np.array(avg_t_mild[avg_t_mild.group == 'sensory']['Average Phi'])\
                     + np.array(avg_r_mild[avg_r_mild.group == 'sensory']['Average Phi']))/2
d_phi_deep_sensory = np.array(avg_t_deep[avg_t_deep.group == 'sensory']['Average Phi'])\
                     - np.array(avg_r_deep[avg_r_deep.group == 'sensory']['Average Phi'])
norm_deep_sensory = (np.array(avg_t_deep[avg_t_deep.group == 'sensory']['Average Phi'])\
                     + np.array(avg_r_deep[avg_r_deep.group == 'sensory']['Average Phi']))/2
d_phi_recovery_sensory = np.array(avg_t_recovery[avg_t_recovery.group == 'sensory']['Average Phi'])\
                     - np.array(avg_r_recovery[avg_r_recovery.group == 'sensory']['Average Phi'])
norm_recovery_sensory = (np.array(avg_t_recovery[avg_t_recovery.group == 'sensory']['Average Phi'])\
                     + np.array(avg_r_recovery[avg_r_recovery.group == 'sensory']['Average Phi']))/2
d_phi_sensory = [d_phi_awake_sensory/norm_awake_sensory,
                d_phi_mild_sensory/norm_mild_sensory,
                d_phi_deep_sensory/norm_deep_sensory,
                d_phi_recovery_sensory/norm_recovery_sensory]



new_df = df_avg[df_avg.task == 'yes']
new_df.drop(columns=['Average Phi','std','task'])

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

plt.close()
plt.figure(figsize=(16,12))

ax = sns.catplot(
    data=df,
    x='combined',
    y='delta_phi',
    hue='Sedation Level',
    kind='bar',
    aspect=3,
    height=3,
    margin_titles=False,
    alpha=0.6,
    legend_out=False)

ax.row_names = []

ax.axes.flat[0].set_xlabel('Group and Task', fontsize=16)

ax.axes.flat[0].annotate('A',xy=(-0.4,0.145),fontsize=12,fontweight='bold')


title = r'$\Delta \Phi$ modulated by Sedation Level'

ax.axes.flat[0].set_title(title, usetex=True, fontsize=14)
ax.axes.flat[0].set_ylabel(r'$\Delta \Phi$   ', usetex=True, fontsize=18, rotation=0)
# axes.set_xlabel('Network', fontsize=20)
ax.axes.flat[0].set_xticklabels(network_names)
#ax.axes.flat[0].set_xticklabels(ax.axes.flat[0].get_xticklabels(), rotation=45, horizontalalignment='right')
ax.axes.flat[0].legend(loc='upper right')
plt.tight_layout()

plt.savefig(main_path+'fig.pdf')



