""""
VSH_tau_sat = 12                # VoceSlipHardening
VSH_b       = 66.6666666667     # VoceSlipHardening
VSH_tau_0   = 40                # VoceSlipHardening
AI_gamma0   = 9.55470706737e-08 # PowerLawSlipRule
AI_n        = 12                # PowerLawSlipRule
"""

#%%

import pandas as pd
import numpy as np

param_range = np.array(
    [
        [10, 12],   # tau_sat
        [50, 100],   # b
        [20, 60],   # tau_0
        [9e-8, 9e8], # gamma0
        [10, 12]    # n
    ])  # range


# %%
