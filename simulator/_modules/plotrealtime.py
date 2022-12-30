
#%%
import os
import pandas as pd
import matplotlib.pyplot as plt

PATH_OUTPUT = '/data2/omz/abq10jobs/cp_ebsd/simulator/output/A617KAERI_grains190/221226150335_2'
os.chdir(PATH_OUTPUT)

output = pd.read_csv(r'output.csv')

lw = 3 # linewidth

#%%
fig, (ax) = plt.subplots (1, figsize = (10,10))
# Plot measurements
ax.plot(output['mTE_zz'], output['mCS_zz'], color = 'steelblue', linewidth=lw, label='mCS_zz')  # plot measurement
ax.set_title('Stress-Strain Curve', fontsize=18)
ax.set_xlabel('True Strain', fontsize=18)
ax.set_ylabel('True Stress [MPa]', fontsize=18)
ax.grid(which='major', axis='both', color='SlateGray', linewidth=1, linestyle=':')
ax.legend(loc='upper left', fontsize=18)
# Set tick font size
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	label.set_fontsize(16)


# Textbox
ax.text(0, 0, ' tau_sat = '  + str(100) + ' MPa' + 
              '\n b = '      + str(50)  + 
              '\n tau_0 = '  + str(20)  + ' MPa' + 
              '\n gamma0 = ' + str(10)  +
              '\n n = '      + str(2),
         fontsize=16, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10, })

#   plt.show()
plt.savefig("SimulationCheck.png")

