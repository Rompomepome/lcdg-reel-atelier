"""Visuels du 19/11/2026, tirés de la revue du 19/11 (LCDG_revue_du_19-11-2026.pdf, lue en entier), sur le plan de
Romain du 19/11 (« enchaîne sur tout ! il faut tout faire ! ») :
- carrousel Secteur 3, 7 slides (4:5) : « une date butoir et des gestes concrets à faire avant » ;
- carrousel « Le point pénuries », une slide par médicament (4:5) : « le sujet que le médecin garde » ;
- visuel chiffre « 1 an » (tiers payant, 4:5), sa story, et une story DPC (9:16) ;
- les deux stories du reel taxe lapin (sondage, lien), en 9:16.

Identité du Cercle des Généralistes, pas celle de Medadom (Romain, 19/11 : « fais bien attention aux couleurs, à la
police »). La première version reprenait carrousel_planche.png, dont le fond indigo et l'accent cyan ne sont pas
ceux du Cercle. Ici, tout vient de lcdg-reel/config/charte.py (couleurs du theme.css du site : PRIMARY #047bbf,
NAVY #1b1046 pour les titres ; vert et rouge des rubriques « clinique » et « patient »), de la police Montserrat et
du logo du dépôt, et la mise en page suit la revue PDF : fond blanc, en-tête logo + « Le Cercle des Généralistes »,
titres bleu nuit, intitulés en bleu, encadré bleu très pâle comme « Le regard du Cercle », pied de page du site.

Balises du texte : *mot en bleu*, **gras**. Rien n'est inventé : chaque slide porte sa source (page du PDF) en
commentaire. Les opinions du regard du Cercle et les lectures de « L'impact » sont attribuées (« Selon le Cercle »).
Deux relectures indépendantes contre le PDF (19/11) : leurs corrections sont intégrées.

Stories : tout le contenu tient entre y 250 et 1560 (barre du haut et champ de réponse d'Instagram) ; la zone
laissée vide sous la flèche est celle du sticker (sondage ou lien), à poser dans Instagram.

    python visuels_1119.py            -> lcdg_1119/visuels/*.png et visuels/planche_*.png"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ICI = Path(__file__).resolve().parent
MOTEUR = ICI.parents[1] / "lcdg-reel"
if not MOTEUR.exists():
    MOTEUR = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
sys.path.insert(0, str(MOTEUR))
from config import charte as C  # noqa: E402  (couleurs, police et logo du Cercle : une seule source)

NB, AP = "\u00a0", "\u2019"
BLANC = C.BLANC
BLEU = C.PRIMARY                     # #047bbf, la couleur du site
NUIT = C.NAVY                        # #1b1046, les titres du site
VERT = C.RUBRIQUES["clinique"]       # #059669
ROUGE = C.RUBRIQUES["patient"]       # #e11d48
TEXTE = (52, 48, 82)                 # le corps de texte : le bleu nuit éclairci, comme le texte courant de la revue
GRIS = C.INSERT_GRIS_TEXTE           # (128, 136, 152) : mentions secondaires
PALE = (240, 245, 251)               # le fond de l'encadré « Le regard du Cercle » de la revue
FILET = C.INSERT_GRIS                # (226, 230, 238)

W = 1080
H_FIL, H_STORY = 1350, 1920
MARGE = 96
URL = "lecercledesgeneralistes.fr"

_cache = {}


def police(taille, graisse="Medium"):
    cle = (taille, graisse)
    if cle not in _cache:
        f = ImageFont.truetype(str(C.POLICE), taille)
        f.set_variation_by_name(graisse)
        _cache[cle] = f
    return _cache[cle]


# ------------------------------------------------------------------ texte riche
def jetons(texte):
    """[(mot, style, colle)] : style « n » normal, « g » gras, « a » accent (gras bleu) ; « colle » quand aucun espace
    ne le sépare du mot précédent (« l’**article** »). Les espaces insécables restent dans le mot."""
    out, fin_espace = [], True
    for morceau in re.split(r"(\*\*.+?\*\*|\*.+?\*)", texte):
        if not morceau:
            continue
        if morceau.startswith("**"):
            style, morceau = "g", morceau[2:-2]
        elif morceau.startswith("*"):
            style, morceau = "a", morceau[1:-1]
        else:
            style = "n"
        for i, mot in enumerate(morceau.split(" ")):
            if mot:
                out.append((mot, style, i == 0 and not fin_espace))
        fin_espace = morceau.endswith(" ")
    return out


def _couper(mots, largeur, espace):
    """Coupe en lignes ; puis, si la dernière ligne n'a qu'un mot, lui en descend un de la ligne d'avant (pas de mot
    seul en dernière ligne). mots : [(mot, style, colle, longueur)]."""
    lignes = [[]]
    for m in mots:
        l = lignes[-1]
        lg = sum(x[3] for x in l) + sum(0 if x[2] else espace for x in l[1:])
        sep = 0 if m[2] else espace
        if l and not m[2] and lg + sep + m[3] > largeur:
            lignes.append([m])
        else:
            l.append(m)
    # un mot collé (ponctuation, apostrophe) voyage avec le mot qui le précède
    if len(lignes) > 1 and len(lignes[-1]) <= 2 and len(lignes[-2]) >= 3:
        groupe = 1
        while groupe < len(lignes[-2]) and lignes[-2][-groupe][2]:
            groupe += 1
        bloc = lignes[-2][-groupe:]
        essai = bloc + lignes[-1]
        lg = sum(x[3] for x in essai) + sum(0 if x[2] else espace for x in essai[1:])
        if len([x for x in lignes[-1] if not x[2]]) == 1 and lg <= largeur and len(lignes[-2]) - groupe >= 2:
            lignes[-2] = lignes[-2][:-groupe]
            lignes[-1] = essai
    return lignes


def _ecrire(d, x, y, largeur, texte, taille, graisse="Medium", graisse_forte="Bold", couleur=TEXTE,
            centre=False, interligne=1.3, accent=BLEU, dessiner=True):
    polices = {"n": police(taille, graisse), "g": police(taille, graisse_forte), "a": police(taille, graisse_forte)}
    couleurs = {"n": couleur, "g": NUIT if couleur == TEXTE else couleur, "a": accent}
    espace = polices["n"].getlength(" ")
    mots = [(m, s, c, polices[s].getlength(m)) for m, s, c in jetons(texte)]
    lignes = _couper(mots, largeur, espace)
    pas = round(taille * interligne)
    if dessiner:
        for k, ligne in enumerate(lignes):
            lg = sum(m[3] for m in ligne) + sum(0 if m[2] else espace for m in ligne[1:])
            cx = x + (largeur - lg) / 2 if centre else x
            for i, (mot, style, colle, l) in enumerate(ligne):
                if i and not colle:
                    cx += espace
                d.text((cx, y + k * pas), mot, font=polices[style], fill=couleurs[style])
                cx += l
    return len(lignes) * pas


def ecrire(d, x, y, largeur, texte, taille, **kw):
    """Texte riche, renvoyé à la ligne dans « largeur » ; un « \\n » ouvre un paragraphe. Renvoie la hauteur."""
    h = 0
    for k, para in enumerate(texte.split("\n")):
        if k:
            h += round(taille * 0.55)
        h += _ecrire(d, x, y + h, largeur, para, taille, **kw)
    return h


def hauteur(texte, taille, largeur, **kw):
    return ecrire(None, 0, 0, largeur, texte, taille, dessiner=False, **kw)


# ------------------------------------------------------------------ éléments
def pastille(d, x, y, texte, taille=28, fond=BLEU, couleur=BLANC, centre_x=None, graisse="Bold"):
    f = police(taille, graisse)
    l = f.getlength(texte)
    px, py = taille * 0.8, taille * 0.5
    if centre_x is not None:
        x = centre_x - (l + 2 * px) / 2
    d.rounded_rectangle([x, y, x + l + 2 * px, y + taille + 2 * py], radius=C.RADIUS, fill=fond)
    d.text((x + px, y + py + taille * 0.04), texte, font=f, fill=couleur)
    return taille + 2 * py


def puce(d, cx, cy, marque):
    r = 30
    if marque in ("ok", "non"):
        c = VERT if marque == "ok" else ROUGE
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        if marque == "ok":
            d.line([(cx - 13, cy + 1), (cx - 3, cy + 11), (cx + 14, cy - 10)], fill=BLANC, width=6, joint="curve")
        else:
            d.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=BLANC, width=6)
            d.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=BLANC, width=6)
        return
    if marque == "?":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLEU, width=4)
        d.text((cx, cy + 1), "?", font=police(32, "ExtraBold"), fill=BLEU, anchor="mm")
        return
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLEU)
    d.text((cx, cy + 1), marque, font=police(30, "Bold"), fill=BLANC, anchor="mm")


def toile(h):
    """Fond blanc, filet bleu en tête (le bandeau de la revue), pied de page du site."""
    im = Image.new("RGB", (W, h), BLANC)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=BLEU)
    return im, d


def entete(im, d, y, kicker=None, num=None, total=None):
    """Le logo du Cercle et son nom, comme l'en-tête de la revue ; la rubrique en pastille bleue dessous."""
    logo = Image.open(C.LOGO_SRC).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    logo.thumbnail((84, 84))
    im.paste(logo, (MARGE, y), logo)
    tx = MARGE + logo.width + 20
    d.text((tx, y + 6), "Le Cercle", font=police(32, "Bold"), fill=NUIT)
    d.text((tx, y + 42), "des Généralistes", font=police(32, "Bold"), fill=NUIT)
    if num:
        d.text((W - MARGE, y + logo.height / 2), f"{num}/{total}", font=police(28, "SemiBold"), fill=GRIS,
               anchor="rm")
    if kicker:
        pastille(d, MARGE, y + 120, kicker)
    return y + 120 + (80 if kicker else 0)


