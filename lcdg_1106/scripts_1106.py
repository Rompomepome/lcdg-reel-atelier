"""Reels du 06/11/2026 : « Cotisation à l'Ordre en société » et « Premières installations », réécrits en phrases
construites. Le reel « Soins chez le pharmacien » est abandonné (Romain, 06/11/2026 : « c'est nul comme thème en
fait, il n'y a aucune vraie valeur ajoutée »).

Romain, 06/11/2026, sur les versions d'une minute du 05/11 : « il nous faut de vraies phrases car on ne comprend pas
du tout en fait », « remets à 2 minutes et quelque », puis « peut-être pas autant, mais fais de vraies phrases
construites ! On doit leur apprendre des choses réelles ! ». Donc : environ 1 min 45 à 1 min 55, chaque notion
expliquée (la file active, ce que fait un recours, d'où vient l'écart de 1 à 4), des phrases complètes à l'écran comme
à la voix, l'accroche dès la première phrase, les recommandations gardées pour le site.

Sources : dossiers du Cercle du 3 novembre (lus en entier), flash CSMF du 22/10/2026, communiqué de l'Assurance
Maladie du 22/10/2026, rapport de la Cour des comptes de septembre 2026 (recommandation n° 2), article L. 4 du code
de justice administrative (« les requêtes n'ont pas d'effet suspensif s'il n'en est autrement ordonné par la
juridiction »). Détail des sources : lcdg_1105/scripts_1105.py.

    python scripts_1106.py"""
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
NB, AP = "\u00a0", "\u2019"
BANDEAU = f"L{AP}analyse complète | sur *notre site*"
SEL, SCP = f"Société d{AP}exercice libéral", "Société civile professionnelle"

