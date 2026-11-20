"""Stories (9:16) et visuel chiffre « 1 an » (4:5) du 19/11/2026, au format des carrousels validé par Romain le 19/11
(« ok parfait, refais les stories et le visuel tiers payant pareil ») : titre en Montserrat ExtraBold, casse normale,
un mot en bleu ; le texte en Montserrat ; une illustration des reels dans le bandeau bleu très pâle du bas.

Stories : le contenu tient entre y 250 et 1560 (barre du haut et champ de réponse d'Instagram). La place du sticker
(sondage ou lien) est laissée vide, sous la flèche, entre le texte et l'illustration.

Textes relus contre le PDF (relecture indépendante du 19/11) : ils reprennent ceux de visuels_1119.py.

    python stories_1119.py            -> lcdg_1119/visuels/*.png (remplace les versions de visuels_1119.py)"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from illustrations import illustration  # noqa: E402
from visuels_1119 import AP, BLANC, BLEU, GRIS, NB, NUIT, PALE, TEXTE, URL, ecrire, police  # noqa: E402
from config import charte as C  # noqa: E402

W = 1080
MARGE = 90
SORTIE = Path(__file__).resolve().parent / "visuels"


def entete(im, d, y, rubrique):
    logo = Image.open(C.LOGO_SRC).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    logo.thumbnail((56, 56))
    im.paste(logo, (MARGE, y), logo)
    d.text((MARGE + logo.width + 16, y + logo.height / 2), f"Le Cercle des Généralistes · {rubrique}",
           font=police(26, "SemiBold"), fill=NUIT, anchor="lm")
    return y + logo.height


def bandeau(im, d, y, bas, ill):
    d.rectangle([0, y, W, bas], fill=PALE)
    larg, haut = W - 2 * MARGE, bas - y - 100
    k = min(larg / ill.width, haut / ill.height, 1.5)
    ill = ill.resize((int(ill.width * k), int(ill.height * k)), Image.LANCZOS)
    im.paste(ill, (int((W - ill.width) / 2), int(y + 50 + (haut - ill.height) / 2)), ill)


def story(s):
    """Rubrique, titre, texte ; la place du sticker sous une flèche ; l'illustration en bas (jusqu'à y 1560)."""
    H = 1920
    im = Image.new("RGB", (W, H), BLANC)
    d = ImageDraw.Draw(im)
    y = entete(im, d, 250, s["rubrique"]) + 60
    y += ecrire(d, MARGE, y, W - 2 * MARGE, s["titre"], 76, graisse="ExtraBold", graisse_forte="ExtraBold",
                couleur=NUIT, accent=BLEU, interligne=1.06)
    y += 36
    y += ecrire(d, MARGE, y, W - 2 * MARGE, s["texte"], 40, graisse="Regular", graisse_forte="Bold", couleur=TEXTE,
                interligne=1.36)
    if s.get("sticker"):
        # la flèche, puis la place du sticker (environ 220 px), laissée vide
        d.text((W / 2, y + 40), "↓", font=police(72, "Bold"), fill=BLEU, anchor="mt")
        y += 40 + 72 + 170
    else:
        y += 60
    if 1640 - y < 340:
        print(f"[!] story « {s['titre'][:30]} » : place de l'illustration trop petite ({1640 - y} px)")
    bandeau(im, d, y, 1640, illustration(s["image"]))
    if s.get("pied"):
        ecrire(d, MARGE, 1670, W - 2 * MARGE, s["pied"], 28, couleur=GRIS, centre=True)
    return im


def chiffre(s, H):
    """Le visuel chiffre : « 1 an » en très grand, sa légende, l'illustration en bas."""
    im = Image.new("RGB", (W, H), BLANC)
    d = ImageDraw.Draw(im)
    haut = 54 if H == 1350 else 250
    y = entete(im, d, haut, s["rubrique"]) + (40 if H == 1350 else 80)
    t = 260
    d.text((MARGE - 8, y), s["chiffre"], font=police(t, "Black"), fill=BLEU)
    y += int(t * 1.08)
    y += ecrire(d, MARGE, y, W - 2 * MARGE, s["legende"], 52, graisse="ExtraBold", graisse_forte="ExtraBold",
                couleur=NUIT, accent=BLEU, interligne=1.1)
    y += 26
    y += ecrire(d, MARGE, y, W - 2 * MARGE, s["detail"], 34, graisse="Regular", graisse_forte="Bold",
                couleur=TEXTE, interligne=1.36)
    if s.get("encadre") and H > 1350:
        y += 36
        y += ecrire(d, MARGE, y, W - 2 * MARGE, s["encadre"], 36, graisse="Regular", graisse_forte="Bold",
                    couleur=TEXTE, interligne=1.36)
    bas = H - 110 if H == 1350 else 1640
    y += 50
    if bas - y < 260:
        print(f"[!] visuel {H} : place de l'illustration trop petite ({bas - y} px)")
    bandeau(im, d, y, bas, illustration(s["image"]))
    d.rectangle([0, bas, W, H], fill=PALE if H == 1350 else BLANC)
    if H == 1350:
        d.text((MARGE, H - 60), s["pied"], font=police(26, "Medium"), fill=GRIS, anchor="lm")
    else:
        ecrire(d, MARGE, 1670, W - 2 * MARGE, s["pied"], 28, couleur=GRIS, centre=True)
    return im