def pied(d, h, texte=None, glisser=False):
    y = h - 92
    d.line([(MARGE, y - 24), (W - MARGE, y - 24)], fill=FILET, width=2)
    d.text((MARGE, y), texte or f"Le Cercle des Généralistes · {URL}", font=police(24, "Medium"), fill=GRIS)
    if glisser:
        d.text((W - MARGE, y + 12), "Glissez →", font=police(28, "Bold"), fill=BLEU, anchor="rm")


def encadre(d, y, texte, taille=36, larg=None):
    """L'encadré bleu très pâle, filet bleu à gauche, comme « Le regard du Cercle » de la revue."""
    larg = larg or W - 2 * MARGE
    hl = hauteur(texte, taille, larg - 92, graisse="SemiBold")
    d.rounded_rectangle([MARGE, y, MARGE + larg, y + hl + 64], radius=C.RADIUS, fill=PALE)
    d.rectangle([MARGE, y + 10, MARGE + 8, y + hl + 54], fill=BLEU)
    ecrire(d, MARGE + 48, y + 32, larg - 92, texte, taille, graisse="SemiBold")
    return hl + 64


def intitule(d, y, texte):
    d.text((MARGE, y), texte, font=police(26, "Bold"), fill=BLEU)
    return 52


# ------------------------------------------------------------------ gabarits
def slide_titre(s, num, total):
    im, d = toile(H_FIL)
    entete(im, d, 70, s.get("kicker"), num, total)
    larg = W - 2 * MARGE
    t = s.get("taille_titre", 82)
    ht = hauteur(s["titre"], t, larg, graisse="ExtraBold", graisse_forte="ExtraBold", interligne=1.14)
    hs = hauteur(s.get("sous_titre", ""), 38, larg) + 44 if s.get("sous_titre") else 0
    y = 330 + (H_FIL - 330 - 180 - ht - hs) / 2
    y += ecrire(d, MARGE, y, larg, s["titre"], t, graisse="ExtraBold", graisse_forte="ExtraBold", couleur=NUIT,
                interligne=1.14)
    if s.get("sous_titre"):
        ecrire(d, MARGE, y + 44, larg, s["sous_titre"], 38, couleur=TEXTE)
    pied(d, H_FIL, glisser=True)
    return im


