"""Render the 18 November 2026 front page (news-image-20261118).

A one-page newspaper drawn with PIL: masthead, six story panels and a
briefs column, all vector shapes and text so everything stays sharp.
Run `python3 draw.py` to regenerate entry.png beside this file.
"""

import os
import random

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAD = 24
INNER = SIZE - 2 * PAD

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_R = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

INK = (20, 20, 20)
GREY = (40, 40, 40)
RED = (178, 34, 34)
NAVY = (20, 33, 61)
GOLD = (200, 162, 60)
PAPER = (250, 246, 236)


def tf(path, px):
    return ImageFont.truetype(path, px)


def split_lines(d, s, f, width):
    out = []
    current = ""
    for word in s.split():
        candidate = word if not current else current + " " + word
        if d.textlength(candidate, font=f) <= width:
            current = candidate
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def draw_lines(d, x, y, rows, f, colour, gap):
    for row in rows:
        d.text((x, y), row, font=f, fill=colour)
        y += gap
    return y


def tag(d, x, y, s):
    f = tf(SANS_B, 15)
    d.text((x, y), s, font=f, fill=RED)
    return y + 21


def head(d, x, y, s, px, width):
    f = tf(SERIF_B, px)
    rows = split_lines(d, s, f, width)
    return draw_lines(d, x, y, rows, f, INK, int(px * 1.08))


def para(d, x, y, s, px, width):
    f = tf(SANS_R, px)
    rows = split_lines(d, s, f, width)
    return draw_lines(d, x, y, rows, f, GREY, int(px * 1.35))


def frame(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(255, 255, 255),
                outline=(30, 30, 30), width=2)
    d.line([(x + 2, y + 2), (x + w - 3, y + 2)], fill=RED, width=3)


# ---------------------------------------------------------------- artwork
def art_summit(d, x, y, w, h):
    """Dusk sky, three flags, Shenzhen towers."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    d.rectangle([x, y, x + w, y + 34], fill=NAVY)
    flag_w, flag_h = 58, 32
    step = (w - 3 * flag_w) // 4
    kinds = ("us", "cn", "ru")
    for idx, kind in enumerate(kinds):
        fx = x + step + idx * (flag_w + step)
        fy = y + 46
        d.line([(fx, fy), (fx, fy + flag_h + 10)], fill=(40, 40, 40), width=3)
        if kind == "us":
            for stripe in range(6):
                c = RED if stripe % 2 == 0 else (255, 255, 255)
                d.rectangle([fx + 3, fy + stripe * 5, fx + 3 + flag_w,
                             fy + (stripe + 1) * 5], fill=c)
            d.rectangle([fx + 3, fy, fx + 23, fy + 15], fill=(30, 60, 120))
        elif kind == "cn":
            d.rectangle([fx + 3, fy, fx + 3 + flag_w, fy + flag_h],
                        fill=(222, 41, 16), outline=(40, 40, 40), width=1)
            d.ellipse([fx + 10, fy + 7, fx + 24, fy + 21], fill=(255, 214, 90))
        else:
            bands = [(255, 255, 255), (30, 60, 160), RED]
            for stripe, c in enumerate(bands):
                d.rectangle([fx + 3, fy + stripe * 11, fx + 3 + flag_w,
                             fy + (stripe + 1) * 11], fill=c)
            d.rectangle([fx + 3, fy, fx + 3 + flag_w, fy + flag_h],
                        outline=(40, 40, 40), width=1)
    bottom = y + h
    heights = [0.40, 0.56, 0.34, 0.62, 0.44, 0.58, 0.36]
    tw = w // 7
    for idx, frac in enumerate(heights):
        bh = int(h * frac)
        bx = x + idx * tw + 2
        d.rectangle([bx, bottom - bh, bx + tw - 4, bottom],
                    fill=(60, 90, 128))
        wy = bottom - bh + 6
        while wy < bottom - 4:
            d.rectangle([bx + 4, wy, bx + tw - 8, wy + 3],
                        fill=(190, 214, 238))
            wy += 10


def art_gulf(d, x, y, w, h):
    """Night over the Gulf: stars, moon, drone streaks, base silhouette."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    rng = random.Random(18112026)
    for _ in range(60):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 4)
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    d.ellipse([x + w - 70, y + 12, x + w - 30, y + 52],
              fill=(235, 230, 200))
    for i in range(4):
        sy = y + 22 + i * 16
        sx = x + 16 + i * 30
        d.line([(sx, sy), (sx + 90, sy + 26)], fill=(255, 140, 60), width=3)
        d.ellipse([sx + 88, sy + 24, sx + 94, sy + 30], fill=(255, 190, 90))
    bottom = y + h
    d.rectangle([x, bottom - 30, x + w, bottom], fill=(18, 70, 105))
    blocks = [(10, 46, 34), (66, 30, 48), (106, 54, 30), (170, 26, 42),
              (206, 48, 36)]
    for bx, bw, bh in blocks:
        d.rectangle([x + bx, bottom - 30 - bh, x + bx + bw, bottom - 30],
                    fill=(8, 12, 28))
        d.rectangle([x + bx + 4, bottom - 30 - bh - 10, x + bx + 8,
                     bottom - 30 - bh], fill=(8, 12, 28))


