import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib

matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *

main_path = '/Users/npopiel/Documents/empirical_phi/concat/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis']#, 'Baseline']

network_names = ['Higher Order', 'Sensory']

states = ['Awake', 'Mild', 'Deep', 'Recovery']

delta_phi_higher_order = pd.read_csv(main_path+'std_corr_higher_order.csv',)
delta_phi_higher_order.state =  delta_phi_higher_order.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
delta_phi_higher_order.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','correlation':'Average Phi'},inplace=True)
delta_phi_higher_order['group'] = ['higher']*delta_phi_higher_order['Average Phi'].count()

avg_phi_higher_order = pd.read_csv(main_path+'mean_corr_higher_order.csv',)
avg_phi_higher_order.state =  avg_phi_higher_order.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
avg_phi_higher_order.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','correlation':'Average Phi'},inplace=True)
avg_phi_higher_order['group'] = ['higher']*avg_phi_higher_order['Average Phi'].count()

delta_phi_sensory = pd.read_csv(main_path+'std_corr_sensory.csv',)
delta_phi_sensory.state =  delta_phi_sensory.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
delta_phi_sensory.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','correlation':'Average Phi'},inplace=True)
delta_phi_sensory['group'] = ['sensory']*delta_phi_sensory['Average Phi'].count()

avg_phi_sensory = pd.read_csv(main_path+'mean_corr_sensory.csv',)
avg_phi_sensory.state =  avg_phi_sensory.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
avg_phi_sensory.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','correlation':'Average Phi'},inplace=True)
avg_phi_sensory['group'] = ['sensory']*avg_phi_sensory['Average Phi'].count()

df_avg = pd.concat([avg_phi_sensory,avg_phi_higher_order])
df_delta = pd.concat([delta_phi_sensory,delta_phi_higher_order])

avg_taken = df_avg[df_delta.task == 'yes']
avg_rest = df_avg[df_delta.task == 'no']

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
d_phi_higher = [100*d_phi_awake_higher/norm_awake_higher,
                100*d_phi_mild_higher/norm_mild_higher,
                100*d_phi_deep_higher/norm_deep_higher,
                100*d_phi_recovery_higher/norm_recovery_higher]

state_labeler = ['Awake']*len(d_phi_awake_higher) + ['Mild']*len(d_phi_mild_higher) + ['Deep']*len(d_phi_deep_higher) + ['Recovery']*len(d_phi_recovery_higher)

network_labeler = ['higher'] * len(state_labeler)

d_phi_higher_stack = np.hstack(d_phi_higher).tolist()

return_array_higher = np.array([d_phi_higher_stack, state_labeler, network_labeler])



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
d_phi_sensory = [100*d_phi_awake_sensory/norm_awake_sensory,
                100*d_phi_mild_sensory/norm_mild_sensory,
                100*d_phi_deep_sensory/norm_deep_sensory,
                100*d_phi_recovery_sensory/norm_recovery_sensory]

state_labeler = ['Awake']*len(d_phi_awake_higher) + ['Mild']*len(d_phi_mild_higher) + ['Deep']*len(d_phi_deep_higher) + ['Recovery']*len(d_phi_recovery_higher)

network_labeler = ['sensory'] * len(state_labeler)

d_phi_sensory_stack = np.hstack(d_phi_sensory).tolist()

return_array_sensory = np.array([d_phi_sensory_stack, state_labeler, network_labeler])

labels = ['d_phi', 'state', 'group']

dict_higher, dict_sensory = {}, {}

for ind, name in enumerate(labels):
    dict_higher[name] = return_array_higher[ind]
    dict_sensory[name] = return_array_sensory[ind]

df_higher = pd.DataFrame(dict_higher)
df_sensory = pd.DataFrame(dict_sensory)

df = pd.concat([df_higher,df_sensory])

df["d_phi"] = pd.to_numeric(df["d_phi"])




sns.set(style="whitegrid", palette="pastel", color_codes=True)

sns.set_context('paper')

plt.close()
plt.figure(figsize=(16,12))

ax = sns.catplot(
    data=df,
    x='group',
    y='d_phi',
    hue='state',
    kind='bar',
    aspect=3,
    height=3,
    margin_titles=False,
    alpha=0.6,
    legend_out=False)

ax.row_names = []

ax.axes.flat[0].set_xlabel('Group', fontsize=16)

#ax.axes.flat[0].annotate('A',xy=(-0.4,0.145),fontsize=12,fontweight='bold')


title = r'$\rho_{\%}$ modulated by Sedation Level'

ax.axes.flat[0].set_title(title, usetex=True, fontsize=14)
ax.axes.flat[0].set_ylabel(r'$\rho_{\%}$   ', usetex=True, fontsize=18, rotation=0)
# axes.set_xlabel('Network', fontsize=20)
ax.axes.flat[0].set_xticklabels(network_names)
#ax.axes.flat[0].set_xticklabels(ax.axes.flat[0].get_xticklabels(), rotation=45, horizontalalignment='right')
ax.axes.flat[0].legend(loc='upper right')
plt.tight_layout()

plt.savefig(main_path+'fig_diff_avg_corr.pdf')



