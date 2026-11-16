# Transposer les phrases italiennes en Algérie

Le palais darija « Dar ed-Darja » a gardé les phrases françaises du palais italien. L'utilisateur veut maintenant qu'elles se passent en **Algérie** : plus de Rome, Milan, Italie, pizza italienne, pape, Dante… Tu réécris les niches de ta liste. Lis d'abord `/home/claude/src/GUIDE_DARIJA.md` (format des lignes, darija d'Alger, arabizi).

## Table de correspondance (à suivre partout, pour la cohérence)
| Italie | Algérie | arabe | arabizi |
|---|---|---|---|
| l'Italie | l'Algérie | الدزاير / الجزاير | d-dzayer |
| Rome | Alger | الدزاير (la ville) / العاصمة | d-dzayer, l-3assima |
| Milan | Oran | وهران | wahran |
| Naples | Constantine | قسنطينة | qsentina |
| Turin | Annaba | عنّابة | 3annaba |
| Florence (ville) | Tlemcen | تلمسان | tlemsen |
| Florence (prénom) | Fatima | فاطمة | fatma |
| Bologne | Béjaïa | بجاية | bjaya |
| Venise | Tipaza | تيبازة | tipaza |
| Gênes (port) | Skikda | سكيكدة | skikda |
| Palerme (chaleur) | Biskra | بسكرة | biskra |
| Vérone (opéra) | Djemila (festival) | جميلة | djemila |
| Pise / la tour de Pise | Ghardaïa / les maisons de Ghardaïa (salle 102) ; la tour Eiffel (salle 28) | غرداية | ghardaya |
| italien / romain | algérien | دزيري | dziri |
| la pizza (en passant, dans une phrase) | le couscous, la karantita, la chorba (selon la phrase) | الكسكسي، الكرنطيطة، الشربة | |
| le parmesan | le gruyère / le fromage | الفروماج | |
| le cappuccino | le noss-noss (café crème) | نصّ نصّ | noss-noss |
| le pape / Rome | l'imam, La Mecque… selon la phrase | | |
| L'Empire romain | L'Empire ottoman | الدولة العثمانية | |
| Dante, Ciacco | un nom algérien (Ali, Mohamed…) | | |

Les niches dont **le mot étudié lui-même** est italien (« la pizza », « les spaghettis », « la pizza margherita », « le parmesan », « le cappuccino ») : garde le mot quand il s'emploie couramment en Algérie (pizza, spaghettis : oui) mais rends la phrase algérienne (« Une pizza au thon, s'il vous plaît »). Sinon, remplace la niche par l'équivalent algérien et change le libellé (« le parmesan » → « le gruyère » ; « le cappuccino » → « le café crème (noss-noss) » ; « la pizza margherita ; la marguerite » → « la marguerite (fleur) »).

Salle 102 (villes et pays) : remplace chaque ville italienne par la ville algérienne de la table (libellé, phrase, traduction, mot-clé, scène, décryptage : toute la niche). Les villes et pays non italiens (Paris, l'Espagne…) ne changent pas, sauf si la phrase mentionne l'Italie.

## Ce que tu modifies
1. Dans `rooms/rNNN_darija.txt`, remplace la ligne de chaque niche de ta liste par la ligne mise à jour (même format, 11 champs + 12ᵉ « libellé FR corrigé » si le libellé change). Garde la cible darija si elle est toujours juste (ex. « le jour » reste نهار) ; mets à jour phrase arabe, phrase latine, segment surligné, et la scène / le décryptage s'ils mentionnent l'Italie (ambiance algérienne). Ne touche pas aux autres lignes.
2. Dans `rooms/rNNN_px.txt`, pour les exemples supplémentaires de ta liste qui mentionnent l'Italie, remplace la traduction (même position, même nombre de lignes par niche).
3. Écris `fixes/LOT.json` (LOT = la lettre de ton lot) : un objet dont les clés sont `"salle:niche"` et les valeurs `{"efr": nouvelle phrase FR, "efm": segment FR à surligner (copié exactement de efr)}`, plus `"px": {"n°": "nouvelle phrase FR"}` pour les exemples supplémentaires changés (n° = position dans la liste de la niche, à partir de 0).

## Contrôle
`cd /home/claude/src && python3 build_darija.py --check NNN` pour chaque salle touchée, jusqu'à OK. Vérifie aussi que `python3 -c "import json;json.load(open('fixes/LOT.json'))"` passe et que chaque efm figure dans son efr. Puis `grep -n -i "rome\|ital\|milan\|venise\|florence\|naples\|pise" ` sur tes lignes ne doit plus rien donner (hors étymologie).

Rapport final en français, 6 lignes max : nombre de niches modifiées, contrôles OK, choix discutables.
