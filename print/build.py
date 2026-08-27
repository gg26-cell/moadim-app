#!/usr/bin/env python3
"""Fabrique la feuille de miel : injecte les polices et le QR, écrit les deux HTML autonomes.

  python3 print/build.py            # -> print/dist/*.html
  node print/topdf.mjs              # -> print/dist/*.pdf
"""
import base64
import pathlib
import re
import segno

ICI = pathlib.Path(__file__).parent
DIST = ICI / "dist"
POLICES = ICI / "fonts"
LIEN_QR = "https://get.moadim.app"

FACES = [
    ("Frank Ruhl Libre", "frank-he.woff2", "400 700", "U+0307-0308,U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F"),
    ("Fraunces", "fraunces-latin.woff2", "400 700", None),
    ("Public Sans", "publicsans-latin.woff2", "400 700", None),
]


def font_faces() -> str:
    morceaux = []
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
        morceaux.append("\n".join(regle))
    return "\n".join(morceaux)


def qr_svg() -> str:
    qr = segno.make(LIEN_QR, error="m")
    svg = qr.svg_inline(dark="#2C2417", light=None, border=0)
    # segno pose une largeur en px : on laisse la CSS décider.
    return re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)


def ecrire(cible: pathlib.Path, contenu: str) -> None:
    cible.write_text(contenu, encoding="utf-8")
    print(f"{cible}  {cible.stat().st_size // 1024} Ko")


def main() -> None:
    gabarit = (ICI / "feuille-miel-simanim.src.html").read_text(encoding="utf-8")
    corps = gabarit.replace("__FONTS__", font_faces()).replace("__QR__", qr_svg())
    DIST.mkdir(exist_ok=True)
    tete, reste = corps.split("</style>", 1)
    for nom, classe in (("feuille-miel-simanim-BAT", ' class="bat"'), ("feuille-miel-simanim", "")):
        page = (f'<!doctype html>\n<html lang="fr"><head>{tete}</style></head>'
                f"<body{classe}>{reste}</body></html>")
        ecrire(DIST / f"{nom}.html", page)

    # Version destinée à un Artifact : pas d'enveloppe html/head/body, la classe
    # « bat » est posée au chargement.
    ecrire(DIST / "apercu-artifact.html",
           corps + '\n<script>document.body.classList.add("bat")</script>\n')


if __name__ == "__main__":
    main()
