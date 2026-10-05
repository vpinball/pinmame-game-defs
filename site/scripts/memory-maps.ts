import { execFileSync } from 'node:child_process'
import { existsSync, lstatSync, mkdirSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'

export const PINBALL_MEMORY_MAPS_REPOSITORY = 'https://github.com/tomlogic/pinball-memory-maps'
/**
 * Since August 2026 upstream licenses the map database under ODbL 1.0 and its
 * individual contents under DbCL 1.0; its LGPL now covers only `tools/`, which
 * this build never reads. Both licence texts sit at the upstream root and are
 * mirrored beside the generated maps.
 */
export const PINBALL_MEMORY_MAPS_LICENSE = 'ODbL-1.0'
export const PINBALL_MEMORY_MAPS_CONTENTS_LICENSE = 'DbCL-1.0'
export const PINBALL_MEMORY_MAPS_LICENSE_FILES = [
	{ license: PINBALL_MEMORY_MAPS_LICENSE, sourcePath: 'LICENSE-ODbL.md' },
	{ license: PINBALL_MEMORY_MAPS_CONTENTS_LICENSE, sourcePath: 'LICENSE-DbCL' },
] as const
/** What every copied map must declare in `_metadata.license`, exactly. */
const MAP_LICENSE = 'Open Data Commons Open Database License (ODbL) v1.0'
export const PINBALL_MEMORY_MAPS_ATTRIBUTION = 'This program makes use of content from the Pinball Memory Maps project.'

export type MemoryMapSummary = {
	sourcePath: string
	sourceUrl: string
	dataUrl: string
	platform: string
	platformSourceUrl: string
	platformDataUrl: string
	fileFormat: number | null
	version: number | null
	roms: string[]
	sections: string[]
}

export type MemoryMapsLicenseFile = {
	license: string
	sourcePath: string
	sourceUrl: string
	dataUrl: string
}

export type MemoryMapsSource = {
	repository: string
	commit: string
	license: string
	contentsLicense: string
	licenseFiles: MemoryMapsLicenseFile[]
	attribution: string
}

export type MemoryMapsBuildData = {
	source: MemoryMapsSource
	maps: MemoryMapSummary[]
	byDriver: Map<string, MemoryMapSummary>
	unmatchedRoms: string[]
}

type MemoryMapDocument = {
	_fileformat?: unknown
	_metadata?: {
		version?: unknown
		platform?: unknown
		license?: unknown
		roms?: unknown
	}
	[key: string]: unknown
}

const DRIVER_ID = /^[a-z0-9_]+$/
const PLATFORM_ID = /^[A-Za-z0-9][A-Za-z0-9._-]*$/
const COMMIT_ID = /^[0-9a-f]{40}$/

function requirePlainObject(value: unknown, label: string): Record<string, unknown> {
	if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${label} must be a JSON object.`)
	return value as Record<string, unknown>
}

function parseJson(bytes: Buffer, label: string): unknown {
	try {
		return JSON.parse(bytes.toString('utf8'))
	} catch (error) {
		throw new Error(`${label} is not valid JSON: ${error instanceof Error ? error.message : String(error)}`)
	}
}

type PinnedTree = {
	/** Exact committed bytes of a regular file, or a fail-closed error. */
	read: (relativePath: string, expectedPrefix?: string) => Buffer
}

/** Paths this build may read; everything else in the commit is never loaded. */
const isReadablePath = (path: string) =>
	path === 'index.json'
	|| PINBALL_MEMORY_MAPS_LICENSE_FILES.some(file => file.sourcePath === path)
	|| (path.startsWith('maps/') && path.endsWith('.map.json'))
	|| (path.startsWith('platforms/') && path.endsWith('.json'))

/**
 * Load the readable files of `commit` straight from the object database, in one
 * `ls-tree` and one `cat-file --batch`. Paths resolve inside the commit's tree,
 * so nothing can escape the checkout, and only regular-file blobs (modes 100644
 * and 100755) are returned: a symlink or submodule entry is refused.
 */
function readPinnedTree(root: string, commit: string): PinnedTree {
	const git = (args: string[], input?: Buffer) =>
		execFileSync('git', ['-C', root, ...args], { input, maxBuffer: 1 << 30 })
	const files = new Map<string, string>()
	const refused = new Set<string>()
	for (const record of git(['ls-tree', '-r', '-z', '--full-tree', commit]).toString('utf8').split('\0')) {
		if (!record) continue
		const match = /^(\d{6}) (\w+) ([0-9a-f]{40,64})\t(.+)$/s.exec(record)
		if (!match) throw new Error(`Unexpected Pinball Memory Maps tree entry: ${record}`)
		const [, mode, type, object, path] = match
		if (!isReadablePath(path!)) continue
		if (type === 'blob' && (mode === '100644' || mode === '100755')) files.set(path!, object!)
		else refused.add(path!)
	}

	const blobs = new Map<string, Buffer>()
	const objects = [...new Set(files.values())]
	if (objects.length) {
		const output = git(['cat-file', '--batch'], Buffer.from(objects.map(object => `${object}\n`).join('')))
		let offset = 0
		for (const object of objects) {
			const headerEnd = output.indexOf(0x0a, offset)
			const header = output.subarray(offset, headerEnd).toString('utf8')
			const match = /^([0-9a-f]+) blob (\d+)$/.exec(header)
			if (!match || match[1] !== object) throw new Error(`Unexpected git cat-file header for ${object}: ${header}`)
			const size = Number(match[2])
			blobs.set(object, output.subarray(headerEnd + 1, headerEnd + 1 + size))
			offset = headerEnd + 1 + size + 1
		}
	}

	return {
		read(relativePath, expectedPrefix) {
			const portable = relativePath.replace(/\\/g, '/')
			const parts = portable.split('/')
			if (!portable || portable.startsWith('/') || parts.some(part => !part || part === '.' || part === '..')) {
				throw new Error(`Unsafe Pinball Memory Maps path: ${relativePath}`)
			}
			if (expectedPrefix && !portable.startsWith(expectedPrefix)) {
				throw new Error(`Pinball Memory Maps path must start with ${expectedPrefix}: ${relativePath}`)
			}
			if (refused.has(portable)) throw new Error(`Pinball Memory Maps path is not a regular file at ${commit}: ${relativePath}`)
			const object = files.get(portable)
			if (!object) throw new Error(`Pinball Memory Maps path is missing from commit ${commit}: ${relativePath}`)
			return blobs.get(object)!
		},
	}
}

function checkoutCommit(root: string): string {
	let commit: string
	try {
		commit = execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim().toLowerCase()
	} catch (error) {
		throw new Error(`Unable to resolve the Pinball Memory Maps checkout commit at ${root}: ${error}`)
	}
	if (!COMMIT_ID.test(commit)) throw new Error(`Unexpected Pinball Memory Maps commit: ${commit}`)
	return commit
}

function writeExternalFile(bytes: Buffer, outputRoot: string, relativePath: string) {
	const destination = join(outputRoot, ...relativePath.split('/'))
	mkdirSync(dirname(destination), { recursive: true })
	writeFileSync(destination, bytes)
}

/**
 * Load and validate the optional read-only Pinball Memory Maps checkout.
 *
 * The caller owns the generated output root. This function copies exact upstream
 * map bytes there, but it never writes to the checkout or the canonical defs tree.
 * Every file is read from the pinned commit's Git objects, never the working
 * tree: a Windows checkout with `core.autocrlf=true` holds CRLF copies, and a
 * locally edited one holds bytes that commit never contained.
 */
export function loadPinballMemoryMaps(
	rootValue: string | undefined,
	expectedCommit: string | undefined,
	catalogDriverIds: ReadonlySet<string>,
	generatedOutputRoot: string,
): MemoryMapsBuildData | null {
	if (!rootValue?.trim()) return null
	const root = resolve(rootValue)
	if (!existsSync(root) || !lstatSync(root).isDirectory()) {
		throw new Error(`PINBALL_MEMORY_MAPS_ROOT is not a directory: ${root}`)
	}

	const commit = checkoutCommit(root)
	if (expectedCommit) {
		const normalizedExpected = expectedCommit.trim().toLowerCase()
		if (!COMMIT_ID.test(normalizedExpected)) throw new Error(`PINBALL_MEMORY_MAPS_COMMIT must be a full Git commit: ${expectedCommit}`)
		if (commit !== normalizedExpected) {
			throw new Error(`Pinball Memory Maps checkout is ${commit}, expected ${normalizedExpected}.`)
		}
	}
	const tree = readPinnedTree(root, commit)

	// Both texts are required: a checkout missing either is not one this build
	// knows how to license, so it fails before any map is mirrored.
	const licenseFiles = PINBALL_MEMORY_MAPS_LICENSE_FILES.map(({ license, sourcePath }) => {
		const outputPath = `memory-maps/${sourcePath}`
		return {
			bytes: tree.read(sourcePath),
			outputPath,
			file: {
				license,
				sourcePath,
				sourceUrl: `${PINBALL_MEMORY_MAPS_REPOSITORY}/blob/${commit}/${sourcePath}`,
				dataUrl: `data/${outputPath}`,
			},
		}
	})
	for (const { bytes, outputPath } of licenseFiles) writeExternalFile(bytes, generatedOutputRoot, outputPath)

	const index = requirePlainObject(parseJson(tree.read('index.json'), 'index.json'), 'Pinball Memory Maps index.json')
	const mapCache = new Map<string, MemoryMapSummary>()
	const copiedPlatforms = new Set<string>()
	const byDriver = new Map<string, MemoryMapSummary>()
	const unmatchedRoms: string[] = []

	for (const [driver, sourcePathValue] of Object.entries(index).sort(([a], [b]) => a.localeCompare(b))) {
		if (driver.startsWith('_')) continue
		if (!DRIVER_ID.test(driver)) throw new Error(`Invalid driver ID in Pinball Memory Maps index: ${driver}`)
		if (typeof sourcePathValue !== 'string' || !sourcePathValue.endsWith('.map.json')) {
			throw new Error(`Invalid map path for ${driver}: ${String(sourcePathValue)}`)
		}
		const sourcePath = sourcePathValue.replace(/\\/g, '/')
		let summary = mapCache.get(sourcePath)
		if (!summary) {
			const mapBytes = tree.read(sourcePath, 'maps/')
			const document = requirePlainObject(parseJson(mapBytes, sourcePath), sourcePath) as MemoryMapDocument
			const metadata = requirePlainObject(document._metadata, `${sourcePath}._metadata`)
			const platform = metadata.platform
			if (typeof platform !== 'string' || !PLATFORM_ID.test(platform)) throw new Error(`${sourcePath} has an invalid _metadata.platform.`)
			if (metadata.license !== MAP_LICENSE) {
				throw new Error(`${sourcePath} does not declare the ODbL v1.0 in _metadata.license: ${String(metadata.license)}`)
			}
			const platformSourcePath = `platforms/${platform}.json`
			const platformBytes = tree.read(platformSourcePath, 'platforms/')
			if (!copiedPlatforms.has(platformSourcePath)) {
				writeExternalFile(platformBytes, generatedOutputRoot, `memory-maps/${platformSourcePath}`)
				copiedPlatforms.add(platformSourcePath)
			}
			const romsValue = metadata.roms
			if (!Array.isArray(romsValue) || !romsValue.length || romsValue.some(rom => typeof rom !== 'string' || !DRIVER_ID.test(rom))) {
				throw new Error(`${sourcePath} has an invalid _metadata.roms array.`)
			}
			const roms = [...new Set(romsValue as string[])]
			if (roms.length !== romsValue.length) throw new Error(`${sourcePath} has duplicate _metadata.roms entries.`)
			const fileFormat = typeof document._fileformat === 'number' ? document._fileformat : null
			const version = typeof metadata.version === 'number' ? metadata.version : null
			const sections = Object.keys(document).filter(key => !key.startsWith('_')).sort()
			const outputPath = `memory-maps/${sourcePath}`
			summary = {
				sourcePath,
				sourceUrl: `${PINBALL_MEMORY_MAPS_REPOSITORY}/blob/${commit}/${sourcePath}`,
				dataUrl: `data/${outputPath}`,
				platform,
				platformSourceUrl: `${PINBALL_MEMORY_MAPS_REPOSITORY}/blob/${commit}/${platformSourcePath}`,
				platformDataUrl: `data/memory-maps/${platformSourcePath}`,
				fileFormat,
				version,
				roms,
				sections,
			}
			writeExternalFile(mapBytes, generatedOutputRoot, outputPath)
			mapCache.set(sourcePath, summary)
		}
		if (!summary.roms.includes(driver)) {
			throw new Error(`${sourcePath} does not list indexed driver ${driver} in _metadata.roms.`)
		}
		if (catalogDriverIds.has(driver)) byDriver.set(driver, summary)
		else unmatchedRoms.push(driver)
	}

	return {
		source: {
			repository: PINBALL_MEMORY_MAPS_REPOSITORY,
			commit,
			license: PINBALL_MEMORY_MAPS_LICENSE,
			contentsLicense: PINBALL_MEMORY_MAPS_CONTENTS_LICENSE,
			licenseFiles: licenseFiles.map(({ file }) => file),
			attribution: PINBALL_MEMORY_MAPS_ATTRIBUTION,
		},
		maps: [...mapCache.values()].sort((a, b) => a.sourcePath.localeCompare(b.sourcePath)),
		byDriver,
		unmatchedRoms: unmatchedRoms.sort(),
	}
}