def slide_liste(s, num, total):
    """Titre, sous-titre, puis des lignes (marque, texte) — marque : « 1 », « ? », « ok », « non » — et un encadré."""
    im, d = toile(H_FIL)
    y = entete(im, d, 70, s.get("kicker"), num, total) + 40
    larg = W - 2 * MARGE
    y += ecrire(d, MARGE, y, larg, s["titre"], s.get("taille_titre", 66), graisse="ExtraBold",
                graisse_forte="ExtraBold", couleur=NUIT, interligne=1.15)
    if s.get("sous_titre"):
        y += 24
        y += ecrire(d, MARGE, y, larg, s["sous_titre"], 38, couleur=TEXTE)
    y += 48
    corps = s.get("taille", 40)
    for marque, texte in s.get("lignes", []):
        hl = hauteur(texte, corps, larg - 100)
        puce(d, MARGE + 30, y + corps * 0.64, marque)
        ecrire(d, MARGE + 100, y, larg - 100, texte, corps)
        y += hl + s.get("ecart", 38)
    if s.get("encadre"):
        y += 12
        y += encadre(d, y, s["encadre"])
    if s.get("adresse"):
        pastille(d, 0, H_FIL - 330, s["adresse"], taille=36, fond=NUIT, centre_x=W / 2)
        d.text((W / 2, H_FIL - 230), "Lien en bio", font=police(28, "SemiBold"), fill=GRIS, anchor="mm")
    pied(d, H_FIL, glisser=num < total)
    return im


