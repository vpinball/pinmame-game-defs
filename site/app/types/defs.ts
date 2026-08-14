export type CoverageStatus = 'stub' | 'partial' | 'author_ready'

export type ProvenanceStatus = 'unknown' | 'candidate' | 'observed' | 'validated' | 'conflicted' | 'deprecated'

export interface Alias {
	namespace: string
	value: string
}

export interface Provenance {
	status: ProvenanceStatus
	source_refs?: string[]
}

export interface Binding {
	group: string
	device: number
	channel?: string
}

export interface Wiring {
	board?: string
	drive_connection?: string
	drive_wire?: string
	return_connection?: string
	return_wire?: string
	control_wire?: string
	driver_transistor?: string
	connector?: string
	[key: string]: string | undefined
}

export interface SpatialPlacement {
	id: string
	/** `sensor` reads the ball, `effect` moves it, `emitter` lights it. */
	role: 'sensor' | 'effect' | 'emitter'
	space: 'playfield'
	/** Normalised player view: x 0 = left, y 0 = rear/backglass. */
	x: number
	y: number
	provenance?: Provenance
}

export type Spatial =
	| { status: 'candidate' | 'observed' | 'validated' | 'conflicted', placements: SpatialPlacement[] }
	| { status: 'not_applicable', reason: string, provenance?: Provenance }

export interface Device {
	id: string
	kind: string
	label: string
	binding: Binding
	aliases?: Alias[]
	roles?: string[]
	availability?: 'used' | 'unused' | 'optional'
	normally_closed?: boolean
	pulse?: boolean
	physical?: { switch_type?: string, [key: string]: unknown }
	wiring?: Wiring
	spatial?: Spatial
	provenance?: Provenance
	notes?: string
}

export interface Display {
	id: string
	kind: string
	label: string
	width?: number
	height?: number
	provenance?: Provenance
}

export interface Mechanism {
	id: string
	kind: string
	label: string
	behavior?: string
	actuators?: string[]
	sensors?: string[]
	provenance?: Provenance
}

export interface Relationship {
	id: string
	kind: string
	source: string
	destination: string
	provenance?: Provenance
}

/** A transcribed region of a source, so a reader can see what it actually said. */
export interface Excerpt {
	id: string | null
	/** Where in the source this region is: page, sheet, drawing number, block. */
	locator: string | null
	/** The transcription, already rendered. */
	html: string
	/** Repository path, for linking back to the file. */
	path: string
	/** Rendered page crop, for facts that are drawings rather than tables. */
	imageUrl: string | null
	imageDerivation: string | null
	method: string | null
	transcribedBy: string | null
	reviewed: boolean | null
}

export interface Source {
	/** Controller-profile citations omit both of these. */
	id?: string
	kind?: string
	uri?: string
	locator?: string
	revision?: string
	sha256?: string
	excerpts?: Excerpt[]
	license?: string
	attribution?: string
	rights?: string
	original_filename?: string
	acquired_at?: string
	source_id?: string
}

/**
 * A conflict as the page consumes it — enriched at build time by
 * `scripts/conflicts.ts` from the raw record's single prose field.
 */
export interface RichConflict {
	id: string
	/** `ignored` = a real disagreement that cannot reach a recreation. */
	status: 'unresolved' | 'ignored'
	/** Why it cannot reach one. Present only on an ignored conflict. */
	rationaleHtml: string | null
	/** Humanised id, or null when it only restates the address. */
	title: string | null
	path: string | null
	/** The addresses in dispute, where the free-form `path` could be parsed. */
	targets: { label: string, group: string | null }[]
	bodyHtml: string
	/** What a human has to go and do, when the record says. */
	resolutionHtml: string | null
	sources: {
		id: string
		kind: string | null
		uri: string | null
		locator: string | null
		/** True when `source_refs` names an id the definition does not define. */
		missing: boolean
	}[]
}

export interface DriverVariant {
	id: string
	description: string
	year?: string
	manufacturer?: string
	clone_of?: string
	flags?: number
	physical_compatibility?: string
	variant_notes?: string
}

export interface CatalogDriver {
	id: string
	description: string
	year?: string
	manufacturer?: string
	clone_of?: string
	root_driver: string
	machine_id: string
	coverage_status: CoverageStatus
}

