"""Nombre de lignes de chaque temps de texte, coupé comme le moteur le coupe (retour à la
ligne à chaque fin de phrase, puis à la largeur de la colonne). Règle du CLAUDE.md : trois
lignes au plus par temps ; montage.verifier ne contrôle que la zone sûre, pas ce nombre.

    python lignes_textes.py episodes/<dossier> [...]"""
import json
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from lcdg import habillage as hb
from lcdg import texte as T

MAX = 3
trop = 0
for dossier in sys.argv[1:]:
    ep = json.loads((R / dossier / "script.json").read_text(encoding="utf-8"))
    print(f"== {Path(dossier).name}")
    for k, b in enumerate(ep["blocs"]):
        if not b.get("texte") or b.get("type") == "chiffre":
            continue
        for i, temps in enumerate(b["texte"].split("|")):
            temps = temps.strip()
            if b.get("type") == "phrase":
                _, n = hb.style_ajuste(temps)
            else:
                st = hb.style_bloc()
                n = len(T.equilibrer(temps, T.mesureur(st), st["largeur"]))
            alerte = "  <-- TROP" if n > MAX else ""
            trop += n > MAX
            print(f"  B{k}.{i}  {n} l.  {temps}{alerte}")
sys.exit(1 if trop else 0)
