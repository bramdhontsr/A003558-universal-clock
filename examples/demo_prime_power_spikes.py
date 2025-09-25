
import numpy as np, math
import matplotlib.pyplot as plt
from a003558.number_theory import multiplicative_order, phi

N=5000
points = []
for n in range(1,N+1):
    m = 2*n - 1
    L = multiplicative_order(2, m)
    points.append((n, L, m))
points = np.array(points, dtype=object)

plt.figure(figsize=(9,5))
plt.scatter(points[:,0], points[:,1], s=5, alpha=0.5, label='L(n)')
pp_x = []; pp_y = []
for n,L,m in points:
    x = m; p=None; good=True; d=2
    while d*d<=x:
        e=0
        while x%d==0:
            x//=d; e+=1
        if e:
            if p is None: p=d
            else: good=False
        d = 3 if d==2 else d+2
    if x>1:
        if p is None: p=x
        else: good=False
    if good and p and p%2==1:
        pp_x.append(n); pp_y.append(L)
plt.scatter(pp_x, pp_y, s=14, label='prime-power spikes')
plt.legend(); plt.grid(True, ls='--', alpha=0.4)
plt.title("Prime-power spikes where ord ≈ φ(m)")
plt.xlabel("n"); plt.ylabel("L")
plt.show()
