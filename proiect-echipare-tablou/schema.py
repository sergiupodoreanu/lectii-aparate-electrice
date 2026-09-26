#!/usr/bin/env python3
# Schema monofilară „T.E. LOCUINȚĂ” — temă de proiect, Școala de maiștri electricieni
# Generează: schema_monofilara.svg (A3, mm, straturi Inkscape), varianta cu rezolvare, și datele circuitelor (JSON)
import json, math, sys

# ---------------- date ----------------
U0, UL = 230, 400
circuits = [
 # cod, destinație, Pi[kW], cosφ, trifazat, cablu, aparat, poli, In, curbă, IΔn, tip, fază, grup RCCB
 dict(cod='CL1', dest='Iluminat parter',            Pi=0.8, cosf=0.9, tri=False, cablu='CYY-F 3×1,5', ap='RCBO', poli='1P+N', In=10, curba='B', idn=30, tip='A',  faza='L1', grp=None),
 dict(cod='CL2', dest='Iluminat etaj',              Pi=0.6, cosf=0.9, tri=False, cablu='CYY-F 3×1,5', ap='RCBO', poli='1P+N', In=10, curba='B', idn=30, tip='A',  faza='L2', grp=None),
 dict(cod='CP1', dest='Prize parter',               Pi=2.0, cosf=0.8, tri=False, cablu='CYY-F 3×2,5', ap='RCBO', poli='1P+N', In=16, curba='C', idn=30, tip='A',  faza='L3', grp=None),
 dict(cod='CP2', dest='Prize etaj',                 Pi=2.0, cosf=0.8, tri=False, cablu='CYY-F 3×2,5', ap='RCBO', poli='1P+N', In=16, curba='C', idn=30, tip='A',  faza='L1', grp=None),
 dict(cod='CP3', dest='Prize bucătărie',            Pi=2.5, cosf=0.8, tri=False, cablu='CYY-F 3×2,5', ap='RCBO', poli='1P+N', In=16, curba='C', idn=30, tip='A',  faza='L2', grp=None),
 dict(cod='CF1', dest='Plită electrică',            Pi=7.0, cosf=1.0, tri=True,  cablu='CYY-F 5×2,5', ap='MCB',  poli='3P+N', In=16, curba='C', idn=None, tip=None, faza='L1,L2,L3', grp='D6'),
 dict(cod='CF2', dest='Cuptor electric',            Pi=3.5, cosf=1.0, tri=False, cablu='CYY-F 3×2,5', ap='MCB',  poli='1P+N', In=16, curba='C', idn=None, tip=None, faza='L3', grp='D6'),
 dict(cod='CF3', dest='Boiler electric',            Pi=2.0, cosf=1.0, tri=False, cablu='CYY-F 3×2,5', ap='RCBO', poli='1P+N', In=16, curba='C', idn=30, tip='A',  faza='L3', grp=None),
 dict(cod='CF4', dest='Aer condiționat (invertor)', Pi=2.5, cosf=0.85,tri=False, cablu='CYY-F 3×2,5', ap='RCBO', poli='1P+N', In=16, curba='C', idn=30, tip='F',  faza='L1', grp=None),
 dict(cod='CF5', dest='Stație încărcare auto 11 kW',Pi=11.0,cosf=1.0, tri=True,  cablu='CYY-F 5×4',   ap='MCB',  poli='3P+N', In=20, curba='C', idn=None, tip=None, faza='L1,L2,L3', grp='D11'),
 dict(cod='R',   dest='Rezervă',                    Pi=2.0, cosf=0.8, tri=False, cablu='—',           ap='RCBO', poli='1P+N', In=16, curba='C', idn=30, tip='A',  faza='L2', grp=None),
]
groups = {  # RCCB comune
 'D6':  dict(poli='4P', In=40, idn=30, tip='A', nota='RCCB 4P 40 A / 30 mA tip A — pentru CF1 + CF2'),
 'D11': dict(poli='4P', In=25, idn=30, tip='B', nota='RCCB 4P 25 A / 30 mA tip B — pentru CF5 (stație încărcare)'),
}
for c in circuits:
    c['Ic'] = c['Pi']*1000/(math.sqrt(3)*UL*c['cosf']) if c['tri'] else c['Pi']*1000/(U0*c['cosf'])
Pi = sum(c['Pi'] for c in circuits if c['cod']!='R')
ks = 0.45
Pa = Pi*ks
Ic_gen = Pa*1000/(math.sqrt(3)*UL*0.9)
head = dict(Pi=Pi, Pa=Pa, Ic=Ic_gen, alim='CYY-F 5×10 mm² de la BMPM 3×32 A', Isc='4,8 kA (din avizul de racordare)')

