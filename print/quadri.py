#!/usr/bin/env python3
"""Passe `dist/quadri.pdf` en quadrichromie et pose les boîtes de rognage.

Ghostscript convertit tout l'espace colorimétrique en CMJN et incorpore les
polices ; pikepdf inscrit ensuite TrimBox (le format fini) et BleedBox (le fond
perdu), que l'imprimeur lit pour caler la coupe.

Usage : python3 print/quadri.py
"""
import pathlib
import subprocess

import pikepdf

ICI = pathlib.Path(__file__).parent
DIST = ICI / "dist"

MM = 72 / 25.4
ROGNE, FOND_PERDU = 8, 3          # mm, cf. build.py


def boite(page: pikepdf.Page, marge: float) -> list[float]:
    """Rectangle inscrit à `marge` millimètres du bord du média de cette page.

    Les boîtes se déduisent du format réel : le même code sert à la page A4
    seule (226 × 313) et à la feuille A3 à plier (436 × 313).
    """
    x0, y0, x1, y1 = (float(v) for v in page.MediaBox)
    d = marge * MM
    return [round(v, 4) for v in (x0 + d, y0 + d, x1 - d, y1 - d)]


def convertir(source: pathlib.Path) -> None:
    cible = source.with_name(source.stem + "-BAT.pdf")
    intermediaire = cible.with_suffix(".tmp.pdf")
    subprocess.run(
        ["gs", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dQUIET",
         "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/prepress",
         "-sColorConversionStrategy=CMYK", "-dProcessColorModel=/DeviceCMYK",
         "-dEmbedAllFonts=true", "-dSubsetFonts=true", "-dAutoRotatePages=/None",
         "-dDownsampleColorImages=false", "-dDownsampleGrayImages=false",
         "-dDownsampleMonoImages=false", "-dCompatibilityLevel=1.4",
         f"-o{intermediaire}", str(source)],
        check=True,
    )
    with pikepdf.open(intermediaire) as pdf:
        for page in pdf.pages:
            page.TrimBox = boite(page, ROGNE)
            page.BleedBox = boite(page, ROGNE - FOND_PERDU)
        pdf.save(cible, linearize=True)
    intermediaire.unlink()
    source.unlink()
    print(f"{cible}  {cible.stat().st_size // 1024} Ko  ({len(pikepdf.open(cible).pages)} pages)")


def main() -> None:
    for source in sorted(DIST.glob("*-quadri.pdf")):
        convertir(source)


if __name__ == "__main__":
    main()
