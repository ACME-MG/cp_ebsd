
BEGIN SCULPT
    
    # Dimensions
    nelx = 5
    nely = 88
    nelz = 113

    # Mesh Improvement
    smooth = 2
    defeature = 1
    remove_bad = 0.0

    # Remove cuts if any
    void_mat = 100000
    
    # Solver
    laplacian_iters = 10
    max_opt_iters = 100
    # adapt_type = 5
    # adapt_levels = 2
    
    # Output
    input_spn = ./results/221230123017/voxellation.spn
    exodus_file = ./results/221230123017/mesh.e

END SCULPT
