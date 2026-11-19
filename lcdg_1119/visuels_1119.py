"""Visuels du 19/11/2026, tirés de la revue du 19/11 (LCDG_revue_du_19-11-2026.pdf, lue en entier), sur le plan de
Romain du 19/11 (« enchaîne sur tout ! il faut tout faire ! ») :
- carrousel Secteur 3, 7 slides (4:5) : « une date butoir et des gestes concrets à faire avant » ;
- carrousel « Le point pénuries », une slide par médicament (4:5) : « le sujet que le médecin garde » ;
- visuel chiffre « 1 an » (tiers payant, 4:5), sa story, et une story DPC (9:16) ;
- les deux stories du reel taxe lapin (sondage, lien), en 9:16.

Style : celui de carrousel_planche.png (fond indigo, titre blanc à mot coloré, puces rondes numérotées, adresse en
pastille blanche), avec la police et le logo de lcdg-reel (charte inchangée). Balises du texte : *mot coloré*,
**gras**. Rien n'est inventé : chaque slide porte sa source (page du PDF) en commentaire. Les opinions du regard du
Cercle et les lectures de « L'impact » sont attribuées (« Selon le Cercle », « Selon nous »).

Stories : tout le contenu tient entre y 250 et 1560 (barre du haut et champ de réponse d'Instagram) ; la zone
laissée vide est celle du sticker (sondage ou lien), à poser dans Instagram.

    python visuels_1119.py            -> lcdg_1119/visuels/*.png et visuels/planche_*.png"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ICI = Path(__file__).resolve().parent
MOTEUR = ICI.parents[1] / "lcdg-reel"
if not MOTEUR.exists():
    MOTEUR = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
POLICE = MOTEUR / "assets" / "fonts" / "Montserrat.ttf"
LOGO = MOTEUR / "assets" / "logo" / "LOGO_LCDG.png"
SORTIE = ICI / "visuels"

NB, AP = "\u00a0", "\u2019"
# couleurs relevées sur carrousel_planche.png (fond, texte crème) ; accent cyan de la planche ; rouge et vert des
# rubriques « patient » et « clinique » de config/charte.py
FOND = (27, 8, 104)
FOND_BAS = (44, 22, 132)
CREME = (249, 244, 230)
ACCENT = (64, 200, 222)
ROUGE = (240, 72, 110)
VERT = (52, 199, 140)
GRIS = (178, 173, 204)
NAVY = (27, 16, 70)

W = 1080
H_FIL, H_STORY = 1350, 1920
MARGE = 96

_cache = {}


def police(taille, graisse="Medium"):
    cle = (taille, graisse)
    if cle not in _cache:
        f = ImageFont.truetype(str(POLICE), taille)
        f.set_variation_by_name(graisse)
        _cache[cle] = f
    return _cache[cle]


def fond(h):
    im = Image.new("RGB", (W, h), FOND)
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(FOND, FOND_BAS)))
    # un grand cercle très pâle, comme le filigrane de la planche de référence
    voile = Image.new("L", (W, h), 0)
    ImageDraw.Draw(voile).ellipse([W * 0.18, h * 0.30, W * 1.18, h * 0.30 + W], outline=40, width=3)
    voile = voile.filter(ImageFilter.GaussianBlur(1))
    im.paste(Image.new("RGB", (W, h), CREME), (0, 0), voile.point(lambda v: v // 3))
    return im


def jetons(texte):
    """[(mot, style, colle)] : style « n » normal, « g » gras, « a » accent (gras coloré) ; « colle » quand aucun espace
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


def ecrire(d, x, y, largeur, texte, taille, **kw):
    """Texte riche, renvoyé à la ligne dans « largeur » ; un « \\n » ouvre un paragraphe. Renvoie la hauteur écrite."""
    h = 0
    for k, para in enumerate(texte.split("\n")):
        h += (round(taille * 0.5) if k else 0) + _ecrire(d, x, y + h + (round(taille * 0.5) if k else 0), largeur,
                                                          para, taille, **kw)
    return h


