# -*- coding: utf-8 -*-
"""Mică bibliotecă pentru scheme electrice SVG editabile în Inkscape.
Fiecare aparat = un <g> cu simbolul și etichetele lui, pe stratul „Aparate”;
conductoarele pe stratul „Conductoare”; textele explicative pe stratul „Text”."""
import html

FONT = "font-family='DejaVu Sans, Arial, sans-serif'"
K = "stroke='#111' stroke-width='1.6' fill='none' stroke-linecap='round' stroke-linejoin='round'"
KT = "stroke='#111' stroke-width='1.1' fill='none' stroke-linecap='round' stroke-linejoin='round'"
KD = "stroke='#111' stroke-width='1.2' fill='none' stroke-dasharray='5 4'"
KB = "stroke='#1d5fa8' stroke-width='1.6' fill='none' stroke-linecap='round'"   # semnal / comandă
KR = "stroke='#b3261e' stroke-width='1.6' fill='none' stroke-linecap='round'"   # roșu (avarie / incendiu)
KF = K.replace("fill='none'", "fill='#fff'")
KDR = KD.replace('#111', '#b3261e')
KFB = K.replace("fill='none'", "fill='#111'")
KG = "stroke='#2e7d32' stroke-width='1.6' fill='none' stroke-linecap='round'"   # verde (aer / proces)

def esc(s): return html.escape(str(s), quote=True)

def lab(x, y, t, anchor="middle", size=11, cls="", weight="normal", fill="#111", rot=None):
    tr = f" transform='rotate({rot} {x} {y})'" if rot is not None else ""
    return (f"<text x='{x}' y='{y}' text-anchor='{anchor}' font-size='{size}' font-weight='{weight}' "
            f"fill='{fill}' {FONT} dominant-baseline='central'{tr}>{esc(t)}</text>")

def ap(name, *parts):
    """un aparat: grup cu id/label Inkscape"""
    return f"<g id='{esc(name)}' inkscape:label='{esc(name)}'>" + "".join(parts) + "</g>"

def wire(d, style=K): return f"<path d='{d}' {style}/>"
def line(x1, y1, x2, y2, style=K): return f"<path d='M{x1} {y1}L{x2} {y2}' {style}/>"
def dot(x, y, r=2.6): return f"<circle cx='{x}' cy='{y}' r='{r}' fill='#111'/>"
def term(x, y, r=3.2): return f"<circle cx='{x}' cy='{y}' r='{r}' {KF}/>"
def rect(x, y, w, h, style=K, rx=0): return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' {style}/>"
def arrow(x1, y1, x2, y2, style=KB, head=6):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - head * math.cos(a - 0.45); hy1 = y2 - head * math.sin(a - 0.45)
    hx2 = x2 - head * math.cos(a + 0.45); hy2 = y2 - head * math.sin(a + 0.45)
    return f"<path d='M{x1} {y1}L{x2} {y2}' {style}/><path d='M{hx1:.1f} {hy1:.1f}L{x2} {y2}L{hx2:.1f} {hy2:.1f}' {style}/>"

# ---------- simboluri (IEC 60617), verticale, curentul curge de sus în jos ----------
def s_fuse(x, y, h=28, w=10):
    """siguranță fuzibilă: dreptunghi cu conductorul prin el"""
    return (rect(x - w / 2, y, w, h) + line(x, y - 6, x, y + h + 6))

def s_contact_no(x, y, h=30):
    """contact normal deschis (contactor): de sus jos, cu contactul oblic"""
    return (line(x, y - 6, x, y) + line(x, y, x - 9, y + h - 6) + line(x, y + h, x, y + h + 6))

def s_disconnector(x, y, h=30):
    """separator (întrerupător-separator): contact oblic cu bară la capăt"""
    return (line(x, y - 6, x, y) + line(x, y, x - 9, y + h - 6) + line(x - 5, y - 1, x + 5, y - 1) + line(x, y + h, x, y + h + 6))

def s_breaker(x, y, h=30):
    """întrerupător automat (disjunctor): contact oblic + cruce"""
    return (line(x, y - 6, x, y) + line(x, y, x - 9, y + h - 6) + f"<path d='M{x-4} {y-4}L{x+4} {y+4}M{x-4} {y+4}L{x+4} {y-4}' {K}/>" + line(x, y + h, x, y + h + 6))

def s_thermal(x, y, h=26):
    """releu termic (element termic): dreptunghi cu linia frântă"""
    return (line(x, y - 6, x, y) + rect(x - 7, y, 14, h) +
            f"<path d='M{x} {y}L{x} {y+6}L{x+4} {y+6}L{x+4} {y+h-6}L{x} {y+h-6}L{x} {y+h}' {K}/>" + line(x, y + h, x, y + h + 6))

def s_motor(x, y, r=18, txt="M", sub="3~"):
    return (f"<circle cx='{x}' cy='{y}' r='{r}' {KF}/>" + lab(x, y - 4, txt, size=13, weight="bold") + lab(x, y + 9, sub, size=9))

def s_ptc(x, y):
    """termistor PTC: dreptunghi cu -t° """
    return rect(x - 12, y - 6, 24, 12) + lab(x, y, "ϑ", size=9) + f"<path d='M{x-12} {y+6}L{x-4} {y-8}' {KT}/>"

