"""Volume de la narration pendant chaque indication de jeu : un blanc (< -40 dB) veut dire
qu'elle n'a pas été prononcée.

    python controle_indications.py episodes/<dossier>"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from lcdg import binaires as B, voix

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = R / sys.argv[1]
ep = json.loads((D / "script.json").read_text(encoding="utf-8"))
texte = " ".join(t for t, _ in voix.textes(ep)[1])
v = voix.choix(ep)
mp3, js = voix.chemins(texte, v["id"], D / "voix", v.get("modele"), v.get("reglages"))
al = json.loads(js.read_text(encoding="utf-8"))
deb, fin = al["character_start_times_seconds"], al["character_end_times_seconds"]
TAUX = 16000
son = np.frombuffer(subprocess.run([B.FFMPEG, "-v", "error", "-i", str(mp3), "-f", "f32le", "-ac", "1", "-ar",
                                    str(TAUX), "-"], capture_output=True, check=True).stdout, dtype="<f4")
ref = 20 * np.log10(np.sqrt((son ** 2).mean()) + 1e-9)
for m in re.finditer(r"\[[^\]]*\]", texte):
    a, z = deb[m.start()], fin[m.end() - 1]
    seg = son[int(a * TAUX):max(int(a * TAUX) + 1, int(z * TAUX))]
    db = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)
    etat = "blanc" if db < ref - 25 else "SON"
    print(f"  {m.group():18} {a:6.2f}-{z:6.2f} s  {db - ref:6.1f} dB / moyenne  {etat}")
