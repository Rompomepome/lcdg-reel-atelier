"""Reel « minimum de patients par medecin traitant » (dossier du 13/10/2026, reel booste en ads).
Chaque fait verifie le 16/10/2026 dans le rapport de la Cour des comptes (septembre 2026) et la
proposition de loi n° 3264 (Assemblee nationale, 6 octobre 2026)."""
import json
from pathlib import Path

D = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes\2026-10-13-minimum-patients")
NB, AP = "\u00a0", "\u2019"
modele = json.loads((D.parent / "2026-09-21-desogestrel" / "script.json").read_text(encoding="utf-8"))
script = {
    "slug": "minimum-patients",
    "date": "2026-10-13",
    "rubrique": "pro",
    "label": "Médecin traitant",
    "sous_titre": f"Un minimum de patients *obligatoire* pour vous{NB}?",
    "appel": modele["appel"],                                   # « Nos 3 recommandations : »
    "bandeau": modele["bandeau"].replace("*DESO*", "*500*"),
    # Romain, 16/10 : une femme, une voix qui reagit (« pardon ?! »), interrogative et surprise.
    # La surprise porte sur l'obligation et sur ce que personne ne dit (sanction, decompte),
    # jamais sur le chiffre de 500 : la moyenne est de 1 130, s'en indigner serait trompeur.
    # 20/10 : Jeanne (bibliotheque), « plus jeune donc plus punchy » ; femme_agee resonnait
    "voix_off": "femme_jeune",
    "badge": "Cour des comptes",
    "blocs": [
        {"duree": 3.0, "texte": None, "requete": "busy doctor waiting room patients", "fichier": "B0.mp4"},
        # recommandation n° 2 : « Rendre obligatoire [...] un seuil minimal de patientele prise en charge
        # en tant que medecin traitant, pour tout medecin generaliste liberal installe »
        {"duree": 7.0,
         "texte": f"La Cour des comptes veut un minimum de patients *obligatoire*. | "
                  f"Pour chaque généraliste libéral installé.",
         "requete": "page : https://www.ccomptes.fr/fr/publications/le-dispositif-du-medecin-traitant",
         "fichier": "B1.mp4",
         # « Pardon ?! » retire par Romain le 16/10 : coupe dans la lecture validee (couper_pardon.py)
         # le medecin est medecin traitant, jamais le patient (Romain, 16/10) ; titre du dossier :
         # « la Cour des comptes veut imposer un minimum de patients a chaque generaliste »
         "voix": "[incredulous] La Cour des comptes veut imposer un minimum de patients ? | [emphatic] "
                 "À chaque généraliste libéral installé !"},
        # « Le seuil de 500 patients [...] pourrait etre envisage »
        {"duree": 5.5, "type": "chiffre", "valeur": 500, "suffixe": f"{NB}patients",
         # Romain, 16/10 : « c'est 500 patients par medecin traitant » (relu seul, revoix.py)
         "legende": "par médecin traitant, le seuil que la Cour *envisage*.",
         "requete": "crowded waiting room clinic", "fichier": "B2.mp4", "cadrage": "largeur",
         "voix": "[curious] Et le seuil qu’elle envisage ? Cinq cents patients par médecin traitant."},
        # 8 553 generalistes liberaux sous le seuil de 200 patients medecin traitant vus dans l'annee
        {"duree": 6.5, "type": "chiffre", "valeur": 8553,
         # recenses en 2024 : l'annee se dit et s'affiche
         "legende": "généralistes libéraux étaient médecin traitant de moins de *200 patients* vus en 2024.",
         "requete": "doctors walking hospital corridor", "fichier": "B3.mp4",
         "voix": "En deux mille vingt-quatre, huit mille cinq cent cinquante-trois généralistes libéraux "
                 "étaient le médecin traitant de moins de deux cents patients vus dans l’année. [surprised] "
                 "Voire d’aucun !"},
        # tableau 14 : grands centres urbains 75 % (contre 50 % des medecins traitants)
        {"duree": 6.0,
         "texte": f"Qui sont-ils{NB}? | 3 sur 4 exercent dans un *grand centre urbain*.",
         "requete": "aerial view big city France", "fichier": "B4.mp4",
         "voix": "[curious] Qui sont-ils ? | Trois sur quatre exercent dans un grand centre urbain. "
                 "Chez l’ensemble des médecins traitants, c’est un sur deux.",
         "insert": {"type": "barres", "suffixe": " %", "lignes": [
             {"label": "Les 8 553", "valeur": 75, "temps": 1},
             {"label": "Les médecins traitants", "valeur": 50, "reference": True, "temps": 1}]}},
        # PPL n° 3264 : fraction minimale >= 30 % de la patientele ; sans mesure conventionnelle dans
        # les 12 mois suivant la promulgation, le ministre la fixe (apres avis HAS et CNOM)
        {"duree": 8.0,
         # deposee le 6 octobre, pas adoptee : « prevoit », jamais « a retenu » ni « fixe »
         # « fraction minimale de patients qui ont designe le medecin comme medecin traitant [...] ne
         # peut etre inferieure a 30 % de la patientele »
         # « La convention determine ladite fraction » ; « Si, dans les douze mois suivant la
         # promulgation [...] », le ministre la fixe
         "texte": f"Une proposition de loi prévoit qu{AP}au moins *30{NB}%* de vos patients vous aient "
                  f"déclaré médecin traitant. | "
                  f"Si la convention ne fixe pas ce seuil en 12{NB}mois, le ministre le fixerait.",
         "requete": "page : https://www.assemblee-nationale.fr/dyn/17/textes/l17b3264_proposition-loi",
         "fichier": "B5.mp4",
         "voix": "[excited] Et ce n’est pas tout ! Le six octobre, des députés ont déposé une proposition de "
                 "loi. Elle prévoit qu’au moins trente pour cent de vos patients vous aient déclaré médecin "
                 "traitant. | [shocked] Et si la convention médicale ne fixe pas ce seuil dans l’année qui "
                 "suit la loi ? C’est le ministre qui le fixerait !"},
        {"duree": 4.5, "type": "phrase",
         "texte": f"Rien ne s{AP}applique aujourd{AP}hui. | Mais deux questions restent *sans réponse*.",
         "requete": "doctor looking out window thinking", "fichier": "B6.mp4",
         "voix": "[reassuring] Rassurez-vous : rien de tout cela ne s’applique aujourd’hui. | [intrigued] "
                 "Mais deux questions restent sans réponse."},
        # le rapport ne dit pas si le seuil compte les patients declares ou vus ; la PPL compte les
        # patients qui ont designe le medecin ; ni l'un ni l'autre ne prevoit de consequence
        {"duree": 8.0,
         "texte": f"Patients déclarés ou patients vus{NB}? Le rapport ne le dit pas. | "
                  f"Et sous le seuil, que risqueriez-vous{NB}? | "
                  f"Ni le rapport ni la proposition de loi *ne le disent*.",
         "requete": "doctor reviewing patient files", "fichier": "B7.mp4",
         "voix": "[curious] Le seuil compterait-il vos patients déclarés ? Ou vos patients vus ? Le rapport "
                 "ne le dit pas. | [concerned] Et sous le seuil, que risqueriez-vous ? | [incredulous] Ni le "
                 "rapport, ni la proposition de loi ne le disent !"},
        # 1 130 patients medecin traitant en moyenne en 2024, contre 919 en 2016
        {"duree": 6.0, "type": "chiffre", "valeur": 1130, "depuis": 919, "suffixe": f"{NB}patients",
         "legende": "suivis en moyenne par un médecin traitant libéral, *en 2024*.",
         "requete": "doctor consultation patient office", "fichier": "B8.mp4",
         "voix": "[thoughtful] Pour rappel, en deux mille vingt-quatre, un médecin traitant libéral suivait "
                 "en moyenne mille cent trente patients. Contre neuf cent dix-neuf en deux mille seize."},
        {"duree": 4.5,
         "texte": f"Êtes-vous concerné{NB}? | Le Cercle fait *3{NB}recommandations*.",
         "requete": "general practitioner desk", "fichier": "B9.mp4",
         "voix": "[warm] Alors, êtes-vous concerné ? | [cheerful] Le Cercle vous donne trois "
                 "recommandations concrètes, sur son site.",
         "insert": {"type": "verrou", "n": 3}},
    ],
}
D.mkdir(parents=True, exist_ok=True)
(D / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
lu = " ".join(b.get("voix", "") for b in script["blocs"]).replace("|", "")
print(D / "script.json", "-", len(lu.split()), "mots lus,", len(lu), "caracteres")
