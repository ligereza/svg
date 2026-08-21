from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

ROOT = Path(r"C:\IA\svg\rd_database_complete\assets\generated_icons")
OUT = Path(r"C:\IA\svg\chemsex_8_sustancias_from_zero_v3.png")
W, H = 1080, 1440

navy = (18, 25, 49, 255)
cream = (247, 242, 227, 255)
coral = (235, 75, 88, 245)
yellow = (247, 192, 46, 245)
mint = (103, 183, 151, 235)
violet = (123, 87, 170, 235)
blue = (56, 111, 195, 235)

img = Image.new("RGBA", (W, H), navy)
draw = ImageDraw.Draw(img, "RGBA")

bold = r"C:\Windows\Fonts\arialbd.ttf"
title_font = ImageFont.truetype(bold, 132)
kicker_font = ImageFont.truetype(bold, 26)
name_font = ImageFont.truetype(bold, 30)
long_font = ImageFont.truetype(bold, 20)

# Monumental fields: four shapes span the page and carry several icons at once.
draw.polygon([(-120, 270), (1190, 80), (1180, 430), (-80, 635)], fill=cream)
draw.ellipse((730, -235, 1270, 305), fill=yellow)
draw.ellipse((-360, 760, 390, 1530), fill=coral)
draw.polygon([(590, 825), (1110, 620), (1130, 1440), (430, 1440)], fill=violet)
draw.polygon([(-70, 1100), (470, 1000), (730, 1450), (-80, 1450)], fill=mint)
draw.polygon([(0, 520), (250, 410), (540, 650), (0, 870)], fill=blue)

# Coarse print texture.
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain, "RGBA")
random.seed(31)
for _ in range(21000):
    gd.point((random.randrange(W), random.randrange(H)), fill=(255, 255, 255, random.randrange(5, 18)))
img = Image.alpha_composite(img, grain)
draw = ImageDraw.Draw(img, "RGBA")

# Oversized title, cropped by the page edges on purpose.
draw.text((38, 50), "SUSTANCIAS", font=title_font, fill=cream)
draw.text((55, 190), "CHEMSEX", font=kicker_font, fill=coral)
draw.line((55, 236, 420, 236), fill=navy, width=6)

def paste_icon(name, x, y, size, angle=0):
    icon = Image.open(ROOT / f"{name}.png").convert("RGBA")
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    if angle:
        icon = icon.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    alpha = icon.getchannel("A")
    shadow = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    shadow.putalpha(alpha.point(lambda p: int(p * .30)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    img.alpha_composite(shadow, (x + 11, y + 13))
    img.alpha_composite(icon, (x, y))

def label(text, x, y, angle=0, long=False, light=False, accent=coral):
    fnt = long_font if long else name_font
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    box = d.textbbox((0, 0), text, font=fnt)
    layer = Image.new("RGBA", (box[2] - box[0] + 32, box[3] - box[1] + 24), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer, "RGBA")
    fill = cream if light else navy
    ld.text((16, 8), text, font=fnt, fill=fill)
    ld.line((16, layer.height - 5, layer.width - 16, layer.height - 5), fill=accent, width=6)
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    img.alpha_composite(layer, (x, y))

# Larger, overlapping icon scale; no grid and no equal cards.
paste_icon("cannabis", -12, 300, 270, angle=-9)
label("CANNABIS", 68, 548, angle=-6, accent=mint)

paste_icon("cocaine", 730, 250, 245, angle=7)
label("COCAÍNA", 760, 515, angle=4, light=True, accent=blue)

paste_icon("alkyl_nitrites", 280, 585, 205, angle=-13)
label("NITRITOS DE ALQUILO", 104, 790, angle=-10, long=True, light=True, accent=yellow)

paste_icon("ketamine", 808, 580, 210, angle=9)
label("KETAMINA", 826, 810, angle=11, light=True, accent=violet)

paste_icon("mdma", -15, 855, 245, angle=-9)
label("MDMA", 44, 1123, angle=-4, accent=coral)

paste_icon("ghb_gbl", 450, 790, 190, angle=8)
label("GHB / GBL", 430, 1000, angle=4, light=True, accent=mint)

paste_icon("amphetamine", 800, 920, 190, angle=-12)
label("ANFETAMINA", 752, 1135, angle=-8, light=True, accent=yellow)

paste_icon("methamphetamine", 300, 1130, 265, angle=8)
label("METANFETAMINA", 270, 1380, angle=3, long=True, accent=blue)

img.save(OUT)
print(OUT)
