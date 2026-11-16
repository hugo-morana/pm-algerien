"""Remplace les références à l'italien (langue, nationalité) par le darija / l'Algérie dans les niches concernées.
Met à jour rooms/rNNN_darija.txt et écrit fr_fix.json (libellé, phrase FR, segment FR) lu par build_darija.py."""
import json, os

F = ["it", "lt", "pr", "fo", "eit", "elt", "eim", "mc", "sc", "de", "frl"]
FIX = {
 (1, 91): dict(efr="J'apprends le darija.", efm="apprends", eit="راني نتعلّم الدارجة.", elt="Rani net3allem d-darja.",
               sc="Un élève APPREND le darija au tableau : « T'AS L'AIMANT ? » (mot-clé faible)"),
 (7, 7): dict(frl="Je suis algérien.", efr="Je suis algérien.", efm="Je suis algérien", eit="أنا دزيري.", elt="Ana dziri.", eim="أنا دزيري",
              fo="fém. دزيرية dziriya ; var. جزايري dzayri ; français : فرانسي fransi",
              sc="Un ANANAS coiffé d'une chéchia, drapeau vert et blanc à la main, proclame : « JE SUIS ALGÉRIEN ! ».",
              de="ana ≈ ana(nas) ; la chéchia = la nationalité. Pas de verbe « être » au présent ; دزيري = algérois, algérien (fam.)"),
 (8, 67): dict(frl="Mon darija n'est pas très bon.", efr="Mon darija n'est pas très bon.", efm="Mon darija n'est pas très bon",
               it="الدارجة تاعي ماشي مليحة بزّاف", lt="d-darja ta3i machi mli7a bezzaf", pr="ed-DAR-ja TA-'i",
               fo="« mon arabe » : العربية تاعي l-3arbiya ta3i ; « mon français » : الفرانسي تاعي",
               eit="الدارجة تاعي ماشي مليحة بزّاف.", elt="D-darja ta3i machi mli7a bezzaf.", eim="الدارجة تاعي ماشي مليحة بزّاف",
               sc="Un boxeur THAÏ bafouille trois mots avant le combat : « MON DARIJA N'EST PAS TRÈS BON. »",
               de="ta3i ≈ thaï (mot-clé faible) ; le bafouillage = mon darija n'est pas très bon"),
 (8, 69): dict(frl="Je ne sais pas comment le dire en darija.", efr="Je ne sais pas comment le dire en darija.", efm="Je ne sais pas comment le dire en darija",
               it="ما نعرفش كيفاش نقولها بالدارجة", lt="ma na3refch kifach n9oulha b d-darja",
               fo="« en arabe » : بالعربية b l-3arbiya ; « en français » : بالفرانسي",
               eit="ما نعرفش كيفاش نقولها بالدارجة.", elt="Ma na3refch kifach n9oulha b d-darja.", eim="ما نعرفش كيفاش نقولها بالدارجة",
               sc="Il lève une canette de COLA, bouche ouverte, sans trouver le mot : « JE NE SAIS PAS COMMENT LE DIRE EN DARIJA. »",
               de="n9oulha ≈ (n)-cola ; la bouche ouverte = je ne sais pas comment le dire"),
 (9, 23): dict(frl="Je parle darija.", efr="Je parle darija.", efm="Je parle darija", it="نهدر الدارجة", lt="nehder d-darja", pr="NEH-der ed-DAR-ja",
               fo="le darija : الدارجة d-darja ; l'arabe : العربية l-3arbiya", eit="نهدر الدارجة.", elt="Nehder d-darja.", eim="نهدر الدارجة",
               mc="nez dur, dard", sc="Un homme au NEZ DUR plante un DARD dans la carte de l'Algérie et lance fièrement : JE PARLE DARIJA.",
               de="nehder ≈ nez-d(u)r ; darja ≈ dar(d)-ja ; la carte de l'Algérie = le darija"),
 (9, 34): dict(frl="Je ne parle pas (langue).", fo="le chinois : الشينوية ch-chinwiya ; le darija : الدارجة d-darja"),
 (9, 90): dict(frl="Je parle un peu darija.", efr="Je parle un peu darija.", efm="Je parle un peu darija", fo="+ langue : الدارجة d-darja",
               eit="نهدر شويّة الدارجة.", elt="Nehder chwiya d-darja.",
               sc="Un homme au NEZ DUR pince deux doigts presque collés : JE PARLE UN PEU DARIJA.",
               de="nehder ≈ nez-d(u)r ; les doigts presque collés = un peu"),
 (10, 1): dict(frl="Je ne parle pas très bien darija.", efr="Je ne parle pas très bien darija.", efm="Je ne parle pas très bien darija",
               fo="la langue : الدارجة d-darja", eit="ما نهدرش مليح الدارجة.", elt="Ma nehderch mli7 d-darja.",
               sc="Georges MÉLIÈS, dans un film muet, bafouille devant la Casbah : JE NE PARLE PAS TRÈS BIEN DARIJA."),
 (11, 49): dict(frl="Tu parles bien darija !", efr="Tu parles bien darija !", efm="Tu parles bien darija", it="تهدر الدارجة مليح", lt="tehder d-darja mli7",
                pr="teh-DER ed-DAR-ja m'LIH", fo="الدارجة = le darija ; fém. تهدري tehedri", eit="تهدر الدارجة مليح!", elt="Tehder d-darja mli7!",
                eim="تهدر الدارجة مليح", mc="tes daims, dard",
                sc="TES DAIMS applaudissent à coups de sabots pendant qu'un DARD se plante dans le mille : TU PARLES BIEN DARIJA !",
                de="tehder ≈ te(s)-d(aims) ; darja ≈ dar(d) ; le mille atteint = bien parler"),
 (11, 57): dict(frl="Est-ce que tu parles darija ?", efr="Est-ce que tu parles darija ?", efm="Est-ce que tu parles darija", it="واش تهدر الدارجة؟",
                lt="wach tehder d-darja", eit="واش تهدر الدارجة؟", elt="Wach tehder d-darja?", eim="واش تهدر الدارجة",
                sc="Une montre (WATCH) parlante s'illumine à ton poignet : EST-CE QUE TU PARLES DARIJA ?"),
 (11, 86): dict(frl="Où est-ce que tu as appris le darija ?", efr="Où est-ce que tu as appris le darija ?", efm="Où est-ce que tu as appris le darija",
                it="وين تعلّمت الدارجة؟", lt="win t3allemt d-darja", eit="وين تعلّمت الدارجة؟", elt="Win t3allemt d-darja?", eim="وين تعلّمت الدارجة",
                sc="Un AIMANT géant attire des mots darija qui volent vers ta tête : OÙ EST-CE QUE TU AS APPRIS LE DARIJA ?"),
 (13, 7): dict(efr="J'aime la nourriture algérienne.", efm="J'aime la nourriture", fo="الماكلة = la nourriture ; الدزيرية = algérienne",
               eit="نحبّ الماكلة الدزيرية.", elt="N7ebb l-makla d-dziriya.",
               sc="Une McLAREN bourrée de couscous et de chorba fonce vers toi : J'AIME LA NOURRITURE algérienne."),
 (14, 64): dict(efr="J'apprends le darija.", efm="J'apprends", fo="تعلّم = apprendre ; inacc. يتعلّم ; « étudier » : قرا ; le darija : الدارجة",
                eit="راني نتعلّم الدارجة.", elt="Rani net3allem d-darja.", eim="نتعلّم الدارجة"),
 (15, 93): dict(efr="Comment dit-on cela en darija ?", efm="Comment dit-on cela en darija", fo="litt. « comment disent-ils ? » ; le darija : الدارجة",
                eit="كيفاش يقولو هادي بالدارجة؟", elt="Kifach y9oulou hadi b d-darja?", eim="كيفاش يقولو هادي بالدارجة",
                sc="Un chef verse un COULIS rouge et demande à son apprenti : COMMENT DIT-ON CELA EN DARIJA ?"),
 (15, 95): dict(efr="Comment dit-on « chat » en darija ?", efm="Comment dit-on « chat » en darija", it="كيفاش يقولو… بالدارجة؟",
                lt="kifach y9oulou… b d-darja?", pr="KI-fach y'QOU-lou bed-DAR-ja ?",
                eit="كيفاش يقولو «قطّ» بالدارجة؟", elt="Kifach y9oulou «9ett» b d-darja?", eim="كيفاش يقولو «قطّ» بالدارجة",
                sc="Un GOUROU caresse un chat sur ses genoux : COMMENT DIT-ON « CHAT » EN DARIJA ?"),
 (15, 96): dict(efr="Désolé pour mon darija, je suis seulement débutant.", efm="Désolé pour mon darija, je suis seulement débutant",
                eit="سمحولي على الدارجة تاعي، راني غير بديت.", elt="Sam7ouli 3la d-darja ta3i, rani ghir bdit.",
                eim="سمحولي على الدارجة تاعي، راني غير بديت",
                sc="Un BANDIT bafouille ses menaces dans un darija hésitant : DÉSOLÉ, JE SUIS SEULEMENT DÉBUTANT."),
 (25, 50): dict(efr="Tu savais qu'il est algérien ?", efm="Tu savais qu", fo="« tu savais que » (litt. « tu étais à savoir que ») ; algérien : دزيري",
                eit="كنت تعرف بلّي راهو دزيري؟", elt="Kount ta3ref belli rahou dziri?", eim="كنت تعرف بلّي",
                sc="Le COMTE lit le TARIF d'un BELLINI au port d'Alger : TU SAVAIS QU'IL EST ALGÉRIEN ?"),
 (28, 7): dict(efr="Son mari est algérien.", efm="mari", eit="راجلها دزيري.", elt="Rajelha dziri."),
 (28, 98): dict(efr="Je suis un cours de darija.", efm="cours", eit="راني نقرا دروس تاع الدارجة.", elt="Rani ne9ra drous ta3 d-darja."),
 (34, 86): dict(efr="Cette amie est algérienne.", efm="Cette", eit="هاد الصّاحبة دزيرية.", elt="Had s-sa7ba dziriya.",
                sc="Le capitaine HADDOCK montre du doigt CETTE amie algérienne, en criant « Mille sabords ! »."),
 (35, 8): dict(efr="Petit à petit, j'apprends le darija.", efm="Petit à petit", eit="شويّة بشويّة، راني نتعلّم الدارجة.",
               elt="Chwiya b chwiya, rani net3allem d-darja.",
               sc="CHEWBACCA, lunettes sur le nez, APPREND LE DARIJA PETIT À PETIT, une page par jour.",
               de="chwiya ≈ Chew(bacca) ; la page par jour = petit à petit. الدارجة = le darija"),
 (41, 55): dict(efr="Mon Dieu, notre dernier souvenir d'Alger !", efm="dernier", eit="يا ربّي، الذكرى اللّخرانية تاعنا على الدزاير!",
                elt="Ya rebbi, d-dikra l-lekhranya ta3na 3la d-dzayer!",
                sc="Sur une carte, L'UKRAINE s'efface : notre DERNIER souvenir d'Alger s'envole avec elle."),
 (53, 66): dict(efr="Le chef de cuisine est algérien.", efm="chef de cuisine", eit="الطبّاخ دزيري.", elt="T-tabbakh dziri."),
 (55, 18): dict(efr="Il a une bonne connaissance du darija.", efm="connaissance", eit="يعرف الدارجة مليح.", elt="Ya3ref d-darja mli7.",
                sc="MARIE-FANNY récite des proverbes algérois par cœur : quelle CONNAISSANCE du darija !",
                de="ma3rifa ≈ Ma(r)i(e)-fa ; le recueil récité = la connaissance. Phrase naturelle avec le verbe : « il connaît bien le darija »"),
 (62, 23): dict(efr="C'est une expression algérienne.", efm="expression", eit="هادا تعبير دزيري.", elt="Hada ta3bir dziri.",
                sc="« Lève TA BIÈRE ! » : voilà une EXPRESSION que le serveur répète à chaque table du café."),
 (62, 63): dict(efr="Le drapeau algérien.", efm="drapeau", fo="pl. أعلام a3lam ; très courant aussi : الدّرابو d-drabo (du français) ; algérien : دزيري",
                eit="العلم الدزيري.", elt="L-3lem d-dziri.",
                de="3lem ≈ (e)l-'lem → elle aime ; le tissu flottant = le drapeau"),
 (63, 49): dict(efr="Le réalisateur est algérien.", efm="réalisateur", fo="pl. مخرجين mokhrijin ; algérien : دزيري dziri",
                eit="المخرج دزيري.", elt="L-mokhrij dziri."),
 (63, 61): dict(efr="Il a un accent algérien.", efm="accent", fo="du français l'accent ; algérien : دزيري", eit="عندو لاكسون دزيري.",
                elt="3andou l'aksoun dziri.",
                sc="Au bord d'un LAC, un pêcheur pousse un SON chantant : il a un ACCENT algérois à couper au couteau."),
 (66, 7): dict(efr="J'étudie le darija.", efm="étudie", eit="راني نقرا الدارجة.", elt="Rani na9ra d-darja.", eim="نقرا الدارجة",
               sc="À ACCRA, sous un baobab, il ÉTUDIE LE DARIJA dans un énorme dictionnaire."),
 (68, 97): dict(efr="Elle enseigne le darija.", efm="enseigne", eit="تقرّي الدارجة.", elt="T9arri d-darja.",
                sc="Une maîtresse en kimono de KARATÉ ENSEIGNE le darija en cassant des planches."),
 (69, 72): dict(efr="Il faut améliorer ton darija.", efm="améliorer", eit="لازم تحسّن الدارجة تاعك.", elt="Lazem t7assen d-darja ta3ek.",
                eim="تحسّن الدارجة تاعك",
                sc="Un ASCENSEUR monte d'étage en étage à chaque leçon : il faut AMÉLIORER TON DARIJA.",
                de="7assen ≈ (a)ssen(seur) ; la montée = améliorer ; doublon avec niche 34 ; الدارجة = le darija"),
 (77, 15): dict(efr="Tu améliores ton darija chaque jour.", efm="améliores", eit="راك تحسّن الدارجة تاعك كلّ نهار.",
                elt="Rak t7assen d-darja ta3ek koul nhar.",
                sc="Ton voisin HASSEN coche chaque jour une ligne de plus au tableau : tu AMÉLIORES ton darija."),
 (84, 89): dict(efr="Vous comprenez le darija ?", efm="comprenez", fo="فهم fhem (comprendre) ; le darija : الدارجة d-darja",
                eit="تفهمو الدارجة؟", elt="Tefhmou d-darja?", sc="« TES FEMMES COMPRENNENT-elles le darija ? » demande le pêcheur du port."),
 (85, 68): dict(efr="Vous parlez darija ?", efm="parlez", fo="هدر hder (parler) ; le darija : الدارجة d-darja",
                eit="تهدرو الدارجة؟", elt="Tehedrou d-darja?", sc="TES HYDRES PARLENT darija ? Les sept têtes chantent du chaâbi."),
 (92, 20): dict(efr="Le film est doublé en arabe.", efm="doublé", eit="الفيلم مدوبلي بالعربية.", elt="L-film mdoubli b l-3arbiya.",
                sc="À DUBLIN, un acteur irlandais DOUBLE un film en arabe, la main sur son micro."),
 (93, 77): dict(efr="La République algérienne.", efm="République", eit="الجمهورية الجزايرية.", elt="L-joumhouriya l-jazayriya."),
 (98, 35): dict(efr="Le doublage arabe est très bon.", efm="doublage", fo="emprunt très courant (séries doublées) ; « doublé » : مدوبلي",
                eit="الدوبلاج بالعربية مليح بزّاف.", elt="Ed-doublaj b l-3arbiya mli7 bezzaf.",
                de="doublaj ≈ doubl(e)-(pl)age ; le micro devant l'écran = le doublage"),
 (101, 34): dict(efr="Il a enseigné le darija pendant trente ans.", efm="enseigné", eit="قرّا الدارجة ثلاثين عام.", elt="9arra d-darja tlatin 3am.",
                 sc="Il a ENSEIGNÉ le darija trente ans, debout sur un bloc de marbre de CARRARE."),
}

frfix = {}
for (ri, i), u in FIX.items():
    p = f"salles/r{ri:03d}_darija.txt"
    L = open(p, encoding="utf8").read().split("\n")
    for k, line in enumerate(L):
        if line.startswith(f"{i} |"):
            f = [x.strip() for x in line.split("|")]
            vals = dict(zip(F, f[1:] + [""] * (12 - len(f))))
            for key in F:
                if key in u: vals[key] = u[key]
            out = [str(i)] + [vals[x] for x in F[:10]] + ([vals["frl"]] if vals["frl"] else [])
            L[k] = " | ".join(out)
            break
    else:
        raise SystemExit(f"niche {ri}:{i} introuvable")
    open(p, "w", encoding="utf8").write("\n".join(L))
    if "efr" in u:
        frfix[f"{ri}:{i}"] = {"efr": u["efr"], "efm": u["efm"]}
json.dump(frfix, open("fr_fix.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(FIX), "niches corrigées,", len(frfix), "phrases FR adaptées")
