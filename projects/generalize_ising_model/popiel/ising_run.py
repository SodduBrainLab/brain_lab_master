import numpy as np
import time
import scipy
import os
from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import to_save_results

def load_matrix(file):

    extension = file.split('.')[-1]
    if str(extension) == 'csv':
        return np.genfromtxt(file,delimiter = ',')
    elif str(extension) == 'npy':
        return np.load(file)
    elif str(extension) == 'mat':
        return scipy.io.loadmat(file)
    elif str(extension) == 'npz':
        return np.load(file)

def makedir2(path):

    if not os.path.exists(path):
        os.mkdir(path)
        return True
    return True

def file_exists(filename):

    exists = os.path.isfile(filename)
    if exists:
        return True
    else:
        return False

def save_file(data,path,name):

    default_delimiter = ','
    format = '%1.5f'

    if isinstance(data,list):
        data = np.array(data)

    if len(data.shape) <= 2:
        file = path + str(name) + '.csv'

        if not file_exists(file):
            np.savetxt(file, np.asarray(data), delimiter=default_delimiter, fmt=format)
    else:
        file = path + str(name) + '.npy'
        if not file_exists(file):
            np.save(file,np.asarray([data]))


subject_list = ['Sub1',
                'Sub2',
                'Sub3',
                'Sub4',
                'Sub5',
                'Sub6',
                'Sub7',
                'Sub8',
                'Sub9',
                'Sub10',
                'Sub11',
                'Sub12',
                'Sub13',
                'Sub14',
                'Sub15',
                'Sub16',
                'Sub17',
                'Sub18',
                'Sub19',
                'Sub20',
                'Sub21',
                'Sub22',
                'Sub23',
                'Sub24',
                'Sub25']


parcels = ['AAL2','Parcellation']
main_path = '/home/brainlab/Desktop/Rudas/Data/DTI_st_joes/Average/'
temperature_params = [(0.0001,5,100),(0.0001,4,100)]
no_simulations = 4000
thermalize_time =0.3

for sub in subject_list:

    for ind, parcel in enumerate(parcels):

        save_path = main_path + 'Ising/' + sub + '/' + parcel + '/'

        if not file_exists(save_path+'plots.png'):

            makedir2(main_path + 'Ising/')
            makedir2(main_path + 'Ising/' + sub + '/')
            makedir2(save_path)

            J = np.squeeze(load_matrix(main_path + sub + '/' + parcel + '/Jij.csv'))

            # Ising Parameters
            temperature_parameters = temperature_params[ind]  # Temperature parameters (initial tempeture, final tempeture, number of steps)

            start_time = time.time()
            print('Fitting Generalized Ising model for ',sub,' with the ', parcel, ' parcellation scheme.')
            simulated_fc, critical_temperature, E, M, S, H = generalized_ising(J,
                                                                                temperature_parameters=temperature_parameters,
                                                                                n_time_points=no_simulations,
                                                                                thermalize_time=thermalize_time,)

            to_save_results(temperature_parameters, J, E, M, S, H, simulated_fc, critical_temperature, save_path,
                            temperature_distribution='linear')
            print('It took ', time.time() - start_time, 'seconds to fit the generalized ising model')

        else:
            print(save_path, 'DONE!')