def s_converter(x, y, w=64, h=54, t1="~", t2="~"):
    """convertizor de frecvență: dreptunghi cu diagonala, ~ sus-stânga, ~ jos-dreapta (f variabil)"""
    return (rect(x - w / 2, y, w, h, style=K) + line(x - w / 2, y + h, x + w / 2, y) +
            lab(x - w / 4 + 2, y + h / 4 + 2, t1, size=14) + lab(x + w / 4 - 2, y + 3 * h / 4 - 2, t2, size=14) +
            lab(x + w / 4 - 2, y + 3 * h / 4 + 10, "f var.", size=7))

def s_filter(x, y, w=44, h=30, t="≈"):
    return rect(x - w / 2, y, w, h) + lab(x, y + h / 2, t, size=14)

def s_choke(x, y, h=30):
    """bobină (reactanță): 3 semicercuri pe verticală"""
    r = h / 6
    d = f"M{x} {y-6}L{x} {y}" + "".join(f"A{r} {r} 0 0 1 {x} {y + 2*r*(i+1)}" for i in range(3)) + f"L{x} {y+h+6}"
    return f"<path d='{d}' {K}/>"

def s_ground(x, y):
    return f"<path d='M{x} {y}L{x} {y+8}M{x-8} {y+8}L{x+8} {y+8}M{x-5} {y+12}L{x+5} {y+12}M{x-2} {y+16}L{x+2} {y+16}' {K}/>"

def s_rcd(x, y, h=30):
    """dispozitiv de protecție diferențială: contact + elipsă (sumator) """
    return (line(x, y - 6, x, y) + line(x, y, x - 9, y + h - 6) + line(x, y + h, x, y + h + 6) +
            f"<ellipse cx='{x+9}' cy='{y+h/2}' rx='5' ry='9' {KT}/>" + line(x - 4, y + h - 8, x + 4, y + h / 2, KT))

def s_fan(x, y, r=16):
    """ventilator (simbol în canal): cerc cu două pale"""
    return (f"<circle cx='{x}' cy='{y}' r='{r}' {KF}/>" +
            f"<path d='M{x} {y}Q{x-r*0.9} {y-r*0.9} {x-r*0.5} {y-r*0.05}Q{x-r*0.2} {y+r*0.3} {x} {y}Z' {KFB}/>" +
            f"<path d='M{x} {y}Q{x+r*0.9} {y+r*0.9} {x+r*0.5} {y+r*0.05}Q{x+r*0.2} {y-r*0.3} {x} {y}Z' {KFB}/>")

def s_sensor(x, y, txt="p"):
    """traductor: cerc cu literă (P = presiune, T = temperatură, CO2)"""
    return f"<circle cx='{x}' cy='{y}' r='11' {KF}/>" + lab(x, y, txt, size=9)

def s_coil(x, y, w=26, h=14, t=""):
    """bobină releu/contactor: dreptunghi orizontal"""
    return rect(x - w / 2, y - h / 2, w, h) + lab(x, y, t, size=8)

def s_pushbutton(x, y, nc=False):
    """buton: contact NO (apasă-închide) sau NC; orizontal, curent de la stânga la dreapta"""
    if nc:
        return (line(x - 14, y, x - 4, y) + line(x - 4, y, x + 6, y - 9) + line(x + 4, y, x + 14, y) +
                line(x + 1, y - 5, x + 1, y - 14) + f"<path d='M{x-4} {y-14}L{x+6} {y-14}' {K}/>" + line(x + 1, y - 16, x + 1, y - 14))
    return (line(x - 14, y, x - 4, y) + line(x - 4, y, x + 6, y - 9) + line(x + 4, y, x + 14, y) +
            line(x + 1, y - 5, x + 1, y - 14) + f"<path d='M{x-4} {y-14}L{x+6} {y-14}' {K}/>")

def s_contact_h(x, y, nc=False, label=""):
    """contact orizontal (releu): NO sau NC"""
    if nc:
        s = line(x - 14, y, x - 4, y) + line(x - 4, y, x + 6, y - 9) + line(x + 4, y, x + 14, y) + line(x + 4, y - 9, x + 4, y)
    else:
        s = line(x - 14, y, x - 4, y) + line(x - 4, y, x + 6, y - 9) + line(x + 4, y, x + 14, y)
    return s + (lab(x, y - 16, label, size=9) if label else "")

def doc(w, h, aparate, conductoare, text=(), title=""):
    """asamblează documentul SVG cu straturi Inkscape"""
    head = (f"<svg xmlns='http://www.w3.org/2000/svg' xmlns:inkscape='http://www.inkscape.org/namespaces/inkscape' "
            f"xmlns:sodipodi='http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>"
            f"<title>{esc(title)}</title><rect width='{w}' height='{h}' fill='#fff'/>")
    L = lambda name, items: f"<g inkscape:groupmode='layer' inkscape:label='{name}' id='layer_{name}'>" + "".join(items) + "</g>"
    return head + L("Conductoare", conductoare) + L("Aparate", aparate) + L("Text", text) + "</svg>"

def save(path, s):
    open(path, "w", encoding="utf-8").write(s)
