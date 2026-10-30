"""Recherche Pexels pour plusieurs blocs d'un episode, puis liste des candidats libres
(jamais utilises, pas du meme tournage) avec le titre de leur page Pexels.

    python chercher_plans.py episodes/<dossier> "<bloc>|<requete>|<requete>..." [...]"""
import json
import subprocess
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from lcdg import registre

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

dossier = sys.argv[1]
nom = Path(dossier).name
for spec in sys.argv[2:]:
    bloc, *requetes = spec.split("|")
    r = subprocess.run([sys.executable, "scripts/broll.py", "chercher", dossier, bloc, "--mixte", *requetes],
                       cwd=R, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print(f"== bloc {bloc} : erreur\n{r.stderr[-400:]}")
        continue
    cands = json.loads((R / dossier / "broll" / "candidats" / f"{bloc}.json").read_text(encoding="utf-8"))
    libres = []
    for i, x in enumerate(cands, 1):
        if registre.ids_utilises(sauf=f"{nom}/{bloc}").get(x["id"]) or registre.meme_tournage(x, nom):
            continue
        libres.append(f"C{i} {x['duree']}s {'V' if x['vertical'] else 'P'} "
                      f"{x['url_page'].rstrip('/').split('/')[-1][:60]}")
    print(f"== bloc {bloc} : {len(libres)} libres / {len(cands)}")
    for l in libres:
        print("   ", l)
