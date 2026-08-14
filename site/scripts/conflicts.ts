/**
 * Turns a conflict record into something a reader can act on.
 *
 * A conflict is the catalog admitting that two sources disagree and nobody has
 * settled it. The record carries that as one unbroken paragraph of prose — up
 * to 2 000 characters of it — with the address, the disagreeing parties, the
 * evidence and the way out all run together. The reader's actual questions are
 * narrower: *which address is affected*, *who disagrees*, and *what would it
 * take to settle this*. Each is pulled out here so the page can answer them
 * without making anyone read a wall of text first.
 *
 * The prose itself is never rewritten, only marked up: identifiers become code,
 * PinMAME source paths become links into the pinned revision, and long passages
 * are broken into paragraphs at sentence boundaries.
 */

const PINMAME_REPO = 'https://github.com/vpinball/pinmame'

export type ConflictSourceRef = {
	id: string
	kind: string | null
	uri: string | null
	locator: string | null
	/** True when `source_refs` names an id the definition does not define. */
	missing: boolean
}

export type ConflictTarget = { label: string, group: string | null }

export type RichConflict = {
	id: string
	/** Humanised id, or null when it only restates the address. */
	title: string | null
	path: string | null
	targets: ConflictTarget[]
	bodyHtml: string
	/** What a human has to go and do, when the record says. */
	resolutionHtml: string | null
	sources: ConflictSourceRef[]
}

const escape = (text: string) =>
	text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

/**
 * Tokens that are code rather than prose. Deliberately narrow: a false positive
 * puts an ordinary English word in a monospace box on sixty machine pages,
 * which is worse than missing one. Every pattern requires a shape English does
 * not have — a call, an assignment, an underscore, a file extension.
 */
const CODE_PATTERNS: RegExp[] = [
	// The name must look like an identifier. `\w+` alone turns the ordinary
	// English of "an #define block" into code.
	/#define\s+(?=\w*[A-Z_0-9])\w+(?:\s+\w+\([^)]*\))?/g,
	/\b[A-Za-z_]\w*\([^()\s]{0,40}\)/g, //  SolCallback(56), CORE_CUSTSOLNO(6)
	/\b\w+\s*=\s*-?\d+\b/g, //              swLRampEnt=84
	/\b[A-Za-z]+\d*_\w+\b/g, //             SW85_Hit, tz_handleMech
	/\b[a-z]\w*\.[ch]\b/g, //               gw.c
	/\b[A-Z]{2,}\d{2,}\b/g, //              FLIP3031
]

/** `src/wpc/sims/wpc/full/tz.c` — linkable into the pinned PinMAME tree. */
const SOURCE_PATH = /\b(?:src|core)\/[\w./-]+\.[ch]\b/g

/**
 * Marks up one already-escaped run of prose.
 *
 * Each match is parked behind a placeholder so later patterns cannot match
 * inside markup that earlier ones produced, which is what would otherwise nest
 * a `<code>` inside a link's own href. The sentinels are private-use characters
 * rather than anything resembling text: an early version used ` 12 `, and since
 * conflict prose is full of bare numbers — "binds its top right lane insert to
 * PinMAME lamp 65" — it swapped lamp numbers for code spans from elsewhere in
 * the paragraph.
 */
function markup(text: string, revision: string): string {
	const held: string[] = []
	const OPEN = ''
	const CLOSE = ''
	const hold = (html: string) => {
		held.push(html)
		return `${OPEN}${held.length - 1}${CLOSE}`
	}

	let out = escape(text)

	// Backticks first: the author marking something as code beats any guess.
	out = out.replace(/`([^`]+)`/g, (_, code: string) => hold(`<code>${code}</code>`))

	out = out.replace(SOURCE_PATH, path =>
		hold(`<a href="${PINMAME_REPO}/blob/${revision}/${path}" target="_blank" rel="noopener noreferrer"><code>${path}</code></a>`))

	for (const pattern of CODE_PATTERNS) {
		out = out.replace(pattern, match => hold(`<code>${match}</code>`))
	}

	return out.replace(new RegExp(`${OPEN}(\\d+)${CLOSE}`, 'g'), (_, index: string) => held[Number(index)]!)
}

/**
 * Groups sentences into paragraphs. One 2 000-character block is unreadable at
 * any measure, while splitting every sentence turns an argument into a list.
 * Around 300 characters keeps a paragraph to a few lines and leaves reasoning
 * that belongs together in one place.
 */
function paragraphs(text: string, revision: string): string {
	if (!text.trim()) return ''
	const sentences = text.match(/[^.!?]+(?:[.!?]+["')\]]*|$)/g) ?? [text]
	const grouped: string[] = []
	let current = ''

	for (const [index, sentence] of sentences.entries()) {
		current += sentence
		// Not every `.` or `?` ends a sentence: this prose is full of
		// `(Not used?)` and `A-21287-1 … Assy.` mid-clause. Breaking there
		// starts the next paragraph with ", and pulses 32 …". Only break where
		// what follows can actually begin one.
		// The whitespace test matters on its own: `x about .312, .399` splits
		// after the decimal point, and the fragment starts with a digit, which
		// otherwise looks like a legitimate new sentence.
		const following = sentences[index + 1] ?? ''
		const next = following.trimStart()
		if (current.length >= 300 && /^\s/.test(following) && /^[A-Z0-9"'`(]/.test(next)) {
			grouped.push(current.trim())
			current = ''
		}
	}
	if (current.trim()) {
		// A short tail reads as an afterthought; fold it into the previous one.
		if (grouped.length && current.trim().length < 120) grouped[grouped.length - 1] += ` ${current.trim()}`
		else grouped.push(current.trim())
	}

	return grouped.map(part => `<p>${markup(part, revision)}</p>`).join('')
}

