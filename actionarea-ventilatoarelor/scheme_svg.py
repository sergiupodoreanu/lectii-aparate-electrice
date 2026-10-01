# -*- coding: utf-8 -*-
"""Scheme pentru lecția „Acționarea ventilatoarelor cu convertizor de frecvență”. Rulează: python3 scheme_svg.py"""
import math, os
from svglib import *

OUT = "svg"; os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ 01 curbe ventilator + instalație
def curbe_ventilator():
    W, H = 760, 400
    ox, oy, gw, gh = 70, 340, 300, 270          # grafic stânga
    ox2 = 430
    A, C = [], []
    def axes(ox, t):
        s = arrow(ox, oy, ox, oy - gh - 10, K) + arrow(ox, oy, ox + gw + 10, oy, K)
        s += lab(ox + gw / 2, oy + 24, "debit de aer Q", size=11) + lab(ox - 40, oy - gh - 4, "Δp", size=11)
        s += lab(ox + gw / 2, oy - gh - 22, t, size=12, weight="bold")
        return s
    def fan(ox, n=1.0, style=K):
        # caracteristica ventilatorului: Δp = p0·n² − k·Q² (parabolă descrescătoare)
        pts = [(ox + q, oy - (0.95 * gh * n * n - 0.85 * gh * (q / gw) ** 2 * n * n)) for q in range(0, int(gw * 0.98))]
        return f"<path d='M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f"' {style}/>"
    def inst(ox, k=1.0, style=KG):
        pts = [(ox + q, oy - min(gh, k * gh * 0.9 * (q / gw) ** 2)) for q in range(0, gw)]
        pts = [p for p in pts if p[1] > oy - gh]
        return f"<path d='M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f"' {style}/>"
    # stânga: reglare cu clapetă (instalația se schimbă, ventilatorul nu)
    C += [axes(ox, "A. Reglare cu clapetă (turație constantă)")]
    C += [fan(ox), inst(ox, 1.0), inst(ox, 2.6, KR)]
    # puncte de funcționare
    def inter(k, n=1.0):
        for q in range(0, gw):
            pf = 0.95 * gh * n * n - 0.85 * gh * (q / gw) ** 2 * n * n
            pi = k * gh * 0.9 * (q / gw) ** 2
            if pi >= pf: return ox + q, oy - pf
        return None
    p1 = inter(1.0); p2 = inter(2.6)
    A += [ap("Punct 1", dot(*p1, 4), lab(p1[0] + 10, p1[1] + 12, "1: clapetă deschisă, Q = 100 %", "start", 10)),
          ap("Punct 2", dot(*p2, 4), lab(p2[0] + 10, p2[1] - 12, "2: clapetă închisă parțial, Q = 60 %", "start", 10)),
          ap("Etichete A", lab(ox + 120, oy - 258, "ventilator n = 100 %", "start", 10),
             lab(ox + 210, oy - 60, "instalație, clapetă deschisă", "start", 10, fill="#2e7d32"),
             lab(ox + 150, oy - 245, "instalație, clapetă strânsă", "start", 10, fill="#b3261e"),
             lab(ox + 50, oy - 140, "Δp irosit pe clapetă", "start", 9, fill="#b3261e"))]
    # săgeata Δp irosit
    C += [f"<path d='M{p2[0]:.1f} {p2[1]:.1f}L{p2[0]:.1f} {oy - 0.9*gh*(0.6)**2:.1f}' {KDR}/>"]
    # dreapta: reglare turație (ventilatorul se schimbă, instalația nu)
    ox = ox2
    C += [axes(ox, "B. Reglare de turație (convertizor)")]
    C += [fan(ox), fan(ox, 0.6, KD), inst(ox, 1.0)]
    p1 = inter(1.0); p3 = inter(1.0, 0.6)
    A += [ap("Punct 1b", dot(*p1, 4), lab(p1[0] + 10, p1[1] + 12, "1: n = 100 %, Q = 100 %", "start", 10)),
          ap("Punct 3", dot(*p3, 4), lab(p3[0] + 10, p3[1] - 12, "3: n = 60 %, Q = 60 %", "start", 10)),
          ap("Etichete B", lab(ox + 120, oy - 258, "ventilator n = 100 %", "start", 10),
             lab(ox + 120, oy - 112, "ventilator n = 60 %", "start", 10),
             lab(ox + 210, oy - 60, "instalație (neschimbată)", "start", 10, fill="#2e7d32"),
             lab(ox + 10, oy - 275, "P₃ ≈ 0,6³ · P₁ ≈ 22 % din P₁", "start", 10, weight="bold"))]
    save(f"{OUT}/01_curbe_ventilator_instalatie.svg", doc(W, H, A, C, title="Curba ventilatorului și a instalației: reglare cu clapetă și cu turație"))

# ------------------------------------------------------------------ 02 legile de similitudine
def legi_similitudine():
    W, H = 720, 400
    ox, oy, gw, gh = 80, 340, 560, 280
    A, C = [], []
    C += [arrow(ox, oy, ox, oy - gh - 10, K), arrow(ox, oy, ox + gw + 10, oy, K)]
    for i in range(0, 11):
        x = ox + gw * i / 10
        C += [line(x, oy, x, oy + 5), lab(x, oy + 16, f"{i*10}", size=9)]
    for i in range(0, 11, 2):
        y = oy - gh * i / 10
        C += [line(ox - 5, y, ox, y), lab(ox - 18, y, f"{i*10}", size=9)]
    C += [lab(ox + gw / 2, oy + 34, "turația n (% din nominal)", size=11), lab(ox - 40, oy - gh - 4, "%", size=11)]
    def curve(p, style):
        pts = [(ox + gw * t / 100, oy - gh * (t / 100) ** p) for t in range(0, 101)]
        return f"<path d='M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f"' {style}/>"
    C += [curve(1, KG), curve(2, KB), curve(3, KR)]
    A += [ap("Legenda", lab(ox + 300, oy - 262, "Q ~ n   (debit)", "start", 11, fill="#2e7d32", weight="bold"),
             lab(ox + 300, oy - 244, "Δp ~ n²   (presiune)", "start", 11, fill="#1d5fa8", weight="bold"),
             lab(ox + 300, oy - 226, "P ~ n³   (putere absorbită)", "start", 11, fill="#b3261e", weight="bold"),
             rect(ox + 290, oy - 275, 240, 62, KT))]
    # punct exemplu n = 80 %
    x80 = ox + gw * 0.8
    C += [f"<path d='M{x80} {oy}L{x80} {oy-gh*0.8}' {KD}/>"]
    A += [ap("Exemplu 80%", dot(x80, oy - gh * 0.8, 4), dot(x80, oy - gh * 0.64, 4), dot(x80, oy - gh * 0.512, 4),
             lab(x80 + 8, oy - gh * 0.8 + 2, "Q = 80 %", "start", 10, fill="#2e7d32"),
             lab(x80 + 8, oy - gh * 0.64 + 2, "Δp = 64 %", "start", 10, fill="#1d5fa8"),
             lab(x80 + 8, oy - gh * 0.512 + 2, "P = 51 %", "start", 10, fill="#b3261e"))]
    x50 = ox + gw * 0.5
    C += [f"<path d='M{x50} {oy}L{x50} {oy-gh*0.5}' {KD}/>"]
    A += [ap("Exemplu 50%", dot(x50, oy - gh * 0.5, 4), dot(x50, oy - gh * 0.25, 4), dot(x50, oy - gh * 0.125, 4),
             lab(x50 + 8, oy - gh * 0.5 + 2, "Q = 50 %", "start", 10, fill="#2e7d32"),
             lab(x50 + 8, oy - gh * 0.25 + 2, "Δp = 25 %", "start", 10, fill="#1d5fa8"),
             lab(x50 + 8, oy - gh * 0.125 + 2, "P = 12,5 %", "start", 10, fill="#b3261e"))]
    save(f"{OUT}/02_legile_de_similitudine.svg", doc(W, H, A, C, title="Legile de similitudine ale ventilatoarelor"))

