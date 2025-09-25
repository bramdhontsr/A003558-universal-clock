
import numpy as np
import matplotlib.pyplot as plt
from a003558.number_theory import multiplicative_order

N=1024
n_vals = np.arange(1,N+1)
L_vals = np.array([ multiplicative_order(2, 2*n-1) for n in n_vals ])

plt.figure(figsize=(9,5))
plt.scatter(n_vals, L_vals, s=6, alpha=0.5)
plt.step(n_vals, 1+np.ceil(np.log2(n_vals)), where='post', lw=2, label='horizon lower bound')
plt.title("Back-front cycles and dyadic horizon")
plt.xlabel("n"); plt.ylabel("L")
plt.grid(True, ls='--', alpha=0.4); plt.legend()
plt.show()
