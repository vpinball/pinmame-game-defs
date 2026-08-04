/**
 * Turns the catalog's JSON Schemas into a reference table per type.
 *
 * Reads `schemas/*.schema.json` from the defs repository and emits
 * `data/schema.json`: one entry per object the schema defines, with its fields,
 * types, enum values, constraints and required-ness. The `/schema` page renders
 * that directly, so a field added upstream documents itself on the next build.
 *
 * Two things the schema cannot say are stated here instead, and both are
 * checked on every run so they cannot quietly rot:
 *
 *   - REFERENCES: which `identifier` fields hold the id of something else. In
 *     JSON Schema they are all just strings.
 *   - NOTES: a sentence where the schema has no `description` and the field
 *     name is not self-explanatory.
 *
 * Runs as part of `npm run data`.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const projectRoot = resolve(here, '..')

/** Same resolution order as prepare-data.ts. */
function findDefsRoot(): string {
	const candidates = [
		process.env.PINMAME_DEFS_ROOT,
		resolve(projectRoot, '..'),
		resolve(projectRoot, '../pinmame-game-defs'),
		resolve(projectRoot, '../.worktrees/pinmame-game-defs-machine-definitions'),
	].filter(Boolean) as string[]

	for (const candidate of candidates) {
		if (existsSync(join(candidate, 'schemas', 'machine.schema.json'))) return candidate
	}
	throw new Error(
		'Could not locate the pinmame-game-defs checkout. Set PINMAME_DEFS_ROOT to a directory containing schemas/machine.schema.json.\nTried:\n  '
		+ candidates.join('\n  '),
	)
}

const defsRoot = findDefsRoot()

// ---------------------------------------------------------------------------
// the documents to describe, and the two things their schemas cannot say
// ---------------------------------------------------------------------------

const DOCUMENTS = [
	{
		id: 'machine',
		file: 'machine.schema.json',
		title: 'Machine definition',
		blurb: 'One document per physical machine: what the ROM can address, what each address is on the '
			+ 'real playfield, and where every claim came from. This is the file behind each machine page.',
	},
	{
		id: 'controller',
		file: 'controller.schema.json',
		title: 'Controller profile',
		blurb: 'One document per controller platform: the address groups a machine on that platform may bind '
			+ 'to, the legal numbers in each, and whether the emulator has already normalised polarity.',
	},
]

/**
 * Fields holding the id of something else. JSON Schema has no way to express
 * this — every one of them is just a string matching the identifier pattern —
 * so the graph of what points at what lives here.
 */
const REFERENCES: Record<string, string> = {
	'machine:controller.platform': 'the id of a controller profile',
	'machine:driver.clone_of': 'another driver id in this document',
	'machine:mechanism.actuators': 'output ids',
	'machine:mechanism.sensors': 'input ids',
	'machine:mechanism.positions.sensors': 'input ids',
	'machine:relationship.source': 'an input id',
	'machine:relationship.destination': 'an output id',
	'machine:provenance.source_refs': 'source ids',
	'machine:conflict.source_refs': 'source ids',
	'machine:displayOverride.target': 'a display id',
	'machine:deviceOverride.target': 'an input or output id',
	'machine:output.model': 'a shared behaviour model',
	'machine:input.roles': 'portable role names such as cabinet.start or ball.position',
	'machine:output.roles': 'portable role names, engine-neutral',
}

/**
 * Sentences for fields the schema does not describe and whose names do not
 * carry the meaning on their own. Anything with a `description` upstream is
 * left alone — that text is the schema's to own.
 */
