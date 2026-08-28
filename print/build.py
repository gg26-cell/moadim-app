#!/usr/bin/env python3
"""Fabrique la feuille de miel à partir de `feuille-miel-simanim.src.html`.

Deux versions, chacune en deux sorties :
  complete   4 pages — signes, Kiddouch du 1er soir, Kiddouch du 2e soir, autour de la table
  courte     2 pages — signes et autour de la table, sans le Kiddouch
  …-A4       page A4 nue, pour l'imprimante de bureau
  …-quadri   226 × 313 mm : A4 + 3 mm de fond perdu + traits de coupe, pour l'imprimeur
Plus `apercu-artifact.html` : la version complète sans enveloppe html/body, pour un Artifact.

Usage : python3 print/build.py
"""
import base64
import pathlib
import re
import segno

ICI = pathlib.Path(__file__).parent
DIST = ICI / "dist"
POLICES = ICI / "fonts"
ASSETS = ICI / "assets"

LIEN_QR = "https://apps.apple.com/fr/app/moadim/id6782411711"
LOGO = "logo-moadim.jpg"

FACES = [
    ("Frank Ruhl Libre", "frank-he.woff2", "400 700",
     "U+0307-0308,U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F"),
    ("Fraunces", "fraunces-latin.woff2", "400 700", None),
    ("Public Sans", "publicsans-latin.woff2", "400 700", None),
]

# Géométrie des fichiers quadri, en millimètres.
ROGNE = 8          # du bord du média au trait de coupe
FOND_PERDU = 3     # débord de l'aplat au-delà du trait de coupe
TRAIT = 5          # longueur des traits de coupe
MEDIA_L, MEDIA_H = 210 + 2 * ROGNE, 297 + 2 * ROGNE          # page A4 seule
PLI_L, PLI_H = 420 + 2 * ROGNE, 297 + 2 * ROGNE              # feuille A3 à plier


def font_faces() -> str:
    blocs = []
    for famille, fichier, poids, plage in FACES:
        b64 = base64.b64encode((POLICES / fichier).read_bytes()).decode()
        regle = [
            "@font-face {",
            f'  font-family: "{famille}";',
            "  font-style: normal;",
            f"  font-weight: {poids};",
            "  font-display: block;",
            f'  src: url(data:font/woff2;base64,{b64}) format("woff2");',
        ]
        if plage:
            regle.append(f"  unicode-range: {plage};")
        regle.append("}")
        blocs.append("\n".join(regle))
    return "\n".join(blocs)


def logo_css(nom: str) -> str:
    """Le logo n'est encodé qu'une fois, en fond de la règle .logo."""
    b64 = base64.b64encode((ASSETS / nom).read_bytes()).decode()
    return (".logo { background-image: url(data:image/jpeg;base64,"
            + b64 + "); background-size: cover; background-position: center; }")


def qr_svg() -> str:
    svg = segno.make(LIEN_QR, error="m").svg_inline(dark="#2C2417", light=None, border=0)
    return re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)


def traits_de_coupe(largeur: int = None, hauteur: int = None, pliage: bool = False) -> str:
    """Traits aux quatre coins, arrêtés à la limite du fond perdu.

    En mode pliage, deux traits supplémentaires marquent l'axe du pli.
    """
    largeur = largeur or MEDIA_L
    hauteur = hauteur or MEDIA_H
    assert ROGNE - FOND_PERDU >= 0, "les traits mordraient sur le fond perdu"
    lignes = []
    for x in (ROGNE, largeur - ROGNE):
        lignes += [(x, 0, x, TRAIT), (x, hauteur - TRAIT, x, hauteur)]
    for y in (ROGNE, hauteur - ROGNE):
        lignes += [(0, y, TRAIT, y), (largeur - TRAIT, y, largeur, y)]
    if pliage:
        milieu = largeur / 2
        lignes += [(milieu, 0, milieu, TRAIT), (milieu, hauteur - TRAIT, milieu, hauteur)]
    traits = "".join(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>' for x1, y1, x2, y2 in lignes
    )
    return (f'<svg class="marques" viewBox="0 0 {largeur} {hauteur}" aria-hidden="true">'
            f'<g stroke="#000" stroke-width="0.12">{traits}</g></svg>')


