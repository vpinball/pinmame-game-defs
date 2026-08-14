/**
 * One place that decides a page's title, description, canonical URL and social
 * card, so the four cannot drift apart.
 *
 * `siteUrl` carries any deployment subpath and `route.path` does not, so a
 * canonical is simply the two concatenated. Static hosting serves
 * `<route>/index.html`, so canonicals end in a slash and the sitemap is
 * generated to match exactly.
 */
export function useSeo(input: {
	/** Page title without the site suffix; omit on the home page. */
	title?: MaybeRefOrGetter<string | undefined>
	description: MaybeRefOrGetter<string>
	/** Public path or absolute URL for a page-specific social card. */
	image?: MaybeRefOrGetter<string | undefined>
	imageAlt?: MaybeRefOrGetter<string | undefined>
	/** Keeps a page reachable and crawlable but out of the index. */
	noindex?: MaybeRefOrGetter<boolean>
}) {
	const route = useRoute()
	const siteUrl = useRuntimeConfig().public.siteUrl.replace(/\/+$/, '')

	const canonical = computed(() => {
		const path = route.path === '/' ? '/' : `${route.path.replace(/\/+$/, '')}/`
		return `${siteUrl}${path}`
	})

	const title = computed(() => toValue(input.title))
	const description = computed(() => toValue(input.description))
	const socialTitle = computed(() =>
		title.value ? `${title.value} · PinMAME Machine Reference` : 'PinMAME Machine Reference')
	const socialImage = computed(() => {
		const image = toValue(input.image)?.trim()
		if (!image) return `${siteUrl}/og.png`
		if (/^https?:\/\//i.test(image)) return image
		return `${siteUrl}/${image.replace(/^\/+/, '')}`
	})
	const socialImageAlt = computed(() => toValue(input.imageAlt) ?? 'PinMAME Machine Reference — every switch, lamp and coil PinMAME can talk to')

	useHead({
		title,
		link: [{ rel: 'canonical', href: canonical }],
	})

	useSeoMeta({
		description,
		ogTitle: socialTitle,
		ogDescription: description,
		ogUrl: canonical,
		ogType: 'website',
		ogSiteName: 'PinMAME Machine Reference',
		ogImage: socialImage,
		ogImageWidth: 1200,
		ogImageHeight: 630,
		ogImageAlt: socialImageAlt,
		twitterCard: 'summary_large_image',
		twitterTitle: socialTitle,
		twitterDescription: description,
		twitterImage: socialImage,
		twitterImageAlt: socialImageAlt,
		// `follow` matters: a stub still links to its ROM sets and its machine's
		// siblings, and those links should keep carrying weight.
		robots: () => (toValue(input.noindex) ? 'noindex, follow' : 'index, follow'),
	})

	return { canonical }
}
