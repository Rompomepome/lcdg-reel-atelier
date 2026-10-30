"""Reel « cumul emploi-retraite 2027 », version 3 (27/10/2026), au niveau des reels vaccins et
arrêts : ouverture sur l'enjeu, schéma animé sur presque chaque plan, le regard du Cercle en
phrase forte (« la décision est déjà prise, et à l'aveugle »). La v1 est dans scripts_1022.py.

Chaque fait vient du dossier (cumul-emploi-retraite-2027.txt) :
- Service Public : à partir de 2027, la distinction cumul intégral / plafonné disparaît, « seul
  l'âge compte » ; avant l'âge légal, revenus d'activité et de remplacement (IJ) déduits en
  totalité dès le 1er euro ; de l'âge légal à 67 ans, 7 000 € brut par an, au-delà pension
  diminuée de 50 % du dépassement ; à partir de 67 ans, cumul intégral, sans plafond ;
- seuil de 7 000 € : décret pas paru au 24 septembre (Assurance retraite) ;
- Carmf : exemple 35 000 € de pension, 60 000 € de revenus -> 8 500 € ; demande déposée après
  le 30 septembre 2026 -> effet en 2027 -> nouvelles règles ; points de retraite complémentaire
  en cumul intégral dès le 1er janvier 2027 ;
- exclusions (zones sous-denses, permanence des soins, régulation) renvoyées à un décret ;
- regard : « il fallait donc, en règle générale, déposer sa demande avant cette date, alors que
  le décret qui fixe le seuil n'était toujours pas paru » ; « un médecin ne peut pas décider de
  sa fin de carrière sur un projet de décret ».

    python script_cumul_v3.py"""
import json
import re
from pathlib import Path

D = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes\2026-10-22-cumul-emploi-retraite")
NB, AP = "\u00a0", "\u2019"

entete = {
    "slug": "cumul-emploi-retraite", "date": "2026-10-22", "rubrique": "pro", "label": "Cumul emploi-retraite",
    "sous_titre": f"Retraite avant 67 ans{NB}: votre pension *réduite*{NB}?",
    "appel": f"Notre recommandation{NB}:", "voix_off": "femme_agee", "badge": "Cumul emploi-retraite",
    "bandeau": f"L{AP}analyse complète | sur *notre site*"}
