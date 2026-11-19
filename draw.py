"""Draw the 18 November 2026 front page for make.fun news-image-20261118.

Flat vector-style newspaper front page, drawn programmatically with PIL.
Run:  python3 draw.py        # writes entry.png (1024x1024) next to this file
"""

import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CONTENT_W = W - 2 * MARGIN

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, color=(178, 34, 34)):
    f = font(SANS_BOLD, 15)
    draw.text((x, y), label, font=f, fill=color)
    return y + 21


def headline(draw, x, y, text, size, max_w, color=(20, 20, 20)):
    f = font(SERIF, size)
    lines = wrap(draw, text, f, max_w)
    return text_block(draw, (x, y), lines, f, color, leading=int(size * 1.08))


def body(draw, x, y, text, size, max_w, color=(40, 40, 40)):
    f = font(SANS, size)
    lines = wrap(draw, text, f, max_w)
    return text_block(draw, (x, y), lines, f, color, leading=int(size * 1.35))


def panel(draw, x, y, w, h, border=(30, 30, 30)):
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=(255, 255, 255),
                   outline=border, width=2)
    draw.line([x + 2, y + 2, x + w - 3, y + 2], fill=(178, 34, 34), width=3)
    return x + 16, y + 12


# ---------------------------------------------------------------- scenes
def scene_shenzhen(draw, x, y, w, h):
    """Three flags above a Shenzhen skyline, dusk sky."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    # dusk band
    draw.rectangle([x, y, x + w, y + 34], fill=(24, 44, 78))
    # three flags: US, China, Russia
    fw, fh = 58, 32
    gap = (w - 3 * fw) // 4
    for i, kind in enumerate(["us", "cn", "ru"]):
        fx = x + gap + i * (fw + gap)
        fy = y + 46
        draw.line([(fx, fy), (fx, fy + fh + 10)], fill=(40, 40, 40), width=3)
        if kind == "us":
            for s in range(6):
                col = (178, 34, 34) if s % 2 == 0 else (255, 255, 255)
                draw.rectangle([fx + 3, fy + s * 5, fx + 3 + fw,
                                fy + (s + 1) * 5], fill=col)
            draw.rectangle([fx + 3, fy, fx + 23, fy + 15],
                           fill=(30, 60, 120))
        elif kind == "cn":
            draw.rectangle([fx + 3, fy, fx + 3 + fw, fy + fh],
                           fill=(222, 41, 16), outline=(40, 40, 40), width=1)
            draw.ellipse([fx + 10, fy + 7, fx + 24, fy + 21],
                         fill=(255, 214, 90))
        else:
            for s, col in enumerate([(255, 255, 255), (30, 60, 160),
                                     (178, 34, 34)]):
                draw.rectangle([fx + 3, fy + s * 11, fx + 3 + fw,
                                fy + (s + 1) * 11], fill=col)
            draw.rectangle([fx + 3, fy, fx + 3 + fw, fy + fh],
                           outline=(40, 40, 40), width=1)
    # skyline of towers along the bottom
    base = y + h
    fracs = [0.40, 0.56, 0.34, 0.62, 0.44, 0.58, 0.36]
    tw = w // 7
    for i, fr in enumerate(fracs):
        bh = int(h * fr)
        bx = x + i * tw + 2
        draw.rectangle([bx, base - bh, bx + tw - 4, base], fill=(60, 90, 128))
        for wy in range(base - bh + 6, base - 4, 10):
            draw.rectangle([bx + 4, wy, bx + tw - 8, wy + 3],
                           fill=(190, 214, 238))


def scene_gulf(draw, x, y, w, h):
    """Night sky over the Gulf: drone streaks and a naval base silhouette."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    rng = random.Random(18112026)
    for _ in range(60):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 4)
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # moon
    draw.ellipse([x + w - 70, y + 12, x + w - 30, y + 52],
                 fill=(235, 230, 200))
    # drone streaks crossing the sky
    for i in range(4):
        sy = y + 22 + i * 16
        draw.line([(x + 16 + i * 30, sy), (x + 16 + i * 30 + 90, sy + 26)],
                  fill=(255, 140, 60), width=3)
        draw.ellipse([x + 16 + i * 30 + 88, sy + 24,
                      x + 16 + i * 30 + 94, sy + 30], fill=(255, 190, 90))
    # sea and base silhouette
    base = y + h
    draw.rectangle([x, base - 30, x + w, base], fill=(18, 70, 105))
    for bx, bw, bh in [(10, 46, 34), (66, 30, 48), (106, 54, 30),
                       (170, 26, 42), (206, 48, 36)]:
        draw.rectangle([x + bx, base - 30 - bh, x + bx + bw, base - 30],
                       fill=(8, 12, 28))
        draw.rectangle([x + bx + 4, base - 30 - bh - 10, x + bx + 8,
                        base - 30 - bh], fill=(8, 12, 28))


