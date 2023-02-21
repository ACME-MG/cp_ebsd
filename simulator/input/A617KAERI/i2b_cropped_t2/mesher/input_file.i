
BEGIN SCULPT
    
    # Dimensions
    nelx = 2
    nely = 44
    nelz = 57

    # Mesh Improvement
    smooth = 2
    defeature = 1
    pillow_curves = true
    pillow_boundaries = true
    pillow_curve_layers = 3
    opt_threshold = 0.8
    micro_shave = true

    # Remove cuts if any
    void_mat = 100000
    
    # Solver
    laplacian_iters = 5
    max_opt_iters = 100
    # adapt_type = 5
    # adapt_levels = 1
    
    # Output
    input_spn = ./results/230215124252/voxellation.spn
    exodus_file = ./results/230215124252/mesh.e

END SCULPT
