import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy.stats as ss
import matplotlib

matplotlib.rcParams.update({'font.size': 18})
from projects.phi.tools.utils import *

main_path = '/Users/npopiel/Documents/empirical_phi/subject_level/Phi/'

networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis']#, 'Baseline']

network_names = ['Auditory', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Frontoparietal', 'Retrosplenial', 'SM Hand',
                 'SM Mouth', 'Visual']#, 'Random']



states = ['Awake', 'Mild', 'Deep', 'Recovery']

df = pd.read_csv(main_path+'tot_phi2.csv')

def ttest_pairwise_df(df, tup1, tup2, params=('network', 'state', 'task'), var='phi'):
    # tup1 and tup2 are tuples of the relevant parmeter for comparison.
    # i.e. (network, state, task)
    # Possible network codings are:
    # networks = ['Aud', 'DMN', 'Dorsal', 'Ventral', 'Cingulo', 'Fronto', 'Retro', 'SMhand', 'SMmouth', 'Vis']
    # Possible state codings are:
    # states = ['Awake', 'Mild', 'Deep', 'Recovery']
    # And possible task codings are:
    # tasks = ['no', 'yes']
    # params are the default parameters of interest
    # var is the name of the column containing the numerical variable of interest (defaults to phi)

    net1, state1, task1 = tup1[0], tup1[1], tup1[2]
    net2, state2, task2 = tup2[0], tup2[1], tup2[2]

    df_net1 = df[df[params[0]] == net1]
    df_state1 = df_net1[df_net1[params[1]]==state1]
    df_task1 = df_state1[df_state1[params[2]]==task1]
    arr1 = np.array(df_task1[var])

    df_net2 = df[df[params[0]] == net2]
    df_state2 = df_net2[df_net2[params[1]] == state2]
    df_task2 = df_state2[df_state2[params[2]] == task2]
    arr2 = np.array(df_task2[var])

    t, p = ss.ttest_rel(arr1,arr2)

    return t, p

state_mat = np.outer(np.array(states,dtype='object'),np.array([1,1,1,1]))

ind1, ind2 = np.triu_indices(len(states),k=1)

tasks = ['no','yes']
'''
for task in tasks:
    makedir2(main_path+task+'/')
    for network in networks:
        net_list = []
        makedir2(main_path + task + '/'+network+'/')
        # Compare across conditions
        for s1, s2 in zip(ind1,ind2):
            t, p = ttest_pairwise_df(df,(network,states[s1],task),(network, states[s2], task))

            net_list.append((t,p,states[s1],states[s2]))


        np.savetxt(main_path + task + '/'+network+'/stats.csv',np.asarray(net_list),delimiter=',',fmt='%s')

'''

for network in networks:
    net_list = []
    makedir2(main_path + '/' + network + '/')
    # Compare across conditions
    for state in states:
        t, p = ttest_pairwise_df(df, (network, state, 'no'), (network, state, 'yes'))

        net_list.append((t, p, state, state))

    np.savetxt(main_path + '/' + network + '/stats.csv', np.asarray(net_list), delimiter=',', fmt='%s')
