"""Kit de publication des 4 reels (05/10/2026) : un dossier par reel, dans l'ordre conseille,
avec les videos, les couvertures et les legendes pretes a copier (texte brut)."""
import re
import shutil
from pathlib import Path

# dossier personnel plutot que C:\Users\NR SMART : marche aussi sur un autre PC (voir README)
E = Path.home() / "tools" / "lcdg-reel" / "episodes"
KIT = Path.home() / "Downloads" / "Reels_LCDG_a_publier"
REELS = [  # ordre de publication conseille : (dossier, episode, slug, titre, mot cle, quand)
    ("1_Fluoxetine", "2026-09-30-fluoxetine", "fluoxetine", "1. FLUOXÉTINE 20 MG", "FLUOX",
     "avant la mi-octobre : le reel parle d’une situation prévue jusqu’à cette date."),
    ("2_Franchises", "2026-09-21-franchises-medicales", "franchises", "2. FRANCHISES MÉDICALES", "140",
     "en vigueur depuis le 1er octobre : à publier vite."),
    ("3_Desogestrel", "2026-09-21-desogestrel", "desogestrel", "3. DÉSOGESTREL ET MÉNINGIOME", "DESO",
     "les courriers de l’ANSM sont partis en septembre : à publier sans tarder."),
    ("4_Protections_periodiques", "2026-09-30-protections-periodiques", "protections-periodiques",
     "4. PROTECTIONS PÉRIODIQUES", "60",
     "seulement après la mise à jour de l’article sur le site (voir « À faire »)."),
    ("5_Grippe_Covid", "2026-10-06-grippe-covid", "grippe-covid", "5. GRIPPE ET COVID-19", "GRIPPE",
     "en premier, avant le 13 octobre, jour où la campagne démarre."),
    ("6_PLFSS_2027", "2026-10-06-plfss-2027", "plfss-2027", "6. PLFSS 2027", "PLFSS",
     "pendant l’examen du texte au Parlement."),
    ("7_Minimum_patients", "2026-10-13-minimum-patients", "minimum-patients",
     "7. MINIMUM DE PATIENTS MÉDECIN TRAITANT", "500",
     "semaine du 19 octobre, puis en publicité (textes de la publicité dans legende_publicite_meta.txt)."),
    # depuis le 22/10/2026, plus de mot cle a commenter : le bandeau renvoie au site
    ("8_Arrets_de_travail_MSO", "2026-10-22-arrets-travail-mso", "arrets-travail-mso",
     "8. ARRÊTS DE TRAVAIL : MISE SOUS OBJECTIFS ET SOS IJ", None,
     "dès que l’article est en ligne : les courriers des caisses partent « prochainement ». "
     "Puis en publicité (textes dans legende_publicite_meta.txt)."),
    ("9_Vaccins_au_cabinet", "2026-10-22-vaccins-cabinet", "vaccins-cabinet",
     "9. VACCINS GRIPPE ET COVID-19 AU CABINET", None,
     "dès que possible : la campagne contre la grippe court jusqu’au 31 janvier 2027. "
     "Puis en publicité (textes dans legende_publicite_meta.txt)."),
    ("10_Cumul_emploi_retraite", "2026-10-22-cumul-emploi-retraite", "cumul-emploi-retraite",
     "10. CUMUL EMPLOI-RETRAITE 2027", None,
     "dès que possible : le décret qui fixe le seuil est attendu avant la fin de 2026. "
     "Puis en publicité (textes dans legende_publicite_meta.txt)."),
    ("11_Docteurs_juniors", "2026-10-28-docteurs-juniors", "docteurs-juniors",
     "11. DOCTEURS JUNIORS : LA 4E ANNÉE ARRIVE LE 2 NOVEMBRE", None,
     "en premier, avant le 2 novembre, jour où les docteurs juniors arrivent. "
     "Puis en publicité (textes dans legende_publicite_meta.txt)."),
    ("12_Acces_direct_IPA", "2026-10-28-acces-direct-ipa", "acces-direct-ipa",
     "12. ACCÈS DIRECT AUX IPA EN CPTS", None,
     "avant le 1er décembre, début de l’expérimentation. "
     "Puis en publicité (textes dans legende_publicite_meta.txt)."),
    # 13 (soins chez le pharmacien) abandonne le 06/11/2026 : « aucune vraie valeur ajoutee » (Romain)
    ("14_Cotisation_Ordre_en_societe", "2026-11-04-cotisation-ordre", "cotisation-ordre",
     "14. COTISATION À L’ORDRE EN SOCIÉTÉ", None,
     "tant que le Conseil d’État n’a pas jugé le recours de la CSMF. "
     "Puis en publicité : version d’environ 30 s (textes dans legende_publicite_meta.txt)."),
    ("15_Premieres_installations", "2026-11-04-premieres-installations", "premieres-installations",
     "15. PREMIÈRES INSTALLATIONS : +22,8 %", None,
     "dès que possible : les chiffres datent du 22 octobre. "
     "Puis en publicité : version d’environ 30 s (textes dans legende_publicite_meta.txt)."),
    # reels du 13/11/2026 : articles du 10/11, pas encore en ligne le 13/11 (liens a completer)
    ("16_Maladie_pro_tableau_57", "2026-11-10-maladie-pro-tableau-57", "maladie-pro-tableau-57",
     "16. MALADIE PROFESSIONNELLE : L’IRM DE L’ÉPAULE ET LE TABLEAU 57", None,
     "dès que l’article est en ligne, tant que la liste d’examens d’ameli indique encore l’IRM. "
     "Puis en publicité : version d’environ 45 s (textes dans legende_publicite_meta.txt)."),
    ("17_TDAH_Xurta_Tentin", "2026-11-10-tdah-xurta-tentin", "tdah-xurta-tentin",
     "17. TDAH : XURTA ET TENTIN REMBOURSÉS, SOUS FORMULAIRE", None,
     "dès que l’article est en ligne : l’Assurance Maladie peut préciser le cas des patients déjà traités. "
     "Puis en publicité : version d’environ 45 s (textes dans legende_publicite_meta.txt)."),
]
# version publicite d'un reel (episode a part, monte depuis la meme narration)
PUB = {"7_Minimum_patients": ("2026-10-13-minimum-patients-pub", "minimum-patients-pub"),
       "8_Arrets_de_travail_MSO": ("2026-10-22-arrets-travail-mso-pub", "arrets-travail-mso-pub"),
       "9_Vaccins_au_cabinet": ("2026-10-22-vaccins-cabinet-pub", "vaccins-cabinet-pub"),
       "10_Cumul_emploi_retraite": ("2026-10-22-cumul-emploi-retraite-pub", "cumul-emploi-retraite-pub"),
       "11_Docteurs_juniors": ("2026-10-28-docteurs-juniors-pub", "docteurs-juniors-pub"),
       "12_Acces_direct_IPA": ("2026-10-28-acces-direct-ipa-pub", "acces-direct-ipa-pub"),
       # reels 14 et 15 refaits le 06/11/2026 en phrases construites (environ 1 min 55) ; publicites
       # d'environ 30 s decoupees dans la nouvelle narration (Romain : « les versions pub je veux bien »)
       "14_Cotisation_Ordre_en_societe": ("2026-11-04-cotisation-ordre-pub", "cotisation-ordre-pub"),
       "15_Premieres_installations": ("2026-11-04-premieres-installations-pub", "premieres-installations-pub"),
       "16_Maladie_pro_tableau_57": ("2026-11-10-maladie-pro-tableau-57-pub", "maladie-pro-tableau-57-pub"),
       "17_TDAH_Xurta_Tentin": ("2026-11-10-tdah-xurta-tentin-pub", "tdah-xurta-tentin-pub")}
