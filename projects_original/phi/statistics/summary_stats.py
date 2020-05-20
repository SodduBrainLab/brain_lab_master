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
#networks = ['Aud','DMN','Dorsal','Ventral','Cingulo','Fronto','Retro','SMhand','SMmouth','Vis']#,'Baseline']

networks = ['Aud','DMN','Dorsal','Ventral','Cingulo','Fronto','Retro','SMhand','SMmouth','Vis','Baseline']

arrays = [['Awake', 'Awake', 'Mild', 'Mild', 'Deep', 'Deep', 'Recovery', 'Recovery'],
          [   'no',   'yes',   'no',  'yes',   'no',  'yes',       'no',      'yes']]

tuples = list(zip(*arrays))

index = pd.MultiIndex.from_tuples(tuples, names=['state', 'task'])

test_df = pd.DataFrame(df.groupby(by=['network','task','state']).mean()).unstack().unstack()
t1 =  pd.DataFrame(df.groupby(by=['network','task','state']).mean()).unstack()

test_df2 = pd.DataFrame(df[df.network=='Aud'].groupby(by=['task','state']).mean()).unstack()

#df2 = pd.DataFrame(df.phi,index=networks,columns=index)
print(t1.to_latex())

#print(test_df.to_latex())


