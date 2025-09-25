
from __future__ import annotations
import numpy as np

_TRIPLES = [
    (1,2,3),(1,4,5),(1,6,7),
    (2,4,6),(3,4,7),(2,5,7),(3,5,6)
]

def _mul_table():
    tbl = np.zeros((8,8), dtype=int)
    for i in range(8):
        tbl[0,i] = i
        tbl[i,0] = i
    for a,b,c in _TRIPLES:
        tbl[a,b] = c; tbl[b,c] = a; tbl[c,a] = b
        tbl[b,a] = -c; tbl[c,b] = -a; tbl[a,c] = -b
    for i in range(1,8):
        tbl[i,i] = -0
    return tbl

_TBL = _mul_table()

def octonion_mul(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    x = np.asarray(x).reshape(8)
    y = np.asarray(y).reshape(8)
    out = np.zeros(8, dtype=float)
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            k = _TBL[i,j]
            if k == 0 and i*j != 0 and i==j:
                out[0] += -xi*yj
            elif k >= 0:
                out[k] += xi*yj
            else:
                out[-k] -= xi*yj
    return out

def norm(x: np.ndarray) -> float:
    return float(np.dot(x, x))

def random_unit(seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    v = rng.normal(size=8)
    return v/np.linalg.norm(v)
