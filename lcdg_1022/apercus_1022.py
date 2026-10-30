"""Aperçus sans voix des reels du 22/10 (aucun crédit ElevenLabs) : copie de l'épisode dans
episodes/_apercu-<slug>, champs "voix" retirés (la durée de chaque plan vient alors de
"duree"), puis render.py en 9:16. Les dossiers _apercu-* ne se commitent pas.

    python apercus_1022.py [vaccins] [arrets]"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
EPISODES = {"vaccins": "2026-10-22-vaccins-cabinet", "arrets": "2026-10-22-arrets-travail-mso",
            "cumul": "2026-10-22-cumul-emploi-retraite"}

for nom in sys.argv[1:] or list(EPISODES):
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
    r = subprocess.run([sys.executable, "scripts/render.py", str(dst)], cwd=R)
    print(f"{nom} : {'OK' if r.returncode == 0 else 'ECHEC'} -> {dst / f'reel_{slug}.mp4'}", flush=True)