/* ---------------------------------------------------------------------------
   External data

   Read-only material generated at build time from an upstream project that this
   repository does not own. It is checked out during the site build, never copied
   into canonical repository data, and it carries its own licence and provenance.

   Deliberately a separate branch of `MachineDetail` rather than extra `sources`
   entries: a `Source` is evidence a curator read and weighed, and this is not —
   nothing here contributes to a machine's coverage.
--------------------------------------------------------------------------- */

/** Where an external dataset came from, and under what terms it may be shown. */
export interface ExternalSourceRef {
	/** Upstream repository — a URL, or `owner/name`. */
	repository: string
	/** Full commit the build pinned. */
	commit: string
	/** SPDX identifier of the upstream licence. */
	license: string
	attribution: string
}

/** One upstream memory map, as the build-time generator resolved it. */
export interface MemoryMap {
	/** Path of the map within the upstream repository. */
	sourcePath: string
	/** Permalink to that file at the pinned upstream commit. */
	sourceUrl: string
	/** The copy this site generated, served as a static asset. */
	dataUrl: string
	/** Memory platform the map describes, in upstream's own vocabulary. */
	platform: string
	/** Exact upstream and generated copies of that platform's memory layout. */
	platformSourceUrl: string
	platformDataUrl: string
	/** Upstream's own file-format and content revisions, when it states them. */
	fileFormat: number | null
	version: number | null
	/** ROM sets the upstream map names. */
	roms: string[]
	/** Catalog drivers those ROM names resolved to on this machine. */
	matchedDrivers: string[]
	/** Named regions the map documents. */
	sections: string[]
}

export interface PinballMemoryMaps {
	source: ExternalSourceRef
	maps: MemoryMap[]
}

/** Optional, and absent for every machine no upstream dataset covers. */
export interface ExternalData {
	pinballMemoryMaps?: PinballMemoryMaps
}

export interface MachineDetail {
	slug: string
	format: string
	schema_version: number
	machine: {
		id: string
		name: string
		manufacturer: string
		year?: number
		ipdb_id?: number
	}
	controller?: {
		platform?: string
		inversion_applied_by_emulator?: boolean
	}
	coverage: {
		status: CoverageStatus
		completion_score: number
		missing: string[]
		dimensions: Record<string, string>
	}
	knowledge?: { path?: string, status?: string }
	inputs: Device[]
	outputs: Device[]
	displays: Display[]
	mechanisms: Mechanism[]
	relationships: Relationship[]
	drivers: DriverVariant[]
	sources: Source[]
	conflicts: RichConflict[]
	sourcePath: string
	knowledgePath: string | null
	knowledgeHtml: string | null
	knowledgeHeadings: { id: string, text: string }[]
	/** Leading `Label: **value**` lines, lifted out of the note's prose. */
	knowledgeSummary: { label: string, value: string }[]
	catalogDrivers: CatalogDriver[]
	/**
	 * Generated from upstream projects at build time. Never canonical, never part
	 * of coverage — see `ExternalData`.
	 */
	externalData?: ExternalData
	/** The title this machine is one edition of, when it has siblings. */
	family: { slug: string, title: string, editions: number, differences: string | null } | null
	related: { slug: string, name: string, manufacturer: string, year: number | null, status: CoverageStatus }[]
}

/** Row shape of `data/machines.json` — positional to keep the index small. */
export interface MachineSummary {
	slug: string
	name: string
	manufacturer: string
	year: number | null
	status: CoverageStatus
	completionScore: number
	platform: string | null
	drivers: number
	switches: number
	lamps: number
	coils: number
	mechanisms: number
	highlights: string[]
	definition: string
	roms: string[]
	/**
	 * External memory maps joining this machine by exact driver id — see
	 * `ExternalData`. Zero when the build ran without an upstream checkout, and
	 * zero is the only signal the browse page needs to render nothing.
	 *
	 * Independent of `status`: a stub with a matching ROM name has one, and an
	 * author-ready machine may have none. Never treat it as coverage.
	 */
	memoryMaps: number
}