const NOTES: Record<string, string> = {
	'machine:__root__.format': 'Identifies the document type. Always this exact string.',
	'machine:machineIdentity.id': 'The physical product: one playfield, one wiring loom, one definition, however many ROM revisions exist.',
	'machine:machineIdentity.year': 'Null where the release year is genuinely unknown rather than merely unrecorded.',
	'machine:coverage.status': 'Fail-closed. Only the completeness validator may grant author_ready; do not set it by hand.',
	'machine:coverage.missing': 'The authoring requirements not yet satisfied. Empty is what author_ready requires.',
	'machine:coverage.dimensions': 'How well each axis of the definition is established. Keys are the seven axes below.',
	'machine:driver.id': 'One exact PinMAME ROM set. Many drivers resolve to one machine.',
	'machine:driver.flags': 'The PinMAME driver flags for this set, as a bitfield.',
	'machine:binding.group': 'Names the address space. The platform profile says which numbers are legal in it.',
	'machine:binding.device': 'The number PinMAME reports, not a hardware pin. Negative numbers are real: they carry dedicated and diagnostic inputs from outside the matrix.',
	'machine:binding.channel': 'Only meaningful for an rgb_lamp, which binds one channel per colour.',
	'machine:alias.namespace': 'Which naming system the value belongs to — vpx, pinmame, the operator manual.',
	'machine:alias.value': 'The name that namespace uses for this device.',
	'machine:input.id': 'The stable semantic name a table should bind to. If a controller number ever changes, this does not.',
	'machine:input.normally_closed': 'A fact about the real part — an opto conducting at rest, a drop target closed while raised. Build the hardware behaviour; do not convert it into a runtime flip.',
	'machine:input.pulse': 'The switch fires its coil directly in copper, so it must act whether or not a game is running.',
	'machine:input.availability': 'unused means the address was checked and found to have nothing wired to it — which is not the same as nobody having looked.',
	'machine:output.id': 'The stable semantic name a table should bind to.',
	'machine:output.availability': 'unused means the address was checked and found to drive nothing.',
	'machine:output.range': 'The travel of a servo or other modulated drive.',
	'machine:mechanism.behavior': 'How the assembly acts, in prose: what ejects, what confirms, what state it starts in.',
	'machine:mechanism.positions': 'The named states the assembly can be in, and the sensors that report each.',
	'machine:relationship.kind': 'pulse is the one to watch: the switch fires the coil in hardware, so pops and slings must not wait for the ROM.',
	'machine:source.uri': 'Where the source lives. Never a copy of the source itself — no ROM, manual or table binary is committed.',
	'machine:source.locator': 'The exact place inside it: page, line range or section.',
	'machine:source.known_working': 'This table is known to run the real ROM, which is what makes it authoritative on bindings.',
	'machine:conflict.path': 'Where in the document the sources disagree.',
	'machine:conflict.source_refs': 'At least two, since a conflict needs two sides.',
	'machine:physical.location': 'Prose from the manual. Never used to infer coordinates — that is what spatial is for.',
	'machine:knowledge.path': 'The recreation note beside this definition.',
	'machine:spatialPlacement.role': 'What the device does at that point: reads the ball, moves it, or lights it.',
	'machine:spatialPlacement.x': '0 is the left edge of the playfield, 1 the right.',
	'machine:spatialPlacement.y': '0 is the rear, at the backglass end; 1 is the front, at the apron.',
	'machine:provenance.status': 'How well this single assertion is established — not how complete the document is.',
	'machine:provenance.source_refs': 'At least one. An assertion the catalog cannot attribute does not belong in it.',
	'controller:__root__.format': 'Identifies the document type. Always this exact string.',
	'controller:__root__.inversion_applied_by_emulator': 'Always true: PinMAME reports logical active state, so inverting again in a table boots every optical switch backwards.',
	'controller:group.id': 'The value a device binding names in its group field.',
	'controller:group.direction': 'Which way the data flows across this group.',
	'controller:addressRule.values': 'An explicit list, where the legal numbers are not a contiguous range.',
	'controller:group.transports': 'How this group reaches the emulator, per integration.',
}

/** Definitions that name a value rather than a shape, and so describe nothing by themselves. */
const TYPE_NOTES: Record<string, string> = {
	'machine:identifier': 'The shape every id in the catalog takes: lowercase, dot, hyphen or underscore separated.',
	'machine:assertionState': 'How well one assertion is established. Per claim, not per document — observing that an output toggled is not the same as knowing what it drives, and failing to observe one is not evidence that it is unused.',
}

