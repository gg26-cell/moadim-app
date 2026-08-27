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
SOURCE = ICI / "dist" / "feuille-miel-5787-quadri.pdf"
CIBLE = ICI / "dist" / "feuille-miel-5787-quadri-BAT.pdf"

MM = 72 / 25.4
ROGNE, FOND_PERDU = 8, 3          # mm, cf. build.py
MEDIA_L, MEDIA_H = 226, 313       # mm


def boite(marge: float) -> list[float]:
    return [round(v * MM, 4) for v in
            (marge, marge, MEDIA_L - marge, MEDIA_H - marge)]


def main() -> None:
    intermediaire = CIBLE.with_suffix(".cmjn.tmp.pdf")
    subprocess.run(
        ["gs", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dQUIET",
         "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/prepress",
         "-sColorConversionStrategy=CMYK", "-dProcessColorModel=/DeviceCMYK",
         "-dEmbedAllFonts=true", "-dSubsetFonts=true", "-dAutoRotatePages=/None",
         "-dDownsampleColorImages=false", "-dDownsampleGrayImages=false",
         "-dDownsampleMonoImages=false", "-dCompatibilityLevel=1.4",
         f"-o{intermediaire}", str(SOURCE)],
        check=True,
    )
    with pikepdf.open(intermediaire) as pdf:
        for page in pdf.pages:
            page.TrimBox = boite(ROGNE)
            page.BleedBox = boite(ROGNE - FOND_PERDU)
        pdf.save(CIBLE, linearize=True)
    intermediaire.unlink()
    print(f"{CIBLE}  {CIBLE.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
