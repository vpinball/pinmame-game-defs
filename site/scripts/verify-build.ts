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
import { MAX_DMD_TITLE_CHARS, OG_HEIGHT, OG_WIDTH, wrapDmdTitle } from './og-card'
import { COMPLETION_REQUIREMENTS } from '../app/utils/completion'
import {
	PINBALL_MEMORY_MAPS_ATTRIBUTION,
	PINBALL_MEMORY_MAPS_CONTENTS_LICENSE,
	PINBALL_MEMORY_MAPS_LICENSE,
	PINBALL_MEMORY_MAPS_LICENSE_FILES,
} from './memory-maps'

const projectRoot = resolve(fileURLToPath(import.meta.url), '../..')
const outRoot = join(projectRoot, '.output', 'public')

if (!existsSync(outRoot)) {
	console.error('[verify] .output/public not found — run `npm run generate` first.')
	process.exit(1)
}

const readIndex = <T>(name: string): T =>
	JSON.parse(readFileSync(join(projectRoot, 'data', name), 'utf8'))

const machines = readIndex<{ columns: string[], rows: [string, ...unknown[]][] }>('machines.json')
const platforms = readIndex<{ id: string, slug: string, hardwareFamily: string | null }[]>('platforms.json')
const families = readIndex<{ slug: string }[]>('families.json')
const site = readIndex<{ summary: { machine_count: number, driver_count: number } }>('site.json')
const memoryMapIndexPath = join(projectRoot, 'public', 'data', 'memory-maps', 'index.json')
const memoryMaps = existsSync(memoryMapIndexPath)
	? JSON.parse(readFileSync(memoryMapIndexPath, 'utf8')) as {
		source?: {
			license?: string
			contentsLicense?: string
			licenseFiles?: { license?: string, sourcePath?: string, dataUrl?: string }[]
			attribution?: string
		}
		maps?: { dataUrl?: string, platformDataUrl?: string }[]
		drivers?: { machineSlug?: string }[]
	}
	: null

const expected = [
	'',
	'machines',
	'roms',
	'platforms',
	'coverage',
	'guide',
	'schema',
	'about',
	...machines.rows.map(row => `machines/${row[0]}`),
	...platforms.map(platform => `platforms/${platform.slug}`),
	...families.map(family => `families/${family.slug}`),
]

const missing = expected.filter(route => !existsSync(join(outRoot, route, 'index.html')))
const invalid: string[] = []
const statusColumn = machines.columns.indexOf('status')
const curatedMachines = statusColumn >= 0 ? machines.rows.filter(row => Number(row[statusColumn]) > 0) : []
if (statusColumn < 0) invalid.push('data/machines.json has no status column for social-card generation.')

// Missing requirements must be visible on the built page, not only shipped in JSON.
const missingColumn = machines.columns.indexOf('missing')
if (missingColumn < 0) invalid.push('data/machines.json has no missing-requirements column.')
for (const row of machines.rows) {
	const pagePath = join(outRoot, 'machines', row[0], 'index.html')
	if (!existsSync(pagePath)) continue
	const html = readFileSync(pagePath, 'utf8')
	const section = /<section\b[^>]*\bid="missing-data"[^>]*>([\s\S]*?)<\/section>/.exec(html)?.[1]
	if (!section?.includes('Missing data')) {
		invalid.push(`Machine ${row[0]} has no rendered Missing data section.`)
		continue
	}
	if (Number(row[statusColumn]) === 2) {
		if (!section.includes('No missing data.')) invalid.push(`Complete machine ${row[0]} has no Missing data empty state.`)
	} else {
		for (const key of (row[missingColumn] ?? []) as string[]) {
			const requirement = COMPLETION_REQUIREMENTS[key]
			if (!requirement || !section.includes(requirement.label) || !section.includes(requirement.description)) {
				invalid.push(`Machine ${row[0]} does not explain missing requirement ${key}.`)
			}
		}
		const detailPath = join(outRoot, 'data', 'machines', `${row[0]}.json`)
		if (existsSync(detailPath)) {
			const detail = JSON.parse(readFileSync(detailPath, 'utf8'))
			if (detail.completionNotes?.html && !section.includes(detail.completionNotes.html)) {
				invalid.push(`Machine ${row[0]} omits its recorded completion blockers.`)
			}
		}
	}
}