def _ecrire(d, x, y, largeur, texte, taille, graisse="Medium", graisse_forte="Bold", couleur=CREME,
           centre=False, interligne=1.28, accent=ACCENT):
    """Texte riche, renvoyé à la ligne dans « largeur » ; renvoie la hauteur écrite."""
    polices = {"n": police(taille, graisse), "g": police(taille, graisse_forte), "a": police(taille, graisse_forte)}
    couleurs = {"n": couleur, "g": couleur, "a": accent}
    espace = polices["n"].getlength(" ")
    lignes, ligne, lg = [], [], 0
    for mot, style, colle in jetons(texte):
        l = polices[style].getlength(mot)
        # un signe de ponctuation collé au mot précédent (« *mot*, ») ne passe jamais seul à la ligne
        sep = 0 if (colle and ligne) else espace
        if ligne and lg + sep + l > largeur and not (sep == 0):
            lignes.append((ligne, lg))
            ligne, lg, sep = [], 0, 0
        ligne.append((mot, style, sep if ligne else 0, l))
        lg += (sep if len(ligne) > 1 else 0) + l
    if ligne:
        lignes.append((ligne, lg))
    pas = round(taille * interligne)
    for k, (ligne, lg) in enumerate(lignes):
        cx = x + (largeur - lg) / 2 if centre else x
        for mot, style, sep, l in ligne:
            cx += sep
            d.text((cx, y + k * pas), mot, font=polices[style], fill=couleurs[style])
            cx += l
    return len(lignes) * pas


def hauteur(texte, taille, largeur, **kw):
    im = Image.new("RGB", (10, 10))
    return ecrire(ImageDraw.Draw(im), 0, -10000, largeur, texte, taille, **kw)


def pastille(d, x, y, texte, taille=30, fond_=CREME, couleur=FOND, centre_x=None, graisse="Bold"):
    f = police(taille, graisse)
    l = f.getlength(texte)
    px, py = taille * 0.8, taille * 0.45
    if centre_x is not None:
        x = centre_x - (l + 2 * px) / 2
    d.rounded_rectangle([x, y, x + l + 2 * px, y + taille + 2 * py], radius=(taille + 2 * py) / 2, fill=fond_)
    d.text((x + px, y + py + taille * 0.02), texte, font=f, fill=couleur)
    return taille + 2 * py, l + 2 * px


def puce(d, cx, cy, marque, couleur=ACCENT):
    r = 30
    if marque in ("ok", "non"):
        c = VERT if marque == "ok" else ROUGE
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        if marque == "ok":
            d.line([(cx - 13, cy + 1), (cx - 3, cy + 11), (cx + 14, cy - 10)], fill=CREME, width=6, joint="curve")
        else:
            d.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=CREME, width=6)
            d.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=CREME, width=6)
        return
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=couleur, width=4)
    f = police(30, "Bold")
    d.text((cx, cy + 1), marque, font=f, fill=CREME, anchor="mm")


def entete(im, d, kicker, num=None, total=None):
    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((92, 92))
    im.paste(logo, (MARGE, 70), logo)
    d.text((MARGE + logo.width + 20, 70 + logo.height / 2), "Le Cercle des Généralistes", font=police(28, "Bold"),
           fill=CREME, anchor="lm")
    if num:
        d.text((W - MARGE, 70 + logo.height / 2), f"{num}/{total}", font=police(28, "SemiBold"), fill=GRIS, anchor="rm")
    if kicker:
        pastille(d, MARGE, 200, kicker, taille=28, fond_=ACCENT, couleur=FOND)


