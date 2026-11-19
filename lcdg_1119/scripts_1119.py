"""Reel du 19/11/2026, tiré du dossier « PLFSS 2027 : ce que le Sénat a voté pour votre cabinet » (revue du
19/11/2026, LCDG_revue_du_19-11-2026.pdf, pages 2 à 5, lu en entier avec ses sources, page 20).

Demande de Romain, le 19/11 : « Taxe lapin : un reel (4:5, 50 s à 1 min 10) ». « C'est le sujet le plus chaud et il
raconte une histoire : 5 € annoncés en séance, un texte voté qui va jusqu'au prix de la consultation, une condition
(le rappel au patient) et une question sans réponse (qui encaisse ?) ». Déroulé demandé : l'accroche sur l'écart
entre l'annonce et le texte, ce que dit vraiment le texte, la condition du rappel, qui encaisse, la recommandation
(activer les rappels dès maintenant), puis la carte finale. D'où, par rapport aux reels du 13/11 :
- environ 1 min, et non 1 min 45 à 2 min (demande expresse pour ce reel) ;
- la recommandation est donnée, mais seulement ce que dit déjà « L'ESSENTIEL » (« Que faire : activer dès
  maintenant les rappels de rendez-vous, sans appliquer de pénalité avant la loi définitive »). Le reste de la
  recommandation (garder la trace, compter un mois de rendez-vous manqués pour décider) est gardé pour le site ;
- format 4:5 : le 9:16 est déjà composé pour le recadrage 4:5 du fil (zone sûre y 285-1635) ; le fichier 4:5
  s'en tire par un recadrage centré, sans rien changer à la charte.

Faits (dossier, « CE QUI EST CONFIRMÉ ») :
- amendements identiques n° 7 rectifié octies et n° 84 rectifié quater, adoptés le 16 novembre 2026 ; ensemble du
  PLFSS adopté le 18 novembre (201 voix contre 124) ; « ils ne sont pas définitifs » : commission mixte paritaire,
  puis nouvelle lecture en cas d'échec ;
- le texte adopté permet à l'établissement de santé, au centre de santé ou au professionnel de santé libéral
  d'« exiger du patient le paiement d'une pénalité » lorsqu'il ne se présente pas ou annule « sans respecter un
  délai raisonnable » ;
- « est proportionnelle au tarif de la consultation ou est fixée à une somme forfaitaire, et ne peut en aucun cas
  excéder le montant de la consultation » ;
- pas de pénalité si le patient justifie d'un « motif impérieux d'ordre personnel, familial ou professionnel » ou
  d'un motif de santé ; sa mise en place est « un choix discrétionnaire » du professionnel ;
- pour la réclamer, il « doit avoir informé le patient à la prise de rendez-vous et lui avoir rappelé la date et
  l'horaire au moins une fois » ;
- paiement « à l'organisme d'assurance maladie de l'assuré, prélevée sur son compte après autorisation ou récupérée
  sur ses prestations à venir » ; « sans dire si la somme est ensuite reversée au professionnel » (CE QUI POSE
  QUESTION) ;
- un décret en Conseil d'État doit fixer le délai raisonnable, les motifs d'exonération et le règlement amiable ;
- en séance, « le sénateur qui a défendu l'amendement n° 7 a présenté une « pénalité limitée à 5 euros » et une
  « possibilité d'annuler un rendez-vous jusqu'à 24 heures avant » ; ni ce montant ni ce délai ne figurent dans le
  texte adopté ».
Regard du Cercle (attribué) : « tant que rien ne dit qu'elle sera reversée au médecin, elle ne compense pas le
créneau perdu ».
Gardé pour le site : la censure de 2025 et la survie du texte (CMP, Conseil constitutionnel), la demande du Cercle
(qui encaisse, signalement depuis l'agenda), la recommandation entière (trace, un mois de comptage).

Non relu à la source le 19/11 : senat.fr est hors du réseau de la session cloud. Le texte adopté n° 33 et le compte
rendu du 16/11 sont à relire avant la voix (la presse, dont un cabinet d'avocats, titre encore « 5 euros, 24 heures »).

    python scripts_1119.py"""
