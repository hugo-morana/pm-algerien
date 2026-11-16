"""Second passage sur index.html : retire les dernières traces d'italien (maison Lisa, décors, libellés, analyse des mots)."""
import re, sys
p = sys.argv[1]
h = open(p, encoding="utf8").read()

def sub(old, new, count=1):
    global h
    k = h.count(old)
    assert k >= 1, ("absent", old[:80])
    if count is not None:
        assert k == count, (old[:80], k)
    h = h.replace(old, new)

# titre de l'appli sur l'écran d'accueil
if 'content="Palazzo"' in h:
    sub('content="Palazzo"', 'content="Darja"')

# enseignes des familles (décor) en darija
FAMS = {"mercato": "السّوق", "bottega": "الحانوت تاع الصّنعة", "pinacoteca": "الرّواق", "salotto": "الصالون",
        "sala dei ponti": "قاعة القناطر", "cortile": "وسط الدار", "teatro": "المسرح", "piazza": "الرّحبة",
        "loggia": "السقيفة", "sala dei riflessi": "قاعة الضّيّ", "sala degli specchi": "قاعة المرايات",
        "studio dell'architetto": "بيرو المهندس"}
for a, b in FAMS.items():
    sub(f'it: "{a}"', f'it: "{b}"')
sub('fr: "loggia des orateurs"', 'fr: "patio des orateurs"')

# maison Lisa : pièces et objets
ROOMS = {"L'ingresso": "المدخل", "Il soggiorno": "الصالون", "La sala da pranzo": "بيت الماكلة", "La cucina": "الكوزينة",
         "La lavanderia": "بيت الصابون", "Il garage": "الڨاراج", "La cantina": "الكاڤ", "La terrazza": "السطح",
         "Il giardino": "الجنان", "La piscina": "البيسين", "La soffitta": "السدّة", "La cameretta": "بيت الذراري",
         "Il bagno": "الحمّام", "La camera da letto": "بيت الرقاد", "Lo studio": "البيرو", "Il gabinetto": "الطواليت"}
for a, b in ROOMS.items():
    sub(f'it: "{a}"', f'it: "{b}"')
s = h.index("const HOMES"); e = h.index("];", s)
blk = h[s:e]
objs = list(re.finditer(r'\["([^"]+) · ([^"]+)", "([^"]+)"', blk))
DZ = [l.split(" (")[0].strip() for l in open(sys.argv[2], encoding="utf8") if l.strip()]
assert len(DZ) == len(objs), (len(DZ), len(objs))
out, last = [], 0
for m, dz in zip(objs, DZ):
    out.append(blk[last:m.start(1)]); out.append(dz); last = m.end(1)
out.append(blk[last:])
h = h[:s] + "".join(out) + h[e:]

# libellés restants
sub("dans le sens italien → français", "dans le sens darija → français")
sub('${lg === "it" ? "italien" : "français"} parlé', '${lg === "it" ? "darija" : "français"} parlé')
sub('parlé italien (score fin)', 'parlé darija (score fin)')

# analyse des mots de la phrase : sur la translittération latine (chiffres de l'arabizi gardés)
sub(r'''.replace(/[^a-zà-öø-ÿ' ]/g, " ").split(/\s+/).map(w => w.replace(/^'+/, "")).filter(Boolean);
const wkey''', r'''.replace(/[^a-zà-öø-ÿ0-9' ]/g, " ").split(/\s+/).map(w => w.replace(/^'+/, "")).filter(Boolean);
const wkey''')
sub(r'''/^(il|lo|la|i|gli|le|l'|un|una|uno|un')$/.test(t[0])''', r'''/^(el|l|l'|ech|ed|er|es|et|ez|en|ej|ch|d|r|s|t|z|n|j|dh)$/.test(t[0])''')
sub('''for (const raw of String(rawIt(x)).replace''', '''for (const raw of String(x.lt || rawIt(x)).replace''')
sub('''const idx = wordIndex(), T = ctoks(x.eit), out''', '''const idx = wordIndex(), T = ctoks(x.elt || x.eit).flatMap(t => t.w.includes("-") ? t.w.split("-").filter(Boolean).map(w => ({ w, cap: t.cap })) : [t]), out''')

open(p, "w", encoding="utf8").write(h)
left = [m.group(0) for m in re.finditer(r".{40}(?:ital|Palazzo|palazzo).{30}", h) if "italic" not in m.group(0)]
print("ok ; occurrences restantes :", len(left))
for l in left: print("  ", l)