# ------------------------------------------------------------------ 03 comparație putere absorbită: clapetă / IGV / CF
def comparatie_putere():
    W, H = 720, 400
    ox, oy, gw, gh = 80, 340, 560, 280
    A, C = [], []
    C += [arrow(ox, oy, ox, oy - gh - 10, K), arrow(ox, oy, ox + gw + 10, oy, K)]
    for i in range(0, 11):
        x = ox + gw * i / 10; C += [line(x, oy, x, oy + 5), lab(x, oy + 16, f"{i*10}", size=9)]
    for i in range(0, 11, 2):
        y = oy - gh * i / 10; C += [line(ox - 5, y, ox, y), lab(ox - 18, y, f"{i*10}", size=9)]
    C += [lab(ox + gw / 2, oy + 34, "debit de aer Q (% din nominal)", size=11), lab(ox - 40, oy - gh - 6, "P %", size=11)]
    # curbe tipice (după Danfoss, Projektierungshandbuch FC 102, fig. 2.12; valori orientative)
    def poly(vals, style):
        pts = [(ox + gw * q / 100, oy - gh * v / 100) for q, v in vals]
        return f"<path d='M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f"' {style}/>"
    clapeta = [(0, 55), (20, 66), (40, 77), (60, 86), (80, 94), (100, 100)]
    igv = [(0, 25), (20, 33), (40, 44), (60, 58), (80, 77), (100, 100)]
    cf = [(q, max(3, (q / 100) ** 3 * 100 + 3)) for q in range(0, 101, 10)]
    C += [poly(clapeta, KR), poly(igv, KB), poly(cf, KG)]
    A += [ap("Legenda", rect(ox + 20, oy - 275, 250, 62, KT),
             lab(ox + 30, oy - 262, "clapetă de refulare", "start", 11, fill="#b3261e", weight="bold"),
             lab(ox + 30, oy - 244, "clapete de aspirație cu palete (IGV)", "start", 11, fill="#1d5fa8", weight="bold"),
             lab(ox + 30, oy - 226, "convertizor de frecvență", "start", 11, fill="#2e7d32", weight="bold"))]
    x60 = ox + gw * 0.6
    C += [f"<path d='M{x60} {oy}L{x60} {oy-gh*0.86}' {KD}/>"]
    A += [ap("La 60%", dot(x60, oy - gh * 0.86, 4), dot(x60, oy - gh * 0.58, 4), dot(x60, oy - gh * 0.246, 4),
             lab(x60 + 8, oy - gh * 0.86 - 10, "clapetă: 86 %", "start", 10, fill="#b3261e"),
             lab(x60 + 8, oy - gh * 0.58 - 10, "IGV: 58 %", "start", 10, fill="#1d5fa8"),
             lab(x60 + 8, oy - gh * 0.246 - 10, "CF: ≈ 25 %", "start", 10, fill="#2e7d32"),
             lab(x60, oy - gh - 8, "Q = 60 %", size=10, weight="bold"))]
    save(f"{OUT}/03_comparatie_putere_absorbita.svg", doc(W, H, A, C, title="Puterea absorbită la debit redus: clapetă, IGV, convertizor"))

# ------------------------------------------------------------------ 04 metodele de reglare a turației (blocuri)
def metode_reglare():
    W, H = 900, 300
    A, C, T = [], [], []
    cols = [("A. Transformator în trepte", "trafo"), ("B. Regulator electronic de tensiune", "triac"),
            ("C. Convertizor de frecvență", "cf"), ("D. Ventilator EC", "ec")]
    for i, (title, kind) in enumerate(cols):
        x0 = 20 + i * 220
        T += [lab(x0 + 100, 22, title, size=11, weight="bold")]
        # rețea
        C += [line(x0 + 100, 40, x0 + 100, 70)]
        T += [lab(x0 + 100, 48, "3~ 400 V, 50 Hz" if kind != "triac" else "1~ 230 V, 50 Hz", size=9)]
        if kind == "trafo":
            A += [ap("Transformator în trepte", rect(x0 + 60, 70, 80, 60), lab(x0 + 100, 88, "T", size=12, weight="bold"),
                     lab(x0 + 100, 104, "5 trepte", size=9), lab(x0 + 100, 118, "80…230 V", size=9),
                     f"<path d='M{x0+130} {80}L{x0+130} {120}M{x0+124} {84}L{x0+130} {80}L{x0+136} {84}' {KT}/>")]
            T += [lab(x0 + 100, 150, "U scade → n scade (alunecare mare)", size=9), lab(x0 + 100, 164, "f = 50 Hz constant", size=9),
                  lab(x0 + 100, 178, "pierderi mari în motor la n mic", size=9, fill="#b3261e")]
        elif kind == "triac":
            A += [ap("Regulator electronic", rect(x0 + 60, 70, 80, 60), lab(x0 + 100, 92, "U var.", size=11, weight="bold"),
                     f"<path d='M{x0+75} {112}L{x0+85} {112}L{x0+90} {104}L{x0+96} {120}L{x0+101} {104}L{x0+106} {120}L{x0+111} {112}L{x0+125} {112}' {KT}/>")]
            T += [lab(x0 + 100, 150, "tăiere de fază (triac) – U eficace scade", size=9), lab(x0 + 100, 164, "numai motoare mici, comandabile în tensiune", size=9),
                  lab(x0 + 100, 178, "zgomot magnetic, armonici", size=9, fill="#b3261e")]
        elif kind == "cf":
            A += [ap("Convertizor de frecvență", s_converter(x0 + 100, 72, 80, 58), lab(x0 + 100, 145, "U/f = ct. (curbă pătratică)", size=9))]
            T += [lab(x0 + 100, 164, "f și U variabile, 0…50 Hz", size=9), lab(x0 + 100, 178, "orice motor asincron standard", size=9, fill="#2e7d32")]
        else:
            A += [ap("Ventilator EC", rect(x0 + 60, 70, 80, 60), lab(x0 + 100, 86, "redresor +", size=9), lab(x0 + 100, 98, "invertor +", size=9),
                     lab(x0 + 100, 110, "motor PM", size=9), lab(x0 + 100, 122, "integrate", size=9))]
            T += [lab(x0 + 100, 150, "comandă 0–10 V / PWM / Modbus", size=9), lab(x0 + 100, 164, "randament maxim, fără cablu ecranat", size=9, fill="#2e7d32"),
                  lab(x0 + 100, 178, "motorul și electronica formează un tot", size=9)]
        # motor
        C += [line(x0 + 100, 130, x0 + 100, 200)]
        A += [ap(f"Motor {kind}", s_motor(x0 + 100, 218, 18, "M", "3~" if kind != "ec" else "EC"), s_fan(x0 + 100, 268, 14))]
        C += [line(x0 + 100, 236, x0 + 100, 254)]
    save(f"{OUT}/04_metode_reglare_turatie.svg", doc(W, H, A, C, T, title="Metode de reglare a turației ventilatoarelor"))

# ------------------------------------------------------------------ 05 schema monofilară de forță
def monofilara_forta():
    W, H = 900, 560
    x = 150
    A, C, T = [], [], []
    C += [line(x, 30, x, 60)]
    T += [lab(x + 12, 36, "3~ 400 V, 50 Hz, TN-S", "start", 10), lab(x + 12, 50, "din tabloul de forță al CTA", "start", 9)]
    A += [ap("Q1 separator cu siguranțe", s_disconnector(x, 66), s_fuse(x, 108, 26), lab(x + 20, 80, "Q1", "start", 11, weight="bold"),
             lab(x + 20, 96, "separator blocabil cu lacăt", "start", 9), lab(x + 20, 121, "F1 gG 25 A (după manualul CF)", "start", 9))]
    C += [line(x, 140, x, 170)]
    A += [ap("K1 contactor de rețea (opțional)", s_contact_no(x, 176), lab(x + 20, 190, "K1 (opțional) AC-1, ≥ curentul de intrare al CF", "start", 9),
             lab(x + 20, 203, "numai pentru separare / oprire de urgență, nu pentru start-stop", "start", 8))]
    C += [line(x, 212, x, 240)]
    A += [ap("L1 bobină de rețea", s_choke(x, 246, 30), lab(x + 20, 262, "L1 bobină de rețea (armonici) sau filtru CEM", "start", 9))]
    C += [line(x, 282, x, 310)]
    A += [ap("U1 convertizor de frecvență", s_converter(x, 310, 70, 60), lab(x + 45, 325, "U1 convertizor 7,5 kW, IP20 în tablou", "start", 10, weight="bold"),
             lab(x + 45, 340, "curbă U/f pătratică (VT), PID intern", "start", 9), lab(x + 45, 354, "intrări: 0–10 V, 4–20 mA, DI, PTC, STO", "start", 9))]
    C += [line(x, 370, x, 400)]
    A += [ap("Z1 filtru de ieșire", s_filter(x, 400, 46, 30, "du/dt"), lab(x + 35, 415, "Z1 filtru du/dt (cablu > 50 m) sau filtru sinus", "start", 9),
             lab(x + 35, 428, "(mai multe motoare, motor cu rotor exterior, cablu neecranat)", "start", 8))]
    C += [line(x, 436, x, 470), f"<path d='M{x-10} 440L{x-10} 500' {KT} stroke-dasharray='3 3'/>", f"<path d='M{x+10} 440L{x+10} 500' {KT} stroke-dasharray='3 3'/>"]
    T += [lab(x + 35, 460, "cablu de motor ecranat 4G2,5 mm², ecran la 360° la ambele capete", "start", 9),
          lab(x + 35, 473, "L ≤ 50 m (după manual); nu în același jgheab cu cablurile de semnal", "start", 8)]
    A += [ap("Q2 separator de service la ventilator", s_disconnector(x, 476), lab(x + 20, 492, "Q2 separator de service lângă ventilator, cu contact", "start", 9),
             lab(x + 20, 504, "auxiliar cu deschidere anticipată → oprire CF înainte de separare", "start", 8))]
    C += [line(x, 512, x, 522)]
    A += [ap("M1 motor ventilator", s_motor(x, 540, 18), s_ptc(x + 45, 540), line(x + 18, 540, x + 33, 540, KT),
             lab(x + 70, 534, "M1 7,5 kW, 14,8 A, 1460 min⁻¹, IE3", "start", 10, weight="bold"),
             lab(x + 70, 548, "cu termistori PTC în bobinaj (bornele T1-T2 → CF)", "start", 9))]
    # chenar tablou
    C += [f"<rect x='40' y='150' width='520' height='300' {KD}/>", lab(60, 165, "tablou electric TE-CTA", "start", 9)]
    # legendă dreapta
    T += [rect(600, 40, 280, 250, KT), lab(740, 58, "Reguli de amplasare", size=11, weight="bold"),
          lab(612, 82, "1. Separator + siguranțe înaintea CF (Q1, F1).", "start", 9),
          lab(612, 100, "2. Contactorul K1 este opțional; nu se pornește", "start", 9), lab(612, 112, "    și nu se oprește motorul din K1.", "start", 9),
          lab(612, 130, "3. Nimic nu se deschide între CF și motor în", "start", 9), lab(612, 142, "    mers; Q2 numai cu contact anticipat → stop CF.", "start", 9),
          lab(612, 160, "4. Cablu de motor ecranat, ecran la 360°.", "start", 9),
          lab(612, 178, "5. Protecția la suprasarcină a motorului o face", "start", 9), lab(612, 190, "    CF (I²t) + PTC; fără releu termic.", "start", 9),
          lab(612, 208, "6. Protecție diferențială, dacă e cerută: tip B.", "start", 9),
          lab(612, 226, "7. Filtru de ieșire după lungimea cablului și", "start", 9), lab(612, 238, "    tipul motorului (manualul CF).", "start", 9),
          lab(612, 256, "8. PE la CF, la filtru și la motor; ecranul nu", "start", 9), lab(612, 268, "    înlocuiește PE.", "start", 9)]
    save(f"{OUT}/05_schema_monofilara_forta.svg", doc(W, H, A, C, T, title="Schema monofilară de forță: ventilator acționat cu convertizor de frecvență"))

