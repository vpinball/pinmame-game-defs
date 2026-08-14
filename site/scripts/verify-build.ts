/**
 * Post-generate guard.
 *
 * Nitro is configured with `failOnError: false` so one malformed definition
 * cannot block a whole deploy — but a silently missing page is worse than a
 * loud failure, so every expected route is checked here and reported by name.
 */
import { existsSync, readFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const projectRoot = resolve(fileURLToPath(import.meta.url), '../..')
const outRoot = join(projectRoot, '.output', 'public')

if (!existsSync(outRoot)) {
	console.error('[verify] .output/public not found — run `npm run generate` first.')
	process.exit(1)
}

const readIndex = <T>(name: string): T =>
	JSON.parse(readFileSync(join(projectRoot, 'data', name), 'utf8'))

const machines = readIndex<{ rows: [string, ...unknown[]][] }>('machines.json')
const platforms = readIndex<{ slug: string }[]>('platforms.json')
const families = readIndex<{ slug: string }[]>('families.json')
const site = readIndex<{ summary: { machine_count: number, driver_count: number } }>('site.json')

const expected = [
	'',
	'machines',
	'roms',
	'platforms',
	'coverage',
	'guide',
	'schema',
	...machines.rows.map(row => `machines/${row[0]}`),
	...platforms.map(platform => `platforms/${platform.slug}`),
	...families.map(family => `families/${family.slug}`),
]

const missing = expected.filter(route => !existsSync(join(outRoot, route, 'index.html')))
const invalid: string[] = []

// The client-only indexes must survive too, or search and the ROM table break.
for (const asset of [
	'data/drivers.json',
	'data/search.json',
	'data/index.json',
	'data/platforms.json',
	'favicon.svg',
	'og.png',
	'sitemap.xml',
	'robots.txt',
	'llms.txt',
	'.nojekyll',
]) {
	if (!existsSync(join(outRoot, asset))) missing.push(asset)
}

type PublicMachine = { id: string, machineKind: string | null, roms: string[] }
type PublicIndex = { format: string, version: number, counts?: { machines?: number, drivers?: number }, machines?: PublicMachine[] }
type PublicDriver = { id: string, machineId: string }

const publicIndexPath = join(outRoot, 'data', 'index.json')
const publicDriversPath = join(outRoot, 'data', 'drivers.json')
if (existsSync(publicIndexPath) && existsSync(publicDriversPath)) {
	try {
		const index = JSON.parse(readFileSync(publicIndexPath, 'utf8')) as PublicIndex
		const drivers = JSON.parse(readFileSync(publicDriversPath, 'utf8')) as PublicDriver[]
		const publicMachines = index.machines ?? []
		if (index.format !== 'pinmame-machine-reference-index') invalid.push(`data/index.json has unexpected format ${JSON.stringify(index.format)}.`)
		if (index.version !== 2) invalid.push(`data/index.json is catalog version ${index.version}; expected version 2.`)
		if (index.counts?.machines !== publicMachines.length) invalid.push(`data/index.json declares ${index.counts?.machines ?? 'no'} machines but contains ${publicMachines.length}.`)
		if (index.counts?.drivers !== drivers.length) invalid.push(`data/index.json declares ${index.counts?.drivers ?? 'no'} drivers but data/drivers.json contains ${drivers.length}.`)
		if (publicMachines.length !== site.summary.machine_count) invalid.push(`Catalog v2 contains ${publicMachines.length} machines but catalog/pinmame.json declares ${site.summary.machine_count}.`)
		if (drivers.length !== site.summary.driver_count) invalid.push(`data/drivers.json contains ${drivers.length} drivers but catalog/pinmame.json declares ${site.summary.driver_count}.`)

		const machinesById = new Map<string, PublicMachine>()
		for (const machine of publicMachines) {
			if (!machine.id) {
				invalid.push('data/index.json contains a machine without an id.')
				continue
			}
			if (machinesById.has(machine.id)) invalid.push(`data/index.json contains duplicate machine id ${machine.id}.`)
			machinesById.set(machine.id, machine)
			if (!machine.machineKind?.trim()) invalid.push(`Machine ${machine.id} has no machineKind in catalog v2.`)
			if (!Array.isArray(machine.roms) || machine.roms.length === 0) invalid.push(`Machine ${machine.id} has no ROM list in catalog v2.`)
		}

		const expectedRoms = new Map<string, Set<string>>()
		for (const driver of drivers) {
			const ids = expectedRoms.get(driver.machineId) ?? new Set<string>()
			ids.add(driver.id)
			expectedRoms.set(driver.machineId, ids)
		}
		for (const [machineId, expectedIds] of expectedRoms) {
			const machine = machinesById.get(machineId)
			if (!machine) {
				invalid.push(`Driver index references machine ${machineId}, which is absent from catalog v2.`)
				continue
			}
			const actualRoms = Array.isArray(machine.roms) ? machine.roms : []
			const actualIds = new Set(actualRoms)
			const omitted = [...expectedIds].filter(id => !actualIds.has(id))
			const extra = [...actualIds].filter(id => !expectedIds.has(id))
			if (actualIds.size !== actualRoms.length) invalid.push(`Machine ${machineId} has duplicate ROM ids in catalog v2.`)
			if (omitted.length || extra.length) invalid.push(`Machine ${machineId} ROM list differs from data/drivers.json (missing: ${omitted.join(', ') || 'none'}; extra: ${extra.join(', ') || 'none'}).`)
		}
		for (const machine of publicMachines) {
			if (machine.id && machine.roms?.length && !expectedRoms.has(machine.id)) invalid.push(`Machine ${machine.id} has ROM ids in catalog v2 but no record in data/drivers.json.`)
		}
	} catch (error) {
		invalid.push(`Catalog v2 validation failed: ${error instanceof Error ? error.message : String(error)}`)
	}
}

if (missing.length || invalid.length) {
	if (missing.length) {
		console.error(`[verify] ${missing.length} of ${expected.length} routes/assets are missing from the build:`)
		for (const route of missing.slice(0, 40)) console.error(`  · /${route}`)
		if (missing.length > 40) console.error(`  … and ${missing.length - 40} more`)
		console.error('[verify] Run `npx nuxt dev` and open one of them to see the render error.')
	}
	if (invalid.length) {
		console.error(`[verify] Catalog v2 has ${invalid.length} contract error${invalid.length === 1 ? '' : 's'}:`)
		for (const problem of invalid.slice(0, 40)) console.error(`  · ${problem}`)
		if (invalid.length > 40) console.error(`  … and ${invalid.length - 40} more catalog errors`)
		console.error('[verify] Regenerate the data and repair the reported catalog or driver mismatch.')
	}
	process.exit(1)
}

console.log(`[verify] ${expected.length} routes present, static assets and catalog v2 intact.`)
