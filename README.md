# A003558 Universal Clock — Brain ↔ Cosmos

A scientific code repository to test whether **A003558** (the multiplicative order of 2 modulo odd moduli) can act as a **critical staircase / universal clock** across domains:
- Discrete dynamics (back–front permutation ↔ order of 2 mod (2n−1))
- Neural rhythms & information-capacity staircases (2^n horizons)
- Cosmology (phase transitions at 2^n horizons; prime-power spikes)
- **Octonionic connections** embedded in an **octahedral / Fano**-style matrix for cross-domain coupling

## Structure
```
A003558-universal-clock/
├─ pyproject.toml
├─ README.md
├─ src/a003558/
│  ├─ __init__.py
│  ├─ number_theory.py          # A003558, horizons, back-front cycles
│  ├─ horizons.py               # 2^n staircases, constraints, analytics
│  ├─ brain.py                  # toy brain model: Quenneau→2^n abstraction
│  ├─ cosmos.py                 # toy cosmology: phase transitions & horizons
│  ├─ octonions.py              # Cayley algebra; Fano-plane structure constants
│  ├─ octahedral_matrix.py      # octahedral adjacency & embeddings
│  └─ coupling.py               # octonionic coupling of brain/cosmos clocks
├─ tests/
│  ├─ test_number_theory.py
│  ├─ test_horizons.py
│  ├─ test_octonions.py
│  └─ test_coupling.py
├─ examples/
│  ├─ demo_staircase.py
│  ├─ demo_prime_power_spikes.py
│  └─ demo_octonion_coupling.py
├─ notebooks/
│  └─ exploration.ipynb         # (placeholder)
├─ data/                         # (placeholder)
└─ .github/workflows/pytest.yml  # CI
```

## Install
```bash
pip install -e .
pytest -q
```

## Scientific Questions encoded as tests
1. **Horizon bound:** if `L = ord_{2n-1}(2)` then `n <= 2^(L-1)`.
2. **Prime-power spikes:** for `m = p^k`, often `ord_m(2) = φ(m)` (maximal orbit) unless Wieferich obstructions.
3. **Back–front cycles:** length equals `ord_{2n-1}(2)` exactly.
4. **Brain toy-model:** Quenneau-like “spin” patterns coarse-grain to dyadic capacity steps (2^n), minimizing loss.
5. **Cosmos toy-model:** phase transition triggers when dyadic horizon is crossed; spikes align with prime-powers.
6. **Octonionic coupling:** alternativity holds; norm multiplicativity (`||xy||=||x||||y||`) numerically; coupling maps clocks.

See `examples/` for quick plots and `tests/` for the formal criteria.