# ------------------------------------------------------------------ 06 schema de comandă (borne CF)
def schema_comanda():
    W, H = 900, 610
    A, C, T = [], [], []
    bx, by, bw, bh = 340, 40, 230, 545
    A += [ap("U1 convertizor – regleta de comandă", rect(bx, by, bw, bh, K), lab(bx + bw / 2, by + 18, "U1 – borne de comandă", size=12, weight="bold"),
             lab(bx + bw / 2, by + 34, "(denumiri generice; numerele din manualul CF)", size=8))]
    Y = dict(p24=80, di1=125, di2=175, di3=225, di4=275, p10=320, ai1=350, gnd=380, ai2=420, ptc=472, sto=510, r1=545, r2=570)
    names = dict(p24="+24 V", di1="DI1 Start/Stop", di2="DI2 Reset", di3="DI3 Mod incendiu", di4="DI4 Treaptă fixă", p10="+10 V",
                 ai1="AI1 0–10 V referință", gnd="GND", ai2="AI2 4–20 mA reacție", ptc="T1/T2 PTC motor", sto="STO 1 / STO 2",
                 r1="Releu 1: funcționare", r2="Releu 2: avarie")
    for k, y in Y.items():
        A += [ap(f"Bornă {names[k]}", term(bx, y), lab(bx + 10, y, names[k], "start", 9))]
    xr = 60; xc = 200   # bara +24 V și poziția contactelor
    C += [line(xr, Y["p24"], bx, Y["p24"]), line(xr, Y["p24"], xr, Y["di4"]), dot(xr, Y["di1"]), dot(xr, Y["di2"]), dot(xr, Y["di3"])]
    T += [lab(xr + 8, Y["p24"] + 12, "+24 V", "start", 9)]
    def row(k, sym, l1, l2="", col="#111"):
        y = Y[k]
        C.append(line(xr, y, xc - 14, y)); C.append(line(xc + 14, y, bx, y))
        A.append(ap(l1, sym, lab(xc, y - 18, l1, size=9, fill=col), lab(xc, y + 16, l2, size=8, fill=col)))
    row("di1", s_contact_h(xc, Y["di1"]), "K-BMS: Auto (contact menținut)", "comandă în 2 fire")
    row("di2", s_pushbutton(xc, Y["di2"]), "S2 Reset avarie", "buton cu revenire")
    row("di3", s_contact_h(xc, Y["di3"], nc=True), "K-CDI: contact NC al centralei de incendiu", "deschis = incendiu → n max.", "#b3261e")
    row("di4", s_contact_h(xc, Y["di4"]), "S4 Treaptă fixă (noapte 60 %)", "referință preselectată")
    # potențiometru între +10 V și GND
    px = 150
    A += [ap("R1 potențiometru 10 kΩ", rect(px - 7, Y["p10"] + 8, 14, Y["gnd"] - Y["p10"] - 16, K),
             f"<path d='M{px+22} {Y['ai1']}L{px+9} {Y['ai1']}M{px+15} {Y['ai1']-6}L{px+9} {Y['ai1']}L{px+15} {Y['ai1']+6}' {K}/>",
             lab(px - 14, Y["ai1"] - 6, "R1", "end", 10), lab(px - 14, Y["ai1"] + 8, "10 kΩ", "end", 8))]
    C += [line(px, Y["p10"], px, Y["p10"] + 8), line(px, Y["p10"], bx, Y["p10"]), line(px, Y["gnd"] - 8, px, Y["gnd"]), line(px, Y["gnd"], bx, Y["gnd"]),
          line(px + 22, Y["ai1"], bx, Y["ai1"])]
    T += [lab(240, Y["ai1"] - 12, "sau 0–10 V din BMS", "start", 8, fill="#1d5fa8")]
    # traductor presiune
    sx = 120
    A += [ap("B1 traductor presiune diferențială", rect(sx - 26, Y["ai2"] - 16, 52, 32, K), s_sensor(sx, Y["ai2"], "Δp"),
             lab(sx, Y["ai2"] + 27, "B1 0…1000 Pa / 4–20 mA, 2 fire", size=8), lab(sx, Y["ai2"] + 38, "în canalul de refulare", size=8))]
    C += [line(sx - 26, Y["ai2"] - 8, 40, Y["ai2"] - 8), line(40, Y["ai2"] - 8, 40, Y["p24"] - 20), line(40, Y["p24"] - 20, xr + 40, Y["p24"] - 20),
          line(xr + 40, Y["p24"] - 20, xr + 40, Y["p24"]), dot(xr + 40, Y["p24"]), line(sx + 26, Y["ai2"], bx, Y["ai2"])]
    T += [lab(30, Y["ai2"] - 30, "+24 V", "start", 8), lab(255, Y["ai2"] - 10, "4–20 mA", "start", 8)]
    # PTC
    A += [ap("PTC motor M1", s_ptc(sx, Y["ptc"]), lab(sx, Y["ptc"] + 18, "PTC în bobinajul M1 (T1-T2)", size=8))]
    C += [line(sx + 12, Y["ptc"], bx, Y["ptc"]), line(sx - 12, Y["ptc"], 80, Y["ptc"]), line(80, Y["ptc"], 80, Y["ptc"] + 12), line(80, Y["ptc"] + 12, 300, Y["ptc"] + 12), line(300, Y["ptc"] + 12, 300, Y["ptc"]), dot(300, Y["ptc"])]
    # STO
    A += [ap("K-STO releu de siguranță", rect(70, Y["sto"] - 10, 110, 44, KT), lab(125, Y["sto"] + 4, "releu de siguranță", size=8), lab(125, Y["sto"] + 18, "PL d – oprire de urgență", size=8))]
    C += [line(180, Y["sto"], bx, Y["sto"]), line(180, Y["sto"] + 20, 300, Y["sto"] + 20), line(300, Y["sto"] + 20, 300, Y["sto"]), dot(300, Y["sto"])]
    # ieșiri dreapta
    A += [ap("H1 semnal funcționare", f"<circle cx='690' cy='{Y['r1']}' r='10' {K}/>", f"<path d='M683 {Y['r1']-7}L697 {Y['r1']+7}M683 {Y['r1']+7}L697 {Y['r1']-7}' {KT}/>", lab(708, Y["r1"], "H1 funcționare → BMS", "start", 9)),
          ap("H2 semnal avarie", f"<circle cx='690' cy='{Y['r2']}' r='10' {K}/>", f"<path d='M683 {Y['r2']-7}L697 {Y['r2']+7}M683 {Y['r2']+7}L697 {Y['r2']-7}' {KT}/>", lab(708, Y["r2"], "H2 avarie → BMS", "start", 9, fill="#b3261e"))]
    C += [line(bx + bw, Y["r1"], 680, Y["r1"]), line(bx + bw, Y["r2"], 680, Y["r2"])]
    A += [ap("Ieșire analogică / bus", term(bx + bw, Y["ai1"]), lab(bx + bw + 10, Y["ai1"], "AO 0–10 V: turația → BMS", "start", 9),
             term(bx + bw, Y["gnd"]), lab(bx + bw + 10, Y["gnd"], "RS-485 Modbus RTU / BACnet → BMS", "start", 9))]
    T += [rect(600, 60, 285, 200, KT), lab(742, 78, "Semnale tipice la un ventilator", size=11, weight="bold"),
          lab(612, 100, "• Start/Stop: contact menținut din BMS (2 fire)", "start", 9),
          lab(612, 116, "• Referință: 0–10 V din BMS sau PID intern cu", "start", 9), lab(612, 128, "   reacție 4–20 mA de la traductorul de presiune", "start", 9),
          lab(612, 146, "• Mod incendiu: contact NC – la fir rupt sau", "start", 9), lab(612, 158, "   incendiu, ventilatorul merge la turația maximă", "start", 9),
          lab(612, 176, "• PTC: protecția termică a motorului", "start", 9),
          lab(612, 194, "• STO: oprire sigură din releul de siguranță", "start", 9),
          lab(612, 212, "• Relee: funcționare / avarie spre BMS", "start", 9),
          lab(612, 230, "• Comunicație: Modbus RTU / BACnet MS/TP", "start", 9),
          lab(612, 248, "• Cablurile de semnal: ecranate, separat de forță", "start", 9)]
    save(f"{OUT}/06_schema_comanda_borne.svg", doc(W, H, A, C, T, title="Schema de comandă a convertizorului pentru un ventilator de CTA"))