def slide_liste(s, num, total, h=H_FIL):
    """Titre, puis des lignes : (marque, texte). Marque : « 1 », «  ? », « ok », « non », « ! »."""
    im = fond(h)
    d = ImageDraw.Draw(im)
    haut = 250 if h == H_STORY else 0
    entete(im, d, s.get("kicker"), num, total) if h == H_FIL else None
    if h == H_STORY:
        d2 = ImageDraw.Draw(im)
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((84, 84))
        im.paste(logo, (MARGE, haut), logo)
        d2.text((MARGE + logo.width + 18, haut + logo.height / 2), "Le Cercle des Généralistes",
                font=police(28, "Bold"), fill=CREME, anchor="lm")
        if s.get("kicker"):
            pastille(d2, MARGE, haut + 120, s["kicker"], taille=28, fond_=ACCENT, couleur=FOND)
        y = haut + 230
    else:
        y = 300
    larg = W - 2 * MARGE
    y += ecrire(d, MARGE, y, larg, s["titre"], s.get("taille_titre", 68), graisse="ExtraBold",
                graisse_forte="ExtraBold", interligne=1.15)
    if s.get("sous_titre"):
        y += 28
        y += ecrire(d, MARGE, y, larg, s["sous_titre"], 38, graisse="Medium", couleur=GRIS, accent=ACCENT)
    y += 50
    corps = s.get("taille", 42)
    for marque, texte in s.get("lignes", []):
        hl = hauteur(texte, corps, larg - 100)
        puce(d, MARGE + 30, y + corps * 0.62, marque)
        ecrire(d, MARGE + 100, y, larg - 100, texte, corps)
        y += hl + s.get("ecart", 34)
    if s.get("encadre"):
        y += 10
        texte = s["encadre"]
        hl = hauteur(texte, 38, larg - 80, graisse="SemiBold")
        d.rounded_rectangle([MARGE, y, W - MARGE, y + hl + 64], radius=28, outline=ACCENT, width=3)
        ecrire(d, MARGE + 40, y + 32, larg - 80, texte, 38, graisse="SemiBold")
        y += hl + 60
    if s.get("pied"):
        f = police(26, "Medium")
        ecrire(d, MARGE, h - 150 if h == H_FIL else 1500, larg, s["pied"], 26, couleur=GRIS)
    if s.get("adresse"):
        yy = (h - 250) if h == H_FIL else 1380
        pastille(d, 0, yy, s["adresse"], taille=34, centre_x=W / 2)
    if s.get("glisser"):
        d.text((W - MARGE, h - 90), "Glissez →", font=police(30, "Bold"), fill=ACCENT, anchor="rm")
    return im, y


def slide_titre(s, num, total, h=H_FIL):
    """Une slide d'ouverture : un grand titre centré verticalement."""
    im = fond(h)
    d = ImageDraw.Draw(im)
    entete(im, d, s.get("kicker"), num, total)
    larg = W - 2 * MARGE
    ht = hauteur(s["titre"], s.get("taille_titre", 84), larg, graisse="ExtraBold", graisse_forte="ExtraBold",
                 interligne=1.12)
    hs = hauteur(s.get("sous_titre", ""), 38, larg) if s.get("sous_titre") else 0
    y = (h - ht - hs - 40) / 2 + 20
    y += ecrire(d, MARGE, y, larg, s["titre"], s.get("taille_titre", 84), graisse="ExtraBold",
                graisse_forte="ExtraBold", interligne=1.12)
    if s.get("sous_titre"):
        ecrire(d, MARGE, y + 40, larg, s["sous_titre"], 38, couleur=GRIS)
    if s.get("pied"):
        ecrire(d, MARGE, h - 150, larg, s["pied"], 26, couleur=GRIS)
    if s.get("glisser"):
        d.text((W - MARGE, h - 90), "Glissez →", font=police(30, "Bold"), fill=ACCENT, anchor="rm")
    return im


