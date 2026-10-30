"""28/10/2026 : texte lu final des reels vaccins et cumul, avant la génération des voix (Romain :
« fais un putain de bon script, tu connais mes attentes et la cible, on l'a vu pour le reel arrêts »).

Même ton que le reel arrêts : des faits dits net, une réaction (incrédule, sérieuse) sur ce qui
choque vraiment, jamais sur un chiffre qu'elle gonflerait ; aucune interjection en ouverture.
Chaque phrase garde l'écran : même contenu, même ordre, autant de « | ». Faits du dossier :
- vaccins : arrêté du 8 octobre, l'Assurance Maladie ne rémunère ni la commande, ni le stockage,
  ni les doses perdues (« aucune autre rémunération ») ; délivrance par le pharmacien (décret) ;
- cumul : regard du Cercle, « il fallait donc, en règle générale, déposer sa demande avant cette
  date, alors que le décret qui fixe le seuil n'était toujours pas paru ».

Réécrit les script.json : à relancer après scripts_1022_v3.py ou script_cumul_v3.py, qui remettent
l'ancien texte lu."""
import json
from pathlib import Path

A = Path(__file__).resolve().parent
EP = Path(r"C:\Users\NR SMART\tools\lcdg-reel\episodes")

VACCINS = [
    ("[matter-of-fact] Depuis le onze octobre, vous pouvez stocker au cabinet des vaccins contre la grippe.",
     "[matter-of-fact] Depuis le onze octobre, vous pouvez stocker des vaccins contre la grippe au cabinet."),
    ("[incredulous] Mais ces doses, c’est vous qui les payez d’abord !",
     "[incredulous] Mais ces doses… c’est vous qui les payez d’abord !"),
    ("Onze euros soixante-quinze la dose de Vaxigrip. Plus du double pour Efluelda. | C’est le prix public, "
     "hors honoraire de dispensation.",
     "[matter-of-fact] Onze euros soixante-quinze la dose de Vaxigrip. [surprised] Et plus du double pour "
     "Efluelda, le vaccin hautement dosé ! | Prix public, hors honoraire de dispensation."),
    ("Une fois injectée, l’Assurance Maladie vous la rembourse, avec la majoration S.K.B. ou S.K.C. |",
     "Une fois la dose injectée, l’Assurance Maladie vous la rembourse au prix public : c’est la majoration "
     "S.K.B., ou S.K.C. |"),
    ("Il vous faut aussi une enceinte réfrigérée qui enregistre la température. | Et dès la délivrance, "
     "transport et stockage sont sous votre responsabilité.",
     "Il vous faut aussi une enceinte réfrigérée, qui enregistre la température. | [serious] Et dès que le "
     "pharmacien vous remet les doses, transport et stockage sont sous votre responsabilité."),
    # ni le décret, ni l'arrêté, ni le message de l'Assurance Maladie (qui renvoie à la FAQ du ministère,
    # dont l'article ne dit rien) : la voix nomme les deux textes, plus juste que « aucun texte »
    ("Aucun texte ne dit qui la paie.", "Ni le décret, ni l’arrêté ne disent qui la paie."),
    ("Deux autres questions restent ouvertes. Faut-il le bon de prise en charge du patient ?",
     "[curious] Et deux autres questions restent sans réponse. Faut-il le bon de prise en charge du "
     "patient ?"),
    ("Le vaccin vous est remboursé. Mais la commande et le stock, eux, ne sont pas payés.",
     "[serious] Remboursé, oui. Rémunéré, non : rien pour la commande, rien pour le stock, rien pour les "
     "doses perdues."),
    ("Alors, combien de doses commander, et à quel rythme ?",
     "[curious] Alors, combien de doses commander, et à quel rythme ?"),
]

CUMUL = [
    ("Si elle commence dès deux mille vingt-sept, avant soixante-sept ans, vos revenus pourront réduire "
     "votre pension.",
     "[serious] Si elle commence à partir de deux mille vingt-sept, avant soixante-sept ans, vos revenus "
     "pourront réduire votre pension."),
    ("Avant l’âge légal, vos revenus d’activité seront déduits de la pension dès le premier euro.",
     "Avant l’âge légal, vos revenus d’activité seront déduits de la pension… [incredulous] dès le premier "
     "euro !"),
    ("Au-delà, la pension baisse de la moitié du dépassement : | deux euros gagnés en plus, un euro de pension "
     "en moins.",
     "[emphatic] Au-delà, la pension baisse de la moitié du dépassement. | Deux euros gagnés en plus… un euro "
     "de pension en moins."),
    ("L’exemple de la Carmf : trente-cinq mille euros de pension, soixante mille euros de revenus. La pension "
     "tombe à huit mille cinq cents euros.",
     "L’exemple de la Carmf : trente-cinq mille euros de pension par an, soixante mille euros de revenus. "
     "[incredulous] La pension tombe à huit mille cinq cents euros !"),
    ("À partir de soixante-sept ans, le cumul reste intégral, sans plafond : |",
     "[warm] À partir de soixante-sept ans, le cumul reste intégral, sans plafond : |"),
    ("[serious] Pour garder les anciennes règles, il fallait donc, en général, déposer avant. Sans connaître "
     "le seuil : son décret n’était toujours pas paru.",
     "[serious] Pour garder les anciennes règles, il fallait donc, en règle générale, déposer avant. "
     "[incredulous] Sans même connaître le seuil : son décret n’était toujours pas paru ! [serious] Une "
     "décision prise à l’aveugle."),
    ("Et les zones sous-denses, la permanence des soins, la régulation : seront-elles exclues du calcul ? | "
     "Un décret doit le dire. Rien n’est publié.",
     "[curious] Et les zones sous-denses, la permanence des soins, la régulation : seront-elles exclues du "
     "calcul ? | Un décret doit le dire. [incredulous] Rien n’est publié !"),
    ("Retraite avant soixante-sept ans, en continuant d’exercer ?",
     "[warm] Retraite avant soixante-sept ans, en continuant d’exercer ?"),
]


def appliquer(dossier, paires):
    """Remplace chaque passage dans le champ voix du seul bloc qui le contient (script.json)."""
    p = EP / dossier / "script.json"
    ep = json.loads(p.read_text(encoding="utf-8"))
    for a, b in paires:
        blocs = [bl for bl in ep["blocs"] if a in bl.get("voix", "")]
        assert len(blocs) == 1, (dossier, a[:60], len(blocs))
        bl = blocs[0]
        bl["voix"] = bl["voix"].replace(a, b)
    for k, bl in enumerate(ep["blocs"][1:], 1):
        if bl.get("type") != "chiffre":
            assert bl["voix"].count("|") == (bl.get("texte") or "").count("|"), (dossier, k)
    p.write_text(json.dumps(ep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # le texte lu final reste aussi dans l'atelier, à côté des scripts qui l'ont produit
    (A / f"voix_finale_{dossier[11:]}.json").write_text(
        json.dumps([bl.get("voix", "") for bl in ep["blocs"]], ensure_ascii=False, indent=1), encoding="utf-8")
    lu = " ".join(bl.get("voix", "") for bl in ep["blocs"]).replace("|", "")
    print(f"{dossier} : {len(lu)} caractères lus")


appliquer("2026-10-22-vaccins-cabinet", VACCINS)
appliquer("2026-10-22-cumul-emploi-retraite", CUMUL)
