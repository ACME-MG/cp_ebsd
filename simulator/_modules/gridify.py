#%%
import os, re
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def gridify_output(PATH_OUTPUT, PIXEL_SIZE, MAX_HORIZONTAL, MAX_VERTICAL):

    os.chdir(PATH_OUTPUT)

    include_name = 'output_VPEVS_'
    exclude_name = 'output_VPEVS_time.csv'

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
    print('------------------------------------')
    print('List All VPEVS Output Files')
    print('VectorPostprocessors: type = ElementValueSampler')
    print('------------------------------------')
    print(df_names)
    print('------------------------------------')

    for df in df_list:

        # Extract numbers from the dataframe name
        numbers = re.findall(r'\d+', df.name)
        df_count = ''.join(numbers)
        df_name  = 'output_gridify_' + df_count + '.csv'
        print(df_name)

        xOld = df['z']
        yOld = df['y']

        xNew = np.arange(min(round(xOld)), max(round(xOld)), PIXEL_SIZE)
        yNew = np.arange(min(round(yOld)), max(round(yOld)), PIXEL_SIZE)
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
            # Plot gridified data
            # -------------------------------
            # Create plot name
            plt_name = column + '_' + df_count
            # Calculate (width_of_image/height_of_image)
            ratio = zGrid.shape[1]/zGrid.shape[0]
            fig, (ax) = plt.subplots(1, figsize=(8, 8))
            plt.contourf(xGrid, yGrid, zGrid, 20, cmap='bwr', 
                vmin=round(np.amin(zGrid),4), vmax=round(np.amax(zGrid),4))
            plt.xlim([0, MAX_HORIZONTAL])
            plt.ylim([0, MAX_VERTICAL])
            plt.xticks([])
            plt.yticks([])
            plt.axis('image')
            plt.colorbar(orientation="horizontal", fraction=0.040*ratio)
            plt.tight_layout()
            plt.savefig(plt_name)
            plt.close(fig)
        # Save gridified data in columns    
        dfNew.to_csv(df_name, index=False)
