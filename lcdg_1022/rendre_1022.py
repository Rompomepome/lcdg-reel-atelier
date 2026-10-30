"""Rend les reels LCDG du 22/10/2026 (9:16 puis carre) et range les livrables dans final/
sous leurs noms habituels.

    python rendre_1022.py vaccins-cabinet arrets-travail-mso"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
DOSSIERS = {"vaccins-cabinet": "2026-10-22-vaccins-cabinet", "arrets-travail-mso": "2026-10-22-arrets-travail-mso",
            "cumul-emploi-retraite": "2026-10-22-cumul-emploi-retraite",
            "arrets-travail-mso-pub": "2026-10-22-arrets-travail-mso-pub",
            "vaccins-cabinet-pub": "2026-10-22-vaccins-cabinet-pub",
            "cumul-emploi-retraite-pub": "2026-10-22-cumul-emploi-retraite-pub"}

for nom in sys.argv[1:]:
    ep_dir = R / "episodes" / DOSSIERS[nom]
    for script in ("render.py", "render_carre.py"):
        print(f"== {nom} : {script}", flush=True)
        r = subprocess.run([sys.executable, f"scripts/{script}", str(ep_dir.relative_to(R))], cwd=R,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        lignes = (r.stdout + r.stderr).strip().splitlines()
        print("\n".join(l for l in lignes if "OK" in l or "[!]" in l or "conforme" in l or "Traceback" in l
                        or "Error" in l)[-1500:], flush=True)
        if r.returncode:
            print("\n".join(lignes[-15:]))
            sys.exit(f"[!] {nom} : {script} a echoue")
    slug = json.loads((ep_dir / "script.json").read_text(encoding="utf-8"))["slug"]
    final = ep_dir / "final"
    final.mkdir(exist_ok=True)
    for src, dst in {f"reel_{slug}.mp4": f"reel_{slug}_9x16.mp4", f"reel_{slug}_carre.mp4": f"reel_{slug}_1x1.mp4",
                     f"couverture_{slug}.jpg": f"couverture_{slug}_9x16.jpg",
                     f"couverture_{slug}_4x5.jpg": f"couverture_{slug}_4x5.jpg",
                     f"couverture_{slug}_carre.jpg": f"couverture_{slug}_1x1.jpg"}.items():
        shutil.copyfile(ep_dir / src, final / dst)
    print(f"{nom} : livrables dans {final}", flush=True)
print("FINI", flush=True)
