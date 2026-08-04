<script setup lang="ts">
import type { Source } from '~/types/defs'

defineProps<{ sources: Source[] }>()

const SOURCE_META: Record<string, { label: string, icon: string, blurb: string }> = {
	manual: { label: 'Operator manual', icon: 'lucide:book-open', blurb: 'Authoritative for wiring, connectors, switch construction and assembly geometry.' },
	service_bulletin: { label: 'Service bulletin', icon: 'lucide:file-warning', blurb: 'Factory correction to the manual.' },
	service_diagnostic: { label: 'Service diagnostic', icon: 'lucide:activity', blurb: 'Names read out of the machine’s own test menus.' },
	vpx_script: { label: 'VPX script', icon: 'lucide:file-code-2', blurb: 'Known-working table script — ground truth for controller addresses and mechanism causality.' },
	vpx_table: { label: 'VPX table', icon: 'lucide:table-2', blurb: 'The table file the script came from, for physical-object evidence.' },
	pinmame_core: { label: 'PinMAME source', icon: 'lucide:cpu', blurb: 'Authoritative for emulator routing, display layout and output typing.' },
	pinmame_catalog: { label: 'PinMAME catalog', icon: 'lucide:list', blurb: 'Driver identity as reported by the pinned library build.' },
	pinmame_sim: { label: 'PinMAME simulator', icon: 'lucide:play', blurb: 'Names from PinMAME’s built-in table simulator.' },
	rom_static_analysis: { label: 'ROM analysis', icon: 'lucide:binary', blurb: 'Facts recovered from the game ROM itself.' },
	runtime_scenario: { label: 'Runtime run', icon: 'lucide:terminal', blurb: 'Observed by actually booting the ROM in a harness.' },
	human_review: { label: 'Human review', icon: 'lucide:user-check', blurb: 'A curator’s reviewed judgement.' },
	legacy_json: { label: 'Legacy definition', icon: 'lucide:archive', blurb: 'Imported from the previous VPE game definitions.' },
	vpe_csharp: { label: 'VPE C# definition', icon: 'lucide:file-type-2', blurb: 'Imported from the original C# game classes.' },
}

// Controller profiles cite sources without a `kind`, so fall back gracefully.
const meta = (kind: string | undefined) =>
	(kind ? SOURCE_META[kind] : undefined) ?? { label: kind ? titleCase(kind) : 'Reference', icon: 'lucide:file', blurb: '' }
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
					<p class="num mt-0.5 text-[11px] break-all text-ink-4">
						{{ source.id ?? source.locator }}
					</p>
				</div>
			</div>

			<p v-if="source.locator" class="mt-3 text-xs leading-relaxed text-ink-2">
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
