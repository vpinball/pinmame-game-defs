<script setup lang="ts">
import type { Source } from '~/types/defs'

defineProps<{ sources: Source[] }>()

// One card can carry several excerpts — a manual is normally cited for its switch table, its
// lamp table and each schematic sheet separately — so track which are open individually.
const open = ref(new Set<string>())
const toggle = (key: string) => {
	const next = new Set(open.value)
	next.has(key) ? next.delete(key) : next.add(key)
	open.value = next
}

// Kind vocabulary lives in app/utils/sources.ts so the conflict panel names
// a disagreeing source exactly as this list does.
const meta = sourceMeta

const sourceLabel = (source: Source) => source.id ?? source.uri
const hasLongLocator = (source: Source) => (source.locator?.length ?? 0) > 240
</script>

<template>
	<ul class="grid gap-3 md:grid-cols-2">
		<li v-for="(source, index) in sources" :key="source.id ?? index" class="panel flex min-w-0 flex-col p-4 [overflow-wrap:anywhere]">
			<div class="flex items-start gap-3">
				<span class="mt-0.5 grid size-7 shrink-0 place-items-center rounded-md border border-line bg-raised text-ink-2">
					<Icon :name="meta(source.kind).icon" class="size-3.5" />
				</span>
				<div class="min-w-0 flex-1">
					<div class="flex items-baseline gap-2">
						<h4 class="text-sm font-semibold">
							{{ meta(source.kind).label }}
						</h4>
						<span v-if="source.license && source.license !== 'NOASSERTION'" class="num rounded border border-line px-1 text-[10px] text-ink-3">{{ source.license }}</span>
					</div>
					<p v-if="sourceLabel(source)" class="num mt-0.5 text-[11px] break-all text-ink-4">
						{{ sourceLabel(source) }}
					</p>
				</div>
			</div>

			<details v-if="source.locator && hasLongLocator(source)" class="group mt-3 rounded-md border border-line-soft bg-raised/30">
				<summary class="flex cursor-pointer list-none items-center gap-2 px-2.5 py-2 text-[11px] text-ink-3 transition-colors hover:text-amber [&::-webkit-details-marker]:hidden">
					<Icon name="lucide:map-pinned" class="size-3 shrink-0 opacity-70" />
					<span class="flex-1">Source locations</span>
					<Icon name="lucide:chevron-down" class="size-3 shrink-0 opacity-70 transition-transform group-open:rotate-180" />
				</summary>
				<p class="border-t border-line-soft px-2.5 py-3 text-xs leading-relaxed text-ink-2">
					{{ source.locator }}
				</p>
			</details>

			<p v-else-if="source.locator" class="mt-3 text-xs leading-relaxed text-ink-2">
				{{ source.locator }}
			</p>

			<!-- deep links: the exact file at the pinned revision, or the exact
			     page of the manual, rather than the project's front door -->
			<div v-if="sourceRefs(source).length || source.uri || locatorHints(source).length" class="mt-3 flex flex-wrap gap-1.5">
				<a
					v-for="ref in sourceRefs(source)"
					:key="ref.href"
					:href="ref.href"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex max-w-full items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px] text-ink-2 transition-colors hover:border-amber/40 hover:text-amber"
				>
					<Icon
						:name="ref.kind === 'file' ? 'lucide:file-code-2' : ref.kind === 'page' ? 'lucide:file-text' : 'lucide:external-link'"
						class="size-3 shrink-0 opacity-70"
					/>
					<span class="num truncate">{{ ref.label }}</span>
				</a>
				<span
					v-if="!sourceRefs(source).length && source.uri"
					class="num inline-flex max-w-full items-center gap-1.5 rounded-md border border-line-soft px-1.5 py-1 text-[11px] break-all text-ink-4"
					title="Identifier, not a resolvable location"
				>{{ source.uri }}</span>
				<span
					v-for="hint in locatorHints(source)"
					:key="hint"
					class="num inline-flex items-center rounded-md border border-line-soft px-1.5 py-1 text-[11px] text-ink-4"
					title="Referenced lines — this source cannot be linked at line level"
				>{{ hint }}</span>
			</div>

			<!-- What the source actually said. A hash is only an identity; the excerpt is the
			     evidence, so it is readable in place rather than being a file path to go and find. -->
			<div v-if="source.excerpts?.length" class="mt-3 flex flex-col gap-2">
				<div v-for="excerpt in source.excerpts" :key="excerpt.id ?? excerpt.path" class="rounded-md border border-line-soft bg-raised/40">
					<button
						type="button"
						class="flex w-full items-center gap-2 px-2.5 py-2 text-left text-[11px] text-ink-3 transition-colors hover:text-amber"
						@click="toggle(`${source.id}:${excerpt.path}`)"
					>
						<Icon
							:name="open.has(`${source.id}:${excerpt.path}`) ? 'lucide:chevron-down' : 'lucide:chevron-right'"
							class="size-3 shrink-0 opacity-70"
						/>
						<Icon :name="excerpt.imageUrl ? 'lucide:image' : 'lucide:quote'" class="size-3 shrink-0 opacity-70" />
						<span class="min-w-0 flex-1 truncate">{{ excerpt.locator ?? 'Excerpt' }}</span>
						<span v-if="excerpt.reviewed" class="shrink-0 rounded border border-line px-1 text-[10px] text-ink-4" title="A curator checked this transcription against the rendered page">checked</span>
					</button>

					<div v-if="open.has(`${source.id}:${excerpt.path}`)" class="border-t border-line-soft px-2.5 py-3">
						<a
							v-if="excerpt.imageUrl"
							:href="excerpt.imageUrl"
							target="_blank"
							rel="noopener noreferrer"
							class="mb-3 block overflow-hidden rounded border border-line bg-white"
							:title="excerpt.imageDerivation ?? 'Rendered from the retained document'"
						>
							<img :src="excerpt.imageUrl" :alt="excerpt.locator ?? 'Excerpt'" loading="lazy" class="w-full">
						</a>

						<div class="excerpt text-xs leading-relaxed text-ink-2" v-html="excerpt.html" />

						<p class="num mt-2 text-[10px] text-ink-4">
							{{ excerpt.path }}<template v-if="excerpt.method"> · transcribed {{ excerpt.method }}</template><template v-if="excerpt.transcribedBy"> · {{ excerpt.transcribedBy }}</template>
						</p>
					</div>
				</div>
			</div>

			<dl class="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-ink-4">
				<div v-if="source.attribution" class="flex gap-1.5">
					<dt class="text-ink-4">
						by
					</dt>
					<dd class="text-ink-3">
						{{ source.attribution }}
					</dd>
				</div>
				<div v-if="source.revision" class="flex gap-1.5">
					<dt>rev</dt>
					<dd class="num text-ink-3">
						{{ shortHash(source.revision) }}
					</dd>
				</div>
				<div v-if="source.sha256" class="flex gap-1.5">
					<dt>sha256</dt>
					<dd class="num text-ink-3" :title="source.sha256">
						{{ shortHash(source.sha256) }}…
					</dd>
				</div>
			</dl>
		</li>
	</ul>
</template>
