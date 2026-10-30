"""Contrôle de prononciation d'une narration, sans l'écouter : la transcription automatique
d'ElevenLabs (Scribe, incluse dans le compte gratuit) est comparée mot à mot au texte lu. Un mot
mal prononcé (« consulpation ») ressort comme une différence.

    python controle_prononciation.py episodes/<dossier>

Les sigles épelés (« C.S.M.F. ») et les nombres en lettres s'écrivent autrement dans une
transcription : ces écarts-là sont normaux, seuls les mots ordinaires comptent."""
import difflib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import requests

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from lcdg import voix

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for l in (R / ".env").read_text(encoding="utf-8").splitlines():
    if l.startswith("ELEVENLABS_API_KEY="):
        os.environ["ELEVENLABS_API_KEY"] = l.split("=", 1)[1].strip().strip('"')

D = R / sys.argv[1]
ep = json.loads((D / "script.json").read_text(encoding="utf-8"))
texte = " ".join(t for t, _ in voix.textes(ep)[1])
v = voix.choix(ep)
mp3, _ = voix.chemins(texte, v["id"], D / "voix", v.get("modele"), v.get("reglages"))
cache = mp3.with_suffix(".transcription.json")
if not cache.exists():
    with open(mp3, "rb") as f:
        r = requests.post("https://api.elevenlabs.io/v1/speech-to-text",
                          headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
                          data={"model_id": "scribe_v1", "language_code": "fra", "tag_audio_events": "false"},
                          files={"file": (mp3.name, f, "audio/mpeg")}, timeout=300)
    if not r.ok:
        raise SystemExit(f"[!] transcription refusée ({r.status_code}) : {r.text[:200]}")
    cache.write_text(json.dumps(r.json(), ensure_ascii=False), encoding="utf-8")
transcrit = json.loads(cache.read_text(encoding="utf-8"))["text"]


def mots(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = unicodedata.normalize("NFKD", s.lower().replace("’", "'"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", s)


attendu, entendu = mots(texte), mots(transcrit)
print(f"{mp3.name} : {len(attendu)} mots attendus, {len(entendu)} transcrits")
ecarts = 0
for op, a0, a1, b0, b1 in difflib.SequenceMatcher(None, attendu, entendu, autojunk=False).get_opcodes():
    if op != "equal":
        ecarts += 1
        contexte = " ".join(attendu[max(0, a0 - 3):a0])
        print(f"  {op:8} attendu « {' '.join(attendu[a0:a1])} »  entendu « {' '.join(entendu[b0:b1])} »"
              f"   (après « {contexte} »)")
print(f"{ecarts} écart(s)")
