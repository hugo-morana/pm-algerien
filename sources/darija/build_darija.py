"""Construit data3d.json du palais darija à partir du palais italien (même structure, mêmes phrases FR)."""
import json, re, sys, copy, os

IT = os.environ.get("PM_ITALIEN_DATA", "../../../pm-italien/data3d.json")   # data3d.json du dépôt pm-italien
OUT = "../../data3d.json"

def ipa(lt):
    s = lt.lower()
    s = re.sub(r"^(el|l|ed|er|es|ech|en|et|ez|ej|d|r|s|ch|n|t|z|j)-", lambda m: m.group(1) + "-", s)
    rep = [("kh", "x"), ("gh", "ɣ"), ("ch", "ʃ"), ("dh", "ð"), ("ou", "u"), ("3", "ʕ"), ("7", "ħ"), ("9", "q"),
           ("2", "ʔ"), ("j", "ʒ"), ("y", "j"), ("e", "ə"), ("-", "")]
    for a, b in rep:
        s = s.replace(a, b)
    s = re.sub(r"(.)\1", r"\1ː", s)
    s = re.sub(r"[!?.,;]", "", s)
    return "/" + s.strip() + "/"

def load_main(p):
    out = {}
    for line in open(p, encoding="utf8"):
        if line.startswith("#") or not line.strip():
            continue
        f = [x.strip() for x in line.split("|")]
        i = int(f[0])
        assert len(f) in (11, 12), (p, i, len(f))
        out[i] = dict(it=f[1], lt=f[2], pr=f[3], fo=f[4], eit=f[5], elt=f[6], eim=f[7], mc=f[8], sc=f[9], de=f[10],
                      frl=f[11] if len(f) == 12 else "")
    return out

def load_px(p):
    out = {}
    for line in open(p, encoding="utf8"):
        if line.startswith("#") or not line.strip():
            continue
        f = [x.strip() for x in line.split("|")]
        out.setdefault(int(f[0]), []).append((f[1], f[2]))
    return out

def lien(sc_next):
    s = sc_next.rstrip(".")
    return "Puis : " + (s[0].lower() if not s[:2].isupper() else s[0]) + s[1:] + "."

import os
it = json.load(open(IT, encoding="utf8"))
ENS = {"noms": ("الأسماء · l-asami", "souk algérien"), "verbes": ("الأفعال · l-af3al", "atelier de la Casbah"),
       "adjectifs": ("الصّفات · s-sifat", "galerie aux zelliges"), "pronoms": ("الضّماير · d-dmayer", "salon algérois"),
       "conjonctions": ("أدوات الرّبط · adawat r-rabt", "salle des ponts de Constantine"),
       "prepositions": ("حروف الجرّ · 7rouf j-jarr", "cour à arcades"), "adverbes": ("الظّروف · dh-dhrouf", "théâtre d'Alger"),
       "expressions": ("التّعابير · t-ta3abir", "café maure"), "incises": ("الكلمات العارضة · l-kelmat l-3arda", "patio"),
       "formes": ("التّصريف · t-tasrif", "atelier de la Casbah"), "patrons": ("القوالب · l-9walab", "bibliothèque")}
SPECIAL = {"courantes": "التّعابير الشايعة · t-ta3abir ech-chay3a", "modales": "تعابير يحبّ ويقدر · ta3abir y7ebb w y9der",
           "villes_pays": "المدن والبلدان · l-moudoun w l-bouldan"}
FR_FIX = {(0, 48): "la voiture (soutenu)"}
FRFIX = json.load(open("fr_fix.json", encoding="utf8")) if os.path.exists("fr_fix.json") else {}
import glob as _glob
for _f in sorted(_glob.glob("fixes/*.json")):   # transpositions Italie → Algérie
    for _k, _v in json.load(open(_f, encoding="utf8")).items():
        FRFIX.setdefault(_k, {}).update(_v)
