"""Render the THUNDERCLATTER wordmark as a pixel-art PNG: own 7x9 bitmap font, cyan-to-purple
dithered gradient, dark outline, purple extruded shadow. Usage: python3 -I scripts/make-title.py"""
from PIL import Image

G = {
 'T': ["#######","#######","..###..","..###..","..###..","..###..","..###..","..###..","..###.."],
 'H': ["##...##","##...##","##...##","##...##","#######","#######","##...##","##...##","##...##"],
 'U': ["##...##","##...##","##...##","##...##","##...##","##...##","##...##",".#####.",".#####."],
 'N': ["##...##","###..##","####.##","#######","##.####","##..###","##...##","##...##","##...##"],
 'D': ["######.","#######","##...##","##...##","##...##","##...##","##...##","#######","######."],
 'E': ["#######","#######","##.....","#####..","#####..","##.....","##.....","#######","#######"],
 'R': ["######.","#######","##...##","##...##","#######","#####..","##.##..","##..###","##...##"],
 'C': [".######","#######","##.....","##.....","##.....","##.....","##.....","#######",".######"],
 'L': ["##.....","##.....","##.....","##.....","##.....","##.....","##.....","#######","#######"],
 'A': [".#####.","#######","##...##","##...##","#######","#######","##...##","##...##","##...##"],
}
TEXT = "THUNDERCLATTER"
OUTLINE, SHADOW = (11, 8, 48), (88, 24, 160)
# gradient bands top to bottom, one per glyph row
BANDS = [(60,235,255),(60,215,255),(70,180,255),(90,140,255),(120,100,255),(150,60,240),(175,40,225),(190,30,200),(150,30,170)]

W, H = len(TEXT) * 8 + 3, 9 + 6
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
px = img.load()
mask = set()
for i, ch in enumerate(TEXT):
    for y, row in enumerate(G[ch]):
        for x, c in enumerate(row):
            if c == '#':
                mask.add((2 + i * 8 + x, 2 + y))

def put(x, y, col):
    if 0 <= x < W and 0 <= y < H:
        px[x, y] = col + (255,)

for (x, y) in mask:                      # extruded shadow, then outline, then fill
    for d in (1, 2, 3):
        put(x, y + d, SHADOW)
for (x, y) in mask:
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (x + dx, y + dy) not in mask:
                put(x + dx, y + dy, OUTLINE)
for (x, y) in mask:
    r = y - 2
    band = BANDS[r]
    if r % 2 == 1 and (x + y) % 2 == 0:  # checkerboard dither toward next band
        band = BANDS[min(r + 1, len(BANDS) - 1)]
    put(x, y, band)
img.save("assets/title.png", optimize=True)
img.resize((W * 8, H * 8), Image.NEAREST).save("/tmp/title-prev.png")
print(W, H)
