
#%%
import os
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.colors as colors
# Example of making your own norm.  Also see matplotlib.colors.
# From Joe Kington: This one gives two different linear ramps:

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
#####

os.chdir('/home/omz/abq10jobs/cp_ebsd/simulator/output/A617KAERI_grains190/221226150335_0')
df = pd.read_csv('output_ELMTS_0307.csv')

#%%
plt.plot(df['y'], df['z'], '.', markersize=0.1)
plt.show()

#%%
plt.scatter(df['z'], df['y'], c=df['cauchy_stress_zz'], marker='o', s=1, 
vmin=0, vmax=200)
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.show()

#%%

x = np.arange(0, 113, 0.1)
y = np.arange(0, 88, 0.1)
X, Y = np.meshgrid(x, y)

Z = interpolate.griddata((df['z'], df['y']), df['cauchy_stress_zz'], (X, Y), method='nearest')

plt.contourf(X, Y, Z, 20, cmap='bwr', norm=MidpointNormalize(midpoint=0))
plt.colorbar() 
plt.axis('image')

#%%

y = np.arange(0, 88, 1)
z = np.arange(0, 113, 1)
yy, zz = np.meshgrid(y, z)