# ------------------------------------------------------------------ 07 reglare presiune constantă (VAV)
def reglare_presiune():
    W, H = 900, 380
    A, C, T = [], [], []
    # CTA: filtru, baterie, ventilator, canal, cutii VAV
    A += [ap("Priză de aer", f"<path d='M40 150L40 210L90 210L90 150Z' {K}/>", f"<path d='M50 160L80 160M50 175L80 175M50 190L80 190' {KT}/>", lab(65, 225, "aer proaspăt", size=8))]
    A += [ap("Filtru", rect(110, 140, 30, 80), f"<path d='M110 140L140 220M110 220L140 140' {KT}/>", lab(125, 235, "filtru", size=8))]
    A += [ap("Baterie încălzire/răcire", rect(160, 140, 40, 80), f"<path d='M165 145L195 215M165 215L195 145' {KT}/>", lab(180, 235, "baterii", size=8))]
    A += [ap("Ventilator de refulare", rect(220, 140, 80, 80), s_fan(260, 180, 26), lab(260, 235, "ventilator refulare", size=8))]
    A += [ap("M1", s_motor(260, 120, 14), line(260, 134, 260, 154, KT))]
    C += [f"<path d='M300 165L860 165M300 195L860 195' {K}/>", f"<rect x='40' y='140' width='260' height='80' {KD}/>", lab(170, 132, "centrală de tratare a aerului (CTA)", size=9)]
    # cutii VAV
    for i, x in enumerate([560, 680, 800]):
        A += [ap(f"Cutie VAV {i+1}", rect(x - 20, 195, 40, 30), f"<path d='M{x-12} 200L{x+12} 220' {K}/>", f"<circle cx='{x}' cy='210' r='3' fill='#111'/>",
                 lab(x, 240, f"VAV {i+1}", size=8), lab(x, 252, "clapetă de zonă", size=7), line(x, 225, x, 260, KT), lab(x, 270, "→ încăpere", size=7))]
    # traductor presiune la 2/3 din canal
    A += [ap("B1 traductor presiune statică", s_sensor(460, 120, "Δp"), line(460, 131, 460, 165, KT), lab(460, 100, "B1: presiune statică în canal", size=9), lab(460, 88, "(la ≈ 2/3 din lungimea canalului)", size=8))]
    # convertizor
    A += [ap("U1 convertizor", s_converter(340, 40, 60, 50), lab(370, 30, "U1 cu PID intern", size=9))]
    C += [line(340, 90, 340, 110), line(340, 110, 260, 110), line(260, 110, 260, 106)]  # către motor
    C += [arrow(449, 120, 372, 68, KB), lab(400, 84, "4–20 mA", "start", 8, fill="#1d5fa8")]
    A += [ap("Referință", rect(230, 40, 80, 40, KT), lab(270, 52, "referință", size=9), lab(270, 66, "300 Pa", size=9, weight="bold"))]
    C += [arrow(310, 60, 340, 60, KB)]
    T += [lab(660, 130, "Funcționare:", "start", 10, weight="bold"),
          lab(660, 146, "clapetele VAV se închid → Δp crește → PID scade turația", "start", 8),
          lab(660, 158, "clapetele se deschid → Δp scade → PID crește turația", "start", 8),
          lab(660, 170, "p = ct. → Q după nevoie → P ~ n³", "start", 8, fill="#2e7d32")]
    T += [lab(40, 320, "Regulă practică: referința se alege ca presiunea minimă la care ultima cutie VAV, complet deschisă, primește debitul de calcul", "start", 9),
          lab(40, 336, "(„resetul presiunii” în BMS coboară referința când toate clapetele sunt parțial închise). Frecvența minimă: 15–20 Hz, ca motorul să se răcească.", "start", 9)]
    save(f"{OUT}/07_reglare_presiune_constanta_VAV.svg", doc(W, H, A, C, T, title="Reglarea presiunii constante în canal (sistem VAV)"))

# ------------------------------------------------------------------ 08 reglare după CO2 / temperatură (CAV)
def reglare_co2():
    W, H = 900, 340
    A, C, T = [], [], []
    A += [ap("Ventilator refulare", rect(60, 120, 80, 70), s_fan(100, 155, 22), lab(100, 205, "refulare", size=8)), ap("M1", s_motor(100, 96, 12), line(100, 108, 100, 133, KT))]
    A += [ap("Ventilator evacuare", rect(60, 230, 80, 70), s_fan(100, 265, 22), lab(100, 315, "evacuare", size=8)), ap("M2", s_motor(30, 265, 12), line(42, 265, 78, 265, KT))]
    C += [f"<path d='M140 140L420 140M140 170L420 170' {K}/>", f"<path d='M140 250L420 250M140 280L420 280' {K}/>"]
    A += [ap("Încăpere", rect(420, 60, 300, 240, KD), lab(570, 78, "sală de clasă / birou", size=10), lab(570, 92, "(volum constant de aer, CAV)", size=8)),
          ap("B2 senzor CO2", rect(600, 150, 60, 34, K), lab(630, 162, "CO₂", size=10, weight="bold"), lab(630, 176, "ppm", size=8)),
          ap("B3 senzor temperatură", s_sensor(700, 167, "T"))]
    A += [ap("U1 convertizor refulare", s_converter(260, 30, 56, 46), lab(288, 20, "U1", size=9)), ap("U2 convertizor evacuare", s_converter(260, 200, 56, 46), lab(288, 190, "U2", size=9))]
    C += [line(260, 76, 260, 90), line(260, 90, 100, 90), line(100, 90, 100, 84)]
    C += [line(260, 246, 260, 258), line(260, 258, 30, 258), line(30, 258, 30, 253)]
    C += [arrow(600, 167, 292, 60, KB), lab(420, 40, "0–10 V de la senzorul CO₂ (referință 800 ppm)", "start", 8, fill="#1d5fa8")]
    C += [arrow(288, 76, 288, 200, KB), lab(300, 140, "AO turație → U2 urmărește U1", "start", 8, fill="#1d5fa8"), lab(300, 152, "(sau diferență fixă de debit)", "start", 8, fill="#1d5fa8")]
    T += [lab(740, 130, "Funcționare:", "start", 10, weight="bold"), lab(740, 146, "CO₂ crește (mulți", "start", 8), lab(740, 158, "elevi) → turația crește", "start", 8),
          lab(740, 174, "CO₂ scade → turația", "start", 8), lab(740, 186, "scade, dar nu sub", "start", 8), lab(740, 198, "f min = 20 Hz (aer", "start", 8), lab(740, 210, "minim de igienă)", "start", 8),
          lab(740, 230, "Evacuarea urmărește", "start", 8), lab(740, 242, "refularea → încăperea", "start", 8), lab(740, 254, "rămâne echilibrată", "start", 8)]
    save(f"{OUT}/08_reglare_CO2_temperatura_CAV.svg", doc(W, H, A, C, T, title="Reglarea după CO₂ / temperatură (sistem CAV) cu două convertizoare"))

