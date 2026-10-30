"""Choisit un plan par bloc, y compris un candidat trouve pour un autre bloc du meme episode
(il est recopie dans la liste du bloc), puis telecharge et inscrit au registre (broll.py choisir).

    python choisir_plans.py episodes/<dossier> <bloc>:<bloc source>:C<n> [...]"""
import json
import subprocess
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
dossier = sys.argv[1]
C = R / dossier / "broll" / "candidats"
for spec in sys.argv[2:]:
    bloc, src, code = spec.split(":")
    cand = json.loads((C / f"{src}.json").read_text(encoding="utf-8"))[int(code[1:]) - 1]
    cible = json.loads((C / f"{bloc}.json").read_text(encoding="utf-8")) if (C / f"{bloc}.json").exists() else []
    ids = [c["id"] for c in cible]
    if cand["id"] in ids:
        n = ids.index(cand["id"]) + 1
    else:
        cible.append(cand)
        n = len(cible)
        (C / f"{bloc}.json").write_text(json.dumps(cible, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([sys.executable, "scripts/broll.py", "choisir", dossier, bloc, f"C{n}"], cwd=R,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print((r.stdout + r.stderr).strip().splitlines()[-1])
