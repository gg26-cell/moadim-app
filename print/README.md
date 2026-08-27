# La feuille de miel — Roch Hachana 5787

Feuille A4 recto-verso à poser sur la table de Roch Hachana : le seder des signes
(usage tunisien) au recto, les gestes qui l'entourent au verso.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| `feuille-miel-simanim.src.html` | la source, seul fichier à modifier |
| `build.py` | injecte les polices et le QR, écrit `dist/` |
| `topdf.mjs` | rend les HTML de `dist/` en PDF A4 |
| `dist/feuille-miel-simanim-BAT.pdf` | épreuve : repères de bon à tirer en bas de page |
| `dist/feuille-miel-simanim.pdf` | version propre, sans repères, pour le tirage |

## Refabriquer

```sh
python3 -m pip install segno
python3 print/build.py
PLAYWRIGHT=/chemin/vers/playwright node print/topdf.mjs   # PLAYWRIGHT inutile si installé localement
```

`build.py` produit aussi `dist/apercu-artifact.html` : le même document sans enveloppe
`html/head/body`, prêt à être publié en Artifact pour relecture sur téléphone.

## Spécifications d'impression

- **Format** : A4 (210 × 297 mm), 2 pages, recto-verso, reliure bord long.
- **Marges** : 11 mm en tête, 13 mm sur les côtés, 8 mm en pied — aucun fond perdu,
  la feuille s'imprime sur n'importe quelle imprimante de bureau.
- **Couleurs** : palette « Parchemin » de la charte Moadim — fond `#FBF4E4`,
  encre `#2C2417`, bronze `#7A4F0F`, filets `#A6863F`.
- **Impression des fonds** : cocher « imprimer les arrière-plans » ; ils sont déjà
  aplatis dans le PDF.
- **Papier conseillé** : 120 g mat ivoire ou blanc cassé. Le fond crème du document
  suffit à donner le grain du parchemin, inutile de payer un papier teinté.

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

Embarquées en base64 dans le HTML pour que le document soit autonome. Toutes sous
licence libre : Fraunces (OFL), Public Sans (OFL), Frank Ruhl Libre (OFL) pour l'hébreu
vocalisé. Sous-ensembles latin et hébreu uniquement, téléchargés depuis Google Fonts.
