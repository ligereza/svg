from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

ROOT = Path(r"C:\IA\svg\rd_database_complete\assets\generated_icons")
OUT = Path(r"C:\IA\svg\chemsex_8_sustancias_from_zero_v2.png")
W, H = 1080, 1440

img = Image.new("RGBA", (W, H), (246, 241, 232, 255))
draw = ImageDraw.Draw(img, "RGBA")

bold = r"C:\Windows\Fonts\arialbd.ttf"
regular = r"C:\Windows\Fonts\arial.ttf"
title_font = ImageFont.truetype(bold, 92)
kicker_font = ImageFont.truetype(bold, 23)
name_font = ImageFont.truetype(bold, 22)
long_font = ImageFont.truetype(bold, 16)

navy = (22, 29, 53, 255)
cream = (246, 241, 232, 255)
coral = (235, 76, 91, 235)
yellow = (245, 190, 54, 230)
blue = (56, 103, 174, 205)
mint = (85, 153, 129, 210)
violet = (121, 84, 157, 210)

# Three broad color fields create one visual system, not eight individual cards.
draw.rectangle((0, 0, W, 16), fill=navy)
draw.polygon([(0, 344), (850, 180), (1080, 300), (1080, 760), (170, 980), (0, 850)], fill=blue)
draw.ellipse((-310, 810, 430, 1550), fill=mint)
draw.polygon([(690, 880), (1080, 690), (1080, 1440), (570, 1440)], fill=violet)
draw.ellipse((780, -220, 1230, 300), fill=yellow)
draw.polygon([(0, 610), (340, 490), (520, 760), (350, 1000), (0, 930)], fill=coral)

# Restrained paper grain.
noise = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(noise, "RGBA")
random.seed(14)
for _ in range(16000):
    nd.point((random.randrange(W), random.randrange(H)), fill=(22, 29, 53, random.randrange(7, 20)))
img = Image.alpha_composite(img, noise)

# Strong, compact title. No invented explanatory copy.
draw = ImageDraw.Draw(img, "RGBA")
draw.text((56, 54), "SUSTANCIAS", font=title_font, fill=navy)
draw.text((62, 160), "CHEMSEX", font=kicker_font, fill=coral)
draw.line((62, 205, 360, 205), fill=navy, width=5)

def paste_icon(name, x, y, size, angle=0):
    icon = Image.open(ROOT / f"{name}.png").convert("RGBA")
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    if angle:
        icon = icon.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    # subtle offset shadow, no frame or card
    alpha = icon.getchannel("A")
    shadow = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    shadow.putalpha(alpha.point(lambda p: int(p * .18)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(11))
    img.alpha_composite(shadow, (x + 8, y + 10))
    img.alpha_composite(icon, (x, y))

def label(text, x, y, angle=0, long=False, light=False, accent=coral):
    fnt = long_font if long else name_font
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    box = d.textbbox((0, 0), text, font=fnt)
    layer = Image.new("RGBA", (box[2] - box[0] + 26, box[3] - box[1] + 20), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer, "RGBA")
    fill = cream if light else navy
    ld.text((13, 6), text, font=fnt, fill=fill)
    ld.line((13, layer.height - 5, layer.width - 13, layer.height - 5), fill=accent, width=4)
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    img.alpha_composite(layer, (x, y))

# Eight exact local icons, arranged as an uneven editorial cascade.
paste_icon("cannabis", 94, 295, 215, angle=-8)
label("CANNABIS", 84, 510, angle=-5, accent=mint)

paste_icon("cocaine", 760, 278, 190, angle=7)
label("COCAÍNA", 772, 472, angle=4, accent=blue)

paste_icon("alkyl_nitrites", 300, 565, 150, angle=-10)
label("NITRITOS DE ALQUILO", 158, 746, angle=-8, long=True, accent=yellow)

paste_icon("ketamine", 820, 575, 165, angle=8)
label("KETAMINA", 832, 760, angle=9, accent=violet)

paste_icon("mdma", 74, 875, 185, angle=-8)
label("MDMA", 84, 1068, angle=-4, accent=coral)

paste_icon("ghb_gbl", 470, 790, 150, angle=8)
label("GHB / GBL", 450, 948, angle=4, accent=mint)

paste_icon("amphetamine", 800, 900, 150, angle=-12)
label("ANFETAMINA", 766, 1066, angle=-8, accent=yellow)

paste_icon("methamphetamine", 350, 1112, 205, angle=7)
label("METANFETAMINA", 307, 1320, angle=3, long=True, accent=blue)

img.save(OUT)
print(OUT)
