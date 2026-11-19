"""Carrousels du 19/11/2026, deuxième version : Secteur 3 (récit) et Le point pénuries (fiche épurée).

Romain, 19/11 : « les carrousels ne doivent pas être chargés du tout ! ils doivent avoir au contraire beaucoup de
valeur ajoutée », avec en exemple un carrousel « image plus texte » (inspi_carrousel.pdf : une idée par slide, un
titre de 2 ou 3 mots en capitales, un paragraphe qui raconte et pousse à la slide suivante, une image en bas, une
flèche ronde). Puis « ok go ». Ce qu'on en garde, aux couleurs du Cercle (« c'est pour le Cercle, pas pour Medadom ») :
- la structure : titre en Montserrat Black capitales, bleu nuit avec un mot en bleu du site ; le récit en Montserrat ;
  l'image dans un bandeau bleu très pâle en bas ; la flèche ronde, bleue ;
- les images : les illustrations des reels (lcdg-reel/lcdg/inserts.py) dessinées à leur état final — à nous, sans
  visage, et qui montrent un mécanisme ;
- Secteur 3 en récit : ce que le médecin ne sait pas (les actes, pas seulement les médicaments ; le raisonnement du
  Conseil d'État) et le pourquoi ; les recommandations, données (fiche pratique voulue par Romain) ; ce que le Cercle
  demande, gardé pour le site ;
- Pénuries en fiche épurée, qu'on rouvre en consultation : par médicament, la date en très grand et un seul geste.

Source de chaque slide en commentaire (pages du PDF de la revue du 19/11). Opinions du Cercle attribuées.

    python carrousels_1119.py         -> lcdg_1119/carrousels/*.png et planches"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from illustrations import illustration  # noqa: E402
from visuels_1119 import (AP, BLANC, BLEU, GRIS, NB, NUIT, PALE, TEXTE, URL, ecrire, hauteur,  # noqa: E402
                          police)
from config import charte as C  # noqa: E402

W, H = 1080, 1350
MARGE = 90
SORTIE = Path(__file__).resolve().parent / "carrousels"


def titre(d, y, texte, taille=72):
    """Titre en capitales, Montserrat Black ; *mot* en bleu."""
    return ecrire(d, MARGE, y, W - 2 * MARGE, texte, taille, graisse="ExtraBold", graisse_forte="ExtraBold",
                  couleur=NUIT, accent=BLEU, interligne=1.04)


def fleche(d):
    cx, cy, r = W - 104, H - 104, 66
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLEU)
    d.line([(cx - 28, cy), (cx + 24, cy)], fill=BLANC, width=14)
    d.line([(cx + 4, cy - 24), (cx + 28, cy), (cx + 4, cy + 24)], fill=BLANC, width=14, joint="curve")


def entete(im, d, num, total, rubrique):
    logo = Image.open(C.LOGO_SRC).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    logo.thumbnail((56, 56))
    im.paste(logo, (MARGE, 54), logo)
    d.text((MARGE + logo.width + 16, 54 + logo.height / 2), f"Le Cercle des Généralistes · {rubrique}",
           font=police(26, "SemiBold"), fill=NUIT, anchor="lm")
    d.text((W - MARGE, 54 + logo.height / 2), f"{num}/{total}", font=police(26, "SemiBold"), fill=GRIS, anchor="rm")


def bandeau_image(im, d, y, ill, marge_bas=60):
    """Le bandeau bleu très pâle du bas, l'illustration centrée dedans."""
    d.rectangle([0, y, W, H], fill=PALE)
    if ill is None:
        return
    larg, haut = W - 2 * MARGE, H - y - 60 - marge_bas
    k = min(larg / ill.width, haut / ill.height, 1.5)
    ill = ill.resize((int(ill.width * k), int(ill.height * k)), Image.LANCZOS)
    im.paste(ill, (int((W - ill.width) / 2), int(y + 50 + (haut - ill.height) / 2)), ill)


