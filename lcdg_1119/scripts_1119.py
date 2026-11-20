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
                 "défendait. | Mais le texte voté va jusqu’au prix de la consultation.",
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
         "voix": "Mais il y a deux conditions."},
        {"duree": 10.0, "fichier": "B5.mp4", "requete": "receptionist phone call hands desk",
         "texte": f"Un{NB}: à la prise de rendez-vous, *prévenir le patient*… | "
                  f"qu{AP}une pénalité est possible, *sauf motif* ou annulation à temps. | "
                  f"Deux{NB}: lui rappeler la date et l{AP}heure, *au moins une fois*. | "
                  f"Sinon, *rien à réclamer*.",
         "voix": "Un : à la prise de rendez-vous, prévenir le patient… | qu’une pénalité est possible, sauf motif "
                 "valable ou annulation à temps. | Deux : lui rappeler la date et l’heure, au moins une fois avant "
                 "le rendez-vous. | [serious] Sinon, rien à réclamer.",
         # scène animée : le téléphone sonne (la prise de rendez-vous), puis le rappel arrive en vol
         "insert": {"type": "appel", "etapes": [
             {"icone": "telephone", "label": "Prise de rendez-vous", "note": "pénalité annoncée", "temps": 0},
             {"icone": "courrier", "label": "Rappel date et heure", "note": "au moins 1 fois", "temps": 2}]}},
        # la question sans réponse : qui encaisse
        {"duree": 10.0, "fichier": "B6.mp4", "requete": "card payment terminal hand counter",
         "texte": f"Et qui *encaisse*{NB}? | "
                  f"Le patient paierait la pénalité *à sa caisse*. | "
                  f"Le texte ne dit pas si la somme *vous est reversée*.",
         "voix": "[curious] Et qui encaisse ? | Le patient paierait la pénalité à sa caisse d’assurance maladie. | "
                 "Mais le texte ne dit pas si la somme vous est reversée.",
         "insert": {"type": "renvoi", "etapes": [
             {"label": "Patient"}, {"label": "Sa caisse", "temps": 1},
             {"label": "Au médecin ?", "question": True, "temps": 2}]}},
        # la recommandation du Cercle (attribuée), dans ce que dit « L'ESSENTIEL » ; rien n'est définitif (CMP)
        {"duree": 10.0, "fichier": "B7.mp4", "requete": "hands typing laptop calendar bright",
         "texte": f"Selon nous, activez dès maintenant *un rappel*… | "
                  f"avant chaque rendez-vous. | "
                  f"Mais ne réclamez *aucune pénalité*{NB}: le texte n{AP}est pas définitif.",
         "voix": "[warm] Selon nous, activez dès maintenant un rappel | avant chaque rendez-vous. | "
                 "Mais ne réclamez aucune pénalité : le texte n’est pas définitif.",
         "insert": {"type": "choix", "lignes": [
             {"label": "Un rappel avant chaque rendez-vous", "ok": True, "temps": 0},
             {"label": "Une pénalité avant la loi définitive", "ok": False, "temps": 2}]}},
        # la promesse : ce que le site garde (le comptage d'un mois, la décision, la survie du texte)
        {"duree": 7.0, "fichier": "B8.mp4", "requete": "notebook pen desk window light",
         "texte": f"Comment décider *si vous l{AP}appliquerez*{NB}? | "
                  f"Notre recommandation complète est *sur le site*.",
         "voix": "[curious] Et comment décider si vous l’appliquerez ? | Notre recommandation complète est sur "
                 "le site du Cercle.",
         "insert": {"type": "verrou", "n": 1}},
    ]}

