#%%
import sys, os
import numpy as np
sys.path.append('/home/omz/seacas/lib')
import exodus 

#%%

PATH_WORK = '/home/omz/abq10jobs/cp_ebsd/simulator/output/A617KAERI_grains191/230101071205'
os.chdir(PATH_WORK)
PATH_CHECK = os.getcwd()
print(PATH_CHECK)

#%%

E = exodus.exodus('input_meshfile.e', 'r')
num_steps = len(E.get_times()[:])
num_blks  = E.num_blks()
num_elms  = E.num_elems()
num_nodes = E.num_nodes()

x_coords, y_coords, z_coords = E.get_coords()
xMin = min(x_coords)
xMax = max(x_coords)
yMin = min(y_coords)
yMax = max(y_coords)
zMin = min(z_coords)
zMax = max(z_coords)

print('x_coords:'  , xMin, xMax, 
      '\ny_coords:', yMin, yMax,
      '\nz_coords:', zMin, zMax)


# %%
