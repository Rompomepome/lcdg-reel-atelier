# Atelier des reels LCDG (dépôt privé)

Le moteur des reels du Cercle des Généralistes est dans le dépôt **public** `Rompomepome/lcdg-reel`.
Ce dépôt-ci, **privé**, garde tout le reste : ce qui ne peut pas aller dans un dépôt public, ou qui
n'est que du travail de passage.

- **Les textes payants des articles** et les sources : `sources/` (dossiers LCDG en PDF, revues,
  textes Légifrance et pages ministérielles cités dans les reels), et `lcdg_1022/*.txt`.
- **Les scripts de production** de chaque série de reels : `lcdg_1022/` (reels du 22/10 : arrêts de
  travail, cumul emploi-retraite, vaccins), `lcdg_1028/` (docteurs juniors, accès direct aux IPA),
  et les outils à la racine (`kit_publication.py` fabrique le kit à publier). Les outils devenus
  génériques sont passés dans `lcdg-reel/scripts/` (commit `68fa44e`) : partir de ceux-là.
- **Les relectures Codex** (`codex_review*.log`) et les messages de commit préparés.
- **`sauvegarde/`** : ce que le dépôt public ignore, et qu'on ne peut pas refaire gratuitement.
  - `assets/audio/echo-sax-no4.mp3` (la musique de Romain) et `assets/sfx/` (les bruitages) ;
  - `episodes/<épisode>/voix/` : les voix ElevenLabs déjà payées (cache) ;
  - `episodes/<épisode>/pages/` : les captures des pages officielles montrées à l'écran ;
  - `kit/` : les légendes, couvertures et le LISEZ-MOI du kit `Reels_LCDG_a_publier` (sans les vidéos).
- **`docs/memoire_claude/`** : les règles apprises avec Romain (copie de la mémoire de Claude Code
  du PC de travail, partie LCDG) et `CLAUDE_global.md`, ses consignes pour tous les projets.

Ne sont **pas** ici :
- les vidéos (aperçus, reels rendus, kit) : trop lourdes pour GitHub ;
- les B-roll Pexels (9 Go) : chaque plan choisi est noté, avec son identifiant et son lien Pexels, dans
  `lcdg-reel/episodes/plans_utilises.json` (versionné), donc retrouvable ; pour une copie exacte,
  un disque externe ou un Drive ;
- les anciennes musiques Mixkit : licence sans redistribution, plus utilisées depuis le 21/09/2026 ;
- l'ancien atelier Medadom (`medadom/`) : tout ce qui sert est dans le dépôt privé
  `NRSmart26/medadom-reel`, séparé à la demande de Romain.

## Reprendre sur un autre PC

1. Cloner les deux dépôts côte à côte dans `~/tools/` :
   `git clone https://github.com/Rompomepome/lcdg-reel` et
   `git clone https://github.com/Rompomepome/lcdg-reel-atelier`.
2. Installer `lcdg-reel` selon son README (Python, ffmpeg, `pip install -r requirements.txt`).
3. Créer `lcdg-reel/.env` à partir de `.env.example` : `ELEVENLABS_API_KEY` et `PEXELS_API_KEY`.
   Les clés ne sont dans aucun dépôt : les reprendre sur les comptes ElevenLabs et Pexels.
4. Remettre la sauvegarde à sa place dans `lcdg-reel` :
   - `sauvegarde/assets/*` dans `lcdg-reel/assets/` ;
   - `sauvegarde/episodes/*` dans `lcdg-reel/episodes/` (fusion avec les dossiers existants).
   Sans les voix en cache, un nouveau rendu repaierait la voix.
5. Vérifier : `python scripts/doctor.py`, puis `python scripts/smoke_test.py`.
6. Les B-roll ne sont utiles que pour refaire un reel : un nouveau reel les cherche avec
   `scripts/broll.py` (voir le README de `lcdg-reel`).

Les scripts de `lcdg_1022/` et `lcdg_1028/` écrivent leurs chemins en dur (`C:\Users\NR SMART\...`) :
ils servent de modèles, à adapter. `kit_publication.py` part du dossier personnel (`~/tools/lcdg-reel`,
`~/Downloads/Reels_LCDG_a_publier`).