# ------------------------------------------------------------------ Tiers payant (PDF p. 3, 4 et 5)
# p. 3 : « l'article 32, adopté le 16 novembre, fixe à un an après l'acte le délai pour se faire payer en tiers
# payant, contre 2 ans aujourd'hui selon le rapport de la commission » ; p. 2 : votes non définitifs ; p. 5, REGARD
# (attribué) : « un acte refacturé plus d'un an après sa réalisation ne serait plus payé »
TIERS_PAYANT = {
    "rubrique": "Tiers payant", "chiffre": "1 an",
    "legende": f"après l{AP}acte, pour vous faire payer *en tiers payant*",
    "detail": f"Selon le texte voté par le Sénat le 16{NB}novembre (article{NB}32). Contre **2{NB}ans aujourd{AP}hui**, "
              f"selon le rapport de la commission.",
    "encadre": f"Selon le Cercle, un acte refacturé plus d{AP}un an après sa réalisation **ne serait plus payé**{NB}: "
               f"le risque des rejets passe sur le cabinet.",
    "image": {"type": "delai", "titre": "Délai pour vous faire payer", "jours": 365, "temps": 0,
              "fin": f"1 an après l{AP}acte", "temps_fin": 1},
    "pied": f"Texte non définitif · {URL}"}

STORIES = {
    # p. 3 (article 33, selon le rapport de la commission) ; p. 4, question ouverte sur le financement
    "story_dpc": {
        "rubrique": "DPC", "titre": f"Le Sénat vote la fin de l{AP}obligation de *DPC*",
        "texte": f"Selon le rapport de la commission, l{AP}article{NB}33 supprime l{AP}obligation de DPC pour les "
                 f"professions dotées d{AP}un ordre, soumises à la **certification périodique**, **au plus tard "
                 f"fin{NB}2027**. La formation restera-t-elle financée{NB}?",
        "sticker": True,
        "image": [{"type": "rature", "titre": "Vos obligations de formation",
                   "lignes": [{"texte": "Obligation de DPC", "temps": 1}],
                   "pilule": f"Reste{NB}: certification périodique", "temps_pilule": 2}],
        "pied": f"Texte non définitif{NB}: commission mixte paritaire à venir."},
    # p. 2-5 : la pénalité, ses deux conditions, l'exonération ; la question de la revue
    "story_taxe_lapin_sondage": {
        "rubrique": "Taxe lapin", "titre": f"Si la loi passe, l{AP}appliqueriez-vous *à vos patients*{NB}?",
        "texte": f"Pénalité votée par le Sénat{NB}: **jusqu{AP}au prix de la consultation**, si le patient a été "
                 f"informé et a reçu un rappel. Sauf motif impérieux ou de santé. Texte non définitif.",
        "sticker": True,
        "image": {"type": "duel", "cartes": [{"date": "Annoncé en séance", "texte": f"5{NB}€"},
                                             {"date": "Le texte voté", "texte": "Jusqu’au prix de la consultation"}]}},
    # p. 2 et 4 : paiement à la caisse de l'assuré, sans dire si la somme est reversée
    "story_taxe_lapin_lien": {
        "rubrique": "Taxe lapin", "titre": f"Et la pénalité, *qui l{AP}encaisse*{NB}?",
        "texte": f"Le texte voté prévoit un paiement à la caisse d{AP}assurance maladie du patient, sans dire si la "
                 f"somme vous est reversée. Notre analyse et notre recommandation{NB}:",
        "sticker": True,
        "image": {"type": "renvoi", "etapes": [{"label": "Patient"}, {"label": "Sa caisse"},
                                               {"label": "Au médecin ?", "question": True}]}},
}

if __name__ == "__main__":
    SORTIE.mkdir(exist_ok=True)
    images = {"tiers_payant_4x5": chiffre(TIERS_PAYANT, 1350), "story_tiers_payant": chiffre(TIERS_PAYANT, 1920)}
    images.update({n: story(s) for n, s in STORIES.items()})
    for n, im in images.items():
        im.save(SORTIE / f"{n}.png", optimize=True)
    stories = [images[n] for n in ("story_tiers_payant", "story_dpc", "story_taxe_lapin_sondage",
                                   "story_taxe_lapin_lien")]
    k = 0.3
    p = Image.new("RGB", (4 * int(W * k) + 5 * 16, int(1920 * k) + 32), (200, 205, 215))
    for i, im in enumerate(stories):
        p.paste(im.resize((int(W * k), int(1920 * k)), Image.LANCZOS), (16 + i * (int(W * k) + 16), 16))
    p.save(SORTIE / "planche_chiffre_et_stories.png")
    images["tiers_payant_4x5"].resize((540, 675), Image.LANCZOS).save(SORTIE / "planche_tiers_payant.png")
    print(len(images), "images dans", SORTIE)
