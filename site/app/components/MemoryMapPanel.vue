<script setup lang="ts">
import type { PinballMemoryMaps } from '~/types/defs'

/**
 * Pinball memory maps from the external `pinball-memory-maps` project.
 *
 * This is the one block on a machine page that is **not** this repository's own
 * work. It is checked out during the build, copied to a generated asset, and
 * shown here because an author debugging a ROM wants it — but it is neither
 * evidence for the definition above it nor part of the machine's coverage, and
 * it is under a different licence.
 *
 * So it is deliberately framed as borrowed: a dashed rule rather than the solid
 * hairline every canonical panel uses, an explicit "external" label rather than
 * a colour cue alone, and the upstream commit stated in the header so a reader
 * can tell exactly which revision of someone else's data they are looking at.
 */
const props = defineProps<{ data: PinballMemoryMaps }>()

const config = useRuntimeConfig()

/* -- upstream links ------------------------------------------------------- */

/** `https://github.com/owner/repo` or a bare `owner/repo` both resolve. */
const repoUrl = computed(() => {
	const repository = props.data.source.repository.trim().replace(/\.git$/, '').replace(/\/+$/, '')
	if (/^https?:\/\//i.test(repository)) return repository
	if (/^[\w.-]+\/[\w.-]+$/.test(repository)) return `https://github.com/${repository}`
	return null
})

/** Display form: the host adds nothing once the link is there. */
const repoLabel = computed(() => {
	const repository = props.data.source.repository.trim().replace(/\.git$/, '').replace(/\/+$/, '')
	const match = /^https?:\/\/[^/]+\/(.+)$/i.exec(repository)
	return match ? match[1]! : repository
})

const commit = computed(() => props.data.source.commit ?? '')
const shortCommit = computed(() => commit.value.slice(0, 7))

const isGitHub = computed(() => !!repoUrl.value && /^https?:\/\/(?:[^/]*\.)?github\.com\//i.test(`${repoUrl.value}/`))

const commitUrl = computed(() =>
	isGitHub.value && commit.value ? `${repoUrl.value}/commit/${commit.value}` : null)

/**
 * The licence text at the same pinned commit. The build also mirrors a copy next
 * to the generated maps, but its path is the generator's to choose — this one is
 * derivable from the contract alone and can never drift out of step with it.
 */
const licenseUrl = computed(() =>
	isGitHub.value && commit.value ? `${repoUrl.value}/blob/${commit.value}/LICENSE` : null)

/**
 * The generated copy. The generator owns this string, so accept whatever form it
 * emits: an absolute URL passes through, a site-root path picks up the deploy
 * base (GitHub project pages serve from `/<repo>/`), and a path that already
 * carries that base is left alone rather than gaining a second one.
 */
const dataHref = (url: string) => {
	if (/^(?:[a-z][\w+.-]*:|\/\/)/i.test(url)) return url
	const base = (config.app.baseURL || '/').replace(/\/+$/, '')
	const path = url.replace(/^\/+/, '')
	if (base && `/${path}`.startsWith(`${base}/`)) return `/${path}`
	return `${base}/${path}`
}

/* -- long chip lists ------------------------------------------------------ */

/**
 * A map can name enough ROMs or sections to overwhelm the page. Truncate those
 * lists, but keep the rest one click away — the section names are the most
 * useful thing here for deciding whether a map is worth opening.
 */
const LIMIT = 12

const expanded = ref(new Set<string>())
const toggle = (key: string) => {
	const next = new Set(expanded.value)
	next.has(key) ? next.delete(key) : next.add(key)
	expanded.value = next
}
const isExpanded = (key: string) => expanded.value.has(key)
const shown = (key: string, list: string[]) => (isExpanded(key) ? list : list.slice(0, LIMIT))

const mapKey = (index: number, field: string) => `${index}:${field}`

/** ROM sets named upstream that do not belong to the machine on this page. */
const additionalRoms = (roms: string[], matchedDrivers: string[]) => {
	const matched = new Set(matchedDrivers)
	return roms.filter(rom => !matched.has(rom))
}

/** `maps/wpc/mm.map.json` -> `mm.map.json`, for a heading that fits. */
const fileName = (path: string) => path.split('/').filter(Boolean).at(-1) ?? path
</script>

<template>
	<section
		class="rounded-panel border border-dashed border-line bg-panel"
		aria-labelledby="memory-maps-heading"
	>
		<header class="border-b border-dashed border-line px-4 py-3 sm:px-5">
			<div class="flex flex-wrap items-center gap-x-3 gap-y-2">
				<h2 id="memory-maps-heading" class="flex items-center gap-2 text-sm font-semibold">
					<Icon name="lucide:memory-stick" class="size-4 text-ink-3" />
					Pinball memory maps
				</h2>
				<span class="inline-flex items-center gap-1.5 rounded-full border border-line bg-raised px-2 py-0.5 text-[11px] text-ink-3">
					<Icon name="lucide:external-link" class="size-3" />
					External source
				</span>
				<a
					v-if="licenseUrl"
					:href="licenseUrl"
					target="_blank"
					rel="noopener noreferrer license"
					class="num rounded border border-line px-1.5 py-0.5 text-[10px] text-ink-3 transition-colors hover:border-amber/40 hover:text-amber"
					title="Licence of the upstream data, not of this repository"
				>{{ data.source.license }}</a>
				<span
					v-else
					class="num rounded border border-line px-1.5 py-0.5 text-[10px] text-ink-3"
					title="Licence of the upstream data, not of this repository"
				>{{ data.source.license }}</span>
				<span class="num ml-auto text-[11px] text-ink-4">{{ data.maps.length }} map{{ data.maps.length === 1 ? '' : 's' }}</span>
			</div>

			<p class="mt-2 max-w-3xl text-[13px] leading-relaxed text-ink-3">
				RAM layouts published by an independent project and mirrored here at a pinned commit. They are
				<strong class="font-medium text-ink-2">not part of this machine’s definition</strong>: nothing below was used as
				evidence for the definition, and none of it counts towards coverage. Check claims against the upstream
				project.
			</p>

			<dl class="mt-3 flex flex-wrap items-baseline gap-x-5 gap-y-1.5 text-[11px]">
				<div class="flex min-w-0 items-baseline gap-1.5">
					<dt class="text-ink-4">
						Upstream
					</dt>
					<dd class="min-w-0">
						<a
							v-if="repoUrl"
							:href="repoUrl"
							target="_blank"
							rel="noopener noreferrer"
							class="num inline-flex max-w-full items-center gap-1 break-all text-ink-2 transition-colors hover:text-amber"
						>
							{{ repoLabel }}
							<Icon name="lucide:arrow-up-right" class="size-3 shrink-0" />
						</a>
						<span v-else class="num break-all text-ink-2">{{ repoLabel }}</span>
					</dd>
				</div>

				<div v-if="commit" class="flex items-baseline gap-1.5">
					<dt class="text-ink-4">
						Commit
					</dt>
					<dd>
						<a
							v-if="commitUrl"
							:href="commitUrl"
							target="_blank"
							rel="noopener noreferrer"
							class="num inline-flex items-center gap-1 text-ink-2 transition-colors hover:text-amber"
							:title="commit"
						>
							{{ shortCommit }}
							<Icon name="lucide:arrow-up-right" class="size-3 shrink-0" />
						</a>
						<span v-else class="num text-ink-2" :title="commit">{{ shortCommit }}</span>
					</dd>
				</div>
			</dl>

			<!-- The upstream licence requires this notice to be shown wherever its
			     content is used, so it is rendered verbatim rather than reworded. -->
			<p v-if="data.source.attribution" class="mt-2.5 flex items-start gap-2 text-[11px] leading-relaxed text-ink-4">
				<Icon name="lucide:scale" class="mt-0.5 size-3 shrink-0" />
				<span>{{ data.source.attribution }}</span>
			</p>
		</header>

		<article
			v-for="(map, index) in data.maps"
			:key="map.sourcePath"
			class="border-b border-line-soft px-4 py-4 last:border-0 sm:px-5"
		>
			<div class="flex flex-wrap items-baseline gap-x-3 gap-y-1.5">
				<h3 class="num text-[13px] font-semibold break-all text-ink">
					{{ fileName(map.sourcePath) }}
				</h3>
				<span
					class="num rounded border border-line bg-raised px-1.5 py-0.5 text-[11px] text-ink-2"
					title="Memory platform, as the upstream map names it"
				>{{ map.platform }}</span>
				<span v-if="map.version != null" class="num text-[11px] text-ink-4" title="Upstream map revision">v{{ map.version }}</span>
				<span
					v-if="map.fileFormat != null"
					class="num text-[11px] text-ink-4"
					title="Upstream file-format revision"
				>format {{ map.fileFormat }}</span>
			</div>

			<p class="num mt-1 text-[11px] break-all text-ink-4">
				{{ map.sourcePath }}
			</p>

			<dl class="mt-3 space-y-2.5">
				<!-- Lead with the useful claim: which ROM sets on this machine the map
				     applies to. Do not repeat the full upstream list when it is identical. -->
				<div v-if="map.matchedDrivers.length" class="flex flex-col gap-1.5 sm:flex-row sm:gap-3">
					<dt class="eyebrow shrink-0 pt-1 sm:w-28" title="ROM sets on this machine that are covered by the upstream map">
						Applies to ROMs
					</dt>
					<dd class="flex min-w-0 flex-wrap items-center gap-1.5">
						<span
							v-for="driver in shown(mapKey(index, 'drivers'), map.matchedDrivers)"
							:key="driver"
							class="num rounded-md border border-amber/25 bg-amber/8 px-1.5 py-0.5 text-[11px] text-amber"
						>{{ driver }}</span>
						<button
							v-if="map.matchedDrivers.length > LIMIT"
							type="button"
							class="rounded-md border border-line px-1.5 py-0.5 text-[11px] text-ink-3 transition-colors hover:border-amber/40 hover:text-amber"
							:aria-expanded="isExpanded(mapKey(index, 'drivers'))"
							@click="toggle(mapKey(index, 'drivers'))"
						>
							{{ isExpanded(mapKey(index, 'drivers')) ? 'Show fewer' : `+${map.matchedDrivers.length - LIMIT} more` }}
						</button>
					</dd>
				</div>

				<!-- A shared map can cover a wider driver family. Only surface those extra
				     upstream ROM IDs when there is an actual distinction to explain. -->
				<div v-if="additionalRoms(map.roms, map.matchedDrivers).length" class="flex flex-col gap-1.5 sm:flex-row sm:gap-3">
					<dt class="eyebrow shrink-0 pt-1 sm:w-28" title="Other ROM sets named by the upstream map that are not on this machine page">
						Also covers
					</dt>
					<dd class="flex min-w-0 flex-wrap items-center gap-1.5">
						<span
							v-for="rom in shown(mapKey(index, 'additional-roms'), additionalRoms(map.roms, map.matchedDrivers))"
							:key="rom"
							class="num rounded-md border border-line bg-raised px-1.5 py-0.5 text-[11px] text-ink-2"
						>{{ rom }}</span>
						<button
							v-if="additionalRoms(map.roms, map.matchedDrivers).length > LIMIT"
							type="button"
							class="rounded-md border border-line px-1.5 py-0.5 text-[11px] text-ink-3 transition-colors hover:border-amber/40 hover:text-amber"
							:aria-expanded="isExpanded(mapKey(index, 'additional-roms'))"
							@click="toggle(mapKey(index, 'additional-roms'))"
						>
							{{ isExpanded(mapKey(index, 'additional-roms')) ? 'Show fewer' : `+${additionalRoms(map.roms, map.matchedDrivers).length - LIMIT} more` }}
						</button>
					</dd>
				</div>

				<div v-if="map.sections.length" class="flex flex-col gap-1.5 sm:flex-row sm:gap-3">
					<dt class="eyebrow shrink-0 pt-1 sm:w-28">
						Sections
					</dt>
					<dd class="flex min-w-0 flex-wrap items-center gap-1.5">
						<span
							v-for="section in shown(mapKey(index, 'sections'), map.sections)"
							:key="section"
							class="num rounded-md border border-line-soft bg-raised/60 px-1.5 py-0.5 text-[11px] text-ink-3"
						>{{ section }}</span>
						<button
							v-if="map.sections.length > LIMIT"
							type="button"
							class="rounded-md border border-line px-1.5 py-0.5 text-[11px] text-ink-3 transition-colors hover:border-amber/40 hover:text-amber"
							:aria-expanded="isExpanded(mapKey(index, 'sections'))"
							@click="toggle(mapKey(index, 'sections'))"
						>
							{{ isExpanded(mapKey(index, 'sections')) ? 'Show fewer' : `+${map.sections.length - LIMIT} more` }}
						</button>
					</dd>
				</div>
			</dl>

			<!--
				Four links to two artefacts, so each one names both which file it is
				and which copy: repeating "Generated JSON" twice would leave a reader
				tabbing through the links unable to tell the map from the platform.
				The icon carries the copy (mirrored / upstream), the text the artefact.
			-->
			<div class="mt-3 flex flex-wrap items-center gap-1.5">
				<a
					:href="dataHref(map.dataUrl)"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex max-w-full items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px] text-ink-2 transition-colors hover:border-amber/40 hover:text-amber"
					title="Exact upstream map bytes, mirrored by this build"
				>
					<Icon name="lucide:file-json-2" class="size-3 shrink-0 opacity-70" />
					<span>Map JSON</span>
				</a>
				<a
					:href="map.sourceUrl"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex max-w-full items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px] text-ink-2 transition-colors hover:border-amber/40 hover:text-amber"
					:title="`${map.sourcePath} at ${shortCommit || 'the pinned commit'}`"
				>
					<Icon name="lucide:file-code-2" class="size-3 shrink-0 opacity-70" />
					<span>Map source</span>
				</a>

				<!-- Groups the pairs where all four fit on one line. Below that they
				     wrap anyway, and a rule stranded at the end of a row reads as a
				     stray tick rather than a divider. -->
				<span class="mx-0.5 hidden h-4 w-px shrink-0 bg-line sm:block" aria-hidden="true" />

				<a
					:href="dataHref(map.platformDataUrl)"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex max-w-full items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px] text-ink-2 transition-colors hover:border-amber/40 hover:text-amber"
					:title="`Mirrored copy of the ${map.platform} memory layout this map is read against`"
				>
					<Icon name="lucide:file-json-2" class="size-3 shrink-0 opacity-70" />
					<span>Platform JSON</span>
				</a>
				<a
					:href="map.platformSourceUrl"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex max-w-full items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px] text-ink-2 transition-colors hover:border-amber/40 hover:text-amber"
					:title="`The ${map.platform} platform definition at ${shortCommit || 'the pinned commit'}`"
				>
					<Icon name="lucide:file-code-2" class="size-3 shrink-0 opacity-70" />
					<span>Platform source</span>
				</a>
			</div>

			<!--
				Visible rather than a `title`: a map is a list of offsets, and without
				the platform file naming the regions those offsets sit in, it cannot be
				read at all. That is not a detail to hide behind a hover.
			-->
			<p class="mt-2 text-[11px] leading-relaxed text-ink-3">
				<span class="num">{{ map.platform }}</span> defines the RAM layout this map’s offsets are read against — the
				map is not interpretable without it.
			</p>
		</article>
	</section>
</template>
