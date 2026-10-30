"""Contrôle d'une narration générée, sans l'écouter : débit par bloc, blancs anormaux, et une
indication de jeu prononcée par erreur (un « [ » ou un mot anglais lu dans l'horodatage).

    python controle_voix.py episodes/<dossier>"""
import json
import re
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from lcdg import voix

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = R / sys.argv[1]
ep = json.loads((D / "script.json").read_text(encoding="utf-8"))
_, morceaux = voix.textes(ep)
tv = [t for t, _ in morceaux]
texte = " ".join(tv)
v = voix.choix(ep)
mp3, js = voix.chemins(texte, v["id"], D / "voix", v.get("modele"), v.get("reglages"))
al = json.loads(js.read_text(encoding="utf-8"))
deb, fin = al["character_start_times_seconds"], al["character_end_times_seconds"]
print(f"{mp3.name} : {fin[-1]:.1f} s pour {len(texte)} caractères")


def lisible(i0, i1):
    """Index des caractères lus (hors indications entre crochets) de [i0, i1)."""
    out, dans = [], False
    for i in range(i0, i1):
        c = texte[i]
        if c == "[":
            dans = True
        elif c == "]":
            dans = False
        elif not dans and c.strip():
            out.append(i)
    return out


p = 0
for k, t in enumerate(tv, 1):
    idx = lisible(p, p + len(t))
    a, z = deb[idx[0]], fin[idx[-1]]
    lu = len(re.sub(r"\[[^\]]*\]", "", t))
    print(f"  B{k:<2} {a:6.2f}-{z:6.2f} s  {z - a:5.2f} s  {lu / (z - a):5.1f} car/s")
    p += len(t) + 1
blancs = []
idx = lisible(0, len(texte))
for i, j in zip(idx, idx[1:]):
    g = deb[j] - fin[i]
    if g > 0.9:
        blancs.append((g, texte[max(0, i - 30):i + 1]))
for g, ctx in sorted(blancs, reverse=True)[:6]:
    print(f"  blanc de {g:.2f} s après « …{ctx} »")
# une indication de jeu doit durer presque rien : si elle prend plus de 0,4 s, elle a été lue
for m in re.finditer(r"\[[^\]]*\]", texte):
    d = fin[m.end() - 1] - deb[m.start()]
    if d > 0.4:
        print(f"  [!] indication {m.group()} : {d:.2f} s, peut-être prononcée")