CM103 = [l.strip() for l in open("cm_darija.txt", encoding="utf8") if l.strip()]
def check(ri, write=False):
    room_it = it["rooms"][ri]
    main = load_main(f"salles/r{ri:03d}_darija.txt")
    px = load_px(f"salles/r{ri:03d}_px.txt") if os.path.exists(f"salles/r{ri:03d}_px.txt") else {}
    want = [i for i, n in enumerate(room_it["niches"]) if n]
    errs = []
    if sorted(main) != want:
        errs.append(f"niches manquantes {sorted(set(want) - set(main))} / en trop {sorted(set(main) - set(want))}")
    room = {k: v for k, v in room_it.items() if k != "niches"}
    e = ENS.get(room_it["fam"], ("", ""))
    rid = room_it["id"]; base = rid.rsplit("_", 1)[0] if rid[-1].isdigit() else rid
    num = rid.rsplit("_", 1)[1] if rid[-1].isdigit() and "_" in rid else ""
    lab = SPECIAL.get(base, e[0])
    room.update(it=lab + (" " + num if num and num != "1" else ""), decor=e[1])
    niches = []
    for i, x in enumerate(room_it["niches"]):
        if not x or i not in main:
            niches.append(None if not x else None); continue
        d = main[i]
        n = copy.deepcopy(x)
        n["fr"] = d["frl"] or FR_FIX.get((ri, i), re.sub(r"\s*\((\w+), pluriel\)", " (pluriel)", n["fr"]))
        for k in ("it", "lt", "eit", "sc", "mc"):
            if not d[k]: errs.append(f"{i}: champ {k} vide")
        n.update(it=d["it"], lt=d["lt"], pr=d["pr"], api=ipa(d["lt"]), mc=d["mc"], sc=d["sc"], de=d["de"], fo=d["fo"],
                 eit=d["eit"], elt=d["elt"], eim=d["eim"])
        if d["eim"] not in d["eit"]: errs.append(f"{i}: segment surligné « {d['eim']} » absent de « {d['eit']} »")
        n.update(zi=None, zie=None, oi=None, co=None, ai=None, ap=None, am=None)
        for k in ("itd", "ito", "itp", "ax"):   # champs propres à l'italien (tournures paramétriques, structures)
            n.pop(k, None)
        if d["frl"] and d["frl"] != x["fr"]:
            n["af"] = None   # le son FR du libellé ne correspond plus
        fx = FRFIX.get(f"{ri}:{i}")
        if fx:
            if "efr" in fx:
                n.update(efr=fx["efr"], efm=fx["efm"], ae=None)
        if ri == 103 and n.get("cm"):
            n["cm"] = CM103[i]
        if x.get("px"):
            tr = px.get(i, [])
            if len(tr) != len(x["px"]): errs.append(f"{i}: {len(tr)} exemples supplémentaires au lieu de {len(x['px'])}")
            n["px"] = [[e[0], t[0], e[2], None, t[1]] for e, t in zip(x["px"], tr)]
        elif i in px:
            errs.append(f"{i}: exemples supplémentaires en trop")
        for j, t in ((fx or {}).get("px") or {}).items():
            j = int(j)
            if n.get("px") and j < len(n["px"]):
                n["px"][j][0] = t; n["px"][j][2] = None
        niches.append(n)
    room["niches"] = niches
    return room, errs

if __name__ == "__main__" and sys.argv[1] == "--check":
    bad = 0
    for ri in map(int, sys.argv[2:]):
        try:
            _, errs = check(ri)
        except Exception as ex:
            errs = [f"erreur de lecture : {ex!r}"]
        print(f"salle {ri} :", "OK" if not errs else "\n  " + "\n  ".join(errs)); bad += bool(errs)
    sys.exit(1 if bad else 0)

rooms = []
for ri in range(len(it["rooms"])):
    if not os.path.exists(f"salles/r{ri:03d}_darija.txt"): continue
    room, errs = check(ri)
    if errs: print("salle", ri, "ignorée :", errs[:3]); continue
    rooms.append(room)
allN = [n for r in rooms for n in r["niches"] if n]
for k, n in enumerate(allN):
    n["li"] = lien(allN[(k + 1) % len(allN)]["sc"])
used = sorted({n[k][0] for n in allN for k in ("af", "ae") if n.get(k)} |
              {e[2][0] for n in allN for e in (n.get("px") or []) if e[2]})
data = {"langue": "darija", "rev": it["rev"], "migr": [], "packs": it["packs"], "ext": [],
        "themes": it["themes"], "scorder": it["scorder"], "rooms": rooms}
json.dump(data, open(OUT, "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
open("packs_used.txt", "w").write("\n".join(it["packs"][p].split("?")[0] for p in used))
print(len(rooms), "salles,", len(allN), "niches")
