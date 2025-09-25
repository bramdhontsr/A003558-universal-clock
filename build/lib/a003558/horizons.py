
from __future__ import annotations
import math

def staircase_level(n: int) -> int:
    """Dyadic staircase level: k such that 2^{k-1} < = n <= 2^k (returns k = 1+ceil(log2 n))."""
    if n <= 0:
        raise ValueError("n must be positive")
    return 1 + math.ceil(math.log2(n))

def horizon_bound(n: int, L: int) -> bool:
    """
    Horizon condition: if L = ord_{2n-1}(2) then n <= 2^{L-1},
    equivalently: L >= 1 + ceil(log2 n).
    """
    return L >= 1 + math.ceil(math.log2(n))
