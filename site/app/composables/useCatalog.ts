import type { DriverEntry, MachineDetail, MachineSummary, PlatformEntry, SearchRow, SiteData } from '~/types/defs'
import siteJson from '../../data/site.json'
import platformsJson from '../../data/platforms.json'
import detailSlugs from '../../data/detail-slugs.json'

/** Repository-wide counters and roll-ups. Small enough to ship everywhere. */
export const useSite = () => siteJson as unknown as SiteData

export const usePlatforms = () => platformsJson as unknown as PlatformEntry[]

/**
 * The browse index. Imported lazily so only the pages that list machines pay
 * for it — machine detail pages never load it.
 */
export async function loadMachineIndex(): Promise<MachineSummary[]> {
	const index = await import('../../data/machines.json')
	return decodeMachineRows(index.default as any)
}

/** Big client-only documents served as static assets, fetched on demand. */
function assetUrl(path: string) {
	const base = useRuntimeConfig().app.baseURL || '/'
	return `${base.replace(/\/$/, '')}/${path.replace(/^\//, '')}`
}

const withDetail = new Set(detailSlugs as string[])

export const hasMachineDetail = (slug: string) => withDetail.has(slug)

/**
 * One machine's full definition.
 *
 * Fetched as a static asset rather than imported as a module: a dynamic import
 * per machine would create 100+ JS chunks, and Nuxt's build manifest emits a
 * `<link rel="prefetch">` for every one of them on every page — several
 * megabytes of definitions nobody asked for. As a plain asset it is fetched
 * only when a page actually needs it, and it is the same document the public
 * `/data` endpoints serve.
 */
export async function loadMachineDetail(slug: string): Promise<MachineDetail | null> {
	if (!withDetail.has(slug)) return null

	// The prerenderer does not serve `public/` to `$fetch`, so on the server the
	// same file is read straight off disk. This branch is stripped from the
	// client bundle.
	if (import.meta.server) {
		const { readFile } = await import('node:fs/promises')
		const { join } = await import('node:path')
		return JSON.parse(await readFile(join(process.cwd(), 'public', 'data', 'machines', `${slug}.json`), 'utf8'))
	}

	return await $fetch<MachineDetail>(assetUrl(`data/machines/${slug}.json`))
}

let driversPromise: Promise<DriverEntry[]> | null = null
export function loadDrivers(): Promise<DriverEntry[]> {
	driversPromise ??= $fetch<DriverEntry[]>(assetUrl('data/drivers.json'))
	return driversPromise
}

let searchPromise: Promise<SearchRow[]> | null = null
export function loadSearchIndex(): Promise<SearchRow[]> {
	searchPromise ??= $fetch<SearchRow[]>(assetUrl('data/search.json'))
	return searchPromise
}