// The client-only indexes must survive too, or search and the ROM table break.
for (const asset of [
	'data/drivers.json',
	'data/search.json',
	'data/index.json',
	'data/platforms.json',
	'favicon.svg',
	'og.png',
	...curatedMachines.map(row => `og/machines/${row[0]}.png`),
	...platforms.map(platform => `og/platforms/${platform.slug}.png`),
	'sitemap.xml',
	'robots.txt',
	'llms.txt',
	'.nojekyll',
	...(memoryMaps
		? [
			'data/memory-maps/index.json',
			'data/memory-maps/source.json',
			'data/memory-maps/LICENSE-ODbL.md',
			'data/memory-maps/LICENSE-DbCL',
			...(memoryMaps.maps ?? []).map(memoryMap => memoryMap.dataUrl).filter((path): path is string => typeof path === 'string'),
			...(memoryMaps.maps ?? []).map(memoryMap => memoryMap.platformDataUrl).filter((path): path is string => typeof path === 'string'),
		]
		: []),
]) {
	if (!existsSync(join(outRoot, asset))) missing.push(asset)
}

const pngSignature = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
const verifyPng = (path: string, label: string) => {
	if (!existsSync(path)) return
	const card = readFileSync(path)
	if (card.length < 24 || !card.subarray(0, 8).equals(pngSignature)) invalid.push(`${label} social card is not a valid PNG.`)
	else if (card.readUInt32BE(16) !== OG_WIDTH || card.readUInt32BE(20) !== OG_HEIGHT) invalid.push(`${label} social card is not ${OG_WIDTH}x${OG_HEIGHT}.`)
}

const nameColumn = machines.columns.indexOf('name')
if (nameColumn < 0) {
	invalid.push('data/machines.json has no name column for social-card generation.')
} else {
	for (const row of machines.rows) {
		const slug = row[0]
		const curated = statusColumn >= 0 && Number(row[statusColumn]) > 0
		const name = String(row[nameColumn] ?? '')
		const cardPath = join(outRoot, 'og', 'machines', `${slug}.png`)
		const pagePath = join(outRoot, 'machines', slug, 'index.html')
		if (curated) {
			const layout = wrapDmdTitle(name)
			if (layout.lines.length < 1 || layout.lines.length > 2) invalid.push(`Machine ${slug} social title uses ${layout.lines.length} DMD lines; expected one or two.`)
			if (layout.lines.some(line => line.length > MAX_DMD_TITLE_CHARS)) invalid.push(`Machine ${slug} social title exceeds the ${MAX_DMD_TITLE_CHARS}-character DMD line width.`)
			if (layout.truncated && !layout.lines.at(-1)?.endsWith('...')) invalid.push(`Machine ${slug} social title is truncated without a visible ellipsis.`)
			verifyPng(cardPath, `Machine ${slug}`)
			if (existsSync(pagePath) && !readFileSync(pagePath, 'utf8').includes(`/og/machines/${slug}.png`)) invalid.push(`Machine ${slug} page does not reference its social card.`)
		} else {
			if (existsSync(cardPath)) invalid.push(`Stub machine ${slug} has a generated custom social card.`)
			if (existsSync(pagePath) && !readFileSync(pagePath, 'utf8').includes('/og.png')) invalid.push(`Stub machine ${slug} page does not reference the generic social card.`)
		}
	}
}

for (const platform of platforms) {
	const title = platform.hardwareFamily ?? platform.id
	const layout = wrapDmdTitle(title)
	if (layout.lines.length < 1 || layout.lines.length > 2) invalid.push(`Platform ${platform.id} social title uses ${layout.lines.length} DMD lines; expected one or two.`)
	if (layout.lines.some(line => line.length > MAX_DMD_TITLE_CHARS)) invalid.push(`Platform ${platform.id} social title exceeds the ${MAX_DMD_TITLE_CHARS}-character DMD line width.`)
	if (layout.truncated && !layout.lines.at(-1)?.endsWith('...')) invalid.push(`Platform ${platform.id} social title is truncated without a visible ellipsis.`)
	verifyPng(join(outRoot, 'og', 'platforms', `${platform.slug}.png`), `Platform ${platform.id}`)
	const pagePath = join(outRoot, 'platforms', platform.slug, 'index.html')
	if (existsSync(pagePath) && !readFileSync(pagePath, 'utf8').includes(`/og/platforms/${platform.slug}.png`)) invalid.push(`Platform ${platform.id} page does not reference its social card.`)
}

