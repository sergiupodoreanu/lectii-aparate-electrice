# MCB, MCCB, DDR (RCCB) și RCBO — fișă de curs

Material didactic pentru **Școala de maiștri electricieni**, modulul „Aparate electrice”.
Autor: Prof. Sergiu Podoreanu, Liceul Tehnologic „Grigore C. Moisil” Buzău.

Pagina se deschide direct din `index.html` (nu are nevoie de server sau de conexiune la internet, în afară de fonturile Google, care au fallback).

## Conținut

1. De ce avem nevoie de mai multe tipuri de aparate (supracurenți vs. curent de defect)
2. MCB — întreruptorul automat modular: construcție, declanșator termic și electromagnetic, curbe B/C/D, valori Icn
3. MCCB — întreruptorul în carcasă turnată: secțiune, reglaje Ir / Im / Isd, accesorii (MX, MN, motorizare)
4. DDR — dispozitivul diferențial: principiul torului, IΔn, tipuri AC / A / F / B, tip S
5. RCBO — întreruptorul diferențial combinat; schema RCCB comun vs. RCBO pe circuit
6. Selectivitatea dispozitivelor diferențiale (I7 fig. 4.2)
7. Tabel de sinteză și regulă de alegere
8. Test de verificare (10 întrebări)

Fiecare temă are caseta albastră cu articolele din **Normativul I7-2011** aplicabile
(4.1.4.1.11, 4.1.4.1.14, 4.1.5.2.1–4.1.5.2.8, 4.2.2.8, 4.2.2.9, 4.3.1–4.3.7, 5.3.4.0.3, 5.3.4.1.2, 5.3.4.3, 7.1.3.5, 7.5.2.1).

## Structura depozitului

```
index.html               fișa de curs (text, scheme SVG, test fără răspunsuri)
img/                16 fotografii (JPEG, max. 900 px lățime)
README.md
```

Schemele (fig. 1–6 și 2b) sunt desenate inline ca SVG și pot fi copiate în Inkscape.

## Fotografii și licențe

Toate fotografiile provin de pe **Wikimedia Commons**; sub fiecare fotografie din pagină este linkul către pagina sursă (File:…), autorul și licența. Rezumat:

| Fișier | Sursă (Wikimedia Commons) | Autor | Licență |
|---|---|---|---|
| foto01-mcb-inchis.jpg | File:Circuit_breaker_structure_ON.JPG | Kae | CC BY-SA 3.0 |
| foto02-mcb-deschis.jpg | File:Circuit_breaker_structure_OFF.JPG | Kae | CC BY-SA 3.0 |
| foto03-mcb-repere.jpg | File:Circuitbreaker.jpg | Ali@gwc.org.uk | CC BY-SA 2.5 |
| foto04-camera-stingere.jpg | File:Arc_chute_from_MCB.JPG | Dmitry G | CC BY-SA 3.0 |
| foto05-bimetal.jpg | File:Bimetallic_strip_from_circuit_breaker.JPG | Dmitry G | CC BY-SA 3.0 |
| foto06-bobina.jpg | File:Coil_from_circuit_breaker.JPG | Dmitry G | CC BY-SA 3.0 |
| foto07-mccb-ns250n.jpg | File:MCCB_Merlin_Gerin_compact_NS250N_(front_side).jpg | Pui108108 | CC BY 4.0 |
| foto08-mccb-tmax-630a.jpg | File:630_Amps_Molded_Case_Circuit_Breaker.jpg | Balurbala | CC BY-SA 3.0 |
| foto09-mccb-deschis.jpg | File:MCCB_3P3E_30A_inside.jpg | BnonB | CC BY-SA 4.0 |
| foto10-bobina-mx.jpg | File:Circuit_breaker_IMG_8455.JPG | 01x07x2022000 | CC0 |
| foto11-rccb-exterior.jpg | File:Residual_current_device_2pole.jpg | Jimbob82 | domeniu public |
| foto12-rccb-deschis.jpg | File:Old_Rccb_Breaker.jpg | Devinda Vimesh | CC BY-SA 4.0 |
| foto13-rccb-repere.jpg | File:ResidualCurrentCircuitBreak.jpg | Ali@gwc.org.uk | CC BY-SA 3.0 |
| foto14-releu-ddr.jpg | File:Fi_relé_leoldó_elektromechanikai_modulja.jpg | Szab | domeniu public |
| foto15-rcbo-idpn-vigi.jpg | File:Schneider_Electric_A9D31620.JPG | Dmitry G | CC BY-SA 3.0 |
| foto16-rcbo-deschis.jpg | File:SB_3W_30A_inside.jpg | BnonA | CC BY-SA 4.0 |

Fotografiile au fost redimensionate (max. 900 px) și recomprimate; conținutul nu a fost modificat.

## Licența materialului

Textul și schemele: © Sergiu Podoreanu, publicate sub licența
[Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.ro) —
pot fi folosite și adaptate în scop didactic cu menționarea autorului și păstrarea aceleiași licențe.
Fotografiile își păstrează licențele individuale din tabelul de mai sus.

## Bibliografie

- Normativ I7-2011 pentru proiectarea, execuția și exploatarea instalațiilor electrice aferente clădirilor (Ordinul MDRT 2741/2011, M.Of. 802 bis/2011), completat prin Ordinul 959/2023
- SR EN 60898-1 (MCB), SR EN 60947-2 (MCCB, DDR industriale), SR EN 61008-1 (RCCB), SR EN 61009-1 (RCBO), SR EN 62423 (DDR tip F și B)
- Schneider Electric, *Electrical Installation Guide*, cap. H — https://www.electrical-installation.org
- Schneider Electric, *What is the difference between MCB, MCCB, RCB, RCD, RCCB and RCBO?* (punct de plecare; valorile au fost verificate după standardele SR EN)