# poziții aparate (D0 … D12)
pos = [
 ('D0','Descărcător de supratensiuni SPD tip 2, 4P (3P+N), Imax 40 kA, Up ≤ 1,5 kV'),
 ('D1','Separator de sarcină 4P, In = 40 A'),
]
n=2
dev_of = {}
for c in circuits:
    if c['grp']:
        if c['grp'] not in dev_of:
            g=groups[c['grp']]; dev_of[c['grp']]=c['grp']
            pos.append((c['grp'], f"Întreruptor diferențial (RCCB) {g['poli']}, In = {g['In']} A, IΔn = {g['idn']} mA, tip {g['tip']}"))
    d=f'D{n}'; n+=1
    while d in groups: d=f'D{n}'; n+=1
    c['dev']=d
    if c['ap']=='RCBO':
        pos.append((d, f"Întreruptor automat diferențial (RCBO) {c['poli']}, In = {c['In']} A, curba {c['curba']}, IΔn = {c['idn']} mA, tip {c['tip']}, 6 kA"))
    else:
        pos.append((d, f"Întreruptor automat (MCB) {c['poli']}, In = {c['In']} A, curba {c['curba']}, 6 kA"))
json.dump(dict(circuits=circuits, groups=groups, head=head, pos=pos), open('date.json','w'), ensure_ascii=False, indent=1, default=float)

# ---------------- desen ----------------
W,H = 420,297
FS = 'font-family="Arial, Liberation Sans, sans-serif"'
lay_ap, lay_cd, lay_tx = [], [], []
def L(x1,y1,x2,y2,w=0.35): lay_cd.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#000" stroke-width="{w}"/>')
def T(x,y,s,size=2.6,anchor='start',bold=False,layer=None,rot=0):
    b=' font-weight="bold"' if bold else ''
    r=f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ''
    (layer if layer is not None else lay_tx).append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" {FS}{b}{r}>{s}</text>')
def cond_mark(x,y,n):  # marcaj număr conductoare
    lay_cd.append(f'<line x1="{x-1.5:.2f}" y1="{y+1.5:.2f}" x2="{x+1.5:.2f}" y2="{y-1.5:.2f}" stroke="#000" stroke-width="0.35"/>')
    T(x+2,y+0.8,str(n),2.2)

