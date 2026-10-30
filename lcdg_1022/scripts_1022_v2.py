"""Reels LCDG du 22/10/2026, version 2 (Romain : « il faut être cinglant et tranchant, ça doit
refléter l'esprit de la revue et être juste », « s'il doit y avoir des schémas animés, n'hésite
pas »). Vaccins au cabinet et arrêts de travail ; le cumul emploi-retraite reste en version 1.

Le fil de chaque reel suit « Le regard du Cercle » du dossier : vaccins = « construit comme un
remboursement, et non comme une rémunération » ; arrêts = « 2 messages contraires ». La chute
cite ce regard en une phrase ; les recommandations restent sur le site. Chaque fait vient du
dossier (texte dans ce dossier, *.txt). Les plans déjà choisis sont réutilisés (champ fichier)."""
import json
import re
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
NB, AP = "\u00a0", "\u2019"
BANDEAU = f"L{AP}analyse complète | sur *notre site*"


def episode(dossier, entete, blocs):
    D = R / dossier
    script = dict(entete, bandeau=BANDEAU, blocs=blocs)
    (D / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lu = " ".join(b.get("voix", "") for b in blocs).replace("|", "")
    mots = len(re.sub(r"\[[^\]]*\]", "", lu).split())
    print(f"{dossier} : {len(blocs)} blocs, {mots} mots lus, {len(lu)} caractères")


# --------------------------------------------------------------------------- vaccins au cabinet
episode("2026-10-22-vaccins-cabinet", {
    "slug": "vaccins-cabinet", "date": "2026-10-22", "rubrique": "pro", "label": "Vaccins au cabinet",
    "sous_titre": f"Le vaccin «{NB}gratuit{NB}» que vous *payez d{AP}abord*",
    "appel": f"Notre recommandation{NB}:", "voix_off": "homme_jeune", "badge": "Décret du 9 octobre"}, [
    {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "flu vaccine syringe vial"},
    # décret n° 2026-939, en vigueur le 11 octobre ; regard : « le patient ciblé peut repartir vacciné »
    {"duree": 7.0, "fichier": "B1.mp4", "requete": "page : ameli, vaccination grippe, espace médecin",
     "texte": f"Grippe, Covid-19{NB}: les vaccins *au cabinet*. | Le patient ciblé repart vacciné.",
     "voix": "Depuis le onze octobre, vous pouvez garder au cabinet les vaccins contre la grippe et le "
             "Covid-19. | Le patient ciblé repart vacciné, dès la consultation."},
    # le médecin paie d'abord les doses au pharmacien ; Vaxigrip 11,75 € (base publique des médicaments)
    {"duree": 6.0, "type": "chiffre", "valeur": 11.75, "decimales": 2, "suffixe": f"{NB}€",
     "legende": f"la dose de Vaxigrip{NB}: c{AP}est vous qui *l{AP}avancez*", "fichier": "B3.mp4",
     "requete": "pharmacist handing medicine",
     "voix": "Mais ces doses, c’est vous qui les payez d’abord au pharmacien : onze euros soixante-quinze "
             "la dose de Vaxigrip."},
    # arrêté du 8 octobre : majoration = prix public du vaccin administré ; SKB standard, SKC hautement dosé
    {"duree": 6.5, "fichier": "B2.mp4", "requete": "doctor typing computer office",
     "texte": f"Remboursée *une fois injectée*. | SKB, ou SKC pour le vaccin hautement dosé.",
     "voix": "L’Assurance Maladie vous la rembourse une fois injectée : | c’est la majoration S.K.B., ou "
             "S.K.C. pour un vaccin hautement dosé."},
    # ameli : injection « dans le cadre d'une consultation sans code acte spécifique »
    {"duree": 6.0, "fichier": "B5.mp4", "requete": "vaccine injection arm",
     "texte": f"L{AP}injection{NB}? *Aucun code.* | Elle se fond dans la consultation.",
     "voix": "Et l’injection ? Aucun code : | elle se fait dans le cadre de la consultation."},
    {"duree": 4.0, "type": "phrase", "fichier": "B6.mp4", "requete": "vaccine vial blue background",
     "texte": f"Et la dose *qui ne sert pas*{NB}?",
     "voix": "Et la dose qui ne sert pas ?"},
    # ni le décret, ni l'arrêté, ni l'Assurance Maladie ne disent ce que devient une dose périmée ou
    # perdue ; CSMF : « les doses perdues ou périmées restent à votre charge »
    {"duree": 7.5, "fichier": "B7.mp4", "requete": "vials on the table",
     "texte": f"Périmée ou perdue{NB}: *aucun texte* ne dit qui paie. | Selon la CSMF, c{AP}est vous.",
     "voix": "Périmée, ou perdue après une rupture de la chaîne du froid : aucun texte ne dit qui la paie. | "
             "Selon la C.S.M.F., elle reste à votre charge.",
     "insert": {"type": "circuit", "lignes": [
         {"titre": "Dose injectée", "etapes": ["−11,75 €", "+11,75 €"], "fin": "remboursée", "ok": True, "temps": 0},
         {"titre": "Dose perdue ou périmée", "etapes": ["−11,75 €", "? €"], "fin": "à votre charge ?",
          "ok": False, "temps": 1}]}},
    # regard : « construit comme un remboursement, et non comme une rémunération » ; l'arrêté ne prévoit
    # aucune autre rémunération pour la commande, le stockage ou les doses perdues
    {"duree": 5.5, "type": "phrase", "fichier": "B4.mp4", "requete": "counting coins desk",
     "texte": f"Remboursé, *pas rémunéré*.",
     "voix": "Un remboursement, pas une rémunération : rien pour la commande, rien pour le stock, rien pour "
             "les doses perdues."},
    {"duree": 5.0, "fichier": "B9.mp4", "requete": "hands writing notebook",
     "texte": f"Combien de doses commander{NB}? | Notre recommandation, *sur le site*.",
     "voix": "Alors, combien de doses commander ? | Notre recommandation est sur le site du Cercle.",
     "insert": {"type": "verrou", "n": 1}},
])

# --------------------------------------------------------------------------- arrêts de travail
episode("2026-10-22-arrets-travail-mso", {
    "slug": "arrets-travail-mso", "date": "2026-10-22", "rubrique": "pro", "label": "Arrêts de travail",
    "sous_titre": f"Arrêts de travail{NB}: *650 médecins* dans le viseur",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "homme_age", "badge": "Mise sous objectifs"}, [
    {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "doctor filling form"},
    # MG France : nouvelle campagne présentée le 14 octobre aux syndicats
    {"duree": 7.0, "fichier": "B1.mp4", "requete": "office telephone",
     "texte": f"Arrêts de travail{NB}: retour de la *mise sous objectifs*. | Annoncée aux syndicats le 14 octobre.",
     "voix": "L’Assurance Maladie relance la mise sous objectifs sur les arrêts de travail. | Elle l’a "
             "annoncée aux syndicats le quatorze octobre, selon MG France."},
    # CSMF, 15 octobre : « 650 médecins vont être contrôlés »
    {"duree": 5.0, "type": "chiffre", "valeur": 650, "suffixe": f"{NB}médecins", "fichier": "B2.mp4",
     "legende": f"vont être contrôlés, *selon la CSMF*", "requete": "envelopes letters",
     "voix": "Six cent cinquante médecins vont être contrôlés, selon la C.S.M.F."},
    # au 22 octobre, rien sur ameli.fr ; L. 162-1-15 : « pour une activité comparable », sans méthode publiée
    {"duree": 5.5, "fichier": "B3.mp4", "requete": "man at computer monitor",
     "texte": f"Sur quels critères{NB}? | *Pas une ligne* sur ameli.fr.",
     "voix": "Sur quels critères ? | Au vingt-deux octobre, pas une ligne sur ameli.fr."},
    # SOS IJ, 20 octobre : arrêts complexes, premier retour sous 48 heures ; 14 -> 20 octobre = 6 jours
    {"duree": 8.0, "fichier": "B7.mp4", "requete": "page : ameli, SOS IJ",
     "texte": f"6 jours plus tard{NB}: *SOS IJ*, pour vous aider. | Arrêts complexes, 1er retour sous 48{NB}h.",
     "voix": "Six jours plus tard, la même Assurance Maladie lance S.O.S. I.J. pour vous aider : | un service "
             "d’amelipro pour les arrêts de travail complexes, avec un premier retour sous quarante-huit heures.",
     "insert": {"type": "duel", "cartes": [
         {"date": "14 octobre", "texte": "Une campagne de contrôle", "ok": False, "temps": 0},
         {"date": "20 octobre", "texte": "Un outil pour vous aider", "ok": True, "temps": 0}]}},
    # regard : « L'Assurance Maladie envoie 2 messages contraires »
    {"duree": 3.5, "type": "phrase", "fichier": "B4.mp4", "requete": "telephone pink background",
     "texte": f"*Deux messages* contraires.",
     "voix": "Deux messages contraires."},
    # Ce qui pose question : un arrêt signalé dans SOS IJ sera-t-il retiré du calcul ?
    {"duree": 7.0, "fichier": "B8.mp4", "requete": "tablet charts data",
     "texte": f"Un arrêt signalé dans SOS IJ sortira-t-il *du calcul*{NB}? | Rien ne le dit.",
     "voix": "Car un arrêt signalé dans S.O.S. I.J. sortira-t-il du calcul qui sert à cibler les médecins ? | "
             "Rien ne le dit."},
    # regard : « tant que ces arrêts pèsent dans le calcul [...], le généraliste qui suit les situations
    # les plus difficiles reste le plus exposé »
    {"duree": 5.5, "type": "phrase", "fichier": "B6.mp4", "requete": "signing certificate",
     "texte": f"Le plus exposé{NB}: celui qui suit *les cas lourds*.",
     "voix": "Tant que ces arrêts comptent, le médecin le plus exposé, c’est celui qui suit les situations "
             "les plus difficiles."},
    # CSS R. 148-1 (1 mois pour les observations), R. 148-3 (15 jours pour refuser, silence = accepté)
    {"duree": 8.0, "fichier": "B5.mp4", "requete": "marking calendar",
     "texte": f"Ciblé{NB}? *1 mois* pour vos observations. | *15 jours* pour refuser. Sinon, accepté.",
     "voix": "Si vous êtes ciblé : un mois pour présenter vos observations, | puis quinze jours pour refuser "
             "la mise sous objectifs. Sans réponse, elle est considérée comme acceptée.",
     "insert": {"type": "frise", "etapes": [
         {"label": "Vos chiffres notifiés", "temps": 0},
         {"label": "1 mois : vos observations", "temps": 0},
         {"label": "Proposition de MSO", "temps": 1},
         {"label": "15 jours pour refuser", "temps": 1},
         {"label": "Sans réponse : acceptée", "alerte": True, "temps": 1}]}},
    {"duree": 5.0, "fichier": "B9.mp4", "requete": "notebook phone desk",
     "texte": f"Votre caisse vous appelle{NB}? | Ce qu{AP}il faut faire, *dès l{AP}appel*.",
     "voix": "Votre caisse vous appelle ? | Ce qu’il faut faire, dès l’appel, est sur le site du Cercle.",
     "insert": {"type": "verrou", "n": 2}},
])
