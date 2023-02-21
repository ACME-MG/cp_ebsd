
BEGIN SCULPT
    
    # Dimensions
    nelx = 5
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
    # adapt_levels = 2
    
    # Output
    input_spn = ./results/230209120525/voxellation.spn
    exodus_file = ./results/230209120525/mesh.e

END SCULPT
