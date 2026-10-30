"""Reels LCDG du 22/10/2026, version 3 (Romain, 23/10 : « on va faire des ads dessus, ils
doivent vraiment être percutants », « il y a encore pas mal de choses qu'on peut intégrer pour
vraiment informer et donner envie de lire la suite sur le site » ; puis, sur « L'injection ?
Aucun code » : « ça veut dire quoi ? fais attention au wording et tournure de phrase ! »).

Ce qui change depuis la v2 (scripts_1022_v2.py) :
- les 2 premières secondes portent le conflit (la pub démarre sur le bloc 1) : vaccins = « vous
  pouvez garder des vaccins au cabinet, mais vous les payez d'abord » ; arrêts = le compteur
  « 650 médecins » en ouverture ;
- plus de faits confirmés et utiles : prix Vaxigrip / Efluelda, enceinte réfrigérée et
  responsabilité du stock (décret), les 3 questions ouvertes ; critères de la campagne
  précédente (10 % / 2 fois la moyenne), courriers « précédés en principe d'un appel » ;
- inserts : barres de prix, tampon, liste « ? » des questions ouvertes ; barres « ×2 » ;
- chaque phrase dit ce qu'elle veut dire, sans raccourci de spécialiste : « pas facturable à
  part » plutôt que « aucun code », « la dose vous est remboursée » plutôt que « remboursée » ;
  3 lignes au plus par temps (contrôle : lignes_textes.py).

Contrainte de crédits : il reste 278 crédits ElevenLabs jusqu'au 27/10 (environ 0,22 crédit
par caractère) ; la voix des arrêts doit tenir sous 1 150 caractères, avec la marge d'une
reprise. Chaque fait vient du dossier (*.txt de ce dossier)."""
import json
import re
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
NB, AP = "\u00a0", "\u2019"
BANDEAU = f"L{AP}analyse complète | sur *notre site*"


