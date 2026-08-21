from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(r"C:\Users\issvk\.codex\generated_images\01a01361-7f6d-76b0-b1b1-f4c1c81197fe\exec-84de0cc8-4e63-41bb-99e7-eb6f42f303da.png")
OUT = Path(r"C:\IA\svg\chemsex_8_sustancias_typography_mockup.png")

img = Image.open(SRC).convert("RGBA")
draw = ImageDraw.Draw(img)

font_bold = r"C:\Windows\Fonts\arialbd.ttf"
font_regular = r"C:\Windows\Fonts\arial.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

title = font(font_bold, 42)
kicker = font(font_bold, 15)
name = font(font_bold, 23)
small = font(font_bold, 19)

navy = (21, 32, 59, 235)
cream = (247, 241, 220, 255)
yellow = (255, 220, 117, 255)
pink = (255, 102, 140, 255)
guide = (255, 233, 165, 235)
dot_fill = (255, 112, 145, 255)

def label(x, y, text, fnt, angle=0, anchor="la"):
    bbox = draw.textbbox((0, 0), text, font=fnt, stroke_width=7 if fnt == name else 6)
    w = bbox[2] - bbox[0] + 28
    h = bbox[3] - bbox[1] + 28
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((14, 14), text, font=fnt, fill=cream, stroke_width=7 if fnt == name else 6, stroke_fill=navy)
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    if anchor == "mm":
        pos = (int(x - layer.width / 2), int(y - layer.height / 2))
    else:
        pos = (x, y)
    img.alpha_composite(layer, pos)

def connector(points):
    draw.line(points, fill=guide, width=3, joint="curve")
    x, y = points[-1]
    draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=dot_fill, outline=navy, width=3)

# One irregular title treatment entering from the upper-left edge.
card = Image.new("RGBA", (300, 190), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.polygon([(10, 10), (286, 2), (294, 180), (18, 188)], fill=navy, outline=yellow)
cd.text((38, 42), "8 SÍMBOLOS", font=kicker, fill=yellow, spacing=2)
cd.text((35, 83), "SUSTANCIAS", font=title, fill=cream)
cd.line((39, 143, 255, 133), fill=pink, width=6)
card = card.rotate(4, expand=True, resample=Image.Resampling.BICUBIC)
img.alpha_composite(card, (-4, 28))

# Eight labels follow the icon network instead of forming rows.
connector([(258, 336), (89, 333)])
label(67, 278, "COCAÍNA", name, angle=7)

connector([(620, 159), (733, 78)])
label(644, 29, "CANNABIS", name, angle=-4, anchor="mm")

connector([(851, 426), (985, 445)])
label(884, 364, "KETAMINA", small, angle=-8)

connector([(164, 749), (66, 827)])
label(30, 838, "MDMA", name, angle=8)

connector([(805, 849), (950, 923)])
label(824, 935, "METANFETAMINA", small, angle=-8)

connector([(191, 1050), (56, 1164)])
label(27, 1172, "ANFETAMINA", small, angle=8)

connector([(419, 1251), (348, 1370)])
label(348, 1395, "GHB / GBL", name, angle=4, anchor="mm")

connector([(744, 1260), (895, 1340)])
label(902, 1350, "NITRITOS DE ALQUILO", small, angle=-5, anchor="mm")

img.save(OUT)
print(OUT)
