"""Les illustrations animées des reels (lcdg-reel/lcdg/inserts.py), dessinées à leur état final sur fond transparent,
pour servir d'image fixe dans un carrousel. Même mécanique que lcdg-reel/scripts/proto_inserts.py."""
import sys
from pathlib import Path

from PIL import Image

MOTEUR = Path(__file__).resolve().parents[2] / "lcdg-reel"
if not MOTEUR.exists():
    MOTEUR = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(MOTEUR))
from config import charte as C  # noqa: E402
from lcdg import inserts as I  # noqa: E402


class _Part:
    def __init__(self, debut):
        self.debut = debut

    def _sortie(self, t):
        return 0.0


class _Scene:
    def __init__(self, temps):
        self.debut, self.fin = temps[0], temps[-1] + 10
        self.parts = [_Part(x) for x in temps]


def illustration(specs, bas=1500, temps=(0, 3, 6, 9, 12), rubrique="pro"):
    """L'insert (ou la liste d'inserts) à son état final, recadré au plus juste, en RGBA."""
    specs = [specs] if isinstance(specs, dict) else specs
    scene = _Scene(list(temps))
    objs, premier = [], None
    for sp in specs:
        o = I.TYPES[sp["type"]](rubrique, sp, scene, bas - C.INSERT_ECART)
        if sp.get("sur") and premier is not None:
            o.x = premier.x + (premier.w - o.w) / 2
            o.y = premier.y + (premier.h - o.h) / 2
        premier = premier or o
        objs.append(o)
    im = Image.new("RGBA", (C.LARGEUR, C.HAUTEUR), (0, 0, 0, 0))
    for o in objs:
        o.dessiner(im, 0, final=True)
    return im.crop(im.getbbox())
