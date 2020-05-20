from projects.qm_brain.utils.utils import  *
import numpy as np
import pandas as pd

num_subjects = 13
main_path = '/home/user/Desktop/QMBrain/nyc_data/'

condition_list = ['Cond10/','Cond12/']

dictX,dictY = {},{}

for condition in condition_list:

    min_x_list, min_y_list,tot_list = [], [],[]

    max_x, max_y = [],[]

    for i in range(num_subjects):

        subject_path = main_path + condition + str(i + 1) + '/results/norm/'

        uncertain_x = load_matrix(subject_path+'DeltaXDeltaPX.csv')
        uncertain_y = load_matrix(subject_path+'DeltaXDeltaPY.csv')

        min_x_list.append(np.min(uncertain_x))
        min_y_list.append(np.min(uncertain_y))
        max_x.append(np.max(uncertain_x))
        max_y.append(np.max(uncertain_y))
    dictX[condition] = min_x_list
    dictY[condition] = min_y_list

    avg_x = np.mean(np.array(min_x_list))
    avg_y = np.mean(np.array(min_y_list))

    std_x = np.std(np.array(min_x_list))
    std_y = np.std(np.array(min_y_list))

    tot_list.append(min_x_list)
    tot_list.append(min_y_list)

    print('The minimum uncertainty is: ', avg_x, 'plus or minus', np.std(np.array(min_x_list)),condition)
    print('The minimum uncertainty for y is: ', avg_y, 'plus or minus', np.std(np.array(min_y_list)),condition)
    print('The minimum uncertainty is: ', np.mean(np.array(tot_list)), 'plus or minus',  np.std(np.array(tot_list)), condition)
    print('The maximum uncertainty for x is: ', np.max(np.array(max_x)), condition)
    print('The maximum uncertainty for y is: ', np.max(np.array(max_y)), condition)


table_x = pd.DataFrame(dictX)
table_y = pd.DataFrame(dictY)

print('Table X')
print(table_x.to_latex())

print('Table Y')
print(table_y.to_latex())

