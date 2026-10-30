"""Planche d'un aperçu : une image par plan, prise juste avant la sortie du texte (l'insert est
alors complet), plus une au milieu du plan. Le reel livré commence au bloc 1 (la couverture est
coupée), d'où le décalage du bloc 0.

    python planche_v3.py <dossier _apercu-...> <sortie.png>"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

dossier, sortie = Path(sys.argv[1]), Path(sys.argv[2])
ep = json.loads((dossier / "script.json").read_text(encoding="utf-8"))
video = dossier / f"reel_{ep['slug']}.mp4"
blocs = ep["blocs"][1:]
t, instants = 0.0, []
for k, b in enumerate(blocs, 1):
    instants += [(k, "milieu", t + b["duree"] * 0.45), (k, "fin", t + b["duree"] - 0.45)]
    t += b["duree"]
L = 270
images = []
for k, quand, ti in instants:
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ti:.2f}", "-i", str(video), "-frames:v", "1",
                        "-vf", f"scale={L}:-1", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True, check=True)
    from io import BytesIO
    images.append((k, quand, ti, Image.open(BytesIO(r.stdout)).convert("RGB")))
h = images[0][3].height
cols = 6
rows = (len(images) + cols - 1) // cols
planche = Image.new("RGB", (cols * (L + 8) + 8, rows * (h + 34) + 8), (240, 240, 244))
d = ImageDraw.Draw(planche)
try:
    f = ImageFont.truetype("arial.ttf", 18)
except OSError:
    f = ImageFont.load_default()
for i, (k, quand, ti, im) in enumerate(images):
    x, y = 8 + (i % cols) * (L + 8), 8 + (i // cols) * (h + 34)
    d.text((x, y), f"B{k} {quand} {ti:.1f}s", fill=(20, 20, 40), font=f)
    planche.paste(im, (x, y + 26))
planche.save(sortie)
print(sortie, planche.size)
