"""Fiche de relecture des reels du 13/11/2026 pour Romain : par plan, l'écran et la voix, avant de générer la voix.

    python fiche_textes_1113.py      (écrit textes_1113.md à côté)"""
import json
import re
from pathlib import Path

EP = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
ICI = Path(__file__).resolve().parent
CARS = {"homme_age": 14.1, "femme_agee": 15.8, "femme_jeune": 14.6}
VOIX = {"homme_age": "Guillaume (homme, posé)", "femme_agee": "Emilie (femme, sérieuse)",
        "femme_jeune": "Jeanne (femme, plus jeune et punchy)"}
JEU = {"curious": "curieuse", "matter-of-fact": "factuelle", "surprised": "surprise", "incredulous": "incrédule",
       "serious": "grave", "concerned": "préoccupée", "thoughtful": "posée", "warm": "chaleureuse"}


def ecran(t):
    return " / ".join(s.strip() for s in t.replace("*", "").replace("\u00a0", " ").split("|"))


def lu(v):
    return re.sub(r"\[[a-z-]+\]\s*", "", v).replace(" | ", " ").replace("|", "")


def jeu(v):
    """Les indications de jeu d'un plan, en français, dans l'ordre."""
    return ", puis ".join(JEU.get(x, x) for x in re.findall(r"\[([a-z-]+)\]", v)) or "neutre"


def animation(b):
    ins = b.get("insert")
    if b.get("type") in ("chiffre", "phrase"):
        return {"chiffre": "chiffre clé qui défile", "phrase": "phrase forte, en grand"}[b["type"]]
    return " + ".join(i["type"] for i in (ins if isinstance(ins, list) else [ins])) if ins else "aucune"


lignes = ["# Reels du 13/11/2026 : textes à valider avant la voix", ""]
for nom in ("2026-11-10-maladie-pro-tableau-57", "2026-11-10-tdah-xurta-tentin"):
    d = json.loads((EP / nom / "script.json").read_text(encoding="utf-8"))
    total = sum(len(lu(b.get("voix") or "")) for b in d["blocs"])
    s = total / CARS[d["voix_off"]]
    lignes += [f"## {d['label']}", "",
               f"- Couverture : « {ecran(d['sous_titre'])} »",
               f"- Pastille d'ouverture : {d['badge']} · voix : {VOIX[d['voix_off']]} · "
               f"durée estimée : {s // 60:.0f} min {s % 60:02.0f} s", ""]
    for i, b in enumerate(d["blocs"][1:], 1):
        if b.get("type") == "chiffre":
            e = f"{b['valeur']}{b.get('suffixe', '')} — {ecran(b['legende'])}"
        else:
            e = ecran(b["texte"])
        lignes += [f"**Plan {i}**", "", f"- Écran : {e}", f"- Voix ({jeu(b['voix'])}) : {lu(b['voix'])}",
                   f"- Animation : {animation(b)}", ""]
(ICI / "textes_1113.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
print(ICI / "textes_1113.md")
