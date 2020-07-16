'''
For each subject
    load in AP
    load in PA
    normalize AP
    normalize PA
    Average AP, PA
    ensure average is normalized
    save
'''

import numpy as np
import scipy.io
import os
import networkx as nx




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

def to_normalize(J,netx = False):
    if netx:
        J = nx.to_numpy_array(J)
    max_J = np.max(J)
    min_J = np.min(J)

    if max_J >= 0 and max_J <= 1 and min_J >= 0 and min_J <= 1:
        if netx:
            return nx.to_networkx_graph(J)
        else:
            return J
    else:
        if netx:
            return nx.to_networkx_graph(J / max_J)
        else:
            return J / max_J

main_path = '/home/brainlab/Desktop/Rudas/Data/DTI_st_joes/'

ap_path = main_path + 'AP/output/workingdir/preproc/'

pa_path = main_path +'PA/output/workingdir/preproc/'

avg_path = main_path + 'Average/'

parcellation_list = ['_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..Visual..Visual_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..VentralAttn..VentralAttn_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..SMmouth..SMmouth_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..SMhand..SMhand_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..RetrosplenialTemporal..RetrosplenialTemporal_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..FrontoParietal..FrontoParietal_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..DorsalAttn..DorsalAttn_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..Default..Default_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..CinguloParietal..CinguloParietal_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..CinguloOperc..CinguloOperc_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn_parcellations..Auditory..Auditory_parcellation_5.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..rsn..Parcels_MNI_222.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..atlas_NMI_2mm.nii',
                    '_atlas_to_apply_..home..brainlab..Desktop..Rudas..Data..Parcellation..AAL2..aal2.nii']

sub_list = ['_subject_id_Sub1',
            '_subject_id_Sub2',
            '_subject_id_Sub3',
            '_subject_id_Sub4',
            '_subject_id_Sub5',
            '_subject_id_Sub6',
            '_subject_id_Sub7',
            '_subject_id_Sub8',
            '_subject_id_Sub9',
            '_subject_id_Sub10',
            '_subject_id_Sub11',
            '_subject_id_Sub12',
            '_subject_id_Sub13',
            '_subject_id_Sub14',
            '_subject_id_Sub15',
            '_subject_id_Sub16',
            '_subject_id_Sub17',
            '_subject_id_Sub18',
            '_subject_id_Sub19',
            '_subject_id_Sub20',
            '_subject_id_Sub21',
            '_subject_id_Sub22',
            '_subject_id_Sub23',
            '_subject_id_Sub24',
            '_subject_id_Sub25']

for ind, sub in enumerate(sub_list):
    sub_save_path = avg_path + 'Sub'+ str(ind+1)+ '/'
    makedir2(sub_save_path)
    for parcel in parcellation_list:
        parcel_save = sub_save_path + parcel.split('.')[-4] +'/'
        makedir2(parcel_save)

        ap_J = to_normalize(np.squeeze(load_matrix(ap_path + sub + '/' + parcel + '/tractography/Jij.csv')))
        pa_J = to_normalize(np.squeeze(load_matrix(pa_path + sub + '/' + parcel + '/tractography/Jij.csv')))

        avg = np.around(np.average(np.stack([ap_J,pa_J]),axis=0), 4)

        save_file(avg,parcel_save,'Jij')




