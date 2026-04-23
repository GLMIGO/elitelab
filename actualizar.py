#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ELITE LAB PRO — Actualizador automático
Corre diariamente via GitHub Actions.
Vai buscar classificações ao Sofascore e actualiza o index.html
"""

import json, re, os, sys, time, urllib.request, urllib.error
from datetime import date, datetime

# ═══════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════

HTML_FILE = "index.html"

LIGAS = {
    "La Liga":        {"tid": 8,   "sid": 61643},
    "Premier League": {"tid": 17,  "sid": 61627},
    "Bundesliga":     {"tid": 35,  "sid": 61644},
    "Serie A":        {"tid": 23,  "sid": 61645},
    "Ligue 1":        {"tid": 34,  "sid": 61646},
    "Eredivisie":     {"tid": 37,  "sid": 61647},
    "Liga Portugal":  {"tid": 238, "sid": 61648},
}

NOMES = {
    "Barcelona":"Barcelona","Real Madrid":"Real Madrid","Villarreal":"Villarreal",
    "Atletico Madrid":"Atlético Madrid","Atletico de Madrid":"Atlético Madrid",
    "Real Betis":"Real Betis","Celta Vigo":"Celta Vigo","Real Sociedad":"Real Sociedad",
    "Getafe":"Getafe","Osasuna":"Osasuna","Espanyol":"Espanyol",
    "Athletic Club":"Athletic Bilbao","Girona":"Girona","Rayo Vallecano":"Rayo Vallecano",
    "Valencia":"Valencia","Mallorca":"Mallorca","Sevilla":"Sevilla",
    "Alaves":"Alavés","Deportivo Alaves":"Alavés","Elche":"Elche",
    "Levante":"Levante","Oviedo":"Oviedo","Real Oviedo":"Oviedo",
    "Arsenal":"Arsenal","Manchester City":"Manchester City",
    "Manchester United":"Manchester United","Aston Villa":"Aston Villa",
    "Liverpool":"Liverpool","Chelsea":"Chelsea","Brentford":"Brentford",
    "Bournemouth":"Bournemouth","Brighton":"Brighton","Everton":"Everton",
    "Sunderland":"Sunderland","Fulham":"Fulham","Crystal Palace":"Crystal Palace",
    "Newcastle United":"Newcastle United","Leeds United":"Leeds United",
    "Nottingham Forest":"Nottingham Forest","West Ham":"West Ham United",
    "West Ham United":"West Ham United","Tottenham":"Tottenham Hotspur",
    "Tottenham Hotspur":"Tottenham Hotspur","Burnley":"Burnley",
    "Wolverhampton":"Wolverhampton","Wolverhampton Wanderers":"Wolverhampton",
    "Bayern Munich":"Bayern München","Borussia Dortmund":"Borussia Dortmund",
    "Hoffenheim":"TSG Hoffenheim","TSG Hoffenheim":"TSG Hoffenheim",
    "Stuttgart":"VfB Stuttgart","VfB Stuttgart":"VfB Stuttgart",
    "RB Leipzig":"RB Leipzig","Leverkusen":"Bayer Leverkusen",
    "Bayer Leverkusen":"Bayer Leverkusen","Eintracht Frankfurt":"Eintracht Frankfurt",
    "Freiburg":"SC Freiburg","SC Freiburg":"SC Freiburg",
    "Augsburg":"FC Augsburg","FC Augsburg":"FC Augsburg",
    "Union Berlin":"Union Berlin","Hamburger SV":"Hamburger SV",
    "Borussia M'gladbach":"Borussia Mönchengladbach",
    "Borussia Monchengladbach":"Borussia Mönchengladbach",
    "Borussia Mönchengladbach":"Borussia Mönchengladbach",
    "Werder Bremen":"Werder Bremen","Mainz":"Mainz","Mainz 05":"Mainz",
    "Koln":"1. FC Köln","FC Koln":"1. FC Köln","1. FC Köln":"1. FC Köln",
    "Wolfsburg":"Wolfsburg","VfL Wolfsburg":"Wolfsburg",
    "St. Pauli":"FC St. Pauli","FC St. Pauli":"FC St. Pauli",
    "Heidenheim":"1. FC Heidenheim","1. FC Heidenheim":"1. FC Heidenheim",
    "Internazionale":"Inter Milan","Inter":"Inter Milan","Inter Milan":"Inter Milan",
    "Napoli":"Napoli","AC Milan":"AC Milan","Milan":"AC Milan",
    "Juventus":"Juventus","Como":"Como","Como 1907":"Como",
    "Roma":"Roma","AS Roma":"Roma","Atalanta":"Atalanta","Bologna":"Bologna",
    "Lazio":"Lazio","Udinese":"Udinese","Sassuolo":"Sassuolo","Torino":"Torino",
    "Genoa":"Genoa","Parma":"Parma","Fiorentina":"Fiorentina","Cagliari":"Cagliari",
    "Cremonese":"Cremonese","US Cremonese":"Cremonese","Lecce":"Lecce",
    "Hellas Verona":"Hellas Verona","Verona":"Hellas Verona","Pisa":"Pisa",
    "Paris Saint-Germain":"PSG","PSG":"PSG","Marseille":"Marseille","Monaco":"Monaco",
    "Lille":"Lille","Lyon":"Lyon","Lens":"Lens","RC Lens":"Lens",
    "Nice":"Nice","OGC Nice":"Nice","Rennes":"Rennes","Strasbourg":"Strasbourg",
    "Brest":"Brest","Toulouse":"Toulouse","Auxerre":"Auxerre","AJ Auxerre":"Auxerre",
    "Nantes":"Nantes","Reims":"Reims","Le Havre":"Havre","Havre":"Havre",
    "Angers":"Angers","Montpellier":"Montpellier",
    "Saint-Etienne":"Saint-Étienne","Saint-Étienne":"Saint-Étienne",
    "PSV":"PSV Eindhoven","PSV Eindhoven":"PSV Eindhoven","Ajax":"Ajax",
    "Feyenoord":"Feyenoord","AZ":"AZ","AZ Alkmaar":"AZ",
    "NEC":"NEC","NEC Nijmegen":"NEC","Twente":"Twente","FC Twente":"Twente",
    "Utrecht":"Utrecht","FC Utrecht":"Utrecht",
    "Sparta Rotterdam":"Sparta Rotterdam","Go Ahead Eagles":"Go Ahead Eagles",
    "Heerenveen":"Heerenveen","SC Heerenveen":"Heerenveen","NAC Breda":"NAC Breda",
    "Heracles":"Heracles Almelo","Heracles Almelo":"Heracles Almelo",
    "PEC Zwolle":"PEC Zwolle","Fortuna Sittard":"Fortuna Sittard","Volendam":"Volendam",
    "Groningen":"Groningen","Excelsior":"Excelsior","Telstar":"Telstar",
    "FC Porto":"Porto","Porto":"Porto","Sporting CP":"Sporting CP","Sporting":"Sporting CP",
    "Benfica":"Benfica","SL Benfica":"Benfica","Braga":"Braga","SC Braga":"Braga",
    "Vitoria Guimaraes":"Vitória Guimarães","Vitoria SC":"Vitória Guimarães",
    "Vitória Guimarães":"Vitória Guimarães","Gil Vicente":"Gil Vicente",
    "Famalicao":"Famalicão","Famalicão":"Famalicão","Moreirense":"Moreirense",
    "Estoril":"Estoril Praia","Estoril Praia":"Estoril Praia","Santa Clara":"Santa Clara",
    "Casa Pia":"Casa Pia","Rio Ave":"Rio Ave","Arouca":"Arouca","Nacional":"Nacional",
    "Estrela Amadora":"Estrela da Amadora","Estrela da Amadora":"Estrela da Amadora",
    "CF Estrela":"Estrela da Amadora","Tondela":"Tondela",
    "Alverca":"Alverca","FC Alverca":"Alverca","AVS":"AVS","AVS Futebol":"AVS",
}

ZONAS = {
    "La Liga":        {"cl":4,"el":1,"ecl":1,"po":0,"releg":3,"total":20},
    "Premier League": {"cl":4,"el":1,"ecl":1,"po":0,"releg":3,"total":20},
    "Bundesliga":     {"cl":4,"el":1,"ecl":1,"po":1,"releg":2,"total":18},
    "Serie A":        {"cl":4,"el":1,"ecl":1,"po":0,"releg":3,"total":20},
    "Ligue 1":        {"cl":3,"el":1,"ecl":1,"po":1,"releg":2,"total":18},
    "Eredivisie":     {"cl":2,"el":1,"ecl":2,"po":1,"releg":2,"total":18},
    "Liga Portugal":  {"cl":1,"el":1,"ecl":1,"po":1,"releg":3,"total":18},
}

XG = {
    "Barcelona":(2.46,0.97),"Real Madrid":(2.21,0.93),"Villarreal":(1.61,1.16),
    "Atlético Madrid":(1.54,1.03),"Real Betis":(1.52,1.23),"Celta Vigo":(1.39,1.29),
    "Real Sociedad":(1.33,1.55),"Getafe":(0.90,1.03),"Osasuna":(1.37,1.23),
    "Espanyol":(1.42,1.55),"Athletic Bilbao":(1.56,1.45),"Girona":(1.22,1.45),
    "Rayo Vallecano":(1.48,1.23),"Valencia":(1.43,1.48),"Mallorca":(1.30,1.55),
    "Sevilla":(1.19,1.65),"Alavés":(1.28,1.48),"Elche":(1.28,1.52),
    "Levante":(1.24,1.61),"Oviedo":(1.09,1.77),
    "Arsenal":(2.12,0.94),"Manchester City":(2.19,1.09),"Manchester United":(1.67,1.27),
    "Aston Villa":(1.58,1.39),"Liverpool":(1.82,1.48),"Chelsea":(1.76,1.42),
    "Brentford":(1.58,1.45),"Bournemouth":(1.64,1.64),"Brighton":(1.67,1.48),
    "Everton":(1.45,1.42),"Sunderland":(1.52,1.64),"Fulham":(1.48,1.58),
    "Crystal Palace":(1.34,1.38),"Newcastle United":(1.39,1.48),
    "Leeds United":(1.45,1.67),"Nottingham Forest":(1.21,1.48),
    "West Ham United":(1.15,1.67),"Tottenham Hotspur":(1.27,1.61),
    "Burnley":(0.91,1.88),"Wolverhampton":(0.85,2.06),
    "Bayern München":(3.73,0.97),"Borussia Dortmund":(1.83,0.93),
    "TSG Hoffenheim":(1.83,1.17),"VfB Stuttgart":(1.77,1.27),
    "RB Leipzig":(1.80,1.30),"Bayer Leverkusen":(1.67,1.20),
    "Eintracht Frankfurt":(1.80,1.83),"SC Freiburg":(1.30,1.53),
    "FC Augsburg":(1.23,1.63),"Union Berlin":(1.20,1.60),
    "Hamburger SV":(1.17,1.53),"Borussia Mönchengladbach":(1.27,1.73),
    "Werder Bremen":(1.23,1.77),"Mainz":(1.07,1.70),"1. FC Köln":(1.03,1.80),
    "Wolfsburg":(0.97,1.90),"FC St. Pauli":(0.87,2.10),"1. FC Heidenheim":(0.80,2.00),
    "Inter Milan":(2.44,1.00),"Napoli":(2.03,1.50),"AC Milan":(1.88,1.25),
    "Juventus":(1.72,0.91),"Como":(2.09,1.16),"Roma":(1.81,1.28),
    "Atalanta":(1.84,1.34),"Bologna":(1.56,1.41),"Lazio":(1.63,1.56),
    "Udinese":(1.38,1.50),"Sassuolo":(1.44,1.56),"Torino":(1.19,1.72),
    "Genoa":(1.09,1.31),"Parma":(1.16,1.69),"Fiorentina":(1.22,1.44),
    "Cagliari":(1.03,1.38),"Cremonese":(0.88,1.53),"Lecce":(0.91,1.66),
    "Hellas Verona":(0.81,1.81),"Pisa":(0.69,2.09),
    "PSG":(2.73,0.80),"Marseille":(2.13,1.03),"Monaco":(2.03,1.10),
    "Lille":(1.70,1.17),"Lyon":(1.53,1.23),"Lens":(1.33,1.23),
    "Nice":(1.27,1.30),"Rennes":(1.20,1.33),"Strasbourg":(1.13,1.37),
    "Brest":(1.07,1.40),"Toulouse":(0.93,1.40),"Auxerre":(0.87,1.47),
    "Nantes":(0.80,1.53),"Reims":(0.73,1.57),"Havre":(0.70,1.67),
    "Angers":(0.60,1.80),"Montpellier":(0.53,1.90),"Saint-Étienne":(0.50,2.07),
    "PSV Eindhoven":(3.28,0.79),"Ajax":(2.66,1.03),"Feyenoord":(2.52,1.10),
    "AZ":(2.14,1.17),"NEC":(1.62,1.31),"Twente":(1.52,1.34),
    "Utrecht":(1.38,1.38),"Sparta Rotterdam":(1.21,1.45),
    "Go Ahead Eagles":(1.10,1.45),"Heerenveen":(1.03,1.52),
    "NAC Breda":(0.97,1.59),"Heracles Almelo":(0.90,1.66),
    "PEC Zwolle":(0.83,1.72),"Fortuna Sittard":(0.76,1.79),
    "Volendam":(0.69,1.86),"Groningen":(0.62,2.00),
    "Excelsior":(0.59,2.24),"Telstar":(0.52,2.52),
    "Porto":(1.83,0.33),"Sporting CP":(2.33,0.50),"Benfica":(1.90,0.60),
    "Braga":(1.83,0.87),"Vitória Guimarães":(1.43,1.27),"Gil Vicente":(1.23,0.87),
    "Famalicão":(1.10,0.97),"Moreirense":(1.10,1.27),"Estoril Praia":(1.67,1.57),
    "Santa Clara":(1.23,1.40),"Casa Pia":(1.00,1.33),"Rio Ave":(1.00,1.43),
    "Arouca":(0.77,1.50),"Nacional":(0.87,1.53),"Estrela da Amadora":(0.77,1.67),
    "Tondela":(0.67,1.77),"Alverca":(0.60,1.90),"AVS":(0.57,2.07),
}

def zona(pos, cfg):
    cl,el,ecl = cfg["cl"],cfg["el"],cfg["ecl"]
    po,releg,total = cfg["po"],cfg["releg"],cfg["total"]
    if pos <= cl:                     return "champions"
    if pos <= cl+el:                  return "europa_el"
    if pos <= cl+el+ecl:              return "conference"
    if pos >= total-releg+1:          return "relegation"
    if po > 0 and pos == total-releg: return "playoff_releg"
    return "mid"

HDR = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.sofascore.com/",
}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=HDR)
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"    ERRO: {e}")
        return None

def buscar_liga(liga, cfg):
    tid, sid = cfg["tid"], cfg["sid"]

    # Jornada actual
    j_data = fetch(f"https://api.sofascore.com/api/v1/tournament/{tid}/season/{sid}/rounds")
    jornada = "?"
    if j_data and "currentRound" in j_data:
        jornada = j_data["currentRound"].get("round", "?")
    time.sleep(0.5)

    # Classificação
    data = fetch(f"https://api.sofascore.com/api/v1/tournament/{tid}/season/{sid}/standings/total")
    time.sleep(0.8)
    if not data: return None, None

    sl = data.get("standings", [])
    if not sl: return None, None
    table = None
    for s in sl:
        if "total" in s.get("name","").lower() or s.get("name","") in ("","All"):
            table = s.get("rows", [])
            break
    if table is None: table = sl[0].get("rows", [])
    if not table: return None, None

    cfg_z = ZONAS.get(liga, {"cl":4,"el":1,"ecl":1,"po":0,"releg":3,"total":20})
    eqs = []
    for r in table:
        api  = r.get("team",{}).get("name","") or r.get("team",{}).get("shortName","")
        nome = NOMES.get(api, api)
        pos  = r.get("position", 0)
        fm   = r.get("form","") or ""
        if "," in fm: fm = "".join(fm.split(",")[:5])
        fm   = fm[:5].ljust(5,"?")
        xgA, xgD = XG.get(nome, (1.20, 1.20))
        eqs.append({
            "nome":nome,"pos":pos,"pts":r.get("points",0),
            "gf":r.get("scoresFor",0),"ga":r.get("scoresAgainst",0),
            "gp":r.get("matches",0),"w":r.get("wins",0),
            "d":r.get("draws",0),"l":r.get("losses",0),
            "form5":fm,"zone":zona(pos,cfg_z),
            "xgAtt":xgA,"xgDef":xgD,
        })
    eqs.sort(key=lambda x: x["pos"])
    return eqs, jornada

def gerar_js(todas):
    hoje = datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")
    out = [f"const STANDINGS_REAL = {{ // Sofascore {hoje}"]
    for liga, (eqs, j) in todas.items():
        out.append(f"  // {liga} — J{j} 2025/26")
        out.append(f"  '{liga}': {{")
        for e in eqs:
            out.append(
                f"    '{e['nome']}': {{"
                f" pos:{e['pos']:2}, pts:{e['pts']:3},"
                f" gf:{e['gf']:3}, ga:{e['ga']:3},"
                f" gp:{e['gp']:2}, w:{e['w']:2}, d:{e['d']:2}, l:{e['l']:2},"
                f" xgAtt:{e['xgAtt']:.2f}, xgDef:{e['xgDef']:.2f},"
                f" zone:'{e['zone']}', form5:'{e['form5']}' }},"
            )
        out.append("  },")
    out.append("};")
    return "\n".join(out)

def injectar(html_path, js_block):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    start = content.find("const STANDINGS_REAL = {")
    if start == -1:
        print("ERRO: STANDINGS_REAL não encontrado"); return False
    chunk = content[start:]
    depth = 0
    for i, ch in enumerate(chunk):
        if ch == "{":   depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = start + i + 1; break
    if content[end:end+1] == ";": end += 1
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content[:start] + js_block + ";" + content[end:])
    return True

def main():
    print(f"\n{'='*50}")
    print(f"  ELITE LAB PRO — Actualizar Classificações")
    print(f"  {datetime.utcnow().strftime('%d/%m/%Y %H:%M UTC')}")
    print(f"{'='*50}\n")

    todas = {}
    falhas = []

    for liga, cfg in LIGAS.items():
        print(f"  [{liga}]...", end="", flush=True)
        eqs, jornada = buscar_liga(liga, cfg)
        if eqs:
            todas[liga] = (eqs, jornada)
            print(f" OK — J{jornada}, {len(eqs)} equipas, líder: {eqs[0]['nome']} {eqs[0]['pts']}pts")
        else:
            falhas.append(liga)
            print(" FALHA")

    if not todas:
        print("\n  Sem dados do Sofascore — abortando")
        sys.exit(1)

    print(f"\n  A actualizar {HTML_FILE}...")
    ok = injectar(HTML_FILE, gerar_js(todas))

    if ok:
        print(f"  ✓ {len(todas)} liga(s) actualizadas")
        if falhas:
            print(f"  ✗ Falhas: {', '.join(falhas)}")
    else:
        sys.exit(1)

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    main()
