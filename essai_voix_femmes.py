"""Essai de voix de femme de la bibliotheque ElevenLabs (20/10/2026) : Romain entend de la
resonance dans femme_agee (voix creee par synthese). Meme passage du reel pour chaque voix,
modele v3 et memes indications de jeu ; on mesure la resonance (lcdg/resonance.py) et on
met les essais bout a bout dans un seul fichier a ecouter."""
import subprocess
import sys
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(R))
from dotenv import load_dotenv
load_dotenv(R / ".env")
import numpy as np
from config import charte as C
from lcdg import voix, resonance

TEXTE = ("[incredulous] La Cour des comptes veut imposer un minimum de patients ? [emphatic] À chaque "
         "généraliste libéral installé ! [curious] Et le seuil qu\u2019elle envisage ? Cinq cents patients "
         "par médecin traitant.")
VOIX = [("1_Sarah", "t8BrjWUT5Z23DLLBzbuY"), ("2_Jeanne", "txtf1EDouKke753vN8SL"),
        ("3_Genevieve", "mlIQEcTmPRMIHZApujDD"), ("4_Emilie", "d3AXX0BlgJHYFCuH9X88")]
TRAVAIL = Path(r"C:\Users\NR SMART\AppData\Local\Temp\lcdg_art\oct\essai_voix")
SORTIE = Path(r"C:\Users\NR SMART\Downloads\Essai_voix_femme_LCDG")
TRAVAIL.mkdir(parents=True, exist_ok=True)
SORTIE.mkdir(parents=True, exist_ok=True)
lo, hi = C.VOIX_RESONANCE_BANDE


def ff(*a):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", *a], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-600:])


morceaux = []
for nom, vid in VOIX:
    try:
        mp3, _ = voix.synthese(TEXTE, vid, TRAVAIL / nom, "eleven_v3", None)
    except (SystemExit, Exception) as e:
        print(f"{nom} : refusee ({e})")
        continue
    freq, rel = resonance.relief(mp3)
    m = (freq > lo) & (freq < hi)
    top = np.argsort(rel[m])[-2:][::-1]
    bosses = ", ".join(f"{freq[m][i]:.0f} Hz +{rel[m][i]:.1f} dB" for i in top)
    print(f"{nom:12} ecart-type {resonance.mesure(mp3):.2f} dB | bosses {bosses}")
    wav = TRAVAIL / f"{nom}.wav"
    ff("-i", str(mp3), "-af", f"atempo={C.VOIX_TEMPO_V3},loudnorm=I=-16:TP=-1.5,aresample=48000,apad=pad_dur=1.2",
       "-ac", "2", str(wav))
    ff("-i", str(wav), "-c:a", "libmp3lame", "-b:a", "192k", str(SORTIE / f"{nom}.mp3"))
    morceaux.append(wav)
liste = TRAVAIL / "liste.txt"
liste.write_text("\n".join(f"file '{m.as_posix()}'" for m in morceaux), encoding="utf-8")
ff("-f", "concat", "-safe", "0", "-i", str(liste), "-c:a", "libmp3lame", "-b:a", "192k",
   str(SORTIE / "0_les_4_voix_a_la_suite.mp3"))
print(SORTIE)
