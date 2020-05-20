from projects.neuroimaging_pipelines.pipeline import PipelineDWI

paths = {'input_path': '/home/brainlab/Desktop/Pubu/test_dwi',
         'image_parcellation_path': [
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
         't1_relative_path': 'data/T1w/T1w_acpc_dc_restore_1.25.nii.gz',
         'dwi_relative_path': 'data/T1w/Diffusion/data.nii.gz',
         'bvec_relative_path': 'data/T1w/Diffusion/bvecs',
         'bval_relative_path': 'data/T1w/Diffusion/bvals'}

parameters = {'iso_size': 2}

subject_list = ['103414']
                #'857263_3T_Diffusion_preproc',
                #'856766_3T_Diffusion_preproc',
                #'792564_3T_Diffusion_preproc',
                #'756055_3T_Diffusion_preproc',
                #'751348_3T_Diffusion_preproc',
                #'672756_3T_Diffusion_preproc',
                #'654754_3T_Diffusion_preproc',
                #'499566_3T_Diffusion_preproc',
                #'414229_3T_Diffusion_preproc',
                #'397760_3T_Diffusion_preproc',
                #'366446_3T_Diffusion_preproc',
                #'298051_3T_Diffusion_preproc',
                #'280739_3T_Diffusion_preproc']
                #'211720_3T_Diffusion_preproc']
                #'245333_3T_Diffusion_preproc',
                #'239944_3T_Diffusion_preproc',
                #'221319_3T_Diffusion_preproc',
                #'214423_3T_Diffusion_preproc',
                #'212318_3T_Diffusion_preproc']

pipeline = PipelineDWI(paths=paths, parameters=parameters, subject_list=subject_list)
pipeline.run()
