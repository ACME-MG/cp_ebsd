import os
import pandas as pd
import matplotlib.pyplot as plt

lw = 3  # linewidth
 
def plot_sscurve(PATH_OUTPUT, VSH_tau_sat, VSH_b, VSH_tau_0, AI_gamma0, AI_n):
    
    print('------------------------------------')
    print('Start Plotting Stress-Strain Curves')
    print('------------------------------------')

    # Go to work directory            
    os.chdir(PATH_OUTPUT)
    # Import output file
    output = pd.read_csv(r'output.csv')
    # XX ------------------------------------------
    # ---------------------------------------------
    fig, (ax) = plt.subplots (1, figsize = (10,10))
    # Plot measurements
    ax.plot(output['mTE_xx'], output['mCS_xx'], color = 'steelblue', 
            linewidth=lw, label='mCS_xx')  # plot measurement
    ax.set_title('XX Stress-Strain Curve', fontsize=18)
    ax.set_xlabel('True Strain(mTE_xx) ', fontsize=18)
    ax.set_ylabel('True Stress (mCS_xx) [MPa]', fontsize=18)
    ax.grid(which='major', axis='both', color='SlateGray', linewidth=1, linestyle=':')
    ax.legend(loc='upper left', fontsize=18)
    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    	label.set_fontsize(16)
    # plt.show()
    plt.savefig("SSC_xx.png")
    # YY ------------------------------------------
    # ---------------------------------------------
    fig, (ax) = plt.subplots(1, figsize=(8, 8))
    # Plot measurements
    ax.plot(output['mTE_yy'], output['mCS_yy'], color='steelblue',
            linewidth=lw, label='mCS_yy')  # plot measurement
    ax.set_title('YY Stress-Strain Curve', fontsize=18)
    ax.set_xlabel('True Strain(mTE_yy) ', fontsize=18)
    ax.set_ylabel('True Stress (mCS_yy) [MPa]', fontsize=18)
    ax.grid(which='major', axis='both',
            color='SlateGray', linewidth=1, linestyle=':')
    ax.legend(loc='upper left', fontsize=18)
    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    	label.set_fontsize(16)
    # plt.show()
    plt.savefig("SSC_yy.png")
    # ZZ ------------------------------------------
    # ---------------------------------------------
    fig, (ax) = plt.subplots(1, figsize=(8, 8))
    # Plot measurements
    ax.plot(output['mTE_zz'], output['mCS_zz'], color='steelblue',
            linewidth=lw, label='mCS_zz')  # plot measurement
    ax.set_title('ZZ Stress-Strain Curve', fontsize=18)
    ax.set_xlabel('True Strain(mTE_zz) ', fontsize=18)
    ax.set_ylabel('True Stress (mCS_zz) [MPa]', fontsize=18)
    ax.grid(which='major', axis='both',
            color='SlateGray', linewidth=1, linestyle=':')
    ax.legend(loc='upper left', fontsize=18)
    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    	label.set_fontsize(16)
    # Textbox
    ax.text(0, 0, '  tau_sat = ' + str(VSH_tau_sat) + ' MPa' +
                  '\n  b = ' + str(VSH_b) + ' MPa' +
                  '\n  tau_0 = ' + str(VSH_tau_0) + ' MPa' +
                  '\n  gamma0 = ' + str(AI_gamma0) +
                  '\n  n = ' + str(AI_n),
            fontsize=16, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10, })
    #   plt.show()
    plt.savefig("SSC_zz.png")

    print('------------------------------------')
    print('Finish Plotting Stress-Strain Curves')
    print('------------------------------------')