# ------------------------------------------------------------------ 09 mai multe ventilatoare pe un convertizor cu filtru sinus
def mai_multe_ventilatoare():
    W, H = 900, 480
    A, C, T = [], [], []
    x = 120
    C += [line(x, 30, x, 60)]; T += [lab(x + 12, 40, "3~ 400 V", "start", 10)]
    A += [ap("Q1", s_disconnector(x, 66), s_fuse(x, 108, 26), lab(x + 20, 80, "Q1 + F1 gG", "start", 10))]
    C += [line(x, 140, x, 170)]
    A += [ap("U1 convertizor cu filtru sinus integrat", s_converter(x, 170, 70, 60), s_filter(x, 240, 46, 26, "∿"),
             lab(x + 45, 190, "U1 convertizor pentru ventilatoare cu filtru sinus", "start", 10, weight="bold"),
             lab(x + 45, 204, "integrat, „allpolig” (fază-fază și fază-PE)", "start", 9),
             lab(x + 45, 218, "ex. Ziehl-Abegg Fcontrol FSDM, Helios FU", "start", 9),
             lab(x + 30, 253, "filtru sinus", "start", 9))]
    C += [line(x, 230, x, 240), line(x, 266, x, 300)]
    # bara de distribuție către 3 motoare
    C += [line(x, 300, 740, 300)]
    T += [lab(430, 290, "cablu de motor neecranat (tensiune sinusoidală) – ΣI motoare ≤ I nominal CF", size=9)]
    for i, mx in enumerate([220, 430, 640]):
        C += [line(mx, 300, mx, 320), dot(mx, 300)]
        A += [ap(f"F{i+2} aparat de protecție motor", s_breaker(mx, 326), lab(mx + 14, 340, f"F{i+2} disjunctor motor", "start", 9),
                 lab(mx + 14, 352, "(protecție cablu; termicul", "start", 8), lab(mx + 14, 362, "nu vede curentul corect la f mic)", "start", 8))]
        C += [line(mx, 362, mx, 400)]
        A += [ap(f"M{i+1} motor ventilator", s_motor(mx, 418, 18), s_fan(mx, 460, 12), line(mx, 436, mx, 448, KT),
                 lab(mx + 24, 412, f"M{i+1}", "start", 10, weight="bold"), lab(mx + 24, 426, "1,5 kW, 3,6 A", "start", 9),
                 rect(mx - 60, 405, 24, 12, KT), lab(mx - 48, 411, "TB", size=7), line(mx - 36, 411, mx - 18, 411, KT))]
        # termocontacte în serie
    # linie termocontacte TB în serie → CF
    C += [f"<path d='M160 411L160 380L600 380' {KB}/>", f"<path d='M200 380L200 411' {KB}/>", f"<path d='M370 411L370 380' {KB}/>", f"<path d='M580 411L580 380' {KB}/>", f"<path d='M160 380L160 226L85 226' {KB}/>"]
    T += [lab(90, 240, "TB/TP", "start", 8, fill="#1d5fa8"), lab(300, 372, "termocontactele TB ale motoarelor în serie → intrarea TB/TP a CF (max. 6 PTC)", "start", 8, fill="#1d5fa8")]
    T += [rect(700, 40, 190, 220, KT), lab(795, 58, "Când e permis?", size=10, weight="bold"),
          lab(710, 80, "• numai cu filtru sinus", "start", 8), lab(710, 92, "  (tensiune sinusoidală la", "start", 8), lab(710, 104, "  toate motoarele)", "start", 8),
          lab(710, 122, "• ventilatoare identice sau", "start", 8), lab(710, 134, "  de aceeași familie", "start", 8),
          lab(710, 152, "• fiecare motor cu propria", "start", 8), lab(710, 164, "  protecție (TB/PTC sau", "start", 8), lab(710, 176, "  aparat de protecție motor)", "start", 8),
          lab(710, 194, "• CF: I nominal ≥ ΣI motoare;", "start", 8), lab(710, 206, "  U/f pătratic, fără AMA", "start", 8), lab(710, 218, "  (autotune) pe grup", "start", 8),
          lab(710, 236, "• fără comutare a unui", "start", 8), lab(710, 248, "  motor în mers", "start", 8)]
    save(f"{OUT}/09_mai_multe_ventilatoare_filtru_sinus.svg", doc(W, H, A, C, T, title="Mai multe ventilatoare pe un convertizor cu filtru sinus"))

# ------------------------------------------------------------------ 10 bypass cu două contactoare interblocate
def bypass():
    W, H = 900, 520
    A, C, T = [], [], []
    x = 200
    C += [line(x, 30, x, 60)]; T += [lab(x + 12, 40, "3~ 400 V", "start", 10)]
    A += [ap("Q1", s_disconnector(x, 66), s_fuse(x, 108, 26), lab(x + 20, 80, "Q1 + F1", "start", 10))]
    C += [line(x, 140, x, 170), line(x, 170, 420, 170), dot(x, 170)]
    # ramura CF
    A += [ap("K1 contactor intrare CF", s_contact_no(x, 176), lab(x + 20, 190, "K1 (AC-1)", "start", 9))]
    C += [line(x, 212, x, 240)]
    A += [ap("U1 convertizor", s_converter(x, 240, 70, 60), lab(x + 45, 270, "U1", "start", 10, weight="bold"))]
    C += [line(x, 300, x, 330)]
    A += [ap("K2 contactor ieșire CF", s_contact_no(x, 336), lab(x + 20, 350, "K2 (AC-3) – se închide numai cu CF oprit", "start", 9),
             lab(x + 20, 362, "și se deschide numai după stop CF", "start", 8))]
    C += [line(x, 372, x, 420)]
    # ramura bypass
    xb = 420
    C += [line(xb, 170, xb, 240)]
    A += [ap("K3 contactor bypass", s_contact_no(xb, 246), lab(xb + 20, 260, "K3 (AC-3) bypass rețea", "start", 9))]
    C += [line(xb, 282, xb, 310)]
    A += [ap("F2 releu termic bypass", s_thermal(xb, 316), lab(xb + 20, 330, "F2 releu termic, reglat la I n motor", "start", 9), lab(xb + 20, 342, "(numai în bypass motorul nu e protejat de CF)", "start", 8))]
    C += [line(xb, 348, xb, 420), line(x, 420, xb, 420), dot(x, 420), line(310, 420, 310, 440)]
    A += [ap("M1 motor ventilator", s_motor(310, 458, 18), lab(340, 452, "M1 ventilator", "start", 10, weight="bold"), lab(340, 466, "pornire directă în bypass: I p = 6…8 × I n", "start", 8, fill="#b3261e"))]
    # interblocare
    C += [f"<path d='M{x-40} 350L{x-40} 262L{xb-40} 262' {KDR}/>"]
    T += [lab(x - 44, 300, "interblocare mecanică + electrică K2 ↔ K3", "start", 8, fill="#b3261e", rot=-90)]
    T += [rect(600, 40, 290, 300, KT), lab(745, 58, "Secvența de comutare CF → bypass", size=10, weight="bold"),
          lab(612, 82, "1. Stop la CF (rampa de oprire) și așteptarea", "start", 9), lab(612, 94, "   opririi ventilatorului (poate fi 30…90 s).", "start", 9),
          lab(612, 112, "2. Se deschide K2 (ieșirea CF liberă).", "start", 9),
          lab(612, 130, "3. Temporizare ≥ 1 s (Ziehl-Abegg cere min. 1 s).", "start", 9),
          lab(612, 148, "4. Se închide K3: motorul pornește direct, cu", "start", 9), lab(612, 160, "   I p; F2 protejează motorul.", "start", 9),
          lab(612, 184, "Invers (bypass → CF): K3 deschis → pauză →", "start", 9), lab(612, 196, "K2 închis → start CF cu „prindere din mers”", "start", 9),
          lab(612, 208, "(flying start), altfel CF dă supracurent.", "start", 9),
          lab(612, 232, "Niciodată tensiune de rețea pe ieșirea CF!", "start", 9, weight="bold", fill="#b3261e"),
          lab(612, 256, "Bypassul se folosește la ventilatoare de", "start", 9), lab(612, 268, "siguranță (desfumare) sau unde oprirea", "start", 9),
          lab(612, 280, "nu e admisă (săli de operație, servere).", "start", 9),
          lab(612, 304, "Manual: comutator 0 – AUTO – 100 % (ex.", "start", 9), lab(612, 316, "Ziehl-Abegg S-D-25) în locul K2/K3.", "start", 9)]
    save(f"{OUT}/10_bypass_contactoare.svg", doc(W, H, A, C, T, title="Ocolirea (bypass) convertizorului cu contactoare interblocate"))

