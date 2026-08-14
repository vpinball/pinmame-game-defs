/** Generates the default and per-machine Open Graph PNGs for the static site. */
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { OG_HEIGHT, OG_WIDTH, renderDefaultOgCard, renderMachineOgCard, renderPlatformOgCard } from './og-card'

interface MachineIndex {
	columns: string[]
	rows: unknown[][]
}

interface PlatformIndexEntry {
	id: string
	slug: string
	hardwareFamily: string | null
}

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const publicRoot = join(projectRoot, 'public')
const ogOut = join(publicRoot, 'og')
const machineOut = join(ogOut, 'machines')
const platformOut = join(ogOut, 'platforms')
const index = JSON.parse(readFileSync(join(projectRoot, 'data', 'machines.json'), 'utf8')) as MachineIndex
const platforms = JSON.parse(readFileSync(join(projectRoot, 'data', 'platforms.json'), 'utf8')) as PlatformIndexEntry[]

const column = (name: string) => {
	const indexOfColumn = index.columns.indexOf(name)
	if (indexOfColumn < 0) throw new Error(`machines.json has no ${name} column`)
	return indexOfColumn
}

const slugColumn = column('slug')
const nameColumn = column('name')
const manufacturerColumn = column('manufacturer')
const yearColumn = column('year')
const statusColumn = column('status')

mkdirSync(publicRoot, { recursive: true })
writeFileSync(join(publicRoot, 'og.png'), renderDefaultOgCard())

// This directory contains generated files only. Recreate it so removed or
// renamed catalog entries cannot leave stale cards in the deployed site.
rmSync(ogOut, { recursive: true, force: true })
mkdirSync(machineOut, { recursive: true })
mkdirSync(platformOut, { recursive: true })

const curatedRows = index.rows.filter(row => Number(row[statusColumn]) > 0)
for (const row of curatedRows) {
	const slug = String(row[slugColumn] ?? '')
	const name = String(row[nameColumn] ?? '')
	const manufacturer = String(row[manufacturerColumn] ?? '')
	const rawYear = row[yearColumn]
	const year = typeof rawYear === 'number' ? rawYear : null
	if (!slug || !name) throw new Error(`machines.json contains a row without a slug or name: ${JSON.stringify(row)}`)
	writeFileSync(join(machineOut, `${slug}.png`), renderMachineOgCard({ name, manufacturer, year }))
}

for (const platform of platforms) {
	if (!platform.slug || !platform.id) throw new Error(`platforms.json contains an entry without a slug or id: ${JSON.stringify(platform)}`)
	writeFileSync(join(platformOut, `${platform.slug}.png`), renderPlatformOgCard({ name: platform.hardwareFamily ?? platform.id, id: platform.id }))
}

console.log(`[og]   wrote ${OG_WIDTH}x${OG_HEIGHT} default card, ${curatedRows.length} curated machine cards and ${platforms.length} platform cards`)
