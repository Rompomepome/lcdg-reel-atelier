"""Déplace dans config/charte.py les valeurs de mise en page et de rythme écrites en dur dans les
illustrations du 27/10 (review Codex). Les proportions internes d'un dessin restent dans le code."""
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")

c = R / "config" / "charte.py"
s = c.read_text(encoding="utf-8")
CR = [
    ("bulle_pad=20, curseur=17, deplacement=0.9, pause=0.75, ecart=5)",
     "bulle_pad=20, curseur=17, deplacement=0.9, pause=0.75, ecart=5, label_ecart=14,\n"
     "                bulle_ecart=8)"),
    ("jeton=46, jeton_px=20, envol=0.8, envol_pas=0.32, envol_px=26, vague=5)",
     "jeton=46, jeton_px=20, envol=0.8, envol_pas=0.32, envol_px=26, vague=5,\n"
     "                 onde=(1.3, 0.9), envol_dy=60, envol_ecart=16, egal_px=64, egal_y=0.55, jeton_haut=70,\n"
     "                 jeton_vie=1.4)"),
    ("pension=6, cycle=1.05, cycles=2, chute=0.38, envol=0.6, label_px=26, compteur_px=34)",
     "pension=6, cycle=1.05, cycles=2, chute=0.38, envol=0.6, label_px=26, compteur_px=34,\n"
     "                  label_ecart=14, chute_haut=150, envol_dx=90, envol_dy=120, compteur_ecart=10,\n"
     "                  chute_pas=0.55, envol_delai=1.4)"),
    ("petit_px=22, remplissage=1.1, part_duree=0.7, eclat=12, point=10)",
     "petit_px=22, remplissage=1.1, part_duree=0.7, eclat=12, point=10, colonne=36,\n"
     "                pilule_pad=18, centre_dy=6, legende_y=18, legende_pas=1.7, point_ecart=14)"),
    ("pli=0.42, ecart=40, legende_px=27, pilule_px=30, pilule_h=60)",
     "pli=0.42, ecart=40, legende_px=27, pilule_px=30, pilule_h=60, page_rayon=22,\n"
     "                   bas_y=26, page_marge=(28, 26), pilule_pad=24, legende_y=30, pilule_dy=6)"),
    ("ICONES_GEO = dict(ecart=22, icone=118, icone_y=24, label_px=27, badge=48, trait=9, decalage=0.22)",
     "ICONES_GEO = dict(ecart=22, icone=118, icone_y=24, label_px=27, badge=48, trait=9, decalage=0.22,\n"
     "                  label_marge=24, label_ecart=18, badge_pos=0.55)"),
]
for a, b in CR:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
c.write_text(s, encoding="utf-8")