const overflowProbe = wrapDmdTitle('THIS DELIBERATELY LONG MACHINE TITLE CANNOT FIT ON TWO DMD LINES')
if (overflowProbe.lines.length !== 2 || !overflowProbe.truncated || !overflowProbe.lines[1]?.endsWith('...')) invalid.push('Social-card title wrapping does not enforce two lines with an ellipsis on overflow.')

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

// The memory maps are mirrored under upstream's ODbL/DbCL terms, which ask for
// the licence and attribution wherever the content is shown.
const licenseProblems: string[] = []
if (memoryMaps) {
	const source = memoryMaps.source ?? {}
	if (source.license !== PINBALL_MEMORY_MAPS_LICENSE) licenseProblems.push(`Memory maps declare licence ${source.license}, expected ${PINBALL_MEMORY_MAPS_LICENSE}.`)
	if (source.contentsLicense !== PINBALL_MEMORY_MAPS_CONTENTS_LICENSE) licenseProblems.push(`Memory maps declare contents licence ${source.contentsLicense}, expected ${PINBALL_MEMORY_MAPS_CONTENTS_LICENSE}.`)
	if (source.attribution !== PINBALL_MEMORY_MAPS_ATTRIBUTION) licenseProblems.push('Memory maps omit the upstream attribution sentence.')
	const files = new Map((source.licenseFiles ?? []).map(file => [file.license, file]))
	for (const { license, sourcePath } of PINBALL_MEMORY_MAPS_LICENSE_FILES) {
		const file = files.get(license)
		if (file?.sourcePath !== sourcePath || file.dataUrl !== `data/memory-maps/${sourcePath}`) licenseProblems.push(`Memory maps do not list ${sourcePath} as the ${license} text.`)
	}
	// Which pages must show the panel comes from the data, not the HTML, so a
	// panel that stops rendering is caught rather than skipped. Stubs have no
	// detail document and render no panel.
	let panels = 0
	for (const row of machines.rows) {
		const detailPath = join(outRoot, 'data', 'machines', `${row[0]}.json`)
		if (!existsSync(detailPath)) continue
		const detail = JSON.parse(readFileSync(detailPath, 'utf8'))
		if (!detail.externalData?.pinballMemoryMaps?.maps?.length) continue
		const pagePath = join(outRoot, 'machines', row[0], 'index.html')
		if (!existsSync(pagePath)) continue
		const html = readFileSync(pagePath, 'utf8')
		const section = /<section\b[^>]*\bid="memory-maps"[^>]*>([\s\S]*?)<\/section>/.exec(html)?.[1]
		if (!section) {
			licenseProblems.push(`Machine ${row[0]} has memory-map data but renders no memory-map panel.`)
			continue
		}
		panels++
		const contentsLabel = `${PINBALL_MEMORY_MAPS_CONTENTS_LICENSE} contents`
		if (!section.includes(PINBALL_MEMORY_MAPS_LICENSE) || !section.includes(contentsLabel) || !section.includes(PINBALL_MEMORY_MAPS_ATTRIBUTION)) {
			licenseProblems.push(`Machine ${row[0]} shows memory maps without their ODbL/DbCL licences and attribution.`)
		}
	}
	if (!panels && memoryMaps.drivers?.length) licenseProblems.push('No machine page renders a memory-map panel, although the build mirrored matched maps.')
	const llmsPath = join(outRoot, 'llms.txt')
	const llms = existsSync(llmsPath) ? readFileSync(llmsPath, 'utf8') : ''
	if (!llms.includes(PINBALL_MEMORY_MAPS_LICENSE) || !llms.includes(PINBALL_MEMORY_MAPS_CONTENTS_LICENSE)) {
		licenseProblems.push(`llms.txt does not name the memory maps' ${PINBALL_MEMORY_MAPS_LICENSE}/${PINBALL_MEMORY_MAPS_CONTENTS_LICENSE} licences.`)
	}
}

if (missing.length || invalid.length || licenseProblems.length) {
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
	if (licenseProblems.length) {
		console.error(`[verify] Pinball Memory Maps licensing has ${licenseProblems.length} problem${licenseProblems.length === 1 ? '' : 's'}:`)
		for (const problem of licenseProblems.slice(0, 40)) console.error(`  · ${problem}`)
		if (licenseProblems.length > 40) console.error(`  … and ${licenseProblems.length - 40} more`)
		console.error('[verify] Check site/scripts/memory-maps.ts against the pinned upstream licence and MemoryMapPanel.vue.')
	}
	process.exit(1)
}

console.log(`[verify] ${expected.length} routes present, static assets and catalog v2 intact.`)
