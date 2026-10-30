"""28/10/2026 : reel vaccins au niveau du reel cumul : les prix en boîtes et étiquettes (au lieu de
barres), les questions ouvertes en cartes dessinées (au lieu de pilules de texte)."""
from pathlib import Path

p = Path(__file__).with_name("scripts_1022_v3.py")
s = p.read_text(encoding="utf-8")
for x, y in [
    ('''     "insert": {"type": "barres", "suffixe": " €", "lignes": [
         {"label": "Vaxigrip", "valeur": 11.75},
         {"label": "Efluelda", "valeur": 23.97}]}},''',
     '''     "insert": {"type": "prix", "pastille": "plus du double", "boites": [
         {"nom": "Vaxigrip", "prix": f"11,75{NB}€"},
         {"nom": "Efluelda", "prix": f"23,97{NB}€", "ton": "rouge"}]}},'''),
    ('''     "insert": {"type": "choix", "lignes": [
         {"label": f"Doses perdues{NB}: qui paie{NB}?", "temps": 0},
         {"label": f"Bon de prise en charge{NB}: obligatoire{NB}?", "temps": 0},
         {"label": f"Enfants de 2 à 17 ans sans comorbidité{NB}?", "temps": 1}]}},''',
     '''     "insert": {"type": "icones", "cartes": [
         {"icone": "poubelle", "label": f"Doses perdues{NB}: qui paie{NB}?", "temps": 0},
         {"icone": "bon", "label": f"Bon de prise en charge obligatoire{NB}?", "temps": 0},
         {"icone": "enfant", "label": f"2 à 17 ans sans comorbidité{NB}?", "temps": 1}]}},'''),
]:
    assert s.count(x) == 1, x[:60]
    s = s.replace(x, y)
p.write_text(s, encoding="utf-8")
print("ok")
