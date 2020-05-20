from projects.phi.tools.utils import *
import os
import numpy as np

def empirical_ts_concat(time_series,path_output,all=False):
    import numpy as np

    b = path_output

    array_list = []


    for i in range(len(time_series)):

        if all is False:

            new_ts = np.delete(np.asarray(time_series), i,axis=0)

            allArrays = np.empty((0, 5))

            for k in range(new_ts.shape[0]):
                myArray = np.squeeze(new_ts[k])
                allArrays = np.append(allArrays, myArray, axis=0)

            array_list.append(allArrays)

        if all is True:
            new_ts = np.array(time_series)

            allArrays = np.empty((0, 5))

            for k in range(new_ts.shape[0]):
                myArray = np.squeeze(new_ts[k])
                allArrays = np.append(allArrays, myArray, axis=0)
            array_list.append(allArrays)


    return array_list

main_path = '/home/user/Desktop/data_phi/Propofol/Baseline/'

ts_name = 'ts_all.csv'

number_regions = 5
brain_states = ['Awake','Deep','Mild','Recovery']
                # ['Recovery']


for state in brain_states:

    test_path = main_path + state + '/' + ts_name

    big_ts = load_matrix(test_path)
    array_list = permutation_ts(big_ts,'')
    save_path = '/home/user/Desktop/data_phi/time_series/' + state + '/Baseline'
    makedir2(save_path)
    np.save(save_path+'/ts_all',array_list)