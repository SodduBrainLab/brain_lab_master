import numpy as np
import scipy.stats as ss
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests
import pandas as pd
from statsmodels.stats.multicomp import (pairwise_tukeyhsd,
                                         MultiComparison)
#import matplotlib.pyplot as plt

from projects.phi.tools.utils import *

main_path = '/Users/npopiel/Documents/empirical_phi/'

data_path = main_path + 'tot_phi.csv'

df = pd.read_csv(data_path)

df_baseline = df[df.network == 'Baseline']

states = ['Awake','Mild','Deep','Recovery']
networks = ['Aud','DMN','Dorsal','Ventral','Cingulo','Fronto','Retro','SMhand','SMmouth','Vis']#,'Baseline']

list_p_vals_uncor = []

for network in networks:

    test_df = pd.concat((df[df.network == network],df_baseline))
    #print('Network:', network)
    model = ols('phi ~ C(network)+ C(task) + C(state) +  C(network):C(task) + C(network):C(state) + C(task):C(state) + C(network):C(task):C(state)', data=test_df).fit()
    anova_table = sm.stats.anova_lm(model, typ=3)
    list_p_vals_uncor.append(anova_table['PR(>F)'])
    #print(anova_table)

    # I have now gotten the anova results for all of the interactions
    # Now I need to correct the p values and then run Tukey tests

significance_levels = [0.05,0.001]
num_for_correct = 11
sig_val = 0.05
list_sig_interactions = []
for series in list_p_vals_uncor:
    copy = series.copy()
    copy.reindex(np.arange(len(copy)))
    for ind,p in enumerate(series):
        if p < sig_val/num_for_correct:
            copy[ind] = True
        else:
            copy[ind] = False
    list_sig_interactions.append(copy)


#print(list_sig_interactions)

comparisons = [(),('network',),('task',),('state',),('network','task'),('network','state'),('task','state'),('network','task','state'),()]

for ind,network in enumerate(networks):

    significant_data = np.multiply(list_sig_interactions[ind].astype('int8').tolist(), comparisons)

    test_df = pd.concat((df[df.network == network],df_baseline))
    '''
    for dat in significant_data:
        if len(dat) == 1:
            # DO t-test
            test_df[dat[0]]
            t,p = ss.ttest_ind()
        elif len(dat) == 2:
            # DO correct multiple comparison
            x=4
        elif len(dat)==3:
            # Do three way main effect?
            y=3
    '''
    print(network)
    task_comp = MultiComparison(test_df['phi'],
                                test_df['task'])
    print('Task')
    print(task_comp.tukeyhsd().summary())
    print(task_comp.allpairtest(ss.ttest_ind, method='Holm')[0])
    net_comp = MultiComparison(test_df['phi'],
                                test_df['network'])
    print('Network')
    print(net_comp.tukeyhsd().summary())
    print(net_comp.allpairtest(ss.ttest_ind, method='Holm')[0])
    state_comp = MultiComparison(test_df['phi'],
                                test_df['state'])
    print('State')
    print(state_comp.tukeyhsd().summary())
    print(state_comp.allpairtest(ss.ttest_ind, method='Holm')[0])
