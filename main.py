#!/usr/bin/env python3
"""Global Wire front page: the world's news of Thursday 26 November 2026.

Draws a 1024x1024 newspaper front page with PIL (stdlib only) and writes it
to /output/entry.png. Deterministic: no time, randomness or network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 253, 248)
INK = (12, 12, 12)
RED = (178, 34, 34)
GREY = (90, 90, 90)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width in pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading, color=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x, y, w, thick=3):
    draw.rectangle([x, y, x + w, y + thick - 1], fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 44  # margin

    # ---- masthead ----
    d.text((m, 18), "GLOBAL WIRE", font=font(SERIF, 96), fill=INK)
    rule(d, m, 138, W - 2 * m, 5)
    d.text((m, 152), "THURSDAY 26 NOVEMBER 2026", font=font(SANS_B, 30), fill=RED)
    d.text((W - m - 330, 154), "THE WORLD TODAY", font=font(SANS, 26), fill=GREY)
    rule(d, m, 192, W - 2 * m, 2)

    # ---- lead story ----
    y = 208
    d.text((m, y), "TRADE WAR ESCALATES", font=font(SANS_B, 24), fill=RED)
    y += 36
    d.text((m, y), "US UNVEILS NEW TARIFFS", font=font(SERIF, 40), fill=INK)
    y += 48
    d.text((m, y), "ON 14 NATIONS", font=font(SERIF, 40), fill=INK)
    y += 50
    y = para(d, m, y,
             "China, the EU, Japan and India among the targets as Washington "
             "acts on overcapacity.",
             font(SERIF_R, 25), W - 2 * m - 310, 31)
    y += 6
    y = para(d, m, y,
             "Washington proposed country-specific tariffs on 14 partners on "
             "Thursday, the latest escalation in a trade fight shaking "
             "markets worldwide.",
             font(SANS, 21), W - 2 * m - 310, 27)

    # lead graphic: tariff bars, right of the lead text
    gx, gy, gw, gh = 700, 208, 280, 236
    d.rectangle([gx, gy, gx + gw, gy + gh], outline=INK, width=2)
    d.text((gx + 12, gy + 10), "TARIFFS PROPOSED", font=font(SANS_B, 18), fill=INK)
    bars = [("CHINA", 100), ("EU", 80), ("JAPAN", 60), ("INDIA", 85)]
    base = gy + 150
    bx = gx + 22
    for name, h in bars:
        d.rectangle([bx, base - h, bx + 42, base], fill=RED)
        d.text((bx - 2, base + 8), name, font=font(SANS, 14), fill=INK)
        bx += 62
    d.text((gx + 12, gy + gh - 28), "Up to 25% on some goods",
           font=font(SANS, 16), fill=GREY)

    rule(d, m, 516, W - 2 * m, 3)

    # ---- second row: two stories ----
    y = 536
    colw = (W - 2 * m - 30) // 2
    d.text((m, y), "DISASTER  •  CAIRO", font=font(SANS_B, 20), fill=RED)
    y2 = para(d, m, y + 28, "TANKER FIRE KILLS AT LEAST 31",
              font(SERIF, 30), colw, 36)
    para(d, m, y2 + 6,
         "A fuel tanker overturned and burst into flames on Cairo's ring "
         "road. At least 31 people died, Egypt's health ministry said.",
         font(SANS, 20), colw, 26)
    x2 = m + colw + 30
    d.text((x2, y), "CONFLICT  •  UKRAINE", font=font(SANS_B, 20), fill=RED)
    y2 = para(d, x2, y + 28, "UKRAINE STRIKES RUSSIAN AIRBASE",
              font(SERIF, 30), colw, 36)
    para(d, x2, y2 + 6,
         "Kyiv said it hit five Russian military jets at Savasleyka "
         "airfield. Hours later ballistic missiles struck the capital.",
         font(SANS, 20), colw, 26)

    rule(d, m, 736, W - 2 * m, 2)

    # ---- third row: three stories ----
    y = 756
    c3 = (W - 2 * m - 60) // 3
    stories = [
        ("SPACE  •  TIANGONG", "FIRST PAKISTANI IN SPACE",
         "Muhammad Zeeshan Ali boarded China's Tiangong station aboard "
         "Shenzhou-24, the first foreign national to join it."),
        ("MARKETS  •  NEW YORK", "AI SELL-OFF HITS NASDAQ HARD",
         "US stocks fell again as AI-linked selling continued; the Nasdaq "
         "fell about 4%."),
        ("ASIA  •  PYONGYANG", "KIM CALLS FOR WIDER NUCLEAR DEPLOYMENT",
         "North Korea's leader urged wider deployment of tactical nuclear "
         "weapons, blaming the US."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        x = m + i * (c3 + 30)
        d.text((x, y), kick, font=font(SANS_B, 17), fill=RED)
        y2 = para(d, x, y + 26, head, font(SERIF, 24), c3, 28)
        para(d, x, y2 + 4, body, font(SANS, 18), c3, 22)

    # ---- footer ----
    rule(d, m, 956, W - 2 * m, 3)
    d.text((m, 968), "GLOBAL WIRE  •  All stories reported Thursday 26 November 2026",
           font=font(SANS, 19), fill=GREY)
    d.text((W - m - 52, 968), "P. 1", font=font(SANS_B, 19), fill=INK)

    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png")


if __name__ == "__main__":
    main()
