from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

BASE3 = Path(r"C:\Users\issvk\.codex\generated_images\01a01361-7f6d-76b0-b1b1-f4c1c81197fe\exec-47e1e617-6007-4ce2-b643-e4b3f353f6e3.png")
BASE4 = Path(r"C:\Users\issvk\.codex\generated_images\01a01361-7f6d-76b0-b1b1-f4c1c81197fe\exec-b13181c5-3a77-4bf1-b6ea-e105eec46238.png")
ICON_ROOT = Path(r"C:\IA\svg\rd_database_complete\assets\generated_icons")
OUT3 = Path(r"C:\IA\svg\chemsex_lamina_03_contexto_sustancias_v4.png")
OUT4 = Path(r"C:\IA\svg\chemsex_lamina_04_reduccion_danos_v4.png")

NAVY = (24, 34, 57, 255)
CREAM = (248, 243, 226, 245)
CORAL = (238, 93, 111, 255)
GOLD = (231, 166, 65, 255)
MINT = (157, 180, 145, 255)

bold_path = r"C:\Windows\Fonts\arialbd.ttf"
regular_path = r"C:\Windows\Fonts\arial.ttf"
title_font = ImageFont.truetype(bold_path, 52)
section_font = ImageFont.truetype(bold_path, 28)
body_font = ImageFont.truetype(regular_path, 21)
label_font = ImageFont.truetype(bold_path, 17)
small_font = ImageFont.truetype(regular_path, 16)

def wrap(draw, text, font, width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def text_block(img, xy, text, font, fill=NAVY, width=350, spacing=5):
    d = ImageDraw.Draw(img, "RGBA")
    lines = []
    for paragraph in text.split("\n"):
        lines.extend(wrap(d, paragraph, font, width) if paragraph else [""])
    d.multiline_text(xy, "\n".join(lines), font=font, fill=fill, spacing=spacing,
                     stroke_width=2, stroke_fill=(248, 243, 226, 205))
    return len(lines) * (font.size + spacing)

def add_title(img, title, subtitle=None):
    d = ImageDraw.Draw(img, "RGBA")
    d.text((48, 38), title, font=title_font, fill=NAVY,
           stroke_width=3, stroke_fill=(248, 243, 226, 220))
    d.line((50, 105, 390, 105), fill=CORAL, width=5)
    if subtitle:
        d.text((52, 120), subtitle, font=small_font, fill=NAVY,
               stroke_width=2, stroke_fill=(248, 243, 226, 205))

def paste_icon(img, name, x, y, size, angle=0):
    icon = Image.open(ICON_ROOT / f"{name}.png").convert("RGBA")
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    if angle:
        icon = icon.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    alpha = icon.getchannel("A")
    shadow = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    shadow.putalpha(alpha.point(lambda p: int(p * .15)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(shadow, (x + 7, y + 8))
    img.alpha_composite(icon, (x, y))
    return icon.width, icon.height

def icon_label(img, text, x, y, width=200, accent=CORAL, font=label_font):
    d = ImageDraw.Draw(img, "RGBA")
    lines = wrap(d, text, font, width)
    d.multiline_text((x, y), "\n".join(lines), font=font, fill=NAVY, spacing=2,
                     stroke_width=2, stroke_fill=(248, 243, 226, 205))
    line_y = y + len(lines) * (font.size + 2) + 2
    d.line((x, line_y, min(x + width, x + 190), line_y), fill=accent, width=3)

def place_text_zone(img, title, body, x, y, width, accent):
    d = ImageDraw.Draw(img, "RGBA")
    d.text((x, y), title, font=section_font, fill=NAVY,
           stroke_width=2, stroke_fill=(248, 243, 226, 210))
    line_y = y + 37
    d.line((x, line_y, x + min(width, 250), line_y), fill=accent, width=4)
    text_block(img, (x, line_y + 18), body, body_font, fill=NAVY, width=width, spacing=5)

# ---------------- Slide 3: context + substances ----------------
slide3 = Image.open(BASE3).convert("RGBA")
add_title(slide3, "El contexto en Chile", "En Chile es más frecuente en contextos de:")

d3 = ImageDraw.Draw(slide3, "RGBA")
context_lines = ["Fiestas privadas y orgías", "Cruising, sexo en lugares públicos", "Encuentros coordinados por aplicaciones"]
for i, line in enumerate(context_lines):
    yy = 158 + i * 35
    d3.ellipse((52, yy + 7, 60, yy + 15), fill=CORAL)
    d3.text((72, yy), line, font=small_font, fill=NAVY)

d3.text((52, 275), "Entre las sustancias utilizadas comúnmente se encuentran:", font=small_font, fill=NAVY)

# Exact source list; the symbols are editorial references, not identity claims.
items = [
    ("mda", "Éxtasis (pasti o pilas)", 690, 70, 112, -8, 690, 205, GOLD),
    ("mdma", "MDMA", 545, 255, 104, 7, 555, 382, CORAL),
    ("cannabis", "Marihuana", 760, 360, 112, -8, 760, 495, MINT),
    ("alkyl_nitrites", "Popper", 385, 470, 100, -10, 382, 590, CORAL),
    ("cocaine", "Cocaína", 190, 475, 105, 8, 195, 600, GOLD),
    ("ketamine", "Ketamina", 730, 605, 110, 8, 735, 735, MINT),
    ("methamphetamine", "Metanfetamina (cristal)", 200, 820, 125, -7, 150, 965, CORAL),
    ("ghb_gbl", "GHB", 520, 1110, 120, 6, 525, 1250, GOLD),
]
for name, label_text, x, y, size, angle, lx, ly, accent in items:
    paste_icon(slide3, name, x, y, size, angle)
    icon_label(slide3, label_text, lx, ly, width=210, accent=accent, font=small_font)

slide3.save(OUT3)

# ---------------- Slide 4: reduction of harms ----------------
slide4 = Image.open(BASE4).convert("RGBA")
add_title(slide4, "Reducción de daños")

# Three exact content blocks follow the open negative-space zones of the new
# Chemsex-specific illustration: testing, sexual health/boundaries and mental health.
place_text_zone(slide4, "Prevenir", "los riesgos asociados al consumo de drogas", 365, 155, 390, CORAL)
place_text_zone(slide4, "Cuidar", "de infecciones de transmisión sexual y otros daños físicos relacionados", 355, 595, 330, GOLD)
place_text_zone(slide4, "Proteger", "la salud mental durante y después de las sesiones", 430, 980, 370, MINT)

slide4.save(OUT4)
print(OUT3)
print(OUT4)