# ------------------------------------------------------------------ 11 curba U/f liniară vs pătratică
def curba_uf():
    W, H = 720, 380
    ox, oy, gw, gh = 80, 320, 560, 260
    A, C = [], []
    C += [arrow(ox, oy, ox, oy - gh - 10, K), arrow(ox, oy, ox + gw + 10, oy, K)]
    for i in range(0, 6):
        x = ox + gw * i / 5; C += [line(x, oy, x, oy + 5), lab(x, oy + 16, f"{i*10}", size=9)]
    for i in range(0, 5):
        y = oy - gh * i / 4; C += [line(ox - 5, y, ox, y), lab(ox - 22, y, f"{i*100}", size=9)]
    C += [lab(ox + gw / 2, oy + 34, "frecvența f (Hz)", size=11), lab(ox - 40, oy - gh - 6, "U (V)", size=11)]
    lin = [(ox + gw * f / 50, oy - gh * (0.03 + 0.97 * f / 50) * 400 / 400) for f in range(0, 51)]
    quad = [(ox + gw * f / 50, oy - gh * (0.03 + 0.97 * (f / 50) ** 2)) for f in range(0, 51)]
    C += [f"<path d='M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in lin) + f"' {KB}/>", f"<path d='M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in quad) + f"' {KG}/>"]
    x25 = ox + gw * 25 / 50
    C += [f"<path d='M{x25} {oy}L{x25} {oy-gh*0.515}' {KD}/>"]
    A += [ap("Legenda", rect(ox + 20, oy - 255, 300, 62, KT), lab(ox + 30, oy - 242, "U/f liniar (cuplu constant): 25 Hz → 200 V", "start", 10, fill="#1d5fa8", weight="bold"),
             lab(ox + 30, oy - 224, "U/f pătratic (ventilatoare, pompe): 25 Hz → ≈ 110 V", "start", 10, fill="#2e7d32", weight="bold"),
             lab(ox + 30, oy - 206, "→ flux magnetic redus, pierderi mai mici, zgomot mai mic", "start", 9)),
          ap("Puncte 25 Hz", dot(x25, oy - gh * 0.515, 4), dot(x25, oy - gh * 0.2725, 4), lab(x25 + 8, oy - gh * 0.515, "200 V", "start", 9, fill="#1d5fa8"),
             lab(x25 + 8, oy - gh * 0.2725, "≈ 110 V", "start", 9, fill="#2e7d32"), lab(ox + gw + 4, oy - gh, "400 V la 50 Hz", "start", 9))]
    save(f"{OUT}/11_curba_Uf_liniar_patratic.svg", doc(W, H, A, C, title="Caracteristica U/f liniară și pătratică (VT)"))

# ------------------------------------------------------------------ 12 mod incendiu / desfumare
def mod_incendiu():
    W, H = 900, 300
    A, C, T = [], [], []
    A += [ap("CDI centrală de detecție incendiu", rect(40, 60, 140, 80, K), lab(110, 82, "centrală de", size=10), lab(110, 96, "detecție incendiu", size=10), lab(110, 116, "ieșire releu", size=8)),
          ap("K-CDI contact NC", s_contact_h(260, 100, nc=True, label="contact NC"), lab(260, 118, "se deschide la alarmă", size=8, fill="#b3261e")),
          ap("U1 convertizor ventilator desfumare", s_converter(450, 60, 80, 70), lab(490, 40, "U1 – DI „mod incendiu”", size=9, weight="bold")),
          ap("M1 ventilator desfumare", s_motor(660, 95, 20, "M", "3~"), s_fan(720, 95, 16), line(680, 95, 704, 95, KT), lab(690, 130, "ventilator de desfumare F400 (400 °C / 2 h)", size=8))]
    C += [line(180, 100, 246, 100), line(274, 100, 410, 100), line(410, 100, 410, 90), line(410, 90, 450, 90, KB), line(490, 130, 490, 160), line(490, 160, 660, 160), line(660, 160, 660, 115)]
    T += [lab(180, 90, "24 V", "start", 8), lab(600, 152, "3~ U var.", "start", 8)]
    T += [rect(40, 180, 850, 105, KT), lab(465, 198, "Ce face „modul incendiu” (fire mode / Feuerbetrieb)", size=10, weight="bold"),
          lab(52, 218, "• CF trece pe referința de incendiu (de obicei 50 Hz sau f max.) și ignoră toate celelalte comenzi, inclusiv oprirea din BMS.", "start", 9),
          lab(52, 234, "• Se dezactivează avertizările și limitările neesențiale: supratemperatura CF, managementul termic, limitarea de curent — CF merge „până cade”.", "start", 9),
          lab(52, 250, "• Se folosește contact NC (deschis = incendiu): un fir rupt de foc pune singur ventilatorul la turație maximă. Protecția PTC nu mai oprește motorul.", "start", 9),
          lab(52, 266, "• Bypassul cu contactor (schema 10) rămâne soluția impusă de multe proiecte de desfumare: la avaria CF, motorul pornește direct din rețea.", "start", 9)]
    save(f"{OUT}/12_mod_incendiu_desfumare.svg", doc(W, H, A, C, T, title="Modul incendiu la ventilatoarele de desfumare"))

# ------------------------------------------------------------------ 13 traductor de presiune și montaj
def montaj_traductor():
    W, H = 900, 300
    A, C, T = [], [], []
    C += [f"<path d='M40 120L860 120M40 180L860 180' {K}/>"]
    T += [lab(450, 150, "canal de refulare →", size=11, fill="#2e7d32")]
    A += [ap("Ventilator", s_fan(90, 150, 24), lab(90, 200, "ventilator", size=8)),
          ap("Cot", f"<path d='M180 120L220 120M180 180L220 180' {KR}/>", lab(200, 200, "cot / tranziție", size=8, fill="#b3261e"), lab(200, 212, "(zonă turbulentă)", size=8, fill="#b3261e")),
          ap("B1 traductor Δp", rect(540, 60, 70, 36, K), lab(575, 72, "B1 Δp", size=10, weight="bold"), lab(575, 88, "4–20 mA", size=8),
             f"<path d='M560 96L560 120' {KT}/>", f"<path d='M590 96L590 106L640 106L640 50L860 50' {KT}/>", lab(750, 40, "priza „–”: presiune atmosferică / încăpere", size=8),
             lab(560, 110, "+", "end", 9)),
          ap("Zonă montaj", f"<path d='M300 100L300 200' {KD}/>", f"<path d='M840 100L840 200' {KD}/>", lab(570, 230, "traductorul: pe porțiune dreaptă, la 2/3 din canal (nu lângă ventilator, nu după cot)", size=9),
             lab(570, 246, "priza de presiune statică perpendiculară pe perete; furtun scurt; cablul de semnal ecranat", size=9))]
    C += [arrow(560, 120, 560, 106, KB)]
    save(f"{OUT}/13_montaj_traductor_presiune.svg", doc(W, H, A, C, T, title="Montajul traductorului de presiune în canal"))