// ---------------------------------------------------------------------------
// schema -> model
// ---------------------------------------------------------------------------

type Node = Record<string, any>

type Field = {
	name: string
	type: string
	/** Anchor of the type this field is described by, when it has one. */
	link: string | null
	required: boolean
	description: string
	values: string[]
	constraints: string[]
	reference: string | null
}

type SchemaType = {
	id: string
	name: string
	kind: 'root' | 'object' | 'union' | 'scalar'
	description: string
	fields: Field[]
	/** Enum members or pattern, for the definitions that are just a value. */
	values: string[]
	pattern: string | null
	/** One-of variants, for a definition that is a choice between shapes. */
	variants: { name: string, link: string }[]
	/** Constraints about the whole object rather than one field. */
	rules: string[]
	/** Reverse index: every field elsewhere that is described by this type. */
	usedBy: { type: string, link: string, field: string }[]
}

const usedNotes = new Set<string>()
const usedReferences = new Set<string>()
const usedTypeNotes = new Set<string>()

const anchor = (docId: string, name: string) =>
	`${docId}-${name.replace(/\[\]/g, '').replace(/[._]/g, '-').replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()}`

/** `machineIdentity` -> `machine identity`; dotted synthetic names stay as they are. */
const displayName = (name: string) =>
	name.includes('.') ? name : name.replace(/([a-z0-9])([A-Z])/g, '$1 $2').toLowerCase()

