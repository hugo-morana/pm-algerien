# Dar ed-Darja

Palais mental 3D pour apprendre le **darija algérien** (parler d'Alger) : 104 salles, 9 581 niches, rangées par classe grammaticale et par fréquence.

## Le palais

- `index.html` : l'appli (three.js en local dans `vendor/`), installable sur iPhone et utilisable hors-ligne grâce à `sw.js` et `offline.js`.
- `data3d.json` : toutes les salles. Chaque niche contient le mot français, la traduction darija en écriture arabe avec sa translittération latine (arabizi : 3 = ع, 7 = ح, 9 = ق, 2 = ء), la prononciation à la française, l'API, un mot-clé sonore français, une scène mnémotechnique, la phrase d'exemple française et sa traduction darija, et des exemples supplémentaires.
- `validation.html` : la table de relecture, salle par salle, avec un filtre « à vérifier » pour les niches signalées comme douteuses.
- `audio/` : les sons français (voix Hugo Pro). Le darija est lu par la voix arabe de l'appareil.
- `config.js` : clés Supabase pour la connexion par e-mail (vide par défaut : la progression reste sur l'appareil). La progression darija est rangée sous ses propres clés (`pmdz:` en local, `dz_` dans Supabase), séparée de celle de l'italien.

## Sources de la traduction

`sources/darija/` contient tout ce qui sert à reconstruire le palais :

- `salles/rNNN_darija.txt` et `salles/rNNN_px.txt` : la traduction de chaque salle (une niche par ligne) et ses exemples supplémentaires ;
- `GUIDE_DARIJA.md` : les conventions de traduction et d'écriture ;
- `build_darija.py` : construit `data3d.json` à partir de la structure du palais italien (dépôt `pm-italien`) et des fichiers de salles ;
- `patch_app.py`, `patch_app2.py` : adaptent la page du palais italien au darija (écriture arabe, voix, libellés, maison « Lisa ») ;
- `fix_lang.py`, `fr_fix.json`, `cm_darija.txt`, `homes_darija.txt` : phrases adaptées au darija, commentaires des patrons syntaxiques, objets de la maison.

```bash
cd sources/darija
python3 build_darija.py --check 0 1 2            # contrôle de salles
PM_ITALIEN_DATA=/chemin/vers/pm-italien/data3d.json python3 build_darija.py x   # reconstruit ../../data3d.json
```

## À faire

- Relecture par un locuteur natif algérois : les doutes et les mots-clés faibles sont signalés dans les décryptages (filtre « à vérifier » de `validation.html`).
- Pas de fréquences darija (aucun corpus fiable du darija parlé) : les vues « fréquence DZ » sont masquées.
- Sons darija à générer (ElevenLabs).
