from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

ROOT = Path(r"C:\IA\svg\rd_database_complete\assets\generated_icons")
OUT = Path(r"C:\IA\svg\chemsex_8_sustancias_from_zero.png")

W, H = 1080, 1440
bg = (246, 241, 232, 255)
img = Image.new("RGBA", (W, H), bg)
draw = ImageDraw.Draw(img, "RGBA")

font_bold = r"C:\Windows\Fonts\arialbd.ttf"
font_regular = r"C:\Windows\Fonts\arial.ttf"
font_title = ImageFont.truetype(font_bold, 108)
font_title_small = ImageFont.truetype(font_bold, 42)
font_name = ImageFont.truetype(font_bold, 24)
font_name_long = ImageFont.truetype(font_bold, 17)
font_micro = ImageFont.truetype(font_regular, 16)
font_huge = ImageFont.truetype(font_bold, 560)

navy = (24, 30, 55, 255)
coral = (232, 83, 95, 220)
yellow = (244, 190, 59, 220)
blue = (56, 107, 179, 190)
mint = (86, 157, 132, 190)
violet = (125, 89, 163, 190)
ink = (24, 30, 55, 255)
paper = (246, 241, 232, 255)

# New visual language: large type, cut-paper geometry and asymmetrical clusters.
draw.rectangle((0, 0, W, 18), fill=navy)
draw.rectangle((0, 1372, W, H), fill=navy)
draw.ellipse((700, -180, 1190, 310), fill=yellow)
draw.polygon([(0, 270), (280, 150), (420, 405), (95, 520)], fill=blue)
draw.polygon([(770, 240), (1080, 140), (1080, 460), (915, 580)], fill=coral)
draw.ellipse((-180, 890, 300, 1370), fill=mint)
draw.polygon([(650, 1020), (1080, 820), (1080, 1335), (820, 1395)], fill=violet)

# A huge translucent numeral acts as structure, not as an information list.
draw.text((300, 405), "8", font=font_huge, fill=(232, 83, 95, 28), stroke_width=2, stroke_fill=(24, 30, 55, 20))

# Title: typographic architecture with a deliberately cropped edge.
draw.text((56, 48), "SUSTANCIAS", font=font_title, fill=navy, stroke_width=1, stroke_fill=navy)
draw.text((62, 171), "CHEMSEX", font=font_title_small, fill=coral)
draw.line((64, 226, 438, 226), fill=navy, width=5)
draw.text((64, 244), "ocho nombres / ocho símbolos", font=font_micro, fill=navy)

def add_noise(layer):
    # A restrained paper grain, independent from the previous reference style.
    noise = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(noise, "RGBA")
    random.seed(8)
    for _ in range(18000):
        x = random.randrange(W)
        y = random.randrange(H)
        a = random.randrange(8, 25)
        nd.point((x, y), fill=(30, 35, 50, a))
    return Image.alpha_composite(layer, noise)

def load_icon(name, box, angle=0, shadow=True):
    path = ROOT / f"{name}.png"
    icon = Image.open(path).convert("RGBA")
    icon.thumbnail((box, box), Image.Resampling.LANCZOS)
    if shadow:
        shadow_layer = Image.new("RGBA", icon.size, (0, 0, 0, 0))
        alpha = icon.getchannel("A")
        shadow_layer.putalpha(alpha.point(lambda p: int(p * 0.22)))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(12))
        # The shadow is composited by the caller after positioning.
    if angle:
        icon = icon.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    return icon

def paste_icon(name, x, y, size, angle=0, bg_color=None):
    icon = load_icon(name, size, angle)
    if bg_color:
        # Free-form cut-paper blob rather than a card or medallion.
        blob = Image.new("RGBA", (icon.width + 42, icon.height + 42), (0, 0, 0, 0))
        bd = ImageDraw.Draw(blob, "RGBA")
        points = [(20, 34), (blob.width - 30, 12), (blob.width - 5, blob.height // 2), (blob.width - 42, blob.height - 8), (30, blob.height - 18), (4, blob.height // 2)]
        bd.polygon(points, fill=bg_color)
        img.alpha_composite(blob, (x - 21, y - 21))
    img.alpha_composite(icon, (x, y))
    return (x + icon.width // 2, y + icon.height // 2, icon.width, icon.height)

def label(text, x, y, angle=0, long=False, color=ink):
    fnt = font_name_long if long else font_name
    box = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text, font=fnt, stroke_width=0)
    layer = Image.new("RGBA", (box[2] - box[0] + 22, box[3] - box[1] + 18), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer, "RGBA")
    ld.text((11, 8), text, font=fnt, fill=color, stroke_width=2, stroke_fill=paper)
    if angle:
        layer = layer.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    img.alpha_composite(layer, (x, y))

# Eight icons as a loose editorial cascade. Exact local icon assets are used.
paste_icon("cannabis", 90, 300, 230, angle=-8, bg_color=(213, 230, 170, 235))
label("CANNABIS", 82, 538, angle=-5)

paste_icon("cocaine", 738, 275, 215, angle=7, bg_color=(189, 210, 237, 235))
label("COCAÍNA", 773, 508, angle=5)

paste_icon("alkyl_nitrites", 280, 570, 170, angle=-12, bg_color=(248, 195, 105, 230))
label("NITRITOS DE ALQUILO", 152, 740, angle=-8, long=True)

paste_icon("ketamine", 800, 570, 180, angle=10, bg_color=(225, 195, 225, 235))
label("KETAMINA", 828, 758, angle=12)

paste_icon("mdma", 78, 845, 200, angle=-10, bg_color=(246, 173, 162, 235))
label("MDMA", 88, 1052, angle=-4)

paste_icon("ghb_gbl", 460, 790, 165, angle=8, bg_color=(188, 226, 214, 235))
label("GHB / GBL", 442, 958, angle=4)

paste_icon("amphetamine", 805, 880, 165, angle=-13, bg_color=(239, 213, 123, 235))
label("ANFETAMINA", 770, 1060, angle=-9)

paste_icon("methamphetamine", 330, 1100, 220, angle=8, bg_color=(174, 194, 232, 235))
label("METANFETAMINA", 296, 1330, angle=4, long=True)

# Minimal editorial footer, leaving the content open for the literal approved copy.
draw = ImageDraw.Draw(img, "RGBA")
draw.text((738, 1391), "RD / INFORMACIÓN", font=font_micro, fill=paper)

img = add_noise(img)
img.save(OUT)
print(OUT)