p = R / "lcdg" / "inserts.py"
s = p.read_text(encoding="utf-8")
IR = [
    ('self.ry + rh / 2 + self.px(14)), self.zones[i]["label"]',
     'self.ry + rh / 2 + self.px(g["label_ecart"])), self.zones[i]["label"]'),
    ('self.ry - self.px(g["curseur"]) - self.px(8) - (b.height',
     'self.ry - self.px(g["curseur"]) - self.px(g["bulle_ecart"]) - (b.height'),
    ('(x / self.vw * 1.3 + t * 0.9)', '(x / self.vw * g["onde"][0] + t * g["onde"][1])'),
    ('dy = self.px(60) * T.lisse(w2)', 'dy = self.px(g["envol_dy"]) * T.lisse(w2)'),
    ('ecart = self.vw / 2 + self.px(16)', 'ecart = self.vw / 2 + self.px(g["envol_ecart"])'),
    ('self.fond_y - self.vh * 0.55), "=", self.px(64),',
     'self.fond_y - self.vh * g["egal_y"]), "=", self.px(g["egal_px"]),'),
    ('            if 0 < w2 < 1.4:\n', '            if 0 < w2 < g["jeton_vie"]:\n'),
    ('y0 = self.fond_y - self.vh - self.px(70)', 'y0 = self.fond_y - self.vh - self.px(g["jeton_haut"])'),
    ('min(1.0, (1.4 - w2) * 3))', 'min(1.0, (g["jeton_vie"] - w2) * 3))'),
    ('(cx, self.sol + self.px(14)), lab,', '(cx, self.sol + self.px(g["label_ecart"])), lab,'),
    ('tj = tc + j * g["chute"] * 0.55', 'tj = tc + j * g["chute"] * g["chute_pas"]'),
    ('tp = tc + g["chute"] * 1.4 ', 'tp = tc + g["chute"] * g["envol_delai"] '),
    ('y = y_fin - self.px(150) * (1 - w2 * w2)', 'y = y_fin - self.px(g["chute_haut"]) * (1 - w2 * w2)'),
    ('x = self.cx[1] + self.px(90) * T.lisse(w2)', 'x = self.cx[1] + self.px(g["envol_dx"]) * T.lisse(w2)'),
    ('y = y0 - self.px(120) * T.lisse(w2)', 'y = y0 - self.px(g["envol_dy"]) * T.lisse(w2)'),
    ('(g["pension"] + 1) * self.pas - self.px(10)', '(g["pension"] + 1) * self.pas - self.px(g["compteur_ecart"])'),
    ('(tc + g["chute"] * 1.55, "clic"), (tc + g["chute"] * 1.4, "souffle")',
     '(tc + g["chute"] * (1 + g["chute_pas"]), "clic"),\n'
     '                    (tc + g["chute"] * g["envol_delai"], "souffle")'),
    ('self.xl = self.c[0] + self.r + self.ep / 2 + self.px(36)',
     'self.xl = self.c[0] + self.r + self.ep / 2 + self.px(g["colonne"])'),
    ('self.px(g["pilule_h"]), self.px(18), C.INSERT_VERT, queue=False)',
     'self.px(g["pilule_h"]), self.px(g["pilule_pad"]), C.INSERT_VERT, queue=False)'),
    ('_ecrire(d, (cx, cy - self.px(6)), f"{int(round(self.part',
     '_ecrire(d, (cx, cy - self.px(g["centre_dy"])), f"{int(round(self.part'),
    ('y = cy + self.px(18) + i * lp * 1.7', 'y = cy + self.px(g["legende_y"]) + i * lp * g["legende_pas"]'),
    ('(self.xl + 2 * r + self.px(14), y), texte, lp,', '(self.xl + 2 * r + self.px(g["point_ecart"]), y), texte, lp,'),
    ('        tete = self.px(g["tete"])\n', '        tete, ra = self.px(g["tete"]), self.px(g["page_rayon"])\n'),
    ('radius=self.px(22) * k, fill=C.BLANC + (255,))', 'radius=ra * k, fill=C.BLANC + (255,))'),
    ('(tete + self.px(22)) * k], radius=self.px(22) * k,', '(tete + ra) * k], radius=ra * k,'),
    ('dd.rectangle([0, tete * k, w * k - 1, (tete + self.px(22)) * k]', 'dd.rectangle([0, tete * k, w * k - 1, (tete + ra) * k]'),
    ('_ecrire(d, (w / 2, h - self.px(26)), p.get("bas", "")', '_ecrire(d, (w / 2, h - self.px(g["bas_y"])), p.get("bas", "")'),
    ('self.px_x = self.m + self.px(28)', 'self.px_x = self.m + self.px(g["page_marge"][0])'),
    ('self.py = self.m + self.h - self.pages[0].height - self.px(26)',
     'self.py = self.m + self.h - self.pages[0].height - self.px(g["page_marge"][1])'),
    ('self.px(24), C.INSERT_ROUGE, queue=False)', 'self.px(g["pilule_pad"]), C.INSERT_ROUGE, queue=False)'),
    ('(self.xl, self.py + self.px(30) + j * lp * 1.2), l, lp,', '(self.xl, self.py + self.px(g["legende_y"]) + j * lp * 1.2), l, lp,'),
    ('self.px(g["pilule_h"]) / 2 - self.px(6), kk,', 'self.px(g["pilule_h"]) / 2 - self.px(g["pilule_dy"]), kk,'),
    ('self.cw - self.px(24))', 'self.cw - self.px(g["label_marge"]))'),
    ('ic.height + self.px(18)', 'ic.height + self.px(g["label_ecart"])'),
    ('self.cw / 2 - self.px(g["badge"]) * 0.55,', 'self.cw / 2 - self.px(g["badge"]) * g["badge_pos"],'),
    ('self.m + self.px(g["badge"]) * 0.55 + dy', 'self.m + self.px(g["badge"]) * g["badge_pos"] + dy'),
]
for a, b in IR:
    assert s.count(a) == 1, (s.count(a), a)
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
print("ok")