def slide(s, num, total, rubrique):
    im = Image.new("RGB", (W, H), BLANC)
    d = ImageDraw.Draw(im)
    entete(im, d, num, total, rubrique)
    y = 150
    y += titre(d, y, s["titre"], s.get("taille_titre", 72))
    y += 34
    y += ecrire(d, MARGE, y, W - 2 * MARGE, s["texte"], s.get("taille", 38), graisse="Regular",
                graisse_forte="Bold", couleur=TEXTE, interligne=1.36)
    if s.get("adresse"):
        y += 40
        f = police(36, "Bold")
        l = f.getlength(URL)
        d.rounded_rectangle([MARGE, y, MARGE + l + 60, y + 80], radius=C.RADIUS, fill=NUIT)
        d.text((MARGE + 30, y + 40), URL, font=f, fill=BLANC, anchor="lm")
        d.text((MARGE + l + 90, y + 40), "Lien en bio", font=police(30, "SemiBold"), fill=GRIS, anchor="lm")
        y += 80
    ill = illustration(s["image"]) if s.get("image") else None
    yb = max(y + 50, s.get("bandeau_min", 820))
    if ill is not None and H - yb < 400:
        print(f"[!] {rubrique} {num}/{total} : bandeau de l'image trop bas ({H - yb} px), raccourcir le texte")
    bandeau_image(im, d, yb, ill)
    if num < total:
        fleche(d)
    return im


def fiche(f, num, total):
    """Le point pénuries : le médicament, la date en très grand, un geste. Rien d'autre."""
    im = Image.new("RGB", (W, H), BLANC)
    d = ImageDraw.Draw(im)
    entete(im, d, num, total, "Le point pénuries")
    y = 160
    # le nom tel qu'il s'écrit (« µg », « mg ») : pas de capitales
    y += ecrire(d, MARGE, y, W - 2 * MARGE, f["nom"], 86, graisse="Black", graisse_forte="Black",
                couleur=NUIT, interligne=1.04)
    y += 16
    y += ecrire(d, MARGE, y, W - 2 * MARGE, f["forme"], 32, couleur=GRIS)
    # la date : le seul chiffre de la slide, en très grand
    y += 70
    d.text((MARGE, y), f["libelle"], font=police(30, "Bold"), fill=GRIS)
    y += 56
    y += ecrire(d, MARGE, y, W - 2 * MARGE, f["date"], f.get("taille_date", 96), graisse="ExtraBold",
                graisse_forte="Black", couleur=BLEU, accent=BLEU, interligne=1.0)
    # le geste, dans le bandeau pâle du bas
    yb = max(y + 70, 860)
    d.rectangle([0, yb, W, H], fill=PALE)
    d.text((MARGE, yb + 56), f["qui"], font=police(28, "Bold"), fill=BLEU)
    ecrire(d, MARGE, yb + 110, W - 2 * MARGE - 140, f["geste"], 38, graisse="SemiBold", graisse_forte="ExtraBold",
           couleur=NUIT, interligne=1.3)
    if num < total:
        fleche(d)
    return im


