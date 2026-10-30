"""Étiquettes de prix accrochées au flanc des boîtes (elles cachaient le nom du vaccin)."""
from pathlib import Path

R = Path(r"C:\Users\NR SMART\tools\lcdg-reel")
c = R / "config" / "charte.py"
s = c.read_text(encoding="utf-8")
a = "etiquette_pad=(24, 14), etiquette_x=0.3, etiquette_y=12, etiquette_angle=-10,"
assert s.count(a) == 1
s = s.replace(a, "etiquette_pad=(24, 14), etiquette_x=0.48, etiquette_y=0.62, etiquette_angle=-10,")
c.write_text(s, encoding="utf-8")

p = R / "lcdg" / "inserts.py"
s = p.read_text(encoding="utf-8")
for x, y in [
    ("_poser(out, self.etiquettes[i], ex, self.haut + self.px(g[\"etiquette_y\"]) + dy, 1.0,",
     "_poser(out, self.etiquettes[i], ex, self.haut + self.bh * g[\"etiquette_y\"] + dy, 1.0,"),
    ("_poser(out, self.pastille, self.cx[-1] - self.bw * 0.1, self.haut - self.px(g[\"pastille_dy\"]), kk,",
     "_poser(out, self.pastille, self.cx[-1], self.haut - self.px(g[\"pastille_dy\"]), kk,"),
]:
    assert s.count(x) == 1, x
    s = s.replace(x, y)
p.write_text(s, encoding="utf-8")
print("ok")
