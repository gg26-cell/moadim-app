// Rend les HTML de print/dist/ en PDF A4, fonds compris.
// Usage : node print/topdf.mjs   (PLAYWRIGHT=/chemin/vers/playwright si l'install est globale)
const module = await import(process.env.PLAYWRIGHT ?? 'playwright')
const { chromium } = module.default ?? module
import { readdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const dist = path.join(path.dirname(fileURLToPath(import.meta.url)), 'dist')
const pages = readdirSync(dist).filter((f) => f.endsWith('.html') && !f.startsWith('apercu'))

const navigateur = await chromium.launch()
const onglet = await navigateur.newPage()
for (const fichier of pages) {
  await onglet.goto('file://' + path.join(dist, fichier), { waitUntil: 'networkidle' })
  await onglet.evaluate(() => document.fonts.ready)
  const sortie = path.join(dist, fichier.replace(/\.html$/, '.pdf'))
  await onglet.pdf({ path: sortie, format: 'A4', printBackground: true, preferCSSPageSize: true })
  console.log(sortie)
}
await navigateur.close()