def art_bridge(d, x, y, w, h):
    """A bridge over grey water with one span broken and smoking."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 208, 220))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(90, 125, 155))
    for i in range(5):
        wy = y + int(h * 0.68) + i * 12
        d.line([(x + 8, wy), (x + w - 8, wy)], fill=(150, 180, 205), width=2)
    deck = y + int(h * 0.52)
    d.rectangle([x, deck, x + w // 2 - 34, deck + 8], fill=(70, 70, 78))
    d.rectangle([x + w // 2 + 34, deck, x + w, deck + 8], fill=(70, 70, 78))
    d.polygon([(x + w // 2 - 34, deck),
               (x + w // 2 + 10, deck + 44),
               (x + w // 2 + 34, deck + 40),
               (x + w // 2 - 8, deck + 2)], fill=(50, 50, 58))
    for px in (x + 60, x + w - 80):
        d.rectangle([px, deck + 8, px + 14, y + h - 8], fill=(90, 90, 98))
    puffs = [(0, -6, 10), (12, -22, 13), (-8, -36, 16), (6, -52, 18)]
    for dx, dy, r in puffs:
        cx = x + w // 2 + dx
        cy = deck + dy
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 128))


def art_senate(d, x, y, w, h):
    """Ballot box and a 56-to-44 bar chart."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    bottom = y + h - 26
    bw = 52
    left_x = x + 44
    right_x = x + w - 44 - bw
    h_left = int((h - 60) * 0.56)
    h_right = int((h - 60) * 0.44)
    d.rectangle([left_x, bottom - h_left, left_x + bw, bottom],
                fill=(30, 80, 160))
    d.rectangle([right_x, bottom - h_right, right_x + bw, bottom], fill=RED)
    f = tf(SANS_B, 22)
    for bx, bh, txt, col in ((left_x, h_left, "56", (30, 80, 160)),
                             (right_x, h_right, "44", RED)):
        tw = d.textlength(txt, font=f)
        d.text((bx + bw // 2 - tw // 2, bottom - bh - 30), txt, font=f,
               fill=col)
    d.rectangle([x + w // 2 - 26, y + 12, x + w // 2 + 26, y + 22],
                fill=(40, 40, 40))
    f2 = tf(SANS_B, 13)
    label = "ALASKA DECIDES"
    d.text((x + w // 2 - d.textlength(label, font=f2) // 2, y + 28), label,
           font=f2, fill=(40, 40, 40))


def art_ipo(d, x, y, w, h):
    """A stock line climbing through its expected-range ceiling."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 244, 238))
    for i in range(1, 4):
        gy = y + i * h // 4
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(210, 220, 208), width=1)
    ceil = y + int(h * 0.34)
    d.line([(x + 8, ceil), (x + w - 8, ceil)], fill=RED, width=2)
    f = tf(SANS_B, 13)
    d.text((x + 10, ceil - 20), "EXPECTED RANGE", font=f, fill=RED)
    pts = [(x + 12, y + h - 24), (x + w * 0.25, y + h * 0.62),
           (x + w * 0.45, y + h * 0.55), (x + w * 0.62, y + h * 0.42),
           (x + w * 0.80, y + h * 0.26), (x + w - 14, y + 14)]
    d.line(pts, fill=(30, 110, 60), width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(30, 110, 60))
    d.text((x + 14, y + h - 52), "$83", font=tf(SERIF_B, 34), fill=INK)


def art_quad(d, x, y, w, h):
    """Four flags behind a table in Manila."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    top = y + int(h * 0.58)
    d.ellipse([x + 16, top, x + w - 16, top + 44], fill=(120, 80, 50))
    d.rectangle([x + 16, top + 22, x + w - 16, top + 44], fill=(96, 62, 38))
    colours = [(30, 60, 120), RED, (30, 110, 60), (200, 140, 30)]
    for i, col in enumerate(colours):
        cx = x + 30 + i * (w - 60) // 3
        d.rectangle([cx - 3, y + 14, cx + 3, top + 6], fill=(60, 50, 40))
        d.rectangle([cx + 4, y + 14, cx + 34, y + 40], fill=col,
                    outline=(40, 40, 40), width=1)
        d.ellipse([cx - 10, top - 14, cx + 10, top + 6],
                  fill=(220, 200, 170), outline=(120, 100, 80), width=1)


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, SIZE, 118], fill=NAVY)
    d.rectangle([0, 118, SIZE, 122], fill=GOLD)
    d.text((PAD, 14), "THE WORLD IN ONE PICTURE", font=tf(SERIF_B, 46),
           fill=(255, 255, 255))
    d.text((PAD, 86),
           "WEDNESDAY 18 NOVEMBER 2026  •  THE DAY'S NEWS IN ONE PAGE",
           font=tf(SANS_B, 17), fill=GOLD)

    # lead story: Xi meets Putin in Shenzhen
    lx, ly, lw, lh = PAD, 136, INNER, 322
    frame(d, lx, ly, lw, lh)
    art_summit(d, lx + 2, ly + 2, 560, lh - 4)
    tx = lx + 578
    yy = tag(d, tx, ly + 14, "DIPLOMACY  •  SHENZHEN")
    yy = head(d, tx, yy, "XI MEETS PUTIN ON THE EVE OF THE BIG THREE SUMMIT",
              30, lw - 594)
    para(d, tx, yy + 8,
         "Xi Jinping and Vladimir Putin open talks in Shenzhen, one "
         "day before their trilateral summit with Donald Trump. Xi "
         "pledges to stand against trade protectionism; Putin attacks "
         "Western sanctions.", 16, lw - 594)

    # second row: Gulf drones and the Crimean Bridge
    ry, rh = 472, 218
    pw = (INNER - 16) // 2
    px = PAD
    frame(d, px, ry, pw, rh)
    art_gulf(d, px + 2, ry + 2, pw - 4, 92)
    yy = tag(d, px + 16, ry + 106, "WAR  •  THE GULF")
    yy = head(d, px + 16, yy,
              "IRAN'S DRONES HIT US BASES IN KUWAIT AND BAHRAIN", 21, pw - 32)
    para(d, px + 16, yy + 4,
         "Tehran says it struck Ali Al Salem air base after US jets "
         "hit Qeshm Island. Bahrain intercepts several attacks.", 14,
         pw - 32)
    px = PAD + pw + 16
    frame(d, px, ry, pw, rh)
    art_bridge(d, px + 2, ry + 2, pw - 4, 92)
    yy = tag(d, px + 16, ry + 106, "WAR  •  UKRAINE")
    yy = head(d, px + 16, yy,
              "CRIMEAN BRIDGE PARTLY DOWN AFTER UKRAINE STRIKE", 21, pw - 32)
    para(d, px + 16, yy + 4,
         "A span of the bridge collapses under a Ukrainian attack "
         "as fighting grinds on. The EU proposes a €45bn loan for "
         "Kyiv.", 14, pw - 32)

    # third row: Alaska Senate and the Anthropic IPO
    ry, rh = 704, 180
    px = PAD
    frame(d, px, ry, pw, rh)
    art_senate(d, px + 2, ry + 2, pw - 4, 70)
    yy = tag(d, px + 16, ry + 82, "POLITICS  •  USA")
    yy = head(d, px + 16, yy,
              "PELTOLA TAKES ALASKA; DEMOCRATS HOLD 56-44 SENATE", 19,
              pw - 32)
    para(d, px + 16, yy + 4,
         "Democrat Mary Peltola unseats Dan Sullivan in the final "
         "Senate race, sealing a 56-44 Democratic majority.", 13,
         pw - 32)
    px = PAD + pw + 16
    frame(d, px, ry, pw, rh)
    art_ipo(d, px + 2, ry + 2, pw - 4, 70)
    yy = tag(d, px + 16, ry + 82, "BUSINESS  •  AI")
    yy = head(d, px + 16, yy, "ANTHROPIC PRICES ITS IPO AT $83 A SHARE",
              19, pw - 32)
    para(d, px + 16, yy + 4,
         "The AI firm prices above its expected range in one of the "
         "year's biggest tech listings.", 13, pw - 32)

    # bottom row: Quad panel and the briefs column
    ry, rh = 898, 102
    bw = (INNER - 16) // 2
    px = PAD
    frame(d, px, ry, bw, rh)
    art_quad(d, px + 2, ry + 2, 168, rh - 4)
    tx = px + 186
    yy = tag(d, tx, ry + 10, "DIPLOMACY  •  MANILA")
    yy = head(d, tx, yy, "QUAD MEETS AT LEADER LEVEL AGAIN", 15, bw - 202)
    para(d, tx, yy + 3,
         "Trump announces a trade deal with the Philippines.",
         12, bw - 202)
    px = PAD + bw + 16
    frame(d, px, ry, bw, rh)
    yy = tag(d, px + 16, ry + 10, "ALSO TODAY")
    briefs = [
        "EU proposes a €45bn loan for Ukraine.",
        "US loses its measles-free status after 26 years.",
        "Cold kills in Gaza's displaced camps.",
        "Russian military plane crashes in Siberia: 19 dead.",
    ]
    f_brief = tf(SANS_R, 13)
    for item in briefs:
        d.text((px + 16, yy), "•  " + item, font=f_brief, fill=GREY)
        yy += 18

    return img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    render().save(target, format="PNG", optimize=True)
    print("wrote", target, os.path.getsize(target), "bytes")