/** Editions of one title, derived from the shared PinMAME driver prefix. */
export interface MachineFamily {
	slug: string
	title: string
	manufacturer: string
	/** Null once the family is authored rather than inferred from ROM names. */
	driverPrefix: string | null
	/** True when the catalog states the grouping instead of the site deriving it. */
	authored: boolean
	/** Shared overview prose from the family's knowledge note. */
	overviewHtml: string | null
	years: [number, number]
	machines: {
		slug: string
		name: string
		/** The name with the shared title removed — "Pro", "Vault Edition". */
		edition: string
		/** Authored prose: what this edition has that its siblings do not. */
		differences: string | null
		year: number | null
		status: CoverageStatus
		platform: string | null
		drivers: number
		counts: { switches: number, lamps: number, coils: number, flashers: number, gi: number, mechanisms: number }
		mechanismKinds: Record<string, number>
		displays: string[]
	}[]
}

/** One field of one type, as `scripts/prepare-schema.ts` describes it. */
export interface SchemaField {
	name: string
	type: string
	/** Anchor of the type describing this field, when it has one. */
	link: string | null
	required: boolean
	description: string
	values: string[]
	constraints: string[]
	/** What this id points at — the one thing JSON Schema cannot say. */
	reference: string | null
}

export interface SchemaType {
	id: string
	name: string
	kind: 'root' | 'object' | 'union' | 'scalar'
	description: string
	fields: SchemaField[]
	values: string[]
	pattern: string | null
	variants: { name: string, link: string }[]
	/** Constraints about the whole object rather than one field. */
	rules: string[]
	usedBy: { type: string, link: string, field: string }[]
}

export interface SchemaReference {
	documents: {
		id: string
		title: string
		blurb: string
		path: string
		schemaTitle: string
		types: SchemaType[]
	}[]
}

export interface ControllerGroup {
	id: string
	direction: string
	kind: string
	label: string
	address_rules?: { minimum?: number, maximum?: number, values?: number[] }[]
	transports?: Record<string, Record<string, unknown>>
	notes?: string
	notes_format?: 'plain_text' | 'markdown'
	notesHtml?: string | null
}

export interface PlatformEntry {
	id: string
	slug: string
	hardwareFamily: string | null
	hasProfile: boolean
	sourcePath: string | null
	groupCount: number
	inversionAppliedByEmulator: boolean | null
	machines: number
	authorReady: number
	examples: { slug: string, name: string }[]
	profile: {
		id: string
		authority: string
		hardware_family: string
		inversion_applied_by_emulator: boolean
		groups: ControllerGroup[]
		sources?: Source[]
	} | null
}

export interface DriverEntry {
	id: string
	description: string
	year: string | null
	manufacturer: string | null
	cloneOf: string | null
	rootDriver: string
	machineId: string
	machineSlug: string
	machineName: string
	status: CoverageStatus
	/**
	 * The upstream memory map this ROM set resolves to, when one exists. A
	 * per-driver pointer, not the full record the machine page renders.
	 */
	memoryMap?: { sourcePath: string, dataUrl: string, platform: string } | null
}

export interface SearchRow {
	/** machine · driver · family */
	t: 'm' | 'd' | 'f'
	s: string
	n: string
	d: string
	k: string
	c: CoverageStatus
}

export interface SiteData {
	generatedAt: string
	pinmameRevision: string
	libraryVersion: string
	schemaVersion: number
	summary: Record<string, number>
	coverage: Record<string, any> | null
	counts: {
		machines: number
		drivers: number
		authorReady: number
		partial: number
		stub: number
		platforms: number
		profiles: number
		manufacturers: number
	}
	decades: { decade: number, total: number, authorReady: number, partial: number }[]
	manufacturers: { name: string, machines: number, authorReady: number, partial: number }[]
	/** Totals of what the corpus describes today, across every definition. */
	corpus: {
		switches: number
		lamps: number
		coils: number
		flashers: number
		gi: number
		mechanisms: number
		relationships: number
		sources: number
		conflicts: number
	}
	missing: { requirement: string, count: number }[]
	platforms: { id: string, slug: string, hardwareFamily: string | null, hasProfile: boolean, machines: number, authorReady: number }[]
	abstractParents: { id: string, direct_child_count: number }[]
	/**
	 * Roll-up of the external datasets this build pinned. Empty when none were
	 * configured. Kept apart from `counts` and `corpus`, which describe what this
	 * repository itself has curated.
	 */
	externalSources?: {
		pinballMemoryMaps?: ExternalSourceRef & {
			mapCount: number
			matchedDriverCount: number
			/** ROM names upstream carries that no catalog driver resolves. */
			unmatchedRomCount: number
		}
	}
}
