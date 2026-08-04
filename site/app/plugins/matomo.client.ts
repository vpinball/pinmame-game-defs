/**
 * Matomo, adapted for a prerendered single-page app.
 *
 * The stock snippet calls `trackPageView` once per document load. That is right
 * for a set of plain HTML pages, but this site hydrates into an SPA: after the
 * first paint every link is a client-side navigation, no document loads, and
 * Matomo would record one view per session no matter how much of the catalog
 * someone read. So the loader is kept and the page view is driven by the
 * router instead.
 *
 * Two details that matter here specifically:
 *
 *   - The URL is compared without its hash. `/schema` and `/guide` are long
 *     pages full of in-page anchors, and vue-router treats every anchor click
 *     as a navigation — counting those would inflate views several times over.
 *   - `enableLinkTracking` is re-armed after each view, because Matomo binds to
 *     the links present when it runs and the DOM has since been replaced.
 */
export default defineNuxtPlugin((nuxtApp) => {
	const { matomo, siteUrl } = useRuntimeConfig().public

	if (!matomo?.url || !matomo?.siteId) return

	/*
	 * Only the real deployment reports. `npm run generate` followed by a local
	 * preview is a genuine production build served over http — `import.meta.dev`
	 * would not catch it, and a week of someone's own testing is indistinguishable
	 * from traffic once it is in the dashboard. Matching the configured public
	 * origin is exact, and reuses the value canonical URLs and the sitemap
	 * already depend on, rather than inventing a second thing to keep in step.
	 */
	if (import.meta.dev || location.origin !== new URL(siteUrl).origin) return

	const base = matomo.url.replace(/\/*$/, '/')

	/*
	 * Resolved on every call, never captured. `_paq` starts life as a plain
	 * array of queued commands, and `matomo.js` *replaces* the global with a
	 * proxy that executes them once it loads. A held reference would still point
	 * at the original array, so everything pushed after the tracker arrived —
	 * which is every client-side page view — would land in a detached queue that
	 * nothing ever drains.
	 */
	const push = (...command: unknown[]) => {
		const queue = ((window as any)._paq ||= [])
		queue.push(command)
	}

	push('setTrackerUrl', `${base}matomo.php`)
	push('setSiteId', matomo.siteId)

	/** The address as a page view, deliberately excluding the in-page anchor. */
	const address = () => location.origin + location.pathname + location.search

	let previous = ''
	let previousTitle = ''

	function track() {
		const url = address()
		if (url === previous) return
		// Matomo's own referrer is the previous document; within a session the
		// useful one is the page actually navigated from.
		if (previous) push('setReferrerUrl', previous)
		push('setCustomUrl', url)
		push('setDocumentTitle', document.title)
		push('trackPageView')
		push('enableLinkTracking')
		previous = url
		previousTitle = document.title
	}

	// The landing page is prerendered, so its title is already correct in the
	// served HTML and there is nothing to wait for.
	track()

	/*
	 * `page:finish` fires when the incoming page component is mounted, but the
	 * title is not in the document yet — Unhead applies the head patch on a
	 * later frame, and how many frames later varies with whether the route's
	 * chunk was already loaded. Recording immediately attributes each view to
	 * the *previous* page's title, which a stub collector confirmed; waiting a
	 * fixed frame or two only makes it intermittent.
	 *
	 * So wait for the thing itself: the title changing. A page whose title
	 * genuinely matches the last one simply falls through after the cap, and is
	 * recorded with the right title anyway.
	 */
	function trackWhenTitled(framesLeft = 12) {
		if (document.title === previousTitle && framesLeft > 0) {
			requestAnimationFrame(() => trackWhenTitled(framesLeft - 1))
			return
		}
		track()
	}

	nuxtApp.hook('page:finish', () => nextTick(trackWhenTitled))

	const script = document.createElement('script')
	script.async = true
	script.src = `${base}matomo.js`
	document.head.appendChild(script)
})
