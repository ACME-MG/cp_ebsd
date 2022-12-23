
# ==================================================
# Define global parameters
# ==================================================
[GlobalParams]
  displacements = 'disp_x disp_y disp_z'
[]
# ==================================================
# Define Mesh
# ==================================================
[Mesh]
  [./mesh_input]
    type = FileMeshGenerator
    file = "inmeshfile.e"
  [../]
  [./add_side_sets]
    input = mesh_input
    type = SideSetsFromNormalsGenerator
    normals = '0 -1  0 
               0  1  0
               -1 0  0
               1  0  0
               0  0 -1
               0  0  1'
    fixed_normal = true
    new_boundary = 'y0 y1 x0 x1 z0 z1'
  [../]
[]
# ==================================================
# Define Initial Orientations
# ==================================================
[UserObjects]
  [./euler_angle_file]
    type = ElementPropertyReadFile
    nprop = 3
    prop_file_name = "ingrainsfile.csv"
    read_type = block
    nblock = 190
    use_zero_based_block_indexing = false
  [../]
[]
# ==================================================
# Define Modules
# ==================================================
[Modules]
  [./TensorMechanics]
    [./Master]
      [./all]
        strain = FINITE #FINITE (for large deformation)
        add_variables = true
        new_system = true
        formulation = TOTAL
        volumetric_locking_correction = false
        generate_output = 'elastic_strain_xx elastic_strain_yy elastic_strain_zz
                           strain_xx strain_yy strain_zz
                           cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz
                           mechanical_strain_xx mechanical_strain_yy mechanical_strain_zz'
      [../]
    [../]
  [../]
[]
# ==================================================
# Define Variables
# ==================================================
[AuxVariables]
  # Material
  [./a]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./b]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./D]
    family = MONOMIAL
    order = CONSTANT
  [../]
  # For crystal orientations (quaternion)
  [./orientation_q1]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q2]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q3]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./orientation_q4]
    order = CONSTANT
    family = MONOMIAL
  [../]
[]
# ==================================================
# Define Kernels
# ==================================================
[AuxKernels]
  [q1]
    type = MaterialStdVectorAux
    property = orientation
    index = 0
    variable = orientation_q1
  [../]
  [q2]
    type = MaterialStdVectorAux
    property = orientation
    index = 1
    variable = orientation_q2
  [../]
  [q3]
    type = MaterialStdVectorAux
    property = orientation
    index = 2
    variable = orientation_q3
  [../]
  [q4]
    type = MaterialStdVectorAux
    property = orientation
    index = 3
    variable = orientation_q4
  [../]
[]
# ==================================================
# Apply stress
# ==================================================
[Functions]
  [./applied_load_x]
    type = PiecewiseLinear
    x = '0 1'
    y = '0 0'
  [../]
  [./applied_load_y]
    type = PiecewiseLinear
    x = '0 1'
    y = '0 0'
  [../]
  [./applied_load_z]
    type = PiecewiseLinear
    x = '0 1'
    y = '0 100'
  [../]
[]
# ==================================================
# Boundary Conditions
# ==================================================
[BCs]
  [./x0]
    type = DirichletBC
    variable = disp_x
    boundary = x0
    value = 0.0
  [../]
  [./y0]
    type = DirichletBC
    variable = disp_y
    boundary = y0
    value = 0.0
  [../]
  [./z0]
    type = DirichletBC
    variable = disp_z
    boundary = z0
    value = 0.0
  [../]
  [./x1]
    type = FunctionNeumannBC
    boundary = x1
    function = applied_load_x
    variable = disp_x
  [../]
  [./y1]
    type = FunctionNeumannBC
    boundary = y1
    function = applied_load_y
    variable = disp_y
  [../]
  [./z1]
    type = FunctionNeumannBC
    boundary = z1
    function = applied_load_z
    variable = disp_z
  [../]
[]
# ==================================================
# Define Material
# ==================================================

[Materials]
  [./stress]
    type = NEMLCrystalPlasticity
    database = "inmatfile.xml"
    model = "CP1"
    large_kinematics = true
    euler_angle_reader = euler_angle_file
  [../]
[]
# ==================================================
# Define Preconditioning
# ==================================================
[Preconditioning]
  [./SMP]
    type = SMP
    full = true
  [../]
[]
# ==================================================
# Define Postprocessing (History)
# ==================================================
[VectorPostprocessors]
  [./ELMTS]
    type = ElementValueSampler
    variable = 'orientation_q1 orientation_q2 orientation_q3 orientation_q4
                cauchy_stress_xx cauchy_stress_yy cauchy_stress_zz
                strain_xx strain_yy strain_zz
                elastic_strain_xx elastic_strain_yy elastic_strain_zz
                mechanical_strain_xx mechanical_strain_yy mechanical_strain_zz'
    contains_complete_history = false
    #execute_on = 'initial timestep_end' #NONE
    sort_by = id
    #outputs = ELSpler
  [../]
