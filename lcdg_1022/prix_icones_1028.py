"""28/10/2026 : illustration « prix » (boîtes de vaccin et étiquettes) et icônes poubelle, bon,
enfant, pour le reel vaccins ; une carte d'icônes peut porter son propre "temps"."""
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")

c = R / "config" / "charte.py"
s = c.read_text(encoding="utf-8")
a = "ICONES_H = 300\n"
assert s.count(a) == 1
s = s.replace(a, """PRIX_H = 330
PRIX_GEO = dict(boite=(250, 196), bande=56, rayon=16, nom_px=30, trait=3, sol=8, etiquette_px=40,
                etiquette_pad=(24, 14), etiquette_x=0.3, etiquette_y=12, etiquette_angle=-10, chute=0.45,
                chute_haut=120, decalage=1.4, balance=(9, 1.6, 3.0), pastille_px=26, pastille_h=52,
                pastille_pad=20, pastille_dy=44, pastille_delai=0.3)
ICONES_H = 300
""")
c.write_text(s, encoding="utf-8")

p = R / "lcdg" / "inserts.py"
s = p.read_text(encoding="utf-8")
R2 = [
    # l'etiquette de prix devient une fonction partagee (refrigerateur, boites de vaccin)
    ('''# -------------------------------------------------------------- frigo
class Frigo(_Insert):''',
     '''def _etiquette(lignes, px, padx, pady, couleur=C.INSERT_ROUGE):
    """Etiquette de prix (pointe et trou a gauche), texte blanc ; ni rotation ni ombre."""
    lignes = [T.normaliser(l) for l in lignes]
    lh = px * 1.18
    h = len(lignes) * lh + 2 * pady
    pointe = h * 0.42
    w = max(T.largeur(l, px, C.INSERT_GRAISSE_FORTE, 0) for l in lignes) + 2 * padx + pointe

    def dessin(d, k):
        W, H, P = w * k, h * k, pointe * k
        fond = tuple(couleur) + (255,)
        d.rounded_rectangle([P * 0.6, 0, W, H], radius=H * 0.16, fill=fond)
        d.polygon([(P + 1, 0), (0, H / 2), (P + 1, H)], fill=fond)
        r = H * 0.085
        d.ellipse([P * 0.5 - r, H / 2 - r, P * 0.5 + r, H / 2 + r], fill=(0, 0, 0, 0))
    im = _net(w, h, dessin)
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lignes):
        _ecrire(d, (pointe + (w - pointe) / 2, pady + lh * (i + 0.5)), l, px, C.INSERT_GRAISSE_FORTE,
                C.BLANC + (255,), "mm")
    return im


# -------------------------------------------------------------- frigo
class Frigo(_Insert):'''),
    ('''        """L'etiquette de prix, deja tournee (sans ombre)."""
        g = C.FRIGO_GEO
        px = max(8, int(round(g["etiquette_px"] * s)))
        lignes = [T.normaliser(l) for l in self.spec.get("etiquette", [])]
        lh = px * 1.18
        padx, pady = g["etiquette_pad"][0] * s, g["etiquette_pad"][1] * s
        h = len(lignes) * lh + 2 * pady
        pointe = h * 0.42
        w = max(T.largeur(l, px, C.INSERT_GRAISSE_FORTE, 0) for l in lignes) + 2 * padx + pointe

        def dessin(d, k):
            W, H, P = w * k, h * k, pointe * k
            rouge = C.INSERT_ROUGE + (255,)
            d.rounded_rectangle([P * 0.6, 0, W, H], radius=H * 0.16, fill=rouge)
            d.polygon([(P + 1, 0), (0, H / 2), (P + 1, H)], fill=rouge)
            r = H * 0.085
            d.ellipse([P * 0.5 - r, H / 2 - r, P * 0.5 + r, H / 2 + r], fill=(0, 0, 0, 0))
        im = _net(w, h, dessin)
        d = ImageDraw.Draw(im)
        for i, l in enumerate(lignes):
            _ecrire(d, (pointe + (w - pointe) / 2, pady + lh * (i + 0.5)), l, px, C.INSERT_GRAISSE_FORTE,
                    C.BLANC + (255,), "mm")
        return im.rotate(-g["etiquette_angle"], resample=Image.BICUBIC, expand=True)''',
     '''        """L'etiquette de prix, deja tournee (sans ombre)."""
        g = C.FRIGO_GEO
        im = _etiquette(self.spec.get("etiquette", []), max(8, int(round(g["etiquette_px"] * s))),
                        g["etiquette_pad"][0] * s, g["etiquette_pad"][1] * s)
        return im.rotate(-g["etiquette_angle"], resample=Image.BICUBIC, expand=True)'''),
    # icones : poubelle, bon, enfant ; le casque devient explicite
    ('''            else:                                         # le casque de la regulation''',
     '''            elif nom == "poubelle":                       # une dose perdue : poubelle et piece
                dd.rounded_rectangle([S * 0.38, S * 0.1, S * 0.62, S * 0.2], radius=S * 0.03, fill=navy)
                dd.rounded_rectangle([S * 0.12, S * 0.18, S * 0.78, S * 0.27], radius=S * 0.03, fill=navy)
                dd.polygon([(S * 0.18, S * 0.3), (S * 0.72, S * 0.3), (S * 0.65, S * 0.96), (S * 0.25, S * 0.96)],
                           fill=navy)
                for x in (0.34, 0.45, 0.56):
                    dd.line([(S * x, S * 0.42), (S * x, S * 0.84)], fill=C.BLANC + (255,), width=int(e * 0.55))
                r = S * 0.17
                dd.ellipse([S * 0.82 - r, S * 0.2 - r, S * 0.82 + r, S * 0.2 + r], fill=C.INSERT_ROUGE + (255,))
            elif nom == "bon":                            # le bon de prise en charge : un formulaire
                pli = S * 0.2
                dd.polygon([(S * 0.18, S * 0.05), (S * 0.82 - pli, S * 0.05), (S * 0.82, S * 0.05 + pli),
                            (S * 0.82, S * 0.96), (S * 0.18, S * 0.96)], fill=C.BLANC + (255,), outline=navy,
                           width=int(e * 0.6))
                dd.polygon([(S * 0.82 - pli, S * 0.05), (S * 0.82 - pli, S * 0.05 + pli), (S * 0.82, S * 0.05 + pli)],
                           fill=gris)
                dd.rounded_rectangle([S * 0.3, S * 0.3, S * 0.62, S * 0.38], radius=S * 0.02, fill=rub)
                for y in (0.5, 0.62, 0.74):
                    dd.rounded_rectangle([S * 0.3, S * y, S * 0.7, S * (y + 0.05)], radius=S * 0.02, fill=gris)
            elif nom == "enfant":                         # un enfant
                cx, r = S / 2, S * 0.15
                dd.ellipse([cx - r, S * 0.06, cx + r, S * 0.06 + 2 * r], fill=navy)
                dd.line([(cx - S * 0.15, S * 0.48), (cx - S * 0.3, S * 0.66)], fill=rub, width=int(e))
                dd.line([(cx + S * 0.15, S * 0.48), (cx + S * 0.3, S * 0.66)], fill=rub, width=int(e))
                dd.rounded_rectangle([cx - S * 0.17, S * 0.4, cx + S * 0.17, S * 0.74], radius=S * 0.08, fill=rub)
                dd.rounded_rectangle([cx - S * 0.13, S * 0.68, cx - S * 0.03, S * 0.96], radius=S * 0.04, fill=navy)
                dd.rounded_rectangle([cx + S * 0.03, S * 0.68, cx + S * 0.13, S * 0.96], radius=S * 0.04, fill=navy)
            else:                                         # le casque de la regulation'''),
    ('''        return _net(s, s, dessin)

    def _carte(self, c):''',
     '''        im = _net(s, s, dessin)
        if nom == "poubelle":                             # la piece porte « € »
            _ecrire(ImageDraw.Draw(im), (s * 0.82, s * 0.2), "€", max(6, int(s * 0.2)), C.INSERT_GRAISSE_FORTE,
                    C.BLANC + (255,), "mm")
        return im

    def _carte(self, c):'''),
    ('''    def _t(self, i):
        return self.t0(self.spec.get("temps", 0)) + i * C.ICONES_GEO["decalage"]''',
     '''    def _t(self, i):
        """Une carte arrive avec le temps du texte de son "temps" (celui de l'insert par defaut)."""
        defaut = self.spec.get("temps", 0)
        tps = self.items[i].get("temps", defaut)
        avant = [j for j in range(i) if self.items[j].get("temps", defaut) == tps]
        return self.t0(tps) + len(avant) * C.ICONES_GEO["decalage"]'''),
    # illustration « prix »
    ('''TYPES = {"verrou": Verrou,''',
     '''# ---------------------------------------------------------------- prix
class Prix(_Insert):
    """Des boites de vaccin dessinees ; une etiquette de prix tombe sur chacune, au temps de sa
    boite, se balance, puis une pastille (« plus du double ») claque au-dessus de la derniere."""

    def taille_nominale(self):
        return C.TEXTE_LARGEUR, C.PRIX_H

    def __init__(self, *a):
        super().__init__(*a)
        g = C.PRIX_GEO
        self.items = self.spec["boites"]
        n = len(self.items)
        self.boites = [_ombre_marge(self._boite(b["nom"]), self.s) for b in self.items]
        self.etiquettes = [_ombre_marge(_etiquette([b["prix"]], self.px(g["etiquette_px"]),
                                                   self.px(g["etiquette_pad"][0]), self.px(g["etiquette_pad"][1]),
                                                   _ton(b, self.rubrique)), self.s) for b in self.items]
        self.pastille = (_ombre_marge(_bulle(self.spec["pastille"], self.px(g["pastille_px"]), self.px(g["pastille_h"]),
                                             self.px(g["pastille_pad"]), C.INSERT_ROUGE, queue=False), self.s)
                         if self.spec.get("pastille") else None)
        self.cx = [self.m + self.w * (i + 0.5) / n for i in range(n)]
        self.bw, self.bh = self.px(g["boite"][0]), self.px(g["boite"][1])
        self.haut = self.m + self.h - self.px(g["sol"]) - self.bh            # haut des boites

    def _boite(self, nom):
        g = C.PRIX_GEO
        w, h, bande = self.px(g["boite"][0]), self.px(g["boite"][1]), self.px(g["bande"])
        ra, tr = self.px(g["rayon"]), max(1, self.px(g["trait"]))
        rub, navy = tuple(self.rubrique) + (255,), C.NAVY + (255,)

        def dessin(d, k):
            W, H, B, Q = w * k, h * k, bande * k, ra * k
            d.rounded_rectangle([0, 0, W - 1, H - 1], radius=Q, fill=C.BLANC + (255,))
            d.rounded_rectangle([0, 0, W - 1, B + Q], radius=Q, fill=rub)
            d.rectangle([0, B, W - 1, B + Q], fill=C.BLANC + (255,))
            cx, cy = W * 0.5, B + (H - B) * 0.55                # une seringue preremplie
            L, e = W * 0.42, (H - B) * 0.2
            d.rounded_rectangle([cx - L / 2, cy - e / 2, cx + L / 2, cy + e / 2], radius=e * 0.3,
                                fill=_teinte(self.rubrique, 0.75) + (255,), outline=navy, width=int(tr * k))
            d.rectangle([cx - L / 2 - L * 0.24, cy - e * 0.12, cx - L / 2, cy + e * 0.12], fill=navy)
            d.rectangle([cx - L / 2 - L * 0.28, cy - e * 0.55, cx - L / 2 - L * 0.22, cy + e * 0.55], fill=navy)
            d.rectangle([cx + L / 2, cy - e * 0.08, cx + L / 2 + L * 0.3, cy + e * 0.08], fill=navy)
            for i in range(1, 5):
                x = cx - L / 2 + L * i / 5
                d.line([(x, cy - e / 2), (x, cy - e * 0.05)], fill=navy, width=int(tr * k))
        im = _net(w, h, dessin)
        _ecrire(ImageDraw.Draw(im), (w / 2, bande / 2), nom, self.px(g["nom_px"]), C.INSERT_GRAISSE_FORTE,
                C.BLANC + (255,), "mm")
        return im

    def _t(self, i):
        g = C.PRIX_GEO
        defaut = self.spec.get("temps", 0)
        tps = self.items[i].get("temps", defaut)
        avant = [j for j in range(i) if self.items[j].get("temps", defaut) == tps]
        return self.t0(tps) + C.INSERT_ENTREE * 0.5 + len(avant) * g["decalage"]

    def _t_pastille(self):
        g = C.PRIX_GEO
        return max(self._t(i) for i in range(len(self.items))) + g["chute"] + g["pastille_delai"]

    def image(self, t, final):
        g = C.PRIX_GEO
        out = Image.new("RGBA", (self.w + 2 * self.m, self.h + 2 * self.m), (0, 0, 0, 0))
        for i, boite in enumerate(self.boites):
            k, a = _entree(t, self.t0() + i * C.INSERT_DECALAGE, final)
            if a <= 0:
                continue
            _poser(out, boite, self.cx[i], self.haut + self.bh / 2, k, a)
            u = 1.0 if final else (t - self._t(i)) / g["chute"]
            if u <= 0:
                continue
            dy = 0.0 if u >= 1 else -self.px(g["chute_haut"]) * (1 - u * u)
            angle = g["etiquette_angle"]
            if not final and u >= 1:                      # elle se balance, puis se pose
                amp, freq, amorti = g["balance"]
                tau = t - self._t(i) - g["chute"]
                angle += amp * math.sin(2 * math.pi * freq * tau) * math.exp(-amorti * tau)
            ex = self.cx[i] + self.bw * g["etiquette_x"]
            _poser(out, self.etiquettes[i], ex, self.haut + self.px(g["etiquette_y"]) + dy, 1.0,
                   1.0 if final else min(1.0, u * 3), angle)
        if self.pastille is not None:
            v = 1.0 if final else (t - self._t_pastille()) / C.TAMPON_FRAPPE
            if v > 0:
                kk = 1.0 if final or v >= 1 else C.TAMPON_ECHELLE - (C.TAMPON_ECHELLE - 1) * v * v
                _poser(out, self.pastille, self.cx[-1] - self.bw * 0.1, self.haut - self.px(g["pastille_dy"]), kk,
                       1.0 if final else min(1.0, v * 2), 4)
        return out

    def sons(self):
        g = C.PRIX_GEO
        out = [(self._t(i) + g["chute"], "clic") for i in range(len(self.items))]
        if self.pastille is not None:
            out.append((self._t_pastille() + C.TAMPON_FRAPPE, "impact"))
        return out


TYPES = {"verrou": Verrou,'''),
    ('''         "vases": Vases, "pieces": Pieces, "part": Part, "bascule": Bascule, "icones": Icones}''',
     '''         "vases": Vases, "pieces": Pieces, "part": Part, "bascule": Bascule, "icones": Icones,
         "prix": Prix}'''),
    ('''  {"type": "icones", "cartes": [{"icone": "repere" | "lune" | "casque", "label": "..."}, ...]}
      des cartes a icone dessinee, un « ? » qui se balance au coin de chacune''',
     '''  {"type": "icones", "cartes": [{"icone": "repere" | "lune" | "casque" | "poubelle" | "bon" | "enfant",
                                 "label": "...", "temps": 1}, ...]}
      des cartes a icone dessinee, un « ? » qui se balance au coin de chacune
  {"type": "prix", "boites": [{"nom": "Vaxigrip", "prix": "11,75 €"}, {..., "ton": "rouge"}],
   "pastille": "plus du double"}
      des boites de vaccin dessinees, une etiquette de prix tombe sur chacune, une pastille claque'''),
]
for x, y in R2:
    assert s.count(x) == 1, (s.count(x), x[:80])
    s = s.replace(x, y)
p.write_text(s, encoding="utf-8")
print("ok")
