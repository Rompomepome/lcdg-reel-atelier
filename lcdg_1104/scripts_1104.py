"""Reels du 04/11/2026 : « Soins chez le pharmacien », « Cotisation à l'Ordre en société » et
« Premières installations ». Au niveau du reel arrêts de travail (une illustration animée sur presque
chaque plan) ; public nommé en pastille et dans la première phrase lue. Texte corrigé après la relecture
indépendante du 04/11/2026 (6 erreurs bloquantes, 24 à corriger), puis resserré autour de 100 s.

Chaque fait vient des dossiers du Cercle du 3 novembre 2026 (PDF, Téléchargements), vérifiés le 04/11/2026
aux sources quand elles sont accessibles :

Soins chez le pharmacien (LCDG_dossier_decret-soins-pharmacien-medecin-traitant.pdf)
- décret n° 2026-999 du 26 octobre 2026, JO du 28, en vigueur le 29 (Vidal, Ordre des pharmaciens) ;
- situations cliniques fixées par un arrêté : introuvable au 3 novembre (Vidal : pas publié au 29 oct.) ;
- transmission au médecin traitant par messagerie sécurisée, y compris quand le patient est seulement
  orienté (R. 5125-33-14) ; contenu : Ordre des pharmaciens, 29/10/2026 ;
- selon l'Ordre, le décret généralise OSyS : brûlures, plaies simples, piqûres de tique, conjonctivites ;
  4 régions ; la liste du décret reste à fixer par arrêté ;
- 19 % de l'ensemble des patients ont évité le recours à un médecin : Cour des comptes, septembre 2026,
  note 135, lue dans le PDF ;
- regard : favorable aux motifs simples, « du temps médical rendu aux cabinets » ; « en vigueur sans son
  contenu » ;
- pas de délai de lecture, d'obligation de répondre, de modalité de reprise ; « le patient orienté, lui,
  attend une réponse » (impact) ; sans médecin traitant : DMP seul, aucune transmission à un médecin ;
- aucune rémunération fixée par le décret, rien d'annoncé pour le médecin ; 2 recommandations.

Cotisation à l'Ordre (LCDG_dossier_cotisation-ordre-medecins-societe-hausse.pdf)
- relances : CSMF, flash info du 22/10/2026, lu ; barème : Médecins n° 102, page 8, lue ;
- SEL : 1,5 cotisation par associé médecin ; SCP : 1,5 quel que soit le nombre ;
  547,50 / 2 190 € : calcul du Cercle, au barème de 365 € ;
- Conseil d'État, 30 avril 2026, n° 505930, lue sur conseil-etat.fr : délibération de l'Ordre des kinés
  annulée, 2 000 € pour les SPFPL contre 90 € pour les autres sociétés d'exercice, « manifestement
  disproportionné » ; des montants différents restent admis ;
- conseil de la CSMF : régler au montant d'une société unipersonnelle, avec son courrier type, tant
  qu'aucune véritable mise en demeure n'arrive ; question ouverte : le paiement partiel si le recours est
  rejeté ; regard : l'argument des vérifications vaut par société ;
- dans la légende, pas dans le reel : « de près de 50 % » (question écrite n° 16716, lue) et « avoisinant
  ou dépassant 60 % par associé », pour certaines structures (CSMF, 16/01/2026).

Premières installations (LCDG_dossier_installations-medecins-generalistes-22-8.pdf)
- communiqué de l'Assurance Maladie du 22/10/2026, lu, données au 30 juin 2026 : +22,8 %, +523 sur 12 mois
  à fin juin 2026 ; ZIP +28,5 %, même période ; ALD sans médecin traitant 5,6 % fin 2022, 4,3 % fin 2025,
  4,1 % au 30 juin 2026 ; patientèle moyenne 1 048 ; file active moyenne -2,5 % ;
- dans la légende, pas dans le reel : 2 810 en 2025, 2 130 en 2024 (années civiles : la soustraction ne
  donne pas 523) ;
- seuil de 500 : Cour des comptes, lu dans le PDF ;
- regard : « contredisent le récit d'une profession qui fuirait l'installation » ; « freiner une
  dynamique qui repart » ; « c'est d'abord leur travail que mesure cet indicateur » ; publier la file
  active hors nouveaux installés ; 2 recommandations.

    python scripts_1104.py"""
