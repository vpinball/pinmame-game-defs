<script setup lang="ts">
import type { CoverageStatus } from '~/types/defs'

const props = defineProps<{
	status: CoverageStatus
	score: number
	dimensions: Record<string, string>
	missing: string[]
}>()

/** Order matters: this is the order the validator walks the definition. */
const DIMENSION_ORDER = [
	'catalog_identity',
	'address_enumeration',
	'semantic_naming',
	'physical_wiring',
	'mechanisms',
	'variant_coverage',
	'recreation_knowledge',
]

const LEVEL: Record<string, { rank: number, color: string }> = {
	validated: { rank: 4, color: 'var(--color-ready)' },
	observed: { rank: 3, color: 'var(--color-k-switch)' },
	candidate: { rank: 2, color: 'var(--color-partial)' },
	conflicted: { rank: 1, color: 'var(--color-alert)' },
	unknown: { rank: 0, color: 'var(--color-ink-4)' },
}

const rows = computed(() =>
	DIMENSION_ORDER
		.filter(key => key in props.dimensions)
		.map(key => {
			const value = props.dimensions[key]!
			const level = LEVEL[value] ?? LEVEL.unknown!
			return { key, label: titleCase(key), value, ...level }
		}),
)

const meta = computed(() => STATUS_META[props.status])
</script>

<template>
	<div class="panel p-4 sm:p-5">
		<div class="flex items-start gap-3">
			<StatusChip :status="status" />
			<p class="text-xs leading-relaxed text-ink-3">
				{{ meta.blurb }}
			</p>
		</div>

		<CompletionMeter class="mt-4" :score="score" :status="status" />
		<p class="mt-2 text-[11px] leading-relaxed text-ink-4">
			Progress is derived from the fixed author-readiness requirements. It helps rank unfinished work, but only a 100% author-ready definition passes the publication gate.
		</p>

		<dl v-if="rows.length" class="mt-4 space-y-2">
			<div v-for="row in rows" :key="row.key" class="flex items-center gap-3">
				<dt class="w-40 shrink-0 truncate text-xs text-ink-2">
					{{ row.label }}
				</dt>
				<dd class="flex flex-1 items-center gap-2">
					<div class="flex flex-1 gap-1">
						<span
							v-for="step in 4"
							:key="step"
							class="h-1.5 flex-1 rounded-full"
							:style="{ background: step <= row.rank ? row.color : 'var(--color-line)' }"
						/>
					</div>
					<span class="w-20 shrink-0 text-right text-[11px]" :style="{ color: row.color }">{{ row.value }}</span>
				</dd>
			</div>
		</dl>

		<div v-if="missing.length" class="mt-4 rounded-lg border border-partial/25 bg-partial/6 p-3">
			<div class="eyebrow mb-2 !text-partial">
				Still missing · {{ missing.length }}
			</div>
			<div class="flex flex-wrap gap-1.5">
				<span
					v-for="item in missing"
					:key="item"
					class="rounded border border-partial/25 px-1.5 py-0.5 text-[11px] text-partial/90"
				>{{ titleCase(item) }}</span>
			</div>
		</div>
	</div>
</template>
