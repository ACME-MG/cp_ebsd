"""
MAIN
"""
#%%

from modules.makematfile import matfile_cp_voce
from modules.makesimfile import simfile_uniaxial
import time, subprocess, os, csv

FOLDER_NAME         = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))

# Create paths
PATH_HOME    = os.getcwd()
PATH_RESULTS = PATH_HOME + '/results' 
PATH_SIM     = PATH_RESULTS + '/' + FOLDER_NAME

# Create a simulation folder
os.mkdir(PATH_RESULTS + '/' + FOLDER_NAME)
# Copy input files into the simulation folder
os.system('cp inmeshfile.e ingrainsfile.csv ' + PATH_SIM)
# Walk to the simulation folder
os.chdir(PATH_SIM)

#%%
# ----------------------------------------------------------
# MOOSE/DEER SIMULATIONS
# ----------------------------------------------------------
PATH_DEER       = "~/moose/deer/deer-opt"
NUM_PROCESSORS  = 32
TASKS_PER_NODE  = 8
VERBOSE_DISPLAY = True

# ----------------------------------------------------------
# MATERIAL FILE INPUTS:
# ----------------------------------------------------------
MATERIAL_NAME = 'CP1'
YOUNGS   = 211000             # IsotropicLinearElasticModel
POISSONS = 0.30               # IsotropicLinearElasticModel
# Asaro Inelasticity  
VSH_tau_sat = 12              # VoceSlipHardening
VSH_b       = 66.6666666667   # VoceSlipHardening
VSH_tau_0   = 40              # VoceSlipHardening
AI_gamma0   = 9.55470706737e-08 # PowerLawSlipRule
AI_n        = 12                # PowerLawSlipRule
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
MESH_FILE      = "inmeshfile.e"
GRAINS_FILE    = "ingrainsfile.csv"
NUM_GRAINS     = 190
MATERIAL_FILE  = "inmatfile.xml"
# Loading
STRESS_X    = 0
STRESS_Y    = 0 
STRESS_Z    = 100
# Time
START_TIME  = 0
END_TIME    = 1
# Solver 
dt_START    = 0.1
dt_MIN      = 1e-10
dt_MAX      = 0.1
# ----------------------------------------------------------
# Create MOOSE/DEER simulation file
simfile_uniaxial(MESH_FILE, GRAINS_FILE, NUM_GRAINS, MATERIAL_FILE, MATERIAL_NAME,  
START_TIME, END_TIME, STRESS_X, STRESS_Y, STRESS_Z, dt_START, dt_MIN, dt_MAX)

#%%
# ----------------------------------------------------------
# RUN SIMULATIONS
# ----------------------------------------------------------
command = "mpiexec -np {num_processors} {path_deer} -i {input_path}".format(
    path_deer       = PATH_DEER,
    num_processors  = NUM_PROCESSORS,
    tasks_per_node  = TASKS_PER_NODE,
    input_path      = 'insimfile.i',
)

#%%
#subprocess.call([command], shell = True)
subprocess.run([command],  shell = True, check = True)