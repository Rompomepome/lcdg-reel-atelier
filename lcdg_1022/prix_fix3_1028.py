"""Review Codex : une boîte entre avec le temps de son étiquette (« temps » de la boîte, sinon de
l'insert), pas toujours au début du bloc."""
from pathlib import Path

p = Path(r"C:\Users\NR SMART\tools\lcdg-reel\lcdg\inserts.py")
s = p.read_text(encoding="utf-8")
for x, y in [
    ('''    def _t(self, i):
        g = C.PRIX_GEO
        defaut = self.spec.get("temps", 0)
        tps = self.items[i].get("temps", defaut)
        avant = [j for j in range(i) if self.items[j].get("temps", defaut) == tps]
        return self.t0(tps) + C.INSERT_ENTREE * 0.5 + len(avant) * g["decalage"]''',
     '''    def _t_boite(self, i):
        """Entree de la boite i : avec le temps du texte de son "temps" (celui de l'insert par
        defaut), les boites d'un meme temps a la suite."""
        defaut = self.spec.get("temps", 0)
        tps = self.items[i].get("temps", defaut)
        avant = [j for j in range(i) if self.items[j].get("temps", defaut) == tps]
        return self.t0(tps) + len(avant) * C.INSERT_DECALAGE

    def _t(self, i):
        """Chute de l'etiquette i, apres l'entree de sa boite ; les etiquettes d'un meme temps a
        la suite."""
        g = C.PRIX_GEO
        defaut = self.spec.get("temps", 0)
        tps = self.items[i].get("temps", defaut)
        avant = [j for j in range(i) if self.items[j].get("temps", defaut) == tps]
        return self.t0(tps) + C.INSERT_ENTREE * 0.5 + len(avant) * g["decalage"]'''),
    ('''            k, a = _entree(t, self.t0() + i * C.INSERT_DECALAGE, final)
            if a <= 0:
                continue
            _poser(out, boite, self.cx[i], self.haut + self.bh / 2, k, a)''',
     '''            k, a = _entree(t, self._t_boite(i), final)
            if a <= 0:
                continue
            _poser(out, boite, self.cx[i], self.haut + self.bh / 2, k, a)'''),
]:
    assert s.count(x) == 1, x[:60]
    s = s.replace(x, y)
p.write_text(s, encoding="utf-8")
print("ok")
