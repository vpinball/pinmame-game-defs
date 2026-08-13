/**
 * Build-time data pipeline.
 *
 * Reads the `pinmame-game-defs` repository and emits a set of small, static
 * JSON documents under `data/` that the Nuxt app imports directly. Nothing in
 * the app ever touches the defs repo at runtime — the site is fully static.
 *
 * Resolution order for the defs repo:
 *   1. $PINMAME_DEFS_ROOT
 *   2. the parent directory (site lives inside the defs repo, e.g. `site/`)
 *   3. ../pinmame-game-defs
 *   4. ../.worktrees/pinmame-game-defs-machine-definitions   (local dev)
 */
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs'
import { dirname, join, relative, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'
import { marked, Renderer } from 'marked'

const here = dirname(fileURLToPath(import.meta.url))
const projectRoot = resolve(here, '..')
const outRoot = join(projectRoot, 'data')

function findDefsRoot(): string {
	const candidates = [
		process.env.PINMAME_DEFS_ROOT,
		resolve(projectRoot, '..'),
		resolve(projectRoot, '../pinmame-game-defs'),
		resolve(projectRoot, '../.worktrees/pinmame-game-defs-machine-definitions'),
	].filter(Boolean) as string[]

	for (const candidate of candidates) {
		if (existsSync(join(candidate, 'catalog', 'pinmame.json'))) {
			return candidate
		}
	}
	throw new Error(
		'Could not locate the pinmame-game-defs checkout. Set PINMAME_DEFS_ROOT to a directory containing catalog/pinmame.json.\nTried:\n  ' +
		candidates.join('\n  '),
	)
}

const defsRoot = findDefsRoot()
const publicDataRoot = join(projectRoot, 'public', 'data')
const publicEvidenceRoot = join(projectRoot, 'public', 'evidence')

rmSync(outRoot, { recursive: true, force: true })
rmSync(publicDataRoot, { recursive: true, force: true })
rmSync(publicEvidenceRoot, { recursive: true, force: true })
mkdirSync(outRoot, { recursive: true })
mkdirSync(publicDataRoot, { recursive: true })
mkdirSync(publicEvidenceRoot, { recursive: true })

// ---------------------------------------------------------------------------
// helpers
// ---------------------------------------------------------------------------

const readJson = <T = any>(...segments: string[]): T =>
	JSON.parse(readFileSync(join(defsRoot, ...segments), 'utf8'))

const readJsonAbs = <T = any>(path: string): T => JSON.parse(readFileSync(path, 'utf8'))

function walk(dir: string, out: string[] = []): string[] {
	if (!existsSync(dir)) return out
	for (const entry of readdirSync(dir)) {
		const full = join(dir, entry)
		if (statSync(full).isDirectory()) walk(full, out)
		else out.push(full)
	}
	return out
}

function writeTo(root: string, relPath: string, value: unknown) {
	const target = join(root, relPath)
	mkdirSync(dirname(target), { recursive: true })
	writeFileSync(target, JSON.stringify(value))
	return target
}

/** Bundled with the app — imported directly by pages and components. */
const writeOut = (relPath: string, value: unknown) => writeTo(outRoot, relPath, value)

/** Served as a static asset — fetched lazily by the client, never bundled. */
const writePublic = (relPath: string, value: unknown) => writeTo(publicDataRoot, relPath, value)

/** Absolute path -> repo-relative, forward-slashed, for linking into GitHub. */
const repoPath = (absolute: string) => relative(defsRoot, absolute).split(sep).join('/')

/** `stern.metallica-pro.2013` -> `stern-metallica-pro-2013` */
const slugify = (id: string) =>
	id.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')

/** `stub.pinmame.aar_101` -> `aar_101` (stub machines are keyed by root driver) */
const stubDriver = (id: string) => (id.startsWith('stub.pinmame.') ? id.slice('stub.pinmame.'.length) : null)

// ---------------------------------------------------------------------------
// load the corpus
// ---------------------------------------------------------------------------

type Catalog = {
	format: string
	schema_version: number
	source: { pinmame_revision: string, library_version: string, library_sha256: string }
	summary: Record<string, number>
	abstract_parents: { id: string, direct_child_count: number }[]
	drivers: CatalogDriver[]
	machines: CatalogMachine[]
}

type CatalogDriver = {
	id: string
	description: string
	year?: string
	manufacturer?: string
	clone_of?: string
	root_driver: string
	machine_id: string
	definition: string
	coverage_status: 'stub' | 'partial' | 'author_ready'
	flags?: number
}

type CatalogMachine = {
	id: string
	definition: string
	coverage_status: 'stub' | 'partial' | 'author_ready'
	completion_score: number
	driver_count: number
	machine_kind?: string
	missing?: string[]
	processing_order?: number
	processing_year?: number | null
	root_drivers: string[]
}

const catalog = readJson<Catalog>('catalog', 'pinmame.json')

console.log(`[data] defs root      : ${defsRoot}`)
console.log(`[data] pinmame rev    : ${catalog.source.pinmame_revision.slice(0, 12)}`)
console.log(`[data] drivers        : ${catalog.drivers.length}`)
console.log(`[data] catalog records: ${catalog.machines.length}`)

// Every machine definition on disk, keyed by machine.id. The catalog can lag
// behind a freshly committed definition, so disk wins for content.
const definitionFiles = walk(join(defsRoot, 'machines')).filter(f => f.endsWith('.json'))
const definitions = new Map<string, { path: string, doc: any }>()
for (const path of definitionFiles) {
	const doc = readJsonAbs(path)
	if (doc?.format !== 'pinmame-machine-definition') continue
	definitions.set(doc.machine.id, { path, doc })
}
console.log(`[data] definitions    : ${definitions.size}`)

// ---------------------------------------------------------------------------
// knowledge notes
// ---------------------------------------------------------------------------

marked.use({ gfm: true, breaks: false })

const escapeHtml = (value: string) => value.replace(/[&<>"']/g, character => ({
	'&': '&amp;',
	'<': '&lt;',
	'>': '&gt;',
	'"': '&quot;',
	"'": '&#39;',
})[character]!)

