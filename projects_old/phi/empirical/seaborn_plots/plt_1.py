import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib
matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *

def phi_load_organize(path,n,network):

    if network == 'Baseline':
        phi_by_state = []

        for state in states:
            phi = []
            for i in range(n):

                op_path = path + state + '/phi/'

                phi.append(load_matrix(op_path + 'phi_'+str(i)+'.csv'))

            phi_by_state.append(phi)

        phi_array_base = np.squeeze(np.array(phi_by_state,dtype='float')).T

        state_labeler = ['Awake'] * n + ['Mild'] * n + ['Deep'] * n + ['Recovery'] * n

        network_labeler = [network] * len(state_labeler)

        return_array_phi = phi_array_base.flatten('F').tolist()

        return_array = np.array([return_array_phi,state_labeler,network_labeler])

    else:

        phi_list = []

        for i in range(n):

            file_path_open = path + 'phi_' + str(i) + '.csv'

            phi_list.append(load_matrix(file_path_open))

        state_labeler = ['Awake'] * n + ['Mild'] * n + ['Deep'] * n + ['Recovery'] * n

        network_labeler = [network] * len(state_labeler)

        return_array_phi = np.squeeze(np.array(phi_list,dtype='float')).flatten('F').tolist()

        return_array = np.array([return_array_phi,state_labeler,network_labeler])

    return return_array


main_path = '/home/user/Desktop/data_phi/phi/'

networks = ['Aud','DMN','Dorsal','Ventral','Cingulo','Fronto','Retro','SMhand','SMmouth','Vis','Baseline']

network_names = ['Auditory','DMN','Dorsal','Ventral','Cingulo','Frontoparietal','Retrosplenial','SM Hand','SM Mouth','Visual','Baseline']

baseline_path_rest = '/home/user/Desktop/data_phi/Propofol/Baseline/'
baseline_path_task = '/home/user/Desktop/data_phi/Propofol/task/Baseline/'

states = ['Awake','Mild','Deep','Recovery']
state_pos = np.arange(len(states))

labels = ['phi','state','network']

phi_net_rest, phi_net_task = [],[]

for network in networks:

    if network == 'Baseline':

        open_path_rest = baseline_path_rest
        open_path_task = baseline_path_task

        n = 100

        phi_baseline_rest = phi_load_organize(open_path_rest, n, network)
        phi_baseline_task = phi_load_organize(open_path_task, n, network)
    else:
        open_path_rest = main_path + network + '/SbyS2/'
        open_path_task = main_path + network + '/SbyS/task/'

        n = 17

        phi_rest = phi_load_organize(open_path_rest, n, network)
        phi_task = phi_load_organize(open_path_task, n, network)

        phi_net_rest.append(phi_rest)
        phi_net_task.append(phi_task)

phi_array_rest = np.hstack(phi_net_rest)
phi_array_task = np.hstack(phi_net_task)

phi_net_array_rest = np.hstack([phi_array_rest,phi_baseline_rest])
phi_net_array_task = np.hstack([phi_array_task,phi_baseline_task])

dict_rest,dict_task = {},{}

for ind,name in enumerate(labels):

    dict_rest[name] = phi_net_array_rest[ind]
    dict_task[name] = phi_net_array_task[ind]

df_rest = pd.DataFrame(dict_rest)
df_task = pd.DataFrame(dict_task)


df_rest['task'] = ['no']*df_rest['phi'].count()
df_task['task'] = ['yes']*df_rest['phi'].count()


df = pd.concat([df_rest,df_task])

df["phi"] = pd.to_numeric(df["phi"])

sns.set(style="whitegrid", palette="pastel", color_codes=True)

save_path = '/home/user/Desktop/plots_phi_paper/'

df.to_csv(save_path+'tot_phi.csv',index=False)


