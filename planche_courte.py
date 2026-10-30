"""Planche de presélection : 3 images (debut, milieu, fin) de chaque candidat, lues directement
dans le fichier Pexels distant, avec le titre de la page.

    python planche_courte.py <dossier candidats> <sortie.jpg> <fichier:Cn> [...]"""
import json
import subprocess
import sys
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TW, TH = 300, 300
dossier, sortie, codes = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
police = ImageFont.truetype("arial.ttf", 16)


def image(lien, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", lien, "-frames:v", "1",
                        "-vf", "scale=600:-2", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True, timeout=180)
    if not r.stdout:
        return None
    im = Image.open(BytesIO(r.stdout)).convert("RGB")
    im.thumbnail((TW, TH))
    return im


feuille = Image.new("RGB", (3 * (TW + 4) + 20, len(codes) * (TH + 30) + 10), (240, 240, 244))
d = ImageDraw.Draw(feuille)
for i, code in enumerate(codes):
    fichier, c = code.split(":")
    cand = json.loads((dossier / f"{fichier}.json").read_text(encoding="utf-8"))[int(c[1:]) - 1]
    y = 10 + i * (TH + 30)
    titre = cand["url_page"].rstrip("/").split("/")[-1][:70]
    d.text((10, y), f"{code}  {cand['duree']}s  {titre}", font=police, fill=(0, 0, 0))
    duree = float(cand["duree"])
    for k, t in enumerate((1.0, duree / 2, max(1.0, duree - 1.5))):
        im = image(cand["lien"], t)
        if im:
            feuille.paste(im, (10 + k * (TW + 4), y + 24))
    print(code, titre, flush=True)
feuille.save(sortie, quality=85)
print(sortie)