COTISATION = {
    "slug": "cotisation-ordre", "date": "2026-11-04", "rubrique": "pro", "label": "Cotisation de votre société",
    "sous_titre": f"Relancé par l{AP}Ordre{NB}: *faut-il payer*{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "femme_agee", "badge": "Médecins en société",
    "bandeau": BANDEAU,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "envelope letter desk hands opening"},
        # l'accroche, puis qui est concerné
        {"duree": 9.0, "fichier": "B1.mp4", "requete": "mail envelope hands desk",
         "texte": f"Relancé par l{AP}Ordre{NB}: *faut-il payer*{NB}? | "
                  f"Selon la CSMF, certains qui contestent *sont relancés*.",
         "voix": "[curious] Médecins en société, relancés par l’Ordre : faut-il payer ? | Selon la C.S.M.F., des conseils "
                 "départementaux relancent les médecins qui contestent la cotisation deux mille vingt-six de leur société.",
         "insert": [{"type": "lettre", "carre": False, "entete": f"Conseil départemental de l{AP}Ordre",
                     "titre": "Cotisation 2026 de votre société"},
                    {"type": "tampon", "carre": False, "texte": "Relance", "sur": True, "delai": 0.3}]},
        # ce qu'ils contestent : le barème, expliqué
        {"duree": 11.0, "fichier": "B2.mp4", "requete": "mail envelope hands desk",
         "texte": f"En société d{AP}exercice libéral, chaque associé compte *1,5{NB}cotisation*. | "
                  f"À 4{NB}associés, la société paie *2{NB}190{NB}€* (calcul du Cercle).",
         "voix": "Ce qu’ils contestent, c’est le nouveau barème. En société d’exercice libéral, la société paie une cotisation "
                 "et demie par associé médecin. | À quatre associés, cela fait deux mille cent quatre-vingt-dix euros, selon "
                 "le calcul du Cercle.",
         "insert": {"type": "associes", "lignes": [{"titre": SEL, "ton": "rouge", "montants": [
             {"n": 1, "montant": f"547,50{NB}€"}, {"n": 4, "montant": f"2{NB}190{NB}€", "temps": 1}]}]}},
        {"duree": 9.0, "fichier": "B3.mp4", "requete": "doctors office corridor daylight",
         "texte": f"En société civile professionnelle, c{AP}est *547,50{NB}€*… | "
                  f"quel que soit le nombre d{AP}associés. À 4, c{AP}est *4{NB}fois moins*.",
         "voix": "En société civile professionnelle, c’est cinq cent quarante-sept euros cinquante… | quel que soit le "
                 "nombre d’associés. [incredulous] À quatre, c’est quatre fois moins !",
         "insert": {"type": "associes", "lignes": [
             {"titre": SEL, "ton": "rouge", "montants": [{"n": 4, "montant": f"2{NB}190{NB}€"}]},
             {"titre": SCP, "note": f"quel que soit le nombre d{AP}associés",
              "montants": [{"n": 4, "montant": f"547,50{NB}€"}]}]}},
        # ce que fait un recours, et ce qu'il ne fait pas
        {"duree": 10.0, "fichier": "B9.mp4", "requete": "page : https://www.csmf.org/actualites/flash-info-12/",
         "texte": f"La CSMF a saisi le Conseil d{AP}État{NB}: *pas encore jugé*. | "
                  f"Et ce recours *ne suspend rien*, sauf décision du juge.",
         "voix": "La C.S.M.F. a attaqué ce barème devant le Conseil d’État, mais son recours n’est pas encore jugé. | Et sauf "
                 "si le juge en décide autrement, un recours ne suspend pas la décision attaquée.",
         "insert": {"type": "sablier", "pilules": [
             {"texte": "Recours en instruction"}, {"texte": "Aucune date annoncée", "ton": "rouge"}]}},
        # le précédent, et la lecture du Cercle
        {"duree": 16.0, "fichier": "B6.mp4",
         "requete": "page : https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2026-04-30/505930",
         "texte": f"Chez les kinés, le Conseil d{AP}État a annulé *la cotisation 2025*. | "
                  f"Un écart de 2{NB}000{NB}€ contre 90{NB}€ était *disproportionné*. | "
                  f"Selon le Cercle, l{AP}Ordre devra justifier *son écart de 1 à 4*.",
         "voix": "Il y a pourtant un précédent. Chez les kinés, le Conseil d’État a annulé la cotisation deux mille vingt-cinq. | "
                 "Un écart de deux mille euros contre quatre-vingt-dix entre sociétés était « manifestement "
                 "disproportionné ». | Selon le Cercle, l’Ordre des médecins devra donc justifier son écart de un à quatre.",
         "insert": [{"type": "pilule", "texte": "Des écarts admis, pas celui-ci", "temps": 1},
                    {"type": "barres", "suffixe": f"{NB}€", "lignes": [
                        {"label": "Kinés, autres sociétés d’exercice", "valeur": 90, "temps": 1, "reference": True},
                        {"label": "Kinés, sociétés de participations financières", "valeur": 2000, "temps": 1}]}]},
        # retour à la question : le conseil, puis le risque
        {"duree": 11.0, "fichier": "B7.mp4", "requete": "paying bill hands desk",
         "texte": f"En attendant, la CSMF conseille de *payer en partie*. | "
                  f"Seulement le montant d{AP}une *société unipersonnelle*. | "
                  f"Et tant qu{AP}aucune *mise en demeure* n{AP}arrive.",
         "voix": "Alors, en attendant, que faire ? La C.S.M.F. conseille de payer en partie : | seulement le montant d’une "
                 "société unipersonnelle, avec son courrier type. | Et cela, tant qu’aucune véritable mise en demeure "
                 "n’arrive.",
         "insert": {"type": "calcul", "titre": "À 4 associés : le paiement partiel conseillé", "temps": 0,
                    "levee": 34, "parts": [
             {"label": "Réglé", "valeur": 0.25}, {"label": "En litige", "valeur": 0.75}]}},
        {"duree": 12.0, "fichier": "B4.mp4", "requete": "calculator desk paper",
         "texte": f"Si le recours est rejeté, *le barème reste*. | "
                  f"À 4{NB}associés, au moins *1{NB}642,50{NB}€* resteraient dus (calcul du Cercle).",
         "voix": "[curious] Mais si le recours est rejeté, le barème reste en place. | Ce qui n’a pas été payé resterait dû : "
                 "au moins mille six cent quarante-deux euros cinquante pour une société de quatre associés, selon le calcul "
                 "du Cercle.",
         "insert": {"type": "ticket", "titre": "Si le recours est rejeté, à 4 associés", "lignes": [
             {"label": "Déjà payé", "valeur": f"547,50{NB}€", "ok": True},
             {"label": "Resterait dû, au moins", "valeur": f"1{NB}642,50{NB}€", "ok": False, "temps": 1}]}},
        # le médecin seul
        {"duree": 9.0, "fichier": "B10.mp4", "requete": "person working in the office from behind",
         "texte": f"Seul en société{NB}? Vous payez *déjà toute la cotisation*. | "
                  f"Selon nous, ce conseil ne vous apporte *rien*.",
         "voix": "Et si vous êtes seul en société, ce paiement partiel, c’est déjà toute la cotisation réclamée. | Selon nous, "
                 "ce conseil ne vous apporte donc rien.",
         "insert": [{"type": "associes", "lignes": [{"titre": f"Seul en société d{AP}exercice libéral", "ton": "rouge",
                                                     "montants": [{"n": 1, "montant": f"547,50{NB}€"}]}]},
                    {"type": "pilule", "texte": "Rien ne reste impayé", "temps": 1}]},
        {"duree": 8.0, "fichier": "B8.mp4", "requete": "writing notes hands desk bright",
         "texte": f"Votre courrier{NB}: relance, ou *mise en demeure*{NB}? | "
                  f"Le Cercle fait *2{NB}recommandations*.",
         "voix": "[warm] Et le courrier que vous avez reçu : simple relance, ou mise en demeure ? | Deux recommandations : on "
                 "vous les détaille sur le site du Cercle.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

INSTALLATIONS = {
    "slug": "premieres-installations", "date": "2026-11-04", "rubrique": "pro", "label": "Installations et file active",
    "sous_titre": f"Plus d{AP}installations, moins de *patients* par médecin{NB}: pourquoi{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "femme_jeune", "badge": "Médecins généralistes",
    "bandeau": BANDEAU,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "clinic entrance door"},
        # l'accroche : la contradiction
        {"duree": 14.0, "fichier": "B1.mp4", "requete": "moving boxes new office",
         "texte": f"Plus d{AP}installations, mais *moins de patients* par médecin. | "
                  f"*+22,8{NB}%* de premières installations en un an (Assurance Maladie).",
         "voix": "[curious] Médecins généralistes : il y a plus d’installations, mais en moyenne, chaque médecin voit moins de "
                 "patients. Pourquoi ? | Selon l’Assurance Maladie, les premières installations de généralistes ont augmenté "
                 "de vingt-deux virgule huit pour cent en un an, jusqu’à fin juin deux mille vingt-six.",
         "insert": {"type": "plaques", "carre": False, "titre": "Premières installations", "nombre": 523, "prefixe": "+",
                    "legende": "de plus, sur 12 mois", "temps": 1}},
        # la file active, expliquée
        {"duree": 11.0, "type": "chiffre", "valeur": 2.5, "decimales": 1, "prefixe": "−", "suffixe": f"{NB}%",
         "fichier": "B5.mp4", "requete": "medical waiting room chairs",
         "legende": f"de patients différents vus par généraliste en un an. *Spécialistes{NB}: −0,3{NB}%*",
         "voix": "[serious] Mais la file active moyenne, c’est-à-dire le nombre de patients différents vus dans l’année, a "
                 "baissé de deux virgule cinq pour cent. Chez les spécialistes, la baisse n’est que de zéro virgule trois."},
        # pourquoi : personne ne le dit, la lecture du Cercle
        {"duree": 14.0, "fichier": "B6.mp4",
         "requete": "page : https://www.assurance-maladie.ameli.fr/presse/2026-10-22-cp-observatoire-de-l-acces-aux-soins",
         "texte": f"L{AP}Assurance Maladie *ne l{AP}explique pas*. | "
                  f"Selon le Cercle, c{AP}est peut-être *un effet mécanique*. | "
                  f"Les nouveaux installés peuvent tirer la moyenne *vers le bas*.",
         "voix": "Pourquoi ? L’Assurance Maladie donne le chiffre, sans l’expliquer. | Selon le Cercle, une partie de la baisse "
                 "peut être mécanique : | les nouveaux installés, qui commencent à constituer leur patientèle, tirent la "
                 "moyenne vers le bas. Elle peut aussi refléter des patients plus lourds.",
         "insert": {"type": "choix", "lignes": [
             {"label": "Explication de l’Assurance Maladie", "ok": False},
             {"label": "Effet des nouveaux installés", "temps": 1},
             {"label": "Patients plus lourds", "temps": 2}]}},
        # pourquoi ça compte
        {"duree": 15.0, "fichier": "B7.mp4", "requete": "page : https://www.ccomptes.fr/fr/publications/le-dispositif-du-medecin-traitant",
         "texte": f"La Cour des comptes recommande *un seuil obligatoire*. | "
                  f"Pour tout généraliste *libéral installé*. | "
                  f"Elle envisage *500 patients* dont il est médecin traitant.",
         "voix": "Et ce chiffre tombe en plein débat. La Cour des comptes recommande un seuil obligatoire, | pour tout "
                 "généraliste libéral installé : un nombre minimal de patients dont il est le médecin traitant. | Elle envisage "
                 "cinq cents patients, avec un seuil modulable, notamment selon l’ancienneté d’installation."},
        {"duree": 12.0, "fichier": "B8.mp4", "requete": "doctor office chair empty daylight",
         "texte": f"Selon nous, cette ancienneté *n{AP}est pas détaillée*. | "
                  f"Le Cercle demande la file active *sans les nouveaux*.",
         "voix": "Or, selon nous, l’Observatoire de l’Assurance Maladie ne détaille pas cette ancienneté. | Nous demandons donc "
                 "la file active hors nouveaux installés, avant que ce chiffre serve d’argument pour imposer un minimum de "
                 "patients.",
         "insert": {"type": "loupe", "site": "Assurance Maladie", "recherche": "file active hors nouveaux installés",
                    "vide": "Non détaillée"}},
        # la contrainte à l'installation
        {"duree": 12.0, "fichier": "B2.mp4", "requete": "rural village aerial france",
         "texte": f"Là où les médecins manquent le plus{NB}: *+28,5{NB}%* d{AP}installations. | "
                  f"Selon nous, contraindre maintenant freinerait *cette dynamique*.",
         "voix": "Et en zone d’intervention prioritaire, là où les médecins manquent le plus, les premières installations "
                 "progressent encore plus : plus vingt-huit virgule cinq pour cent. | [serious] Selon nous, contraindre "
                 "l’installation maintenant freinerait cette dynamique.",
         "insert": {"type": "barres", "unite": "+", "suffixe": f"{NB}%", "lignes": [
             {"label": "Tout le territoire", "valeur": 22.8, "reference": True},
             {"label": "Zones d’intervention prioritaire", "valeur": 28.5}]}},
        {"duree": 10.0, "fichier": "B9.mp4", "requete": "doctor desk stethoscope laptop daylight",
         "texte": f"En moyenne, médecin traitant de *1{NB}048 patients*. | "
                  f"Et vous{NB}? Le Cercle fait *2{NB}recommandations*.",
         "voix": "[warm] En moyenne, un généraliste est le médecin traitant de mille quarante-huit patients. Et vous, où vous "
                 "situez-vous ? | Deux recommandations : on vous les détaille sur le site du Cercle.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

# caractères lus par seconde, mesurés le 05/11/2026 sur les rendus de ces reels (fin de reel comprise)
CARS_PAR_SECONDE = {"femme_agee": 15.8, "femme_jeune": 14.6}
# le registre des plans est indexé « épisode/bloc » : chaque entrée suit son fichier quand l'ordre des blocs change
REGISTRE = EP / "plans_utilises.json"
registre = json.loads(REGISTRE.read_text(encoding="utf-8"))
for ep in (COTISATION, INSTALLATIONS):
    d = EP / f"{ep['date']}-{ep['slug']}"
    f = d / "script.json"
    blocs_avant = json.loads(f.read_text(encoding="utf-8"))["blocs"]
    par_fichier = {b["fichier"]: registre[f"{d.name}/{i}"] for i, b in enumerate(blocs_avant)
                   if f"{d.name}/{i}" in registre}
    for cle in [c for c in registre if c.startswith(d.name + "/")]:
        del registre[cle]
    for j, b in enumerate(ep["blocs"]):
        if b["fichier"] in par_fichier:
            registre[f"{d.name}/{j}"] = par_fichier[b["fichier"]]
        elif not (d / "broll" / b["fichier"]).exists():
            print(f"[!] {d.name} bloc {j} : {b['fichier']} manque")
        else:
            # un plan repris (retiré un jour, remis le lendemain) n'a plus d'entrée : sans elle, prepare.py et
            # broll.py le croient libre pour un autre reel (review Codex, 06/11/2026). L'inscrire à la main.
            print(f"[!] {d.name} bloc {j} : {b['fichier']} absent du registre des plans, à réinscrire")
    # garder, plan par plan, le recadrage et le crédit déjà faits : le fichier du plan sert de clé
    ancien = {a["fichier"]: a for a in blocs_avant}
    for b in ep["blocs"]:
        a = ancien.get(b["fichier"])
        if a:
            b["requete"] = a.get("requete", b["requete"])
            for cle in ("cadrage", "credit"):
                if cle in a:
                    b[cle] = a[cle]
    f.write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lu = re.sub(r"\[[a-z-]+\]\s*", "", " ".join((b.get("voix") or "") for b in ep["blocs"])).replace(" | ", " ")
    s = len(lu) / CARS_PAR_SECONDE[ep["voix_off"]]
    print(f"{d.name} : {len(ep['blocs']) - 1} plans, {len(lu)} caractères lus, environ {s // 60:.0f} min {s % 60:02.0f} s, "
          f"environ {len(lu) * 300 / 1400:.0f} crédits")
REGISTRE.write_text(json.dumps(dict(sorted(registre.items())), ensure_ascii=False, indent=1), encoding="utf-8")