def slide_chiffre(s, h):
    """Le visuel chiffre : un nombre en très grand, sa légende dessous."""
    im = fond(h)
    d = ImageDraw.Draw(im)
    larg = W - 2 * MARGE
    if h == H_FIL:
        entete(im, d, s.get("kicker"))
        y = 330
    else:
        haut = 250
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((84, 84))
        im.paste(logo, (MARGE, haut), logo)
        d.text((MARGE + logo.width + 18, haut + logo.height / 2), "Le Cercle des Généralistes",
               font=police(28, "Bold"), fill=CREME, anchor="lm")
        pastille(d, MARGE, haut + 120, s["kicker"], taille=28, fond_=ACCENT, couleur=FOND)
        y = haut + 290
    f = police(s.get("taille_chiffre", 300), "Black")
    d.text((W / 2, y), s["chiffre"], font=f, fill=ACCENT, anchor="mt")
    y += s.get("taille_chiffre", 300) * 0.82 + 40
    y += ecrire(d, MARGE, y, larg, s["legende"], 46, graisse="Bold", graisse_forte="ExtraBold", centre=True,
                interligne=1.22)
    if s.get("detail"):
        y += 30
        y += ecrire(d, MARGE, y, larg, s["detail"], 32, couleur=GRIS, centre=True)
    if s.get("encadre"):
        y += 40
        hl = hauteur(s["encadre"], 32, larg - 80, graisse="SemiBold")
        d.rounded_rectangle([MARGE, y, W - MARGE, y + hl + 56], radius=28, outline=ACCENT, width=3)
        ecrire(d, MARGE + 40, y + 28, larg - 80, s["encadre"], 32, graisse="SemiBold")
    if s.get("pied"):
        ecrire(d, MARGE, (h - 150) if h == H_FIL else 1490, larg, s["pied"], 26, couleur=GRIS, centre=True)
    return im


def slide_story(s):
    """Story : un titre, un texte, et la place du sticker (laissée vide)."""
    im = fond(H_STORY)
    d = ImageDraw.Draw(im)
    haut = 250
    larg = W - 2 * MARGE
    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((84, 84))
    im.paste(logo, (MARGE, haut), logo)
    d.text((MARGE + logo.width + 18, haut + logo.height / 2), "Le Cercle des Généralistes", font=police(28, "Bold"),
           fill=CREME, anchor="lm")
    pastille(d, MARGE, haut + 120, s["kicker"], taille=28, fond_=ACCENT, couleur=FOND)
    y = haut + 250
    y += ecrire(d, MARGE, y, larg, s["titre"], s.get("taille_titre", 78), graisse="ExtraBold",
                graisse_forte="ExtraBold", interligne=1.14)
    y += 36
    y += ecrire(d, MARGE, y, larg, s["texte"], 42, couleur=CREME)
    if s.get("sticker"):
        # la place du sticker : une flèche discrète qui y mène, rien d'autre
        d.text((W / 2, y + 70), "↓", font=police(80, "Bold"), fill=ACCENT, anchor="mt")
    if s.get("pied"):
        ecrire(d, MARGE, 1500, larg, s["pied"], 26, couleur=GRIS, centre=True)
    return im