def slide_fiche(f, num, total):
    """Une fiche du point pénuries : le médicament, sa présentation, la date (ou l'état) donnée par l'ANSM, le geste."""
    im, d = toile(H_FIL)
    y = entete(im, d, 70, "Le point pénuries", num, total) + 40
    larg = W - 2 * MARGE
    y += ecrire(d, MARGE, y, larg, f["nom"], 66, graisse="ExtraBold", graisse_forte="ExtraBold", couleur=BLEU,
                interligne=1.12)
    y += 14
    y += ecrire(d, MARGE, y, larg, f["forme"], 34, couleur=TEXTE)
    y += 40
    # la date de retour, dans l'encadré pâle
    lib = f.get("libelle", f"RETOUR ANNONCÉ PAR L{AP}ANSM")
    hv = hauteur(f["retour"], 44, larg - 92, graisse="Bold")
    d.rounded_rectangle([MARGE, y, W - MARGE, y + hv + 110], radius=C.RADIUS, fill=PALE)
    d.rectangle([MARGE, y + 10, MARGE + 8, y + hv + 100], fill=BLEU)
    d.text((MARGE + 48, y + 30), lib, font=police(24, "Bold"), fill=GRIS)
    ecrire(d, MARGE + 48, y + 70, larg - 92, f["retour"], 44, graisse="Bold", couleur=NUIT, accent=NUIT)
    y += hv + 110 + 50
    y += intitule(d, y, f.get("titre_gestes", "NOTRE CONSEIL AU CABINET"))
    for texte in f["gestes"]:
        hl = hauteur(texte, 38, larg - 100)
        puce(d, MARGE + 30, y + 25, "ok")
        ecrire(d, MARGE + 100, y, larg - 100, texte, 38)
        y += hl + 32
    if f.get("note"):
        y += 4
        ecrire(d, MARGE, y, larg, f["note"], 30, couleur=GRIS)
    pied(d, H_FIL, glisser=num < total)
    return im


def slide_chiffre(s, h):
    """Le visuel chiffre : un nombre en très grand, sa légende dessous."""
    im, d = toile(h)
    larg = W - 2 * MARGE
    y = entete(im, d, 70 if h == H_FIL else 250, s.get("kicker")) + (130 if h == H_FIL else 90)
    t = s.get("taille_chiffre", 300)
    d.text((W / 2, y), s["chiffre"], font=police(t, "Black"), fill=BLEU, anchor="mt")
    y += t * 0.80 + 40
    y += ecrire(d, MARGE, y, larg, s["legende"], 48, graisse="Bold", graisse_forte="ExtraBold", couleur=NUIT,
                centre=True, interligne=1.22)
    if s.get("detail"):
        y += 26
        y += ecrire(d, MARGE, y, larg, s["detail"], 34, couleur=TEXTE, centre=True)
    if s.get("encadre"):
        y += 44
        y += encadre(d, y, s["encadre"], taille=34)
    if h == H_FIL:
        pied(d, h, texte=s.get("pied"))
    else:
        ecrire(d, MARGE, 1480, larg, s["pied"], 28, couleur=GRIS, centre=True)
    return im


