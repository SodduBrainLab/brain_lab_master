import numpy as np
import time
import scipy
import os
from projects.generalize_ising_model.core2 import generalized_ising
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
    elif str(extension) == 'txt':
        return np.loadtxt(file)
def makedir2(path):

    if not os.path.exists(path):
        os.mkdir(path)
        return True
    return True

def extract_rho(time_series):


    shape_ts = time_series.shape

    assert len(shape_ts) == 2
    assert shape_ts[0] != shape_ts[1]

    if shape_ts[0]>shape_ts[1]:
        time_series=time_series.T


    rho = np.corrcoef(time_series)

    return rho

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
long_parcels = ['/_image_parcellation_path_..home..brainlab..Desktop..Rudas..Data..Parcellation..AAL2..aal2.nii/',
                '/_image_parcellation_path_..home..brainlab..Desktop..Rudas..Data..Parcellation..atlas_NMI_2mm.nii/']
save_path = '/home/brainlab/Desktop/Rudas/Data/PET_MRI_Data_Preped/emp_fc/'
load_path = '/home/brainlab/Desktop/Rudas/Data/PET_MRI_Data_Preped/Baseline/output/datasink/preprocessing/sub-'
ts_name = 'time_series.csv'
pet_flags = [False,True]

for ind1, sub in enumerate(subject_list):

    for ind, parcel in enumerate(parcels):

        path = load_path + sub + long_parcels[ind] + ts_name

        ts = np.squeeze(load_matrix(path))

        fc = extract_rho(ts)

        makedir2(save_path+sub+'/')
        makedir2(save_path+sub+'/'+parcel+'/')

        save_file(fc,save_path+sub+'/'+parcel+'/','emp_fc')