# ------------------------------------------------------------------ Secteur 3 (PDF p. 9 et 10)
URL = "lecercledesgeneralistes.fr"
SECTEUR3 = [
    # p. 9, SITUATION : « les prescriptions des médecins non conventionnés ne seront plus remboursées : leurs
    # patients viendront vers vous »
    ("titre", {"kicker": "Médecins généralistes",
               "titre": f"Au 1er{NB}janvier, leurs ordonnances *ne seront plus remboursées*.",
               "sous_titre": f"Les prescriptions des médecins non conventionnés (secteur{NB}3). Leurs patients "
                             f"viendront vers vous.", "glisser": True}),
    # p. 9, L'ESSENTIEL et CE QUI EST CONFIRMÉ (article 76, L. 162-5-10 ; CE n° 517230 du 1er octobre 2026)
    ("liste", {"kicker": "Ce qui change", "titre": f"Au 1er{NB}janvier 2027", "taille": 38, "ecart": 32,
               "lignes": [
                   ("1", f"Médicaments, actes et prestations prescrits par un médecin non conventionné{NB}: "
                         f"**plus de remboursement**."),
                   ("2", f"**Seule exception**{NB}: ce qu{AP}il prescrit gratuitement, pour lui-même et ses proches."),
                   ("3", f"La base{NB}: l{AP}**article 76** de la loi de financement de la Sécurité sociale pour 2026."),
                   ("4", f"Le 1er{NB}octobre, le Conseil d{AP}État a **refusé de transmettre** la question des "
                         f"syndicats au Conseil constitutionnel."),
               ], "glisser": True}),
    # p. 9-10 : L'ESSENTIEL (« recevoir en consultation plutôt que recopier une ordonnance ») ; L'IMPACT (afflux en
    # janvier, période hivernale) : lecture du dossier, attribuée
    ("liste", {"kicker": "Au cabinet", "titre": f"Ce qui va arriver *dans votre salle d{AP}attente*",
               "lignes": [
                   ("!", f"Des patients qui vous demandent de **recopier une ordonnance** de leur médecin non "
                         f"conventionné."),
                   ("!", f"Selon le Cercle, un **afflux de demandes en janvier**{NB}: renouvellements de traitements "
                         f"chroniques, biologie, kinésithérapie."),
                   ("!", f"En **pleine période hivernale**."),
               ], "glisser": True}),
    # p. 10, RECOMMANDATIONS, médecin généraliste conventionné ; REGARD (« une consultation et un examen, pas un
    # tampon »)
    ("liste", {"kicker": "Dès décembre", "titre": "Ce que vous pouvez *préparer*",
               "lignes": [
                   ("1", f"Prévoyez des **créneaux de reprise de suivi** pour ces patients, dès décembre."),
                   ("2", f"À cette consultation, proposez de vous **déclarer médecin traitant**, plutôt que de "
                         f"recopier l{AP}ordonnance."),
               ],
               "encadre": f"Selon le Cercle, reprendre un traitement suppose une consultation et un examen, "
                          f"*pas un tampon*.", "glisser": True}),
    # p. 10, RECOMMANDATIONS, secrétariat médical
    ("liste", {"kicker": "Pour votre secrétariat",
               "titre": f"*«{NB}Qui vous a prescrit cette ordonnance{NB}?{NB}»*", "taille_titre": 80,
               "sous_titre": "La question à poser au téléphone, quand un patient appelle pour une ordonnance.",
               "encadre": f"Si ce médecin n{AP}est pas conventionné{NB}: proposer une **consultation avant le "
                          f"1er{NB}janvier 2027**, plutôt qu{AP}un simple renouvellement.", "glisser": True}),
    # p. 9-10, CE QUI POSE QUESTION (3 questions, au 19 novembre)
    ("liste", {"kicker": "Encore sans réponse", "titre": f"3 questions *ouvertes* au 19{NB}novembre",
               "lignes": [
                   ("?", f"Une ordonnance rédigée en 2026, délivrée en 2027, **sera-t-elle remboursée**{NB}?"),
                   ("?", f"Comment le **pharmacien** saura-t-il que le prescripteur n{AP}est pas conventionné{NB}?"),
                   ("?", f"Comment le patient, le **laboratoire** ou l{AP}**infirmier** sauront-ils que la "
                         f"prescription n{AP}est pas remboursable{NB}?"),
               ], "glisser": True}),
    # p. 10, REGARD : ce que le Cercle demande à l'Assurance Maladie (gardé pour le site, annoncé ici)
    ("liste", {"kicker": "Le dossier complet", "titre": f"Ce que le Cercle demande *à l{AP}Assurance Maladie*",
               "sous_titre": f"Et notre analyse de la mesure, dans le dossier de la revue du 19{NB}novembre "
                             f"(inscription gratuite).", "adresse": URL,
               "pied": "Lien en bio"}),
]

# ------------------------------------------------------------------ Pénuries (PDF p. 17 à 19)
def fiche(nom, forme, retour, statut, gestes, note=None):
    lignes = [("ok", g) for g in gestes]
    return ("liste", {"kicker": "Le point pénuries", "titre": f"*{nom}*", "taille_titre": 64,
                      "sous_titre": forme, "lignes": lignes, "encadre": f"**Retour annoncé par l{AP}ANSM**{NB}: {retour}"
                      + (f"\n" if False else "") , "statut": statut, "note": note})


