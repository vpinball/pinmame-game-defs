import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import tailwindcss from '@tailwindcss/vite'

/**
 * Every machine gets a prerendered page, including catalog stubs — a deep link
 * from an authoring tool must always land somewhere that explains the state of
 * the definition.
 */
// The production domain serves from `/`, while GitHub project-page forks serve
// from `/<repo>/`. Normalizing explicit routes to that base keeps them identical
// to routes discovered by the crawler and avoids duplicate prerenders.
const base = (process.env.NUXT_APP_BASE_URL || '/').replace(/\/*$/, '/')
const route = (path: string) => `${base}${path.replace(/^\//, '')}`

function machineRoutes(): string[] {
	try {
		const index = JSON.parse(
			readFileSync(fileURLToPath(new URL('./data/machines.json', import.meta.url)), 'utf8'),
		) as { rows: [string, ...unknown[]][] }
		return index.rows.map(row => `/machines/${row[0]}`)
	}
	catch {
		console.warn('[nuxt] data/machines.json missing — run `npm run data` first.')
		return []
	}
}

function familyRoutes(): string[] {
	try {
		const families = JSON.parse(
			readFileSync(fileURLToPath(new URL('./data/families.json', import.meta.url)), 'utf8'),
		) as { slug: string }[]
		return families.map(f => `/families/${f.slug}`)
	}
	catch {
		return []
	}
}

function platformRoutes(): string[] {
	try {
		const platforms = JSON.parse(
			readFileSync(fileURLToPath(new URL('./data/platforms.json', import.meta.url)), 'utf8'),
		) as { slug: string }[]
		return platforms.map(p => `/platforms/${p.slug}`)
	}
	catch {
		return []
	}
}

export default defineNuxtConfig({
	compatibilityDate: '2025-07-15',
	future: { compatibilityVersion: 4 },
	devtools: { enabled: false },

	modules: ['@nuxt/icon'],

	css: ['~/assets/css/main.css'],

	vite: {
		plugins: [tailwindcss()],
	},

	// Icons are bundled from the local @iconify-json/lucide package and inlined
	// into the client build, so the deployed site never calls out to an API.
	icon: {
		mode: 'svg',
		serverBundle: false,
		clientBundle: { scan: true, includeCustomCollections: true },
	},

	runtimeConfig: {
		public: {
			// Source branch used by edit/create links. This must be runtime config:
			// app config is compiled for the browser and cannot read process.env.
			repoBranch: process.env.NUXT_PUBLIC_REPO_BRANCH || 'master',

			// Absolute public root, including any subpath. Canonical URLs, Open
			// Graph tags and the sitemap all derive from it, so it must match what
			// the site is actually served from.
			siteUrl: process.env.NUXT_PUBLIC_SITE_URL || 'https://games.visualpinball.org',

			/*
			 * Matomo. Clear `NUXT_PUBLIC_MATOMO_SITE_ID` to switch analytics off
			 * entirely — a fork deploying its own copy should, or its traffic
			 * lands in someone else's dashboard. Explicit `https` rather than the
			 * protocol-relative `//count.vpdb.io/`: the site is only ever served
			 * over TLS, and this leaves no downgrade path.
			 */
			matomo: {
				url: process.env.NUXT_PUBLIC_MATOMO_URL ?? 'https://count.vpdb.io/',
				siteId: process.env.NUXT_PUBLIC_MATOMO_SITE_ID ?? '4',
			},
		},
	},

	app: {
		// The production custom domain serves from `/`; forks can override this
		// with NUXT_APP_BASE_URL=/pinmame-game-defs/ for GitHub project pages.
		baseURL: base,
		head: {
			htmlAttrs: { lang: 'en' },
			meta: [
				{ name: 'viewport', content: 'width=device-width, initial-scale=1' },
				{ name: 'theme-color', content: '#0a0b0d' },
			],
			link: [
				{ rel: 'icon', type: 'image/svg+xml', href: `${base}favicon.svg` },
			],
		},
	},

	nitro: {
		preset: 'github_pages',
		prerender: {
			crawlLinks: true,
			failOnError: false,
			routes: ['/', '/machines', '/roms', '/platforms', '/coverage', '/guide', '/schema', ...machineRoutes(), ...platformRoutes(), ...familyRoutes()].map(route),
		},
	},

	experimental: {
		payloadExtraction: true,

		/*
		 * NuxtLink prefetches a route's chunk as soon as the link scrolls into
		 * view. Here every machine chunk embeds that machine's full definition —
		 * 180-260 kB each — so a page showing sixty cards was pulling ~12 MB of
		 * JSON nobody asked for. Prefetch on hover/focus instead: navigation
		 * still feels instant, and idle browsing costs nothing.
		 */
		defaults: {
			nuxtLink: {
				prefetch: true,
				prefetchOn: { visibility: false, interaction: true },
			},
		},
	},

	typescript: {
		strict: true,
	},

})
