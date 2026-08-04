declare global {
	interface Window {
		__pmgQuery?: string
		__pmgPath?: string
	}
}

/**
 * The query string a page should restore its state from.
 *
 * `useRoute().query` cannot be trusted on first load: these pages are
 * prerendered, and during hydration the router briefly rewrites the location to
 * the bare prerendered path, so anything reading the query in `setup` or
 * `onMounted` can catch that window and see nothing. An inline head script
 * snapshots it before any framework code runs.
 *
 * That snapshot describes only the page the visitor landed on. It is returned
 * once, and only to that page — an in-site navigation such as
 * `/machines?mfr=Stern` from a machine page reads the live location instead,
 * which the router has already settled by the time the destination mounts.
 */
export function useInitialQuery(): URLSearchParams {
	if (!import.meta.client) return new URLSearchParams()

	const isLandingPage = window.__pmgPath !== undefined
		&& window.__pmgPath.replace(/\/$/, '') === window.location.pathname.replace(/\/$/, '')

	if (isLandingPage && window.__pmgQuery !== undefined) {
		const snapshot = window.__pmgQuery
		delete window.__pmgQuery
		delete window.__pmgPath
		return new URLSearchParams(snapshot)
	}

	return new URLSearchParams(window.location.search)
}
