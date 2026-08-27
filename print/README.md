# La feuille de miel — Roch Hachana 5787

Feuille A4 recto-verso à poser sur la table de Roch Hachana : le seder des signes
(usage tunisien) au recto, les gestes qui l'entourent au verso. Logo Moadim en
couleur, QR vers la fiche App Store.

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
| `dist/…-bureau-A4.pdf` | A4 nu, RVB — pour l'imprimante de bureau |
| `dist/…-quadri-BAT.pdf` | **le bon à tirer** — CMJN, fond perdu, traits de coupe |

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

- **Format média** 226 × 313 mm = 210 × 297 rogné + 3 mm de fond perdu + 5 mm de
  traits de coupe. `TrimBox` et `BleedBox` sont inscrites dans le PDF.
- **Quadrichromie** : converti en CMJN par Ghostscript, aucun objet RVB résiduel.
  Le brun du texte sort en 0/3/8/83 environ — dominante noire, pas un noir riche.
- **Fond perdu** : l'aplat crème déborde de 3 mm au-delà du trait de coupe.
- **Polices** incorporées et sous-ensemblées. **Images** : logo 720 × 720 px posé à
  21 mm, soit ~870 dpi.
- **Impression recto-verso**, reliure bord long.
- **Papier conseillé** : 150 g mat ivoire pour une feuille, 250 g pour une carte de
  table qui tient debout.

## La version de bureau

A4 strict, sans fond perdu ni traits de coupe, marges 11 / 13 / 8 mm : elle sort telle
quelle sur n'importe quelle imprimante. Penser à cocher « imprimer les arrière-plans ».

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