import json
from pathlib import Path

EP = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")
NB, AP = "\u00a0", "\u2019"
BANDEAU = f"L{AP}analyse complète | sur *notre site*"
SEL, SCP = f"Société d{AP}exercice libéral", "Société civile professionnelle"

PHARMACIEN = {
    "slug": "soins-pharmacien", "date": "2026-11-04", "rubrique": "pro", "label": "Soins chez le pharmacien",
    "sous_titre": f"Le pharmacien va vous écrire. *Et ensuite*{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "homme_age", "badge": "Médecins traitants",
    "bandeau": BANDEAU,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "pharmacy shelves medicine boxes"},
        {"duree": 9.0, "fichier": "B1.mp4", "requete": "pharmacist hands medicine counter",
         "texte": f"Un décret est en vigueur depuis le *29{NB}octobre*. | "
                  f"À venir{NB}: certains cas en pharmacie, *sans ordonnance*.",
         "voix": "Médecins traitants : un décret est en vigueur depuis le vingt-neuf octobre. | "
                 "Pour certaines situations cliniques, votre patient pourra être évalué et pris en charge en "
                 "pharmacie, sans ordonnance.",
         "insert": {"type": "pharmacie", "carre": False, "pilules": [
             {"texte": "Décret en vigueur"}, {"texte": "Sans ordonnance", "ton": "vert", "temps": 1}]}},
        {"duree": 8.0, "fichier": "B2.mp4", "requete": "hands typing laptop stethoscope",
         "texte": f"Vous recevrez *chaque évaluation*, par messagerie sécurisée. | "
                  f"Même quand le patient est *seulement orienté*.",
         "voix": "Et vous, vous recevrez chaque évaluation, par messagerie sécurisée : notamment les symptômes, la "
                 "conclusion, les soins réalisés ou l’orientation. | Même quand le patient est seulement orienté.",
         "insert": {"type": "messagerie", "titre": "Messagerie sécurisée", "messages": [
             {"objet": f"Évaluation d{AP}un patient"}, {"objet": f"Évaluation d{AP}un patient"},
             {"objet": "Patient seulement orienté", "ton": "rouge", "temps": 1}]}},
        {"duree": 8.0, "fichier": "B3.mp4", "requete": "bandage hand first aid close up",
         "texte": f"Selon l{AP}Ordre des pharmaciens, le décret généralise *OSyS*. | "
                  f"Expérimenté dans 4{NB}régions, sur *ces 4{NB}motifs*.",
         "voix": "Selon l’Ordre des pharmaciens, ce décret généralise l’expérimentation Ossis, menée dans quatre "
                 "régions. | Brûlures, plaies simples, piqûres de tique, conjonctivites.",
         "insert": {"type": "motifs", "cartes": [
             {"icone": "brulure", "label": "Brûlures", "temps": 1}, {"icone": "plaie", "label": "Plaies simples", "temps": 1},
             {"icone": "tique", "label": "Piqûres de tique", "temps": 1},
             {"icone": "oeil", "label": "Conjonctivites", "temps": 1}]}},
        {"duree": 7.0, "type": "chiffre", "valeur": 19, "suffixe": f"{NB}%", "fichier": "B4.mp4",
         "requete": "stethoscope desk daylight",
         "legende": f"des patients de l{AP}expérimentation ont *évité un recours* au médecin",
         "voix": "Selon l’évaluation citée par la Cour des comptes, dix-neuf pour cent des patients de l’expérimentation "
                 "ont évité le recours à un médecin. [warm] Bien encadré, c’est, pour le Cercle, du temps médical rendu."},
        {"duree": 4.0, "type": "phrase", "fichier": "B5.mp4", "requete": "open book empty pages desk",
         "texte": f"Pour le Cercle{NB}: en vigueur, sans *son contenu*.",
         "voix": "[serious] Mais pour le Cercle, ce décret est en vigueur… sans son contenu."},
        {"duree": 8.0, "fichier": "B6.mp4", "requete": "page : question écrite",
         "texte": f"La liste du décret{NB}? Elle dépend d{AP}*un arrêté*. | "
                  f"Au 3{NB}novembre{NB}: *introuvable*.",
         "voix": "La liste du décret, elle, dépend d’un arrêté. | Au trois novembre, il reste introuvable.",
         "insert": {"type": "loupe", "site": "Textes officiels", "recherche": "arrêté situations cliniques",
                    "vide": "Introuvable au 3 novembre"}},
        {"duree": 9.0, "fichier": "B7.mp4", "requete": "hands on computer mouse office",
         "texte": f"Et ces évaluations, vous en faites quoi{NB}? | "
                  f"Le décret dit ce que le pharmacien envoie. *Rien sur la suite*.",
         "voix": "Et ces évaluations, vous en faites quoi ? | Le décret ne prévoit ni délai de lecture, ni obligation de "
                 "répondre, ni façon de reprendre un patient orienté vers vous.",
         "insert": {"type": "ticket", "titre": "Dans le décret, pour vous", "lignes": [
             {"label": "Délai de lecture", "valeur": "rien", "ok": False, "temps": 1},
             {"label": "Obligation de répondre", "valeur": "rien", "ok": False, "temps": 1},
             {"label": "Reprise du patient orienté", "valeur": "rien", "ok": False, "temps": 1}]}},
        {"duree": 4.0, "type": "phrase", "fichier": "B8.mp4", "requete": "waiting room chairs daylight",
         "texte": f"Le patient, lui, attend *une réponse*.",
         "voix": "[serious] Mais le patient orienté, lui, attend une réponse."},
        # le bloc « patient sans médecin traitant » a été retiré à 110 s de reel : il reste dans la légende
        {"duree": 8.0, "fichier": "B10.mp4", "requete": "euro coins table bright",
         "texte": f"Et lire ces évaluations, c{AP}est rémunéré{NB}? | "
                  f"Le décret ne fixe *aucune rémunération*.",
         "voix": "Et les lire, c’est rémunéré ? | Le décret ne fixe aucune rémunération. Pour le médecin, "
                 "rien n’est annoncé.",
         "insert": {"type": "compteur", "titre": "Rémunération de cette lecture", "date": "au 3 novembre",
                    "pilule": f"Rien d{AP}annoncé pour le médecin", "temps": 1}},
        {"duree": 7.0, "fichier": "B11.mp4", "requete": "stethoscope desk top view",
         "texte": f"Votre cabinet est-il prêt à recevoir ces messages{NB}? | "
                  f"Le Cercle fait *2{NB}recommandations*.",
         "voix": "[warm] Votre cabinet est-il prêt à recevoir ces messages ? | "
                 "Deux recommandations : on vous les détaille sur le site du Cercle.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

COTISATION = {
    "slug": "cotisation-ordre", "date": "2026-11-04", "rubrique": "pro", "label": f"Cotisation à l{AP}Ordre",
    "sous_titre": f"Relancé par l{AP}Ordre{NB}: *payer la hausse*{NB}?",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "femme_agee", "badge": "Médecins en société",
    "bandeau": BANDEAU,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "envelope letter desk hands opening"},
        {"duree": 8.0, "fichier": "B1.mp4", "requete": "opening letter envelope hands",
         "texte": f"Des conseils de l{AP}Ordre *relancent* des médecins en société. | "
                  f"Parmi ceux qui contestent la cotisation *de leur société* (CSMF).",
         "voix": "Médecins en société : des conseils de l’Ordre relancent… | certains de ceux qui contestent la "
                 "cotisation deux mille vingt-six de leur société, selon la C.S.M.F.",
         "insert": [{"type": "lettre", "carre": False, "entete": f"Conseil départemental de l{AP}Ordre",
                     "titre": "Cotisation 2026 de votre société"},
                    {"type": "tampon", "carre": False, "texte": "Relance", "sur": True, "delai": 1.2}]},
        {"duree": 11.0, "fichier": "B2.mp4", "requete": "business partners signing document hands",
         "texte": f"En société d{AP}exercice libéral{NB}: *1,5{NB}cotisation*, par associé médecin. | "
                  f"À 4{NB}associés{NB}: *2{NB}190{NB}€*, pour la seule société.",
         "voix": "Le barème, en société d’exercice libéral : une cotisation et demie… par associé médecin. | "
                 "À quatre associés, deux mille cent quatre-vingt-dix euros, pour la seule société, selon le calcul "
                 "du Cercle.",
         "insert": {"type": "associes", "lignes": [{"titre": SEL, "ton": "rouge", "montants": [
             {"n": 1, "montant": f"547,50{NB}€"}, {"n": 4, "montant": f"2{NB}190{NB}€", "temps": 1}]}]}},
        {"duree": 8.0, "fichier": "B3.mp4", "requete": "doctors office corridor daylight",
         "texte": f"En société civile professionnelle{NB}: *547,50{NB}€*… | "
                  f"quel que soit le nombre d{AP}associés.",
         "voix": "En société civile professionnelle ? Cinq cent quarante-sept euros cinquante… | "
                 "quel que soit le nombre d’associés.",
         "insert": {"type": "associes", "lignes": [
             {"titre": SEL, "ton": "rouge", "montants": [{"n": 4, "montant": f"2{NB}190{NB}€"}]},
             {"titre": SCP, "note": f"quel que soit le nombre d{AP}associés",
              "montants": [{"n": 4, "montant": f"547,50{NB}€"}]}]}},
        {"duree": 6.0, "type": "phrase", "fichier": "B4.mp4", "requete": "calculator desk paper",
         "texte": f"À 4{NB}associés{NB}: *4{NB}fois plus* qu{AP}une SCP.",
         "voix": "[incredulous] Quatre fois plus qu’une société civile professionnelle ! [serious] Alors que, selon la "
                 "C.S.M.F., les obligations de contrôle sont comparables."},
        {"duree": 8.0, "fichier": "B5.mp4", "requete": "binders folders office shelf bright",
         "texte": f"L{AP}Ordre invoque notamment *les vérifications*. | "
                  f"Pour le Cercle, ça vaut par société, *pas par associé*.",
         "voix": "Cette hausse, l’Ordre la justifie notamment par le coût des vérifications. | [serious] Pour le Cercle, "
                 "cet argument vaut par société, pas par associé.",
         "insert": {"type": "duel", "cartes": [
             {"date": f"L{AP}Ordre", "texte": "Le coût des vérifications", "temps": 0},
             {"date": "Le Cercle", "texte": "Vaut par société, pas par associé", "temps": 1}]}},
        {"duree": 11.0, "fichier": "B6.mp4", "requete": "page : Conseil d'État",
         "texte": f"Le Conseil d{AP}État a annulé la cotisation 2025 *des kinés*. | "
                  f"2{NB}000{NB}€ contre 90{NB}€{NB}: « manifestement *disproportionné* ».",
         "voix": "Dans un litige comparable, le trente avril, le Conseil d’État a annulé la cotisation deux mille "
                 "vingt-cinq de l’Ordre des kinés. | Il admet des écarts. Mais deux mille euros contre quatre-vingt-dix : "
                 "« manifestement disproportionné ».",
         "insert": [{"type": "pilule", "texte": "Des écarts admis, pas celui-ci", "temps": 1},
                    {"type": "barres", "suffixe": f"{NB}€", "lignes": [
                        {"label": "Kinés, autres sociétés d’exercice", "valeur": 90, "temps": 1, "reference": True},
                        {"label": "Kinés, sociétés de participations financières", "valeur": 2000, "temps": 1}]}]},
        {"duree": 13.0, "fichier": "B7.mp4", "requete": "paying bill hands desk",
         "texte": f"Le recours de la CSMF au Conseil d{AP}État{NB}? *En instruction*, dit-elle. | "
                  f"*Paiement partiel* et courrier type, sauf mise en demeure. | "
                  f"Recours rejeté{NB}: que devient ce paiement{NB}? *La CSMF ne le dit pas*.",
         "voix": "Le recours de la C.S.M.F. au Conseil d’État est toujours en instruction, selon elle. | En attendant, "
                 "elle conseille de ne régler que la cotisation d’une société unipersonnelle, avec son courrier type, "
                 "tant qu’aucune véritable mise en demeure n’arrive. | [curious] Et si le recours est rejeté ? La "
                 "C.S.M.F. ne dit pas ce que devient ce paiement partiel.",
         "insert": {"type": "calcul", "titre": "Le paiement partiel conseillé par la CSMF", "temps": 1,
                    "temps_question": 2, "levee": 34, "parts": [
             {"label": "Réglé", "valeur": 0.25}, {"label": "En litige", "valeur": 0.75, "question": True}]}},
        {"duree": 8.0, "fichier": "B8.mp4", "requete": "notebook pen desk daylight",
         "texte": f"Si le recours est rejeté, combien resterait *à payer*{NB}? | "
                  f"Le calcul du Cercle, et ses *2{NB}recommandations*.",
         "voix": "[warm] Si le recours est rejeté, combien resterait à payer ? | Le Cercle a fait ce calcul. Il fait aussi "
                 "deux recommandations : on vous les détaille sur le site du Cercle.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

INSTALLATIONS = {
    "slug": "premieres-installations", "date": "2026-11-04", "rubrique": "pro", "label": "Premières installations",
    "sous_titre": f"Une profession qui fuit l{AP}installation{NB}? *+22,8{NB}%*",
    "appel": f"Nos 2 recommandations{NB}:", "voix_off": "femme_jeune", "badge": "Médecins généralistes",
    "bandeau": BANDEAU,
    "blocs": [
        {"duree": 3.0, "texte": None, "fichier": "B0.mp4", "requete": "doctor office door sign"},
        {"duree": 9.0, "fichier": "B1.mp4", "requete": "doctor unpacking office new desk hands",
         "texte": f"*+22,8{NB}%* de premières installations, sur 12{NB}mois à fin juin 2026. | "
                  f"Soit *523 installations* de plus, selon l{AP}Assurance Maladie.",
         "voix": "Médecins généralistes : plus vingt-deux virgule huit pour cent de premières installations, sur les "
                 "douze mois à fin juin deux mille vingt-six… | soit cinq cent vingt-trois de plus que sur les douze "
                 "mois d’avant, selon l’Assurance Maladie.",
         "insert": {"type": "plaques", "carre": False, "titre": "Premières installations", "nombre": 523, "prefixe": "+",
                    "legende": "de plus, sur 12 mois", "temps": 1}},
        {"duree": 6.0, "fichier": "B2.mp4", "requete": "rural village aerial france",
         "texte": f"Sur ces 12{NB}mois, en zone d{AP}intervention prioritaire{NB}: *+28,5{NB}%*.",
         "voix": "Sur ces mêmes douze mois, dans les zones d’intervention prioritaire : plus vingt-huit virgule cinq "
                 "pour cent.",
         "insert": {"type": "barres", "unite": "+", "suffixe": f"{NB}%", "lignes": [
             {"label": "Tout le territoire", "valeur": 22.8, "reference": True},
             {"label": "Zones d’intervention prioritaire", "valeur": 28.5}]}},
        {"duree": 8.0, "type": "phrase", "fichier": "B3.mp4", "requete": "doctor walking corridor from behind",
         "texte": f"Fuir l{AP}installation{NB}? | Pour le Cercle, *non*.",
         "voix": "[incredulous] Une profession qui fuirait l’installation ? | [serious] Pour le Cercle, ces chiffres "
                 "contredisent ce récit. Et contraindre l’installation maintenant, ce serait freiner une dynamique "
                 "qui repart."},
        {"duree": 11.0, "fichier": "B4.mp4", "requete": "blood pressure senior patient hands",
         "texte": f"Patients en ALD sans médecin traitant{NB}: de 5,6{NB}% à *4,1{NB}%*. | "
                  f"Pour le Cercle, ce recul, c{AP}est *d{AP}abord votre travail*.",
         "voix": "Et la part de patients en A.L.D. sans médecin traitant recule : cinq virgule six pour cent fin deux "
                 "mille vingt-deux, quatre virgule un au trente juin. | [warm] Pour le Cercle, ce recul, c’est d’abord "
                 "votre travail.",
         "insert": {"type": "barres", "suffixe": f"{NB}%", "lignes": [
             {"label": "Fin 2022", "valeur": 5.6, "reference": True},
             {"label": "Fin 2025", "valeur": 4.3, "reference": True},
             {"label": "Au 30 juin 2026", "valeur": 4.1}]}},
        {"duree": 8.0, "type": "chiffre", "valeur": 2.5, "decimales": 1, "prefixe": "−", "suffixe": f"{NB}%",
         "fichier": "B5.mp4", "requete": "medical waiting room chairs",
         "legende": f"de file active moyenne des généralistes, *en 12{NB}mois*",
         "voix": "[serious] Mais la file active moyenne des généralistes recule : moins deux virgule cinq pour cent en "
                 "douze mois."},
        {"duree": 10.0, "fichier": "B6.mp4", "requete": "stethoscope window light",
         "texte": f"Pourquoi{NB}? *Le communiqué* ne le dit pas. | "
                  f"Trois pistes, *rien de confirmé*.",
         "voix": "[curious] Pourquoi ? Le communiqué de l’Assurance Maladie ne l’explique pas. | Départs à la retraite, "
                 "moins de temps médical par médecin, effet de calcul : rien n’est confirmé, rien n’est écarté.",
         "insert": {"type": "choix", "lignes": [
             {"label": "Départs à la retraite", "temps": 1},
             {"label": "Moins de temps médical par médecin", "temps": 1},
             {"label": "Effet de calcul", "temps": 1}]}},
        {"duree": 10.0, "fichier": "B7.mp4", "requete": "page : Cour des comptes",
         "texte": f"En moyenne{NB}: *1{NB}048 patients* par médecin traitant. | "
                  f"La Cour des comptes envisage un seuil minimal{NB}: *500 patients*.",
         "voix": "En moyenne, un généraliste est le médecin traitant de mille quarante-huit patients. | "
                 "La Cour des comptes envisage un seuil minimal : cinq cents patients.",
         "insert": {"type": "barres", "lignes": [
             {"label": "Moyenne des généralistes, au 30 juin 2026", "valeur": 1048, "reference": True},
             {"label": "Seuil envisagé par la Cour des comptes", "valeur": 500, "temps": 1}]}},
        {"duree": 10.0, "fichier": "B8.mp4", "requete": "page : Assurance Maladie",
         "texte": f"Pour le Cercle, avant d{AP}imposer un minimum de patients… | "
                  f"l{AP}Assurance Maladie doit publier la file active *hors nouveaux installés*.",
         "voix": "Pour le Cercle, avant que la file active serve d’argument pour imposer ce seuil… | "
                 "l’Assurance Maladie doit la publier, hors nouveaux installés.",
         "insert": {"type": "loupe", "site": "Observatoire", "recherche": "file active hors nouveaux installés",
                    "vide": "Non détaillée"}},
        {"duree": 7.0, "fichier": "B9.mp4", "requete": "doctor desk stethoscope laptop daylight",
         "texte": f"Et vous, où vous situez-vous face aux *1{NB}048 patients*{NB}? | "
                  f"Le Cercle fait *2{NB}recommandations*.",
         "voix": "[warm] Et vous, où vous situez-vous par rapport à ces mille quarante-huit patients ? | "
                 "Deux recommandations : on vous les détaille sur le site du Cercle.",
         "insert": {"type": "verrou", "n": 2}},
    ]}

for ep in (PHARMACIEN, COTISATION, INSTALLATIONS):
    d = EP / f"{ep['date']}-{ep['slug']}"
    (d / "broll").mkdir(parents=True, exist_ok=True)
    f = d / "script.json"
    if f.exists():                                  # garder le plan, le recadrage et le crédit déjà choisis
        ancien = json.loads(f.read_text(encoding="utf-8"))
        for b, a in zip(ep["blocs"], ancien["blocs"]):
            if len(ancien["blocs"]) == len(ep["blocs"]):
                b["requete"] = a.get("requete", b["requete"])
            for cle in ("cadrage", "credit"):
                if cle in a:
                    b[cle] = a[cle]
    f.write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    texte = " ".join((b.get("voix") or "") for b in ep["blocs"])
    print(f"{d.name} : {len(ep['blocs'])} blocs, {len(texte)} caractères lus")
