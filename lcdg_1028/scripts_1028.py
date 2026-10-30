"""Reels du 28/10/2026 : « 4e année : les docteurs juniors arrivent le 2 novembre » et « Accès direct
aux IPA en CPTS ». Au niveau du reel arrêts de travail (illustration animée sur presque chaque plan),
et selon le conseil reçu par Romain : le public nommé dès la première phrase (« Maîtres de stage : »,
« Médecins traitants : »), en pastille d'ouverture et dans la voix, avec le vocabulaire du métier.

Chaque fait vient des dossiers du Cercle (PDF du 28/10/2026, Téléchargements) :

Docteurs juniors (LCDG_dossier_4e-annee-docteurs-juniors.pdf)
- 2 novembre 2026, pour un an ; autonomie supervisée ; « le docteur junior consulte seul, mais sous
  la responsabilité de son maître de stage, selon l'instruction » ;
- il facture avec sa propre carte CPS ; il « ne peut, en aucun cas, facturer des actes avec la carte
  CPS » du maître de stage : ce serait une fraude, l'Assurance Maladie réalisera des contrôles ;
- regard : « Sans carte CPS au 2 novembre, son docteur junior ne peut pas facturer » ; au 28 octobre,
  aucune information officielle sur le nombre de cartes délivrées ;
- en cabinet, la totalité des tickets modérateurs revient au maître de stage, quel que soit le mode
  de paiement ; encaissés en espèces ou par chèque, il doit les reverser ; l'instruction : 210
  consultations mensuelles = 1 200 € de tickets modérateurs (à titre d'illustration) ;
- l'arrêté du 13 mai 2026 a supprimé l'indemnité de 1 200 € bruts par mois prévue pour les charges
  d'encadrement ; regard : « le maître de stage est désormais payé, pour une large part, par les
  tickets modérateurs que produit le docteur junior » ; « Le maître de stage doit rester celui qui
  forme, pas celui qui remplit l'agenda » ;
- MG France : le ministère indique seulement que « le cadre actuel s'appliquera », sans dire si
  l'assurance du maître de stage couvre un docteur junior qui consulte seul ;
- 2 recommandations (maître de stage qui accueille ; médecin qui veut accueillir en 2027).

Accès direct IPA (LCDG_dossier_acces-direct-ipa-cpts.pdf)
- décret n° 2026-985 du 23 octobre 2026 ; Hérault, Loiret, Martinique, Mayotte, Val-d'Oise, Yonne ;
  du 1er décembre 2026, pour 5 ans ; un IPA qui exerce dans une CPTS peut recevoir un patient sans
  orientation médicale, prescrire, puis adresser un compte rendu au médecin traitant ;
- l'IPA du domaine des pathologies chroniques stabilisées peut, « sans diagnostic médical
  préalable », prescrire un antihypertenseur de première ligne pour une hypertension de grade 1 sans
  retentissement, à l'exclusion des bêtabloquants (ou un hypoglycémiant de première ligne dans le
  diabète de type 2) ; ces prescriptions « ne peuvent être renouvelées sans concertation médicale » ;
- regard : le médecin traitant « le découvrira par compte rendu », une « concertation médicale » que
  personne n'organise ; « le décret fait reposer la sécurité du dispositif sur le médecin traitant
  sans le reconnaître » ; le circuit des CPTS de ces 6 départements « servira de modèle » ;
- impact : comptes rendus à lire et à intégrer, patients réorientés à reprendre ; « Le décret ne
  prévoit aucune rémunération du médecin traitant pour ce travail de coordination » ;
- réorientation « en cas de besoin », sans fixer de délai ; rapport final sur « la pertinence d'une
  généralisation » ; 1 recommandation (médecin installé dans l'un des 6 départements).

    python scripts_1028.py"""
import json
from pathlib import Path

EP = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
NB, AP = "\u00a0", "\u2019"
BANDEAU = f"L{AP}analyse complète | sur *notre site*"

