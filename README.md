# A003558 Universal Clock

Visualisatie- en exporttools rond de OEIS-reeks [A003558](https://oeis.org/A003558), met toepassingen in octaëders, kubussen en Blender.

---

## Live Docs
[![Docs](https://github.com/<user>/<repo>/actions/workflows/pages.yml/badge.svg)](https://<user>.github.io/<repo>/)

## Status
[![CI](https://github.com/<user>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<user>/<repo>/actions)

---


**Testbare hypothese:**  
De OEIS-reeks [A003558](https://oeis.org/A003558) wordt onderzocht als een *kritische trapfunctie* voor faseovergangen in informatie-dichtheid.  
Het project koppelt discrete verdubbelingsfractalen (`2^n`) met octonionale algebra en een octahedronale matrix.

---

## 📂 Inhoud
- **`src/a003558/`** — Python-package met number theory, horizons en octonions  
- **`tests/`** — pytest-modules (✅ momenteel 10/10 groen)  
- **`docs/`** — statische website met uitleg, galerij en renders  
- **`pics/`** — voorbeeldrenders vanuit Blender (WebP)  

---

## 🔬 Doel
- Onderzoek naar **A003558** als discrete kosmische klok  
- Visualisatie van horizons (`2^n`) en back-front orbits  
- Toetsen van **octonion-consistentie** binnen een octahedronale matrix  
- Hypothese: zelfde fractale gelijkvormigheid in **brein** en **kosmos**

---

## ▶️ Gebruik
Clone de repo en activeer de virtuele omgeving:

```bash
git clone https://github.com/bramdhontsr/A003558-universal-clock.git
cd A003558-universal-clock
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
pytest -q