# ------------------------------------------------------------------ 14 schema unui compartiment de grajd (după exemplul Ziehl-Abegg FTET 12.4.1 și DLG-AU Bild 15)
def schema_grajd():
    W, H = 900, 520
    A, C, T = [], [], []
    A += [ap("Compartiment grajd", rect(300, 120, 560, 300, KD), lab(580, 138, "compartiment de porci (populare–depopulare totală)", size=10))]
    for i in range(5):
        x = 575 + i * 68
        A += [ap(f"Boxă {i+1}", rect(x - 25, 340, 50, 40, KT), lab(x, 360, "porci", size=8))]
    A += [ap("M1 ventilator de evacuare", rect(560, 40, 60, 80, K), s_fan(590, 80, 22), lab(590, 30, "coș de evacuare", size=9), lab(650, 60, "M1 1~ 230 V, Ø 630", "start", 9), lab(650, 74, "10 500 m³/h la 30 Pa", "start", 8),
             lab(650, 88, "cu termocontact TB", "start", 8))]
    A += [ap("Clapetă de evacuare cu servomotor", rect(470, 60, 40, 30, K), f"<path d='M475 88L505 62' {K}/>", lab(490, 104, "clapetă", size=8), lab(490, 50, "servomotor 0–10 V", size=8))]
    A += [ap("Admisie de aer cu clapete", rect(305, 300, 12, 100, K), f"<path d='M320 320L400 320M320 320L330 310M320 320L330 330' {KG}/>", f"<path d='M320 380L400 380M320 380L330 370M320 380L330 390' {KG}/>",
             lab(410, 336, "admisie aer, clapete", "start", 8, fill="#2e7d32"), lab(410, 348, "cu revenire cu arc", "start", 8), lab(410, 360, "(se deschid la pană)", "start", 8))]
    A += [ap("B1 senzor temperatură interior", s_sensor(700, 250, "T"), lab(700, 272, "B1 temp. interior", size=8)),
          ap("B2 senzor temperatură exterior", s_sensor(840, 40, "T"), lab(840, 62, "B2 exterior", size=8)),
          ap("B3 senzor umiditate", s_sensor(780, 250, "H"), lab(780, 272, "B3 umiditate", size=8))]
    A += [ap("Anticameră", rect(20, 120, 250, 300, KD), lab(145, 138, "anticameră (aer curat, fără amoniac)", size=9))]
    A += [ap("U1 regulator de climă cu convertizor și filtru sinus", rect(60, 170, 170, 120, K), lab(145, 190, "U1 computer de climă", size=10, weight="bold"),
             lab(145, 206, "cu convertizor de frecvență", size=9), lab(145, 220, "și filtru sinus, IP54", size=9), lab(145, 240, "curbă: 20 °C → 20…100 %", size=8),
             lab(145, 254, "ventilație minimă 20 %", size=8), lab(145, 268, "alarme min/max, Modbus", size=8))]
    A += [ap("S1 comutator 0 / Auto / 100 %", rect(60, 320, 90, 40, K), lab(105, 334, "0 – AUTO – 100 %", size=8), lab(105, 348, "ocolire manuală", size=8)),
          ap("H1 alarmă", f"<circle cx='200' cy='340' r='12' {KR}/>", lab(200, 340, "!", size=12, weight="bold", fill="#b3261e"), lab(200, 362, "alarmă → telefon", size=8, fill="#b3261e"))]
    A += [ap("G1 grup electrogen", rect(60, 440, 110, 50, K), lab(115, 458, "G1 grup electrogen", size=9), lab(115, 474, "+ comutator rețea/grup", size=8)),
          ap("Q0 tablou", rect(200, 440, 70, 50, K), lab(235, 465, "tablou", size=9))]
    C += [f"<path d='M230 275L285 275L285 300L311 300' {KB}/>", lab(258, 267, "0–10 V", size=7, fill="#1d5fa8")]
    C += [f"<path d='M230 195L490 195L490 90' {KB}/>", lab(300, 187, "0–10 V clapetă evacuare", "start", 7, fill="#1d5fa8")]
    C += [f"<path d='M230 235L560 235L560 122L590 122' {K}/>", lab(300, 227, "3~ ieșire CF (cablu neecranat, filtru sinus)", "start", 7)]
    C += [f"<path d='M700 261L700 300L145 300L145 290' {KB}/>", f"<path d='M780 261L780 300' {KB}/>", f"<path d='M840 51L840 300' {KB}/>"]
    C += [line(105, 360, 105, 400), line(105, 400, 145, 400), line(145, 400, 145, 290)]
    C += [line(235, 440, 235, 400), line(235, 400, 145, 400), line(170, 465, 200, 465)]
    T += [lab(300, 450, "Reguli (TierSchNutztV § 3, DLG-Merkblatt 422): dispozitiv de rezervă care asigură aer la pană (clapete cu arc)", "start", 8),
          lab(300, 464, "+ alarmă la căderea ventilației; ventilatoarele pe circuite separate; alarma funcționează ≥ 2 h fără rețea;", "start", 8),
          lab(300, 478, "grup electrogen dimensionat la suma consumatorilor + 20…25 %; test alarmă săptămânal, test grup lunar.", "start", 8)]
    save(f"{OUT}/14_schema_compartiment_grajd.svg", doc(W, H, A, C, T, title="Ventilația unui compartiment de grajd cu regulator de climă și convertizor"))

# ------------------------------------------------------------------ 15 curba de reglare temperatură → ventilație (Ziehl-Abegg FTET: Sollwert, Regelbereich, Min/Max)
def curba_reglare_grajd():
    W, H = 720, 380
    ox, oy, gw, gh = 80, 320, 560, 260
    A, C = [], []
    C += [arrow(ox, oy, ox, oy - gh - 10, K), arrow(ox, oy, ox + gw + 10, oy, K)]
    temps = list(range(14, 30, 2))
    for t in temps:
        x = ox + gw * (t - 14) / 16; C += [line(x, oy, x, oy + 5), lab(x, oy + 16, f"{t}", size=9)]
    for i in range(0, 6):
        y = oy - gh * i / 5; C += [line(ox - 5, y, ox, y), lab(ox - 22, y, f"{i*20}", size=9)]
    C += [lab(ox + gw / 2, oy + 34, "temperatura în grajd (°C)", size=11), lab(ox - 44, oy - gh - 6, "ventilație %", size=11)]
    X = lambda t: ox + gw * (t - 14) / 16; Y = lambda p: oy - gh * p / 100
    # curba: min 20 % până la Sollwert 20 °C, apoi liniar până la 100 % la Sollwert + Regelbereich (4 K) = 24 °C
    C += [f"<path d='M{X(14)} {Y(20)}L{X(20)} {Y(20)}L{X(24)} {Y(100)}L{X(30)} {Y(100)}' {KB}/>"]
    C += [f"<path d='M{X(20)} {oy}L{X(20)} {Y(20)}' {KD}/>", f"<path d='M{X(24)} {oy}L{X(24)} {Y(100)}' {KD}/>"]
    A += [ap("Etichete", lab(X(17), Y(20) - 14, "ventilație minimă 20 % (aer de igienă)", size=9, fill="#1d5fa8"),
             lab(X(20), oy - gh - 4, "valoare prescrisă 20 °C", size=9), lab(X(24) + 4, Y(60), "bandă de reglare 4 K", "start", 9),
             lab(X(27), Y(100) - 12, "maxim 100 %", size=9, fill="#1d5fa8"),
             lab(X(15), Y(90), "iarnă: bandă 3–4 K", "start", 9), lab(X(15), Y(80), "vară: bandă 5–7 K", "start", 9),
             lab(X(15), Y(65), "alarmă la ±5 K față de prescris", "start", 9, fill="#b3261e"))]
    # alarm lines
    C += [f"<path d='M{X(25)} {oy}L{X(25)} {Y(100)}' {KDR}/>", f"<path d='M{X(15)} {oy}L{X(15)} {Y(100)}' {KDR}/>"]
    save(f"{OUT}/15_curba_reglare_temperatura_ventilatie.svg", doc(W, H, A, C, title="Curba de reglare a ventilației după temperatură (regulator de grajd)"))

# ------------------------------------------------------------------ 16 arbore de decizie: cum aleg metoda de reglare și convertizorul
def arbore_decizie():
    W, H = 900, 600
    A, C, T = [], [], []
    def box(x, y, w, h, lines, style=K, size=9, fill="#111", name=None):
        s = rect(x - w / 2, y - h / 2, w, h, style, rx=4)
        for i, l in enumerate(lines):
            s += lab(x, y - (len(lines) - 1) * 6.5 + i * 13, l, size=size, weight="bold" if (i == 0 and len(lines) > 1) else "normal", fill=fill)
        return ap(name or lines[0], s)
    A += [box(450, 40, 320, 40, ["Pasul 1: ce ventilator și ce motor am?"], size=11)]
    A += [box(150, 135, 260, 64, ["A. Ventilator mic 1~ 230 V", "motor cu rotor exterior,", "„comandabil în tensiune”"]),
          box(450, 135, 260, 64, ["B. Motor asincron 3~ standard", "(IEC, orice putere), sau", "ventilator vechi de refăcut"]),
          box(750, 135, 260, 64, ["C. Instalație nouă /", "înlocuire completă", "(CTA, condensator, grajd nou)"])]
    C += [line(450, 60, 450, 95), line(150, 95, 750, 95)]
    for x in (150, 450, 750): C.append(arrow(x, 95, x, 103, K))
    A += [box(150, 245, 260, 76, ["Reglare prin tensiune", "transformator în trepte (ieftin, trepte)", "sau regulator cu triac (zgomot, +10–20 %", "consum) sau CF cu filtru sinus (FTET)"], KB, 8),
          box(450, 245, 260, 76, ["Convertizor de frecvență", "un motor: CF universal / HVAC + cablu", "ecranat; mai multe motoare sau rotor", "exterior: CF cu filtru sinus"], KB, 8),
          box(750, 245, 260, 76, ["Ventilator EC", "convertizor și motor într-un produs;", "comandă 0–10 V / Modbus; randament", "maxim, fără cablu ecranat"], KB, 8)]
    for x in (150, 450, 750): C.append(arrow(x, 167, x, 207, K))
    A += [box(450, 350, 700, 50, ["Pasul 2: mărimea — după curentul de pe plăcuța motorului (nu după kW): I convertizor ≥ I n motor,", "regim de suprasarcină „normală” 110 %; la mai multe motoare pe un convertizor: I ≥ suma curenților"], K, 9)]
    C += [arrow(150, 283, 150, 300, K), arrow(450, 283, 450, 325, K), arrow(750, 283, 750, 300, K), line(150, 300, 750, 300)]
    A += [box(450, 425, 700, 44, ["Pasul 3: unde stă — IP20 în tablou (cablu ecranat până la motor) sau IP54/IP55 lângă ventilator;", "în grajd: în anticameră, nu în adăpost (amoniac, praf, umezeală)"], K, 9)]
    C += [arrow(450, 375, 450, 403, K)]
    A += [box(450, 498, 700, 44, ["Pasul 4: ce mai trebuie — filtru CEM C1/C2 în clădiri, siguranțe după manual, DDR tip B dacă e cerut, PTC/TB,", "separator de service cu contact anticipat, ocolire manuală 0–AUTO–100 % la ventilatoarele vitale, alarmă"], K, 9)]
    C += [arrow(450, 447, 450, 476, K)]
    A += [box(450, 565, 700, 36, ["Pasul 5: parametrii — date de plăcuță, curbă U/f pătratică, f min 15–20 Hz, rampe lungi, prindere din mers, frecvențe de evitare"], K, 9)]
    C += [arrow(450, 520, 450, 547, K)]
    save(f"{OUT}/16_arbore_decizie.svg", doc(W, H, A, C, T, title="Cum aleg metoda de reglare și convertizorul"))


