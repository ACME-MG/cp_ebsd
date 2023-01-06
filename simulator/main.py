"""
MAIN
"""
# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
from _modules.makematfile import matfile_cp_voce
from _modules.makesimfile import simfile_uniaxial
from _modules.plotsscurve import plot_sscurve
from _modules.gridify import gridify_output
import time, subprocess, os, sys 
import pandas as pd
import envbash

sys.path.append('/home/omz/seacas/lib')
import exodus

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# USER INPUTS
# -----------------------------------------------------------------------------------
# Applied Strain
REQUESTED_STRAIN = 0.005  # applied strain
# Time
START_TIME = 0
END_TIME   = 1
# Solver
dt_START = 0.025
dt_MIN   = 1e-10
dt_MAX   = 0.25
# Output 
PIXEL_SIZE = 0.1   # gridifying the outputs
# -----------------------------------------------------------------------------------
# Input/Output folders
FOLDER_INPUT = 'A617KAERI/i2_middle'
FOLDER_OUTPUT = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
print('------------------------------------')
print('FOLDER_INPUT =',  FOLDER_INPUT)
print('FOLDER_OUTPUT =', FOLDER_OUTPUT)
print('------------------------------------')

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# FILE MANAGMENT
# -----------------------------------------------------------------------------------
# Input files
MESH_FILE     = "input_meshfile.e"
GRAINS_FILE   = "input_grainsfile.csv"
MATERIAL_FILE = "input_matfile.xml"
# -----------------------------------------------------------------------------------
# Create paths
PATH_HOME    = os.getcwd()
PATH_INPUT   = PATH_HOME + '/input/'  + FOLDER_INPUT
PATH_OUTPUT  = PATH_HOME + '/output/' + FOLDER_INPUT + '/' + FOLDER_OUTPUT
print('------------------------------------')
print('PATH_INPUT =',  PATH_INPUT)
print('PATH_OUTPUT =', PATH_OUTPUT)
print('------------------------------------')
# -----------------------------------------------------------------------------------
# Create an output folder
os.system('mkdir -p ' + PATH_OUTPUT)
# Copy input files into the simulation folder
os.system('cp ' + PATH_INPUT + '/* ' + PATH_OUTPUT)
# Go the output folder
os.chdir(PATH_OUTPUT)

# %% --------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# INPUT MESH EXODUS FILE
# -----------------------------------------------------------------------------------
# Open input_meshfile.e
E = exodus.exodus(MESH_FILE, 'r')
# Get coorinates
x_coords, y_coords, z_coords = E.get_coords()
print('------------------------------------')
print('./> MODEL INFO/SIZE')
print('------------------------------------')
print('x_coords:',   min(x_coords), max(x_coords),
      '\ny_coords:', min(y_coords), max(y_coords),
      '\nz_coords:', min(z_coords), max(z_coords))
print('NUM_GRAINS = ',   E.num_blks())
print('NUM_ELEMENTS = ', E.num_elems())
print('NUM_NODES = ',    E.num_nodes())
print('------------------------------------')
# Set variables
NUM_GRAINS = E.num_blks()  # number of grains
MAX_X = max(x_coords)
MAX_Y = max(y_coords)
MAX_Z = max(z_coords)

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
# Applied Displacment
APPLIED_DISPLACEMENT = MAX_Z * REQUESTED_STRAIN
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
print('./> RUNNING SIMULATION')
print('------------------------------------')

print(PATH_OUTPUT)
print(COMMAND)
print('------------------------------------')
subprocess.run('ls', cwd=PATH_OUTPUT)
print('------------------------------------')
envbash.load_envbash('/home/omz/.bash_profile')  # source ~/.bash_profile
subprocess.run([COMMAND],  shell=True, check=True, cwd=PATH_OUTPUT)
print('------------------------------------')
print('./> SIMULATION ERROR')
print('------------------------------------')

print('------------------------------------')
print('./> DONE')
print('------------------------------------')

# %% ---------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
print('------------------------------------')
print('./> PLOTTING STRESS-STRAIN CURVES')
print('------------------------------------')

# Plot stress strain curve
plot_sscurve(PATH_OUTPUT, VSH_tau_sat, VSH_b, VSH_tau_0, AI_gamma0, AI_n)

print('------------------------------------')
print('./> DONE')
print('------------------------------------')

# %% ---------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
print('------------------------------------')
print('./> GRIDIFYING OUTPUT')
print('------------------------------------')

# Gridify the output using defined pixel size. 
# The through thickness (X) is not considered. 
gridify_output(PATH_OUTPUT, PIXEL_SIZE, MAX_Z, MAX_Y)

print('------------------------------------')
print('./> DONE')
print('------------------------------------')

# %% ---------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

print('------------------------------------')
print('./> LA FIN (MAIN)')
print('------------------------------------')