import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# le poste de Romain, sinon le dépôt voisin de l'atelier (session cloud du 19/11/2026)
EP = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
if not EP.exists():
    EP = Path(os.environ.get("LCDG_EPISODES", Path(__file__).resolve().parents[2] / "lcdg-reel" / "episodes"))
NB, AP = "\u00a0", "\u2019"
BANDEAU = f"L{AP}analyse complète | sur *notre site*"

TAXE_LAPIN = {
    "slug": "taxe-lapin-senat", "date": "2026-11-19", "rubrique": "pro", "label": "Taxe lapin",
    "sous_titre": f"5{NB}€ annoncés, mais *jusqu{AP}au prix* de la consultation",
    "appel": f"Notre recommandation{NB}:", "voix_off": "femme_jeune", "badge": "Médecins libéraux",
    "bandeau": BANDEAU, "son_limite_db": -4.0, "voix_tempo": 1.08,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "empty waiting room chairs daylight"},
        # l'accroche : l'écart entre l'annonce en séance (le sénateur qui a défendu l'amendement n° 7) et le texte
        {"duree": 9.0, "fichier": "B1.mp4", "requete": "appointment book calendar desk pen",
         "texte": f"Médecins libéraux{NB}: la taxe lapin a été présentée *à 5{NB}€*… | "
                  f"par *le sénateur* qui la défendait. | "
                  f"Le texte voté va *jusqu{AP}au prix* de la consultation.",
         "voix": "[curious] Médecins libéraux : la taxe lapin a été présentée à cinq euros, | par le sénateur qui la "
                 "défendait. | [matter-of-fact] Mais le texte voté va jusqu’au prix de la consultation.",
         "insert": {"type": "duel", "carre": False, "cartes": [
             {"date": "Le sénateur", "texte": "5 € annoncés", "temps": 0},
             {"date": "Le texte voté", "texte": "Jusqu’au prix de la consultation", "temps": 2}]}},
        # même écart sur l'annulation : 24 heures annoncées, un « délai raisonnable » à fixer par décret
        {"duree": 9.0, "fichier": "B2.mp4", "requete": "wall clock office daylight",
         "texte": f"Il parlait d{AP}annuler jusqu{AP}à *24{NB}heures avant*. | "
                  f"Le texte dit *«{NB}un délai raisonnable{NB}»*, | "
                  f"qu{AP}un décret doit *encore fixer*.",
         "voix": "Il parlait d’annuler jusqu’à vingt-quatre heures avant. | Le texte dit : « un délai "
                 "raisonnable », | qu’un décret doit encore fixer.",
         "insert": {"type": "sablier", "pilules": [
             {"texte": "24 h annoncées", "temps": 0},
             {"texte": "« Un délai raisonnable »", "temps": 1},
             {"texte": "À fixer par décret", "ton": "rouge", "temps": 2}]}},
        # ce que dit vraiment le texte : quand, combien, sauf quoi (condition entière, au conditionnel : rien n'est
        # définitif)
        {"duree": 15.0, "fichier": "B3.mp4", "requete": "doctor desk empty chair afternoon",
         "texte": f"Le texte voté permettrait *une pénalité*… | "
                  f"si le patient ne vient pas, ou annule *hors délai*. | "
                  f"Jamais plus que *la consultation*. | "
                  f"Sauf si le patient justifie d{AP}un motif *impérieux*… | "
                  f"personnel, familial ou professionnel, *ou de santé*.",
         "voix": "Le texte voté permettrait une pénalité, | si le patient ne vient pas, ou annule hors délai. "
                 "| Jamais plus que le prix de la consultation. | Sauf s’il justifie d’un motif impérieux, "
                 "| personnel, familial ou professionnel, ou d’un motif de santé.",
         "insert": {"type": "ticket", "titre": "Rendez-vous non honoré", "lignes": [
             {"label": "Absent ou hors délai", "valeur": "pénalité", "ok": True, "temps": 1},
             {"label": "Plafond", "valeur": "1 consultation", "ok": True, "temps": 2},
             {"label": "Motif justifié", "valeur": "pas de pénalité", "ok": False, "temps": 3}]}},
        # les conditions : information à la prise de rendez-vous et au moins un rappel
        {"duree": 4.0, "type": "phrase", "fichier": "B4.mp4", "requete": "smartphone notification hand",
         "texte": "Mais il y a *deux conditions*.",
         "voix": "[matter-of-fact] Mais il y a deux conditions."},
        {"duree": 10.0, "fichier": "B5.mp4", "requete": "receptionist phone call hands desk",
         "texte": f"Vous devez avoir *informé le patient* à la prise de rendez-vous. | "
                  f"Et lui avoir rappelé la date et l{AP}heure *au moins une fois*. | "
                  f"Sinon, *rien à réclamer*.",
         "voix": "Vous devez avoir informé le patient à la prise de rendez-vous, | et lui avoir rappelé la date et "
                 "l’heure, au moins une fois. | [serious] Sinon, rien à réclamer.",
         "insert": {"type": "icones", "cartes": [
             {"icone": "patient", "label": "Patient informé", "question": False, "temps": 0},
             {"icone": "horloge", "label": "Rappel, au moins 1 fois", "question": False, "temps": 1}]}},
        # la question sans réponse : qui encaisse
        {"duree": 10.0, "fichier": "B6.mp4", "requete": "card payment terminal hand counter",
         "texte": f"Et qui *encaisse*{NB}? | "
                  f"Le patient paierait la pénalité *à sa caisse*. | "
                  f"Le texte ne dit pas si la somme *vous est reversée*.",
         "voix": "[curious] Et qui encaisse ? | Le patient paierait la pénalité à sa caisse d’assurance maladie. | "
                 "[thoughtful] Mais le texte ne dit pas si la somme vous est reversée.",
         "insert": {"type": "renvoi", "etapes": [
             {"label": "Patient"}, {"label": "Sa caisse", "temps": 1},
             {"label": "Au médecin ?", "question": True, "temps": 2}]}},
        # la recommandation du Cercle (attribuée), dans ce que dit « L'ESSENTIEL » ; rien n'est définitif (CMP)
        {"duree": 10.0, "fichier": "B7.mp4", "requete": "hands typing laptop calendar bright",
         "texte": f"Selon nous, activez dès maintenant *un rappel*… | "
                  f"avant chaque rendez-vous. | "
                  f"Mais ne réclamez *aucune pénalité*{NB}: le texte n{AP}est pas définitif.",
         "voix": "[warm] Selon nous, activez dès maintenant un rappel | avant chaque rendez-vous. | [matter-of-fact] "
                 "Mais ne réclamez aucune pénalité : le texte n’est pas définitif.",
         "insert": {"type": "choix", "lignes": [
             {"label": "Un rappel avant chaque rendez-vous", "ok": True, "temps": 0},
             {"label": "Une pénalité avant la loi définitive", "ok": False, "temps": 2}]}},
        # la promesse : ce que le site garde (le comptage d'un mois, la décision, la survie du texte)
        {"duree": 7.0, "fichier": "B8.mp4", "requete": "notebook pen desk window light",
         "texte": f"Comment décider *si vous l{AP}appliquerez*{NB}? | "
                  f"Notre recommandation complète est *sur le site*.",
         "voix": "[curious] Et comment décider si vous l’appliquerez ? | [warm] Notre recommandation complète est sur "
                 "le site du Cercle.",
         "insert": {"type": "verrou", "n": 1}},
    ]}

# caractères lus par seconde, mesurés le 05/11/2026 sur les rendus (fin de reel comprise)
CARS_PAR_SECONDE = {"homme_age": 14.1, "femme_agee": 15.8, "femme_jeune": 14.6}
for ep in (TAXE_LAPIN,):
    d = EP / f"{ep['date']}-{ep['slug']}"
    (d / "broll").mkdir(parents=True, exist_ok=True)
    (d / "script.json").write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lu = re.sub(r"\[[a-z-]+\]\s*", "", " ".join((b.get("voix") or "") for b in ep["blocs"])).replace(" | ", " ")
    s = len(lu) / CARS_PAR_SECONDE[ep["voix_off"]]
    print(f"{d.name} : {len(ep['blocs']) - 1} plans, {len(lu)} caractères lus, environ {s // 60:.0f} min {s % 60:02.0f} s, "
          f"environ {len(lu) * 300 / 1400:.0f} crédits")