PENURIES = [
    # p. 17, SITUATION et L'ESSENTIEL ; « contingentement » : p. 18, L'IMPACT
    ("titre", {"kicker": f"Le point pénuries · 19{NB}novembre",
               "titre": f"6 médicaments en tension{NB}: *ce que le prescripteur peut faire*",
               "sous_titre": f"Une sélection de la liste de l{AP}ANSM : la date de retour annoncée, et le geste au cabinet. À "
                             f"garder pour vos consultations.", "glisser": True}),
    # p. 17 (fiche du 13 novembre) ; p. 19, RECOMMANDATIONS (check-list de l'ANSM, stock de dépannage)
    ("fiche", {"nom": "Jext 300 µg", "forme": f"Adrénaline, stylo prérempli · contingenté en ville",
               "retour": f"courant décembre 2026",
               "gestes": [f"Vérifiez à la prochaine consultation que le patient allergique a **2{NB}stylos non "
                          f"périmés** (check-list de l{AP}ANSM).",
                          f"Plus de Jext 300 dans sa pharmacie{NB}? Signalez au pharmacien le **«{NB}stock de "
                          f"dépannage d{AP}urgence en ville{NB}»**."]}),
    # p. 17 (fiche du 3 novembre : ville et hôpital ; diazépam 10 mg sécable disponible) ; p. 19, DCI
    ("fiche", {"nom": f"Diazépam 5{NB}mg", "forme": f"Diazépam Teva 5{NB}mg · contingenté en ville et à l{AP}hôpital",
               "retour": "fin novembre 2026",
               "gestes": [f"Prescrivez **en DCI**{NB}: la fiche de l{AP}ANSM ne vise que la spécialité de Teva. Le "
                          f"pharmacien peut délivrer celle d{AP}un autre laboratoire, si elle est disponible."],
               "note": f"L{AP}ANSM signale le diazépam 10{NB}mg sécable disponible, sans le présenter comme une "
                       f"alternative."}),
    # p. 17 (fiche du 4 novembre : aucune alternative citée) ; p. 19, DCI
    ("fiche", {"nom": "Cotrimoxazole", "forme": f"Cotrimoxazole Teva 800{NB}mg/160{NB}mg · contingenté en ville",
               "retour": "janvier 2027",
               "gestes": [f"Prescrivez **en DCI**{NB}: la fiche ne vise que la spécialité de Teva. Le pharmacien peut "
                          f"délivrer celle d{AP}un autre laboratoire, si elle est disponible."],
               "note": f"La fiche de l{AP}ANSM ne cite aucune alternative."}),
    # p. 18 (fiche du 26 octobre) ; p. 19, DCI et « stock limité de dépannage d'urgence en ville »
    ("fiche", {"nom": f"Nifédipine LP 30{NB}mg", "forme": f"Nifédipine Viatris L.P. 30{NB}mg · contingenté en ville",
               "retour": "début décembre 2026",
               "gestes": [f"Prescrivez **en DCI**, pour que le pharmacien puisse délivrer un autre laboratoire.",
                          f"Signalez-lui le **«{NB}stock limité de dépannage d{AP}urgence en ville{NB}»**."]}),
    # p. 17, CONTEXTE (ANSM, 18 novembre)
    ("fiche", {"nom": f"Furosémide 20 et 40{NB}mg", "forme": "Comprimés",
               "retour": f"pas de date. Les tensions «{NB}devraient durer encore plusieurs mois en 2027{NB}» "
                         f"(ANSM, 18{NB}novembre)",
               "gestes": [f"**Pas besoin de nouvelle ordonnance**{NB}: l{AP}ANSM permet au pharmacien de remplacer "
                          f"les comprimés indisponibles par une **préparation magistrale**."]}),
    # p. 18 (fiche du 17 novembre)
    ("fiche", {"nom": "Zovirax suspension", "forme": f"Aciclovir 200{NB}mg/5{NB}ml, suspension buvable · "
                                                   f"contingenté en ville",
               "retour": "courant janvier 2027",
               "gestes": [f"Selon l{AP}ANSM, **Zovirax 200{NB}mg comprimés reste disponible** pendant la tension "
                          f"de la suspension.",
                          f"Un **stock de dépannage d{AP}urgence en ville** est prévu."]}),
    # p. 18, L'IMPACT (contingentement) ; p. 19, REGARD (ce que demande le Cercle, gardé pour le site)
    ("liste", {"kicker": "Le point pénuries", "titre": f"Contingenté ne veut pas dire *introuvable*",
               "sous_titre": f"Selon le Cercle, la disponibilité peut varier d{AP}une officine et d{AP}une semaine "
                             f"à l{AP}autre.",
               "encadre": f"Ce que le Cercle demande à l{AP}ANSM, et les questions encore ouvertes{NB}: dans le dossier "
                          f"de la revue du 19{NB}novembre (inscription gratuite).",
               "adresse": URL, "pied": "Lien en bio"}),
]

