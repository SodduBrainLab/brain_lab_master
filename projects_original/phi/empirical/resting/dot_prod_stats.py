import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 18})

# The first thing to do is create and store the data as dictionaries to turn into a pandas dataframe

path = '/Users/npopiel/Documents/empirical_phi/'
filename = path + 'tot_phi.csv'

df = pd.read_csv(filename)

states = ['Awake','Mild','Deep','Recovery']
networks = ['Aud','DMN','Dorsal','Ventral','Cingulo','Fronto','Retro','SMhand','SMmouth','Vis','Baseline']

# Establish test vector
test_vector = np.array([4,3,2,1])

# Get the norm of the test vector
len_test_vec = np.linalg.norm(test_vector)

#norm_vector = test_vector/len_test_vec

# Initialize dictionaries and lists for data storage
dict_rest,dict_task = {},{}

cos_list_rest, cos_list_task = [],[]

# Loop over each network
for network in networks:

    # Generate a matrix of the phi values with each column being a state and each row being a subject. Repeat for rest and taken
    rest_by_network = df.loc[df.network==network]
    rest_by_network = rest_by_network.loc[rest_by_network.task=='no']
    rest_matrix = np.array([np.array(rest_by_network.phi[rest_by_network.state=='Awake']),
                            np.array(rest_by_network.phi[rest_by_network.state=='Mild']),
                            np.array(rest_by_network.phi[rest_by_network.state=='Deep']),
                            np.array(rest_by_network.phi[rest_by_network.state=='Recovery'])]).T

    task_by_network = df.loc[df.network == network]
    task_by_network = task_by_network.loc[task_by_network.task == 'yes']
    task_matrix = np.array([np.array(task_by_network.phi[task_by_network.state == 'Awake']),
                            np.array(task_by_network.phi[task_by_network.state == 'Mild']),
                            np.array(task_by_network.phi[task_by_network.state == 'Deep']),
                            np.array(task_by_network.phi[task_by_network.state == 'Recovery'])]).T

    # Take dot product (done as a matrix multiplication for ease)
    phi_dist_rest = rest_matrix@test_vector
    phi_dist_task = task_matrix@test_vector

    #phi_dist_rest = rest_matrix@norm_vector
    #phi_dist_task = task_matrix@norm_vector

    # Get norm of each phi vector
    rest_norm = np.linalg.norm(rest_matrix,axis=1)
    task_norm = np.linalg.norm(task_matrix,axis=1)

    # Get the distribution of cosines
    cos_dist_rest = np.squeeze(np.array(phi_dist_rest/(rest_norm*len_test_vec),dtype='float'))
    cos_dist_task = np.squeeze(np.array(phi_dist_task/(task_norm*len_test_vec),dtype='float'))

    #cos_dist_rest = np.squeeze(np.array(phi_dist_rest / (rest_norm), dtype='float'))
    #cos_dist_task = np.squeeze(np.array(phi_dist_task / (task_norm), dtype='float'))


    # Append the distributions for the network in a list
    cos_list_rest.append(np.array([cos_dist_rest,[network]*len(cos_dist_rest)]))
    cos_list_task.append(np.array([cos_dist_task,[network]*len(cos_dist_task)]))

# Turn the lists into a single column array
cos_array_rest = np.hstack(cos_list_rest)
cos_array_task = np.hstack(cos_list_task)

labels = ['cos_dist','network']

# Populate the dictionaries
for ind,name in enumerate(labels):

    dict_rest[name] = cos_array_rest[ind]
    dict_task[name] = cos_array_task[ind]
# Turn dictionaries into dataframes
df_rest = pd.DataFrame(dict_rest)
df_task = pd.DataFrame(dict_task)

# Add column to dataframe forresponding to whether it is a task or not
df_rest['task'] = ['no']*df_rest['cos_dist'].count()
df_task['task'] = ['yes']*df_rest['cos_dist'].count()

# COncatenate dataframes
df = pd.concat([df_rest,df_task])

df["cos_dist"] = pd.to_numeric(df["cos_dist"])


g = sns.FacetGrid(df, row="task", col="network", margin_titles=True)
bins = np.linspace(0, 1, 13)
g.map(plt.hist, "cos_dist", color="steelblue", bins=bins)
plt.savefig('/Users/npopiel/Documents/empirical_phi/plots_phi_paper/cosinedist/cos_dist_vec12.pdf')