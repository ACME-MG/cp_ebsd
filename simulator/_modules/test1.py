#%%
import os, re
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.colors as colors

PATH_OUTPUT = '/data2/omz/abq10jobs/cp_ebsd/simulator/output/A617KAERI_grains190/221226150335_2'
os.chdir(PATH_OUTPUT)

include_name = 'output_ELMTS_'
exclude_name = 'output_ELMTS_time.csv'

# Initialize an empty list to store the dataframes
df_list = []

# Iterate over the files in the directory
for filename in os.listdir(PATH_OUTPUT):
    # Check if the string is in the filename and if the filename is not the excluded file
    if include_name in filename and filename != exclude_name :
        # If the string is in the filename and the filename is not the excluded file, read the file into a dataframe
        df = pd.read_csv(os.path.join(PATH_OUTPUT, filename))
        df.name = filename
        # Add the dataframe to the list
        df_list.append(df)
     
# Sort the dataframes by their name using the sorted function and a key function   
df_list = sorted(df_list, key=lambda df: df.name)
df_names = [df.name for df in df_list]
print(df_names)

for df in df_list:
    
    # Extract numbers from the dataframe name
    numbers = re.findall(r'\d+', df.name)
    df_count = ''.join(numbers)
    df_name  = 'output_gridify_' + df_count + '.csv'
    print(df_name)

    xOld = df['z']
    yOld = df['y']

    xNew = np.arange(min(round(xOld)), max(round(xOld)), 0.1)
    yNew = np.arange(min(round(yOld)), max(round(yOld)), 0.1)
    xGrid, yGrid = np.meshgrid(xNew, yNew)

    dfNew = pd.DataFrame()
    dfNew = pd.DataFrame({'x': xGrid.flatten(), 'y': yGrid.flatten()})

    column_names = ['cauchy_stress_xx', 'cauchy_stress_yy', 'cauchy_stress_zz',
       'elastic_strain_xx', 'elastic_strain_yy', 'elastic_strain_zz', 'id',
       'mechanical_strain_xx', 'mechanical_strain_yy', 'mechanical_strain_zz',
       'orientation_q1', 'orientation_q2', 'orientation_q3', 'orientation_q4',
       'strain_xx', 'strain_yy', 'strain_zz']

    for column in column_names:
        zOld = df[column]
        zGrid = interpolate.griddata((xOld, yOld), zOld, (xGrid, yGrid), method='nearest')
        dfNew[column] = zGrid.flatten()
    
    dfNew.to_csv(df_name, index=False)

print('La Fin')