def episode(dossier, entete, blocs):
    D = R / dossier
    # la voix fixe la durée ; pour l'aperçu sans voix, on l'estime au débit mesuré sur la
    # narration du 22/10 (1 008 caractères en 55,8 s : 18 caractères par seconde), plus
    # l'arrivée du texte
    for b in blocs[1:]:
        lu = re.sub(r"\[[^\]]*\]", "", b.get("voix", "")).replace("|", "")
        b["duree"] = max(b["duree"], round(len(lu) / 18 + 1.0, 1))
    script = dict(entete, bandeau=BANDEAU, blocs=blocs)
    (D / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lu = " ".join(b.get("voix", "") for b in blocs).replace("|", "")
    mots = len(re.sub(r"\[[^\]]*\]", "", lu).split())
    duree = sum(b["duree"] for b in blocs[1:])
    print(f"{dossier} : {len(blocs)} blocs, {mots} mots lus, {len(lu)} caractères, {duree:.1f} s (sans couverture)")


# --------------------------------------------------------------------------- vaccins au cabinet
episode("2026-10-22-vaccins-cabinet", {
    "slug": "vaccins-cabinet", "date": "2026-10-22", "rubrique": "pro", "label": "Vaccins au cabinet",
    "sous_titre": f"Le vaccin «{NB}gratuit{NB}» que vous *payez d{AP}abord*",
    "appel": f"Notre recommandation{NB}:", "voix_off": "femme_jeune", "badge": "Décret du 9 octobre"}, [
    {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "flu vaccine syringe vial"},
    # décret n° 2026-939, en vigueur le 11 octobre : détention au cabinet ; l'Assurance Maladie :
    # la majoration sert à « récupérer l'avance du coût des doses administrées »
    {"duree": 6.5, "fichier": "B5.mp4", "requete": "vaccine injection syringe",
     "texte": f"Depuis le 11 octobre, vous pouvez stocker *le vaccin grippe*. | "
              f"Mais ces doses, vous les *payez d{AP}abord*.",
     "voix": "[matter-of-fact] Depuis le onze octobre, vous pouvez stocker au cabinet des vaccins contre la "
             "grippe. | [incredulous] Mais ces doses, c’est vous qui les payez d’abord !",
     # le réfrigérateur se remplit de boîtes, puis une pièce « € » sur chacune et l'étiquette ;
     # sous la pastille d'ouverture, il ne tient pas dans le carré
     "insert": {"type": "frigo", "mode": "remplir", "doses": 6, "prix": 1, "carre": False,
                "etiquette": [f"Payées d{AP}abord", "par vous"]}},
    # base de données publique des médicaments : Vaxigrip 11,75 €, Efluelda 23,97 €, hors honoraire
    # de dispensation ; 23,97 > 2 × 11,75
    {"duree": 6.5, "fichier": "B3.mp4", "requete": "pharmacist handing medicine",
     "texte": f"Efluelda, hautement dosé{NB}: *plus du double*. | Prix public, hors honoraire de dispensation.",
     "voix": "Onze euros soixante-quinze la dose de Vaxigrip. Plus du double pour Efluelda. | "
             "C’est le prix public, hors honoraire de dispensation.",
     "insert": {"type": "prix", "pastille": "plus du double", "boites": [
         {"nom": "Vaxigrip", "prix": f"11,75{NB}€"},
         {"nom": "Efluelda", "prix": f"23,97{NB}€", "ton": "rouge"}]}},
    # arrêté du 8 octobre : majoration = prix public du vaccin administré ; SKB standard, SKC
    # hautement dosé ; ameli : injection « dans le cadre d'une consultation sans code acte
    # spécifique » (grippe), « seule cette consultation est facturable » (Covid-19)
    {"duree": 6.5, "fichier": "B1.mp4", "requete": "page : https://www.ameli.fr/medecin/sante-prevention/vaccination/vaccination-grippe-saisonniere",
     "texte": f"La dose vous est remboursée *une fois injectée*. | Et l{AP}injection{NB}? *Pas facturable à part.*",
     "voix": "Une fois injectée, l’Assurance Maladie vous la rembourse, avec la majoration S.K.B. ou S.K.C. | "
             "[incredulous] Et l’injection ? Elle ne se facture pas à part : elle est comprise dans la "
             "consultation.",
     # Impact : « Il facture la consultation ou la visite selon ses modalités habituelles et y ajoute
     # SKB ou SKC »
     "insert": {"type": "ticket", "titre": "Votre facturation", "lignes": [
         {"label": "Dose : SKB ou SKC", "valeur": "remboursée", "ok": True, "temps": 0},
         {"label": "Injection", "valeur": "pas à part", "ok": False, "temps": 1},
         {"label": "Consultation", "valeur": f"comme d{AP}habitude", "ok": True, "temps": 1}]}},
    # ameli : « une enceinte réfrigérée permettant l'enregistrement et la surveillance de la
    # température » ; décret : à compter de la délivrance, transport et détention « s'effectuent sous
    # la responsabilité » du professionnel
    {"duree": 7.0, "fichier": "B7.mp4", "requete": "vials on the table",
     "texte": f"*Enceinte réfrigérée* obligatoire, avec relevé de température. | "
              f"Dès la délivrance, le stock est sous votre responsabilité.",
     "voix": "Il vous faut aussi une enceinte réfrigérée qui enregistre la température. | Et dès la "
             "délivrance, transport et stockage sont sous votre responsabilité.",
     # RCP de Vaxigrip (03/08/2026), rubrique 6.4 : « A conserver au réfrigérateur (entre 2 °C et 8 °C) »
     "insert": [{"type": "frigo", "mode": "releve", "titre": "Température enregistrée"},
                {"type": "tampon", "texte": "Sous votre responsabilité", "temps": 1, "sur": True}]},
    # ni le décret, ni l'arrêté, ni l'Assurance Maladie ne disent ce que devient une dose périmée ou
    # perdue ; CSMF : « les doses perdues ou périmées restent à votre charge »
    {"duree": 7.0, "fichier": "B4.mp4", "requete": "counting coins desk",
     "texte": f"Dose périmée ou perdue{NB}: *aucun texte* ne dit qui paie. | Selon la CSMF, *c{AP}est vous*.",
     "voix": "[curious] Et la dose périmée, ou perdue ? Aucun texte ne dit qui la paie. | [incredulous] Selon "
             "la C.S.M.F., elle reste à votre charge !",
     "insert": {"type": "circuit", "lignes": [
         {"titre": "Dose injectée", "etapes": ["−11,75 €", "+11,75 €"], "fin": "remboursée", "ok": True, "temps": 0},
         {"titre": "Dose perdue ou périmée", "etapes": ["−11,75 €", "? €"], "fin": "à votre charge ?",
          "ok": False, "temps": 1}]}},
    # Ce qui pose question : MG France réserve le dispositif aux patients « disposant d'un bon de prise
    # en charge », l'Assurance Maladie n'en parle pas ; les 2-17 ans sans comorbidité sont pris en
    # charge à 65 %, le dispositif ne vise que les patients à 100 % : exclus ou non, rien ne le dit
    {"duree": 7.5, "fichier": "B6.mp4", "requete": "abstract blue background",
     "texte": f"Faut-il le *bon de prise en charge* du patient{NB}? | "
              f"Et les *2 à 17 ans* sans comorbidité, avec vos doses{NB}?",
     "voix": "Deux autres questions restent ouvertes. Faut-il le bon de prise en charge du patient ? | Et les enfants de deux à dix-sept ans sans comorbidité : "
             "pouvez-vous les vacciner avec vos doses ?",
     "insert": {"type": "icones", "cartes": [
         {"icone": "poubelle", "label": f"Doses perdues{NB}: qui paie{NB}?", "temps": 0},
         {"icone": "bon", "label": f"Bon de prise en charge obligatoire{NB}?", "temps": 0},
         {"icone": "enfant", "label": f"2 à 17 ans sans comorbidité{NB}?", "temps": 1}]}},
    # regard : « construit comme un remboursement, et non comme une rémunération » ; l'arrêté ne prévoit
    # aucune autre rémunération pour la commande, le stockage ou les doses perdues
    {"duree": 5.0, "type": "phrase", "fichier": "B2.mp4", "requete": "doctor typing computer office",
     "texte": f"Remboursé, *pas rémunéré*.",
     "voix": "Le vaccin vous est remboursé. Mais la commande et le stock, eux, ne sont pas payés."},
    # recommandation : ne pas commander plus de doses que de patients ciblés identifiés, renouveler
    # par petites quantités jusqu'au 31 janvier 2027
    {"duree": 5.5, "fichier": "B9.mp4", "requete": "hands writing notebook",
     "texte": f"Combien de doses commander, et *à quel rythme*{NB}? | Notre recommandation, *sur le site*.",
     "voix": "Alors, combien de doses commander, et à quel rythme ? | Notre recommandation est sur le site "
             "du Cercle.",
     "insert": {"type": "verrou", "n": 1}},
])

# --------------------------------------------------------------------------- arrêts de travail
episode("2026-10-22-arrets-travail-mso", {
    "slug": "arrets-travail-mso", "date": "2026-10-22", "rubrique": "pro", "label": "Arrêts de travail",
    "sous_titre": f"Arrêts de travail{NB}: *650 médecins* dans le viseur",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "homme_age", "badge": "Arrêts de travail"}, [
    {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "doctor filling form"},
    # CSMF, 15 octobre : « 650 médecins vont être contrôlés dans le cadre d'une nouvelle campagne
    # MSO/MSAP lancée par les CPAM »
    {"duree": 5.5, "type": "chiffre", "valeur": 650, "suffixe": f"{NB}médecins", "fichier": "B2.mp4",
     "legende": f"vont être contrôlés, *selon la CSMF*", "requete": "envelopes letters",
     "voix": "Six cent cinquante médecins vont être contrôlés sur leurs arrêts de travail, selon la C.S.M.F."},
    # MG France : campagne présentée le 14 octobre aux syndicats ; courriers « prochainement »,
    # « précédés en principe d'un appel téléphonique »
    {"duree": 7.0, "fichier": "B4.mp4", "requete": "telephone pink background",
     "texte": f"Retour de la *mise sous objectifs*. | Les courriers arrivent, en principe *après un appel*.",
     "voix": "L’Assurance Maladie relance la mise sous objectifs. | Selon MG France, les courriers partiront "
             "bientôt, précédés en principe d’un appel.",
     # CSMF : « Dès réception d'un appel téléphonique de votre CPAM »
     "insert": {"type": "appel", "temps": 1, "etapes": [
         {"icone": "telephone", "label": "Appel de votre CPAM", "note": "en principe"},
         {"icone": "courrier", "label": "Puis le courrier"}]}},
    # campagne précédente (jusqu'au 30 juin 2026) : 10 % de prescripteurs au nombre moyen d'IJ par
    # patient actif le plus élevé, ou prescriptions au moins 2 fois supérieures à la moyenne
    {"duree": 7.5, "fichier": "B8.mp4", "requete": "tablet charts data",
     "texte": f"Déjà visés{NB}: les *10{NB}%* qui prescrivent le plus d{AP}IJ par patient actif. | "
              f"Ou *au moins 2 fois* la moyenne.",
     "voix": "La dernière campagne visait les dix pour cent de médecins qui prescrivent le plus d’indemnités "
             "journalières par patient actif, | ou au moins deux fois plus que la moyenne.",
     "insert": {"type": "barres", "unite": "×", "lignes": [
         {"label": "La moyenne", "valeur": 1, "temps": 0},
         {"label": "Ciblés à partir de", "valeur": 2, "temps": 1}]}},
    # au 22 octobre, rien sur ameli.fr ; L. 162-1-15 : « pour une activité comparable », sans méthode
    {"duree": 5.5, "fichier": "B3.mp4", "requete": "man at computer monitor",
     "texte": f"Et cette fois{NB}? *Aucun critère* publié. | Pas une ligne sur ameli.fr.",
     "voix": "[incredulous] Et cette fois ? Aucun critère publié. | Au vingt-deux octobre, pas une ligne sur "
             "ameli.fr.",
     "insert": [{"type": "loupe", "site": "ameli.fr", "recherche": "mise sous objectifs", "vide": "Aucun résultat"},
                {"type": "tampon", "texte": "Non publiés", "temps": 1, "sur": True}]},
    # SOS IJ, 20 octobre : téléservice pour les situations complexes d'arrêt de travail, premier retour
    # sous 48 heures ; 14 -> 20 octobre = 6 jours
    {"duree": 7.0, "fichier": "B7.mp4", "requete": "page : ameli, SOS IJ",
     "texte": f"6 jours plus tard, elle lance *SOS IJ*. | Pour les arrêts complexes{NB}: 1re réponse sous 48{NB}h.",
     "voix": "Six jours plus tard, la même Assurance Maladie lance S.O.S. I.J. : | une aide pour les arrêts "
             "complexes, avec une première réponse sous quarante-huit heures.",
     "insert": {"type": "duel", "cartes": [
         {"date": "14 octobre", "texte": "Une campagne de contrôle", "ok": False, "temps": 0},
         {"date": "20 octobre", "texte": "Un outil pour vous aider", "ok": True, "temps": 0}]}},
    # regard : « L'Assurance Maladie envoie 2 messages contraires la même semaine »
    {"duree": 3.5, "type": "phrase", "fichier": "B1.mp4", "requete": "office telephone",
     "texte": f"*Deux messages* contraires.",
     "voix": "Deux messages contraires, la même semaine."},
    # SOS IJ porte notamment sur des arrêts prolongés par le poste, l'employeur ou la situation sociale,
    # qui pèsent sur le critère de la campagne précédente ; rien de ce qu'a publié l'Assurance Maladie
    # ne relie les 2 dispositifs
    {"duree": 7.0, "fichier": "B6.mp4", "requete": "signing certificate",
     "texte": f"SOS IJ{NB}: les arrêts qui durent à cause *du poste*… | "
              f"Sortiront-ils *du calcul*{NB}? L{AP}Assurance Maladie n{AP}en dit rien.",
     "voix": "S.O.S. I.J. vise notamment les arrêts qui durent à cause du poste, de l’employeur ou d’une "
             "fragilité sociale. | Sortiront-ils du calcul qui cible les médecins ? L’Assurance "
             "Maladie n’en dit rien.",
     # les parts sont une illustration, pas une mesure : aucun chiffre n'est affiché
     "insert": {"type": "calcul", "titre": "Le calcul qui cible les médecins", "temps_question": 1, "parts": [
         {"label": "Vos arrêts de travail", "valeur": 0.68},
         {"label": "Arrêts signalés dans SOS IJ", "valeur": 0.32, "question": True}]}},
    # CSS R. 148-1 (1 mois pour les observations), R. 148-3 (15 jours pour refuser, silence = accepté)
    {"duree": 8.0, "fichier": "B5.mp4", "requete": "marking calendar",
     "texte": f"Ciblé{NB}? *1 mois* pour vos observations. | *15 jours* pour refuser. Sans réponse, c{AP}est accepté.",
     "voix": "Si vous êtes ciblé : un mois pour vos observations, | puis quinze jours pour refuser la "
             "mise sous objectifs. Sans réponse, elle est considérée comme acceptée.",
     "insert": {"type": "frise", "etapes": [
         {"label": "Vos chiffres notifiés", "temps": 0},
         {"label": "1 mois : vos observations", "temps": 0},
         {"label": "Proposition de MSO", "temps": 1},
         {"label": "15 jours pour refuser", "temps": 1},
         {"label": "Sans réponse : acceptée", "alerte": True, "temps": 1}]}},
    # recommandation : contacter son syndicat dès l'appel de la caisse, sans attendre le courrier
    {"duree": 5.0, "fichier": "B9.mp4", "requete": "notebook phone desk",
     "texte": f"Votre caisse vous appelle{NB}? | Ce qu{AP}il faut faire, *dès l{AP}appel*.",
     "voix": "Votre caisse vous appelle ? | Ce qu’il faut faire, dès l’appel, est sur le site du Cercle.",
     "insert": {"type": "verrou", "n": 2}},
])
