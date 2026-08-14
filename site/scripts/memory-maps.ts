import { execFileSync } from 'node:child_process'
import { copyFileSync, existsSync, lstatSync, mkdirSync, readFileSync, realpathSync } from 'node:fs'
import { dirname, join, resolve, sep } from 'node:path'

export const PINBALL_MEMORY_MAPS_REPOSITORY = 'https://github.com/tomlogic/pinball-memory-maps'
export const PINBALL_MEMORY_MAPS_LICENSE = 'LGPL-3.0-only'
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

export type MemoryMapsSource = {
	repository: string
	commit: string
	license: string
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
		roms?: unknown
	}
	[key: string]: unknown
}

const DRIVER_ID = /^[a-z0-9_]+$/
const PLATFORM_ID = /^[A-Za-z0-9][A-Za-z0-9._-]*$/
const COMMIT_ID = /^[0-9a-f]{40}$/

function readJson(path: string): unknown {
	return JSON.parse(readFileSync(path, 'utf8'))
}

function requirePlainObject(value: unknown, label: string): Record<string, unknown> {
	if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${label} must be a JSON object.`)
	return value as Record<string, unknown>
}

function resolveFileWithin(root: string, relativePath: string, expectedPrefix?: string): string {
	const portable = relativePath.replace(/\\/g, '/')
	const parts = portable.split('/')
	if (!portable || portable.startsWith('/') || parts.some(part => !part || part === '.' || part === '..')) {
		throw new Error(`Unsafe Pinball Memory Maps path: ${relativePath}`)
	}
	if (expectedPrefix && !portable.startsWith(expectedPrefix)) {
		throw new Error(`Pinball Memory Maps path must start with ${expectedPrefix}: ${relativePath}`)
	}
	const path = resolve(root, ...parts)
	const rootPrefix = realpathSync(root) + sep
	if (!existsSync(path) || !realpathSync(path).startsWith(rootPrefix)) {
		throw new Error(`Pinball Memory Maps path escapes or is missing from its checkout: ${relativePath}`)
	}
	if (!lstatSync(path).isFile()) throw new Error(`Pinball Memory Maps path is not a regular file: ${relativePath}`)
	return path
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

function copyExternalFile(source: string, outputRoot: string, relativePath: string) {
	const destination = join(outputRoot, ...relativePath.split('/'))
	mkdirSync(dirname(destination), { recursive: true })
	copyFileSync(source, destination)
}

/**
 * Load and validate the optional read-only Pinball Memory Maps checkout.
 *
 * The caller owns the generated output root. This function copies exact upstream
 * map bytes there, but it never writes to the checkout or the canonical defs tree.
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

	const indexPath = resolveFileWithin(root, 'index.json')
	const index = requirePlainObject(readJson(indexPath), 'Pinball Memory Maps index.json')
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
			const absolutePath = resolveFileWithin(root, sourcePath, 'maps/')
			const document = requirePlainObject(readJson(absolutePath), sourcePath) as MemoryMapDocument
			const metadata = requirePlainObject(document._metadata, `${sourcePath}._metadata`)
			const platform = metadata.platform
			if (typeof platform !== 'string' || !PLATFORM_ID.test(platform)) throw new Error(`${sourcePath} has an invalid _metadata.platform.`)
			const platformSourcePath = `platforms/${platform}.json`
			const platformPath = resolveFileWithin(root, platformSourcePath, 'platforms/')
			if (!copiedPlatforms.has(platformSourcePath)) {
				copyExternalFile(platformPath, generatedOutputRoot, `memory-maps/${platformSourcePath}`)
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
			copyExternalFile(absolutePath, generatedOutputRoot, outputPath)
			mapCache.set(sourcePath, summary)
		}
		if (!summary.roms.includes(driver)) {
			throw new Error(`${sourcePath} does not list indexed driver ${driver} in _metadata.roms.`)
		}
		if (catalogDriverIds.has(driver)) byDriver.set(driver, summary)
		else unmatchedRoms.push(driver)
	}

	const licensePath = resolveFileWithin(root, 'LICENSE')
	copyExternalFile(licensePath, generatedOutputRoot, 'memory-maps/LICENSE')

	return {
		source: {
			repository: PINBALL_MEMORY_MAPS_REPOSITORY,
			commit,
			license: PINBALL_MEMORY_MAPS_LICENSE,
			attribution: PINBALL_MEMORY_MAPS_ATTRIBUTION,
		},
		maps: [...mapCache.values()].sort((a, b) => a.sourcePath.localeCompare(b.sourcePath)),
		byDriver,
		unmatchedRoms: unmatchedRoms.sort(),
	}
}