function buildDocument(doc: typeof DOCUMENTS[number]) {
	// Repo-relative and always forward-slashed: it is shown to readers and fed
	// to GitHub blob URLs, neither of which wants a Windows separator.
	const path = `schemas/${doc.file}`
	const schema: Node = JSON.parse(readFileSync(join(defsRoot, path), 'utf8'))
	const defs: Record<string, Node> = schema.$defs ?? {}
	const types: SchemaType[] = []
	const byName = new Map<string, SchemaType>()

	const refName = (node: Node | undefined): string | null =>
		typeof node?.$ref === 'string' ? node.$ref.replace('#/$defs/', '') : null

	/** True for a definition that exists only to name a scalar. */
	const isScalar = (node: Node) => !node.properties && !node.oneOf && !node.anyOf && node.type !== 'object'

	function constraintsOf(node: Node): string[] {
		const out: string[] = []
		const item = node.type === 'array' ? node : null
		if (node.minLength) out.push(`at least ${node.minLength} character${node.minLength === 1 ? '' : 's'}`)
		if (node.minimum !== undefined) out.push(`minimum ${node.minimum}`)
		if (node.exclusiveMinimum !== undefined) out.push(`greater than ${node.exclusiveMinimum}`)
		if (node.maximum !== undefined) out.push(`maximum ${node.maximum}`)
		if (item?.minItems) out.push(`at least ${item.minItems} item${item.minItems === 1 ? '' : 's'}`)
		if (item?.uniqueItems) out.push('unique')
		if (node.format) out.push(node.format)
		if (node.pattern && !/^\^\[a-z0-9\]/.test(node.pattern)) out.push(`pattern ${node.pattern}`)
		return out
	}

	function valuesOf(node: Node): string[] {
		if (node.const !== undefined) return [String(node.const)]
		if (node.enum) return node.enum.map(String)
		if (node.type === 'array' && node.items?.enum) return node.items.enum.map(String)
		return []
	}

	/**
	 * Inline objects get a type of their own rather than being flattened into
	 * their parent's row, so nothing in the schema goes undescribed.
	 */
	function synthesise(parent: string, field: string, node: Node): string {
		// A field of the root document is better known by its own name than by
		// `__root__.something`, as long as no definition already claims it.
		const preferred = parent === '__root__' ? field : `${parent}.${field}`
		const name = defs[preferred] ? `${parent}.${field}` : preferred
		if (!byName.has(name)) register(name, node, 'object')
		return name
	}

	/**
	 * Renders a JSON Schema fragment as a phrase — "coverage.status is
	 * author_ready", "dimensions includes spatial_placement" — so the
	 * conditional rules an `if`/`then` expresses can be read as sentences
	 * rather than looked up in the file.
	 */
	function phrases(node: Node, prefix = ''): string[] {
		const out: string[] = []
		for (const [name, value] of Object.entries((node.properties ?? {}) as Record<string, Node>)) {
			const path = prefix ? `${prefix}.${name}` : name
			if (value.const !== undefined) out.push(`${path} is ${value.const}`)
			else if (value.enum?.length === 1) out.push(`${path} is ${value.enum[0]}`)
			else out.push(...phrases(value, path))
		}
		for (const name of (node.required ?? []) as string[]) {
			if (!node.properties?.[name]) out.push(prefix ? `${prefix} includes ${name}` : `${name} is present`)
		}
		return out
	}

	/** "a, b and c" — named `sentence` because `join` is node:path's. */
	const sentence = (parts: string[]) => parts.length > 1
		? `${parts.slice(0, -1).join(', ')} and ${parts[parts.length - 1]}`
		: parts[0] ?? ''

	/**
	 * The constraints that are about the document as a whole rather than about
	 * one field: `allOf` conditionals, and a `oneOf`/`anyOf` that only says
	 * which combinations of fields are acceptable.
	 */
	function rulesOf(node: Node): string[] {
		const conditionals = ((node.allOf ?? []) as Node[])
			.map((rule) => {
				const when = sentence(phrases(rule.if ?? {}))
				const then = sentence(phrases(rule.then ?? {}))
				return when && then ? `When ${when}, ${then}.` : ''
			})
			.filter(Boolean)

		const choose = (options: Node[], word: string) => {
			if (!options.length || !options.every(option => Object.keys(option).length === 1 && option.required)) return ''
			// One name per option reads as a plain list; multi-field options have
			// to stay grouped, or "minimum and maximum, or values" loses its shape.
			const grouped = options.some(option => (option.required as string[]).length > 1)
			const combinations = options.map(option => sentence(option.required as string[]))
			return `${word} ${grouped ? combinations.join(', or ') : sentence(combinations)}.`
		}

		return [
			...conditionals,
			choose(node.anyOf ?? [], 'Needs at least one of'),
			choose(node.oneOf ?? [], 'Needs exactly one of'),
		].filter(Boolean)
	}

	/** The type a field is described by, if any, plus how to print it. */
	function typeOf(node: Node, owner: string, field: string): { type: string, target: string | null } {
		const direct = refName(node)
		if (direct) return { type: displayName(direct), target: direct }

		if (node.type === 'array') {
			const inner = typeOf(node.items ?? {}, owner, field)
			return { type: `${inner.type}[]`, target: inner.target }
		}
		if (node.const !== undefined) return { type: typeof node.const === 'string' ? 'string' : typeof node.const, target: null }
		if (node.enum) return { type: 'enum', target: null }

		const mapOf = refName(node.additionalProperties)
		if (mapOf) return { type: `map of ${displayName(mapOf)}`, target: mapOf }

		if (node.properties) return { type: 'object', target: synthesise(owner, field, node) }
		if (node.oneOf || node.anyOf) return { type: 'object', target: synthesise(owner, field, node) }
		if (Array.isArray(node.type)) return { type: node.type.filter((t: string) => t !== 'null').join(' or '), target: null }
		return { type: node.type ?? 'any', target: null }
	}

	function fieldsOf(owner: string, node: Node): Field[] {
		const required = new Set<string>(node.required ?? [])
		const entries = Object.entries(node.properties ?? {}) as [string, Node][]

		const fields = entries.map(([name, value]) => {
			const key = `${doc.id}:${owner}.${name}`
			const { type, target } = typeOf(value, owner, name)

			if (NOTES[key]) usedNotes.add(key)
			if (REFERENCES[key]) usedReferences.add(key)

			return {
				name,
				type,
				link: target ? anchor(doc.id, target) : null,
				required: required.has(name),
				description: (value.description as string | undefined)?.trim() || NOTES[key] || '',
				values: valuesOf(value),
				constraints: constraintsOf(value),
				reference: REFERENCES[key] ?? null,
			}
		})

		// Required first, schema order within each half: a reader wants "what a
		// document must carry" before "what it may carry".
		return [...fields.filter(f => f.required), ...fields.filter(f => !f.required)]
	}

	function typeNote(name: string) {
		const key = `${doc.id}:${name}`
		if (TYPE_NOTES[key]) usedTypeNotes.add(key)
		return TYPE_NOTES[key] ?? ''
	}

	function register(name: string, node: Node, kind: SchemaType['kind']) {
		const entry: SchemaType = {
			id: anchor(doc.id, name),
			name: name === '__root__' ? doc.title.toLowerCase() : displayName(name),
			kind,
			description: (node.description as string | undefined)?.trim() || typeNote(name),
			fields: [],
			values: node.enum?.map(String) ?? (node.const !== undefined ? [String(node.const)] : []),
			pattern: node.pattern ?? null,
			variants: [],
			rules: [],
			usedBy: [],
		}
		byName.set(name, entry)
		types.push(entry)

		// Registered before the fields are walked, so a self-referencing type
		// (a driver's clone_of, an inline object naming its own parent) cannot
		// recurse forever.
		const variants: Node[] = node.oneOf ?? node.anyOf ?? []
		entry.variants = variants
			.map(variant => refName(variant))
			.filter((target): target is string => Boolean(target))
			.map(target => ({ name: displayName(target), link: anchor(doc.id, target) }))

		entry.rules = rulesOf(node)
		entry.fields = fieldsOf(name, node)
		return entry
	}

	register('__root__', schema, 'root')
	for (const [name, node] of Object.entries(defs)) {
		if (byName.has(name)) continue
		register(name, node, isScalar(node) ? 'scalar' : (node.oneOf || node.anyOf) && !node.properties ? 'union' : 'object')
	}

	// Reverse index, once every type exists.
	const byAnchor = new Map(types.map(type => [type.id, type]))
	for (const type of types) {
		for (const field of type.fields) {
			const target = field.link ? byAnchor.get(field.link) : null
			if (target && target !== type) target.usedBy.push({ type: type.name, link: type.id, field: field.name })
		}
		for (const variant of type.variants) {
			const target = byAnchor.get(variant.link)
			if (target && target !== type) target.usedBy.push({ type: type.name, link: type.id, field: 'one of' })
		}
	}

	return {
		id: doc.id,
		title: doc.title,
		blurb: doc.blurb,
		path,
		schemaTitle: (schema.title as string | undefined) ?? doc.title,
		types,
	}
}

const documents = DOCUMENTS.map(buildDocument)

const stale = (label: string, all: Record<string, unknown>, used: Set<string>) => {
	const orphans = Object.keys(all).filter(key => !used.has(key))
	if (orphans.length) console.warn(`[schema] WARNING ${label} for a field the schema no longer has: ${orphans.join(', ')}`)
}
stale('note', NOTES, usedNotes)
stale('reference', REFERENCES, usedReferences)
stale('type note', TYPE_NOTES, usedTypeNotes)

mkdirSync(join(projectRoot, 'data'), { recursive: true })
writeFileSync(
	join(projectRoot, 'data', 'schema.json'),
	JSON.stringify({ documents }),
)

const typeCount = documents.reduce((total, document) => total + document.types.length, 0)
const fieldCount = documents.reduce(
	(total, document) => total + document.types.reduce((sum, type) => sum + type.fields.length, 0), 0)
console.log(`[schema] documents     : ${documents.length}`)
console.log(`[schema] types         : ${typeCount} (${fieldCount} fields)`)