# ------------------------------------------------------------------ Téléconsultation assistée (PDF p. 6 à 8)
# Romain, 20/11 : « fais les réels pour les sujets les plus chauds et téléconsultations », puis « fais-en que 2 ».
# Même format que la taxe lapin (environ 1 min 10). Voix d'Emilie : patients âgés, sujet sérieux sans être grave.
# Relu contre le PDF et le texte adopté par le Sénat (article 23 ; article 32, L. 161-35-2), lus le 20/11 sur senat.fr.
TELECONSULTATION = {
    "slug": "teleconsultation-assistee", "date": "2026-11-19", "rubrique": "pro",
    "label": "Téléconsultation assistée",
    "sous_titre": f"Votre patient âgé, vu par *un autre* médecin{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "femme_agee", "badge": "Médecins traitants",
    "bandeau": BANDEAU, "son_limite_db": -4.0,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "elderly woman video call tablet bright home"},
        # p. 6, SITUATION (« le texte ne dit rien de l'information du médecin traitant ») ; article 23 : actes
        # d'assistance « réalisés sur le lieu de vie habituel ou temporaire du patient […] par les infirmiers »
        {"duree": 12.0, "fichier": "B1.mp4", "requete": "nurse hands tablet home visit daylight",
         "texte": f"Médecins traitants{NB}: le Sénat a voté le remboursement… | "
                  f"de la téléconsultation *assistée* à domicile… | "
                  f"par des infirmiers *salariés* de sociétés de téléconsultation. | "
                  f"Sans rien prévoir pour *vous prévenir*.",
         "voix": "Médecins traitants : le Sénat a voté le remboursement | de la téléconsultation "
                 "assistée à domicile | par des infirmiers salariés de sociétés de téléconsultation. | [serious] Sans "
                 "rien prévoir pour vous prévenir.",
         "insert": {"type": "appel", "carre": False, "etapes": [
             {"icone": "infirmier", "label": "Infirmier salarié", "note": "au domicile", "temps": 2},
             {"icone": "telephone", "label": "Téléconsultation", "note": "remboursée", "temps": 2}]}},
        # p. 6, CONTEXTE : « seules 0,3 % des téléconsultations réalisées de 2020 à 2023 l'ont été avec l'assistance
        # d'un professionnel de santé, alors que l'assistance doit permettre aux patients âgés […] d'y accéder »
        {"duree": 6.0, "type": "chiffre", "valeur": 0.3, "decimales": 1, "suffixe": f"{NB}%",
         "legende": f"des téléconsultations de 2020 à 2023 étaient *assistées*, selon le rapport du Sénat",
         "fichier": "B2.mp4", "requete": "laptop screen video call desk calm",
         "voix": "Pourquoi ? Selon le rapport du Sénat, seules zéro virgule trois pour cent des téléconsultations de "
                 "deux mille vingt à deux mille vingt-trois étaient assistées."},
        # p. 7, CE QUI EST CONFIRMÉ : amendement n° 662 rectifié rejeté ; renvoi du rapporteur à l'article 32
        # (L. 161-35-2 : « pour les logiciels proposant également des fonctionnalités de production de documents de
        # santé », des fonctions « permettant, par défaut, l'alimentation par le professionnel du dossier médical
        # partagé ») ; « L'article 32 ne prévoit pas d'informer le médecin traitant »
        {"duree": 16.0, "fichier": "B4.mp4", "requete": "hands typing keyboard medical software",
         "texte": f"Inscrire l{AP}acte au *dossier partagé*{NB}? Amendement rejeté. | "
                  f"Le rapporteur renvoie aux *logiciels* de facturation. | "
                  f"S{AP}ils font aussi les ordonnances{NB}: *dossier rempli*. | "
                  f"Mais rien pour *vous prévenir*.",
         "voix": "Un amendement voulait inscrire chaque téléconsultation au dossier médical partagé : rejeté. | Le "
                 "rapporteur renvoie aux logiciels de facturation. | Quand ils produisent aussi des documents de "
                 "santé, ils devront permettre au soignant de remplir ce dossier. | Mais rien n’oblige à vous "
                 "prévenir.",
         "insert": {"type": "loupe", "site": f"Article{NB}23", "recherche": "informer le médecin traitant",
                    "vide": "Rien"}},
        # p. 7, CE QUI POSE QUESTION : qui sera le médecin téléconsultant ? (territorialité, avec dérogations)
        {"duree": 10.0, "fichier": "B5.mp4", "requete": "elderly man sofa tablet nurse",
         "texte": f"Et qui sera *le médecin* au bout de l{AP}écran{NB}? | "
                  f"Le texte ne dit pas si ce sera vous… *ou un autre médecin*.",
         "voix": "[curious] Et qui sera le médecin, au bout de l’écran ? | Le texte ne dit pas si ce sera vous, ou "
                 "un autre médecin.",
         "insert": {"type": "renvoi", "etapes": [
             {"label": "Patient"}, {"label": "Infirmier salarié", "temps": 0},
             {"label": "Quel médecin ?", "question": True, "temps": 1}]}},
        # p. 7, L'IMPACT (lecture du dossier, attribuée) : « un patient âgé peut être vu à domicile, en téléconsultation,
        # par un autre médecin, et revenir avec une ordonnance dont il ignore l'origine si rien n'est versé au DMP »
        {"duree": 11.0, "fichier": "B6.mp4", "requete": "prescription paper kitchen table elderly hands",
         "texte": f"Selon nous, s{AP}il est vu par *un autre médecin*… | "
                  f"il peut revenir avec une ordonnance… *d{AP}où vient-elle*{NB}? | "
                  f"Vous ne le saurez pas si rien n{AP}est versé *au dossier*.",
         "voix": "Selon nous, s’il est vu par un autre médecin, | il peut revenir avec une ordonnance… d’où "
                 "vient-elle ? | Vous ne le saurez pas, si rien n’est versé à son dossier.",
         "insert": {"type": "dossier", "titre": "Dossier médical partagé", "temps_question": 1}},
        # p. 6, SITUATION et L'ESSENTIEL (« rien n'est définitif » ; « Que faire : proposer dès maintenant à ces patients
        # la téléconsultation assistée avec les infirmiers libéraux du secteur, qui la facturent déjà ») ; p. 6, tarifs
        # selon le rapport (10 € lors d'un soin, 12 € dans un lieu dédié, 15 € au domicile)
        {"duree": 13.0, "fichier": "B7.mp4", "requete": "nurse arriving home visit bag daylight",
         "texte": f"Le texte n{AP}est *pas définitif*. | "
                  f"Mais vous pouvez déjà la proposer avec *les infirmiers libéraux*. | "
                  f"Selon le rapport, ils la facturent{NB}: *15{NB}€* au domicile.",
         "voix": "Le texte n’est pas définitif. | [warm] Mais vous pouvez déjà la proposer à "
                 "vos patients âgés, avec les infirmiers libéraux du secteur. | Selon le rapport, ils la facturent "
                 "déjà : quinze euros au domicile.",
         "insert": {"type": "ticket", "titre": "Infirmier libéral, selon le rapport", "lignes": [
             {"label": "Pendant un soin", "valeur": f"10{NB}€", "temps": 2},
             {"label": "Dans un lieu dédié", "valeur": f"12{NB}€", "temps": 2},
             {"label": "Au domicile", "valeur": f"15{NB}€", "ok": True, "temps": 2}]}},
        # la promesse : les 2 recommandations (repérer une téléconsultation faite ailleurs ; planning de CPTS)
        {"duree": 8.0, "fichier": "B8.mp4", "requete": "notebook pen desk window light morning",
         "texte": f"Comment repérer une téléconsultation *faite ailleurs*{NB}? | "
                  f"Nos *2{NB}recommandations* sont sur le site.",
         "voix": "[curious] Et comment repérer une téléconsultation faite ailleurs ? | Nos deux "
                 "recommandations sont sur le site du Cercle.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

# Secteur 3 : un troisième reel a été écrit le 20/11 puis retiré à la demande de Romain (« ne fais pas trois reels,
# fais-en que 2 » : le quota ElevenLabs du mois n'en permet que deux). Le sujet reste couvert par le carrousel.

# caractères lus par seconde, mesurés le 05/11/2026 sur les rendus (fin de reel comprise)
CARS_PAR_SECONDE = {"homme_age": 14.1, "femme_agee": 15.8, "femme_jeune": 14.6}
for ep in (TAXE_LAPIN, TELECONSULTATION):
    d = EP / f"{ep['date']}-{ep['slug']}"
    (d / "broll").mkdir(parents=True, exist_ok=True)
    (d / "script.json").write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lu = re.sub(r"\[[a-z-]+\]\s*", "", " ".join((b.get("voix") or "") for b in ep["blocs"])).replace(" | ", " ")
    s = len(lu) / CARS_PAR_SECONDE[ep["voix_off"]]
    print(f"{d.name} : {len(ep['blocs']) - 1} plans, {len(lu)} caractères lus, environ {s // 60:.0f} min {s % 60:02.0f} s, "
          f"environ {len(lu) * 300 / 1400:.0f} crédits")
