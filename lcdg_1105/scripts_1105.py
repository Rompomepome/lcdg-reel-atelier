"""Reels du 05/11/2026 : réécriture de « Soins chez le pharmacien », « Cotisation à l'Ordre en société » et
« Premières installations ». Romain, 05/11/2026 : « il faut que tu t'assures qu'on parle bien de ce qui pose
réellement problème, car il est là, notre appât » ; « on doit plutôt expliquer pourquoi le décret n'en parle pas » ;
« Selon le Cercle » ou « Mais selon nous » ; puis : « il faudrait pas qu'il dépasse 1 minute, donc il faut condenser
et parler des choses les plus importantes, et surtout il faut capter l'attention en 3 secondes ou même en 1 seconde,
donc l'ouverture est la plus importante ».

Donc : moins d'une minute, le conflit dès la première phrase (bloc 1 : le bloc 0 n'est que la couverture), un seul
pourquoi par problème, les recommandations gardées pour le site. Un pourquoi vient d'une source ou s'attribue.
Ce qui ne tient pas dans la minute va en légende.

Les textes s'écrivent dans les épisodes du 04/11 (mêmes dossiers, mêmes plans) ; l'ancienne version reste dans git
(commit 53a2cb8) et l'ancienne vidéo dans le kit tant que le nouveau rendu n'est pas validé.

Sources relues le 05/11/2026 (en plus des dossiers du Cercle du 3 novembre, lus en entier) :

Pharmacien
- décret n° 2026-999 du 26 octobre 2026, en vigueur le 29 ; motifs fixés par un arrêté ; « Le décret fixe ce que le
  pharmacien transmet, pas ce que le médecin en fait » ; ni délai, ni obligation de répondre, ni reprise ; « le patient
  orienté, lui, attend une réponse » (dossier) ;
- rémunération : le décret n'en fixe aucune ; « un volet financier à négocier par la voie conventionnelle » (Ordre
  des pharmaciens, 22/01/2026) ; rien d'annoncé pour le médecin (dossier) ;
- arrêté : « nous ne l'avons pas trouvée au 3 novembre » ; rien n'oblige à s'en tenir aux motifs simples ; même schéma
  que l'accès direct aux IPA (dossier, regard). Le 05/11/2026, aucune trace de l'arrêté dans la presse professionnelle.

Cotisation
- CSMF, flash du 22/10/2026, relu le 05/11 : relances, recours en cours d'instruction, « une véritable mise en
  demeure » ; aucune suspension mentionnée ;
- article L. 4 du code de justice administrative : « les requêtes n'ont pas d'effet suspensif s'il n'en est autrement
  ordonné par la juridiction » : ajout, absent du dossier, signalé à Romain ;
- barème : 1,5 cotisation par associé médecin, 2 190 € à 4 associés ; société civile professionnelle, 547,50 € quel
  que soit le nombre d'associés (dossier, calcul du Cercle) ;
- regard : le coût des vérifications vaut par société ; kinés, décision n° 505930 : 2 000 € contre 90 €, « manifestement
  disproportionné » ; 1 642,50 € à 4 associés, « au minimum, la somme qui resterait due selon le barème » ; solo : le
  paiement partiel revient à la somme réclamée (dossier, impact).

Installations
- communiqué de l'Assurance Maladie du 22/10/2026, relu le 05/11 : +22,8 %, +523, ZIP +28,5 %, file active -2,5 %
  (« le nombre de patients différents vus au moins une fois dans l'année »), spécialistes -0,3 %, 1 048 patients ;
- Cour des comptes, septembre 2026, lue le 05/11 : recommandation n° 2, « Rendre obligatoire [...] un seuil minimal de
  patientèle prise en charge en tant que médecin traitant » ; 500 patients « pourrait être envisagé » ; modulation
  selon « l'ancienneté d'installation » ; le dossier du Cercle dit « envisage » : signalé à Romain ;
- regard : « une partie peut être mécanique », « précisément les données que l'Observatoire ne détaille pas », publier
  hors nouveaux installés, « freiner une dynamique qui repart ».

    python scripts_1105.py"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EP = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
NB, AP = "\u00a0", "\u2019"
BANDEAU = f"L{AP}analyse complète | sur *notre site*"
SEL, SCP = f"Société d{AP}exercice libéral", "Société civile professionnelle"

PHARMACIEN = {
    "slug": "soins-pharmacien", "date": "2026-11-04", "rubrique": "pro", "label": "Soins chez le pharmacien",
    "sous_titre": f"Le pharmacien soigne, vous lisez{NB}: *gratuitement*{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "homme_age", "badge": "Médecins traitants",
    "bandeau": BANDEAU, "son_limite_db": -3.5,
    # deuxième prise plus lente que la première (63,0 s au lieu de 60,0) : accélérée au montage, sans crédit
    "voix_tempo": 1.12,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "pharmacy shelves medicine boxes"},
        # l'ouverture : le conflit dès la première seconde
        {"duree": 9.0, "fichier": "B3.mp4", "requete": "bandage hand first aid close up",
         "texte": f"Le pharmacien soigne, vous lisez. *Gratuitement*{NB}? | "
                  f"Décret{NB}: *motifs à fixer*, produits sans prescription obligatoire.",
         "voix": "[incredulous] Médecins traitants : le pharmacien soigne, vous lisez. Gratuitement ? | [serious] C’est un décret, "
                 "depuis le vingt-neuf octobre : motifs encore à fixer, produits sans prescription obligatoire.",
         # pas d'illustration avant le deuxième temps : la première image montre le soin, sans rien devant
         "insert": {"type": "pilule", "carre": False, "texte": "Depuis le 29 octobre", "temps": 1}},
        # ce que le médecin reçoit, et pourquoi rien sur lui
        {"duree": 9.0, "fichier": "B2.mp4", "requete": "hands typing laptop stethoscope",
         "texte": f"*Chaque évaluation*, même si le patient est orienté. | "
                  f"Que devez-vous en faire{NB}? Décret{NB}: *pas un mot*.",
         "voix": "Vous recevrez chaque évaluation, même pour un patient seulement orienté. | Que devez-vous en faire ? Le "
                 "décret fixe ce que le pharmacien transmet, pas ce que vous en faites.",
         "insert": {"type": "messagerie", "titre": "Messagerie sécurisée", "messages": [
             {"objet": f"Évaluation d{AP}un patient"}, {"objet": f"Évaluation d{AP}un patient"},
             {"objet": "Patient seulement orienté", "ton": "rouge"}]}},
        # la conséquence
        {"duree": 8.0, "fichier": "B8.mp4", "requete": "waiting room chairs daylight",
         "texte": f"Orienté vers vous{NB}? Délai, réponse, reprise{NB}: *rien au décret*. | "
                  f"Mais ce patient, lui, *attend une réponse*.",
         "voix": "Patient orienté vers vous ? Ni délai, ni obligation de répondre. | [serious] Mais lui attend une réponse.",
         "insert": {"type": "ticket", "titre": "Dans le décret, pour vous", "lignes": [
             {"label": "Délai de lecture", "valeur": "rien", "ok": False},
             {"label": "Obligation de répondre", "valeur": "rien", "ok": False},
             {"label": "Reprise du patient orienté", "valeur": "rien", "ok": False}]}},
        # la réponse à l'ouverture
        {"duree": 7.0, "fichier": "B10.mp4", "requete": "euro coins table bright",
         "texte": f"Rémunération du pharmacien{NB}: *à négocier*. | "
                  f"Pour vous{NB}: *rien d{AP}annoncé*.",
         "voix": "La rémunération ? Celle du pharmacien doit se négocier. | [incredulous] Pour vous, rien n’est annoncé.",
         "insert": {"type": "compteur", "titre": "Rémunération de cette lecture", "date": "au 3 novembre",
                    "pilule": f"Rien d{AP}annoncé pour le médecin", "temps": 1}},
        {"duree": 9.0, "fichier": "B5.mp4", "requete": "open book empty pages desk",
         "texte": f"L{AP}arrêté des motifs{NB}: *introuvable* au 3{NB}novembre. | "
                  f"Selon le Cercle, rien n{AP}oblige à s{AP}en tenir aux *motifs simples*.",
         "voix": "L’arrêté des motifs, introuvable au trois novembre… | selon le Cercle, rien ne l’oblige à s’en tenir aux motifs "
                 "simples.",
         "insert": {"type": "loupe", "site": "Journal officiel", "recherche": "arrêté situations cliniques",
                    "vide": "Introuvable au 3 novembre"}},
        {"duree": 8.0, "type": "phrase", "fichier": "B4.mp4", "requete": "stethoscope desk daylight",
         "texte": f"Selon nous{NB}: *même schéma* que les IPA.",
         "voix": "[serious] Selon nous, même schéma que les I.P.A. : une information au médecin traitant, et rien sur ce qu’il en "
                 "fait."},
        {"duree": 6.0, "fichier": "B11.mp4", "requete": "stethoscope desk top view",
         "texte": f"Chez vous, qui lit *ces messages*{NB}? | "
                  f"Le Cercle fait *2{NB}recommandations*.",
         "voix": "[warm] Chez vous, qui lit ces messages ? | Deux recommandations sur notre site.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

COTISATION = {
    "slug": "cotisation-ordre", "date": "2026-11-04", "rubrique": "pro", "label": "Cotisation de votre société",
    "sous_titre": f"Relancé par l{AP}Ordre{NB}: *faut-il payer*{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "femme_agee", "badge": "Médecins en société",
    "bandeau": BANDEAU,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "envelope letter desk hands opening"},
        # l'ouverture : la question que se pose celui qui a le courrier en main
        {"duree": 7.0, "fichier": "B1.mp4", "requete": "mail envelope hands desk",
         "texte": f"Relancé par l{AP}Ordre{NB}: *faut-il payer*{NB}? | "
                  f"Selon la CSMF, certains qui contestent *sont relancés*.",
         "voix": "[curious] Médecins en société, relancés par l’Ordre : faut-il payer ? | Selon la C.S.M.F., certains qui contestent "
                 "leur cotisation sont relancés.",
         "insert": [{"type": "lettre", "carre": False, "entete": f"Conseil départemental de l{AP}Ordre",
                     "titre": "Cotisation 2026 de votre société"},
                    {"type": "tampon", "carre": False, "texte": "Relance", "sur": True, "delai": 0.3}]},
        # pourquoi le recours ne règle rien en attendant
        {"duree": 6.0, "fichier": "B9.mp4", "requete": "law books shelf daylight",
         "texte": f"Recours de la CSMF{NB}: *pas jugé*. | "
                  f"Sauf ordre du juge, un recours *ne suspend pas*.",
         "voix": "Son recours au Conseil d’État n’est pas jugé. | [serious] Et sauf ordre du juge, il ne suspend rien.",
         "insert": {"type": "sablier", "pilules": [
             {"texte": "Recours en instruction"}, {"texte": "Aucune date annoncée", "ton": "rouge"}]}},
        # l'injustice, en chiffres
        {"duree": 7.0, "fichier": "B2.mp4", "requete": "mail envelope hands desk",
         "texte": f"En société d{AP}exercice libéral{NB}: *1,5{NB}cotisation*, par associé médecin. | "
                  f"À 4{NB}associés{NB}: *2{NB}190{NB}€* pour la société (calcul du Cercle).",
         "voix": "En société d’exercice libéral, à quatre associés : | deux mille cent quatre-vingt-dix euros.",
         "insert": {"type": "associes", "lignes": [{"titre": SEL, "ton": "rouge", "montants": [
             {"n": 1, "montant": f"547,50{NB}€"}, {"n": 4, "montant": f"2{NB}190{NB}€", "temps": 1}]}]}},
        {"duree": 7.0, "fichier": "B3.mp4", "requete": "doctors office corridor daylight",
         "texte": f"En société civile professionnelle{NB}: *547,50{NB}€*… | "
                  f"quel que soit le nombre d{AP}associés. À 4, *4{NB}fois moins*.",
         "voix": "En S.C.P. : cinq cent quarante-sept euros cinquante… | quel que soit le nombre d’associés. [incredulous] À "
                 "quatre, quatre fois moins !",
         "insert": {"type": "associes", "lignes": [
             {"titre": SEL, "ton": "rouge", "montants": [{"n": 4, "montant": f"2{NB}190{NB}€"}]},
             {"titre": SCP, "note": f"quel que soit le nombre d{AP}associés",
              "montants": [{"n": 4, "montant": f"547,50{NB}€"}]}]}},
        {"duree": 7.0, "fichier": "B6.mp4",
         "requete": "page : https://www.conseil-etat.fr/fr/arianeweb/CE/decision/2026-04-30/505930",
         "texte": f"Le Conseil d{AP}État a annulé la cotisation 2025 *des kinés*. | "
                  f"2{NB}000{NB}€ contre 90{NB}€{NB}: « manifestement *disproportionné* ».",
         "voix": "Chez les kinés, le Conseil d’État a annulé… | un tarif « manifestement disproportionné ».",
         "insert": {"type": "barres", "suffixe": f"{NB}€", "lignes": [
             {"label": "Kinés, autres sociétés d’exercice", "valeur": 90, "temps": 1, "reference": True},
             {"label": "Kinés, sociétés de participations financières", "valeur": 2000, "temps": 1}]}},
        # retour à la question : le conseil, et le risque
        {"duree": 10.0, "fichier": "B7.mp4", "requete": "paying bill hands desk",
         "texte": f"CSMF{NB}: *payer en partie*, avant toute mise en demeure. | "
                  f"Si rejet, à 4{NB}: *1{NB}642,50{NB}€* dus, au moins (notre calcul).",
         "voix": "La C.S.M.F. conseille de payer en partie, avant toute véritable mise en demeure. | [curious] Mais si "
                 "son recours est rejeté ? À quatre, au moins mille six cent quarante-deux euros cinquante resteraient dus.",
         "insert": {"type": "calcul", "titre": "À 4 associés : le paiement partiel conseillé", "temps": 0,
                    "temps_question": 1, "levee": 34, "parts": [
             {"label": "Réglé", "valeur": 0.25}, {"label": "En litige", "valeur": 0.75, "question": True}]}},
        {"duree": 6.0, "fichier": "B10.mp4", "requete": "doctor desk alone from behind daylight",
         "texte": f"Seul en société{NB}? C{AP}est déjà *toute la cotisation*. | "
                  f"Selon le Cercle, ce conseil ne vous apporte *rien*.",
         "voix": "Seul en société ? Vous payez déjà toute sa cotisation. | Selon le Cercle, ce conseil ne vous apporte rien.",
         "insert": [{"type": "associes", "lignes": [{"titre": f"Seul en société d{AP}exercice libéral", "ton": "rouge",
                                                     "montants": [{"n": 1, "montant": f"547,50{NB}€"}]}]},
                    {"type": "pilule", "texte": "Rien ne reste impayé", "temps": 1}]},
        {"duree": 6.0, "fichier": "B8.mp4", "requete": "writing notes hands desk bright",
         "texte": f"Votre courrier{NB}: relance, ou *mise en demeure*{NB}? | "
                  f"Le Cercle fait *2{NB}recommandations*.",
         "voix": "[warm] Votre courrier : relance, ou mise en demeure ? | Deux recommandations sur notre site.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

INSTALLATIONS = {
    "slug": "premieres-installations", "date": "2026-11-04", "rubrique": "pro", "label": "Installations et file active",
    "sous_titre": f"Plus d{AP}installations, moins de *patients* par médecin{NB}: pourquoi{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "femme_jeune", "badge": "Médecins généralistes",
    "bandeau": BANDEAU,
    # troisième prise plus lente (63,5 s pour le même nombre de caractères que la deuxième, à 59,1 s) :
    # accélérée au montage, sans crédit
    "voix_tempo": 1.13,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "clinic entrance door"},
        # l'ouverture : la contradiction, en chiffres à l'écran
        {"duree": 9.0, "fichier": "B1.mp4", "requete": "moving boxes new office",
         "texte": f"Plus d{AP}installations, *moins de patients* par médecin. | "
                  f"*+22,8{NB}%* de premières installations, sur 12{NB}mois à fin juin 2026.",
         "voix": "[curious] Médecins généralistes : plus d’installations, moins de patients vus par médecin. Pourquoi ? | Plus "
                 "vingt-deux virgule huit pour cent de premières installations, selon l’Assurance Maladie.",
         "insert": {"type": "plaques", "carre": False, "titre": "Premières installations", "nombre": 523, "prefixe": "+",
                    "legende": "de plus, sur 12 mois", "temps": 1}},
        {"duree": 6.0, "type": "chiffre", "valeur": 2.5, "decimales": 1, "prefixe": "−", "suffixe": f"{NB}%",
         "fichier": "B5.mp4", "requete": "medical waiting room chairs",
         "legende": f"de file active moyenne des généralistes en 12{NB}mois. *Spécialistes{NB}: −0,3{NB}%*",
         "voix": "[serious] File active : moins deux virgule cinq pour cent."},
        # pourquoi : la lecture du Cercle
        {"duree": 8.0, "fichier": "B6.mp4",
         "requete": "page : https://www.assurance-maladie.ameli.fr/presse/2026-10-22-cp-observatoire-de-l-acces-aux-soins",
         "texte": f"Pas d{AP}explication *officielle*. | "
                  f"Selon le Cercle, les nouveaux peuvent tirer la moyenne *vers le bas*.",
         "voix": "Pas d’explication. | Selon le Cercle, les nouveaux installés peuvent tirer la moyenne vers le bas.",
         # pas de barre en parts : aucune source ne donne la part des nouveaux installés (review Codex, 05/11/2026)
         "insert": {"type": "choix", "lignes": [
             {"label": "Explication de l’Assurance Maladie", "ok": False},
             {"label": "Effet des nouveaux installés", "temps": 1}]}},
        # pourquoi ça compte
        {"duree": 9.0, "fichier": "B7.mp4", "requete": "page : https://www.ccomptes.fr/fr/publications/le-dispositif-du-medecin-traitant",
         "texte": f"La Cour des comptes recommande *un seuil obligatoire*. | "
                  f"Pour tout généraliste *libéral installé*. | "
                  f"Médecin traitant d{AP}au moins *500 patients*{NB}: envisagé, modulable.",
         "voix": "Or la Cour des comptes recommande un minimum obligatoire de patients médecin traitant, | pour tout généraliste "
                 "libéral installé. | Elle "
                 "envisage cinq cents, modulable notamment selon l’ancienneté."},
        {"duree": 9.0, "fichier": "B8.mp4", "requete": "doctor office chair empty daylight",
         "texte": f"Selon nous, l{AP}ancienneté n{AP}est *pas détaillée*. | "
                  f"Le Cercle demande la file active *sans les nouveaux*.",
         "voix": "Selon nous, cette ancienneté n’est pas détaillée. | Nous demandons la file active hors nouveaux installés, avant "
                 "qu’elle serve d’argument.",
         "insert": {"type": "loupe", "site": "Assurance Maladie", "recherche": "file active hors nouveaux installés",
                    "vide": "Non détaillée"}},
        # la contrainte à l'installation, à l'écran
        {"duree": 6.0, "fichier": "B2.mp4", "requete": "rural village aerial france",
         "texte": f"Contraindre l{AP}installation maintenant{NB}? | "
                  f"Selon nous, *un frein* à une dynamique qui repart.",
         "voix": "Contraindre l’installation maintenant ? | [serious] Selon nous, un frein à une dynamique qui repart.",
         "insert": {"type": "barres", "unite": "+", "suffixe": f"{NB}%", "lignes": [
             {"label": "Tout le territoire", "valeur": 22.8, "reference": True},
             {"label": "Zones d’intervention prioritaire", "valeur": 28.5}]}},
        {"duree": 7.0, "fichier": "B9.mp4", "requete": "doctor desk stethoscope laptop daylight",
         "texte": f"En moyenne{NB}: médecin traitant de *1{NB}048 patients*. | "
                  f"Et vous{NB}? Le Cercle fait *2{NB}recommandations*.",
         "voix": "[warm] En moyenne, mille quarante-huit patients par médecin traitant. | Et vous ? Deux recommandations sur notre "
                 "site.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

# caractères lus par seconde, mesurés le 05/11/2026 sur les premiers rendus de ces reels (fin de reel comprise)
CARS_PAR_SECONDE = {"homme_age": 14.1, "femme_agee": 15.8, "femme_jeune": 14.6}
# le registre des plans (episodes/plans_utilises.json) est indexé « épisode/bloc » : quand l'ordre des blocs
# change, chaque entrée suit son fichier, sinon la protection contre les tournages déjà vus se trompe de plan
# (review Codex, 05/11/2026)
REGISTRE = EP / "plans_utilises.json"
registre = json.loads(REGISTRE.read_text(encoding="utf-8"))
for ep in (PHARMACIEN, COTISATION, INSTALLATIONS):
    d = EP / f"{ep['date']}-{ep['slug']}"
    (d / "broll").mkdir(parents=True, exist_ok=True)
    f = d / "script.json"
    blocs_avant = json.loads(f.read_text(encoding="utf-8"))["blocs"] if f.exists() else []
    par_fichier = {b["fichier"]: registre[f"{d.name}/{i}"] for i, b in enumerate(blocs_avant)
                   if f"{d.name}/{i}" in registre}
    for cle in [c for c in registre if c.startswith(d.name + "/")]:
        del registre[cle]
    for j, b in enumerate(ep["blocs"]):
        if b["fichier"] in par_fichier:
            registre[f"{d.name}/{j}"] = par_fichier[b["fichier"]]
    # garder, plan par plan, le choix, le recadrage et le crédit déjà faits : le fichier du plan sert de clé
    ancien = {a["fichier"]: a for a in blocs_avant}
    for b in ep["blocs"]:
        a = ancien.get(b["fichier"])
        if a:
            b["requete"] = a.get("requete", b["requete"])
            for cle in ("cadrage", "credit"):
                if cle in a:
                    b[cle] = a[cle]
    f.write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    texte = " ".join((b.get("voix") or "") for b in ep["blocs"])
    import re
    lu = re.sub(r"\[[a-z-]+\]\s*", "", texte).replace(" | ", " ")
    print(f"{d.name} : {len(ep['blocs']) - 1} plans, {len(lu)} caractères lus, environ "
          f"{len(lu) / CARS_PAR_SECONDE[ep['voix_off']]:.0f} s, environ {len(lu) * 300 / 1400:.0f} crédits")
# même écriture que lcdg/registre.py
REGISTRE.write_text(json.dumps(dict(sorted(registre.items())), ensure_ascii=False, indent=1), encoding="utf-8")