const controllerNotesRenderer = new Renderer()
controllerNotesRenderer.html = ({ text }) => escapeHtml(text)
controllerNotesRenderer.heading = function ({ tokens, depth }) {
	const level = Math.max(4, depth)
	return `<h${level}>${this.parser.parseInline(tokens)}</h${level}>\n`
}
const isSafeControllerNotesUrl = (href: string) => {
	try {
		const url = new URL(href, 'https://games.visualpinball.org')
		return url.protocol === 'http:' || url.protocol === 'https:'
	} catch {
		return false
	}
}
controllerNotesRenderer.link = function ({ href, title, tokens }) {
	const text = this.parser.parseInline(tokens)
	if (!isSafeControllerNotesUrl(href)) return text
	return `<a href="${escapeHtml(href)}"${title ? ` title="${escapeHtml(title)}"` : ''}>${text}</a>`
}
controllerNotesRenderer.image = ({ href, title, text }) => {
	if (!isSafeControllerNotesUrl(href)) return escapeHtml(text)
	return `<img src="${escapeHtml(href)}" alt="${escapeHtml(text)}"${title ? ` title="${escapeHtml(title)}"` : ''}>`
}

function renderControllerNotes(notes: string | undefined, format: string | undefined): string | null {
	if (!notes) return null
	if (format === 'markdown') {
		return marked.parse(notes, { async: false, renderer: controllerNotesRenderer }) as string
	}
	return `<p>${escapeHtml(notes).replace(/\r?\n/g, '<br>\n')}</p>\n`
}

type Knowledge = {
	html: string
	headings: { id: string, text: string }[]
	/** Leading `Label: **value**` lines, promoted out of the prose. */
	summary: { label: string, value: string }[]
}

/** `Coverage: **partial - normalized spatial placements pending.**` */
const SUMMARY_LINE = /^([A-Z][^:\n]{0,72}):\s*\*\*(.+?)\*\*\.?\s*$/

