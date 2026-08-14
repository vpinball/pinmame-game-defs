import type { CoverageStatus, Device, MachineSummary } from '~/types/defs'

/* ---------------------------------------------------------------------------
   Coverage status
--------------------------------------------------------------------------- */

export const STATUS_META: Record<CoverageStatus, { label: string, short: string, color: string, blurb: string }> = {
	author_ready: {
		label: 'Author ready',
		short: 'Ready',
		color: 'var(--color-ready)',
		blurb: 'Full semantic I/O, mechanisms, variants, wiring and recreation notes passed the completeness validator.',
	},
	partial: {
		label: 'Partial',
		short: 'Partial',
		color: 'var(--color-partial)',
		blurb: 'Real evidence exists, but authoring requirements are still missing or in conflict. Verify before shipping a table.',
	},
	stub: {
		label: 'Stub',
		short: 'Stub',
		color: 'var(--color-stub)',
		blurb: 'Only catalog identity is known. The machine is reachable from PinMAME but nothing about it has been described yet.',
	},
}

const STATUS_BY_CODE: CoverageStatus[] = ['stub', 'partial', 'author_ready']

/* ---------------------------------------------------------------------------
   External memory maps
--------------------------------------------------------------------------- */

/**
 * The "memory map available" badge, shared by the browse cards, the browse table
 * and the ROM lookup so the three cannot drift apart.
 *
 * It deliberately borrows nothing from `STATUS_META`. A coverage colour answers
 * "how complete is this repository's own definition"; a memory map is a third
 * party's file that answers nothing of the sort, and a machine can be a bare
 * stub and still have one. So the badge carries no status hue at all — neutral
 * ink inside the dashed border `MemoryMapPanel` already uses for borrowed
 * material, with the words, not a colour, doing the work.
 *
 * The word "external" is in the visible label rather than only in the tooltip or
 * the dashed border, because neither of those survives a screen reader, a touch
 * device or a monochrome print — and "this is not our data" is the whole point.
 * That also makes the label self-sufficient, so the non-interactive badges need
 * no `aria-label`; only the ROM-table link takes one, to keep eighty otherwise
 * identical link names apart.
 */
export const MEMORY_MAP_BADGE = {
	icon: 'lucide:memory-stick',
	label: 'External memory map',
	title: 'An external ROM memory map from the Pinball Memory Maps project covers this machine. It is not part of the definition and does not count towards coverage.',
	chip: 'inline-flex items-center gap-1 rounded border border-dashed border-line bg-raised px-1.5 py-0.5 text-[10px] whitespace-nowrap text-ink-3',
} as const

/* ---------------------------------------------------------------------------
   Device kinds
--------------------------------------------------------------------------- */

export const KIND_LABEL: Record<string, string> = {
	switch: 'Switch',
	dip_switch: 'DIP switch',
	coil: 'Coil',
	flasher: 'Flasher',
	lamp: 'Lamp',
	rgb_lamp: 'RGB lamp',
	gi: 'General illumination',
	motor: 'Motor',
	servo: 'Servo',
	magnet: 'Magnet',
	relay: 'Relay',
	virtual: 'Virtual',
	constant: 'Constant',
	display: 'Display',
}

export const kindColor = (kind: string) => `var(--color-k-${(kind ?? 'virtual').replace(/_lamp$/, '').replace(/_switch$/, '')}, var(--color-k-virtual))`

export const kindLabel = (kind: string) => KIND_LABEL[kind] ?? titleCase(kind)

/* ---------------------------------------------------------------------------
   Matrix layout

   WPC-family platforms address the switch and lamp matrices as `column * 10 +
   row`, so 11-88 lays out as a real 8x8 grid. SAM and most later platforms use
   a flat sequential range, which we chunk into columns of eight so the shape
   still reads like the physical matrix. Anything that fits neither (dedicated
   inputs, negative diagnostic addresses, flipper columns) is listed separately
   rather than forced into the grid.
--------------------------------------------------------------------------- */

export interface MatrixCell {
	address: number
	device: Device | null
}

export interface MatrixModel {
	mode: 'wpc' | 'linear'
	columns: { label: string, cells: MatrixCell[] }[]
	extras: Device[]
}

