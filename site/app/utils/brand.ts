/**
 * Which manufacturer's mark stands for a platform or a maker name.
 *
 * Only a small set of marks exists, so most things resolve to nothing and fall
 * back to a neutral glyph — that is the expected case, not a failure.
 */

/**
 * Platform ids are matched explicitly rather than by substring: `s11`, `s7` and
 * `wpc` are Williams hardware without the word "Williams" anywhere in them, and
 * `de` would match half the alphabet.
 */
const PLATFORM_BRANDS: Record<string, string> = {
	'pinmame.wpc': 'williams',
	'pinmame.wpc-alpha': 'williams',
	'pinmame.s11': 'williams',
	'pinmame.s7': 'williams',
	'pinmame.system11': 'williams',
	'pinmame.bally': 'bally',
	'pinmame.bally-by35': 'bally',
	'pinmame.dataeast': 'data-east',
	'pinmame.de': 'data-east',
	'pinmame.sega': 'sega',
	'pinmame.capcom': 'capcom',
	'pinmame.sam': 'stern-pinball',
	'pinmame.stern': 'stern-pinball',
	// Stern Electronics, not today's Stern Pinball — a deliberate brand lineage
	// rather than the same company, so the modern mark is an anachronism here,
	// but an honest one: the catalog files both under "Stern".
	'pinmame.stern-mpu200': 'stern-pinball',
	'pinmame.gts1': 'gottlieb',
	'pinmame.gts3': 'gottlieb',
	'pinmame.gts80': 'gottlieb',
	'pinmame.system80': 'gottlieb',
	// "Sega/Stern Whitestar" in the catalog, because Stern kept building the
	// board after buying the division. Sega's mark by choice: it is the board's
	// origin, and the Stern-era games on it are the minority here.
	'pinmame.whitestar': 'sega',
}

/**
 * Maker names are messy — "Bally Midway", "Williams / Jess M. Askey",
 * "Sega Pinball" — so the first prefix that matches wins, and the order settles
 * the joint ventures: a Bally/Midway title reads as Bally, matching how the
 * catalog and IPDB list it.
 */
const MANUFACTURER_BRANDS: [prefix: string, brand: string][] = [
	['williams', 'williams'],
	['bally', 'bally'],
	['midway', 'midway'],
	['data east', 'data-east'],
	['sega', 'sega'],
	['capcom', 'capcom'],
	['stern', 'stern-pinball'],
	['gottlieb', 'gottlieb'],
	// Premier Technology bought Gottlieb and kept shipping under the Gottlieb
	// name for another decade; the catalog credits the company, the playfields
	// say Gottlieb.
	['premier', 'gottlieb'],
	['taito', 'taito'],
	['zaccaria', 'zaccaria'],
	['ltd', 'ltd'],
	// Also catches "Inder/Spinball (Spain)", which is Inder's own late run.
	['inder', 'inder'],
]

export const brandForPlatform = (platform: string | null | undefined): string | null =>
	(platform && PLATFORM_BRANDS[platform]) || null

export function brandForManufacturer(manufacturer: string | null | undefined): string | null {
	if (!manufacturer) return null
	const name = manufacturer.trim().toLowerCase()
	return MANUFACTURER_BRANDS.find(([prefix]) => name.startsWith(prefix))?.[1] ?? null
}
