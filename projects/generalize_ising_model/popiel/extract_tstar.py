import numpy as np
import time
import scipy.stats
import os
from projects.generalize_ising_model.core2 import generalized_ising
from projects.generalize_ising_model.tools.utils import to_save_results
import matplotlib.pyplot as plt
import seaborn as sns

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
    elif str(extension) == 'txt':
        return np.loadtxt(file)
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

def find_tstar_fro(mat1_3d,mat2,type = 'fro'):

    assert len(mat1_3d.shape) == 3
    assert mat1_3d.shape[0] == mat1_3d.shape[1]

    norms = []

    for i in range(mat1_3d.shape[2]):

        difference = mat1_3d[...,i] - mat2
        norm = np.linalg.norm(difference,ord = type)
        norms.append(norm)

    return np.where(norms == np.nanmin(norms))[0][0]

def find_tstar_ks(mat1_3d, mat2):

    assert len(mat1_3d.shape) == 3
    assert mat1_3d.shape[0] == mat1_3d.shape[1]

    norms, ks = [], []

    for i in range(mat1_3d.shape[2]):

        kstat, pval = scipy.stats.ks_2samp(np.ravel(mat1_3d[...,i]), np.ravel(mat2))
        norms.append(pval)
        ks.append(kstat)

    return np.where(ks == np.nanmin(ks))[0][0]




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


subject_list = ['Sub2',
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
emp_path = '/home/brainlab/Desktop/Rudas/Data/PET_MRI_Data_Preped/emp_fc/'
temperature_params = [(0.0001,5,100),(0.0001,4,100)]
sizes = ['(120)', '(84)']

pet_flags = [False]#,True]

for pet_flag in pet_flags:

    for sub in subject_list:

        for ind, parcel in enumerate(parcels):

            load_path_sim = main_path + 'Ising/' + sub + '/PET/' + parcel + '/' if pet_flag else main_path + 'Ising/' + sub + '/' + parcel + '/'
            load_path_emp = emp_path + sub + '/' + parcel + '/emp_fc.csv'

            if not file_exists(load_path_sim+'sim_fc_tcrit.png'):

                temperature_parameters = temperature_params[ind]

                emp_fc = np.squeeze(load_matrix(load_path_emp))

                sim_fc = np.squeeze(load_matrix(load_path_sim + 'sim_fc.npy'))

                t_crit = np.squeeze(load_matrix(load_path_sim + 'ctem.csv'))

                temps = np.round(np.linspace(temperature_parameters[0], temperature_parameters[1], num=temperature_parameters[2]),5)

                t_crit_loc = np.where(temps == t_crit)[0]

                # to minimize this distance between matrices take difference (sim_fc - emp_fc) for each temperature
                # then find the distance (norm) of that matrix
                # the matrix with the smallest distance of this difference is the 'best fit'

                #tstar_loc = find_tstar_fro(sim_fc,emp_fc,type='fro')

                tstar_loc = find_tstar_ks(sim_fc,emp_fc)
                save_path = load_path_sim + 'ks/'
                makedir2(save_path)

                save_file(np.array([[tstar_loc]]),save_path,'tstar_loc_fro')
                save_file(np.array([temps[tstar_loc]]),save_path,'tstar_fro')
                save_file(sim_fc[...,tstar_loc],save_path,'best_sim_fc')
                save_file(emp_fc,save_path,'emp_fc')

                plt.figure()
                sns.heatmap(emp_fc,cmap='plasma')
                plt.title('Empirical FC ' + sub + ' ' + sizes[ind])
                plt.savefig(save_path+'emp_fc.png', dpi=600)
                plt.close()

                plt.figure()
                sns.heatmap(sim_fc[...,tstar_loc],cmap='plasma')
                plt.title('Simulated FC at T*' + sub + ' ' + sizes[ind])
                plt.savefig(save_path+'sim_fc_tstar.png', dpi=600)
                plt.close()

                plt.figure()
                sns.heatmap(sim_fc[..., tstar_loc], cmap='plasma')
                plt.title('Simulated FC at Tc' + sub + ' ' + sizes[ind])
                plt.savefig(save_path + 'sim_fc_tcrit.png', dpi=600)
                plt.close()

                print('Done:', save_path,'sim_fc_tcrit.png')
            else:
                print('Already done!',  load_path_sim,'sim_fc_tcrit.png')





