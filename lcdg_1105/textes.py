"""Imprime, reel par reel, ce qu'on lit à l'écran et ce qu'on entend : le texte à valider avant la voix.

    python textes.py"""
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
for slug in ("soins-pharmacien", "cotisation-ordre", "premieres-installations"):
    s = json.loads((EP / f"2026-11-04-{slug}" / "script.json").read_text(encoding="utf-8"))
    print(f"\n=== {s['label']} ({s['voix_off']}) ; couverture : {s['sous_titre'].replace('*', '')}")
    for k, b in enumerate(s["blocs"]):
        if k == 0:
            continue
        ecran = b.get("texte") or f"{b.get('prefixe', '')}{b.get('valeur', '')}{b.get('suffixe', '')} {b.get('legende', '')}"
        voix = re.sub(r"\[[a-z-]+\]\s*", "", b.get("voix") or "")
        print(f"B{k} ECRAN : {ecran.replace('*', '').replace(' | ', ' / ')}")
        print(f"B{k} VOIX  : {voix.replace(' | ', ' ')}")
