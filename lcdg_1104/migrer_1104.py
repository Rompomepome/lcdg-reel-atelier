"""Une seule fois, le 04/11/2026 : des blocs ont été retirés des scripts après la relecture. Les plans
téléchargés, les planches de candidats et le registre des plans suivent les nouveaux numéros de blocs.
Rien n'est perdu sauf le premier candidat automatique d'un bloc retiré (retiré aussi du registre)."""
import json
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
# dossier : {ancien numéro de bloc : nouveau numéro} ; un bloc absent est retiré
PLANS = {
    "2026-11-04-soins-pharmacien": {0: 0, 1: 1, 2: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11},
    "2026-11-04-cotisation-ordre": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 6: 5, 7: 6, 8: 7, 9: 8},
    "2026-11-04-premieres-installations": {0: 0, 1: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9},
}
reg_f = R / "plans_utilises.json"
reg = json.loads(reg_f.read_text(encoding="utf-8"))
for ep, plan in PLANS.items():
    d = R / ep / "broll"
    nb_ancien = max(max(plan), 13) + 1
    # 1. les fichiers : d'abord sous un nom provisoire, puis sous le nouveau (les numéros se chevauchent)
    for vieux in range(nb_ancien):
        (d / f"B{vieux}.jpg").unlink(missing_ok=True)
        src = d / f"B{vieux}.mp4"
        if src.exists():
            if vieux in plan:
                src.rename(d / f"tmp_{plan[vieux]}.mp4")
            else:
                src.unlink()
        for ext in ("json", "jpg"):
            c = d / "candidats" / f"{vieux}.{ext}"
            if c.exists():
                if vieux in plan:
                    c.rename(d / "candidats" / f"tmp_{plan[vieux]}.{ext}")
                else:
                    c.unlink()
    for f in d.glob("tmp_*.mp4"):
        f.rename(d / f"B{f.stem[4:]}.mp4")
    for f in (d / "candidats").glob("tmp_*.*"):
        f.rename(d / "candidats" / f"{f.stem[4:]}{f.suffix}")
    # 2. le registre
    anciennes = {k: v for k, v in reg.items() if k.startswith(ep + "/")}
    for k in anciennes:
        del reg[k]
    for k, v in anciennes.items():
        vieux = int(k.split("/")[1])
        if vieux in plan:
            reg[f"{ep}/{plan[vieux]}"] = v
    print(ep, sorted(p.name for p in d.glob("B*.mp4")), sorted(p.name for p in (d / "candidats").glob("*.jpg")))
reg_f.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
