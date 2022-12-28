import os
import pandas as pd
import matplotlib.pyplot as plt
 
def plot_sscurve(PATH_OUTPUT, VSH_tau_sat, VSH_b, VSH_tau_0, AI_gamma0, AI_n):
                 
    os.chdir(PATH_OUTPUT)
    # Import output file
    output = pd.read_csv(r'output.csv')
    # 
    lw = 3 # linewidth
    # Plot stress-strain curve
    fig, (ax) = plt.subplots (1, figsize = (10,10))
    # Plot measurements
    ax.plot(output['mTE_zz'], output['mCS_zz'], color = 'steelblue', linewidth=lw, label='mCS_zz')  # plot measurement
    ax.set_title('Stress-Strain Curve', fontsize=18)
    ax.set_xlabel('True Strain(mTE_zz) ', fontsize=18)
    ax.set_ylabel('True Stress (mCS_zz) [MPa]', fontsize=18)
    ax.grid(which='major', axis='both', color='SlateGray', linewidth=1, linestyle=':')
    ax.legend(loc='upper left', fontsize=18)
    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    	label.set_fontsize(16)
    # Textbox
    ax.text(0, 0, '  tau_sat = '  + str(VSH_tau_sat) + ' MPa' + 
                  '\n  b = '      + str(VSH_b)       + ' MPa' +
                  '\n  tau_0 = '  + str(VSH_tau_0)   + ' MPa' + 
                  '\n  gamma0 = ' + str(AI_gamma0)   +
                  '\n  n = '      + str(AI_n),
             fontsize=16, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10, })

    #   plt.show()
    plt.savefig("SSCurve.png")