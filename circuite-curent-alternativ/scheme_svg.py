# -*- coding: utf-8 -*-
"""Scheme didactice SVG pentru lecțiile de curent alternativ.
Fiecare funcție întoarce un <svg> ca text. Culorile: u = roșu, i = albastru,
P = verde, Q = portocaliu, S = violet; L1 maro, L2 negru, L3 gri, N albastru (culori conductoare EU).
"""
import math

RED = "#c0392b"; BLUE = "#1f5fbf"; GREEN = "#2e8b57"; ORANGE = "#d97706"; VIOLET = "#7c3aed"
L1 = "#8b5a2b"; L2 = "#3a3a3a"; L3 = "#8a8a8a"; NC = "#2563eb"; GRAY = "#9a9a9a"
FS = 13

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}" '
            f'font-family="IBM Plex Sans, Arial, sans-serif" font-size="{FS}" fill="currentColor" stroke-linecap="round" stroke-linejoin="round">'
            f'<title>{title}</title>{body}</svg>')

def txt(x, y, s, anchor="middle", size=FS, color="currentColor", weight="normal", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" fill="{color}" font-weight="{weight}" stroke="none" {extra}>{s}</text>'

def line(x1, y1, x2, y2, color="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}" fill="none"{d}/>'

def arrow(x1, y1, x2, y2, color="currentColor", w=2, head=8):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - head * math.cos(ang - 0.45); hy1 = y2 - head * math.sin(ang - 0.45)
    hx2 = x2 - head * math.cos(ang + 0.45); hy2 = y2 - head * math.sin(ang + 0.45)
    return (line(x1, y1, x2, y2, color, w) +
            f'<polygon points="{x2:.1f},{y2:.1f} {hx1:.1f},{hy1:.1f} {hx2:.1f},{hy2:.1f}" fill="{color}" stroke="none"/>')

def sine_path(x0, y0, w, amp, phase_deg=0.0, cycles=1.0, n=240):
    pts = []
    for k in range(n + 1):
        f = k / n
        x = x0 + w * f
        y = y0 - amp * math.sin(2 * math.pi * cycles * f + math.radians(phase_deg))
        pts.append(f"{x:.1f},{y:.1f}")
    return "M" + " L".join(pts)

def curve(d, color, w=2.5, dash=""):
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"{dd}/>'

# ---------- simboluri de aparate (dimensiuni în px, orientare orizontală) ----------
def sym_R(x, y, w=44, h=16, label=""):
    """Rezistor: dreptunghi, borne la (x - w/2 - 12, y) și (x + w/2 + 12, y)."""
    s = f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" fill="none" stroke="currentColor" stroke-width="2"/>'
    s += line(x - w/2 - 12, y, x - w/2, y) + line(x + w/2, y, x + w/2 + 12, y)
    if label: s += txt(x, y - h/2 - 6, label, weight="bold")
    return s

def sym_L(x, y, label="", n=4, r=6):
    """Bobină: arce în serie. borne la x-n*r-12 și x+n*r+12."""
    x0 = x - n * r
    d = f"M{x0:.1f},{y:.1f}"
    for k in range(n):
        d += f" a{r},{r} 0 0 1 {2*r},0"
    s = f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2"/>'
    s += line(x0 - 12, y, x0, y) + line(x + n * r, y, x + n * r + 12, y)
    if label: s += txt(x, y - r - 8, label, weight="bold")
    return s

def sym_C(x, y, label="", gap=6, plate=18):
    """Condensator: două plăci verticale. borne la x-gap/2-16 și x+gap/2+16."""
    s = line(x - gap/2, y - plate/2, x - gap/2, y + plate/2, w=2.5) + line(x + gap/2, y - plate/2, x + gap/2, y + plate/2, w=2.5)
    s += line(x - gap/2 - 16, y, x - gap/2, y) + line(x + gap/2, y, x + gap/2 + 16, y)
    if label: s += txt(x, y - plate/2 - 8, label, weight="bold")
    return s

def sym_src(x, y, r=14, label="~"):
    """Sursă c.a.: cerc cu sinusoidă, borne sus/jos la y-r-10 și y+r+10."""
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'
    s += curve(sine_path(x - 8, y, 16, 5), "currentColor", 1.8)
    s += line(x, y - r - 10, x, y - r) + line(x, y + r, x, y + r + 10)
    return s

def sym_motor(x, y, r=16, label="M"):
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'
    s += txt(x, y + 5, label, weight="bold", size=14)
    return s

def sym_meter(x, y, letter, r=11):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="currentColor" stroke-width="1.8"/>' + txt(x, y + 4, letter, size=11, weight="bold")

def dot(x, y, r=3, color="currentColor"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" stroke="none"/>'

def axes(x0, y0, w, up, down, xlabel="", ylabel=""):
    s = arrow(x0 - 5, y0, x0 + w + 12, y0, w=1.2, head=7)
    s += arrow(x0, y0 + down, x0, y0 - up - 12, w=1.2, head=7)
    if xlabel: s += txt(x0 + w + 14, y0 + 14, xlabel, anchor="end", size=12)
    if ylabel: s += txt(x0 + 6, y0 - up - 8, ylabel, anchor="start", size=12)
    return s

def phasor(cx, cy, length, ang_deg, color, label, lab_off=14):
    a = math.radians(ang_deg)
    x2 = cx + length * math.cos(a); y2 = cy - length * math.sin(a)
    lx = x2 + lab_off * math.cos(a); ly = y2 - lab_off * math.sin(a) + 4
    return arrow(cx, cy, x2, y2, color, 2.5, 9) + txt(lx, ly, label, color=color, weight="bold")

def angle_arc(cx, cy, r, a1, a2, color="currentColor", label="", lab_r=None):
    """arc de la unghiul a1 la a2 (grade, sens trigonometric)."""
    if a2 < a1: a1, a2 = a2, a1
    x1 = cx + r * math.cos(math.radians(a1)); y1 = cy - r * math.sin(math.radians(a1))
    x2 = cx + r * math.cos(math.radians(a2)); y2 = cy - r * math.sin(math.radians(a2))
    large = 1 if (a2 - a1) > 180 else 0
    s = f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 0 {x2:.1f},{y2:.1f}" fill="none" stroke="{color}" stroke-width="1.5"/>'
    if label:
        am = math.radians((a1 + a2) / 2); rr = lab_r or r + 12
        s += txt(cx + rr * math.cos(am), cy - rr * math.sin(am) + 4, label, color=color)
    return s

# =====================================================================
# 1. Sinusoida cu mărimile caracteristice
def fig_sinusoida():
    W, H = 640, 300
    x0, y0, w, A = 60, 150, 480, 95
    b = axes(x0, y0, w, A + 10, A + 10, "t", "u")
    b += curve(sine_path(x0, y0, w, A), RED, 3)
    # valoare maximă
    b += line(x0, y0 - A, x0 + w / 4, y0 - A, GRAY, 1, "4 3")
    b += arrow(x0 + w / 4, y0, x0 + w / 4, y0 - A, RED, 1.5, 7)
    b += txt(x0 + w / 4 + 8, y0 - A * 0.3, "Um = 325 V", anchor="start", color=RED, weight="bold")
    b += txt(x0 + w / 4 + 8, y0 - A * 0.3 + 15, "(valoarea maximă)", anchor="start", size=11)
    # valoare efectivă
    ye = y0 - A * 0.707
    b += line(x0, ye, x0 + w, ye, BLUE, 1.5, "6 4")
    b += txt(x0 + w - 4, ye - 6, "U = 230 V  (valoarea efectivă = 0,707 · Um)", anchor="end", color=BLUE, weight="bold", size=12)
    # valoare instantanee
    xi = x0 + w * 0.125; yi = y0 - A * math.sin(2 * math.pi * 0.125)
    b += line(xi, y0, xi, yi, GRAY, 1, "3 3") + dot(xi, yi, 4, RED)
    b += txt(xi, y0 + 16, "t = 2,5 ms", size=11)
    b += txt(xi - 6, yi - 8, "u = 230 V", anchor="end", size=11, color=RED)
    # perioada
    b += arrow(x0 + 2, y0 + A + 30, x0 + w - 2, y0 + A + 30, "currentColor", 1.5, 7)
    b += arrow(x0 + w - 2, y0 + A + 30, x0 + 2, y0 + A + 30, "currentColor", 1.5, 7)
    b += txt(x0 + w / 2, y0 + A + 26, "T = 20 ms = o perioadă (360°)", weight="bold")
    # gradații
    for k, lab in enumerate(["0", "5 ms\n90°", "10 ms\n180°", "15 ms\n270°", "20 ms\n360°"]):
        xk = x0 + w * k / 4
        b += line(xk, y0 - 4, xk, y0 + 4)
        l1, l2 = (lab.split("\n") + [""])[:2]
        below = k in (1, 2)
        if k: b += txt(xk, y0 + 18 if below else y0 - 24, l1, size=11) + txt(xk, y0 + 32 if below else y0 - 10, l2, size=11)
    b += txt(x0 + w / 2 - 70, y0 - A - 6, "alternanța pozitivă", size=11) + txt(x0 + 3 * w / 4 + 40, y0 + A + 12, "alternanța negativă", size=11)
    return svg(W, H, b, "Tensiunea alternativă sinusoidală de 230 V, 50 Hz")

# 2. Principiul generatorului
def fig_generator():
    W, H = 640, 260
    b = ""
    # magneți
    b += f'<rect x="40" y="60" width="50" height="120" fill="{RED}" opacity="0.85"/>' + txt(65, 125, "N", color="#fff", size=22, weight="bold")
    b += f'<rect x="230" y="60" width="50" height="120" fill="{BLUE}" opacity="0.85"/>' + txt(255, 125, "S", color="#fff", size=22, weight="bold")
    # linii de câmp
    for yy in (80, 105, 130, 155):
        b += arrow(92, yy, 228, yy, GRAY, 1, 6)
    # spira (dreptunghi rotit)
    b += f'<polygon points="125,70 205,95 195,175 115,150" fill="none" stroke="{ORANGE}" stroke-width="4"/>'
    b += arrow(160, 40, 200, 40, "currentColor", 1.5, 7) + txt(180, 32, "rotație", size=11)
    b += f'<path d="M150,50 a35,15 0 0 1 60,0" fill="none" stroke="currentColor" stroke-width="1.5"/>'
    # ax + inele colectoare + perii
    b += line(160, 120, 160, 215, "currentColor", 3)
    b += f'<circle cx="160" cy="195" r="9" fill="none" stroke="{ORANGE}" stroke-width="3"/>' + f'<circle cx="160" cy="212" r="9" fill="none" stroke="{ORANGE}" stroke-width="3"/>'
    b += line(169, 195, 200, 195, "currentColor", 2) + line(169, 212, 200, 212, "currentColor", 2)
    b += txt(210, 199, "inele colectoare + perii", anchor="start", size=11)
    b += txt(160, 245, "spira de sârmă se rotește în câmpul magnetic", size=12)
    # sinusoida cu pozițiile
    x0, y0, w, A = 380, 120, 230, 60
    b += axes(x0, y0, w, A + 10, A + 10, "t", "u")
    b += curve(sine_path(x0, y0, w, A), RED, 3)
    for k, lab in enumerate(["0°", "90°", "180°", "270°", "360°"]):
        xk = x0 + w * k / 4
        b += line(xk, y0 - 3, xk, y0 + 3) + txt(xk, y0 + A + 26, lab, size=11)
    b += txt(x0 + w / 2, y0 + A + 42, "o rotație completă = o perioadă", size=12, weight="bold")
    b += txt(x0 + w / 2, 28, "tensiunea indusă", size=12)
    return svg(W, H, b, "Principiul generatorului de curent alternativ")

# 3. Defazaj + fazori
def fig_defazaj():
    W, H = 660, 300
    x0, y0, w, A = 60, 130, 360, 80
    b = axes(x0, y0, w, A + 10, A + 10, "t", "")
    b += curve(sine_path(x0, y0, w, A), RED, 3)
    b += curve(sine_path(x0, y0, w, A * 0.7, -60), BLUE, 3)
    b += txt(x0 + w * 0.22, y0 - A - 6, "u", color=RED, weight="bold", size=15)
    b += txt(x0 + w * 0.42, y0 - A * 0.7 - 6, "i", color=BLUE, weight="bold", size=15)
    # marcaj defazaj: trecerea prin zero
    xz_u = x0; xz_i = x0 + w * (60 / 360)
    b += line(xz_i, y0, xz_i, y0 + A + 20, GRAY, 1, "3 3")
    b += arrow(xz_u, y0 + A + 20, xz_i, y0 + A + 20, "currentColor", 1.5, 6)
    b += txt((xz_u + xz_i) / 2, y0 + A + 36, "φ = 60°", weight="bold")
    b += txt(x0, y0 + A + 58, "curentul trece prin zero MAI TÂRZIU decât tensiunea", anchor="start", size=11) + txt(x0, y0 + A + 72, "→ spunem că este „în urmă” cu φ = 60°", anchor="start", size=11)
    # fazori
    cx, cy = 540, 130
    b += f'<circle cx="{cx}" cy="{cy}" r="85" fill="none" stroke="{GRAY}" stroke-width="1" stroke-dasharray="3 3"/>'
    b += line(cx - 95, cy, cx + 95, cy, GRAY, 1)
    b += phasor(cx, cy, 80, 0, RED, "U")
    b += phasor(cx, cy, 56, -60, BLUE, "I")
    b += angle_arc(cx, cy, 30, -60, 0, "currentColor", "φ")
    b += txt(cx, cy + 105, "diagrama fazorială", size=12, weight="bold")
    b += txt(cx, cy + 120, "(săgețile se rotesc împreună,", size=11) + txt(cx, cy + 133, "unghiul dintre ele rămâne φ)", size=11)
    b += txt(cx, 28, "sens de rotație", size=11) + f'<path d="M{cx-25},38 a28,12 0 0 1 50,0" fill="none" stroke="currentColor" stroke-width="1.5"/>' + arrow(cx - 22, 40, cx - 26, 36, "currentColor", 1.5, 6)
    return svg(W, H, b, "Defazajul dintre tensiune și curent și reprezentarea prin fazori")

# 4–6. Comportarea R, L, C — un panou: schemă + unde + fazor
def fig_element(kind):
    W, H = 700, 230
    b = ""
    # schema
    sx, sy = 70, 115
    b += sym_src(sx, sy)
    b += line(sx, sy - 24, sx, 40) + line(sx, 40, 170, 40) + line(sx, sy + 24, sx, 190) + line(sx, 190, 170, 190)
    if kind == "R":
        b += line(170, 40, 170, 85) + f'<rect x="162" y="85" width="16" height="60" fill="none" stroke="currentColor" stroke-width="2"/>' + line(170, 145, 170, 190)
        b += txt(190, 120, "R", anchor="start", weight="bold", size=15)
        title = "Rezistorul: tensiunea și curentul sunt în fază"
        ph_i, col_note = 0, "φ = 0°  →  i în fază cu u"
    elif kind == "L":
        b += line(170, 40, 170, 75)
        d = "M170,75"
        for k in range(4): d += " a6,6 0 0 1 0,12"
        b += f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2"/>' + line(170, 123, 170, 190)
        b += txt(190, 105, "L", anchor="start", weight="bold", size=15)
        title = "Bobina: curentul rămâne în urma tensiunii cu 90°"
        ph_i, col_note = -90, "φ = +90°  →  i în urmă"
    else:
        b += line(170, 40, 170, 105) + line(160, 105, 180, 105, w=2.5) + line(160, 113, 180, 113, w=2.5) + line(170, 113, 170, 190)
        b += txt(190, 113, "C", anchor="start", weight="bold", size=15)
        title = "Condensatorul: curentul o ia înaintea tensiunii cu 90°"
        ph_i, col_note = 90, "φ = −90°  →  i în avans"
    b += txt(sx - 30, sy + 4, "u", color=RED, weight="bold", size=14) + arrow(sx - 44, sy - 20, sx - 44, sy + 20, RED, 1.5, 6)
    b += arrow(120, 30, 150, 30, BLUE, 1.5, 6) + txt(135, 22, "i", color=BLUE, weight="bold", size=14)
    # unde
    x0, y0, w, A = 240, 115, 260, 65
    b += axes(x0, y0, w, A + 10, A + 10, "t", "")
    b += curve(sine_path(x0, y0, w, A), RED, 3)
    b += curve(sine_path(x0, y0, w, A * 0.65, ph_i), BLUE, 3)
    b += txt(x0 + 8, 30, "u", anchor="start", color=RED, weight="bold", size=14) + txt(x0 + 24, 30, "i", anchor="start", color=BLUE, weight="bold", size=14)
    b += txt(x0 + w / 2, y0 + A + 30, col_note, weight="bold", size=12)
    # fazor
    cx, cy = 620, 115
    b += line(cx - 60, cy, cx + 60, cy, GRAY, 1) + line(cx, cy - 60, cx, cy + 60, GRAY, 1)
    b += phasor(cx, cy, 52, 0, RED, "U")
    if kind == "R": b += phasor(cx, cy, 34, 0, BLUE, "I", lab_off=32)
    else: b += phasor(cx, cy, 40, ph_i, BLUE, "I")
    if kind != "R": b += angle_arc(cx, cy, 20, min(0, ph_i), max(0, ph_i), "currentColor", "90°", 30)
    return svg(W, H, b, title)

# 7. XL și XC în funcție de frecvență
def fig_reactante():
    W, H = 640, 260
    x0, y0, w, hgt = 60, 210, 520, 160
    b = axes(x0, y0, w, hgt, 0, "", "reactanța (Ω)") + txt(x0 + w + 14, y0 + 30, "f (Hz)", anchor="end", size=12)
    # XL liniar: 0,1 H -> 31,4 Ω la 50 Hz; scala: 100 Hz = w, 100 Ω = hgt
    pts = " ".join(f"{x0 + w * f / 100:.1f},{y0 - hgt * (2 * math.pi * f * 0.1) / 100:.1f}" for f in range(0, 101, 5))
    b += f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    b += txt(x0 + w * 0.97, y0 - hgt * 0.63 - 8, "XL = 2π·f·L  (L = 0,1 H)", anchor="end", color=BLUE, weight="bold")
    # XC: 20 µF: 1/(2π f C) -> la 50 Hz 159 Ω... folosim 100 µF: 31,8 Ω la 50 Hz
    pts = " ".join(f"{x0 + w * f / 100:.1f},{max(y0 - hgt, y0 - hgt * (1 / (2 * math.pi * f * 100e-6)) / 100):.1f}" for f in range(14, 101, 2))
    b += f'<polyline points="{pts}" fill="none" stroke="{ORANGE}" stroke-width="3"/>'
    b += txt(x0 + w * 0.97, y0 - hgt * 0.30, "XC = 1/(2π·f·C)  (C = 100 µF)", anchor="end", color=ORANGE, weight="bold")
    for f in (0, 25, 50, 75, 100):
        xk = x0 + w * f / 100; b += line(xk, y0 - 3, xk, y0 + 3) + txt(xk, y0 + 16, str(f), size=11)
    for r in (50, 100):
        yk = y0 - hgt * r / 100; b += line(x0 - 3, yk, x0 + 3, yk) + txt(x0 - 8, yk + 4, str(r), anchor="end", size=11)
    xk = x0 + w / 2; b += line(xk, y0, xk, y0 - hgt * 0.32, GRAY, 1, "3 3") + dot(xk, y0 - hgt * 0.314, 4, "currentColor")
    b += txt(x0 + w * 0.5 + 10, y0 - hgt * 0.06, "la 50 Hz ambele ≈ 31–32 Ω → rezonanță", anchor="start", size=11)
    b += txt(x0 + w * 0.28, y0 - hgt * 0.92, "la f = 0 (curent continuu):", anchor="start", size=11) + txt(x0 + w * 0.28, y0 - hgt * 0.84, "bobina = scurtcircuit, condensatorul = întrerupere", anchor="start", size=11)
    return svg(W, H, b, "Reactanța inductivă crește cu frecvența, cea capacitivă scade")

# 8. Circuit RL serie + triunghiul tensiunilor + triunghiul impedanțelor
def fig_rl():
    W, H = 680, 270
    b = ""
    sx, sy = 60, 135
    b += sym_src(sx, sy) + line(sx, sy - 24, sx, 50) + line(sx, 50, 100, 50) + sym_R(140, 50, label="R = 30 Ω")
    b += line(174, 50, 200, 50) + sym_L(236, 50, label="L = 0,1 H") + line(272, 50, 300, 50) + line(300, 50, 300, 220) + line(300, 220, sx, 220) + line(sx, 220, sx, sy + 24)
    b += txt(sx + 8, sy + 50, "U = 230 V", size=12, weight="bold", anchor="start") + arrow(76, 105, 76, 72, BLUE, 1.5, 6) + txt(84, 92, "I = 5,3 A", anchor="start", color=BLUE, size=11, weight="bold")
    b += txt(140, 80, "UR = 159 V", color=RED, size=11) + txt(236, 80, "UL = 166 V", color=RED, size=11)
    # triunghiul tensiunilor
    ox, oy = 360, 200; k = 0.55
    ur, ul = 159 * k, 166 * k
    b += phasor(ox, oy, 100, 0, BLUE, "I", lab_off=12)
    b += arrow(ox, oy, ox + ur, oy, RED, 2.5, 8) + txt(ox + ur / 2, oy + 18, "UR", color=RED, weight="bold")
    b += arrow(ox + ur, oy, ox + ur, oy - ul, RED, 2.5, 8) + txt(ox + ur + 14, oy - ul / 2, "UL", color=RED, weight="bold")
    b += arrow(ox, oy, ox + ur, oy - ul, RED, 3, 9) + txt(ox + ur / 2 - 12, oy - ul / 2 - 6, "U = 230 V", color=RED, weight="bold")
    b += angle_arc(ox, oy, 28, 0, 46, "currentColor", "φ = 46°", 42)
    b += txt(ox + 45, 60, "triunghiul tensiunilor", weight="bold", size=12) + txt(ox + 45, 76, "U² = UR² + UL²", size=12)
    # triunghiul impedanțelor
    ox2, oy2 = 540, 200; k2 = 2.9
    r_, x_ = 30 * k2, 31.4 * k2
    b += line(ox2, oy2, ox2 + r_, oy2, "currentColor", 2.5) + txt(ox2 + r_ / 2, oy2 + 18, "R = 30 Ω")
    b += line(ox2 + r_, oy2, ox2 + r_, oy2 - x_, "currentColor", 2.5) + txt(ox2 + r_ + 4, oy2 - x_ / 2, "XL = 31,4 Ω", anchor="start")
    b += line(ox2, oy2, ox2 + r_, oy2 - x_, VIOLET, 3) + txt(ox2 + r_ / 2 - 8, oy2 - x_ / 2 - 8, "Z = 43,4 Ω", color=VIOLET, weight="bold")
    b += angle_arc(ox2, oy2, 26, 0, 46, "currentColor", "φ", 36)
    b += txt(ox2 + 50, 60, "triunghiul impedanțelor", weight="bold", size=12) + txt(ox2 + 50, 76, "Z² = R² + XL²", size=12)
    return svg(W, H, b, "Circuit RL serie: tensiunile se adună ca laturile unui triunghi")

# 9. Triunghiul puterilor + analogia cu halba
def fig_puteri():
    W, H = 660, 290
    b = ""
    ox, oy = 90, 210; k = 0.14
    p, q = 841 * k, 881 * k
    b += arrow(ox, oy, ox + p, oy, GREEN, 3, 9) + txt(ox + p / 2, oy + 20, "P = 841 W (putere activă)", color=GREEN, weight="bold", size=12)
    b += arrow(ox + p, oy, ox + p, oy - q, ORANGE, 3, 9) + txt(ox + p + 10, oy - q / 2, "Q = 881 var", anchor="start", color=ORANGE, weight="bold", size=12) + txt(ox + p + 10, oy - q / 2 + 15, "(putere reactivă)", anchor="start", size=11)
    b += arrow(ox, oy, ox + p, oy - q, VIOLET, 3.5, 10) + txt(ox + p / 2 - 30, oy - q / 2 - 10, "S = 1219 VA", color=VIOLET, weight="bold", size=12) + txt(ox + p / 2 - 62, oy - q / 2 + 5, "(putere aparentă)", size=11)
    b += angle_arc(ox, oy, 34, 0, 46, "currentColor", "φ = 46°", 50)
    b += txt(ox + 90, 40, "S² = P² + Q²", weight="bold", size=14) + txt(ox + 90, 60, "cos φ = P / S = 0,69", size=13)
    # halba
    hx, hy = 470, 60
    b += f'<path d="M{hx},{hy} L{hx+8},{hy+170} L{hx+112},{hy+170} L{hx+120},{hy} Z" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += f'<path d="M{hx+120},{hy+40} a28,30 0 0 1 0,80" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += f'<path d="M{hx+3},{hy+60} L{hx+8},{hy+168} L{hx+112},{hy+168} L{hx+117},{hy+60} Z" fill="{GREEN}" opacity="0.55"/>'
    b += f'<path d="M{hx+1},{hy+10} L{hx+3},{hy+60} L{hx+117},{hy+60} L{hx+119},{hy+10} Z" fill="{ORANGE}" opacity="0.45"/>'
    b += txt(hx + 60, hy + 120, "P", color="#fff", weight="bold", size=22) + txt(hx + 60, hy + 42, "Q", color="#fff", weight="bold", size=20)
    b += txt(hx + 60, hy + 195, "halba = S (paharul trebuie", size=11) + txt(hx + 60, hy + 208, "să încapă bere + spumă)", size=11)
    b += txt(hx - 20, hy + 120, "berea = P (ce folosești)", anchor="end", size=11, color=GREEN)
    b += txt(hx - 20, hy + 40, "spuma = Q (ocupă loc,", anchor="end", size=11, color=ORANGE) + txt(hx - 20, hy + 53, "dar nu te satură)", anchor="end", size=11, color=ORANGE)
    return svg(W, H, b, "Triunghiul puterilor și analogia cu halba de bere")

# 10. Compensarea puterii reactive
def fig_compensare():
    W, H = 740, 270
    b = ""
    # schema: L1/N, motor, condensator paralel
    b += line(40, 40, 260, 40, L1, 3) + txt(28, 45, "L1", anchor="end", color=L1, weight="bold") + line(40, 230, 260, 230, NC, 3) + txt(28, 235, "N", anchor="end", color=NC, weight="bold")
    b += line(120, 40, 120, 110) + sym_motor(120, 130) + line(120, 146, 120, 230) + txt(150, 128, "motor", anchor="start", size=12) + txt(150, 143, "cos φ = 0,69", anchor="start", size=11)
    b += line(220, 40, 220, 125) + line(206, 125, 234, 125, w=2.5) + line(206, 133, 234, 133, w=2.5) + line(220, 133, 220, 230) + txt(242, 132, "C = 36 µF", anchor="start", size=12, weight="bold")
    b += dot(120, 40, 3, L1) + dot(220, 40, 3, L1) + dot(120, 230, 3, NC) + dot(220, 230, 3, NC)
    b += arrow(50, 55, 90, 55, BLUE, 2, 7) + txt(70, 72, "I rețea", color=BLUE, size=11, weight="bold") + txt(70, 86, "5,3 A → 3,85 A", color=BLUE, size=11)
    b += txt(150, 22, "condensatorul se leagă ÎN PARALEL cu motorul", size=12, weight="bold")
    # triunghiuri înainte / după
    def tri(ox, oy, p, q, k, title, qc=0):
        s = txt(ox + 40, oy - 130, title, weight="bold", size=12)
        s += arrow(ox, oy, ox + p * k, oy, GREEN, 3, 8) + txt(ox + p * k / 2, oy + 16, f"P = {p} W", color=GREEN, size=11, weight="bold")
        s += arrow(ox + p * k, oy, ox + p * k, oy - q * k, ORANGE, 3, 8) + txt(ox + p * k + 6, oy - q * k / 2, f"Q = {q} var", anchor="start", color=ORANGE, size=11, weight="bold")
        S = round(math.hypot(p, q))
        s += arrow(ox, oy, ox + p * k, oy - q * k, VIOLET, 3, 8) + txt(ox + p * k / 2 - 20, oy - q * k / 2 - 8, f"S = {S} VA", color=VIOLET, size=11, weight="bold")
        if qc:
            s += arrow(ox + p * k, oy - (q + qc) * k, ox + p * k, oy - q * k, GRAY, 2, 7) + f'<line x1="{ox+p*k}" y1="{oy-(q+qc)*k}" x2="{ox+p*k}" y2="{oy-q*k}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="4 3"/>'
            s += txt(ox + p * k + 6, oy - (q + qc / 2) * k, f"QC = {qc} var", anchor="start", color=GRAY, size=11) + txt(ox + p * k + 6, oy - (q + qc / 2) * k + 13, "(dat de condensator)", anchor="start", size=10)
        return s
    b += tri(320, 200, 841, 881, 0.125, "ÎNAINTE: cos φ = 0,69")
    b += tri(530, 200, 841, 278, 0.125, "DUPĂ: cos φ = 0,95", qc=603)
    return svg(W, H, b, "Compensarea puterii reactive cu un condensator în paralel")

# 11. Sistem trifazat: trei sinusoide + steaua fazorilor
def fig_trifazat():
    W, H = 680, 280
    x0, y0, w, A = 50, 130, 400, 80
    b = axes(x0, y0, w, A + 10, A + 10, "t", "")
    b += curve(sine_path(x0, y0, w, A, 0, 1.5), L1, 3) + curve(sine_path(x0, y0, w, A, -120, 1.5), L2, 3) + curve(sine_path(x0, y0, w, A, -240, 1.5), L3, 3)
    b += txt(x0 + w * (90 / 540), y0 - A - 6, "L1", color=L1, weight="bold") + txt(x0 + w * (210 / 540), y0 - A - 6, "L2", color=L2, weight="bold") + txt(x0 + w * (330 / 540), y0 - A - 6, "L3", color=L3, weight="bold")
    xa, xb = x0 + w * (90 / 540), x0 + w * (210 / 540)
    b += line(xa, y0 - A, xa, y0 + A + 20, GRAY, 1, "3 3") + line(xb, y0 - A, xb, y0 + A + 20, GRAY, 1, "3 3")
    b += arrow(xa, y0 + A + 20, xb, y0 + A + 20, "currentColor", 1.5, 6) + arrow(xb, y0 + A + 20, xa, y0 + A + 20, "currentColor", 1.5, 6)
    b += txt((xa + xb) / 2, y0 + A + 38, "120° = 6,67 ms", weight="bold", size=12)
    b += txt(x0 + w / 2, y0 + A + 60, "în orice moment, suma celor trei tensiuni este zero", size=12)
    cx, cy = 570, 140
    b += f'<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{GRAY}" stroke-width="1" stroke-dasharray="3 3"/>'
    b += phasor(cx, cy, 75, 90, L1, "U1 (L1)") + phasor(cx, cy, 75, -30, L2, "U2 (L2)") + phasor(cx, cy, 75, 210, L3, "U3 (L3)")
    b += angle_arc(cx, cy, 30, -30, 90, "currentColor", "120°", 44)
    b += txt(cx, cy + 115, "steaua tensiunilor de fază", size=12, weight="bold")
    return svg(W, H, b, "Sistemul trifazat: trei tensiuni decalate cu 120°")

# 12. Conexiunea stea
def _winding_v(x, y1, y2):
    n = 3; r = (y2 - y1) / (2 * n)
    d = f"M{x},{y1}"
    for k in range(n): d += f" a{r},{r} 0 0 1 0,{2*r}"
    return f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2"/>'

def fig_stea():
    W, H = 680, 300
    b = ""
    # bare L1 L2 L3 N
    for i, (lab, col, y) in enumerate([("L1", L1, 40), ("L2", L2, 70), ("L3", L3, 100), ("N", NC, 130)]):
        b += line(40, y, 640, y, col, 3) + txt(28, y + 4, lab, anchor="end", color=col, weight="bold")
    # receptor stea: trei impedanțe de la fiecare fază la punctul neutru
    px, py = 440, 245  # punct neutru
    for i, (x, y, col, lab) in enumerate([(330, 40, L1, "Z1"), (440, 70, L2, "Z2"), (550, 100, L3, "Z3")]):
        b += dot(x, y, 4, col)
        b += line(x, y, x, 150) + sym_R_v(x, 185, lab) + line(x, 220, x, 245) if False else ""
        b += line(x, y, x, 155) + f'<rect x="{x-8}" y="155" width="16" height="50" fill="none" stroke="currentColor" stroke-width="2"/>' + txt(x + 14, 184, lab, anchor="start", weight="bold")
        b += line(x, 205, x, py) + line(x, py, px, py)
    b += dot(px, py, 5) + txt(px - 12, py + 24, "punct neutru (nul) al receptorului", size=11, anchor="end")
    b += line(px, py, px, 282) + line(px, 282, 610, 282) + line(610, 282, 610, 130) + dot(610, 130, 4, NC)
    b += txt(600, 276, "conductorul N", anchor="end", size=11, color=NC)
    # etichete tensiuni
    b += arrow(300, 46, 300, 124, RED, 1.5, 6) + txt(292, 90, "UF = 230 V", anchor="end", color=RED, weight="bold", size=12) + txt(292, 104, "(fază – neutru)", anchor="end", size=10)
    b += arrow(200, 46, 200, 94, RED, 1.5, 6) + txt(192, 66, "UL = 400 V", anchor="end", color=RED, weight="bold", size=12) + txt(192, 80, "(între două faze)", anchor="end", size=10)
    b += arrow(345, 136, 345, 152, BLUE, 1.5, 6) + txt(352, 148, "IL = IF", anchor="start", color=BLUE, weight="bold", size=12)
    b += txt(590, 175, "STEA:", anchor="start", weight="bold", size=12) + txt(590, 191, "UL = √3 · UF", anchor="start", weight="bold", size=12) + txt(590, 207, "IL = IF", anchor="start", weight="bold", size=12)
    b += txt(340, 24, "receptor trifazat în STEA (Y)", weight="bold", size=13, anchor="start")
    return svg(W, H, b, "Receptor trifazat în conexiune stea")

def sym_R_v(x, y, label):  # placeholder, neutilizat
    return ""

# 13. Conexiunea triunghi
def fig_triunghi():
    W, H = 680, 305
    b = ""
    for lab, col, y in [("L1", L1, 40), ("L2", L2, 70), ("L3", L3, 100)]:
        b += line(40, y, 640, y, col, 3) + txt(28, y + 4, lab, anchor="end", color=col, weight="bold")
    # vârfurile triunghiului
    A_ = (380, 150); B_ = (300, 270); C_ = (460, 270)
    b += line(380, 40, 380, 150) + dot(380, 40, 4, L1)
    b += line(300, 70, 300, 270) + dot(300, 70, 4, L2)
    b += line(460, 100, 460, 270) + dot(460, 100, 4, L3)
    # laturi cu rezistoare (dreptunghi rotit)
    def side(p, q, lab):
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        if ang > 90 or ang < -90: ang -= 180
        s = line(p[0], p[1], q[0], q[1])
        s += f'<rect x="{mx-25}" y="{my-8}" width="50" height="16" fill="var(--bg,#fff)" stroke="currentColor" stroke-width="2" transform="rotate({ang:.1f} {mx} {my})"/>'
        s += txt(mx, my + 4, lab, size=11, weight="bold", extra=f'transform="rotate({ang:.1f} {mx} {my})"')
        return s
    b += side(A_, B_, "Z12") + side(A_, C_, "Z31") + side(B_, C_, "Z23")
    b += dot(*A_, 4) + dot(*B_, 4) + dot(*C_, 4)
    b += arrow(200, 46, 200, 94, RED, 1.5, 6) + txt(192, 66, "UL = UF = 400 V", anchor="end", color=RED, weight="bold", size=12) + txt(192, 80, "(fiecare Z primește 400 V)", anchor="end", size=10)
    b += arrow(395, 110, 395, 135, BLUE, 1.5, 6) + txt(402, 126, "IL", anchor="start", color=BLUE, weight="bold", size=12)
    b += arrow(395, 288, 435, 288, BLUE, 1.5, 6) + txt(388, 292, "IF", anchor="end", color=BLUE, weight="bold", size=12)
    b += txt(520, 200, "triunghi: UL = UF", anchor="start", weight="bold", size=12) + txt(520, 216, "IL = √3 · IF", anchor="start", weight="bold", size=12) + txt(520, 236, "fără conductor neutru", anchor="start", size=11)
    b += txt(340, 24, "receptor trifazat în TRIUNGHI (Δ)", weight="bold", size=13, anchor="start")
    return svg(W, H, b, "Receptor trifazat în conexiune triunghi")

# 14. Cutia de borne a motorului: punți Y și Δ
def fig_borne():
    W, H = 660, 250
    b = ""
    def box(ox, title, mode):
        s = f'<rect x="{ox}" y="50" width="260" height="150" rx="6" fill="none" stroke="currentColor" stroke-width="2"/>'
        s += txt(ox + 130, 36, title, weight="bold", size=12)
        top = ["U1", "V1", "W1"]; bot = ["W2", "U2", "V2"]
        xs = [ox + 55, ox + 130, ox + 205]
        for i, x in enumerate(xs):
            s += txt(x - 14, 94, top[i], size=11, weight="bold", anchor="end")
            s += txt(x, 184, bot[i], size=11, weight="bold")
            col = [L1, L2, L3][i]
            s += line(x, 81, x, 58, col, 3)
            s += txt(x + 6, 62, ["L1", "L2", "L3"][i], anchor="start", size=10, color=col)
        if mode == "Y":
            s += f'<rect x="{xs[0]-12}" y="154" width="{xs[2]-xs[0]+24}" height="12" rx="3" fill="{ORANGE}" opacity="0.8"/>'
            s += txt(ox + 130, 215, "punte orizontală jos: W2–U2–V2 unite = punct neutru", size=11)
        else:
            for x in xs:
                s += f'<rect x="{x-6}" y="90" width="12" height="70" rx="3" fill="{ORANGE}" opacity="0.8"/>'
            s += txt(ox + 130, 215, "punți verticale: U1–W2, V1–U2, W1–V2", size=11)
        # bornele cerc peste punte
        for i, x in enumerate(xs):
            s += f'<circle cx="{x}" cy="90" r="9" fill="none" stroke="currentColor" stroke-width="2"/>' + f'<circle cx="{x}" cy="160" r="9" fill="none" stroke="currentColor" stroke-width="2"/>'
        return s
    b += box(40, "STEA (Y): motor 230 Δ / 400 Y pe rețea 400 V", "Y")
    b += box(360, "TRIUNGHI (Δ): motor 400 Δ / 690 Y pe rețea 400 V", "D")
    return svg(W, H, b, "Cutia de borne a motorului trifazat: punțile pentru stea și triunghi")

# 15. Neutrul întrerupt la receptor dezechilibrat
def fig_neutru():
    W, H = 660, 262
    b = ""
    for lab, col, y in [("L1", L1, 40), ("L2", L2, 70), ("L3", L3, 100), ("N", NC, 130)]:
        b += line(40, y, 620, y, col, 3) + txt(28, y + 4, lab, anchor="end", color=col, weight="bold")
    px, py = 330, 225
    for x, y, col, lab, w in [(230, 40, L1, "bec 100 W", 14), (330, 70, L2, "reșou 2000 W", 26), (430, 100, L3, "bec 60 W", 12)]:
        b += dot(x, y, 4, col) + line(x, y, x, 150) + f'<rect x="{x-w/2}" y="150" width="{w}" height="40" fill="none" stroke="currentColor" stroke-width="2"/>' + txt(x + w/2 + 5, 174, lab, size=10, anchor="start") + line(x, 190, x, py) + line(x, py, px, py)
    b += dot(px, py, 5)
    # N întrerupt
    b += line(px, py, 560, py) + line(560, py, 560, 160) + line(560, 130, 560, 145) + dot(560, 130, 4, NC)
    b += f'<line x1="560" y1="145" x2="575" y2="160" stroke="{RED}" stroke-width="3"/>' + txt(590, 155, "N întrerupt!", anchor="start", color=RED, weight="bold", size=12)
    b += txt(60, 250, "consumatori diferiți pe cele trei faze = receptor DEZECHILIBRAT", size=11, anchor="start")
    b += txt(230, 22, "fără N, punctul neutru „alunecă”: becul mic poate primi până la ~400 V și arde", size=11, color=RED, weight="bold", anchor="start")
    return svg(W, H, b, "Întreruperea neutrului la un receptor dezechilibrat în stea")

FIGS = {
    "sinusoida": fig_sinusoida, "generator": fig_generator, "defazaj": fig_defazaj,
    "R": lambda: fig_element("R"), "L": lambda: fig_element("L"), "C": lambda: fig_element("C"),
    "reactante": fig_reactante, "rl": fig_rl, "puteri": fig_puteri, "compensare": fig_compensare,
    "trifazat": fig_trifazat, "stea": fig_stea, "triunghi": fig_triunghi, "borne": fig_borne, "neutru": fig_neutru,
}

if __name__ == "__main__":
    import os
    os.makedirs("svg", exist_ok=True)
    for k, f in FIGS.items():
        with open(f"svg/{k}.svg", "w", encoding="utf-8") as fh:
            fh.write(f().replace("currentColor", "#222").replace("var(--bg,#fff)", "#fff"))
    print("ok", len(FIGS))
