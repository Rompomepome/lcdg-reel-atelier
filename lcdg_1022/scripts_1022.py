"""Trois reels LCDG du 22/10/2026, tirés des dossiers du jour : vaccins au cabinet (SKA, SKB,
SKC), arrêts de travail (mise sous objectifs, SOS IJ), cumul emploi-retraite en 2027.

Romain, 22/10/2026 : personne ne commente, l'objectif est d'envoyer vers le site. Le bandeau
ne demande plus de commenter un mot clé : il renvoie à l'analyse complète sur le site
(formule valable sur Instagram comme sur LinkedIn).

Chaque phrase vient du dossier correspondant (Downloads/LCDG_dossier_*.pdf), dont le texte
est dans ce dossier (*.txt). Les syndicats sont cités pour ce qu'ils rapportent, toujours
attribués."""
import json
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
NB, AP = "\u00a0", "\u2019"
BANDEAU = f"L{AP}analyse complète | sur *notre site*"


def episode(dossier, entete, blocs):
    D = R / dossier
    D.mkdir(parents=True, exist_ok=True)
    script = dict(entete, bandeau=BANDEAU, blocs=blocs)
    for i, b in enumerate(blocs):
        b.setdefault("fichier", f"B{i}.mp4")
    (D / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lu = " ".join(b.get("voix", "") for b in blocs).replace("|", "")
    import re
    mots = len(re.sub(r"\[[^\]]*\]", "", lu).split())
    print(f"{dossier} : {len(blocs)} blocs, {mots} mots lus, {len(lu)} caractères")


# --------------------------------------------------------------------------- vaccins au cabinet
episode("2026-10-22-vaccins-cabinet", {
    "slug": "vaccins-cabinet", "date": "2026-10-22", "rubrique": "pro", "label": "Vaccins au cabinet",
    "sous_titre": f"Vaccins au cabinet{NB}: *qui paie* les doses perdues{NB}?",
    "appel": f"Notre recommandation{NB}:", "voix_off": "homme_jeune", "badge": "Nouveau décret"}, [
    {"duree": 3.0, "texte": None, "requete": "flu vaccine syringe vial close up"},
    # décret n° 2026-939 du 9 octobre 2026, entré en vigueur le 11 octobre
    {"duree": 7.0, "texte": f"Depuis le 11 octobre, les vaccins *au cabinet*. | Grippe et Covid-19, encadrés par un décret.",
     "requete": "page : ameli, vaccination grippe, espace médecin",
     "voix": "Depuis le onze octobre, un décret vous permet de garder au cabinet les vaccins contre la grippe "
             "et le Covid-19. | Il fixe les règles de détention et de conservation."},
    # arrêté du 8 octobre 2026, en vigueur le 13 octobre : 3 majorations
    {"duree": 7.0, "texte": f"Depuis le 13 octobre, *3 majorations*. | SKB{NB}: grippe standard. SKC{NB}: hautement dosé. SKA{NB}: Covid-19.",
     "requete": "medical billing computer doctor desk",
     "voix": "Depuis le treize octobre, trois majorations remboursent la dose : | S.K.B. pour la grippe "
             "standard, S.K.C. pour le vaccin hautement dosé, S.K.A. pour le Covid-19."},
    # base de données publique des médicaments : Vaxigrip 11,75 € ; la majoration = prix public du vaccin administré
    {"duree": 6.0, "type": "chiffre", "valeur": 11.75, "decimales": 2, "suffixe": f"{NB}€",
     "legende": f"la dose de Vaxigrip{NB}: vous *l{AP}avancez* au pharmacien",
     "requete": "pharmacist handing medicine box hands",
     "voix": "Le principe : vous avancez le prix des doses au pharmacien. Une dose de Vaxigrip : onze euros "
             "soixante-quinze. S.K.B. vous la rembourse quand vous l’injectez."},
    # SKA : 0,02 € pour les vaccins Covid-19 du stock de l'État, jusqu'à épuisement de ce stock
    {"duree": 5.5, "type": "chiffre", "valeur": 0.02, "decimales": 2, "suffixe": f"{NB}€",
     "legende": f"SKA, pour un vaccin Covid-19 du *stock de l{AP}État*",
     "requete": "coins euro small change table",
     "voix": "Pour le Covid-19, le vaccin vient du stock de l’État : S.K.A. vaut deux centimes."},
    # ameli, grippe : injection « dans le cadre d'une consultation sans code acte spécifique »
    {"duree": 6.0, "texte": f"L{AP}injection, elle, n{AP}a *pas de code*. | Elle se fait dans la consultation.",
     "requete": "vaccine injection upper arm",
     "voix": "Et l’injection n’a pas de code propre : | elle se fait dans le cadre de la consultation."},
    {"duree": 4.5, "type": "phrase", "texte": f"Mais *3 questions* restent sans réponse.",
     "requete": "medical refrigerator vaccines",
     "voix": "Mais trois questions restent sans réponse."},
    # Ce qui pose question : doses perdues ou périmées ; bon de prise en charge exigé ?
    {"duree": 7.0, "texte": f"Qui paie une dose *perdue ou périmée*{NB}? | Le bon de prise en charge est-il exigé{NB}?",
     "requete": "expired medicine vials disposal",
     "voix": "Qui paie une dose perdue, ou périmée ? | Le bon de prise en charge est-il exigé ?"},
    # enfants de 2 à 17 ans sans comorbidité (pris en charge à 65 %, sans bon)
    {"duree": 7.0, "texte": f"Les enfants de 2 à 17 ans sans comorbidité sont-ils *exclus*{NB}? | Au 22 octobre, aucun texte ne répond clairement.",
     "requete": "child pediatric vaccination band aid arm",
     "voix": "Et les enfants de deux à dix-sept ans sans comorbidité, sont-ils exclus ? | Au vingt-deux octobre, "
             "aucun texte n’y répond clairement."},
    {"duree": 5.0, "texte": f"Comment commander *sans y perdre*{NB}? | Notre recommandation, sur le site du Cercle.",
     "requete": "doctor desk laptop notes",
     "voix": "Alors, comment commander sans y perdre ? | Le Cercle vous donne sa recommandation sur son site.",
     "insert": {"type": "verrou", "n": 1}},
])

# --------------------------------------------------------------------------- arrêts de travail
episode("2026-10-22-arrets-travail-mso", {
    "slug": "arrets-travail-mso", "date": "2026-10-22", "rubrique": "pro", "label": "Arrêts de travail",
    "sous_titre": f"Arrêts de travail{NB}: *650 médecins* dans le viseur{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "homme_age", "badge": "Mise sous objectifs"}, [
    {"duree": 3.0, "texte": None, "requete": "doctor writing sick note prescription"},
    # MG France : annoncée le 14 octobre aux syndicats par le directeur général de l'Assurance Maladie
    {"duree": 7.0, "texte": f"Une nouvelle campagne de *mise sous objectifs*. | Annoncée aux syndicats le 14 octobre.",
     "requete": "office phone ringing desk",
     "voix": "L’Assurance Maladie prépare une nouvelle mise sous objectifs sur les arrêts de travail. | "
             "Elle l’a annoncée aux syndicats le quatorze octobre, selon MG France."},
    # CSMF, 15 octobre : « 650 médecins vont être contrôlés »
    {"duree": 5.5, "type": "chiffre", "valeur": 650, "suffixe": f"{NB}médecins",
     "legende": f"vont être contrôlés, *selon la CSMF*",
     "requete": "stack of letters envelopes mail",
     "voix": "Six cent cinquante médecins vont être contrôlés, selon la C.S.M.F."},
    # Au 22 octobre, aucune information sur ameli.fr
    {"duree": 6.0, "texte": f"Les critères de ciblage{NB}? | Au 22 octobre, *rien de publié* sur ameli.fr.",
     "requete": "statistics chart on screen",
     "voix": "Les critères de ciblage ? | Au vingt-deux octobre, l’Assurance Maladie n’a rien publié sur ameli.fr."},
    # MG France : courriers « prochainement », « précédés en principe d'un appel téléphonique »
    {"duree": 6.0, "texte": f"D{AP}abord, un appel de votre CPAM. | Puis un courrier, *prochainement*.",
     "requete": "smartphone incoming call on desk",
     "voix": "Le scénario annoncé : un appel de votre caisse, | puis un courrier, prochainement, selon MG France."},
    # CSS, R. 148-1 et R. 148-3
    {"duree": 7.0, "texte": f"*1 mois* pour présenter vos observations. | *15 jours* pour refuser une mise sous objectifs.",
     "requete": "calendar pages deadline",
     "voix": "Les délais sont courts : un mois pour présenter vos observations, | puis quinze jours pour refuser "
             "une mise sous objectifs."},
    {"duree": 4.5, "type": "phrase", "texte": f"Votre silence vaut *acceptation*.",
     "requete": "registered letter envelope",
     "voix": "Et sans réponse dans ce délai, elle est réputée acceptée."},
    # SOS IJ, 20 octobre : 4 thématiques, premier retour sous 48 heures
    {"duree": 7.0, "texte": f"Le 20 octobre, l{AP}Assurance Maladie lance *SOS IJ*. | Pour les arrêts complexes{NB}: 1er retour sous 48{NB}h.",
     "requete": "page : ameli, SOS IJ",
     "voix": "Le vingt octobre, l’Assurance Maladie a lancé S.O.S. I.J. : | un téléservice sur amelipro pour "
             "les arrêts de travail complexes, avec un premier retour sous quarante-huit heures."},
    # Ce qui pose question : un arrêt signalé dans SOS IJ sera-t-il retiré du calcul ?
    {"duree": 7.0, "texte": f"Un arrêt signalé dans SOS IJ sortira-t-il *du calcul*{NB}? | Rien ne le dit.",
     "requete": "doctor looking at laptop screen",
     "voix": "Mais un arrêt signalé dans S.O.S. I.J. sortira-t-il du calcul qui sert à cibler les médecins ? | "
             "Rien de ce qu’a publié l’Assurance Maladie ne le dit."},
    {"duree": 5.0, "texte": f"Votre CPAM vous appelle{NB}? | Ce qu{AP}il faut faire, *dès l{AP}appel*.",
     "requete": "doctor desk phone notepad",
     "voix": "Votre caisse vous appelle ? | Le Cercle vous dit quoi faire, dès l’appel, sur son site.",
     "insert": {"type": "verrou", "n": 2}},
])

# --------------------------------------------------------------------------- cumul emploi-retraite
episode("2026-10-22-cumul-emploi-retraite", {
    "slug": "cumul-emploi-retraite", "date": "2026-10-22", "rubrique": "pro", "label": "Cumul emploi-retraite",
    "sous_titre": f"Retraite avant 67 ans{NB}: votre pension *réduite*{NB}?",
    "appel": f"Notre recommandation{NB}:", "voix_off": "femme_agee", "badge": "Retraite 2027"}, [
    {"duree": 3.0, "texte": None, "requete": "senior doctor stethoscope office back view"},
    # LFSS 2026, article 102 : retraites prenant effet à partir du 1er janvier 2027
    {"duree": 7.0, "texte": f"Retraite à partir de 2027{NB}: le cumul *change*. | Avant 67 ans, vos revenus pourront réduire votre pension.",
     "requete": "page : Service Public, cumul emploi-retraite 2027",
     "voix": "Pour les retraites qui prennent effet dès deux mille vingt-sept, le cumul emploi-retraite change. | "
             "Avant soixante-sept ans, vos revenus pourront réduire votre pension."},
    # Service Public : revenus d'activité et de remplacement (IJ) déduits dès le 1er euro
    {"duree": 7.0, "texte": f"Avant l{AP}âge légal{NB}: déduits *dès le 1er euro*. | Indemnités journalières comprises.",
     "requete": "calculator coins euro",
     "voix": "Avant l’âge légal, vos revenus d’activité seront déduits de la pension dès le premier euro. | "
             "Indemnités journalières comprises."},
    # seuil annoncé de 7 000 € brut par an, que le décret doit encore fixer
    {"duree": 6.0, "type": "chiffre", "valeur": 7000, "suffixe": f"{NB}€",
     "legende": f"brut par an, entre l{AP}âge légal et 67 ans{NB}: le seuil *annoncé*",
     "requete": "doctor consultation desk paperwork",
     "voix": "Entre l’âge légal et soixante-sept ans, le seuil annoncé est de sept mille euros brut par an. "
             "Un décret doit encore le fixer."},
    {"duree": 6.0, "texte": f"Au-delà, la pension baisse de *50{NB}%* du dépassement. | 2{NB}€ gagnés en plus{NB}: 1{NB}€ de pension en moins.",
     "requete": "money banknotes euro counting",
     "voix": "Au-delà, la pension baisse de la moitié du dépassement : | deux euros gagnés en plus, un euro de "
             "pension en moins."},
    # Carmf : 35 000 € de pension, 60 000 € de revenus -> 8 500 €
    {"duree": 6.5, "type": "chiffre", "valeur": 8500, "depuis": 35000, "suffixe": f"{NB}€",
     "legende": f"de pension par an pour 60{NB}000{NB}€ de revenus{NB}: *le calcul de la Carmf*",
     "requete": "retirement savings piggy bank",
     "voix": "L’exemple de la Carmf : trente-cinq mille euros de pension, soixante mille euros de revenus. "
             "La pension tombe à huit mille cinq cents euros."},
    {"duree": 5.0, "texte": f"À partir de 67 ans{NB}: cumul *intégral*, sans plafond.",
     "requete": "elderly doctor hands stethoscope",
     "voix": "À partir de soixante-sept ans, le cumul reste intégral, sans plafond."},
    # Carmf : date d'effet au 1er jour du trimestre civil qui suit la demande
    {"duree": 6.5, "texte": f"À la Carmf, les demandes déposées *après le 30 septembre*. | Elles prennent effet en 2027.",
     "requete": "calendar january new year",
     "voix": "À la Carmf, sont concernées les demandes déposées après le trente septembre : | elles prennent "
             "effet en deux mille vingt-sept."},
    # Ce qui pose question : activités exclues (zones sous-denses, PDSA, régulation), décret attendu
    {"duree": 7.0, "texte": f"Zones sous-denses, permanence des soins, régulation{NB}: *exclues*{NB}? | Un décret doit le dire. Rien n{AP}est publié.",
     "requete": "rural village countryside doctor",
     "voix": "Zones sous-denses, permanence des soins, régulation : seront-elles exclues du calcul ? | "
             "Un décret doit le dire. Rien n’est publié."},
    {"duree": 5.0, "texte": f"Vous comptez liquider avant 67 ans{NB}? | Notre recommandation, *avant de déposer*.",
     "requete": "doctor desk notebook pen",
     "voix": "Vous comptez liquider votre retraite avant soixante-sept ans ? | Lisez d’abord notre recommandation, "
             "sur le site du Cercle.",
     "insert": {"type": "verrou", "n": 1}},
])
