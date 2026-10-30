"""À lancer après la recharge ElevenLabs (27/10/2026, 23 h 59) : voix et rendu des reels vaccins
et cumul emploi-retraite, leurs versions publicité, puis le kit de publication.

Vérifie d'abord le solde de crédits : rien n'est généré s'il ne couvre pas les deux narrations
(environ 0,22 crédit par caractère, mesuré sur les narrations du 22 et du 23/10).

    python nuit_1027.py            (journal dans nuit_1027.log)"""
import json
import os
import subprocess
import sys
from pathlib import Path

import requests

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
A = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
from lcdg import voix

REELS = [("vaccins-cabinet", "2026-10-22-vaccins-cabinet"), ("cumul-emploi-retraite", "2026-10-22-cumul-emploi-retraite")]


def lancer(*cmd, cwd=A):
    print(f"\n>>> {' '.join(cmd)}", flush=True)
    r = subprocess.run([sys.executable, *cmd], cwd=cwd)
    if r.returncode:
        sys.exit(f"[!] échec : {' '.join(cmd)}")


for l in (R / ".env").read_text(encoding="utf-8").splitlines():
    if l.startswith("ELEVENLABS_API_KEY="):
        os.environ["ELEVENLABS_API_KEY"] = l.split("=", 1)[1].strip().strip('"')
j = requests.get("https://api.elevenlabs.io/v1/user/subscription",
                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}, timeout=30).json()
reste = j["character_limit"] - j["character_count"]
besoin = 0
for _, dossier in REELS:
    ep = json.loads((R / "episodes" / dossier / "script.json").read_text(encoding="utf-8"))
    besoin += len(" ".join(t for t, _ in voix.textes(ep)[1]))
besoin = int(besoin * 0.25)                       # marge sur les 0,22 crédit par caractère mesurés
print(f"crédits : {reste} restants, environ {besoin} nécessaires", flush=True)
if reste < besoin:
    sys.exit("[!] crédits insuffisants : la recharge n'est pas encore passée, rien n'est généré")

for nom, _ in REELS:
    lancer("rendre_1022.py", nom)
    lancer("pub_1022.py", nom)
    lancer("rendre_1022.py", f"{nom}-pub")
lancer("kit_publication.py", cwd=A.parent)
print("\nTOUT EST PRÊT", flush=True)