def slide_story(s):
    """Story : la rubrique, un titre, un texte, et la place du sticker (laissée vide, sous la flèche)."""
    im, d = toile(H_STORY)
    larg = W - 2 * MARGE
    y = entete(im, d, 250, s["kicker"]) + 70
    y += ecrire(d, MARGE, y, larg, s["titre"], s.get("taille_titre", 76), graisse="ExtraBold",
                graisse_forte="ExtraBold", couleur=NUIT, interligne=1.14)
    y += 40
    y += ecrire(d, MARGE, y, larg, s["texte"], 42, couleur=TEXTE)
    if s.get("sticker"):
        d.text((W / 2, y + 60), "↓", font=police(80, "Bold"), fill=BLEU, anchor="mt")
    if s.get("pied"):
        ecrire(d, MARGE, 1500, larg, s["pied"], 28, couleur=GRIS, centre=True)
    return im


# ------------------------------------------------------------------ Secteur 3 (PDF p. 9 et 10)
SECTEUR3 = [
    # p. 9, SITUATION : « à partir du 1er janvier 2027, les prescriptions des médecins non conventionnés ne seront plus
    # remboursées : leurs patients viendront vers vous »
    ("titre", {"kicker": "Médecins généralistes",
               "titre": f"Au 1er{NB}janvier 2027, les ordonnances du *secteur{NB}3* ne seront plus remboursées.",
               "sous_titre": f"Les prescriptions des médecins non conventionnés. Leurs patients viendront vers "
                             f"vous."}),
    # p. 9, L'ESSENTIEL et CE QUI EST CONFIRMÉ (article 76 : « à l'exception de ceux prescrits par ces médecins à titre
    # gracieux, pour eux-mêmes et pour leurs proches » ; CE n° 517230 du 1er octobre 2026)
    ("liste", {"kicker": "Ce qui change", "titre": f"Au 1er{NB}janvier 2027", "taille": 38, "ecart": 32,
               "lignes": [
                   ("1", f"Médicaments, actes et prestations prescrits par un médecin non conventionné{NB}: "
                         f"**plus de remboursement**."),
                   ("2", f"**Seule exception**{NB}: ce qu{AP}il prescrit à titre gracieux, pour lui-même et ses "
                         f"proches."),
                   ("3", f"La base{NB}: l{AP}**article{NB}76** de la loi de financement de la Sécurité sociale pour "
                         f"2026."),
                   ("4", f"Le 1er{NB}octobre, le Conseil d{AP}État a **refusé de transmettre** la question des "
                         f"syndicats au Conseil constitutionnel."),
               ]}),
    # p. 9, L'ESSENTIEL (« les recevoir en consultation plutôt que recopier une ordonnance ») ; p. 10, L'IMPACT (afflux
    # en janvier, période hivernale) et REGARD (« guichet de recopie ») : lecture du dossier, attribuée
    ("liste", {"kicker": "Au cabinet", "titre": f"Ce qui risque d{AP}arriver *dans votre salle d{AP}attente*",
               "sous_titre": f"Selon le Cercle{NB}:",
               "lignes": [
                   ("1", f"Des patients qui vous demandent de **recopier une ordonnance** de leur médecin non "
                         f"conventionné."),
                   ("2", f"Un **afflux de demandes en janvier**{NB}: renouvellements de traitements chroniques, "
                         f"biologie, kinésithérapie."),
                   ("3", f"En **pleine période hivernale**."),
               ]}),
    # p. 10, RECOMMANDATIONS, médecin généraliste conventionné ; REGARD (« une consultation et un examen, pas un
    # tampon »)
    ("liste", {"kicker": f"Dès décembre", "titre": "Ce que vous pouvez *préparer*",
               "lignes": [
                   ("1", f"Prévoyez des **créneaux de reprise de suivi** pour ces patients, dès{NB}décembre."),
                   ("2", f"À cette consultation, proposez de vous **déclarer médecin traitant**, plutôt que de "
                         f"recopier l{AP}ordonnance."),
               ],
               "encadre": f"Selon le Cercle, reprendre un traitement suppose une consultation et un examen, "
                          f"*pas un tampon*."}),
    # p. 10, RECOMMANDATIONS, secrétariat médical
    ("liste", {"kicker": "Pour votre secrétariat",
               "titre": f"*«{NB}Qui vous a prescrit cette{NB}ordonnance{NB}?{NB}»*", "taille_titre": 78,
               "sous_titre": "La question à poser au téléphone, quand un patient appelle pour une ordonnance.",
               "encadre": f"Si ce médecin n{AP}est pas conventionné{NB}: proposer une **consultation avant le "
                          f"1er{NB}janvier 2027**, plutôt qu{AP}un simple renouvellement."}),
    # p. 9-10, CE QUI POSE QUESTION (3 questions, au 19 novembre)
    ("liste", {"kicker": "Encore sans réponse", "titre": f"3 questions *ouvertes* au 19{NB}novembre",
               "lignes": [
                   ("?", f"Une ordonnance rédigée en 2026, délivrée en 2027, **sera-t-elle remboursée**{NB}?"),
                   ("?", f"Comment le **pharmacien** saura-t-il que le prescripteur n{AP}est pas conventionné{NB}?"),
                   ("?", f"Comment le patient, le **laboratoire** ou l{AP}**infirmier** sauront-ils que la "
                         f"prescription n{AP}est pas remboursable{NB}?"),
               ]}),
    # p. 10, REGARD : « Le Cercle demande à l'Assurance Maladie d'informer les patients concernés avant le 1er janvier, de
    # préciser le sort des ordonnances en cours, et de reconnaître la consultation de reprise de traitement »
    ("liste", {"kicker": "Le dossier complet", "titre": f"Ce que le Cercle demande *à l{AP}Assurance Maladie*",
               "sous_titre": f"Et notre analyse de la mesure, dans le dossier de la revue du 19{NB}novembre "
                             f"(inscription gratuite).", "adresse": URL}),
]