export function buildMatrix(devices: Device[]): MatrixModel | null {
	const positioned = devices.filter(d => typeof d.binding?.device === 'number')
	if (positioned.length < 8) return null

	const byAddress = new Map<number, Device>()
	for (const device of positioned) byAddress.set(device.binding.device, device)

	const positives = [...byAddress.keys()].filter(a => a > 0)
	if (!positives.length) return null

	// A WPC-style matrix can never contain an address ending in 9 or 0 above the
	// dedicated range — those are not valid column·row positions. A single such
	// address (SAM's 9, 10, 19, 20 …) proves the platform numbers sequentially.
	const hasSequentialMarker = positives.some(a => a > 10 && (a % 10 === 0 || a % 10 === 9))
	const wpcLike = positives.filter(a => a >= 11 && a <= 188 && a % 10 >= 1 && a % 10 <= 8)
	const isWpc = !hasSequentialMarker && wpcLike.length >= 16 && wpcLike.length / positives.length > 0.7

	const used = new Set<number>()
	const columns: MatrixModel['columns'] = []

	if (isWpc) {
		const columnNumbers = [...new Set(wpcLike.map(a => Math.floor(a / 10)))].sort((a, b) => a - b)
		for (const column of columnNumbers) {
			const cells: MatrixCell[] = []
			for (let row = 1; row <= 8; row++) {
				const addr = column * 10 + row
				const device = byAddress.get(addr) ?? null
				if (device) used.add(addr)
				cells.push({ address: addr, device })
			}
			columns.push({ label: String(column), cells })
		}
		return {
			mode: 'wpc',
			columns,
			extras: positioned.filter(d => !used.has(d.binding.device)),
		}
	}

	const max = Math.max(...positives)
	const columnCount = Math.ceil(max / 8)
	for (let column = 0; column < columnCount; column++) {
		const cells: MatrixCell[] = []
		for (let row = 1; row <= 8; row++) {
			const addr = column * 8 + row
			const device = byAddress.get(addr) ?? null
			if (device) used.add(addr)
			cells.push({ address: addr, device })
		}
		columns.push({ label: `${column * 8 + 1}–${column * 8 + 8}`, cells })
	}
	return {
		mode: 'linear',
		columns,
		extras: positioned.filter(d => !used.has(d.binding.device)),
	}
}

/* ---------------------------------------------------------------------------
   Wire colours

   Manual wiring entries use the standard two-letter pinball colour codes, e.g.
   `GRN-BRN` for a green wire with a brown tracer. Rendering them as the actual
   colours makes a wiring column scannable instead of alphabet soup.
--------------------------------------------------------------------------- */

const WIRE_COLORS: Record<string, string> = {
	BLK: '#1a1c20',
	BRN: '#8a5a2b',
	RED: '#e0392c',
	ORG: '#f28c28',
	YEL: '#f2cf2f',
	GRN: '#2fa84f',
	BLU: '#2f6fd0',
	VIO: '#8a4fd0',
	PUR: '#8a4fd0',
	GRY: '#98a2ad',
	GRA: '#98a2ad',
	WHT: '#eef1f5',
	PNK: '#f08bb0',
	TAN: '#cbb08a',
	LTB: '#7fc4f0',
	LTG: '#7fe0a4',
}

export function wireParts(code: string | undefined | null): { code: string, color: string }[] {
	if (!code) return []
	return code
		.toUpperCase()
		.split(/[-/]/)
		.map(part => part.trim())
		.filter(Boolean)
		.map(part => ({ code: part, color: WIRE_COLORS[part] ?? 'var(--color-ink-4)' }))
}

/* ---------------------------------------------------------------------------
   Roles
--------------------------------------------------------------------------- */

/* ---------------------------------------------------------------------------
   Formatting
--------------------------------------------------------------------------- */

export function titleCase(value: string) {
	return value.replace(/[._-]+/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

export const shortHash = (hash: string | undefined) => (hash ? hash.slice(0, 12) : '')

/**
 * Locale-independent thousands grouping. `toLocaleString()` follows the host
 * locale, so a de-CH build server renders 2’873 while an en-US browser expects
 * 2,873 — a hydration mismatch on every stat tile.
 */
export const num = (value: number) => String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ',')

export function decodeMachineRows(index: { rows: any[][] }): MachineSummary[] {
	return index.rows.map(row => ({
		slug: row[0],
		name: row[1],
		manufacturer: row[2],
		year: row[3],
		status: STATUS_BY_CODE[row[4]] ?? 'stub',
		platform: row[5],
		drivers: row[6],
		switches: row[7],
		lamps: row[8],
		coils: row[9],
		mechanisms: row[10],
		highlights: row[11] ?? [],
		definition: row[12] ?? '',
		roms: row[13] ?? [],
		completionScore: row[14] ?? 0,
		// Absent from an index generated before this column existed, and absent in
		// spirit from any build that ran without the upstream checkout — both mean
		// the same thing to every consumer, so both decode to zero.
		memoryMaps: row[15] ?? 0,
	}))
}

/**
 * Newest ROM revision first — an author is almost always binding a recent one,
 * and the truncated table should show those rather than the 1990 prototype.
 *
 * Year alone is too coarse (a machine's whole driver family usually shares one),
 * so the revision encoded in the set name breaks the tie. Numeric collation
 * makes that work on the digits rather than the characters: `mtl_180` sorts
 * above `mtl_103` above `mtl_052`, where a plain string compare would not.
 */
const driverCollator = new Intl.Collator('en', { numeric: true, sensitivity: 'base' })

export function byNewestFirst(a: { id: string, year?: string | null }, b: { id: string, year?: string | null }) {
	return Number(b.year ?? 0) - Number(a.year ?? 0) || driverCollator.compare(b.id, a.id)
}

export const platformShort = (platform: string | null | undefined) =>
	platform ? platform.replace(/^pinmame\./, '').toUpperCase() : '—'

export const platformSlug = (platform: string) => platform.toLowerCase().replace(/[^a-z0-9]+/g, '-')