JUNIORS = {
    "slug": "docteurs-juniors", "date": "2026-10-28", "rubrique": "pro", "label": "Docteurs juniors",
    "sous_titre": f"Docteur junior{NB}: *qui paie*, qui répond{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "homme_age", "badge": "Maîtres de stage",
    "bandeau": BANDEAU,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "doctor desk stethoscope laptop"},
        {"duree": 8.0, "fichier": "B1.mp4", "requete": "doctor typing computer office",
         "texte": f"Le *2{NB}novembre*, votre docteur junior arrive. | "
                  f"Il consulte seul, et facture avec *sa propre carte CPS*.",
         "voix": "Maîtres de stage : le deux novembre, votre docteur junior arrive. | "
                 "Il consulte seul… et il facture avec sa propre carte C.P.S.",
         "insert": {"type": "carte", "titulaire": "Docteur junior", "ok": True, "temps": 1, "carre": False}},
        {"duree": 7.0, "fichier": "B2.mp4", "requete": "health insurance card hand",
         "texte": f"Il facture avec *votre carte*{NB}? En aucun cas. | "
                  f"Ce serait *une fraude*{NB}: des contrôles sont prévus.",
         "voix": "[incredulous] Et avec votre carte à vous ? En aucun cas ! | "
                 "[serious] Ce serait une fraude, et l’Assurance Maladie fera des contrôles.",
         "insert": [{"type": "carte", "titulaire": "Maître de stage", "ok": False},
                    {"type": "tampon", "texte": "Fraude", "temps": 1, "sur": True}]},
        {"duree": 8.0, "fichier": "B3.mp4", "requete": "mailbox letters",
         "texte": f"Sans sa carte, *pas de facturation*. | "
                  f"Combien de cartes délivrées{NB}? *Aucun chiffre* officiel.",
         "voix": "Sans sa carte, il ne peut pas facturer. | [curious] Combien de cartes ont été délivrées ? "
                 "[incredulous] Au vingt-huit octobre, aucun chiffre officiel !",
         "insert": {"type": "compteur", "titre": "Cartes CPS délivrées", "date": "au 28 octobre",
                    "pilule": "Aucun chiffre officiel", "temps": 1}},
        {"duree": 8.0, "fichier": "B4.mp4", "requete": "coins money table",
         "texte": f"En cabinet, ses tickets modérateurs{NB}: *tous pour vous*. | "
                  f"Encaissés en espèces{NB}? Il doit *vous les reverser*.",
         "voix": "En cabinet, les tickets modérateurs de ses consultations vous reviennent, en totalité. | "
                 "Et s’il les encaisse en espèces ou par chèque, il doit vous les reverser.",
         "insert": {"type": "circuit", "lignes": [
             {"titre": "En cabinet : son ticket modérateur", "etapes": ["Son patient", "Vous"],
              "fin": "en totalité", "ok": True},
             {"titre": "Encaissé en espèces ou par chèque", "etapes": ["Lui", "Vous"], "fin": "reversé",
              "ok": True, "temps": 1}]}},
        {"duree": 6.0, "type": "chiffre", "valeur": 1200, "suffixe": f"{NB}€", "fichier": "B5.mp4",
         "requete": "calculator desk paper",
         "legende": f"de tickets modérateurs par mois pour *210 consultations*",
         "voix": "À titre d’exemple, l’instruction estime ses tickets modérateurs à mille deux cents euros par "
                 "mois, pour deux cent dix consultations."},
        {"duree": 9.0, "fichier": "B6.mp4", "requete": "payslip documents desk",
         "texte": f"L{AP}indemnité de 1{NB}200{NB}€ par mois{NB}? *Supprimée* en mai. | "
                  f"Pour le Cercle, *son activité* vous paie en large part.",
         "voix": "[serious] Mais l’indemnité prévue pour l’encadrement, mille deux cents euros bruts par mois, "
                 "a été supprimée en mai. | Pour le Cercle, vous voilà payé, pour une large part, par les "
                 "tickets modérateurs de votre docteur junior.",
         "insert": {"type": "ticket", "titre": "Ce qui change", "lignes": [
             {"label": f"Indemnité de 1{NB}200{NB}€", "valeur": "supprimée", "ok": False},
             {"label": "Ses tickets modérateurs", "valeur": "pour vous", "ok": True, "temps": 1}]}},
        {"duree": 5.0, "type": "phrase", "fichier": "B7.mp4", "requete": "open book stethoscope",
         "texte": f"Former, pas *remplir l{AP}agenda*.",
         "voix": "[serious] Et le maître de stage doit rester celui qui forme… "
                 "pas celui qui remplit l’agenda."},
        {"duree": 10.0, "fichier": "B8.mp4", "requete": "page : MG France",
         "texte": f"Il consulte seul, sous *votre responsabilité*. | "
                  f"Votre assurance{NB}? Selon MG France, *rien de précisé*.",
         "voix": "Il consulte seul, mais sous votre responsabilité. | [curious] Et s’il se trompe ? Selon "
                 "MG France, le ministère dit seulement que « le cadre actuel s’appliquera »… "
                 "[incredulous] sans dire si votre assurance le couvre !",
         "insert": {"type": "bouclier", "temps": 1, "pilules": [
             {"texte": "Sous votre responsabilité"},
             {"texte": f"Votre assurance le couvre{NB}?", "ton": "rouge", "temps": 1}]}},
        {"duree": 7.0, "fichier": "B9.mp4", "requete": "doctor desk notebook",
         "texte": f"Un docteur junior le 2{NB}novembre, ou en 2027{NB}? | "
                  f"Ce qu{AP}il faut faire *avant son arrivée*.",
         "voix": "[warm] Un docteur junior le deux novembre… ou en deux mille vingt-sept ? | "
                 "Ce qu’il faut faire avant son arrivée, on vous le détaille sur le site du Cercle.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

DEPARTEMENTS = [("34", "Hérault"), ("45", "Loiret"), ("972", "Martinique"), ("976", "Mayotte"),
                ("95", f"Val-d{AP}Oise"), ("89", "Yonne")]
IPA = {
    "slug": "acces-direct-ipa", "date": "2026-10-28", "rubrique": "pro", "label": "Accès direct · 6 départements",
    "sous_titre": f"Vos patients *chez l{AP}IPA*, sans passer par vous{NB}?",
    "appel": f"Notre recommandation{NB}:", "voix_off": "femme_agee", "badge": "Médecins traitants",
    "bandeau": BANDEAU,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "nurse blood pressure cuff"},
        {"duree": 10.0, "fichier": "B1.mp4", "requete": "nurse consultation hands",
         "texte": f"Dès le *1er{NB}décembre*, dans 6{NB}départements… | "
                  f"vos patients pourront voir un IPA de CPTS *sans passer par vous*.",
         "voix": "Médecins traitants : à partir du premier décembre, et pour cinq ans, dans six départements… | "
                 "vos patients pourront consulter un infirmier en pratique avancée de C.P.T.S., sans passer "
                 "par vous.",
         "insert": {"type": "departements", "carre": False,
                    "liste": [{"numero": n, "nom": d} for n, d in DEPARTEMENTS]}},
        {"duree": 6.0, "fichier": "B2.mp4", "requete": "nurse writing notes",
         "texte": f"Il les reçoit, prescrit ce qu{AP}un *arrêté* autorise… | puis vous adresse *un compte rendu*.",
         "voix": "Il les reçoit, il prescrit ce qu’un arrêté autorise… | puis il vous adresse un compte rendu.",
         "insert": {"type": "appel", "etapes": [
             {"icone": "infirmier", "label": "Un IPA de CPTS", "note": f"prescrit selon l{AP}arrêté"},
             {"icone": "courrier", "label": "Votre compte rendu", "temps": 1}]}},
        {"duree": 12.0, "fichier": "B3.mp4", "requete": "blood pressure monitor arm",
         "texte": f"L{AP}IPA en pathologies chroniques stabilisées peut même… | "
                  f"instaurer *un antihypertenseur*… | *sans diagnostic* médical préalable.",
         "voix": "[serious] Et l’I.P.A. en pathologies chroniques stabilisées peut même… | instaurer un "
                 "antihypertenseur… | sans diagnostic médical préalable. De première ligne, pour une "
                 "hypertension de grade un sans retentissement, hors bêtabloquants.",
         "insert": {"type": "ordonnance", "titre": "Ordonnance", "marque": "IPA", "lignes": [
             {"label": "Antihypertenseur de 1re ligne",
              "note": "HTA de grade 1 sans retentissement, hors bêtabloquants", "temps": 1}],
             "pied": "Sans diagnostic médical préalable", "temps_pied": 2}},
        {"duree": 9.0, "fichier": "B4.mp4", "requete": "doctor reading letter",
         "texte": f"Vous l{AP}apprenez *par compte rendu*. | "
                  f"Le renouveler{NB}? Il faut une *concertation médicale*… | *Organisée par qui*{NB}?",
         "voix": "Vous, vous l’apprenez par le compte rendu. | Et pour le renouveler ? Il faut une concertation "
                 "médicale… | [curious] Organisée par qui ?",
         "insert": {"type": "icones", "cartes": [
             {"icone": "compte_rendu", "label": "Le compte rendu", "question": False},
             {"icone": "concertation", "label": "Concertation médicale", "temps": 1, "temps_question": 2}]}},
        {"duree": 9.0, "fichier": "B5.mp4", "requete": "doctor paperwork desk",
         "texte": f"Comptes rendus à intégrer, patients à reprendre… | "
                  f"Ce travail{NB}? *Aucune rémunération* prévue.",
         "voix": "Des comptes rendus à lire et à intégrer, des patients réorientés à reprendre… | "
                 "[incredulous] et pour ce travail de coordination, le décret ne prévoit aucune rémunération "
                 "du médecin traitant !",
         "insert": [{"type": "pilule", "texte": "Aucune rémunération prévue", "temps": 1},
                    {"type": "icones", "cartes": [
                        {"icone": "compte_rendu", "label": "Comptes rendus à intégrer", "question": False},
                        {"icone": "patient", "label": "Patients réorientés à reprendre", "question": False}]}]},
        {"duree": 8.0, "fichier": "B6.mp4", "requete": "wall clock waiting room",
         "texte": f"Un patient réorienté vers vous{NB}? | "
                  f"Repris *dans quel délai*{NB}? Le décret n{AP}en fixe aucun.",
         "voix": "[curious] Et quand l’I.P.A. vous réoriente un patient… | dans quel délai le reprendre ? "
                 "Le décret n’en fixe aucun.",
         "insert": {"type": "sablier", "pilules": [
             {"texte": f"Repris dans quel délai{NB}?"},
             {"texte": "Aucun délai fixé", "ton": "rouge", "temps": 1}]}},
        {"duree": 6.0, "type": "phrase", "fichier": "B7.mp4", "requete": "doctor window desk",
         "texte": f"La sécurité{NB}? *Vous*, sans être reconnu.",
         "voix": "[serious] Pour le Cercle, le décret fait reposer la sécurité du dispositif sur vous… "
                 "sans vous reconnaître."},
        {"duree": 9.0, "fichier": "B8.mp4", "requete": "page : décret",
         "texte": f"Et après{NB}? *La généralisation*{NB}? | Pour le Cercle, ces CPTS *serviront de modèle*.",
         "voix": "Et après ? Le rapport final devra se prononcer sur la pertinence d’une généralisation. | "
                 "Pour le Cercle, ces C.P.T.S. serviront de modèle.",
         # le rapport au Parlement est remis au plus tard 6 mois avant le terme des 5 ans
         "insert": {"type": "frise", "etapes": [
             {"label": f"1er{NB}décembre 2026{NB}: début"},
             {"label": f"Rapport{NB}: généraliser{NB}?", "alerte": True},
             {"label": "Fin des 5 ans"}]}},
        {"duree": 7.0, "fichier": "B9.mp4", "requete": "doctor desk notebook pen",
         "texte": f"Médecin dans l{AP}un de ces 6{NB}départements{NB}? | "
                  f"Ce qu{AP}il faut faire *avant le 1er{NB}décembre*.",
         "voix": "[warm] Vous exercez dans l’un de ces six départements ? | Ce qu’il faut faire avant le premier "
                 "décembre, on vous le détaille sur le site du Cercle.",
         "insert": {"type": "verrou", "n": 1}},
    ]}

for ep in (JUNIORS, IPA):
    d = EP / f"{ep['date']}-{ep['slug']}"
    (d / "broll").mkdir(parents=True, exist_ok=True)
    f = d / "script.json"
    if f.exists():                                  # garder les plans déjà choisis
        ancien = json.loads(f.read_text(encoding="utf-8"))
        for b, a in zip(ep["blocs"], ancien["blocs"]):
            b["requete"] = a.get("requete", b["requete"])
            for cle in ("cadrage", "credit"):
                if cle in a:
                    b[cle] = a[cle]
    f.write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    texte = " ".join((b.get("voix") or "") for b in ep["blocs"])
    print(f"{d.name} : {len(ep['blocs'])} blocs, {len(texte)} caractères lus")
