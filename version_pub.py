"""Version publicite (environ 30 s) du reel « minimum de patients » (16/10/2026).

Blocs : 1 (la Cour veut un minimum obligatoire), 2 (500 par medecin traitant), 3 (les 8 553),
puis un bloc qui joint « Rassurez-vous : rien de tout cela ne s'applique aujourd'hui » (bloc 6)
et « Et sous le seuil, que risqueriez-vous ? » (bloc 7), puis l'appel du bloc 9.

La narration n'est pas relue : elle est decoupee dans celle du reel complet, aux silences entre
les phrases (meme prise, meme intonation, aucun credit), et entre dans le cache de voix.py sous
la cle du texte de la publicite : render.py la reprend comme une narration ordinaire.

    python version_pub.py"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from config import charte as C
from lcdg import binaires as B, voix

SRC = R / "episodes" / "2026-10-13-minimum-patients"
DST = R / "episodes" / "2026-10-13-minimum-patients-pub"
TAUX = 44100
FONDU = 0.01
NB, AP = "\u00a0", "\u2019"


def pcm(f):
    r = subprocess.run([B.FFMPEG, "-v", "error", "-i", str(f), "-f", "f32le", "-ac", "1", "-ar", str(TAUX), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype="<f4").copy()


# ---------------------------------------------------------------- script de la publicite
ep = json.loads((SRC / "script.json").read_text(encoding="utf-8"))
b = ep["blocs"]
v6 = b[6]["voix"].split("|")[0].strip()          # « [reassuring] Rassurez-vous : ... aujourd'hui. »
v7 = b[7]["voix"].split("|")[1].strip()          # « [concerned] Et sous le seuil, que risqueriez-vous ? »
assert v6.startswith("[reassuring]") and v7.startswith("[concerned]"), (v6, v7)
pub = {k: v for k, v in ep.items() if k != "blocs"}
pub["slug"] = "minimum-patients-pub"
correspondance = [(0, "B0.mp4"), (1, "B1.mp4"), (2, "B2.mp4"), (3, "B3.mp4"), (6, "B4.mp4"), (9, "B5.mp4")]
blocs = []
for k, (src, fichier) in enumerate(correspondance):
    bl = json.loads(json.dumps(b[src]))
    bl.pop("temps", None)
    bl["fichier"] = fichier
    if src == 6:
        # texte normal : en style « phrase », « risqueriez-vous » surligne sort de la colonne
        bl.pop("type", None)
        bl.update({"texte": f"Rien ne s{AP}applique aujourd{AP}hui. | Et sous le seuil, *que risqueriez-vous*{NB}?",
                   "voix": f"{v6} | {v7}"})
    blocs.append(bl)
pub["blocs"] = blocs
(DST / "broll").mkdir(parents=True, exist_ok=True)
for src, fichier in correspondance:
    shutil.copyfile(SRC / "broll" / b[src]["fichier"], DST / "broll" / fichier)
(DST / "script.json").write_text(json.dumps(pub, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- narration decoupee
vx = voix.choix(ep)
_, m_src = voix.textes(ep)
tv = [t for t, _ in m_src]
texte_src = " ".join(tv)
mp3_s, js_s = voix.chemins(texte_src, vx["id"], SRC / "voix", vx.get("modele"), vx.get("reglages"))
if not (mp3_s.exists() and js_s.exists()):
    raise SystemExit("[!] narration du reel complet absente du cache : rends-le d'abord")
al = json.loads(js_s.read_text(encoding="utf-8"))
assert "".join(al["characters"]) == texte_src
deb, fin = al["character_start_times_seconds"], al["character_end_times_seconds"]
son = pcm(mp3_s)
pos = []
p = 0
for t in tv:
    pos.append(p)
    p += len(t) + 1


def lettres(a, z):
    """Premier et dernier caractere alphanumerique de [a, z) hors indications de jeu."""
    dans, idx = False, []
    for i in range(a, z):
        c = texte_src[i]
        if c == "[":
            dans = True
        elif c == "]":
            dans = False
        elif not dans and c.isalnum():
            idx.append(i)
    return idx[0], idx[-1]


def raccord(fin_a, debut_b):
    """Point le plus calme du blanc entre deux phrases."""
    a, z = fin_a + C.VOIX_RACCORD_GARDE, debut_b - C.VOIX_RACCORD_GARDE
    n = int(C.VOIX_RACCORD_PAS * TAUX)
    i0, i1 = int(a * TAUX), min(int(z * TAUX), len(son))
    if i1 - i0 < 2 * n:
        raise SystemExit(f"[!] pas de blanc entre {fin_a:.2f} s et {debut_b:.2f} s")
    f = son[i0:i1 - (i1 - i0) % n].reshape(-1, n)
    db = 10 * np.log10((f ** 2).mean(axis=1) + 1e-12)
    k = int(np.argmin(db))
    print(f"      raccord dans le blanc {fin_a:.2f}-{debut_b:.2f} s : {(i0 + k * n + n // 2) / TAUX:.2f} s "
          f"({db[k]:.0f} dB)")
    return (i0 + k * n + n // 2) / TAUX


def coupe(fin_texte, debut_texte):
    """Raccord entre le texte qui finit a fin_texte (exclu) et celui qui commence a debut_texte."""
    _, der = lettres(fin_texte - 200 if fin_texte > 200 else 0, fin_texte)
    pre, _ = lettres(debut_texte, len(texte_src))
    return raccord(fin[der], deb[pre])


# segments : (debut, fin exclue) dans le texte du reel complet
s2 = (pos[5], pos[5] + len(v6))
a7 = tv[6].index("[concerned]")
s3 = (pos[6] + a7, pos[6] + a7 + len(v7))
segments = [(pos[0], pos[2] + len(tv[2])), s2, s3, (pos[8], len(texte_src))]
assert texte_src[s2[0]:s2[1]] == v6 and texte_src[s3[0]:s3[1]] == v7
bornes = []
for k, (a, z) in enumerate(segments):
    t0 = 0.0 if a == 0 else coupe(a - 1, a)
    t1 = len(son) / TAUX if z == len(texte_src) else coupe(z, z + 1)
    bornes.append((t0, t1))
    print(f"    segment {k} : {t0:6.2f} -> {t1:6.2f} s  « {texte_src[a:z][:60]}… »")

morceaux, car, debs, fins_, n = [], [], [], [], 0
for k, ((a, z), (t0, t1)) in enumerate(zip(segments, bornes)):
    i0, i1 = int(round(t0 * TAUX)), int(round(t1 * TAUX))
    m = son[i0:i1].copy()
    if k > 0:
        m[:int(FONDU * TAUX)] *= np.linspace(0, 1, int(FONDU * TAUX), dtype=np.float32)
    if k < len(segments) - 1:
        m[-int(FONDU * TAUX):] *= np.linspace(1, 0, int(FONDU * TAUX), dtype=np.float32)
    decal = n / TAUX - i0 / TAUX
    if k > 0:                                       # l'espace entre deux segments : le blanc
        car.append(" ")
        debs.append(fins_[-1])
        fins_.append(max(fins_[-1], deb[a] + decal))
    for q in range(a, z):
        car.append(texte_src[q])
        debs.append(max(0.0, deb[q] + decal))
        fins_.append(max(0.0, fin[q] + decal))
    morceaux.append(m)
    n += len(m)

_, m_pub = voix.textes(pub)
texte_pub = " ".join(t for t, _ in m_pub)
assert "".join(car) == texte_pub, ("".join(car)[:200], texte_pub[:200])
mp3_p, js_p = voix.chemins(texte_pub, vx["id"], DST / "voix", vx.get("modele"), vx.get("reglages"))
mp3_p.parent.mkdir(parents=True, exist_ok=True)
tmp = mp3_p.with_name(mp3_p.stem + ".tmp.mp3")
r = subprocess.run([B.FFMPEG, "-v", "error", "-f", "f32le", "-ar", str(TAUX), "-ac", "1", "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "192k", "-f", "mp3", str(tmp), "-y"],
                   input=np.concatenate(morceaux).astype("<f4").tobytes(), capture_output=True)
if r.returncode:
    raise SystemExit(r.stderr.decode("utf-8", "replace")[-600:])
js_p.write_text(json.dumps({"characters": car,
                            "character_start_times_seconds": [round(x, 4) for x in debs],
                            "character_end_times_seconds": [round(x, 4) for x in fins_]},
                           ensure_ascii=False), encoding="utf-8")
os.replace(tmp, mp3_p)
print(f"narration de la publicite : {n / TAUX:.2f} s, en cache sous {mp3_p.name}")