def imposer(corps: str, marques: str) -> str:
    """Range les quatre pages sur deux feuilles A3 : dos-couverture, puis intérieur.

    Pliée en deux, la feuille donne 1 en couverture, 2-3 en double page, 4 au dos.
    """
    ouvre = '<section class="feuille'
    morceaux = corps.split(ouvre)
    entete, pages = morceaux[0], [ouvre + m for m in morceaux[1:]]
    assert len(pages) == 4, f"quatre pages attendues, {len(pages)} trouvées"
    slug = ('<div class="slug-pli"><span>Moadim · la feuille de miel 5787 — {face}</span>'
            '<span>A3 · recto-verso · pli au centre · fond perdu 3 mm</span></div>')
    feuilles = []
    for face, (gauche, droite) in (("extérieur : dos et couverture", (pages[3], pages[0])),
                                   ("intérieur : double page", (pages[1], pages[2]))):
        feuilles.append(f'<div class="pli"><div class="fond-pli"></div>{marques}'
                        f'{gauche}{droite}{slug.format(face=face)}</div>')
    return entete + "".join(feuilles)


def sans_kiddouch(gabarit: str) -> str:
    """Retire les deux pages de Kiddouch : il reste les signes et le verso."""
    debut, reste = gabarit.split("<!--KIDDOUCH-->", 1)
    court = debut + reste.split("<!--/KIDDOUCH-->", 1)[1]
    # les renvois « voir pages 2 et 3 » n'ont plus d'objet
    while "<!--C-->" in court:
        avant, suite = court.split("<!--C-->", 1)
        court = avant + suite.split("<!--/C-->", 1)[1]
    return court


def ecrire(cible: pathlib.Path, contenu: str) -> None:
    cible.write_text(contenu, encoding="utf-8")
    print(f"{cible}  {cible.stat().st_size // 1024} Ko")


def main() -> None:
    gabarit = (ICI / "feuille-miel-simanim.src.html").read_text(encoding="utf-8")
    commun = (gabarit
              .replace("__FONTS__", font_faces())
              .replace("__QR__", qr_svg())
              .replace("__LOGO__", logo_css(LOGO)))
    DIST.mkdir(exist_ok=True)

    complete = commun.replace("<!--C-->", "").replace("<!--/C-->", "")
    sorties = [
        # nom,                     gabarit,   format de page,               marques,                                  classes,                 imposition
        ("complete-A4", complete, "A4", "", "", False),
        ("courte-A4", sans_kiddouch(commun), "A4", "", "", False),
        ("pliage-A3", complete, "420mm 297mm", "", ' class="pliage"', True),
        ("pliage-quadri", complete, f"{PLI_L}mm {PLI_H}mm",
         traits_de_coupe(PLI_L, PLI_H, pliage=True), ' class="bat pliage quadri"', True),
    ]
    for nom, gabarit, page, marques, classe, imposition in sorties:
        corps = gabarit.replace("__PAGE__", page)
        corps = imposer(corps, marques) if imposition else corps.replace("__MARQUES__", marques)
        corps = corps.replace("__MARQUES__", "")
        tete, reste = corps.split("</style>", 1)
        ecrire(DIST / f"feuille-miel-5787-{nom}.html",
               f'<!doctype html>\n<html lang="fr"><head>{tete}</style></head>'
               f"<body{classe}>{reste}</body></html>")

    apercu = complete.replace("__PAGE__", "A4").replace("__MARQUES__", "")
    ecrire(DIST / "apercu-artifact.html", apercu)


if __name__ == "__main__":
    main()
