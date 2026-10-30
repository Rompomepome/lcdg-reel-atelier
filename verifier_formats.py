"""Contrôle de mise en page d'épisodes en 9:16 ET en carré, sans rien rendre.

    python verifier_formats.py episodes/<dossier> [...]

montage.verifier refuse un texte ou un insert qui ne tient pas, avant tout encodage ; le
carré applique charte.CARRE avant l'import de lcdg (comme scripts/render_carre.py), d'où un
sous-processus par format."""
import subprocess
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
CODE = r'''
import json, sys
sys.path.insert(0, r"{R}")
from config import charte as C
if {carre}:
    for cle, valeur in C.CARRE.items():
        setattr(C, cle, valeur)
from lcdg import montage
ep = json.loads(open(r"{script}", encoding="utf-8").read())
montage.verifier(ep)
print("OK")
'''

ok = True
for dossier in sys.argv[1:]:
    script = (R / dossier / "script.json").resolve()
    for nom, carre in (("9:16", False), ("carre", True)):
        r = subprocess.run([sys.executable, "-c", CODE.format(R=R, carre=carre, script=script)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=R)
        sortie = (r.stdout + r.stderr).strip().splitlines()
        if r.returncode:
            print(f"{Path(dossier).name:34} {nom:6}\n    " + "\n    ".join(sortie[-6:]))
        else:
            print(f"{Path(dossier).name:34} {nom:6} {sortie[-1] if sortie else '?'}")
        ok &= r.returncode == 0
sys.exit(0 if ok else 1)
