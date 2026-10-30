"""Reel minimum de patients (16/10/2026) : Romain garde la lecture mais retire « Pardon ?! » du
debut. Plutot que de relire le bloc 1 (nouvelle prise, autre intonation), on coupe ce passage
dans la narration validee : le son commence au blanc qui precede « La Cour des comptes », avec
la meme avance que la prise d'origine, et l'horodatage est decale d'autant. Le resultat entre
dans le cache de voix.py sous la cle du nouveau texte : render.py le reprend sans appel.

    python couper_pardon.py            (apres avoir retire « [shocked] Pardon ?! » du script)"""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from config import charte as C
from lcdg import binaires as B, voix

E = R / "episodes" / "2026-10-13-minimum-patients"
RETIRE = "[shocked] Pardon ?! "
TAUX = 44100
FONDU = 0.01                       # s : entree du son, contre un clic


def pcm(f):
    r = subprocess.run([B.FFMPEG, "-v", "error", "-i", str(f), "-f", "f32le", "-ac", "1", "-ar", str(TAUX), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype="<f4").copy()


ep = json.loads((E / "script.json").read_text(encoding="utf-8"))
v = voix.choix(ep)
_, morceaux = voix.textes(ep)
neuf = " ".join(t for t, _ in morceaux)
vieux = RETIRE + neuf
dossier = E / "voix"
mp3_v, js_v = voix.chemins(vieux, v["id"], dossier, v.get("modele"), v.get("reglages"))
mp3_n, js_n = voix.chemins(neuf, v["id"], dossier, v.get("modele"), v.get("reglages"))
if not (mp3_v.exists() and js_v.exists()):
    raise SystemExit("[!] narration avec « Pardon » absente du cache : le script a-t-il change ailleurs ?")
al = json.loads(js_v.read_text(encoding="utf-8"))
assert "".join(al["characters"]) == vieux
deb, fin = al["character_start_times_seconds"], al["character_end_times_seconds"]
k = len(RETIRE)                                     # premier caractere garde : « [ » de [incredulous]
dernier_retire = RETIRE.rindex("!")                 # le « ! » de « Pardon ?! »
premier_garde = neuf.index("La Cour") + k           # le « L » de « La Cour »
avance = deb[RETIRE.index("P")]                     # blanc d'entree de la prise d'origine
fin_pardon, debut_la = fin[dernier_retire], deb[premier_garde]
son = pcm(mp3_v)
# coupe au point le plus calme du blanc, sans laisser plus d'avance que la prise d'origine
a, b = fin_pardon + C.VOIX_RACCORD_GARDE, debut_la - C.VOIX_RACCORD_GARDE
n = int(C.VOIX_RACCORD_PAS * TAUX)
i0, i1 = int(a * TAUX), int(b * TAUX)
if i1 - i0 < 2 * n:
    raise SystemExit(f"[!] pas de blanc entre « Pardon ?! » ({fin_pardon:.2f} s) et « La » ({debut_la:.2f} s)")
fen = son[i0:i1 - (i1 - i0) % n].reshape(-1, n)
energie = 10 * np.log10((fen ** 2).mean(axis=1) + 1e-12)
coupe = max(debut_la - avance, (i0 + int(np.argmin(energie)) * n) / TAUX)
print(f"« Pardon ?! » finit a {fin_pardon:.2f} s, « La » commence a {debut_la:.2f} s ; "
      f"coupe a {coupe:.3f} s (avance d'origine {avance:.2f} s) ; blanc le plus calme {energie.min():.1f} dB, "
      f"niveau a la coupe {energie[min(len(energie) - 1, max(0, int((coupe * TAUX - i0) // n)))]:.1f} dB")
reste = son[int(round(coupe * TAUX)):].copy()
f = int(FONDU * TAUX)
reste[:f] *= np.linspace(0, 1, f, dtype=np.float32)
garde = range(k, len(vieux))
nouveau = {"characters": [al["characters"][i] for i in garde],
           "character_start_times_seconds": [round(max(0.0, deb[i] - coupe), 4) for i in garde],
           "character_end_times_seconds": [round(max(0.0, fin[i] - coupe), 4) for i in garde]}
assert "".join(nouveau["characters"]) == neuf
tmp_mp3, tmp_js = mp3_n.with_name(mp3_n.stem + ".tmp.mp3"), js_n.with_name(js_n.stem + ".tmp.json")
r = subprocess.run([B.FFMPEG, "-v", "error", "-f", "f32le", "-ar", str(TAUX), "-ac", "1", "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "192k", "-f", "mp3", str(tmp_mp3), "-y"],
                   input=reste.astype("<f4").tobytes(), capture_output=True)
if r.returncode:
    raise SystemExit(r.stderr.decode("utf-8", "replace")[-600:])
tmp_js.write_text(json.dumps(nouveau, ensure_ascii=False), encoding="utf-8")
os.replace(tmp_mp3, mp3_n)
os.replace(tmp_js, js_n)
print(f"narration : {len(son) / TAUX:.2f} s -> {len(reste) / TAUX:.2f} s, en cache sous {mp3_n.name}")