function renderKnowledge(relPath: string | undefined): Knowledge | null {
	if (!relPath) return null
	const full = join(defsRoot, relPath)
	if (!existsSync(full)) return null
	// Notes are committed with CRLF; `.` never matches \r, so normalise first or
	// every line-anchored pattern below silently misses.
	const raw = readFileSync(full, 'utf8').replace(/\r\n?/g, '\n')
	// Drop the leading H1 — the page already shows the machine name.
	const withoutTitle = raw.replace(/^#\s+.*\n+/, '')

	// Every note opens with one or more `Label: **value**` lines. Left in the
	// prose they read as a stray bold sentence; lifted out they become the
	// note's summary strip.
	const summary: { label: string, value: string }[] = []
	const lines = withoutTitle.split('\n')
	let cursor = 0
	for (; cursor < lines.length; cursor++) {
		const trimmed = lines[cursor]!.trim()
		if (!trimmed) {
			if (summary.length) break
			continue
		}
		const match = SUMMARY_LINE.exec(trimmed)
		if (!match) break
		summary.push({ label: match[1]!.trim(), value: match[2]!.trim() })
	}
	const body = (summary.length ? lines.slice(cursor).join('\n') : withoutTitle).replace(/^\s+/, '')

	const headings: { id: string, text: string }[] = []
	for (const match of body.matchAll(/^##\s+(.+)$/gm)) {
		const text = match[1]!.trim()
		headings.push({ id: slugify(text), text })
	}
	let html = marked.parse(body, { async: false }) as string
	// Anchor the h2s so the in-page table of contents can link to them.
	let index = 0
	html = html.replace(/<h2>/g, () => `<h2 id="${headings[index++]?.id ?? `section-${index}`}">`)
	return { html, headings, summary }
}

// ---------------------------------------------------------------------------
// source excerpts
// ---------------------------------------------------------------------------

/**
 * The transcribed regions a definition was actually read out of.
 *
 * A recorded hash tells a reader nothing about what a source said; the excerpt does. It is inlined
 * as rendered HTML, and any accompanying page crop is copied into `public/evidence/` so the browser
 * can show it. Excerpts are addressed by repository path, so one shared between machines - the
 * AS-2518-43 sheet is cited by both Centaur and Kiss - is copied once and linked from both.
 */
const EXCERPT_PREFIX = 'evidence/excerpts/'

function readExcerpts(source: any): any[] {
	if (!Array.isArray(source?.excerpts)) return []
	const out: any[] = []
	for (const excerpt of source.excerpts) {
		if (!excerpt?.path) continue
		const absolute = join(defsRoot, excerpt.path)
		if (!existsSync(absolute)) continue
		// Drop the leading `# Title`: the source card already names the document.
		const body = readFileSync(absolute, 'utf8').replace(/^#[^\n]*\n+/, '')

		let imageUrl: string | null = null
		if (excerpt.image && existsSync(join(defsRoot, excerpt.image))) {
			const suffix = String(excerpt.image).startsWith(EXCERPT_PREFIX)
				? String(excerpt.image).slice(EXCERPT_PREFIX.length)
				: String(excerpt.image)
			const target = join(publicEvidenceRoot, suffix)
			mkdirSync(dirname(target), { recursive: true })
			copyFileSync(join(defsRoot, excerpt.image), target)
			imageUrl = `/evidence/${suffix.split(sep).join('/')}`
		}

		out.push({
			id: excerpt.id ?? null,
			locator: excerpt.locator ?? null,
			html: marked.parse(body, { async: false }) as string,
			path: excerpt.path,
			imageUrl,
			imageDerivation: excerpt.image_derivation ?? null,
			method: excerpt.method ?? null,
			transcribedBy: excerpt.transcribed_by ?? null,
			reviewed: typeof excerpt.reviewed === 'boolean' ? excerpt.reviewed : null,
		})
	}
	return out
}

// ---------------------------------------------------------------------------
// controller profiles
// ---------------------------------------------------------------------------

const controllerFiles = walk(join(defsRoot, 'controllers')).filter(f => f.endsWith('.json'))
const controllers = new Map<string, any>()
for (const path of controllerFiles) {
	const doc = readJsonAbs(path)
	if (doc?.format !== 'pinmame-controller-profile') continue
	doc.groups = (doc.groups ?? []).map((group: any) => ({
		...group,
		notesHtml: renderControllerNotes(group.notes, group.notes_format),
	}))
	doc.sourcePath = repoPath(path)
	controllers.set(doc.id, doc)
}
console.log(`[data] controllers    : ${controllers.size}`)

// ---------------------------------------------------------------------------
// index building
// ---------------------------------------------------------------------------

const KIND_BUCKETS: Record<string, string> = {
	switch: 'switches',
	dip_switch: 'dips',
	lamp: 'lamps',
	rgb_lamp: 'lamps',
	gi: 'gi',
	coil: 'coils',
	magnet: 'coils',
	relay: 'coils',
	motor: 'motors',
	servo: 'motors',
	flasher: 'flashers',
}

type Counts = Record<string, number>

function countDevices(doc: any): Counts {
	const counts: Counts = {}
	const bump = (key: string, by = 1) => { counts[key] = (counts[key] ?? 0) + by }
	for (const item of [...(doc.inputs ?? []), ...(doc.outputs ?? [])]) {
		const bucket = KIND_BUCKETS[item.kind]
		if (bucket) bump(bucket)
		bump(`kind:${item.kind}`)
		if (item.availability === 'used') bump('used')
		if (item.availability === 'unused') bump('unused')
	}
	bump('inputs', doc.inputs?.length ?? 0)
	bump('outputs', doc.outputs?.length ?? 0)
	bump('mechanisms', doc.mechanisms?.length ?? 0)
	bump('displays', doc.displays?.length ?? 0)
	bump('relationships', doc.relationships?.length ?? 0)
	bump('sources', doc.sources?.length ?? 0)
	bump('conflicts', doc.conflicts?.length ?? 0)
	return counts
}

/**
 * Distinctive hardware highlights. These double as the browse facets, so the
 * list is complete — the card decides how many of them it has room to show.
 */
function highlights(doc: any): string[] {
	const out = new Set<string>()
	for (const display of doc.displays ?? []) {
		if (display.kind === 'dmd') out.add(`${display.width}×${display.height} DMD`)
		else if (display.kind === 'segment') out.add('Segment display')
		else out.add(display.kind)
	}
	for (const mech of doc.mechanisms ?? []) {
		if (mech.kind && mech.kind !== 'other') out.add(mech.kind.replace(/_/g, ' '))
	}
	return [...out].sort()
}

type MachineIndexEntry = {
	slug: string
	id: string
	name: string
	manufacturer: string
	year: number | null
	status: 'stub' | 'partial' | 'author_ready'
	completionScore: number
	platform: string | null
	ipdbId: number | null
	machineKind: string | null
	rootDrivers: string[]
	driverCount: number
	counts: Counts
	highlights: string[]
	missing: string[]
	dimensions: Record<string, string>
	hasKnowledge: boolean
	hasDetail: boolean
	order: number | null
	definition: string
}

/**
 * The browse page loads every machine at once, so its rows carry only what a
 * card or table row renders. Detail-only fields stay in `data/machines/*.json`.
 */
type MachineRow = [
	slug: string,
	name: string,
	manufacturer: string,
	year: number | null,
	status: 0 | 1 | 2, // stub | partial | author_ready
	platform: string | null,
	driverCount: number,
	switches: number,
	lamps: number,
	coils: number,
	mechanisms: number,
	highlights: string[],
	// Repo-relative path of the definition, so every page — stubs included —
	// can link to the exact file rather than the repository root.
	definition: string,
	// Every driver that resolves here. Stub pages have no detail file, so this
	// is the only place a reader can see which ROM sets are waiting on it.
	roms: string[],
	completionScore: number,
]

const STATUS_CODE = { stub: 0, partial: 1, author_ready: 2 } as const

const romsByMachine = new Map<string, string[]>()

const toRow = (m: MachineIndexEntry): MachineRow => [
	m.slug,
	m.name,
	m.manufacturer,
	m.year,
	STATUS_CODE[m.status],
	m.platform,
	m.driverCount,
	m.counts.switches ?? 0,
	m.counts.lamps ?? 0,
	m.counts.coils ?? 0,
	m.counts.mechanisms ?? 0,
	m.highlights,
	m.definition,
	romsByMachine.get(m.id) ?? [],
	m.completionScore,
]

const machineIndex: MachineIndexEntry[] = []
const catalogById = new Map(catalog.machines.map(m => [m.id, m]))
const driversByMachine = new Map<string, CatalogDriver[]>()
for (const driver of catalog.drivers) {
	const list = driversByMachine.get(driver.machine_id) ?? []
	list.push(driver)
	driversByMachine.set(driver.machine_id, list)
}

let detailCount = 0
const seenIds = new Set<string>()
const detailPayloads = new Map<string, any>()

for (const [machineId, { path, doc }] of definitions) {
	seenIds.add(machineId)
	const catalogEntry = catalogById.get(machineId)
	if (!catalogEntry) throw new Error(`Definition ${machineId} is missing from catalog/pinmame.json; rebuild the catalog before generating the site.`)
	const status = doc.coverage?.status ?? 'stub'
	if (catalogEntry.coverage_status !== status) throw new Error(`Definition ${machineId} has coverage status ${status}, but catalog/pinmame.json has ${catalogEntry.coverage_status}; rebuild the catalog before generating the site.`)
	if (!Number.isInteger(catalogEntry.completion_score) || catalogEntry.completion_score < 0 || catalogEntry.completion_score > 100) throw new Error(`Definition ${machineId} has no valid generated completion score in catalog/pinmame.json.`)
	const slug = slugify(machineId)
	const knowledge = status === 'stub' ? null : renderKnowledge(doc.knowledge?.path)
	const catalogDrivers = driversByMachine.get(machineId) ?? []

	const entry: MachineIndexEntry = {
		slug,
		id: machineId,
		name: (doc.machine.name ?? machineId).replace(/^STUB\s*-\s*/, ''),
		manufacturer: doc.machine.manufacturer ?? 'Unknown',
		year: typeof doc.machine.year === 'number' ? doc.machine.year : null,
		status,
		completionScore: catalogEntry.completion_score,
		platform: doc.controller?.platform ?? null,
		ipdbId: doc.machine.ipdb_id ?? null,
		machineKind: catalogEntry?.machine_kind ?? null,
		rootDrivers: catalogEntry?.root_drivers ?? (doc.drivers ?? []).map((d: any) => d.id),
		driverCount: catalogDrivers.length || (doc.drivers?.length ?? 0),
		counts: countDevices(doc),
		highlights: highlights(doc),
		missing: doc.coverage?.missing ?? [],
		dimensions: doc.coverage?.dimensions ?? {},
		hasKnowledge: !!knowledge,
		hasDetail: status !== 'stub',
		order: catalogEntry?.processing_order ?? null,
		definition: repoPath(path),
	}
	machineIndex.push(entry)

	if (entry.hasDetail) {
		detailCount++
		detailPayloads.set(slug, {
			...doc,
			// Optional collections are omitted rather than emitted empty, so the
			// renderer gets a guaranteed shape instead of guarding every access.
			inputs: doc.inputs ?? [],
			outputs: doc.outputs ?? [],
			displays: doc.displays ?? [],
			mechanisms: doc.mechanisms ?? [],
			relationships: doc.relationships ?? [],
			drivers: doc.drivers ?? [],
			sources: (doc.sources ?? []).map((source: any) => {
				const excerpts = readExcerpts(source)
				return excerpts.length ? { ...source, excerpts } : source
			}),
			conflicts: doc.conflicts ?? [],
			coverage: {
				status,
				completion_score: entry.completionScore,
				missing: doc.coverage?.missing ?? [],
				dimensions: doc.coverage?.dimensions ?? {},
			},
			slug,
			sourcePath: relative(defsRoot, path).replace(/\\/g, '/'),
			knowledgePath: doc.knowledge?.path ?? null,
			knowledgeHtml: knowledge?.html ?? null,
			knowledgeHeadings: knowledge?.headings ?? [],
			knowledgeSummary: knowledge?.summary ?? [],
			catalogDrivers,
		})
	}
}

// Catalog records without a definition file on disk (should not happen, but the
// site must never silently drop a supported driver).
for (const record of catalog.machines) {
	if (seenIds.has(record.id)) continue
	const driver = stubDriver(record.id)
	const catalogDrivers = driversByMachine.get(record.id) ?? []
	machineIndex.push({
		slug: slugify(record.id),
		id: record.id,
		name: catalogDrivers[0]?.description ?? driver ?? record.id,
		manufacturer: catalogDrivers[0]?.manufacturer ?? 'Unknown',
		year: record.processing_year ?? null,
		status: record.coverage_status,
		completionScore: record.completion_score,
		platform: null,
		ipdbId: null,
		machineKind: record.machine_kind ?? null,
		rootDrivers: record.root_drivers ?? [],
		driverCount: record.driver_count ?? catalogDrivers.length,
		counts: {},
		highlights: [],
		missing: record.missing ?? [],
		dimensions: {},
		hasKnowledge: false,
		hasDetail: false,
		order: record.processing_order ?? null,
		definition: record.definition ?? '',
	})
}

machineIndex.sort((a, b) => (b.year ?? 0) - (a.year ?? 0) || a.name.localeCompare(b.name))

// ---------------------------------------------------------------------------
// families
//
// Stern shipped most titles as a Pro and a Premium/LE with genuinely different
// playfields, so the catalog holds them as separate physical machines — which
// is correct, and also means four AC/DC entries sit side by side in search with
// nothing saying they are one title.
//
// The catalog has no family field, so this is *derived*: machines of the same
// manufacturer whose PinMAME drivers share a name prefix. That prefix is how
// PinMAME itself groups a title's ROM sets, which makes it evidence rather than
// a guess — `acd_170` and `acd_150h` are the same game by construction. Across
// all 786 machines it produces 15 groups, every one a real edition family.
//
// It stays derived until the catalog says otherwise: the site labels it as
// such, and a `family` field upstream should replace this outright.
// ---------------------------------------------------------------------------

/** `acd_170h` -> `acd`; drivers without a suffix stand alone. */
const driverPrefix = (driver: string) => (driver.includes('_') ? driver.slice(0, driver.indexOf('_')) : driver)

function commonTitle(names: string[]): string {
	if (names.length === 1) return names[0]!
	let end = 0
	outer: for (; end < names[0]!.length; end++) {
		for (const name of names) {
			if (name[end] !== names[0]![end]) break outer
		}
	}
	const prefix = names[0]!.slice(0, end)
	// An exact match is already a whole title ("Volcano" vs "Volcano (Sound
	// Only)"); otherwise cut back to the last word boundary so a shared prefix
	// like "Firepower (Sys.7/" does not become the name.
	if (names.includes(prefix)) return prefix
	const cut = prefix.lastIndexOf(' ')
	return (cut > 0 ? prefix.slice(0, cut) : prefix).replace(/[\s\-:/(,]+$/, '')
}

/**
 * An authored family document, once the catalog carries them:
 *
 *   families/<slug>.json
 *   { "format": "pinmame-machine-family", "schema_version": 1,
 *     "family": { "id", "title", "manufacturer" },
 *     "members": [ { "machine_id", "edition", "differences": "prose" } ],
 *     "knowledge": { "path": "knowledge/families/<slug>.md" },
 *     "sources": [ … ] }
 *
 * `differences` is the per-edition prose — what this one has that its siblings
 * do not — and the knowledge note is the shared overview. Both are optional;
 * identity and members alone already beat the derivation.
 */
type FamilyDoc = {
	format: string
	family: { id: string, title: string, manufacturer?: string }
	members: { machine_id: string, edition?: string, differences?: string }[]
	knowledge?: { path?: string }
	sources?: any[]
}

const familyDocs = walk(join(defsRoot, 'families'))
	.filter(f => f.endsWith('.json'))
	.map(readJsonAbs)
	.filter((doc: any): doc is FamilyDoc => doc?.format === 'pinmame-machine-family')

console.log(`[data] family docs    : ${familyDocs.length}${familyDocs.length ? '' : ' (none yet — grouping derived from driver prefixes)'}`)

const authoredMemberIds = new Set(familyDocs.flatMap(doc => doc.members.map(m => m.machine_id)))

const familyBuckets = new Map<string, MachineIndexEntry[]>()
for (const machine of machineIndex) {
	// Authored families win outright; the derivation only fills the gaps.
	if (authoredMemberIds.has(machine.id)) continue
	const drivers = (driversByMachine.get(machine.id) ?? []).map(d => d.id)
	if (!drivers.length) continue
	const prefixes = [...new Set(drivers.map(driverPrefix))].sort()
	const key = `${machine.manufacturer}::${prefixes.join('+')}`
	familyBuckets.set(key, [...(familyBuckets.get(key) ?? []), machine])
}

const familySlugs = new Set<string>()

/** Per-machine comparison facts, read straight from each definition. */
function familyMember(machine: MachineIndexEntry, title: string, edition?: string, differences?: string) {
	const doc = definitions.get(machine.id)?.doc
	const mechanismKinds: Record<string, number> = {}
	for (const mech of doc?.mechanisms ?? []) {
		mechanismKinds[mech.kind] = (mechanismKinds[mech.kind] ?? 0) + 1
	}
	return {
		slug: machine.slug,
		name: machine.name,
		// What this edition is called once the shared title is removed.
		edition: edition ?? (machine.name.slice(title.length).replace(/^[\s\-:,]+/, '') || 'Base'),
		differences: differences ?? null,
		year: machine.year,
		status: machine.status,
		platform: machine.platform,
		drivers: machine.driverCount,
		counts: {
			switches: machine.counts.switches ?? 0,
			lamps: machine.counts.lamps ?? 0,
			coils: machine.counts.coils ?? 0,
			flashers: machine.counts.flashers ?? 0,
			gi: machine.counts.gi ?? 0,
			mechanisms: machine.counts.mechanisms ?? 0,
		},
		mechanismKinds,
		displays: (doc?.displays ?? []).map((d: any) =>
			d.kind === 'dmd' && d.width ? `${d.width}x${d.height} DMD` : d.label ?? d.kind),
	}
}

const byMachineId = new Map(machineIndex.map(m => [m.id, m]))

const authoredFamilies = familyDocs.map((doc) => {
	// A member that resolves to nothing would vanish from the page without
	// trace, so say so loudly — it means a typo or a renamed machine.
	for (const member of doc.members) {
		if (!byMachineId.has(member.machine_id)) {
			console.warn(`[data] WARNING family "${doc.family.id}" references unknown machine ${member.machine_id}`)
		}
	}
	const members = doc.members
		.map(m => ({ entry: byMachineId.get(m.machine_id), spec: m }))
		.filter((m): m is { entry: MachineIndexEntry, spec: typeof doc.members[number] } => !!m.entry)
		.sort((a, b) => (a.entry.year ?? 0) - (b.entry.year ?? 0) || a.entry.name.localeCompare(b.entry.name))
	const title = doc.family.title
	const slug = slugify(doc.family.id.includes('.') ? title : doc.family.id)
	familySlugs.add(slug)
	const knowledge = renderKnowledge(doc.knowledge?.path)
	return {
		slug,
		title,
		manufacturer: doc.family.manufacturer ?? members[0]?.entry.manufacturer ?? 'Unknown',
		driverPrefix: null as string | null,
		authored: true,
		overviewHtml: knowledge?.html ?? null,
		years: [
			Math.min(...members.map(m => m.entry.year ?? 0)),
			Math.max(...members.map(m => m.entry.year ?? 0)),
		],
		machines: members.map(m => familyMember(m.entry, title, m.spec.edition, m.spec.differences)),
	}
}).filter(f => f.machines.length > 1)

const derivedFamilies = [...familyBuckets.entries()]
	.filter(([, members]) => members.length > 1)
	.map(([key, members]) => {
		const sorted = members.slice().sort((a, b) => (a.year ?? 0) - (b.year ?? 0) || a.name.localeCompare(b.name))
		const title = commonTitle(sorted.map(m => m.name))
		let slug = slugify(title)
		if (familySlugs.has(slug)) slug = slugify(`${title}-${key.split('::')[1]}`)
		familySlugs.add(slug)
		return {
			slug,
			title,
			manufacturer: sorted[0]!.manufacturer,
			driverPrefix: key.split('::')[1]! as string | null,
			authored: false,
			overviewHtml: null as string | null,
			years: [Math.min(...sorted.map(m => m.year ?? 0)), Math.max(...sorted.map(m => m.year ?? 0))],
			machines: sorted.map(m => familyMember(m, title)),
		}
	})

const families = [...authoredFamilies, ...derivedFamilies].sort((a, b) => a.title.localeCompare(b.title))

/** slug -> the family a machine belongs to, for the machine page. */
const familyOf = new Map<string, { slug: string, title: string }>()
for (const family of families) {
	for (const member of family.machines) familyOf.set(member.slug, { slug: family.slug, title: family.title })
}

writeOut('families.json', families)
writePublic('families.json', families)

// ---------------------------------------------------------------------------
// drivers index
// ---------------------------------------------------------------------------

const slugByMachineId = new Map(machineIndex.map(m => [m.id, m.slug]))
const nameByMachineId = new Map(machineIndex.map(m => [m.id, m.name]))

const driverIndex = catalog.drivers.map(driver => ({
	id: driver.id,
	description: driver.description,
	year: driver.year ?? null,
	manufacturer: driver.manufacturer ?? null,
	cloneOf: driver.clone_of ?? null,
	rootDriver: driver.root_driver,
	machineId: driver.machine_id,
	machineSlug: slugByMachineId.get(driver.machine_id) ?? slugify(driver.machine_id),
	machineName: nameByMachineId.get(driver.machine_id) ?? driver.description,
	status: driver.coverage_status,
}))

// ---------------------------------------------------------------------------
// platforms
// ---------------------------------------------------------------------------

const platformUsage = new Map<string, { machines: number, authorReady: number, examples: { slug: string, name: string }[] }>()
for (const machine of machineIndex) {
	if (!machine.platform) continue
	const usage = platformUsage.get(machine.platform) ?? { machines: 0, authorReady: 0, examples: [] }
	usage.machines++
	if (machine.status === 'author_ready') usage.authorReady++
	if (usage.examples.length < 8) usage.examples.push({ slug: machine.slug, name: machine.name })
	platformUsage.set(machine.platform, usage)
}

const platformIndex = [...new Set([...controllers.keys(), ...platformUsage.keys()])].sort().map(id => {
	const profile = controllers.get(id) ?? null
	const usage = platformUsage.get(id) ?? { machines: 0, authorReady: 0, examples: [] }
	return {
		id,
		slug: slugify(id),
		hardwareFamily: profile?.hardware_family ?? null,
		hasProfile: !!profile,
		sourcePath: profile?.sourcePath ?? null,
		groupCount: profile?.groups?.length ?? 0,
		inversionAppliedByEmulator: profile?.inversion_applied_by_emulator ?? null,
		machines: usage.machines,
		authorReady: usage.authorReady,
		examples: usage.examples,
		profile,
	}
})

// ---------------------------------------------------------------------------
// coverage + curation queue
// ---------------------------------------------------------------------------

const coverage = existsSync(join(defsRoot, 'reports', 'coverage.json'))
	? readJson('reports', 'coverage.json')
	: null

function queueCompletionScore(entry: any): number {
	const catalogEntry = catalogById.get(entry.machine_id)
	if (!catalogEntry) throw new Error(`Queue entry ${entry.machine_id ?? '(missing machine_id)'} is missing from catalog/pinmame.json; rebuild the catalog and reports before generating the site.`)
	if (entry.completion_score == null) return catalogEntry.completion_score
	if (entry.completion_score !== catalogEntry.completion_score) throw new Error(`Queue entry ${entry.machine_id} has completion score ${entry.completion_score}, but catalog/pinmame.json has ${catalogEntry.completion_score}; rebuild the reports before generating the site.`)
	return entry.completion_score
}

/**
 * The queue holds every catalog record. The site only shows what is coming up
 * next, so the bundled copy is trimmed to the pending head of the list.
 */
const curationQueue = (() => {
	if (!existsSync(join(defsRoot, 'reports', 'curation-queue.json'))) return { ordering: '', pending: 0, entries: [] }
	const raw = readJson<{ ordering?: string, entries?: any[] }>('reports', 'curation-queue.json')
	const pending = (raw.entries ?? []).filter(entry => entry.coverage_status !== 'author_ready')
	return {
		ordering: raw.ordering ?? '',
		pending: pending.length,
		entries: pending.slice(0, 60).map(entry => ({
			order: entry.order ?? null,
			year: entry.year ?? null,
			name: String(entry.name ?? '').replace(/^STUB\s*-\s*/, ''),
			manufacturer: entry.manufacturer,
			status: entry.coverage_status,
			completionScore: queueCompletionScore(entry),
			slug: slugify(entry.machine_id ?? ''),
		})),
	}
})()

// ---------------------------------------------------------------------------
// derived facets
// ---------------------------------------------------------------------------

const byManufacturer = new Map<string, { machines: number, authorReady: number, partial: number }>()
for (const machine of machineIndex) {
	const bucket = byManufacturer.get(machine.manufacturer) ?? { machines: 0, authorReady: 0, partial: 0 }
	bucket.machines++
	if (machine.status === 'author_ready') bucket.authorReady++
	if (machine.status === 'partial') bucket.partial++
	byManufacturer.set(machine.manufacturer, bucket)
}

const manufacturers = [...byManufacturer.entries()]
	.map(([name, stats]) => ({ name, ...stats }))
	.sort((a, b) => b.machines - a.machines || a.name.localeCompare(b.name))

const decades = new Map<number, { total: number, authorReady: number, partial: number }>()
for (const machine of machineIndex) {
	if (!machine.year) continue
	const decade = Math.floor(machine.year / 10) * 10
	const bucket = decades.get(decade) ?? { total: 0, authorReady: 0, partial: 0 }
	bucket.total++
	if (machine.status === 'author_ready') bucket.authorReady++
	if (machine.status === 'partial') bucket.partial++
	decades.set(decade, bucket)
}

const missingCounts = new Map<string, number>()
for (const machine of machineIndex) {
	for (const requirement of machine.missing) {
		missingCounts.set(requirement, (missingCounts.get(requirement) ?? 0) + 1)
	}
}

/** Totals of what the corpus actually describes today, across every definition. */
const corpus = { switches: 0, lamps: 0, coils: 0, flashers: 0, gi: 0, mechanisms: 0, relationships: 0, sources: 0, conflicts: 0 }
for (const machine of machineIndex) {
	for (const key of Object.keys(corpus) as (keyof typeof corpus)[]) {
		corpus[key] += machine.counts[key] ?? 0
	}
}

const site = {
	generatedAt: new Date().toISOString(),
	defsRoot: relative(projectRoot, defsRoot).replace(/\\/g, '/'),
	pinmameRevision: catalog.source.pinmame_revision,
	libraryVersion: catalog.source.library_version,
	schemaVersion: catalog.schema_version,
	summary: catalog.summary,
	coverage,
	counts: {
		machines: machineIndex.length,
		drivers: driverIndex.length,
		authorReady: machineIndex.filter(m => m.status === 'author_ready').length,
		partial: machineIndex.filter(m => m.status === 'partial').length,
		stub: machineIndex.filter(m => m.status === 'stub').length,
		platforms: platformIndex.length,
		profiles: controllers.size,
		manufacturers: manufacturers.length,
	},
	decades: [...decades.entries()].sort((a, b) => a[0] - b[0]).map(([decade, stats]) => ({ decade, ...stats })),
	manufacturers,
	corpus,
	missing: [...missingCounts.entries()].sort((a, b) => b[1] - a[1]).map(([requirement, count]) => ({ requirement, count })),
	platforms: platformIndex.map(p => ({ id: p.id, slug: p.slug, hardwareFamily: p.hardwareFamily, hasProfile: p.hasProfile, machines: p.machines, authorReady: p.authorReady })),
	abstractParents: catalog.abstract_parents ?? [],
}

// ---------------------------------------------------------------------------
// search index — one compact row per machine and per driver
// ---------------------------------------------------------------------------

const searchIndex = [
	...families.map(f => ({
		t: 'f' as const,
		s: f.slug,
		n: f.title,
		d: `${f.machines.length} editions · ${f.manufacturer}`,
		k: [f.title, f.manufacturer, f.driverPrefix, ...f.machines.map(m => m.edition)].join(' ').toLowerCase(),
		c: 'author_ready' as const,
	})),
	...machineIndex.map(m => ({
		t: 'm' as const,
		s: m.slug,
		n: m.name,
		d: [m.manufacturer, m.year ?? ''].filter(Boolean).join(' · '),
		k: [m.name, m.manufacturer, String(m.year ?? ''), ...m.rootDrivers].join(' ').toLowerCase(),
		c: m.status,
	})),
	...driverIndex.map(d => ({
		t: 'd' as const,
		s: d.machineSlug,
		n: d.id,
		d: d.description,
		k: `${d.id} ${d.description}`.toLowerCase(),
		c: d.status,
	})),
]

// ---------------------------------------------------------------------------
// emit
// ---------------------------------------------------------------------------

// Detail payloads carry their own "related machines" strip so no page needs the
// full machine index just to render a few sibling links.
const byPlatform = new Map<string, MachineIndexEntry[]>()
for (const machine of machineIndex) {
	if (!machine.platform) continue
	const list = byPlatform.get(machine.platform) ?? []
	list.push(machine)
	byPlatform.set(machine.platform, list)
}

const rank = { author_ready: 0, partial: 1, stub: 2 } as const
for (const machine of machineIndex) {
	const payload = detailPayloads.get(machine.slug)
	if (!payload) continue
	const siblings = (byPlatform.get(machine.platform ?? '') ?? [])
		.filter(m => m.slug !== machine.slug && m.hasDetail)
		.sort((a, b) => {
			const sameManufacturer = Number(b.manufacturer === machine.manufacturer) - Number(a.manufacturer === machine.manufacturer)
			if (sameManufacturer) return sameManufacturer
			return rank[a.status] - rank[b.status] || Math.abs((a.year ?? 0) - (machine.year ?? 0)) - Math.abs((b.year ?? 0) - (machine.year ?? 0))
		})
		.slice(0, 6)
		.map(m => ({ slug: m.slug, name: m.name, manufacturer: m.manufacturer, year: m.year, status: m.status }))
	payload.related = siblings
	const family = familyOf.get(machine.slug)
	const familyDoc = family ? families.find(f => f.slug === family.slug)! : null
	payload.family = familyDoc
		? {
				...family!,
				editions: familyDoc.machines.length,
				differences: familyDoc.machines.find(m => m.slug === machine.slug)?.differences ?? null,
			}
		: null
	writeOut(`machines/${machine.slug}.json`, payload)
}

writeOut('site.json', site)
for (const [machineId, drivers] of driversByMachine) {
	romsByMachine.set(machineId, drivers.map(driver => driver.id))
}

writeOut('machines.json', {
	columns: ['slug', 'name', 'manufacturer', 'year', 'status', 'platform', 'drivers', 'switches', 'lamps', 'coils', 'mechanisms', 'highlights', 'definition', 'roms', 'completionScore'],
	rows: machineIndex.map(toRow),
})
writeOut('platforms.json', platformIndex)
writeOut('curation.json', curationQueue)
// Which machines have a detail document. Tiny, and it saves the client a
// request for the 683 stubs that have none.
writeOut('detail-slugs.json', [...detailPayloads.keys()].sort())

// Large, page-specific indexes stay out of the JS bundle.
writePublic('drivers.json', driverIndex)
writePublic('search.json', searchIndex)

// ---------------------------------------------------------------------------
// machine-readable endpoints
//
// The same resolved documents the pages render, served as plain JSON. An agent
// gets catalog drivers already joined, related machines computed and the
// recreation note rendered — none of which the raw repository provides.
// ---------------------------------------------------------------------------

for (const [slug, payload] of detailPayloads) {
	writePublic(`machines/${slug}.json`, payload)
}

const publicIndex = {
	format: 'pinmame-machine-reference-index',
	version: 1,
	generatedAt: site.generatedAt,
	pinmameRevision: site.pinmameRevision,
	schemaVersion: site.schemaVersion,
	counts: site.counts,
	endpoints: {
		index: 'data/index.json',
		machine: 'data/machines/{slug}.json',
		drivers: 'data/drivers.json',
		search: 'data/search.json',
		platforms: 'data/platforms.json',
	},
	machines: machineIndex.map(m => ({
		slug: m.slug,
		id: m.id,
		name: m.name,
		manufacturer: m.manufacturer,
		year: m.year,
		status: m.status,
		completionScore: m.completionScore,
		platform: m.platform,
		rootDrivers: m.rootDrivers,
		// Only described machines have a detail document.
		detail: m.hasDetail ? `data/machines/${m.slug}.json` : null,
		definition: m.definition,
	})),
}
writePublic('index.json', publicIndex)
writePublic('platforms.json', platformIndex)

// ---------------------------------------------------------------------------
// discovery: sitemap, robots, llms.txt
//
// The browse page paginates on the client, so link-following reaches only the
// first screenful of machines. Without a sitemap the overwhelming majority of
// the site is invisible to a crawler.
// ---------------------------------------------------------------------------

const siteUrl = (process.env.NUXT_PUBLIC_SITE_URL || 'https://games.visualpinball.org').replace(/\/+$/, '')
const lastmod = site.generatedAt.slice(0, 10)

/** Static hosting serves `<route>/index.html`, so canonical URLs end in a slash. */
const pageUrl = (path: string) => `${siteUrl}/${path.replace(/^\/+/, '')}`

const sitemapEntries: { loc: string, priority: string }[] = [
	{ loc: pageUrl(''), priority: '1.0' },
	{ loc: pageUrl('machines/'), priority: '0.9' },
	{ loc: pageUrl('roms/'), priority: '0.8' },
	{ loc: pageUrl('platforms/'), priority: '0.7' },
	{ loc: pageUrl('coverage/'), priority: '0.6' },
	{ loc: pageUrl('guide/'), priority: '0.8' },
	{ loc: pageUrl('schema/'), priority: '0.6' },
	// Stubs are `noindex` — a page whose only unique content is a name would
	// dilute the described machines it shares a domain with.
	...machineIndex.filter(m => m.hasDetail).map(m => ({ loc: pageUrl(`machines/${m.slug}/`), priority: '0.7' })),
	...platformIndex.map(p => ({ loc: pageUrl(`platforms/${p.slug}/`), priority: '0.5' })),
	...families.map(f => ({ loc: pageUrl(`families/${f.slug}/`), priority: '0.6' })),
]

writeFileSync(
	join(projectRoot, 'public', 'sitemap.xml'),
	`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${
		sitemapEntries.map(entry =>
			`\t<url><loc>${entry.loc}</loc><lastmod>${lastmod}</lastmod><priority>${entry.priority}</priority></url>`,
		).join('\n')
	}\n</urlset>\n`,
)

writeFileSync(
	join(projectRoot, 'public', 'robots.txt'),
	[
		'User-agent: *',
		'Allow: /',
		'',
		'# Generated JSON is meant to be read by tools and agents.',
		`Sitemap: ${siteUrl}/sitemap.xml`,
		'',
	].join('\n'),
)

writeFileSync(
	join(projectRoot, 'public', 'llms.txt'),
	`# PinMAME Machine Reference

> A browsable reference for the pinmame-game-defs catalog: every switch, lamp, coil, display and
> mechanism of a PinMAME-supported pinball machine, the address the emulator reports for each, and
> the evidence behind every claim. Generated from the catalog; it adds no facts of its own.

Catalog state: ${site.counts.machines} physical machines, ${site.counts.drivers} PinMAME ROM sets,
${site.counts.authorReady} author-ready and ${site.counts.partial} partial definitions, generated
${lastmod} from PinMAME ${site.pinmameRevision.slice(0, 12)}.

## Machine-readable data

Prefer these over scraping the pages. Every document is static JSON, CORS-open, and resolved —
catalog drivers joined, related machines computed, recreation notes rendered to HTML.

- [Index](${siteUrl}/data/index.json): every machine with its slug, status, platform and detail URL
- [Machine detail](${siteUrl}/data/machines/{slug}.json): full I/O, mechanisms, displays, sources
- [Drivers](${siteUrl}/data/drivers.json): all ${site.counts.drivers} ROM sets mapped to a machine
- [Platforms](${siteUrl}/data/platforms.json): controller profiles and address ranges
- [Search](${siteUrl}/data/search.json): compact index over machines and ROM sets

## Pages

- [Machines](${siteUrl}/machines/): browse and filter the catalog
- [ROM lookup](${siteUrl}/roms/): resolve a driver id such as \`mtl_180h\` to its machine
- [Platforms](${siteUrl}/platforms/): controller address groups and normalisation rules
- [Coverage](${siteUrl}/coverage/): completion report and curation queue
- [Guide](${siteUrl}/guide/): how to read a definition — identity, bindings, polarity, provenance
- [Schema](${siteUrl}/schema/): every field of every type, generated from the JSON Schemas

## Notes for agents

- \`coverage.status\` is fail-closed: \`stub\` means nothing is known, \`partial\` means evidence
  exists but authoring requirements are unmet, \`author_ready\` means a validator confirmed
  completeness. Do not present \`stub\` or \`partial\` data as a usable definition.
- \`completionScore\` is generated from the fixed author-readiness requirements. It is 0 for stubs
  and 100 for author-ready definitions, and it never overrides \`coverage.status\`.
- Provenance is per assertion (\`unknown\`, \`candidate\`, \`observed\`, \`validated\`, \`conflicted\`).
  Observing an output toggle is not the same as knowing what it drives.
- Addresses are the values PinMAME's public API reports, not hardware pins.
- The canonical source is https://github.com/vpinball/pinmame-game-defs — this site is a rendering.
`,
)

console.log(`[data] detail pages   : ${detailCount}`)
console.log(`[data] platforms      : ${platformIndex.length}`)
console.log(`[data] search rows    : ${searchIndex.length}`)
console.log(`[data] sitemap urls   : ${sitemapEntries.length} (stubs excluded as noindex)`)
console.log(`[data] written to     : ${relative(projectRoot, outRoot)} + public/data`)
