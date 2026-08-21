from pathlib import Path
from math import cos, sin, radians, degrees, atan2
from PIL import Image, ImageDraw, ImageFont

SRC = Path(r"C:\Users\issvk\.codex\generated_images\01a01361-7f6d-76b0-b1b1-f4c1c81197fe\exec-4cd5b6b9-f536-4ea1-839d-57005af63925.png")
OUT = Path(r"C:\IA\svg\chemsex_8_sustancias_integrated_text.png")

img = Image.open(SRC).convert("RGBA")

font_path = r"C:\Windows\Fonts\arialbd.ttf"
font_title = ImageFont.truetype(font_path, 48)
font_name = ImageFont.truetype(font_path, 22)
font_long = ImageFont.truetype(font_path, 17)

cream = (250, 243, 218, 255)
navy = (20, 32, 53, 255)
pink = (255, 105, 148, 255)
gold = (255, 215, 112, 255)

def text_layer(text, fnt, fill=cream, stroke=navy, stroke_width=6):
    box = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text, font=fnt, stroke_width=stroke_width)
    layer = Image.new("RGBA", (box[2] - box[0] + 24, box[3] - box[1] + 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text((12 - box[0], 12 - box[1]), text, font=fnt, fill=fill, stroke_width=stroke_width, stroke_fill=stroke)
    return layer

def paste_rotated(text, xy, fnt=font_name, angle=0, anchor="mm", fill=cream):
    layer = text_layer(text, fnt, fill=fill)
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    x, y = xy
    if anchor == "mm":
        x -= layer.width // 2
        y -= layer.height // 2
    elif anchor == "rm":
        x -= layer.width
        y -= layer.height // 2
    img.alpha_composite(layer, (int(x), int(y)))

def text_on_arc(text, center, radius, start_deg, end_deg, fnt):
    # Center the full word on the arc and rotate each glyph tangentially.
    widths = [ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(ch, font=fnt) for ch in text]
    total = sum(widths)
    span = end_deg - start_deg
    cursor = start_deg + (span - (total / radius) * 180 / 3.1415926535) / 2
    for ch, width in zip(text, widths):
        step = (width / radius) * 180 / 3.1415926535
        angle = cursor + step / 2
        x = center[0] + radius * cos(radians(angle))
        y = center[1] + radius * sin(radians(angle))
        layer = text_layer(ch, fnt, fill=cream, stroke=navy, stroke_width=5)
        # Pillow angle is clockwise-positive visually after image coordinates are applied.
        layer = layer.rotate(-(angle + 90), expand=True, resample=Image.Resampling.BICUBIC)
        img.alpha_composite(layer, (int(x - layer.width / 2), int(y - layer.height / 2)))
        cursor += step

# The title is a curved typographic ring around the ECG, not a banner.
text_on_arc("SUSTANCIAS", (520, 735), 310, 210, 330, font_title)

# Names are printed onto the colored routes and rotated with their direction.
paste_rotated("CANNABIS", (238, 318), angle=-24)
paste_rotated("COCAÍNA", (690, 350), angle=18)
paste_rotated("NITRITOS DE ALQUILO", (150, 548), fnt=font_long, angle=-18)
paste_rotated("KETAMINA", (850, 350), angle=58)
paste_rotated("MDMA", (803, 700), angle=20)
paste_rotated("GHB / GBL", (165, 1110), angle=-12)
paste_rotated("ANFETAMINA", (468, 1374), angle=-8)
paste_rotated("METANFETAMINA", (827, 1215), fnt=font_long, angle=-24)

# A small editorial marker at the bottom, without adding explanatory copy.
draw = ImageDraw.Draw(img)
draw.arc((382, 1368, 650, 1518), 195, 345, fill=pink, width=4)
draw.ellipse((510, 1435, 522, 1447), fill=gold, outline=navy, width=2)

img.save(OUT)
print(OUT)
