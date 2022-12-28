"""
MAIN
"""
#%%

from _modules.makematfile import matfile_cp_voce
from _modules.makesimfile import simfile_uniaxial
from _modules.plotsscurve import plot_sscurve
import time, subprocess, os, csv

FOLDER_INPUT = 'A617KAERI_grains190'
FOLDER_OUTPUT = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))

# Create paths
PATH_HOME    = os.getcwd()
PATH_INPUT   = PATH_HOME + '/input/'  + FOLDER_INPUT
PATH_OUTPUT  = PATH_HOME + '/output/' + FOLDER_INPUT + '/' + FOLDER_OUTPUT

# Create an output folder
os.system('mkdir -p ' + PATH_OUTPUT)
# Copy input files into the simulation folder
os.system('cp ' + PATH_INPUT + '/* ' + PATH_OUTPUT)
# Go the output folder
os.chdir(PATH_OUTPUT)

#%%
# ----------------------------------------------------------
# MATERIAL FILE INPUTS:
# ----------------------------------------------------------
MATERIAL_NAME = 'CP1'
YOUNGS   = 211000        # IsotropicLinearElasticModel
POISSONS = 0.30          # IsotropicLinearElasticModel
# Asaro Inelasticity  
VSH_tau_sat = 30         # VoceSlipHardening
VSH_b       = 60.0       # VoceSlipHardening
VSH_tau_0   = 20         # VoceSlipHardening
AI_gamma0   = 0.001      # PowerLawSlipRule
AI_n        = 12         # PowerLawSlipRule
# Lattice & Slip Systems
LATTICE_a = 1.0
SLIP_DIRECTION  = "1 1 0"
SLIP_PLANE      = "1 1 1"
# ----------------------------------------------------------
# Creat xml material file
matfile_cp_voce(YOUNGS, POISSONS, SLIP_DIRECTION, SLIP_PLANE, MATERIAL_NAME, 
    VSH_tau_sat, VSH_b, VSH_tau_0, AI_gamma0, AI_n)

#%%
# ----------------------------------------------------------
# SIMULATIONS FILE INPUTS:
# ----------------------------------------------------------
NUM_GRAINS     = 190
MESH_FILE      = "input_meshfile.e"
GRAINS_FILE    = "input_grainsfile.csv"
MATERIAL_FILE  = "input_matfile.xml"
# Boudnary conditions 
BC_X0 = 'DirichletBC'; BC_Y0 = 'DirichletBC'; BC_Z0 = 'DirichletBC'
BC_X1 = 'FunctionNeumannBC' # or/ FunctionDirichletBC
BC_Y1 = 'FunctionNeumannBC' # or/ FunctionDirichletBC
BC_Z1 = 'FunctionDirichletBC' # or/ FunctionDirichletBC
# Loading
LOAD_X = 0
LOAD_Y = 0 
LOAD_Z = 1
# Time
START_TIME = 0
END_TIME   = 1
# Solver 
dt_START   = 0.01
dt_MIN     = 1e-10
dt_MAX     = 0.1
# ----------------------------------------------------------
# Create MOOSE/DEER simulation file
simfile_uniaxial(MESH_FILE, GRAINS_FILE, NUM_GRAINS, MATERIAL_FILE, MATERIAL_NAME,  
                 BC_X0, BC_Y0, BC_Z0, BC_X1, BC_Y1, BC_Z1, LOAD_X, LOAD_Y, LOAD_Z, 
                 START_TIME, END_TIME, dt_START, dt_MIN, dt_MAX)

#%%
# ----------------------------------------------------------
# RUN SIMULATIONS
# ----------------------------------------------------------
PATH_DEER       = "~/moose/deer/deer-opt"
NUM_PROCESSORS  = 32
TASKS_PER_NODE  = 8
VERBOSE_DISPLAY = True
# Run simulation
command = "mpiexec -np {num_processors} {path_deer} -i {input_path}".format(
    path_deer       = PATH_DEER,
    num_processors  = NUM_PROCESSORS,
    tasks_per_node  = TASKS_PER_NODE,
    input_path      = 'input_simfile.i',
)

#%%
#subprocess.call([command], shell = True)
subprocess.run([command],  shell = True, check = True)

#%%
# ----------------------------------------------------------
# PLOT RESULTS
# ----------------------------------------------------------
plot_sscurve(PATH_OUTPUT, VSH_tau_sat, VSH_b, VSH_tau_0, AI_gamma0, AI_n)

#%%
print('----------------------------------')
print('LA FIN')
print('----------------------------------')