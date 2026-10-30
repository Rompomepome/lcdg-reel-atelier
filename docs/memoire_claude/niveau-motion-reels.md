---
name: niveau-motion-reels
description: "Tout nouveau reel LCDG doit atteindre le niveau de design et de motion du reel « arrêts de travail » (23/10/2026) — illustrations animées sur presque chaque plan, accroche percutante, wording limpide"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c52333eb-2092-4068-8d6a-41bf40843acc
  modified: 2026-10-27T16:26:36.706Z
---

Le reel « arrêts de travail : mise sous objectifs et SOS IJ » (publié le 27/10/2026) est la
référence de qualité : « toutes les améliorations qu'on a faites en termes de design et de
motion ultra poussée sur le reel des arrêts de travail, il faut que ce soit aussi poussé que ça
sur les prochains reels » (Romain, 27/10/2026, « garde-le en mémoire !! »).

**Why:** Romain veut des reels « interactifs et ultra ludiques », qui informent et donnent envie
de lire la suite sur le site, assez percutants pour la publicité.

**How to apply:** pour chaque nouveau reel, sans attendre qu'il le demande :
- les 2 premières secondes portent le conflit ou le chiffre fort (la pub démarre au bloc 1) ;
- une illustration animée (lcdg/inserts.py) sur presque chaque bloc de texte : schémas
  (circuit, duel, frise, barres, choix « ? ») et illustrations dessinées (frigo, ticket,
  appel, loupe, calcul, tampon posé « sur » un dessin) ; en créer une nouvelle quand le sujet
  le demande, dessinée en suréchantillonnage, essayée avec proto_inserts.py ;
- un ton cinglant et juste, tiré du regard du Cercle, et des phrases limpides (voir
  [[wording-oral]]) ; 3 lignes au plus par temps (lignes_textes.py) ;
- une version publicité d'environ 35 à 40 s découpée dans la même narration (pub_1022.py), avec
  ses textes Meta ; éviter le vocabulaire réglementaire dans la pastille de la pub (refus Meta
  des publicités jugées politiques en Europe) ;
- un aperçu sans voix pour validation avant de générer la voix.
Voir [[format-reel-v2]] et [[reel-porte-entree]].
