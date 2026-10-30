"""Essaie les inserts du 28/10/2026 avec proto_inserts.py : une planche par insert, dans ce dossier.

    python essayer.py [nom ...]"""
import json
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
PROTO = ICI.parent.parent / "proto_inserts.py"
SPECS = json.loads((ICI / "specs.json").read_text(encoding="utf-8"))

for nom in sys.argv[1:] or list(SPECS):
    e = SPECS[nom]
    f = ICI / f"_{nom}.json"
    f.write_text(json.dumps(e["spec"], ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, str(PROTO), str(f), str(ICI / f"{nom}.png"), "--temps", e["temps"],
                        "--instants", e["instants"]], capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    print(f"== {nom}\n{(r.stdout + r.stderr).strip()[-1200:]}")
