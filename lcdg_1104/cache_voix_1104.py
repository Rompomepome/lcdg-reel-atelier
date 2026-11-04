"""Vérifie, sans appeler ElevenLabs, que la narration de chaque épisode est déjà dans le cache (aucun crédit)."""
import json
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from lcdg import voix

for nom in sys.argv[1:]:
    d = R / "episodes" / nom
    ep = json.loads((d / "script.json").read_text(encoding="utf-8"))
    vx = voix.choix(ep)
    _, m = voix.textes(ep)
    mp3, js = voix.chemins(" ".join(t for t, _ in m), vx["id"], d / "voix", vx.get("modele"), vx.get("reglages"))
    print(nom, "en cache" if mp3.exists() and js.exists() else "ABSENTE : serait regénérée et payée")
