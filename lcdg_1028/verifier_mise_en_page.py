"""Contrôle de mise en page sans rendu (quelques secondes) : montage.verifier sur le script, en 9:16
ou en carré (charte.CARRE appliquée avant d'importer lcdg, comme render_carre.py).

    python verifier_mise_en_page.py episodes/<dossier> [--carre]"""
import json
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from config import charte as C

if "--carre" in sys.argv:
    for cle, valeur in C.CARRE.items():
        setattr(C, cle, valeur)
from lcdg import montage

ep = json.loads((R / sys.argv[1] / "script.json").read_text(encoding="utf-8"))
montage.verifier(ep)
print(f"{Path(sys.argv[1]).name} {'carré' if '--carre' in sys.argv else '9:16'} : mise en page conforme")