[]
# ==================================================
# Define Postprocessing (Model Average)
# ==================================================
[Postprocessors]
# Number of elemetts -----------------------------------------------------------
[./nelem]
  type = NumElems
[../]
# Mumber of degrees of freedom -------------------------------------------------
[./ndof]
  type = NumDOFs
[../]
# TimestepSize -----------------------------------------------------------------
  [./dt]
    type = TimestepSize
  [../]
# NumLinearIterations ----------------------------------------------------------
  [./num_lin_it]
    type = NumLinearIterations
  [../]
# NumNonlinearIterations -------------------------------------------------------
  [./num_nonlin_it]
    type = NumNonlinearIterations
  [../]
# ------------------------------------------------------------------------------
# AVERAGE FULL MODEL
# ------------------------------------------------------------------------------
# Mean: STRESS -----------------------------------------------------------------
  [./mCS_xx]
    type = ElementAverageValue
    variable = cauchy_stress_xx
  [../]
  [./mCS_yy]
    type = ElementAverageValue
    variable = cauchy_stress_yy
  [../]
  [./mCS_zz]
    type = ElementAverageValue
    variable = cauchy_stress_zz
  [../]
  # Mean: TOTAL STRAIN ---------------------------------------------------------
  [./mTE_xx]
    type = ElementAverageValue
    variable = strain_xx
  [../]
  [./mTE_yy]
    type = ElementAverageValue
    variable = strain_yy
  [../]
  [./mTE_zz]
    type = ElementAverageValue
    variable = strain_zz
  [../]
  # Mean: MECHANICAL STRAIN -------------------------------------------------------
  [./mME_xx]
    type = ElementAverageValue
    variable = mechanical_strain_xx
  [../]
  [./mME_yy]
    type = ElementAverageValue
    variable = mechanical_strain_yy
  [../]
  [./mME_zz]
    type = ElementAverageValue
    variable = mechanical_strain_zz
  [../]
  # Mean: ELASTIC STRAIN -------------------------------------------------------
  [./mEE_xx]
    type = ElementAverageValue
    variable = elastic_strain_xx
  [../]
  [./mEE_yy]
    type = ElementAverageValue
    variable = elastic_strain_yy
  [../]
  [./mEE_zz]
    type = ElementAverageValue
    variable = elastic_strain_zz
  [../]
[]
# ==================================================
# Define Simulation
# ==================================================
[Executioner]
  
  # Transient (time-dependent) problem
  type = Transient
  
  # Solver
  solve_type = NEWTON # Use Newton-Raphson, not PJFNK
  
  # Options for PETSc (how to solve linear equations)
  automatic_scaling = false
  petsc_options = '-snes_converged_reason -ksp_converged_reason' 
  petsc_options_iname = '-pc_type -pc_factor_mat_solver_package -ksp_gmres_restart 
                         -pc_hypre_boomeramg_strong_threshold -pc_hypre_boomeramg_interp_type -pc_hypre_boomeramg_coarsen_type 
                         -pc_hypre_boomeramg_agg_nl -pc_hypre_boomeramg_agg_num_paths -pc_hypre_boomeramg_truncfactor'
  petsc_options_value = 'hypre boomeramg 200 0.7 ext+i PMIS 4 2 0.4'
  
  # Solver tolerances
  l_max_its = 300 
  l_tol = 1e-4 #1e-6
  nl_max_its = 15
  nl_rel_tol = 1e-6
  nl_abs_tol = 1e-6
  nl_forced_its = 1
  line_search = 'bt' # 'none'/'bt' 

  # Time variables
  start_time = 0
  end_time = 1
  dtmin = 1e-10
  dtmax = 0.1

  [./TimeStepper]
    type = IterationAdaptiveDT
    growth_factor = 2
    cutback_factor = 0.5
    linear_iteration_ratio = 1000
    optimal_iterations = 12
    iteration_window = 2
    dt = 0.1
  [../]
[]
# ==================================================
# Define Simulation Output
# ==================================================
[Outputs]
  print_linear_residuals = false
  perf_graph = true
    [./exodus]
    type = Exodus
    file_base = 'output'
    elemental_as_nodal = true
    #sync_times = '0 0.1 1 10'
  [../]
  [./console]
    type = Console
    show = 'dt mCS_xx mCS_yy mCS_zz mTE_xx mTE_yy mTE_zz'
    output_linear = true
    print_mesh_changed_info = true
    max_rows = 5
  [../]
  [./outfile]
    type = CSV
    file_base = 'output'
    delimiter = ','
    time_data = true
    execute_vector_postprocessors_on = timestep_end
  [../]
[]
