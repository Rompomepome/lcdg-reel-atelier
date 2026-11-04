"""Planche de contrôle d'une vidéo : une image toutes les N secondes, en grille, avec l'instant.

    python planche.py <video.mp4> <sortie.jpg> [pas=2.5] [colonnes=8] [largeur=240]"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

video, sortie = sys.argv[1], sys.argv[2]
pas = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 8
larg = int(sys.argv[5]) if len(sys.argv) > 5 else 240
info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height",
                                  "-select_streams", "v:0", "-of", "json", video],
                                 capture_output=True, text=True).stdout)
duree = float(info["format"]["duration"])
w, h = info["streams"][0]["width"], info["streams"][0]["height"]
haut = int(larg * h / w)
images = []
t = 0.5
while t < duree:
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                        "-vf", f"scale={larg}:{haut}", "-f", "image2pipe", "-vcodec", "mjpeg", "-"],
                       capture_output=True)
    if r.stdout:
        Path(sortie).with_suffix(".tmp.jpg").write_bytes(r.stdout)
        im = Image.open(Path(sortie).with_suffix(".tmp.jpg")).convert("RGB")
        ImageDraw.Draw(im).text((5, 5), f"{t:.1f}", fill=(255, 255, 0))
        images.append(im)
    t += pas
Path(sortie).with_suffix(".tmp.jpg").unlink(missing_ok=True)
rangs = (len(images) + cols - 1) // cols
feuille = Image.new("RGB", (cols * (larg + 4), rangs * (haut + 4)), (30, 30, 30))
for i, im in enumerate(images):
    feuille.paste(im, ((i % cols) * (larg + 4), (i // cols) * (haut + 4)))
feuille.save(sortie, quality=88)
print(f"{sortie} : {duree:.1f} s, {len(images)} images, {feuille.size}")