# ------------------------------------------------------------------ Pénuries (PDF p. 17 à 19)
PENURIES = [
    # p. 17, SITUATION et L'ESSENTIEL ; le furosémide vient de l'actualité de l'ANSM du 18 novembre (CONTEXTE)
    ("titre", {"kicker": f"Le point pénuries · 19{NB}novembre",
               "titre": f"6 médicaments en tension{NB}: *ce que le prescripteur peut{NB}faire*",
               "sous_titre": f"Une sélection des tensions signalées par l{AP}ANSM, et le geste au cabinet. "
                             f"À{NB}garder pour vos consultations."}),
    # p. 17 (fiche du 13 novembre) ; p. 19, RECOMMANDATIONS du Cercle (« comme le demande la check-list de l'ANSM pour
    # Jext » ; « Stock de dépannage d'urgence en ville » prévu par l'ANSM)
    ("fiche", {"nom": f"Jext 300{NB}µg", "forme": f"Adrénaline, stylo prérempli · contingenté en{NB}ville",
               "retour": "courant décembre 2026",
               "gestes": [f"Vérifiez à la prochaine consultation que le patient allergique a **2{NB}stylos non "
                          f"périmés**, comme le demande la check-list de l{AP}ANSM.",
                          f"Plus de Jext 300 dans sa pharmacie{NB}? Signalez au pharmacien le **«{NB}Stock de "
                          f"dépannage d{AP}urgence en ville{NB}»**."]}),
    # p. 17 (fiche du 3 novembre : ville et hôpital ; diazépam 10 mg sécable disponible) ; p. 19, RECOMMANDATIONS (DCI)
    ("fiche", {"nom": f"Diazépam 5{NB}mg",
               "forme": f"Diazépam Teva 5{NB}mg · contingenté en ville et à{NB}l{AP}hôpital",
               "retour": "fin novembre 2026",
               "gestes": [f"Prescrivez **en DCI**{NB}: la fiche de l{AP}ANSM ne vise que la spécialité de Teva. Le "
                          f"pharmacien peut délivrer celle d{AP}un autre laboratoire, si elle est disponible."],
               "note": f"L{AP}ANSM signale le diazépam 10{NB}mg sécable disponible, sans le présenter comme une "
                       f"alternative."}),
    # p. 17 (fiche du 4 novembre : aucune alternative citée) ; p. 19, RECOMMANDATIONS (DCI)
    ("fiche", {"nom": "Cotrimoxazole",
               "forme": f"Cotrimoxazole Teva 800{NB}mg/160{NB}mg · contingenté en{NB}ville",
               "retour": "janvier 2027",
               "gestes": [f"Prescrivez **en DCI**{NB}: la fiche de l{AP}ANSM ne vise que la spécialité de Teva. Le "
                          f"pharmacien peut délivrer celle d{AP}un autre laboratoire, si elle est disponible."],
               "note": f"La fiche de l{AP}ANSM ne cite aucune alternative."}),
    # p. 18 (fiche du 26 octobre) ; p. 19, RECOMMANDATIONS (DCI ; « stock limité de dépannage d'urgence en ville »)
    ("fiche", {"nom": f"Nifédipine LP 30{NB}mg",
               "forme": f"Nifédipine Viatris L.P. 30{NB}mg · contingenté en{NB}ville",
               "retour": "début décembre 2026",
               "gestes": [f"Prescrivez **en DCI**{NB}: la fiche de l{AP}ANSM ne vise que la spécialité de Viatris. "
                          f"Le pharmacien peut délivrer celle d{AP}un autre laboratoire, si elle est disponible.",
                          f"Signalez-lui le **«{NB}stock limité de dépannage d{AP}urgence en ville{NB}»**."]}),
    # p. 17, CONTEXTE (ANSM, 18 novembre)
    ("fiche", {"nom": f"Furosémide 20 et 40{NB}mg", "forme": "Comprimés",
               "libelle": f"TENSIONS SELON L{AP}ANSM (18{NB}NOVEMBRE)",
               "retour": f"«{NB}Devraient durer encore plusieurs mois en{NB}2027{NB}»",
               "titre_gestes": f"CE QUE PERMET L{AP}ANSM",
               "gestes": [f"Le pharmacien peut remplacer les comprimés indisponibles par une **préparation "
                          f"magistrale**, **sans nouvelle ordonnance**."]}),
    # p. 18 (fiche du 17 novembre)
    ("fiche", {"nom": "Zovirax suspension",
               "forme": f"Aciclovir 200{NB}mg/5{NB}ml, suspension buvable · contingenté en{NB}ville",
               "retour": "courant janvier 2027", "titre_gestes": f"BON À SAVOIR (ANSM)",
               "gestes": [f"«{NB}La spécialité **Zovirax 200{NB}mg comprimés reste disponible** pendant la durée "
                          f"de la tension de la suspension buvable{NB}».",
                          f"Un **stock de dépannage d{AP}urgence en ville** est prévu."]}),
    # p. 18, L'IMPACT (« un contingentement ne veut pas dire que le produit manque partout ») ; p. 19, REGARD : le Cercle
    # demande une conduite à tenir pour le prescripteur et une alerte dans le logiciel métier (gardé pour le site)
    ("liste", {"kicker": "Le point pénuries", "titre": f"Contingenté ne veut pas dire *introuvable*",
               "sous_titre": f"Selon le Cercle, la disponibilité peut varier d{AP}une officine et d{AP}une semaine "
                             f"à l{AP}autre.",
               "encadre": f"Ce que le Cercle demande pour le prescripteur, et les questions encore ouvertes{NB}: "
                          f"dans le dossier de la revue du 19{NB}novembre (inscription gratuite).",
               "adresse": URL}),
]