# ------------------------------------------------------------------ 17 structura convertizorului (redresor – circuit intermediar – invertor PWM)
def structura_convertizor():
    W, H = 900, 360
    A, C, T = [], [], []
    # retea
    T += [lab(60, 150, "rețea", size=10, weight="bold"), lab(60, 166, "3~ 400 V", size=9), lab(60, 180, "50 Hz", size=9)]
    for i, y in enumerate((130, 150, 170)):
        C += [line(100, y, 160, y)]
    # redresor
    A += [ap("Redresor", rect(160, 90, 120, 120, K), lab(220, 110, "redresor", size=10, weight="bold"), lab(220, 126, "6 diode (B6)", size=9),
             f"<path d='M200 150L240 150M225 140L240 150L225 160Z' {KFB}/><path d='M240 140L240 160' {K}/>",
             lab(220, 190, "c.a. → c.c.", size=9))]
    C += [line(280, 110, 380, 110), line(280, 190, 380, 190)]
    # circuit intermediar
    A += [ap("Circuit intermediar de c.c.", rect(380, 90, 110, 120, K), lab(435, 110, "circuit intermediar", size=9, weight="bold"),
             f"<path d='M435 125L435 145M420 145L450 145M420 155L450 155M435 155L435 175' {K}/>", lab(435, 190, "≈ 565 V c.c.", size=9),
             lab(435, 226, "condensatoare: rămân încărcate", size=8, fill="#b3261e"), lab(435, 238, "minute după oprire!", size=8, fill="#b3261e"))]
    C += [line(490, 110, 590, 110), line(490, 190, 590, 190)]
    # invertor
    A += [ap("Invertor", rect(590, 90, 130, 120, K), lab(655, 110, "invertor", size=10, weight="bold"), lab(655, 126, "6 tranzistoare IGBT", size=9),
             f"<path d='M615 150L640 150M640 140L640 160M640 140L660 150L640 160' {KT}/><path d='M660 150L690 150' {KT}/>",
             lab(655, 190, "c.c. → c.a. cu f și U variabile", size=8))]
    for i, y in enumerate((130, 150, 170)):
        C += [line(720, y, 790, y)]
    A += [ap("M1 motor", s_motor(815, 150, 22), lab(815, 190, "f = 0…50 Hz", size=9), lab(815, 204, "U = 0…400 V", size=9))]
    # comanda
    A += [ap("Comanda", rect(380, 260, 340, 60, KB), lab(550, 280, "partea de comandă (microprocesor)", size=10, weight="bold", fill="#1d5fa8"),
             lab(550, 298, "referință 0–10 V / tastatură / Modbus → calculează f și U → comandă tranzistoarele (PWM)", size=8, fill="#1d5fa8"))]
    C += [arrow(655, 260, 655, 212, KB)]
    # forma de unda PWM (mic)
    T += [lab(753, 30, "la ieșire: impulsuri PWM; media lor = sinusoidă", size=8), f"<path d='M700 80L706 80L706 60L712 60L712 80L720 80L720 50L732 50L732 80L744 80L744 44L760 44L760 80L770 80L770 50L782 50L782 80L792 80L792 60L798 60L798 80L806 80' {KT}/>",
          f"<path d='M700 80Q753 10 806 80' {KG}/>"]
    save(f"{OUT}/17_structura_convertizor.svg", doc(W, H, A, C, T, title="Structura convertizorului de frecvență"))

# ------------------------------------------------------------------ 18 n = 60 f / p și U/f
def formula_turatie():
    W, H = 900, 330
    A, C, T = [], [], []
    T += [lab(230, 30, "Turația de sincronism: n₁ = 60 · f₁ / p", size=13, weight="bold"),
          lab(230, 50, "f₁ = frecvența tensiunii de alimentare (Hz), p = numărul de perechi de poli", size=9)]
    rows = [("2p = 2 (p = 1)", 3000, 2880), ("2p = 4 (p = 2)", 1500, 1440), ("2p = 6 (p = 3)", 1000, 960), ("2p = 8 (p = 4)", 750, 720)]
    y0 = 75
    A += [ap("Tabel poli", rect(40, y0, 400, 20 + 22 * len(rows), KT),
             lab(110, y0 + 10, "număr de poli", size=9, weight="bold"), lab(240, y0 + 10, "n₁ la 50 Hz", size=9, weight="bold"), lab(360, y0 + 10, "n (turația rotorului)", size=9, weight="bold"),
             *[lab(110, y0 + 32 + 22 * i, r[0], size=9) for i, r in enumerate(rows)],
             *[lab(240, y0 + 32 + 22 * i, f"{r[1]} min⁻¹", size=9) for i, r in enumerate(rows)],
             *[lab(360, y0 + 32 + 22 * i, f"≈ {r[2]} min⁻¹ (s = 4 %)", size=9) for i, r in enumerate(rows)])]
    T += [lab(230, 200, "Alunecarea: s = (n₁ − n) / n₁ ;  n = n₁ · (1 − s) ;  s = 2…5 % la sarcina nominală", size=9),
          lab(230, 222, "Motor cu 2p = 4, alimentat din convertizor:", size=10, weight="bold"),
          lab(230, 242, "f₁ = 50 Hz → n₁ = 1 500 min⁻¹   ·   f₁ = 25 Hz → 750 min⁻¹   ·   f₁ = 10 Hz → 300 min⁻¹", size=9),
          lab(230, 262, "Turația rotorului se reglează prin frecvența statorică f₁.", size=10, fill="#2e7d32", weight="bold")]
    ox, oy, gw, gh = 520, 260, 320, 200
    C += [arrow(ox, oy, ox, oy - gh - 10, K), arrow(ox, oy, ox + gw + 10, oy, K)]
    T += [lab(ox + gw / 2, oy + 20, "f₁ (Hz)", size=9), lab(ox - 30, oy - gh - 14, "U₁ (V)", size=9)]
    for f_, lbl in ((0, "0"), (25, "25"), (50, "50")):
        x = ox + gw * f_ / 60; C += [line(x, oy, x, oy + 4), lab(x, oy + 12, lbl, size=8)]
    for u, lbl in ((200, "200"), (400, "400")):
        y = oy - gh * u / 400; C += [line(ox - 4, y, ox, y), lab(ox - 16, y, lbl, size=8)]
    C += [f"<path d='M{ox} {oy}L{ox + gw*50/60} {oy-gh}L{ox + gw} {oy-gh}' {KB}/>"]
    x25 = ox + gw * 25 / 60
    C += [f"<path d='M{x25} {oy}L{x25} {oy-gh/2}L{ox} {oy-gh/2}' {KD}/>"]
    T += [lab(ox + gw / 2, oy - gh - 24, "U₁ / f₁ = constant (Φ = constant)", size=11, weight="bold", fill="#1d5fa8"),
          lab(ox + 30, oy - gh + 30, "400 V / 50 Hz = 8 V/Hz", "start", 8), lab(ox + 30, oy - gh + 42, "25 Hz → 200 V; 10 Hz → 80 V", "start", 8),
          lab(x25 + 6, oy - gh / 2 - 10, "200 V", "start", 8, fill="#1d5fa8"),
          lab(ox + gw * 50 / 60 - 40, oy - gh - 10, "f₁ > 50 Hz: U₁ = U₁N (slăbire de câmp)", "start", 7)]
    T += [lab(680, 300, "Fluxul magnetic Φ ≈ U₁ / (4,44 · f₁ · w₁ · kw₁). Dacă f₁ scade și U₁ rămâne constantă,", size=8),
          lab(680, 312, "Φ crește → saturația circuitului magnetic, curent de magnetizare mare, încălzire.", size=8)]
    save(f"{OUT}/18_formula_turatiei_Uf.svg", doc(W, H, A, C, T, title="Turația de sincronism, alunecarea și legea U/f"))

if __name__ == "__main__":
    for f in (curbe_ventilator, legi_similitudine, comparatie_putere, metode_reglare, monofilara_forta, schema_comanda,
              reglare_presiune, reglare_co2, mai_multe_ventilatoare, bypass, curba_uf, mod_incendiu, montaj_traductor,
              schema_grajd, curba_reglare_grajd, arbore_decizie, structura_convertizor, formula_turatie):
        f()
    print("ok", len(os.listdir(OUT)))
