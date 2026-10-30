"""Version publicité des reels du 28/10/2026, découpée dans le reel complet (copie de
lcdg_1022/pub_1022.py, avec les blocs gardés du jour).

Les blocs gardés reprennent texte, plan et animation du reel complet. La narration n'est pas
relue : elle est découpée dans celle du reel complet, dans les silences entre les phrases (même
prise, même intonation, aucun crédit ElevenLabs), puis entre dans le cache de voix.py sous la
clé du texte de la publicité : render.py la reprend comme une narration ordinaire.

    python pub_1028.py docteurs-juniors      (rendre d'abord le reel complet)

Méthode reprise de version_pub.py (reel « minimum de patients », 16/10/2026)."""
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

TAUX = 44100
FONDU = 0.01
# blocs du reel complet gardés dans la publicité (le bloc 0, la couverture, en tête)
PUBS = {
    # le risque, d'un bout à l'autre (42 s) : l'arrivée et sa propre carte CPS -> votre carte, une
    # fraude -> il consulte seul sous votre responsabilité, votre assurance ? -> avant son arrivée. Le
    # bloc de l'indemnité (13 s) commence par « Mais », qui répond aux tickets modérateurs : il reste
    # dans le reel complet. La pastille nomme le public (« Maîtres de stage »)
    "docteurs-juniors": ("2026-10-28-docteurs-juniors", [0, 1, 2, 8, 9]),
    # vos patients chez un IPA de CPTS sans passer par vous -> un antihypertenseur sans diagnostic
    # médical préalable -> comptes rendus, patients à reprendre, aucune rémunération -> avant le 1er
    # décembre
    "acces-direct-ipa": ("2026-10-28-acces-direct-ipa", [0, 1, 3, 5, 9]),
}

nom = sys.argv[1]
dossier, garder, *autres = PUBS[nom]
SRC = R / "episodes" / dossier
DST = R / "episodes" / f"{dossier}-pub"


def pcm(f):
    r = subprocess.run([B.FFMPEG, "-v", "error", "-i", str(f), "-f", "f32le", "-ac", "1", "-ar", str(TAUX), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype="<f4").copy()


# ---------------------------------------------------------------- script de la publicité
ep = json.loads((SRC / "script.json").read_text(encoding="utf-8"))
b = ep["blocs"]
pub = {k: v for k, v in ep.items() if k != "blocs"}
pub["slug"] = f"{ep['slug']}-pub"
pub.update(autres[0] if autres else {})          # champs propres à la publicité (pastille...)
blocs = []
(DST / "broll").mkdir(parents=True, exist_ok=True)
for k, src in enumerate(garder):
    bl = json.loads(json.dumps(b[src]))
    bl.pop("temps", None)
    bl["fichier"] = f"B{k}.mp4"
    shutil.copyfile(SRC / "broll" / b[src]["fichier"], DST / "broll" / bl["fichier"])
    blocs.append(bl)
pub["blocs"] = blocs
(DST / "script.json").write_text(json.dumps(pub, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- narration découpée
vx = voix.choix(ep)
_, m_src = voix.textes(ep)
tv = [t for t, _ in m_src]                       # tv[i] : texte lu du bloc i + 1
texte_src = " ".join(tv)
mp3_s, js_s = voix.chemins(texte_src, vx["id"], SRC / "voix", vx.get("modele"), vx.get("reglages"))
if not (mp3_s.exists() and js_s.exists()):
    raise SystemExit("[!] narration du reel complet absente du cache : rends-le d'abord")
al = json.loads(js_s.read_text(encoding="utf-8"))
assert "".join(al["characters"]) == texte_src
deb, fin = al["character_start_times_seconds"], al["character_end_times_seconds"]
son = pcm(mp3_s)
pos, p = [], 0
for t in tv:
    pos.append(p)
    p += len(t) + 1


def lettres(a, z):
    """Premier et dernier caractère alphanumérique de [a, z) hors indications de jeu."""
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
    """Raccord entre le texte qui finit à fin_texte (exclu) et celui qui commence à debut_texte."""
    _, der = lettres(max(0, fin_texte - 200), fin_texte)
    pre, _ = lettres(debut_texte, len(texte_src))
    return raccord(fin[der], deb[pre])


# segments : suites de blocs parlants consécutifs, (début, fin exclue) dans le texte du reel
parlants = [k for k in garder if k > 0]
suites = []
for k in parlants:
    if suites and k == suites[-1][-1] + 1:
        suites[-1].append(k)
    else:
        suites.append([k])
segments = [(pos[s[0] - 1], pos[s[-1] - 1] + len(tv[s[-1] - 1])) for s in suites]
bornes = []
for k, (a, z) in enumerate(segments):
    t0 = 0.0 if a == 0 else coupe(a - 1, a)
    t1 = len(son) / TAUX if z == len(texte_src) else coupe(z, z + 1)
    bornes.append((t0, t1))
    print(f"    segment {k} (blocs {suites[k]}) : {t0:6.2f} -> {t1:6.2f} s  « {texte_src[a:z][:60]}… »")

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
print(f"narration de la publicité : {n / TAUX:.2f} s, en cache sous {mp3_p.name}")
print(f"script : {DST / 'script.json'}")
