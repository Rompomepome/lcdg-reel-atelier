"""Les boîtes se placent pour que l'étiquette de la dernière reste dans la colonne de texte."""
from pathlib import Path

p = Path(r"C:\Users\NR SMART\tools\lcdg-reel\lcdg\inserts.py")
s = p.read_text(encoding="utf-8")
x = '''        self.cx = [self.m + self.w * (i + 0.5) / n for i in range(n)]
        self.bw, self.bh = self.px(g["boite"][0]), self.px(g["boite"][1])'''
y = '''        self.bw, self.bh = self.px(g["boite"][0]), self.px(g["boite"][1])
        # l'etiquette deborde a droite de sa boite : les centres se resserrent d'autant, pour que la
        # derniere reste dans la colonne
        deborde = max(0.0, self.bw * g["etiquette_x"] + (self.etiquettes[-1].width - 2 * self.m) / 2
                      - self.bw / 2)
        utile = self.w - deborde
        self.cx = [self.m + utile * (i + 0.5) / n for i in range(n)]'''
assert s.count(x) == 1
s = s.replace(x, y)
p.write_text(s, encoding="utf-8")
print("ok")