/** `conflict.aux-lamp-65-97-top-lane-binding` -> `Aux lamp 65 97 top lane binding`. */
function humanise(id: string) {
	const stem = id.replace(/^conflict\./, '').replace(/[-_.]+/g, ' ').trim()
	return stem ? stem.charAt(0).toUpperCase() + stem.slice(1) : ''
}

const alphanumeric = (text: string) => text.toLowerCase().replace(/[^a-z0-9]/g, '')

/**
 * Reads the addresses out of `path`. The field has no single grammar — JSON
 * Pointer, bracket queries, colon-separated and dotted forms all appear across
 * the catalog — so each known shape is tried and anything unrecognised is left
 * for the caller to show verbatim rather than guessed at.
 */
function targetsOf(path: string | undefined): ConflictTarget[] {
	if (!path) return []
	const targets: ConflictTarget[] = []
	const seen = new Set<string>()
	const add = (label: string, group: string | null = null) => {
		const key = `${group}:${label}`
		if (label && !seen.has(key)) {
			seen.add(key)
			targets.push({ label, group })
		}
	}

	// binding:pinmame.output.solenoid/56,57/None
	for (const match of path.matchAll(/binding:([\w.]+)\/([\d,\s-]+)/g)) {
		for (const device of match[2]!.split(',')) add(device.trim(), match[1]!)
	}

	// outputs[binding.group=pinmame.output.gi,binding.device=1,4]
	for (const match of path.matchAll(/binding\.group=([\w.]+)/g)) {
		const devices = /(?:binding\.)?device=([\d,\s-]+)/.exec(path)
		const list = (devices?.[1] ?? '').split(',').map(part => part.trim()).filter(Boolean)
		for (const device of list) add(device, match[1]!)
		if (!list.length) add(match[1]!.split('.').pop()!, match[1]!)
	}

	// inputs[binding.device=37,38] / outputs[device=3,4]
	if (!/binding\.group=/.test(path)) {
		for (const match of path.matchAll(/\b(inputs|outputs)\[(?:binding\.)?device=([\d,\s-]+)\]/g)) {
			for (const device of match[2]!.split(',')) {
				add(device.trim(), match[1] === 'inputs' ? 'input' : 'output')
			}
		}
	}

	// /inputs/switch.matrix-15, outputs[id=coil.driver-22]
	for (const match of path.matchAll(/\/(?:inputs|outputs|mechanisms)\/([\w.*{}\-,]+)/g)) add(match[1]!)
	for (const match of path.matchAll(/\bid=([\w.-]+)/g)) add(match[1]!)

	return targets
}

export function enrichConflict(conflict: any, sources: any[], revision: string): RichConflict {
	const description: string = (conflict.description ?? '').trim()

	// "Resolution path: …" is the record telling a human what to go and do. It
	// is the most actionable sentence in the whole field, and it is buried at
	// the end of a paragraph nobody finishes.
	const split = /(?:^|\s)Resolution path:\s*/i.exec(description)
	const body = (split ? description.slice(0, split.index) : description).trim()
	const resolution = split ? description.slice(split.index + split[0].length).trim() : ''

	// The trailing "Unresolved." restates the panel's own heading.
	const stripUnresolved = (text: string) => text.replace(/\s*Unresolved\.\s*$/i, '').trim()

	const byId = new Map(sources.map(source => [source.id, source]))
	const refs: ConflictSourceRef[] = (conflict.source_refs ?? []).map((id: string) => {
		const source = byId.get(id)
		return {
			id,
			kind: source?.kind ?? null,
			uri: source?.uri ?? null,
			locator: source?.locator ?? null,
			missing: !source,
		}
	})

	const title = humanise(conflict.id)
	const path: string = conflict.path ?? ''
	const settled = stripUnresolved(resolution)

	return {
		id: conflict.id,
		// Auto-generated ids restate the binding they came from, and a heading
		// that repeats the chip beside it is noise.
		title: title && alphanumeric(title) !== alphanumeric(path) ? title : null,
		path: path || null,
		targets: targetsOf(path),
		bodyHtml: paragraphs(stripUnresolved(body), revision),
		resolutionHtml: settled ? markup(settled, revision) : null,
		sources: refs,
	}
}
