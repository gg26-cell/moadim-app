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

# Géométrie du fichier quadri, en millimètres.
MEDIA_L, MEDIA_H = 226, 313
ROGNE = 8          # du bord du média au trait de coupe
FOND_PERDU = 3     # débord de l'aplat au-delà du trait de coupe
TRAIT = 5          # longueur des traits de coupe


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


def traits_de_coupe() -> str:
    """Huit traits aux quatre coins, arrêtés à la limite du fond perdu."""
    g, d = ROGNE, MEDIA_L - ROGNE          # traits verticaux (x)
    h, b = ROGNE, MEDIA_H - ROGNE          # traits horizontaux (y)
    fin = ROGNE - FOND_PERDU               # les traits s'arrêtent avant l'aplat
    lignes = []
    for x in (g, d):
        lignes.append((x, 0, x, TRAIT))
        lignes.append((x, MEDIA_H - TRAIT, x, MEDIA_H))
    for y in (h, b):
        lignes.append((0, y, TRAIT, y))
        lignes.append((MEDIA_L - TRAIT, y, MEDIA_L, y))
    assert fin >= 0
    traits = "".join(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>' for x1, y1, x2, y2 in lignes
    )
    return (f'<svg class="marques" viewBox="0 0 {MEDIA_L} {MEDIA_H}" aria-hidden="true">'
            f'<g stroke="#000" stroke-width="0.12">{traits}</g></svg>')


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

    versions = {"complete": commun.replace("<!--C-->", "").replace("<!--/C-->", ""),
                "courte": sans_kiddouch(commun)}
    formats = [
        ("A4", "A4", "", ""),
        ("quadri", f"{MEDIA_L}mm {MEDIA_H}mm", traits_de_coupe(), ' class="bat quadri"'),
    ]
    for version, texte in versions.items():
        for suffixe, page, marques, classe in formats:
            corps = texte.replace("__PAGE__", page).replace("__MARQUES__", marques)
            tete, reste = corps.split("</style>", 1)
            ecrire(DIST / f"feuille-miel-5787-{version}-{suffixe}.html",
                   f'<!doctype html>\n<html lang="fr"><head>{tete}</style></head>'
                   f"<body{classe}>{reste}</body></html>")

    apercu = versions["complete"].replace("__PAGE__", "A4").replace("__MARQUES__", "")
    ecrire(DIST / "apercu-artifact.html", apercu)


if __name__ == "__main__":
    main()
