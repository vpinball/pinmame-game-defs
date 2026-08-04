import type { Source } from '~/types/defs'

export interface SourceRef {
	href: string
	label: string
	kind: 'file' | 'page' | 'external'
}

const GITHUB_REPO = /^https?:\/\/github\.com\/[^/]+\/[^/]+$/

/** `src/wpc/sam.c`, `src/libpinmame/libpinmame.cpp` — a path, not prose. */
const PATH_TOKEN = /(?:^|[\s(;,`])((?:[\w.@-]+\/)+[\w.@-]+\.[a-z0-9]{1,6})/gi

/** `lines 35, 81-165` / `line 240` immediately after a path. */
const LINE_HINT = /^\s*(?:on\s+)?lines?\s+(\d+)(?:\s*[-–]\s*(\d+))?/i

/** `PDF pages 42-50`, `page 119` */
const PAGE_HINT = /(?:PDF\s+)?pages?\s+(\d+)(?:\s*[-–]\s*(\d+))?/gi

/**
 * Turns a source record into links that actually land on the evidence.
 *
 * A bare repository URL is close to useless to a reader checking a claim, but
 * the locator already names the file — and often the lines or PDF pages — so a
 * pinned revision plus that path gives a permalink straight to the code, and a
 * page number turns a 300-page manual into one anchor.
 */
export function sourceRefs(source: Source): SourceRef[] {
	const uri = source.uri
	// Some records identify an artefact rather than a location, e.g.
	// `external:pinmame-game-code/…`. Those are not links.
	if (!uri || !/^https?:\/\//i.test(uri)) return []
	const locator = source.locator ?? ''
	const refs: SourceRef[] = []

	if (GITHUB_REPO.test(uri) && source.revision) {
		const seen = new Set<string>()
		for (const match of locator.matchAll(PATH_TOKEN)) {
			const path = match[1]!
			if (seen.has(path)) continue
			seen.add(path)
			const after = locator.slice(match.index! + match[0].length)
			const lines = LINE_HINT.exec(after)
			const anchor = lines ? `#L${lines[1]}${lines[2] ? `-L${lines[2]}` : ''}` : ''
			refs.push({
				href: `${uri}/blob/${source.revision}/${path}${anchor}`,
				label: lines ? `${path}:${lines[1]}` : path,
				kind: 'file',
			})
		}
		if (refs.length) return refs
		// No path in the locator — the pinned tree is still better than HEAD.
		return [{ href: `${uri}/tree/${source.revision}`, label: source.revision.slice(0, 12), kind: 'external' }]
	}

	if (/\.pdf($|[?#])/i.test(uri)) {
		const seen = new Set<string>()
		for (const match of locator.matchAll(PAGE_HINT)) {
			const page = match[1]!
			if (seen.has(page)) continue
			seen.add(page)
			refs.push({
				href: `${uri}#page=${page}`,
				label: match[2] ? `pages ${page}–${match[2]}` : `page ${page}`,
				kind: 'page',
			})
			if (refs.length >= 4) break
		}
		if (refs.length) return refs
	}

	return [{ href: uri, label: hostLabel(uri), kind: 'external' }]
}

function hostLabel(uri: string) {
	try {
		return new URL(uri).hostname.replace(/^www\./, '')
	}
	catch {
		return uri
	}
}

/** Line numbers a source names but that no URL can address (VPX scripts, PDFs). */
export function locatorHints(source: Source): string[] {
	const locator = source.locator ?? ''
	const hints: string[] = []
	// "lines 35, 81-165, and 200-453" — everything up to the next clause break.
	const lines = /lines?\s+([^:;]*\d)/i.exec(locator)
	if (lines) hints.push(`lines ${lines[1]!.trim()}`)
	return hints
}