# ------------------------------------------------------------------ Tiers payant et DPC (PDF p. 3 à 5)
# p. 3 : « l'article 32, adopté le 16 novembre, fixe à un an après l'acte le délai pour se faire payer en tiers
# payant, contre 2 ans aujourd'hui selon le rapport de la commission » ; p. 2 : votes non définitifs
TIERS_PAYANT = {"kicker": "Tiers payant · PLFSS 2027", "chiffre": "1 an", "taille_chiffre": 300,
                "legende": f"pour vous faire payer *en tiers payant*, contre 2{NB}ans aujourd{AP}hui",
                "detail": f"Selon le texte voté par le Sénat le 16{NB}novembre (article 32). Le délai court "
                          f"à partir de l{AP}acte.",
                "pied": f"Texte non définitif{NB}: il doit encore passer en commission mixte paritaire. "
                        f"«{NB}2 ans aujourd{AP}hui{NB}»{NB}: selon le rapport de la commission du Sénat."}
# story : la même chose, plus la lecture du Cercle (p. 4, L'IMPACT ; p. 5, REGARD, attribuée)
TIERS_PAYANT_STORY = dict(TIERS_PAYANT, encadre=f"Selon le Cercle, un acte refacturé plus d{AP}un an après sa "
                                                f"réalisation ne serait *plus payé*{NB}: vos rejets sont à traiter "
                                                f"sans attendre.")
# p. 3 : « selon le rapport de la commission, l'article 33, adopté le même jour, supprime l'Agence nationale du DPC et
# l'obligation de DPC pour les professions dotées d'un ordre, soumises à la certification périodique, au plus tard
# fin 2027 » ; p. 4, question ouverte sur le financement de la formation
DPC_STORY = {"kicker": "DPC · PLFSS 2027",
             "titre": f"Fin de l{AP}obligation de *DPC* pour les médecins",
             "texte": f"Votée par le Sénat le 16{NB}novembre (article 33){NB}: selon le rapport de la commission, "
                      f"pour les professions dotées d{AP}un ordre et soumises à la **certification périodique**, "
                      f"**au plus tard fin 2027**. L{AP}Agence nationale du DPC serait supprimée.\n"
                      f"La formation restera-t-elle financée au même niveau{NB}?",
             "sticker": True, "pied": f"Texte non définitif. Le dossier PLFSS{NB}: lien ci-dessus."}

# ------------------------------------------------------------------ Stories du reel taxe lapin (PDF p. 2 à 5)
LAPIN_SONDAGE = {"kicker": "Taxe lapin · PLFSS 2027",
                 "titre": f"Si la loi passe, l{AP}appliqueriez-vous *à vos patients*{NB}?",
                 "texte": f"Le Sénat a voté une pénalité pour les rendez-vous non honorés, **jusqu{AP}au prix de la "
                          f"consultation**, à condition d{AP}avoir informé le patient et de lui avoir rappelé le "
                          f"rendez-vous. Texte non définitif.",
                 "sticker": True}
