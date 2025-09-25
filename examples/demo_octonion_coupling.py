
import numpy as np
from a003558.coupling import coupled_step

for k1 in range(2,7):
    for k2 in range(2,7):
        err = coupled_step(k1,k2)
        print(f"k_brain={k1:2d}, k_cosmos={k2:2d} -> norm error ~ {err:.2e}")
