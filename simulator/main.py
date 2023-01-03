"""
MAIN
"""
# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

from _modules.makematfile import matfile_cp_voce
from _modules.makesimfile import simfile_uniaxial
from _modules.plotsscurve import plot_sscurve
from _modules.gridify import gridify_output
import time, subprocess, os, csv
import pandas as pd
import envbash

# Input/Output folders
FOLDER_INPUT  = 'A617KAERI/i3_middle'
FOLDER_OUTPUT = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))

# Input files
MESH_FILE     = "input_meshfile.e"
GRAINS_FILE   = "input_grainsfile.csv"
MATERIAL_FILE = "input_matfile.xml"

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

# Check the number of grains in "input_grainsfile.csv"
GRAINSFILE = pd.read_csv(r'input_grainsfile.csv', header=None)
NUM_GRAINS = len(GRAINSFILE)  # number of grains

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# USER INPUTS
# -----------------------------------------------------------------------------------
# Model
MAX_HORIZONTAL = 113  # model size
MAX_VERTICAL   = 88  # model size
PIXEL_SIZE     = 0.1  # for gridifying the outputs
# Applied Strain
REQUESTED_STRAIN     = 0.01
APPLIED_DISPLACEMENT = MAX_HORIZONTAL * REQUESTED_STRAIN
# Time
START_TIME = 0
END_TIME   = 1
# Solver
dt_START = 0.1
dt_MIN   = 1e-10
dt_MAX   = 0.1

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# MATERIAL FILE INPUTS:
# -----------------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------------
# Creat xml material file
matfile_cp_voce(YOUNGS, POISSONS, SLIP_DIRECTION, SLIP_PLANE, MATERIAL_NAME, 
    VSH_tau_sat, VSH_b, VSH_tau_0, AI_gamma0, AI_n)

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# SIMULATIONS FILE INPUTS:
# -----------------------------------------------------------------------------------
"""
!> pinXY has to exist in the mesh file 
!> z0 plane is created by mooose 
[BCs]
  [./x0] type = DirichletBC, boundary = 'pinXY', variable = disp_x, value = 0.0
  [./y0] type = DirichletBC, boundary = 'pinXY', variable = disp_y, value = 0.0
  [./z0] type = DirichletBC, boundary = 'z0',    variable = disp_z, value = 0.0
  [./z1] type = FunctionDirichletBC, boundary = 'z1', variable = disp_z, function = applied_displacement
[]
[Functions]
  [./applied_displacement]
    type = PiecewiseLinear
    x = '0 1'
    y = '0 0.19'
  [../]
[]
"""
# -----------------------------------------------------------------------------------
# Create MOOSE/DEER simulation file
simfile_uniaxial(MESH_FILE, GRAINS_FILE, NUM_GRAINS, MATERIAL_FILE, MATERIAL_NAME,  
                 APPLIED_DISPLACEMENT, START_TIME, END_TIME, dt_START, dt_MIN, dt_MAX)

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# RUN SIMULATIONS
# -----------------------------------------------------------------------------------
PATH_DEER       = "/home/omz/moose/deer/deer-opt"
NUM_PROCESSORS  = 32
TASKS_PER_NODE  = 8
VERBOSE_DISPLAY = True
# Run simulation
COMMAND = "mpiexec -np {num_processors} {path_deer} -i {input_path}".format(
    path_deer       = PATH_DEER,
    num_processors  = NUM_PROCESSORS,
    tasks_per_node  = TASKS_PER_NODE,
    input_path      = 'input_simfile.i',
)

print('------------------------------------')
print('./> Running Simulation')
print('------------------------------------')

print(PATH_OUTPUT)
print(COMMAND)
subprocess.run('ls', cwd=PATH_OUTPUT)
envbash.load_envbash('/home/omz/.bash_profile')  # source ~/.bash_profile
subprocess.run([COMMAND],  shell=True, check=True, cwd=PATH_OUTPUT)
print('------------------------------------')
print('./> Simulation Error')
print('------------------------------------')

print('------------------------------------')
print('./> Done')
print('------------------------------------')

# %% ---------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
print('------------------------------------')
print('./> Plotting Stress-Strain Curves')
print('------------------------------------')

plot_sscurve(PATH_OUTPUT, VSH_tau_sat, VSH_b, VSH_tau_0, AI_gamma0, AI_n)

print('------------------------------------')
print('./> Done')
print('------------------------------------')

# %% ---------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
print('------------------------------------')
print('./> Gridifying Output')
print('------------------------------------')

gridify_output(PATH_OUTPUT, PIXEL_SIZE, MAX_HORIZONTAL, MAX_VERTICAL)

print('------------------------------------')
print('./> Done')
print('------------------------------------')

# %% ---------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

print('------------------------------------')
print('./> LA FIN (MAIN)')
print('------------------------------------')