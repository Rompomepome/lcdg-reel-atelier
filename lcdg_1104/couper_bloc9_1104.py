"""Une seule fois, le 04/11/2026 : le bloc 9 du reel pharmacien est retiré. La narration découpée par pub.py
(aucun crédit) passe dans le cache du reel complet, et le registre des plans suit les nouveaux numéros."""
import json
import shutil
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from lcdg import voix

EP = R / "episodes" / "2026-11-04-soins-pharmacien"
PUB = R / "episodes" / "2026-11-04-soins-pharmacien-pub"
ep = json.loads((EP / "script.json").read_text(encoding="utf-8"))
vx = voix.choix(ep)
_, m = voix.textes(ep)
texte = " ".join(t for t, _ in m)
mp3, js = voix.chemins(texte, vx["id"], EP / "voix", vx.get("modele"), vx.get("reglages"))
src_mp3, src_js = voix.chemins(texte, vx["id"], PUB / "voix", vx.get("modele"), vx.get("reglages"))
if not (src_mp3.exists() and src_js.exists()):
    raise SystemExit(f"[!] narration découpée absente : {src_mp3}")
shutil.copyfile(src_mp3, mp3)
shutil.copyfile(src_js, js)
print("narration du reel complet :", mp3.name, f"{len(json.loads(js.read_text(encoding='utf-8'))['characters'])} caractères")

reg_f = R / "episodes" / "plans_utilises.json"
reg = json.loads(reg_f.read_text(encoding="utf-8"))
nom = EP.name
reg.pop(f"{nom}/9", None)
for vieux, neuf in ((10, 9), (11, 10)):
    if f"{nom}/{vieux}" in reg:
        reg[f"{nom}/{neuf}"] = reg.pop(f"{nom}/{vieux}")
reg_f.write_text(json.dumps(dict(sorted(reg.items())), ensure_ascii=False, indent=1), encoding="utf-8")
(EP / "broll" / "B9.mp4").unlink(missing_ok=True)
print("registre à jour")