# ------------------------------------------------------------------ Tiers payant et DPC (PDF p. 2 à 5)
# p. 3 : « l'article 32, adopté le 16 novembre, fixe à un an après l'acte le délai pour se faire payer en tiers
# payant, contre 2 ans aujourd'hui selon le rapport de la commission » ; p. 2 : votes non définitifs
TIERS_PAYANT = {"kicker": f"Tiers payant · PLFSS{NB}2027", "chiffre": "1 an", "taille_chiffre": 300,
                "legende": f"après l{AP}acte, pour vous faire payer *en tiers payant*, selon le texte voté par le "
                           f"Sénat",
                "detail": f"Contre 2{NB}ans aujourd{AP}hui, selon le rapport de la commission (article{NB}32, "
                          f"16{NB}novembre).",
                "pied": f"Texte non définitif · {URL}"}
# story : la même chose, plus la lecture du Cercle (p. 5, REGARD, attribuée)
TIERS_PAYANT_STORY = dict(TIERS_PAYANT,
                          encadre=f"Selon le Cercle, un acte refacturé plus d{AP}un an après sa réalisation ne serait "
                                  f"*plus payé*{NB}: le risque des rejets passe sur le cabinet.",
                          pied=f"Texte non définitif{NB}: il doit encore passer en commission mixte paritaire.")