# ------------------------------------------------------------------ Secteur 3 (PDF p. 9 et 10)
SECTEUR3 = [
    # p. 9, SITUATION ; ESSENTIEL (« Quand : au 1er janvier 2027 »)
    {"titre": f"Secteur{NB}3{NB}: leurs prescriptions *ne seront plus remboursées*",
     "bandeau_min": 700,
     "texte": f"À partir du **1er{NB}janvier 2027**, ce que prescrivent les médecins non conventionnés ne sera plus "
              f"remboursé, sauf exception. **Leurs patients viendront vers vous.**",
     "image": [{"type": "ordonnance", "titre": "Ordonnance", "marque": f"Secteur{NB}3",
                "lignes": [{"label": "Médicaments"}, {"label": "Biologie"}, {"label": "Kinésithérapie"}],
                "pied": f"Dès le 1er{NB}janvier 2027{NB}: non remboursée"}]},
    # p. 9, CE QUI EST CONFIRMÉ (L. 162-5-10 complété par l'article 76 : « Les produits de santé, les actes et les
    # prestations prescrits […] à l'exception de ceux prescrits par ces médecins à titre gracieux, pour eux-mêmes et
    # pour leurs proches ») ; p. 10 (« biologie, imagerie, kinésithérapie, soins infirmiers, transports »)
    {"titre": f"Pas seulement les médicaments{NB}: *la kiné aussi*",
     "texte": f"L{AP}article{NB}76 vise les produits de santé, **les actes et les prestations** prescrits par un "
              f"médecin non conventionné. Donc aussi la biologie, l{AP}imagerie, la kiné, les soins infirmiers, les "
              f"transports.\nUne seule exception{NB}: ce qu{AP}il prescrit **à titre gracieux**, pour lui-même et ses "
              f"proches.",
     "image": {"type": "ticket", "titre": f"Prescrit en secteur{NB}3 dès le 1er{NB}janvier 2027", "lignes": [
         {"label": "Médicaments", "valeur": "non remboursés", "ok": False},
         {"label": "Biologie, imagerie", "valeur": "non remboursées", "ok": False},
         {"label": "Kiné, soins infirmiers", "valeur": "non remboursés", "ok": False},
         {"label": "Transports", "valeur": "non remboursés", "ok": False}]}},
    # p. 9, CE QUI EST CONFIRMÉ (CE n° 517230 du 1er octobre 2026 : refus de renvoyer la QPC de MS3, UFML-S, SML et
    # d'autres ; « il juge que médecins conventionnés et non conventionnés ne sont pas dans une situation comparable et
    # que le droit à la protection de la santé n'est pas atteint, un médecin conventionné restant accessible »)
    {"titre": f"Le Conseil d{AP}État *rejette le recours*",
     "texte": f"Le 1er{NB}octobre, il a refusé de transmettre au Conseil constitutionnel la question "
              f"soulevée par des syndicats.\nIl juge les deux situations non comparables, et "
              f"le droit à la protection de la santé non atteint, **un médecin conventionné restant accessible**."
              f"\nSelon nous, ce médecin conventionné, **ce sera souvent vous.**",
     "image": [{"type": "lettre", "entete": f"Conseil d{AP}État", "titre": f"Décision du 1er{NB}octobre 2026"},
               {"type": "tampon", "texte": "Question non transmise", "sur": True}]},
    # p. 10, L'IMPACT (afflux en janvier : renouvellements, biologie, kiné ; pleine période hivernale) et REGARD
    # (« Le généraliste ne doit pas devenir un guichet de recopie. Une prescription engage celui qui la signe :
    # reprendre un traitement suppose une consultation et un examen, pas un tampon. »)
    {"titre": f"Recopier l{AP}ordonnance{NB}? *Plutôt une consultation*",
     "texte": f"Selon le Cercle, janvier va apporter un **afflux de demandes**{NB}: renouvellements de traitements "
              f"chroniques, biologie, kiné, en pleine période hivernale.\nMais selon nous, une prescription engage "
              f"celui qui la signe{NB}: reprendre un traitement suppose **une consultation et un examen, pas un "
              f"tampon.**",
     "image": {"type": "guichet", "enseigne": "Généraliste", "papier": "Recopie"}},
    # p. 10, RECOMMANDATIONS, médecin généraliste conventionné
    {"titre": f"Prévoyez des créneaux *dès décembre*",
     "texte": f"Notre recommandation{NB}: prévoyez **dès décembre des créneaux de reprise de suivi** pour ces "
              f"patients.\nEt à cette consultation, proposez-leur de vous **déclarer médecin traitant**, plutôt que "
              f"de recopier l{AP}ordonnance.",
     "image": {"type": "icones", "cartes": [
         {"icone": "horloge", "label": "Dès décembre : créneaux de reprise", "question": False},
         {"icone": "patient", "label": "Vous, déclaré médecin traitant", "question": False}]}},
    # p. 10, RECOMMANDATIONS, secrétariat médical
    {"titre": f"Au téléphone{NB}: *«{NB}Qui{NB}vous l{AP}a{NB}prescrite{NB}?{NB}»*",
     "texte": f"Votre secrétariat peut repérer ces patients au téléphone. Quand un patient appelle pour une "
              f"ordonnance{NB}: **«{NB}Qui vous l{AP}a prescrite{NB}?{NB}»**\nSi ce médecin n{AP}est pas "
              f"conventionné{NB}: proposez au patient **une consultation avant le 1er{NB}janvier 2027**, plutôt qu{AP}un simple "
              f"renouvellement.",
     "image": {"type": "icones", "cartes": [
         {"icone": "casque", "label": f"«{NB}Qui vous l{AP}a prescrite{NB}?{NB}»", "question": False},
         {"icone": "patient", "label": f"Consultation avant le 1er{NB}janvier", "question": False}]}},
    # p. 9-10, CE QUI POSE QUESTION (3 questions au 19 novembre)
    {"titre": f"Trois questions *encore sans réponse*",
     "texte": f"Une ordonnance de plusieurs mois, rédigée en 2026 et délivrée en 2027{NB}: remboursée ou pas{NB}? "
              f"**L{AP}article{NB}76 ne règle pas ce cas.**\nEt aucun texte lu ne dit comment le pharmacien saura "
              f"que le prescripteur n{AP}est pas conventionné, ni comment le patient, le laboratoire ou l{AP}infirmier "
              f"l{AP}apprendront.",
     "image": {"type": "loupe", "site": f"Article{NB}76", "recherche": "ordonnance de 2026 délivrée en 2027",
               "vide": "Rien sur ce cas"}},
    # p. 10, REGARD : « Le Cercle demande à l'Assurance Maladie d'informer les patients concernés avant le 1er janvier,
    # de préciser le sort des ordonnances en cours, et de reconnaître la consultation de reprise de traitement comme une
    # consultation à part entière » (3 demandes, gardées pour le site)
    {"titre": f"3 demandes du Cercle *à l{AP}Assurance Maladie*",
     "texte": f"Le Cercle adresse **3{NB}demandes à l{AP}Assurance Maladie**. Elles sont "
              f"dans notre analyse complète, dossier de la revue du 19{NB}novembre.",
     "adresse": True, "image": {"type": "verrou", "n": 3}},
]

