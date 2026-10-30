"""Aperçus sans voix des reels du 28/10 (aucun crédit ElevenLabs) : copie de l'épisode dans
episodes/_apercu-<slug>, champs "voix" retirés (la durée de chaque plan vient alors de "duree"),
puis render.py en 9:16 (et render_carre.py avec --carre). Les dossiers _apercu-* ne se commitent pas.

    python apercus_1028.py [juniors] [ipa] [--carre]"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
EPISODES = {"juniors": "2026-10-28-docteurs-juniors", "ipa": "2026-10-28-acces-direct-ipa"}
carre = "--carre" in sys.argv
noms = [a for a in sys.argv[1:] if not a.startswith("--")] or list(EPISODES)

for nom in noms:
    src = R / "episodes" / EPISODES[nom]
    ep = json.loads((src / "script.json").read_text(encoding="utf-8"))
    slug = "apercu-" + ep["slug"]
    dst = R / "episodes" / f"_{slug}"
    (dst / "broll").mkdir(parents=True, exist_ok=True)
    for b in ep["blocs"]:
        b.pop("voix", None)
        shutil.copyfile(src / "broll" / b["fichier"], dst / "broll" / b["fichier"])
    ep["slug"] = slug
    (dst / "script.json").write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for script in ["render.py"] + (["render_carre.py"] if carre else []):
        r = subprocess.run([sys.executable, f"scripts/{script}", str(dst)], cwd=R)
        print(f"{nom} {script} : {'OK' if r.returncode == 0 else 'ECHEC'}", flush=True)
