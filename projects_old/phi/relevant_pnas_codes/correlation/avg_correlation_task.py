import numpy as np
from projects.phi.tools.utils import *

default_delimiter = ','
format = '%1.5f'

path = '/home/user/Desktop/data_phi/'
main_path = '/home/user/Desktop/data_phi/time_series/task/'
ts_name = 'ts_all.npy'

brain_states = ['Awake','Deep','Mild','Recovery']

networks = ['Aud','DMN','Dorsal','Ventral','Cingulo','Fronto','Retro','SMhand','SMmouth','Vis','Baseline']

for network in networks:

    for state in brain_states:

        load_path = main_path + state + '/' + network + '/'

        big_ts = load_matrix(load_path + ts_name)

        # calculate the correlation

        corr_list,avg_corr_list,upper_cor = [] , [], []

        for i in range(big_ts.shape[0]):

            ts = big_ts[i]

            correlation = np.corrcoef(ts,rowvar=False)

            upper_correlation = np.triu(correlation,k=1)

            corr_list.append(correlation)

            upper_cor.append(upper_correlation)

            avg_corr_list.append(np.mean(np.abs(upper_correlation)))

        makedir2(path+'correlation/')

        makedir2(path+'correlation/'+'task/')

        makedir2(path+'correlation/'+'task/' +state +'/')

        makedir2(path +'correlation/'+'task/'+ state + '/' + network + '/')

        save_path = path +'correlation/'+'task/'+ state + '/' + network + '/'

        np.savetxt(save_path+'abs_corr.csv',avg_corr_list,delimiter=default_delimiter,fmt=format)

