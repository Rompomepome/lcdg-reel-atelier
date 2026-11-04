"""Une rangée d'images d'une vidéo, en grand, aux instants demandés.

    python zooms.py <video.mp4> <sortie.jpg> <largeur> <t1> <t2> ..."""
import subprocess
import sys
from pathlib import Path

from PIL import Image

video, sortie, larg = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
images = []
for t in sys.argv[4:]:
    tmp = sortie.with_suffix(".tmp.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", video, "-frames:v", "1", "-vf", f"scale={larg}:-1",
                    str(tmp), "-y"], check=True)
    images.append(Image.open(tmp).convert("RGB"))
tmp.unlink(missing_ok=True)
w = sum(i.width for i in images) + 6 * (len(images) - 1)
feuille = Image.new("RGB", (w, images[0].height), (30, 30, 30))
x = 0
for i in images:
    feuille.paste(i, (x, 0))
    x += i.width + 6
feuille.save(sortie, quality=90)
print(sortie, feuille.size)