# rappels deja donnes pour tous les reels : on ne les repete pas reel par reel
COMMUNS = ("- étiquette « Info IA »", "- réponse en message privé")


def sections(md):
    """(a faire, instagram, linkedin, lien de bio, publicite ou None) d'un legendes.md."""
    a_faire = re.search(r"avant de publier :\n(.*?)\n\n## ", md, re.S).group(1).strip()
    insta = re.search(r"## Instagram[^\n]*\n(.*?)\n## ", md, re.S).group(1).strip()
    # jusqu'a la section suivante : la publicite Meta, quand il y en a une, vient juste apres
    linkedin = re.search(r"## LinkedIn[^\n]*\n(.*?)\n## ", md, re.S).group(1).strip()
    bio = re.search(r"## Lien de la bio[^\n]*\n(.*)", md, re.S).group(1).strip()
    pub = re.search(r"## Publicité[^\n]*\n(.*?)\n## ", md, re.S)
    return a_faire, insta, linkedin, bio, pub.group(1).strip() if pub else None


def propres(a_faire):
    """Les points propres a ce reel (un point peut tenir sur plusieurs lignes)."""
    points, courant = [], []
    for ligne in a_faire.splitlines():
        if ligne.startswith("- ") and courant:
            points.append(courant); courant = []
        courant.append(ligne)
    if courant:
        points.append(courant)
    return ["\n".join(p) for p in points if not p[0].startswith(COMMUNS)]


# on ne vide que ce que ce script produit : les autres fichiers du dossier (le prompt de
# correction des articles) sont conserves
KIT.mkdir(parents=True, exist_ok=True)
# reels abandonnes : leur dossier sort du kit, pour qu'on ne les publie pas par erreur
ABANDONNES = ("13_Soins_chez_le_pharmacien",)   # 06/11/2026, Romain : « supprime le dossier 13 »
for dossier in [d for d, *_ in REELS] + list(ABANDONNES):
    if (KIT / dossier).exists():
        shutil.rmtree(KIT / dossier)