# p. 3 : « selon le rapport de la commission, l'article 33, adopté le même jour, supprime l'Agence nationale du
# développement professionnel continu et l'obligation de DPC pour les professions dotées d'un ordre, soumises à la
# certification périodique, au plus tard fin 2027 » ; p. 4, question ouverte sur le financement de la formation
DPC_STORY = {"kicker": f"DPC · PLFSS{NB}2027",
             "titre": f"Le Sénat vote la fin de l{AP}obligation de *DPC*",
             "texte": f"Selon le rapport de la commission, l{AP}article{NB}33, voté le 16{NB}novembre, supprime "
                      f"l{AP}Agence nationale du DPC et l{AP}obligation de DPC pour les professions dotées d{AP}un "
                      f"ordre, soumises à la **certification périodique**, **au plus tard fin{NB}2027**.\n"
                      f"La formation restera-t-elle financée au même niveau{NB}?",
             "sticker": True, "pied": f"Texte non définitif{NB}: commission mixte paritaire à venir."}

# ------------------------------------------------------------------ Stories du reel taxe lapin (PDF p. 2 à 5)
LAPIN_SONDAGE = {"kicker": f"Taxe lapin · PLFSS{NB}2027",
                 "titre": f"Si la loi passe, l{AP}appliqueriez-vous *à vos patients*{NB}?",
                 "texte": f"Le Sénat a voté une pénalité pour les rendez-vous non honorés, **jusqu{AP}au prix de la "
                          f"consultation**, si le patient a été informé à la prise de rendez-vous et a reçu un "
                          f"rappel. Sauf motif impérieux ou de santé. Texte non définitif.",
                 "sticker": True}
LAPIN_LIEN = {"kicker": f"Taxe lapin · PLFSS{NB}2027",
              "titre": f"Et la pénalité, *qui l{AP}encaisse*{NB}?",
              "texte": f"Le texte voté prévoit un paiement à la caisse d{AP}assurance maladie du patient, sans dire si "
                       f"la somme vous est reversée. Notre analyse et notre recommandation{NB}:",
              "sticker": True}


# ------------------------------------------------------------------ sortie
SORTIE = ICI / "visuels"


def planche(nom, images, cols=4):
    w, h = images[0].size
    k = 0.3
    lignes = (len(images) + cols - 1) // cols
    p = Image.new("RGB", (int(cols * w * k) + (cols + 1) * 16, int(lignes * h * k) + (lignes + 1) * 16),
                  (200, 205, 215))
    for i, im in enumerate(images):
        p.paste(im.resize((int(w * k), int(h * k))), (16 + (i % cols) * (int(w * k) + 16),
                                                     16 + (i // cols) * (int(h * k) + 16)))
    p.save(SORTIE / f"planche_{nom}.png")


def serie(nom, slides):
    total = len(slides)
    images = []
    for i, (genre, s) in enumerate(slides, 1):
        im = {"titre": slide_titre, "fiche": slide_fiche, "liste": slide_liste}[genre](s, i, total)
        im.save(SORTIE / f"{nom}_{i}.png", optimize=True)
        images.append(im)
    planche(nom, images)


if __name__ == "__main__":
    SORTIE.mkdir(exist_ok=True)
    serie("secteur3", SECTEUR3)
    serie("penuries", PENURIES)
    autres = {"tiers_payant_4x5": slide_chiffre(TIERS_PAYANT, H_FIL),
              "story_tiers_payant": slide_chiffre(TIERS_PAYANT_STORY, H_STORY),
              "story_dpc": slide_story(DPC_STORY),
              "story_taxe_lapin_sondage": slide_story(LAPIN_SONDAGE),
              "story_taxe_lapin_lien": slide_story(LAPIN_LIEN)}
    for n, im in autres.items():
        im.save(SORTIE / f"{n}.png", optimize=True)
    planche("chiffre_et_stories", list(autres.values())[1:], cols=4)
    autres["tiers_payant_4x5"].resize((540, 675)).save(SORTIE / "planche_tiers_payant.png")
    print(len(list(SORTIE.glob("*.png"))), "images dans", SORTIE)
