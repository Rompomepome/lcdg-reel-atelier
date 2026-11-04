"""Une seule fois, le 04/11/2026 : revoix.py sur le reel pharmacien, qui n'est pas encore commité. revoix.py lit
l'ancienne narration dans git ; ici, l'ancien script est le script actuel avec l'ancienne phrase du bloc 4.

    python revoix_1104.py [--essai]"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
EP = R / "episodes" / "2026-11-04-soins-pharmacien"
ANCIENNE = ("Selon l’évaluation citée par la Cour des comptes, dix-neuf pour cent de ses patients ont évité le "
            "recours à un médecin. [warm] Bien encadré, c’est, pour le Cercle, du temps médical rendu.")

spec = importlib.util.spec_from_file_location("revoix", R / "scripts" / "revoix.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def ancien(episode, rev):
    ep = copy.deepcopy(json.loads((EP / "script.json").read_text(encoding="utf-8")))
    ep["blocs"][4]["voix"] = ANCIENNE
    return ep


m._ancien = ancien
sys.argv = ["revoix.py", str(EP.relative_to(R))] + sys.argv[1:]
m.main()