'''
for ind,network in enumerate(networks):

    title = 'Phi in '+network_names[ind]+' Network'

    df_subset = df[df['network']==network]

    plt.figure(figsize=(16,9))

    ax = sns.violinplot(x='state', y='phi', hue='task',
                   split=True, inner='quart',
                   palette={'yes': 'y', 'no': 'b'},alpha=0.2,
                   data=df_subset)
    sns.despine(left=True)
    ax.set_ylabel('Phi', fontsize=20)
    ax.set_xlabel('Sedation Level', fontsize=20)

    ax.set_title(title,fontsize=24)
    leg = ax.get_legend()
    new_title = 'Task'
    leg.set_title(new_title)
    new_labels = ['Rest', 'Taken']
    for t, l in zip(leg.texts, new_labels): t.set_text(l)
    plt.savefig(save_path+'splitplot/'+network+'.pdf')
    plt.close()
    #plt.show()

    plt.figure(figsize=(16,9))
    ax2 = sns.swarmplot(x="state", y="phi", hue="task", palette='pastel',data=df_subset)
    ax2.set_ylabel('Phi', fontsize=20)
    ax2.set_xlabel('Sedation Level', fontsize=20)

    ax2.set_title(title,fontsize=24)
    leg = ax2.get_legend()
    new_title = 'Task'
    leg.set_title(new_title)
    new_labels = ['Rest', 'Taken']
    for t, l in zip(leg.texts, new_labels): t.set_text(l)
    plt.savefig(save_path+'swarmplot/'+network+'.pdf')
    plt.close()
    #plt.show()


for state in states:

    title = 'Phi by Network in '+ state +' Sedation Level'

    df_subset = df[df['state']==state]

    plt.figure(figsize=(16,9))

    ax = sns.barplot(x="network", y="phi", hue="task", edgecolor='0.6', data=df_subset)
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
tasks = ['no','yes']

'''
for state in states:

    for task in tasks:

        if task =='no':
            add_text = ' (Resting)'
        else:
            add_text = ' (Taken)'

        title = 'Phi by Network in '+ state +' Sedation Level' + add_text

        df_subset = df[df['state']==state]

        df_subset = df_subset[df_subset['task']==task]

        plt.figure(figsize=(16,9))

        ax = sns.violinplot(x="network", y="phi", data=df_subset)
        ax.set_ylabel('Phi', fontsize=20)
        ax.set_xlabel('Network', fontsize=20)
        ax.set_title(title,fontsize=24)

        ax.set_xticklabels(network_names)

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        plt.savefig((save_path+'violinplot/'+state+'_'+task+'.pdf'))
        #plt.show()
        plt.close()
    
for state in states:

    title = 'Phi by Task for Each Network in '+ state +' Sedation Level'

    df_subset = df[df['state']==state]

    plt.figure(figsize=(16,9))

    ax = sns.pointplot(x="task", y="phi", hue="network", data=df_subset);
    ax.set_ylabel('Phi', fontsize=20)
    ax.set_xlabel('Task', fontsize=20)
    ax.set_title(title,fontsize=24)

    ax.set_xticklabels(['Rest', 'Taken'])

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    leg = ax.get_legend()
    new_title = 'Network'
    leg.set_title(new_title)
    new_labels = network_names
    for t, l in zip(leg.texts, new_labels): t.set_text(l)
    plt.savefig(save_path+'pointplot/'+state+'.pdf')
    #plt.show()
    plt.close()

for ind,network in enumerate(networks):

    title = 'Phi in '+network_names[ind]+' Network'

    df_subset = df[df['network']==network]

    plt.figure(figsize=(16,9))
    ax = sns.pointplot(x='state', y='phi', hue='task', data=df_subset)
    ax.set_ylabel('Phi', fontsize=20)
    ax.set_xlabel('Sedation Level', fontsize=20)
    ax.set_title(title,fontsize=24)
    leg = ax.get_legend()
    new_title = 'Task'
    leg.set_title(new_title)
    new_labels = ['Rest', 'Taken']
    for t, l in zip(leg.texts, new_labels): t.set_text(l)
    plt.savefig(save_path+'pointplot/'+network+'.pdf')
    #plt.show()
    plt.close()
'''