# ------------------------------------------------------------------ Pénuries (PDF p. 17 à 19)
# Ouverture et fin en slides « récit » ; une fiche par médicament entre les deux.
PENURIES_OUVERTURE = {
    # p. 17, SITUATION et L'ESSENTIEL ; furosémide : actualité de l'ANSM du 18 novembre (CONTEXTE)
    "titre": f"Le point pénuries *du 19{NB}novembre*", "taille_titre": 84,
    "texte": f"6 médicaments en tension, parmi ceux que signale l{AP}ANSM au 19{NB}novembre. Pour chacun{NB}: "
             f"**ce qu{AP}annonce l{AP}ANSM, et ce qu{AP}il faut savoir au cabinet.**\nÀ enregistrer, pour l{AP}avoir sous la main en "
             f"consultation.",
    "image": {"type": "pharmacie", "pilules": [{"texte": "Contingenté en ville"},
                                               {"texte": "Retour annoncé", "temps": 1}]}}
FICHES = [
    # p. 17 (fiche du 13 novembre : remise à disposition courant décembre 2026) ; p. 19, RECOMMANDATIONS (check-list
    # de l'ANSM pour Jext ; « Stock de dépannage d'urgence en ville »)
    {"nom": f"Jext 300{NB}µg", "forme": f"Adrénaline, stylo prérempli · contingenté en{NB}ville",
     "libelle": f"RETOUR ANNONCÉ PAR L{AP}ANSM", "date": f"Courant décembre 2026", "taille_date": 88,
     "qui": "NOTRE CONSEIL",
     "geste": f"Vérifiez que chaque patient allergique a **2{NB}stylos non périmés** (check-list de l{AP}ANSM). "
              f"Plus de Jext dans sa pharmacie{NB}? Signalez le **«{NB}Stock de dépannage d{AP}urgence en ville{NB}»**."},
    # p. 17 (fiche du 3 novembre : remise à disposition fin novembre 2026) ; p. 19, RECOMMANDATIONS (DCI)
    {"nom": f"Diazépam 5{NB}mg", "forme": f"Diazépam Teva 5{NB}mg · contingenté en ville et à{NB}l{AP}hôpital",
     "libelle": f"RETOUR ANNONCÉ PAR L{AP}ANSM", "date": "Fin novembre 2026", "qui": "NOTRE CONSEIL",
     "geste": f"Prescrivez **en DCI**{NB}: la fiche de l{AP}ANSM ne vise que la spécialité de Teva. Le pharmacien "
              f"pourra ainsi délivrer celle d{AP}un autre laboratoire, si elle est disponible."},
    # p. 17 (fiche du 4 novembre : remise à disposition prévue en janvier 2027) ; p. 19, RECOMMANDATIONS (DCI)
    {"nom": "Cotrimoxazole", "forme": f"Cotrimoxazole Teva 800{NB}mg/160{NB}mg · contingenté en{NB}ville",
     "libelle": f"RETOUR ANNONCÉ PAR L{AP}ANSM", "date": "Janvier 2027", "taille_date": 92, "qui": "NOTRE CONSEIL",
     "geste": f"Prescrivez **en DCI**{NB}: la fiche de l{AP}ANSM ne vise que la spécialité de Teva. Le pharmacien "
              f"pourra ainsi délivrer celle d{AP}un autre laboratoire, si elle est disponible."},
    # p. 18 (fiche du 26 octobre : remise à disposition prévue début décembre 2026) ; p. 19, RECOMMANDATIONS (DCI ;
    # « stock limité de dépannage d'urgence en ville »)
    {"nom": f"Nifédipine LP 30{NB}mg", "forme": f"Nifédipine Viatris L.P. 30{NB}mg · contingenté en{NB}ville",
     "libelle": f"RETOUR ANNONCÉ PAR L{AP}ANSM", "date": "Début décembre 2026", "qui": "NOTRE CONSEIL",
     "geste": f"Prescrivez **en DCI**{NB}: la fiche ne vise que la spécialité de Viatris. Et signalez au "
              f"pharmacien le **«{NB}stock limité de dépannage d{AP}urgence en ville{NB}»**."},
    # p. 17, CONTEXTE (ANSM, 18 novembre : « devraient durer encore plusieurs mois en 2027 » ; « permet au pharmacien
    # de remplacer les comprimés indisponibles par une préparation magistrale, sans nouvelle ordonnance »)
    {"nom": f"Furosémide 20 et 40{NB}mg", "forme": "Comprimés",
     "libelle": f"TENSIONS SELON L{AP}ANSM (18{NB}NOVEMBRE)", "date": f"Devraient durer encore plusieurs mois en{NB}2027",
     "taille_date": 66, "qui": f"CE QUE PERMET L{AP}ANSM",
     "geste": f"**Pas de nouvelle ordonnance**{NB}: le pharmacien peut remplacer les comprimés indisponibles par une "
              f"préparation magistrale."},
    # p. 18 (fiche du 17 novembre : remise à disposition courant janvier 2027 ; « La spécialité Zovirax 200 mg
    # comprimés reste disponible pendant la durée de la tension de la suspension buvable »)
    {"nom": "Zovirax suspension", "forme": f"Aciclovir 200{NB}mg/5{NB}ml, suspension buvable · contingenté en{NB}ville",
     "libelle": f"RETOUR ANNONCÉ PAR L{AP}ANSM", "date": "Courant janvier 2027", "taille_date": 92,
     "qui": f"BON À SAVOIR (ANSM)",
     "geste": f"«{NB}La spécialité **Zovirax 200{NB}mg comprimés reste disponible** pendant la durée de la tension "
              f"de la suspension buvable{NB}»."},
]
PENURIES_FIN = {
    # p. 18, L'IMPACT (« un contingentement ne veut pas dire que le produit manque partout : la disponibilité peut
    # varier d'une officine et d'une semaine à l'autre ») ; p. 19, REGARD (gardé pour le site)
    "titre": f"Contingenté ne veut pas dire *introuvable*",
    "texte": f"Selon le Cercle, la disponibilité peut varier **d{AP}une officine et d{AP}une semaine à l{AP}autre**."
             f"\nCe que le Cercle demande pour le prescripteur, et les questions encore ouvertes{NB}: dans le "
             f"dossier de la revue du 19{NB}novembre.",
    "adresse": True, "image": {"type": "verrou", "n": 2}}