LAPIN_LIEN = {"kicker": "Taxe lapin · PLFSS 2027",
              "titre": f"Et la pénalité, *qui l{AP}encaisse*{NB}?",
              "texte": f"Le texte voté prévoit un paiement à la caisse d{AP}assurance maladie du patient, sans dire si "
                       f"la somme vous est reversée. Notre analyse et notre recommandation :",
              "sticker": True}


def rendre_fiche(f, num, total):
    lignes = [("ok", g) for g in f["gestes"]]
    s = {"kicker": "Le point pénuries", "titre": f"*{f['nom']}*", "taille_titre": 66, "sous_titre": f["forme"],
         "lignes": [], "glisser": num < total}
    im, y = slide_liste(s, num, total)
    d = ImageDraw.Draw(im)
    larg = W - 2 * MARGE
    # la date de retour, en bandeau
    y += 0
    ht = hauteur(f["retour"], 42, larg - 80, graisse="Bold")
    d.rounded_rectangle([MARGE, y, W - MARGE, y + ht + 92], radius=28, fill=(255, 255, 255))
    d.text((MARGE + 40, y + 26), f"RETOUR ANNONCÉ PAR L{AP}ANSM", font=police(24, "Bold"), fill=(110, 100, 160))
    ecrire(d, MARGE + 40, y + 62, larg - 80, f["retour"], 42, graisse="Bold", couleur=NAVY, accent=NAVY)
    y += ht + 92 + 50
    d.text((MARGE, y), "LE GESTE AU CABINET", font=police(26, "Bold"), fill=ACCENT)
    y += 56
    for marque, texte in lignes:
        hl = hauteur(texte, 40, larg - 100)
        puce(d, MARGE + 30, y + 25, marque)
        ecrire(d, MARGE + 100, y, larg - 100, texte, 40)
        y += hl + 34
    if f.get("note"):
        y += 6
        ecrire(d, MARGE, y, larg, f["note"], 32, couleur=GRIS)
    return im


def serie(nom, slides):
    total = len(slides)
    images = []
    for i, (genre, s) in enumerate(slides, 1):
        if genre == "titre":
            im = slide_titre(s, i, total)
        elif genre == "fiche":
            im = rendre_fiche(s, i, total)
        else:
            if "glisser" not in s:
                s = dict(s, glisser=i < total)
            im, _ = slide_liste(s, i, total)
        f = SORTIE / f"{nom}_{i}.png"
        im.save(f, optimize=True)
        images.append(im)
    planche(nom, images)


def planche(nom, images, cols=4):
    w, h = images[0].size
    k = 0.3
    lignes = (len(images) + cols - 1) // cols
    p = Image.new("RGB", (int(cols * w * k) + (cols + 1) * 16, int(lignes * h * k) + (lignes + 1) * 16), "white")
    for i, im in enumerate(images):
        p.paste(im.resize((int(w * k), int(h * k))), (16 + (i % cols) * (int(w * k) + 16),
                                                     16 + (i // cols) * (int(h * k) + 16)))
    p.save(SORTIE / f"planche_{nom}.png")


if __name__ == "__main__":
    SORTIE.mkdir(exist_ok=True)
    serie("secteur3", SECTEUR3)
    serie("penuries", [(g, s) for g, s in PENURIES])
    autres = {"tiers_payant_4x5": slide_chiffre(TIERS_PAYANT, H_FIL),
              "story_tiers_payant": slide_chiffre(TIERS_PAYANT_STORY, H_STORY),
              "story_dpc": slide_story(DPC_STORY),
              "story_taxe_lapin_sondage": slide_story(LAPIN_SONDAGE),
              "story_taxe_lapin_lien": slide_story(LAPIN_LIEN)}
    for n, im in autres.items():
        im.save(SORTIE / f"{n}.png", optimize=True)
    planche("chiffre_et_stories", list(autres.values())[1:], cols=4)
    autres["tiers_payant_4x5"].resize((540, 675)).save(SORTIE / "planche_tiers_payant.png")
    print("\n".join(sorted(p.name for p in SORTIE.glob("*.png"))))
