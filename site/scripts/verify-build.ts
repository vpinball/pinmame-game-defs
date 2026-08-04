/**
 * Post-generate guard.
 *
 * Nitro is configured with `failOnError: false` so one malformed definition
 * cannot block a whole deploy — but a silently missing page is worse than a
 * loud failure, so every expected route is checked here and reported by name.
 */
import { existsSync, readFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const projectRoot = resolve(fileURLToPath(import.meta.url), '../..')
const outRoot = join(projectRoot, '.output', 'public')

if (!existsSync(outRoot)) {
	console.error('[verify] .output/public not found — run `npm run generate` first.')
	process.exit(1)
}

const readIndex = <T>(name: string): T =>
	JSON.parse(readFileSync(join(projectRoot, 'data', name), 'utf8'))

const machines = readIndex<{ rows: [string, ...unknown[]][] }>('machines.json')
const platforms = readIndex<{ slug: string }[]>('platforms.json')
const families = readIndex<{ slug: string }[]>('families.json')

const expected = [
	'',
	'machines',
	'roms',
	'platforms',
	'coverage',
	'guide',
	'schema',
	...machines.rows.map(row => `machines/${row[0]}`),
	...platforms.map(platform => `platforms/${platform.slug}`),
	...families.map(family => `families/${family.slug}`),
]

const missing = expected.filter(route => !existsSync(join(outRoot, route, 'index.html')))

// The client-only indexes must survive too, or search and the ROM table break.
for (const asset of [
	'data/drivers.json',
	'data/search.json',
	'data/index.json',
	'data/platforms.json',
	'favicon.svg',
	'og.png',
	'sitemap.xml',
	'robots.txt',
	'llms.txt',
	'.nojekyll',
]) {
	if (!existsSync(join(outRoot, asset))) missing.push(asset)
}

if (missing.length) {
	console.error(`[verify] ${missing.length} of ${expected.length} routes/assets are missing from the build:`)
	for (const route of missing.slice(0, 40)) console.error(`  · /${route}`)
	if (missing.length > 40) console.error(`  … and ${missing.length - 40} more`)
	console.error('[verify] Run `npx nuxt dev` and open one of them to see the render error.')
	process.exit(1)
}

console.log(`[verify] ${expected.length} routes present, static assets intact.`)