def g_open(label): return f'<g inkscape:label="{label}">'
def sym_breaker(x,y,label_lines,diff=None,sw_only=False,name=''):
    """Simbol întreruptor automat (contact + ×) sau întreruptor (fără ×); diff = text tor."""
    g=[g_open(name)]
    g.append(f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{x:.2f}" y2="{y+2:.2f}" stroke="#000" stroke-width="0.35"/>')
    if not sw_only:  # × la contactul fix
        g.append(f'<line x1="{x-1.2:.2f}" y1="{y+0.8:.2f}" x2="{x+1.2:.2f}" y2="{y+3.2:.2f}" stroke="#000" stroke-width="0.35"/>')
        g.append(f'<line x1="{x+1.2:.2f}" y1="{y+0.8:.2f}" x2="{x-1.2:.2f}" y2="{y+3.2:.2f}" stroke="#000" stroke-width="0.35"/>')
    g.append(f'<line x1="{x:.2f}" y1="{y+9:.2f}" x2="{x+3.2:.2f}" y2="{y+2.6:.2f}" stroke="#000" stroke-width="0.5"/>')
    g.append(f'<line x1="{x:.2f}" y1="{y+9:.2f}" x2="{x:.2f}" y2="{y+11:.2f}" stroke="#000" stroke-width="0.35"/>')
    yy=y+2.5
    for s in label_lines:
        g.append(f'<text x="{x+4.5:.2f}" y="{yy:.2f}" font-size="2.3" {FS}>{s}</text>'); yy+=2.8
    if diff:
        g.append(f'<ellipse cx="{x:.2f}" cy="{y+13.5:.2f}" rx="2.2" ry="1.4" fill="none" stroke="#000" stroke-width="0.35"/>')
        g.append(f'<line x1="{x:.2f}" y1="{y+11:.2f}" x2="{x:.2f}" y2="{y+12.1:.2f}" stroke="#000" stroke-width="0.35"/>')
        g.append(f'<line x1="{x:.2f}" y1="{y+14.9:.2f}" x2="{x:.2f}" y2="{y+16:.2f}" stroke="#000" stroke-width="0.35"/>')
        if diff!='x': g.append(f'<text x="{x+4.5:.2f}" y="{y+14.4:.2f}" font-size="2.3" {FS}>{diff}</text>')
    g.append('</g>'); lay_ap.append('\n'.join(g))
    return y+(16 if diff else 11)
def sym_switch_disc(x,y,label_lines,name=''):
    g=[g_open(name)]
    g.append(f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{x:.2f}" y2="{y+2:.2f}" stroke="#000" stroke-width="0.35"/>')
    g.append(f'<line x1="{x-1.5:.2f}" y1="{y+2:.2f}" x2="{x+1.5:.2f}" y2="{y+2:.2f}" stroke="#000" stroke-width="0.5"/>')  # bară separator
    g.append(f'<line x1="{x:.2f}" y1="{y+9:.2f}" x2="{x+3.2:.2f}" y2="{y+2.6:.2f}" stroke="#000" stroke-width="0.5"/>')
    g.append(f'<circle cx="{x:.2f}" cy="{y+9.4:.2f}" r="0.7" fill="none" stroke="#000" stroke-width="0.35"/>')  # rupere în sarcină
    g.append(f'<line x1="{x:.2f}" y1="{y+10.1:.2f}" x2="{x:.2f}" y2="{y+11:.2f}" stroke="#000" stroke-width="0.35"/>')
    yy=y+2.5
    for s in label_lines:
        g.append(f'<text x="{x+4.5:.2f}" y="{yy:.2f}" font-size="2.3" {FS}>{s}</text>'); yy+=2.8
    g.append('</g>'); lay_ap.append('\n'.join(g)); return y+11
def sym_spd(x,y,name='D0'):
    g=[g_open(name)]
    g.append(f'<rect x="{x-2:.2f}" y="{y:.2f}" width="4" height="8" fill="none" stroke="#000" stroke-width="0.35"/>')
    g.append(f'<line x1="{x-1.2:.2f}" y1="{y+6.5:.2f}" x2="{x+1.2:.2f}" y2="{y+1.5:.2f}" stroke="#000" stroke-width="0.35"/>')
    g.append(f'<polygon points="{x+1.2:.2f},{y+1.5:.2f} {x-0.2:.2f},{y+2.2:.2f} {x+1.2:.2f},{y+3.2:.2f}" fill="#000"/>')
    g.append(f'<line x1="{x:.2f}" y1="{y+8:.2f}" x2="{x:.2f}" y2="{y+11:.2f}" stroke="#000" stroke-width="0.35"/>')
    for i,w in enumerate((3,2,1)):
        g.append(f'<line x1="{x-w:.2f}" y1="{y+11+i*0.9:.2f}" x2="{x+w:.2f}" y2="{y+11+i*0.9:.2f}" stroke="#000" stroke-width="0.35"/>')
    for i,s in enumerate(['D0','SPD tip 2, 4P','Imax 40 kA','Up ≤ 1,5 kV']):
        g.append(f'<text x="{x-4:.2f}" y="{y+2+i*2.8:.2f}" font-size="2.3" text-anchor="end" {FS}>{s}</text>')
    g.append('</g>'); lay_ap.append('\n'.join(g))

# --- alimentare + D1 ---
x0, ytop = 60, 28
T(x0-2, ytop-8, head['alim'], 2.6, 'start', True)
T(x0-2, ytop-4, 'de la BMPM', 2.6)
L(x0, ytop, x0, ytop+8)
cond_mark(x0, ytop+5, 5)
yb = sym_switch_disc(x0, ytop+8, ['D1','4P','40 A'], name='D1 separator de sarcină')
L(x0, yb, x0, 70)
# cartuș date tablou
lay_tx.append(f'<rect x="{x0+18}" y="{ytop-2}" width="64" height="22" fill="none" stroke="#000" stroke-width="0.35"/>')
for i,s in enumerate(['T.E. LOCUINȚĂ  (P+1, trifazat)', f"Pi = {head['Pi']:.1f} kW", f"Pa = {head['Pa']:.1f} kW  (ks = {ks})", f"Ic = {head['Ic']:.1f} A", f"Isc la BMPM = {head['Isc']}"]):
    T(x0+20, ytop+2+i*4, s, 2.6, bold=(i==0))
# SPD pe bară, în stânga
ybus = 70
xs = x0-22
L(xs, ybus, x0, ybus)
L(xs, ybus, xs, ybus+2)
sym_spd(xs, ybus+2)
# bara principală
xstart = x0
step = 27
# calcul poziții pe X pentru fiecare plecare (grupurile ocupă 2 poziții)
xs_list=[]; x=x0+18
i=0
order=[]  # elemente: ('single', c) sau ('group', gid, [c,c])
seen=set()
for c in circuits:
    if c['grp']:
        if c['grp'] in seen: continue
        seen.add(c['grp']); members=[m for m in circuits if m['grp']==c['grp']]
        order.append(('group',c['grp'],members))
    else: order.append(('single',c))
xend = x0+18+step*(sum(len(o[2]) if o[0]=='group' else 1 for o in order)-1)
L(x0, ybus, xend, ybus, 0.7)
cond_mark(x0+6, ybus, 5)
ytab = 165
xcol = {}
for o in order:
    if o[0]=='single':
        c=o[1]; xc=x; xcol[c['cod']]=xc; x+=step
        L(xc, ybus, xc, ybus+8)
        cond_mark(xc, ybus+5, 5 if c['tri'] else 3)
        lab=[c['dev'], c['poli'], f"{c['curba']}{c['In']}", '6 kA']
        diff=f"{c['idn']} mA tip {c['tip']}" if c['ap']=='RCBO' else None
        yb=sym_breaker(xc, ybus+8, lab, diff, name=f"{c['dev']} {c['cod']}")
        L(xc, yb, xc, ytab-6)
        cond_mark(xc, ytab-14, 5 if c['tri'] else 3)
    else:
        gid, members = o[1], o[2]; g=groups[gid]
        xg = x + step*(len(members)-1)/2
        L(xg, ybus, xg, ybus+8); cond_mark(xg, ybus+5, 5)
        yb=sym_breaker(xg, ybus+8, [gid, g['poli'], f"{g['In']} A"], f"{g['idn']} mA tip {g['tip']}", sw_only=True, name=f"{gid} RCCB comun")
        ysub = yb+6
        L(xg, yb, xg, ysub)
        L(x, ysub, x+step*(len(members)-1), ysub, 0.5)
        for m in members:
            xc=x; xcol[m['cod']]=xc; x+=step
            L(xc, ysub, xc, ysub+6)
            cond_mark(xc, ysub+3.5, 5 if m['tri'] else 3)
            yb2=sym_breaker(xc, ysub+6, [m['dev'], m['poli'], f"{m['curba']}{m['In']}", '6 kA'], None, name=f"{m['dev']} {m['cod']}")
            L(xc, yb2, xc, ytab-6)
            cond_mark(xc, ytab-14, 5 if m['tri'] else 3)
# bară PE
ype = ytab-3
L(x0-30, ype, xend+12, ype, 0.7); T(x0-34, ype+1, 'PE', 2.6, 'end', True)
for i,w in enumerate((3,2,1)): L(xend+12-w, ype+i*0.9+1, xend+12+w, ype+i*0.9+1)
# tabel circuite
rows=[('Circuit',lambda c:c['cod']),('Pi [kW]',lambda c:f"{c['Pi']:g}"),('cos φ',lambda c:f"{c['cosf']:g}"),('Ic [A]',lambda c:f"{c['Ic']:.1f}"),('Cablu [mm²]',lambda c:c['cablu']),
      ('Protecție',lambda c:(f"{c['poli']} {c['curba']}{c['In']}"+(f"/{c['idn']}mA" if c['idn'] else f" (sub {c['grp']})"))),('Faza',lambda c:c['faza']),('Destinație',lambda c:c['dest'])]
rh=6; xl=x0-30; xr=xend+12
lay_tx.append(f'<rect x="{xl}" y="{ytab}" width="{xr-xl}" height="{rh*len(rows)}" fill="none" stroke="#000" stroke-width="0.5"/>')
for i,(name,fn) in enumerate(rows):
    yy=ytab+rh*i
    if i: L(xl,yy,xr,yy,0.3)
    T(xl+2, yy+4.2, name, 2.4, bold=True)
    for c in circuits:
        s=fn(c); fs=2.3 if len(s)<16 else 1.9
        if name=='Destinație' and len(s)>14:
            parts=s.split(' '); half=len(parts)//2
            T(xcol[c['cod']], yy+3.0, ' '.join(parts[:half]), 1.8, 'middle'); T(xcol[c['cod']], yy+5.2, ' '.join(parts[half:]), 1.8, 'middle')
        else: T(xcol[c['cod']], yy+4.2, s, fs, 'middle')
L(xl+26, ytab, xl+26, ytab+rh*len(rows), 0.3)
for c in circuits: L(xcol[c['cod']]+step/2, ytab, xcol[c['cod']]+step/2, ytab+rh*len(rows), 0.3) if xcol[c['cod']]+step/2 < xr else None


# legendă simboluri (sub tabel)
lx, ly = 18, 218
lay_tx.append(f'<rect x="{lx}" y="{ly}" width="228" height="60" fill="none" stroke="#000" stroke-width="0.4"/>')
T(lx+3, ly+5, 'LEGENDĂ SIMBOLURI', 2.6, bold=True)
sym_switch_disc(lx+8, ly+8, [], name='legendă separator'); T(lx+16, ly+15, 'separator de sarcină', 2.2); T(lx+16, ly+19, '(întreruptor-separator)', 2.0)
sym_breaker(lx+8, ly+23, [], None, name='legendă MCB'); T(lx+16, ly+30, 'întreruptor automat (MCB)', 2.2); T(lx+16, ly+34, '× = declanșator la supracurent', 2.0)
sym_breaker(lx+8, ly+38, [], 'x', name='legendă RCBO'); T(lx+16, ly+46, 'întreruptor automat diferențial (RCBO)', 2.2); T(lx+16, ly+50, 'ovalul = torul diferențial (IΔn, tip)', 2.0)
sym_breaker(lx+88, ly+8, [], 'x', sw_only=True, name='legendă RCCB'); T(lx+96, ly+16, 'întreruptor diferențial (RCCB)', 2.2); T(lx+96, ly+20, 'fără × — nu are declanșator la supracurent', 2.0)
cond_mark(lx+88, ly+34, 3); T(lx+96, ly+35, 'număr de conductoare (3 = L+N+PE, 5 = 3L+N+PE)', 2.2)
lay_tx.append(f'<rect x="{lx+86}" y="{ly+40}" width="4" height="8" fill="none" stroke="#000" stroke-width="0.35"/><line x1="{lx+86.8}" y1="{ly+46.5}" x2="{lx+89.2}" y2="{ly+41.5}" stroke="#000" stroke-width="0.35"/>')
T(lx+96, ly+46, 'descărcător de supratensiuni (SPD)', 2.2)
T(lx+150, ly+16, 'Simboluri conform SR EN 60617 (simplificate,', 2.0); T(lx+150, ly+20, 'ca în planșele de proiect uzuale)', 2.0)
# chenar + indicator
lay_tx.append(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="#000" stroke-width="0.7"/>')
ind_y=H-8-30
lay_tx.append(f'<rect x="{W-8-150}" y="{ind_y}" width="150" height="30" fill="none" stroke="#000" stroke-width="0.5"/>')
L(W-8-150, ind_y+10, W-8, ind_y+10, 0.3); L(W-8-150, ind_y+20, W-8, ind_y+20, 0.3); L(W-8-60, ind_y, W-8-60, ind_y+30, 0.3)
T(W-8-148, ind_y+7, 'Liceul Tehnologic „Grigore C. Moisil” Buzău · Școala de maiștri electricieni', 2.4)
T(W-8-148, ind_y+17, 'TEMĂ DE PROIECT — Echiparea tabloului electric T.E. LOCUINȚĂ', 2.6, bold=True)
T(W-8-148, ind_y+27, 'Schema monofilară (schema electrică de distribuție)', 2.4)
T(W-8-58, ind_y+7, 'Planșa 1 / format A3', 2.4); T(W-8-58, ind_y+17, 'Elev: ______________________', 2.4); T(W-8-58, ind_y+27, 'Prof. Sergiu Podoreanu · 2026', 2.4)
T(12, H-12, 'Notă: numerele de pe marcajele oblice = numărul de conductoare (3 = L+N+PE, 5 = L1+L2+L3+N+PE). Toate aparatele modulare: SR EN 60898-1 / 61008-1 / 61009-1, 230/400 V, 50 Hz.', 2.2)

def layer(name, items):
    return f'<g inkscape:groupmode="layer" inkscape:label="{name}" id="{name}">\n' + '\n'.join(items) + '\n</g>'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" version="1.1">
<sodipodi:namedview inkscape:document-units="mm" pagecolor="#ffffff"/>
<rect width="{W}" height="{H}" fill="#fff"/>
{layer('Conductoare', lay_cd)}
{layer('Aparate', lay_ap)}
{layer('Text', lay_tx)}
</svg>'''
open('schema_monofilara.svg','w',encoding='utf-8').write(svg)
print('ok', head, len(pos), 'poziții')
