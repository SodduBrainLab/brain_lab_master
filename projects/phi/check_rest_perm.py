'''

pseudocode

read in timecourse

    for j in range 100:
    for i in range 1000

        permute timecourse by swapping one row for another row

        (saving the seed so same permutations can be done)

    save new timecourse

    calculate SbyS matrix from new timecourse

    convert sbys to sbyn

    run phi
'''

import numpy as np
import pyphi

from brain_lab_master.projects.phi.tools.utils import *


def swap_rows(timeseries):

    if timeseries.shape[1]>timeseries.shape[0]:
        timeseries = timeseries.T

    len_ts = timeseries.shape[0]

    rand_num1 = np.random.randint(len_ts + 1)
    rand_num2 = np.random.randint(len_ts + 1)

    timeseries[[rand_num1, rand_num2],:] = timeseries[[rand_num2, rand_num1],:]

    return timeseries


default_delimiter = ','
format = '%1.5f'

main_path = '/Users/npopiel2/Desktop/permutation_phi/'

ts_path = main_path + 'ts_Default_parcellation_5_Sub1.csv'

ts = np.squeeze(load_matrix(ts_path))

num_phi = 10

num_perm = 1000

len_ts = ts.shape[0]

for i in range(num_phi):

    timeseries = np.copy(ts)

    new_path = main_path + 'perm' + str(i+1) + '/'

    makedir2(new_path)

    for j in range(num_perm):

        timeseries = swap_rows(np.copy(timeseries))

    np.savetxt(new_path + 'permuted_ts'+ str(i+1)+ '.csv',timeseries,delimeter = default_delimeter,fmt=format)

    tpm, state_total, frequency = main_tpm_branch(timeseries)

    # Normalizing respect to rows
    for div in range(len(state_total)):
        if state_total[div] != 0.0:
            tpm[div, :] /= state_total[div]

    np.savetxt(new_path + 'tpm'+ str(i+1)+ '.csv',tpm,delimeter = default_delimeter,fmt=format)
    np.savetxt(new_path + 'frequency'+ str(i+1)+ '.csv',frequency,delimeter = default_delimeter,fmt=format)

    fpm = pyphi.convert.to_2dimensional(pyphi.convert.state_by_state2state_by_node(tpm))

    mean_phi, phi_sum = to_calculate_mean_phi(fpm,fequency)

    np.savetxt(new_path + 'phi'+ str(i+1)+ '.csv',mean_phi,delimeter = default_delimeter,fmt=format)
    np.savetxt(new_path + 'phiSum' + str(i + 1) + '.csv', phi_sum, delimeter=default_delimeter, fmt=format)