def planche(nom, images, cols=4):
    k = 0.3
    w, h = int(W * k), int(H * k)
    lignes = (len(images) + cols - 1) // cols
    p = Image.new("RGB", (cols * w + (cols + 1) * 16, lignes * h + (lignes + 1) * 16), (200, 205, 215))
    for i, im in enumerate(images):
        p.paste(im.resize((w, h), Image.LANCZOS), (16 + (i % cols) * (w + 16), 16 + (i // cols) * (h + 16)))
    p.save(SORTIE / f"planche_{nom}.png")


if __name__ == "__main__":
    SORTIE.mkdir(exist_ok=True)
    for f in SORTIE.glob("*.png"):
        f.unlink()
    ims = [slide(s, i, len(SECTEUR3), "Secteur 3") for i, s in enumerate(SECTEUR3, 1)]
    for i, im in enumerate(ims, 1):
        im.save(SORTIE / f"secteur3_{i}.png", optimize=True)
    planche("secteur3", ims)
    total = len(FICHES) + 2
    ims = [slide(PENURIES_OUVERTURE, 1, total, "Le point pénuries")]
    ims += [fiche(f, i, total) for i, f in enumerate(FICHES, 2)]
    ims.append(slide(PENURIES_FIN, total, total, "Le point pénuries"))
    for i, im in enumerate(ims, 1):
        im.save(SORTIE / f"penuries_{i}.png", optimize=True)
    planche("penuries", ims)
    print(len(list(SORTIE.glob("*.png"))), "images dans", SORTIE)
