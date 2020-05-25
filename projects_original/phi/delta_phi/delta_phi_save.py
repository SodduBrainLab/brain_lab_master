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

df = pd.read_csv(main_path+'tot_phi2.csv')

def check_list(key,list):
    if key in list:
        return True
    else:
        return False

# high_list, sensory_list, mid_list = [], [], []
# for ind in df.network:
#     high_list.append(check_list(df.network[ind], ['DMN', 'Dorsal', 'Ventral', 'Fronto']))
#     sensory_list.append(check_list(df.networ))




higher_order = df[[check_list(ind, ['DMN','Dorsal','Ventral','Fronto','Cingulo','Retro']) for ind in df.network]]
sensory = df[[check_list(ind, ['Aud','Vis']) for ind in df.network]] # SMhand','SMmouth',
mid = df[[check_list(ind, ['Cingulo','Retro']) for ind in df.network]]

means_higher_order = higher_order.groupby(['sub_num','state','task']).mean()
delta_higher_order = higher_order.groupby(['sub_num','state','task']).std()

means_higher_order.to_csv(main_path+'mean_phi_higher_order3.csv')
delta_higher_order.to_csv(main_path+'std_phi_higher_order3.csv')
'''
means_sensory = sensory.groupby(['sub_num','state','task']).mean()
delta_sensory = sensory.groupby(['sub_num','state','task']).std()

means_sensory.to_csv(main_path+'mean_phi_sensory2.csv')
delta_sensory.to_csv(main_path+'std_phi_sensory2.csv')

means_mid = mid.groupby(['sub_num','state','task']).mean()
delta_mid = mid.groupby(['sub_num','state','task']).std()

means_mid.to_csv(main_path+'mean_phi_mid.csv')
delta_mid.to_csv(main_path+'std_phi_mid.csv')
'''
'''

grouped_df = df.groupby(['sub_num','state','task'])

means = grouped_df.mean()
stds = grouped_df.std()

stds.to_csv(main_path+'std_phi.csv')
means.to_csv(main_path+'avg_phi.csv')


delta_phi = pd.read_csv(main_path+'std_phi.csv',)
delta_phi.state =  delta_phi.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
delta_phi.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Delta Phi'},inplace=True)


avg_phi = pd.read_csv(main_path+'avg_phi.csv',)
avg_phi.state =  avg_phi.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
avg_phi.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Average Phi'},inplace=True)

'''

delta_phi_higher_order = pd.read_csv(main_path+'std_phi_higher_order3.csv',)
delta_phi_higher_order.state =  delta_phi_higher_order.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
delta_phi_higher_order.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Delta Phi'},inplace=True)

avg_phi_higher_order = pd.read_csv(main_path+'mean_phi_higher_order3.csv',)
avg_phi_higher_order.state =  avg_phi_higher_order.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
avg_phi_higher_order.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Average Phi'},inplace=True)
'''
delta_phi_sensory = pd.read_csv(main_path+'std_phi_sensory2.csv',)
delta_phi_sensory.state =  delta_phi_sensory.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
delta_phi_sensory.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Delta Phi'},inplace=True)

avg_phi_sensory = pd.read_csv(main_path+'mean_phi_sensory2.csv',)
avg_phi_sensory.state =  avg_phi_sensory.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
avg_phi_sensory.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Average Phi'},inplace=True)

delta_phi_mid = pd.read_csv(main_path+'std_phi_mid.csv',)
delta_phi_mid.state =  delta_phi_mid.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
delta_phi_mid.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Delta Phi'},inplace=True)

avg_phi_mid = pd.read_csv(main_path+'mean_phi_mid.csv',)
avg_phi_mid.state =  avg_phi_mid.state.astype(dtype='category',categories=["Awake", "Mild", "Deep","Recovery"],ordered=True)
avg_phi_mid.rename(columns={'sub_num':'sub_num','task':'task','state':'Sedation Level','phi':'Average Phi'},inplace=True)
'''
avg_group = [avg_phi_higher_order]#,avg_phi_sensory,avg_phi_mid]
std_group = [delta_phi_higher_order]#,delta_phi_sensory,delta_phi_mid]

titles = ['(Higher Order)']#,'(Sensory)','(Other)']
save_exts = ['higher3']#,'sensory','other']

sns.set(style="whitegrid", palette="pastel", color_codes=True,font_scale=3)

sns.set_context('paper')

for ind, data in enumerate(std_group):

    plt.figure(figsize=(16,12))

    ax = sns.catplot(
        data=data,
        x = 'task',
        y='Delta Phi',
        hue='Sedation Level',
        aspect=3,
        height=3,
        kind='bar',
        margin_titles=False,
        legend_out=False,
        alpha=0.4)



    ax.axes.flat[0].set_xlabel('Task', fontsize=20)
    ax.axes.flat[0].set_title(r'$\Delta \Phi$ by Sedation Level and Task ' + titles[ind],usetex=True,fontsize=24)
    ax.axes.flat[0].set_ylabel(r'$\Delta \Phi$    ', usetex=True, fontsize=20, rotation=0)
    ax.axes.flat[0].set_xticklabels(['Rest','Taken'],fontsize=16)
    ax.axes.flat[0].legend(fontsize = 10,loc='upper left')
    plt.tight_layout()
    plt.savefig(main_path+'fig_delta3b_' + save_exts[ind] +'.pdf')


    plt.figure(figsize=(16,12))

    ax = sns.catplot(
        data=avg_group[ind],
        x = 'task',
        y='Average Phi',
        hue='Sedation Level',
        aspect=3,
        height=3,
        kind='bar',
        margin_titles=False,
        legend_out=False,
        alpha=0.4)

    ax.axes.flat[0].set_xlabel('Task', fontsize=20)
    ax.axes.flat[0].set_title(r'$\langle \Phi \rangle $ by Sedation Level and Task ' + titles[ind],usetex=True,fontsize=24)
    ax.axes.flat[0].set_ylabel(r'$\langle \Phi \rangle$    ', usetex=True, fontsize=20, rotation=0)
    ax.axes.flat[0].set_xticklabels(['Rest','Taken'],fontsize=16)
    ax.axes.flat[0].legend(fontsize = 10,loc='upper left')
    plt.tight_layout()
    plt.savefig(main_path+'fig_avg3b_' + save_exts[ind] +'.pdf')
