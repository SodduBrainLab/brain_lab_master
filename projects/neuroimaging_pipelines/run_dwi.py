from projects.neuroimaging_pipelines.pipeline import PipelineDWI

paths = {'input_path': '/home/brainlab/Desktop/Rudas/Data/DTI_st_joes',
         'image_parcellation_path': [
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/atlas_NMI_2mm.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn/Parcels_MNI_222.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/AAL2/aal2.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/Auditory/Auditory_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/CinguloOperc/CinguloOperc_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/CinguloParietal/CinguloParietal_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/Default/Default_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/DorsalAttn/DorsalAttn_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/FrontoParietal/FrontoParietal_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/RetrosplenialTemporal/RetrosplenialTemporal_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/SMhand/SMhand_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/SMmouth/SMmouth_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/VentralAttn/VentralAttn_parcellation_5.nii',
             '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/Visual/Visual_parcellation_5.nii'],
         'reference': '/home/brainlab/Desktop/Rudas/Data/Parcellation/MNI152_T1_2mm_brain.nii.gz',
         'template_spm_path': '/home/brainlab/Desktop/Rudas/Data/Parcellation/TPM.nii',
         'mcr_path': '/home/brainlab/Desktop/Rudas/Tools/MCR/v713',
         'spm_path': '/home/brainlab/Desktop/Rudas/Tools/spm12_r7487/spm12/run_spm12.sh',
         't1_relative_path': 'T1w.nii.gz',
         'dwi_relative_path': 'AP/data.nii',
         'bvec_relative_path': 'AP/bvec',
         'bval_relative_path': 'AP/bval'}

parameters = {'iso_size': 2}

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


pipeline = PipelineDWI(paths=paths, parameters=parameters, subject_list=subject_list)
pipeline.run()
