from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

ROOT = Path(r"C:\IA\svg\rd_database_complete\assets\generated_icons")
OUT = Path(r"C:\IA\svg\chemsex_8_sustancias_from_zero_v4.png")
W, H = 1080, 1440

paper = (249, 245, 235, 255)
navy = (20, 27, 49, 255)
coral = (235, 72, 89, 255)
muted = (20, 27, 49, 42)

img = Image.new("RGBA", (W, H), paper)
draw = ImageDraw.Draw(img, "RGBA")

bold = r"C:\Windows\Fonts\arialbd.ttf"
regular = r"C:\Windows\Fonts\arial.ttf"
title_font = ImageFont.truetype(bold, 155)
title_small = ImageFont.truetype(bold, 76)
name_font = ImageFont.truetype(bold, 28)
long_font = ImageFont.truetype(bold, 19)
micro = ImageFont.truetype(regular, 17)

# Almost empty page: only a few typographic marks and one accent color.
draw.rectangle((0, 0, 28, H), fill=navy)
draw.rectangle((28, 0, 37, H), fill=coral)
draw.text((64, 56), "CHEMSEX", font=micro, fill=coral)
draw.text((64, 84), "RD / LÁMINA", font=micro, fill=navy)

# The title is the composition: fragmented, oversized and crossing the page.
draw.text((-70, 285), "SUS", font=title_font, fill=navy)
draw.text((200, 410), "TANCIAS", font=title_font, fill=navy)
# A ghosted offset gives the title physical print presence without decorative panels.
draw.text((18, 298), "SUS", font=title_font, fill=(235, 72, 89, 52))
draw.text((288, 423), "TANCIAS", font=title_font, fill=(235, 72, 89, 52))

# Thin editorial rules are the only supporting geometry.
draw.line((72, 640, 1004, 640), fill=coral, width=5)
draw.line((72, 646, 520, 646), fill=navy, width=2)
draw.line((560, 1195, 1004, 1195), fill=navy, width=2)

# Sparse paper grain.
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain, "RGBA")
random.seed(404)
for _ in range(9000):
    gd.point((random.randrange(W), random.randrange(H)), fill=(20, 27, 49, random.randrange(4, 15)))
img = Image.alpha_composite(img, grain)

def paste_icon(name, x, y, size, angle=0):
    icon = Image.open(ROOT / f"{name}.png").convert("RGBA")
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    if angle:
        icon = icon.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    alpha = icon.getchannel("A")
    shadow = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    shadow.putalpha(alpha.point(lambda p: int(p * .20)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(shadow, (x + 8, y + 9))
    img.alpha_composite(icon, (x, y))

def label(text, x, y, angle=0, long=False, color=navy, accent=coral):
    fnt = long_font if long else name_font
    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    box = dummy.textbbox((0, 0), text, font=fnt)
    layer = Image.new("RGBA", (box[2] - box[0] + 26, box[3] - box[1] + 22), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer, "RGBA")
    ld.text((13, 7), text, font=fnt, fill=color)
    ld.line((13, layer.height - 5, layer.width - 13, layer.height - 5), fill=accent, width=4)
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    img.alpha_composite(layer, (x, y))

# Icons punctuate the oversized letters instead of occupying equal slots.
paste_icon("cannabis", 38, 180, 200, angle=-13)
label("CANNABIS", 82, 420, angle=-7)

paste_icon("cocaine", 770, 145, 190, angle=8)
label("COCAÍNA", 786, 355, angle=6)

paste_icon("alkyl_nitrites", 138, 655, 150, angle=-12)
label("NITRITOS DE ALQUILO", 112, 835, angle=-10, long=True)

paste_icon("ketamine", 810, 625, 170, angle=10)
label("KETAMINA", 970, 690, angle=90)

paste_icon("mdma", 18, 920, 210, angle=-8)
label("MDMA", 70, 1135, angle=-6)

paste_icon("ghb_gbl", 450, 780, 150, angle=7)
label("GHB / GBL", 430, 965, angle=4)

paste_icon("amphetamine", 800, 895, 155, angle=-12)
label("ANFETAMINA", 735, 1080, angle=-8)

paste_icon("methamphetamine", 305, 1125, 225, angle=7)
label("METANFETAMINA", 275, 1370, angle=3, long=True)

img.save(OUT)
print(OUT)