blocs = [
    {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "senior man writing desk"},
    # Service Public : à partir de 2027, « seul l'âge compte »
    {"duree": 7.0, "fichier": "B1.mp4", "requete": "page : https://www.service-public.gouv.fr/particuliers/actualites/A18914",
     "texte": f"Toucher sa retraite *et continuer d{AP}exercer*{NB}? | "
              f"Départ dès 2027{NB}? Avant 67 ans, la pension *pourra baisser*.",
     "voix": "[curious] Toucher votre retraite et continuer d’exercer ? | Si elle commence dès deux mille "
             "vingt-sept, avant soixante-sept ans, vos revenus pourront réduire votre pension.",
     # le curseur part de 67 ans et recule vers l'âge légal : plus on part tôt, plus la pension
     # est exposée ; « réduite au-delà d'un seuil » (le seuil n'est pas encore fixé)
     "insert": {"type": "ages", "titre": f"Dès 2027, seul l{AP}âge compte", "carre": False, "ordre": [2, 1, 0],
                "zones": [{"label": f"Avant l{AP}âge légal", "bulle": f"Réduite dès le 1er{NB}€", "ton": "rouge"},
                          {"label": f"De l{AP}âge légal à 67 ans", "bulle": f"Réduite au-delà d{AP}un seuil"},
                          {"label": "67 ans et plus", "bulle": "Cumul intégral", "ton": "vert"}]}},
    # Service Public : déduits en totalité dès le 1er euro, indemnités journalières comprises
    {"duree": 7.0, "fichier": "B2.mp4", "requete": "money wallet bills",
     "texte": f"Avant l{AP}âge légal{NB}: déduits *dès le 1er euro*. | Indemnités journalières comprises.",
     "voix": "Avant l’âge légal, vos revenus d’activité seront déduits de la pension dès le premier euro. | "
             "Indemnités journalières comprises.",
     # avant l'âge légal, déduits en totalité : 1 € gagné, 1 € de pension en moins
     "insert": {"type": "vases", "titre": f"1{NB}€ gagné, 1{NB}€ de pension en moins", "gauche": "Vos revenus",
                "droite": "Votre pension", "ajout": {"label": "IJ", "temps": 1}}},
    # seuil annoncé, que le décret doit encore fixer
    {"duree": 6.0, "type": "chiffre", "valeur": 7000, "suffixe": f"{NB}€", "fichier": "B3.mp4",
     "requete": "wallet money",
     "legende": f"brut par an, entre l{AP}âge légal et 67 ans{NB}: le seuil *annoncé*",
     "voix": "Entre l’âge légal et soixante-sept ans, le seuil annoncé est de sept mille euros brut par an. "
             "Un décret doit encore le fixer."},
    # au-delà, la pension est diminuée de 50 % du dépassement
    {"duree": 6.5, "fichier": "B4.mp4", "requete": "coins bag",
     "texte": f"Au-delà, la pension baisse de *50{NB}%* du dépassement. | 2{NB}€ gagnés en plus{NB}: 1{NB}€ de pension en moins.",
     "voix": "Au-delà, la pension baisse de la moitié du dépassement : | deux euros gagnés en plus, un euro "
             "de pension en moins.",
     "insert": {"type": "pieces", "titre": "Au-delà du seuil", "gauche": "Vos revenus", "droite": "Votre pension",
                "temps": 1}},
    # exemple de la Carmf
    {"duree": 6.5, "type": "chiffre", "valeur": 8500, "depuis": 35000, "suffixe": f"{NB}€", "fichier": "B5.mp4",
     "requete": "stack of papers",
     "legende": f"de pension par an pour 60{NB}000{NB}€ de revenus{NB}: *le calcul de la Carmf*",
     "voix": "L’exemple de la Carmf : trente-cinq mille euros de pension, soixante mille euros de revenus. "
             "La pension tombe à huit mille cinq cents euros."},
    # Service Public : à partir de 67 ans, cumul intégral, sans plafond. Téléconsultation (Romain,
    # 27/10/2026, livre blanc « 7 choix à prendre avant la retraite ») : l'Ordre la recommande en
    # complément d'une activité principalement présentielle, retraités actifs compris ; plafond
    # conventionnel des généralistes : 20 % de l'activité globale conventionnée sur l'année civile,
    # salariés de plateformes compris. Placée après 67 ans, où le cumul ne réduit plus la pension :
    # avant 67 ans, des revenus de téléconsultation entrent dans le calcul comme les autres
    {"duree": 7.5, "fichier": "B10.mp4", "requete": "telemedicine laptop video call",
     "texte": f"À partir de 67 ans{NB}: cumul *intégral*, sans plafond. | "
              f"Au cabinet, et en complément, en téléconsultation.",
     "voix": "À partir de soixante-sept ans, le cumul reste intégral, sans plafond : | au cabinet, et en "
             "complément, en téléconsultation, dans la limite de vingt pour cent de vos actes sur l’année.",
     "insert": {"type": "part", "pastille": "Cumul intégral, sans plafond", "part": 20, "centre": "au plus",
                "legende_part": "Téléconsultation", "legende_reste": "Activité présentielle", "temps_part": 1}},
    # Carmf : la date d'effet est le 1er jour du trimestre qui suit la demande
    {"duree": 7.0, "fichier": "B7.mp4", "requete": "clipboard pencil",
     "texte": f"À la Carmf, une demande déposée *après le 30 septembre* | prend effet en 2027{NB}: nouvelles règles.",
     "voix": "À la Carmf, une demande déposée après le trente septembre | prend effet en deux mille "
             "vingt-sept : nouvelles règles.",
     # Carmf : le 1er octobre 2026 est la dernière date d'effet de 2026, pour une demande déposée au
     # plus tard le 30 septembre ; après, la pension ne peut prendre effet avant le 1er janvier 2027
     "insert": {"type": "bascule", "temps": 1, "pilule": "Nouvelles règles",
                "avant": {"haut": "Sept. 2026", "jour": "30", "bas": "dernier jour"},
                "apres": {"haut": "Janv. 2027", "jour": "1er", "bas": "au plus tôt"},
                "legende_avant": "Dernier dépôt pour un effet en 2026",
                "legende_apres": "Date d’effet de la retraite"}},
    # regard : « la décision est déjà prise, et à l'aveugle »
    {"duree": 6.5, "type": "phrase", "fichier": "B9.mp4", "requete": "glasses on documents",
     "texte": f"Une décision prise *à l{AP}aveugle*.",
     "voix": "[serious] Pour garder les anciennes règles, il fallait donc, en général, déposer avant. Sans "
             "connaître le seuil : son décret n’était toujours pas paru."},
    # Ce qui pose question : activités exclues, renvoyées à un décret ; rien n'est publié
    {"duree": 7.0, "fichier": "B8.mp4", "requete": "village aerial countryside",
     "texte": f"Zones sous-denses, permanence des soins, régulation{NB}: *exclues*{NB}? | "
              f"Un décret doit le dire. Rien n{AP}est publié.",
     "voix": "Et les zones sous-denses, la permanence des soins, la régulation : seront-elles exclues du "
             "calcul ? | Un décret doit le dire. Rien n’est publié.",
     "insert": [{"type": "icones", "cartes": [{"icone": "repere", "label": "Zones sous-denses"},
                                              {"icone": "lune", "label": "Permanence des soins"},
                                              {"icone": "casque", "label": "Régulation"}]},
                {"type": "tampon", "texte": f"Rien n{AP}est publié", "temps": 1, "sur": True}]},
    # recommandation : faire le calcul avec la Carmf avant de déposer ; attendre le décret en zone
    # sous-dense ou en permanence des soins
    # plan sans visage, assez long pour le bloc et la carte de fin (B6.mp4 : 7 s, un visage en gros plan)
    {"duree": 5.5, "fichier": "B11.mp4", "requete": "doctor hands desk documents stethoscope",
     "texte": f"Retraite avant 67 ans en continuant d{AP}exercer{NB}? | Notre recommandation, *avant de déposer*.",
     "voix": "Retraite avant soixante-sept ans, en continuant d’exercer ? | Lisez d’abord notre "
             "recommandation, sur le site du Cercle.",
     "insert": {"type": "verrou", "n": 1}},
]
for b in blocs[1:]:
    lu = re.sub(r"\[[^\]]*\]", "", b.get("voix", "")).replace("|", "")
    b["duree"] = max(b["duree"], round(len(lu) / 18 + 1.0, 1))
(D / "script.json").write_text(json.dumps(dict(entete, blocs=blocs), ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
lu = " ".join(b.get("voix", "") for b in blocs).replace("|", "")
mots = len(re.sub(r"\[[^\]]*\]", "", lu).split())
print(f"{len(blocs)} blocs, {mots} mots lus, {len(lu)} caractères, "
      f"{sum(b['duree'] for b in blocs[1:]):.1f} s (sans couverture)")