lisez = ["REELS LCDG À PUBLIER",
         "====================",
         "",
         "Ordre de publication conseillé (mis à jour le 13/11/2026) : les nouveaux reels 16 (maladie",
         "professionnelle, tableau 57) et 17 (TDAH, Xurta et Tentin), dès que leurs articles sont en",
         "ligne : leurs liens sont à compléter (voir « À faire »). Puis 14 (cotisation à l’Ordre en",
         "société) et 15 (premières installations), refaits le 06/11 en phrases complètes, avec",
         "l’accroche dès la première seconde. Le 13 (soins chez le pharmacien) est abandonné.",
         "Ceux qui restent de la série précédente : 9 et 10 (vaccins, cumul",
         "emploi-retraite) et 12 (accès direct aux IPA, avant le 1er décembre). Les reels 1 à 8 sont publiés.",
         "Grippe (5) et fluoxétine (1) : leur date conseillée est passée (13 octobre, mi-octobre).",
         "S’ils ne sont pas encore en ligne, les faire revoir avant de les publier.",
         "",
         "Un dossier par reel. Dans chaque dossier :",
         "- reel_9x16_instagram_facebook.mp4 : le reel pour Instagram et Facebook ;",
         "- couverture_9x16_instagram_facebook.jpg : à choisir comme couverture du reel",
         "  (Instagram : « Modifier la couverture », puis « Ajouter depuis la pellicule ») ;",
         "- couverture_4x5.jpg : la même, recadrée pour le fil et la grille du profil, si la",
         "  plateforme te demande une image 4:5 ;",
         "- reel_1x1_linkedin.mp4 et couverture_1x1_linkedin.jpg : la vidéo LinkedIn et sa",
         "  miniature ;",
         "- legende_instagram_facebook.txt et legende_linkedin.txt : les textes à copier-coller ;",
         "- reels 7 à 17 : publicite_9x16.mp4 et publicite_1x1.mp4, la version courte pour la",
         "  publicité, et legende_publicite_meta.txt, ses textes dans le gestionnaire de publicités Meta.",
         "",
         "À la racine du dossier : PROMPT_correction_articles.md, le prompt à coller dans Claude pour",
         "corriger les articles du site (mode d’emploi en tête du fichier).",
         "",
         "Pour tous les reels :",
         "- activer l’étiquette « Info IA » sur Instagram et Facebook (voix de synthèse) ;",
         "- le jour de la publication, mettre le lien de l’article dans la bio Instagram (lien",
         "  ci-dessous, il porte le suivi « instagram ») ;",
         "- reels 1 à 7 : répondre en message privé, avec le lien de l’article, à ceux qui commentent",
         "  le mot clé. Depuis le reel 8, plus de mot clé : le bandeau renvoie au site.",
         ""]
for dossier, ep, slug, titre, mot, quand in REELS:
    src = E / ep / "final"
    dst = KIT / dossier
    dst.mkdir()
    for a, b in ((f"reel_{slug}_9x16.mp4", "reel_9x16_instagram_facebook.mp4"),
                 (f"reel_{slug}_1x1.mp4", "reel_1x1_linkedin.mp4"),
                 (f"couverture_{slug}_9x16.jpg", "couverture_9x16_instagram_facebook.jpg"),
                 (f"couverture_{slug}_4x5.jpg", "couverture_4x5.jpg"),
                 (f"couverture_{slug}_1x1.jpg", "couverture_1x1_linkedin.jpg")):
        shutil.copyfile(src / a, dst / b)
    if dossier in PUB:
        ep_pub, slug_pub = PUB[dossier]
        for a, b in ((f"reel_{slug_pub}_9x16.mp4", "publicite_9x16.mp4"),
                     (f"reel_{slug_pub}_1x1.mp4", "publicite_1x1.mp4")):
            shutil.copyfile(E / ep_pub / "final" / a, dst / b)
    a_faire, insta, linkedin, bio, pub = sections((E / ep / "legendes.md").read_text(encoding="utf-8"))
    (dst / "legende_instagram_facebook.txt").write_text(insta + "\n", encoding="utf-8")
    (dst / "legende_linkedin.txt").write_text(linkedin + "\n", encoding="utf-8")
    if pub:
        (dst / "legende_publicite_meta.txt").write_text(pub + "\n", encoding="utf-8")
    lisez += [titre, "-" * len(titre), f"Quand : {quand}"]
    if mot:
        lisez.append(f"Mot clé à commenter : {mot}")
    lisez.append(f"Lien de la bio Instagram : {bio}")
    points = propres(a_faire)
    if points:
        lisez += ["À faire :"] + points
    lisez.append("")
(KIT / "LISEZ-MOI.txt").write_text("\n".join(lisez) + "\n", encoding="utf-8")
for f in sorted(KIT.rglob("*")):
    if f.is_file():
        print(f"{f.stat().st_size // 1024:>7} Ko  {f.relative_to(KIT)}")
