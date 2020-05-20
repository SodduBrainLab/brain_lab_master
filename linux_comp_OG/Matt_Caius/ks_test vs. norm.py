from projects.generalize_ising_model.core import generalized_ising
from projects.generalize_ising_model.tools.utils import *
from projects.phi.tools.utils import *
import time
import scipy

#where data comes from
input_path = '/home/brainlab/Desktop/Matt/ConnectomeData/'
#where it will go
output_path = '/home/brainlab/Desktop/Matt/ConnectomeOutput/Test_2/KSvNORM'

makedir(output_path)

#temporary stuff
file_name = "collab_data.csv"
Output_filename = "CollabJij_"

#fetch the Jij csv file
J = to_normalize(np.loadtxt(input_path + file_name))
print(input_path+file_name)

temperature_parameters = (0.02, 3, 50)  # Temperature parameters (initial temp, final temperature, number of steps)
no_simulations = 1200  # Number of simulations after thermalization
thermalize_time = 0.3  #

start_time = time.time()

Simulated_FC, Critical_Temperature, E, M, S, H, meanSpins, timeCourses = generalized_ising(J,
                                                                                           temperature_parameters=temperature_parameters,
                                                                                           n_time_points=no_simulations,
                                                                                           thermalize_time=thermalize_time,
                                                                                           phi_variables=True,
                                                                                           return_tc=True,
                                                                                           type="digital")

final_time = time.time()
delta_time = final_time - start_time

print("It took " + str(delta_time) + " seconds to calculate the simulated functional connectivity matricies for the test cases\n\n")

TestTPMs = list()
for T in range(timeCourses.shape[-1]):

    tpm, state_total, frequency = main_tpm_branch(np.copy(timeCourses[..., T]))

    # Normalizing respect to rows
    for div in range(len(state_total)):
        if state_total[div] != 0.0:
            tpm[div, :] /= state_total[div]

    TestTPMs.append(tpm)


start_time = time.time()

Simulated_FC, Critical_Temperature, E, M, S, H, meanSpins, timeCourses = generalized_ising(J,
                                                                                           temperature_parameters=temperature_parameters,
                                                                                           n_time_points=no_simulations,
                                                                                           thermalize_time=thermalize_time,
                                                                                           phi_variables=True,
                                                                                           return_tc=True,
                                                                                           type="digital")

final_time = time.time()
delta_time = final_time - start_time

print("It took " + str(delta_time) + " seconds to calculate the simulated functional connectivity matricies for the ans cases\n\n")

AnsTPMs = list()
for T in range(timeCourses.shape[-1]):

    tpm, state_total, frequency = main_tpm_branch(np.copy(timeCourses[..., T]))

    # Normalizing respect to rows
    for div in range(len(state_total)):
        if state_total[div] != 0.0:
            tpm[div, :] /= state_total[div]

    AnsTPMs.append(tpm)

target = 10

save_tpm(AnsTPMs[target],output_path,0)

tstar1 = Find_Tstar(TestTPMs,AnsTPMs[target])
tstar2 = Find_Tstar(TestTPMs,AnsTPMs[target], type = "fro")
tstar3 = Find_Tstar(TestTPMs,AnsTPMs[target],type = "custom")
tstar4 = 0

ksResult = list()

for TPM in TestTPMs:
    ksResult.append(scipy.stats.ks_2samp(np.ravel(TPM), np.ravel(AnsTPMs[target]))[0])

tstar4 = int(np.where(np.asarray(ksResult) == np.min(ksResult))[0])

print(tstar1)
print(tstar2)
print(tstar3)
print(tstar4)

save_tpm(AnsTPMs[tstar1],output_path,1)
save_tpm(AnsTPMs[tstar2],output_path,2)
save_tpm(AnsTPMs[tstar3],output_path,3)
save_tpm(AnsTPMs[tstar4],output_path,4)