def scene_bridge(draw, x, y, w, h):
    """A long bridge over grey water, one span broken and smoking."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 208, 220))
    # sea
    draw.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(90, 125, 155))
    for i in range(5):
        wy = y + int(h * 0.68) + i * 12
        draw.line([(x + 8, wy), (x + w - 8, wy)], fill=(150, 180, 205),
                  width=2)
    # bridge deck with a gap in the middle
    deck_y = y + int(h * 0.52)
    draw.rectangle([x, deck_y, x + w // 2 - 34, deck_y + 8], fill=(70, 70, 78))
    draw.rectangle([x + w // 2 + 34, deck_y, x + w, deck_y + 8],
                   fill=(70, 70, 78))
    # fallen span tilted into the water
    draw.polygon([(x + w // 2 - 34, deck_y),
                  (x + w // 2 + 10, deck_y + 44),
                  (x + w // 2 + 34, deck_y + 40),
                  (x + w // 2 - 8, deck_y + 2)], fill=(50, 50, 58))
    # pillars
    for px in (x + 60, x + w - 80):
        draw.rectangle([px, deck_y + 8, px + 14, y + h - 8], fill=(90, 90, 98))
    # smoke from the gap
    for i, (sx, sy, r) in enumerate([(0, -6, 10), (12, -22, 13), (-8, -36, 16),
                                     (6, -52, 18)]):
        cx = x + w // 2 + sx
        cy = deck_y + sy
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 128))


def scene_senate(draw, x, y, w, h):
    """A ballot box with a rising bar chart: 56 to 44."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    # two bars
    base = y + h - 26
    bw = 52
    bx1 = x + 44
    bx2 = x + w - 44 - bw
    h1 = int((h - 60) * 0.56)
    h2 = int((h - 60) * 0.44)
    draw.rectangle([bx1, base - h1, bx1 + bw, base], fill=(30, 80, 160))
    draw.rectangle([bx2, base - h2, bx2 + bw, base], fill=(178, 34, 34))
    f = font(SANS_BOLD, 22)
    d1 = "56"
    d2 = "44"
    draw.text((bx1 + bw // 2 - draw.textlength(d1, font=f) // 2, base - h1 - 30),
              d1, font=f, fill=(30, 80, 160))
    draw.text((bx2 + bw // 2 - draw.textlength(d2, font=f) // 2, base - h2 - 30),
              d2, font=f, fill=(178, 34, 34))
    # ballot slot
    draw.rectangle([x + w // 2 - 26, y + 12, x + w // 2 + 26, y + 22],
                   fill=(40, 40, 40))
    f2 = font(SANS_BOLD, 13)
    label = "ALASKA DECIDES"
    draw.text((x + w // 2 - draw.textlength(label, font=f2) // 2, y + 28),
              label, font=f2, fill=(40, 40, 40))


def scene_ipo(draw, x, y, w, h):
    """A rising stock chart breaking through a ceiling line."""
    draw.rectangle([x, y, x + w, y + h], fill=(240, 244, 238))
    # grid
    for i in range(1, 4):
        gy = y + i * h // 4
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(210, 220, 208),
                  width=1)
    # ceiling line (expected range top)
    cy = y + int(h * 0.34)
    draw.line([(x + 8, cy), (x + w - 8, cy)], fill=(178, 34, 34), width=2)
    f = font(SANS_BOLD, 13)
    draw.text((x + 10, cy - 20), "EXPECTED RANGE", font=f, fill=(178, 34, 34))
    # rising line
    pts = [(x + 12, y + h - 24), (x + w * 0.25, y + h * 0.62),
           (x + w * 0.45, y + h * 0.55), (x + w * 0.62, y + h * 0.42),
           (x + w * 0.80, y + h * 0.26), (x + w - 14, y + 14)]
    draw.line(pts, fill=(30, 110, 60), width=4, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(30, 110, 60))
    f2 = font(SERIF, 34)
    draw.text((x + 14, y + h - 52), "$83", font=f2, fill=(20, 20, 20))


def scene_quad(draw, x, y, w, h):
    """Four flags around a table in Manila."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    # table
    ty = y + int(h * 0.58)
    draw.ellipse([x + 16, ty, x + w - 16, ty + 44], fill=(120, 80, 50))
    draw.rectangle([x + 16, ty + 22, x + w - 16, ty + 44], fill=(96, 62, 38))
    # four chairs / flags behind the table
    cols = [(30, 60, 120), (178, 34, 34), (30, 110, 60), (200, 140, 30)]
    for i, col in enumerate(cols):
        cx = x + 30 + i * (w - 60) // 3
        draw.rectangle([cx - 3, y + 14, cx + 3, ty + 6], fill=(60, 50, 40),
                       width=1)
        draw.rectangle([cx + 4, y + 14, cx + 34, y + 40], fill=col,
                       outline=(40, 40, 40), width=1)
        draw.ellipse([cx - 10, ty - 14, cx + 10, ty + 6], fill=(220, 200, 170),
                     outline=(120, 100, 80), width=1)
    f = font(SANS_BOLD, 13)
    label = "MANILA"
    draw.text((x + w // 2 - draw.textlength(label, font=f) // 2, y + 4),
              label, font=f, fill=(90, 70, 50))


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), (250, 246, 236))
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 118], fill=(20, 33, 61))
    d.rectangle([0, 118, W, 122], fill=(200, 162, 60))
    f_title = font(SERIF, 46)
    d.text((MARGIN, 14), "THE WORLD IN ONE PICTURE", font=f_title,
           fill=(255, 255, 255))
    f_sub = font(SANS_BOLD, 17)
    d.text((MARGIN, 86),
           "WEDNESDAY 18 NOVEMBER 2026  •  THE DAY'S NEWS IN ONE PAGE",
           font=f_sub, fill=(200, 162, 60))

    # ---- lead story: Xi-Putin in Shenzhen
    lx, ly, lw, lh = MARGIN, 136, CONTENT_W, 322
    panel(d, lx, ly, lw, lh)
    scene_shenzhen(d, lx + 2, ly + 2, 560, lh - 4)
    tx = lx + 578
    y = kicker(d, tx, ly + 14, "DIPLOMACY  •  SHENZHEN")
    y = headline(d, tx, y, "XI MEETS PUTIN ON THE EVE OF THE BIG THREE SUMMIT",
                 30, lw - 594)
    body(d, tx, y + 8,
         "Xi Jinping and Vladimir Putin open talks in Shenzhen, one "
         "day before their trilateral summit with Donald Trump. Xi "
         "pledges to stand against trade protectionism; Putin attacks "
         "Western sanctions.", 16, lw - 594)

    # ---- row 2: Gulf drones + Crimean Bridge
    ry, rh = 472, 218
    pw = (CONTENT_W - 16) // 2
    # Gulf
    px = MARGIN
    panel(d, px, ry, pw, rh)
    scene_gulf(d, px + 2, ry + 2, pw - 4, 92)
    y = kicker(d, px + 16, ry + 106, "WAR  •  THE GULF")
    y = headline(d, px + 16, y, "IRAN'S DRONES HIT US BASES IN KUWAIT AND BAHRAIN",
                 21, pw - 32)
    body(d, px + 16, y + 4,
         "Tehran says it struck Ali Al Salem air base after US jets "
         "hit Qeshm Island. Bahrain intercepts several attacks.", 14,
         pw - 32)
    # Bridge
    px = MARGIN + pw + 16
    panel(d, px, ry, pw, rh)
    scene_bridge(d, px + 2, ry + 2, pw - 4, 92)
    y = kicker(d, px + 16, ry + 106, "WAR  •  UKRAINE")
    y = headline(d, px + 16, y, "CRIMEAN BRIDGE PARTLY DOWN AFTER UKRAINE STRIKE",
                 21, pw - 32)
    body(d, px + 16, y + 4,
         "A span of the bridge collapses under a Ukrainian attack "
         "as fighting grinds on. The EU proposes a €45bn loan for "
         "Kyiv.", 14, pw - 32)

    # ---- row 3: Alaska Senate + Anthropic IPO
    ry, rh = 704, 180
    px = MARGIN
    panel(d, px, ry, pw, rh)
    scene_senate(d, px + 2, ry + 2, pw - 4, 70)
    y = kicker(d, px + 16, ry + 82, "POLITICS  •  USA")
    y = headline(d, px + 16, y, "PELTOLA TAKES ALASKA; DEMOCRATS HOLD 56-44 SENATE",
                 19, pw - 32)
    body(d, px + 16, y + 4,
         "Democrat Mary Peltola unseats Dan Sullivan in the final "
         "Senate race, sealing a 56-44 Democratic majority.", 13,
         pw - 32)
    px = MARGIN + pw + 16
    panel(d, px, ry, pw, rh)
    scene_ipo(d, px + 2, ry + 2, pw - 4, 70)
    y = kicker(d, px + 16, ry + 82, "BUSINESS  •  AI")
    y = headline(d, px + 16, y, "ANTHROPIC PRICES ITS IPO AT $83 A SHARE",
                 19, pw - 32)
    body(d, px + 16, y + 4,
         "The AI firm prices above its expected range in one of the "
         "year's biggest tech listings.", 13, pw - 32)

    # ---- bottom row: Quad panel + "also today" briefs
    ry, rh = 898, 102
    bw = (CONTENT_W - 16) // 2
    # Quad
    px = MARGIN
    panel(d, px, ry, bw, rh)
    scene_quad(d, px + 2, ry + 2, 168, rh - 4)
    tx = px + 186
    y = kicker(d, tx, ry + 10, "DIPLOMACY  •  MANILA")
    y = headline(d, tx, y, "QUAD MEETS AT LEADER LEVEL AGAIN",
                 15, bw - 202)
    body(d, tx, y + 3,
         "Trump announces a trade deal with the Philippines.",
         12, bw - 202)
    # briefs
    px = MARGIN + bw + 16
    panel(d, px, ry, bw, rh)
    y = kicker(d, px + 16, ry + 10, "ALSO TODAY")
    briefs = [
        "EU proposes a €45bn loan for Ukraine.",
        "US loses its measles-free status after 26 years.",
        "Cold kills in Gaza's displaced camps.",
        "Russian military plane crashes in Siberia: 19 dead.",
    ]
    f_brief = font(SANS, 13)
    for b in briefs:
        d.text((px + 16, y), "•  " + b, font=f_brief, fill=(40, 40, 40))
        y += 18

    return img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
