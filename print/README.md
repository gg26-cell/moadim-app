# La feuille de miel — Roch Hachana 5787

Feuille à poser sur la table de Roch Hachana. Quatre pages — les signes, le Kiddouch
du premier soir, le Kiddouch du second soir, les gestes autour de la table — tenant sur
**une seule feuille A3 imprimée recto-verso et pliée en deux**.

Le fichier destiné à l'imprimeur est déjà imposé : chacune de ses deux pages est une
face de la feuille. Extérieur : page 4 à gauche, page 1 à droite. Intérieur : pages 2
et 3. Une fois pliée, la feuille se lit dans l'ordre.

Logo Moadim en couleur, QR vers la fiche App Store.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `feuille-miel-simanim.src.html` | la source, seul fichier à modifier |
| `assets/logo-moadim.jpg` | étoile de pierre sur galaxie — le logo posé en tête des deux pages |
| `assets/logo-moadim-icone-appstore.jpg` | variante : l'icône de l'App Store |
| `assets/logo-moadim-nuit.jpg` | variante : étoile d'or sur fond de nuit |
| `build.py` | injecte polices, logo et QR ; écrit les HTML de `dist/` |
| `topdf.mjs` | rend les HTML en PDF, chacun à son format de page |
| `quadri.py` | passe le PDF quadri en CMJN et pose TrimBox / BleedBox |
| `dist/…-pliage-quadri-BAT.pdf` | **le bon à tirer** — feuille A3 imposée, CMJN, fond perdu, traits de coupe et de pliage |
| `dist/…-pliage-A3.pdf` | la même feuille imposée, sans repères — tirage A3 de bureau |
| `dist/…-complete-A4.pdf` | les 4 pages séparées, une par page A4 — dépannage à la maison |
| `dist/…-courte-A4.pdf` | la version 2 pages sans le Kiddouch |

## Refabriquer

```sh
python3 -m pip install segno pillow pikepdf     # gs (ghostscript) doit être installé
python3 print/build.py
node print/topdf.mjs                            # PLAYWRIGHT=/chemin/playwright si install globale
python3 print/quadri.py
```

`build.py` produit aussi `dist/apercu-artifact.html` : le même document sans enveloppe
`html/head/body`, prêt à publier en Artifact pour relecture à l'écran.

## Le fichier pour l'imprimeur

- **Format média** 436 × 313 mm = A3 (420 × 297) rogné + 3 mm de fond perdu + 5 mm de
  traits de coupe. `TrimBox` et `BleedBox` sont inscrites dans le PDF, déduites du
  format réel de chaque page — le même code sert aux fichiers A4.
- **Deux traits de pliage** marquent l'axe central, en haut et en bas, hors du format
  fini.
- **Quadrichromie** : converti en CMJN par Ghostscript, aucun objet RVB résiduel.
  Le brun du texte sort en 0/3/8/83 environ — dominante noire, pas un noir riche.
- **Fond perdu** : l'aplat crème déborde de 3 mm au-delà du trait de coupe.
- **Polices** incorporées et sous-ensemblées. **Images** : logo 720 × 720 px posé à
  21 mm, soit ~870 dpi.
- **Imposition** : déjà faite dans le fichier de pliage. Impression **recto-verso,
  retournement bord long**, puis un pli au centre. Ne pas laisser l'imprimeur imposer
  une seconde fois.
- **Papier conseillé** : 150 g mat ivoire pour une feuille, 250 g pour une carte de
  table qui tient debout.

## La version de bureau

A4 strict, sans fond perdu ni traits de coupe, marges 11 / 13 / 8 mm : elle sort telle
quelle sur n'importe quelle imprimante. Penser à cocher « imprimer les arrière-plans ».

## Le Kiddouch

Le corps du texte vient du corpus de l'application (`mobile/src/content/seed.ts`,
`prayer-kiddush-yom-tov` et `prayer-kiddush-chabbat`) : hébreu d'après Sefaria,
translittération séfarade et traduction déjà relues. **Deux passages ont dû être
écrits pour Roch Hachana**, que le corpus ne couvre pas encore — il s'arrête à
Pessah, Chavouot, Souccot et Chemini Atseret :

- le corps du jour : « et yom hazikaron hazé, yom (zikhron) teroua » ;
- la conclusion : « mélekh al kol haarets, mekadech (haChabbat vé)Israël veyom
  hazikaron ».

Ce sont les deux endroits à faire valider en priorité. Les variantes sont
**résolues** dans chaque page : le premier soir porte les inserts du Chabbat, le
second soir les omet et ajoute la Havdala.

Le Nom divin est composé **יְיָ** et non en toutes lettres : une feuille distribuée
puis jetée ne doit pas imposer la guéniza. C'est une constante de `build.py` à un
seul endroit si tu veux en changer.

## Contenu

Le recto suit l'ordre courant en Tunisie : datte, pomme au miel, grenade, loubia,
courge, poireau, blettes, tête. Les formules sont données en hébreu, en phonétique
et en français. **L'ordre et les formules varient d'une famille à l'autre** : à faire
valider avant tirage.

Le verso rappelle l'allumage, le pain trempé dans le miel, le moment du seder, la
particularité de 5787 (le 1er Tichri tombe un Chabbat — pas de shofar le premier jour,
sonneries et Tachlikh reportés au dimanche 13 septembre), les cent sonneries, le fruit
nouveau du second soir, ce qu'on écarte de la table, les vœux et une liste à cocher.

## Polices

Embarquées en base64 pour que le document soit autonome. Toutes sous licence libre :
Fraunces (OFL), Public Sans (OFL), Frank Ruhl Libre (OFL) pour l'hébreu vocalisé.
Sous-ensembles latin et hébreu uniquement.
