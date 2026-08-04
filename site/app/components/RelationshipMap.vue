<script setup lang="ts">
import type { Device, Relationship } from '~/types/defs'

const props = defineProps<{
	relationships: Relationship[]
	deviceById: Map<string, Device>
}>()

const KIND_META: Record<string, { label: string, hint: string, color: string }> = {
	pulse: { label: 'pulse', hint: 'Closing the switch fires the coil directly in hardware — do not wait for the ROM.', color: 'var(--color-k-coil)' },
	direct: { label: 'direct', hint: 'The input drives the device continuously while held.', color: 'var(--color-k-switch)' },
	relay_gated: { label: 'relay gated', hint: 'The connection only conducts while a relay is energised.', color: 'var(--color-k-relay)' },
	normally_closed_series: { label: 'NC series', hint: 'Wired in series through a normally-closed contact.', color: 'var(--color-k-dip)' },
	inverted: { label: 'inverted', hint: 'The destination follows the inverse of the source.', color: 'var(--color-k-rgb)' },
}

const rows = computed(() => props.relationships.map(rel => ({
	...rel,
	meta: KIND_META[rel.kind] ?? { label: rel.kind, hint: '', color: 'var(--color-ink-3)' },
	from: props.deviceById.get(rel.source) ?? null,
	to: props.deviceById.get(rel.destination) ?? null,
})))
</script>

<template>
	<div class="panel divide-y divide-line-soft">
		<div
			v-for="rel in rows"
			:key="rel.id"
			class="flex flex-wrap items-center gap-x-3 gap-y-2 px-4 py-3"
		>
			<a
				:href="`#device-${rel.source}`"
				class="inline-flex min-w-0 items-center gap-2 rounded-md border border-line bg-raised px-2 py-1 text-xs transition-colors hover:border-amber/40"
			>
				<span v-if="rel.from" class="num text-ink-3">{{ rel.from.binding.device }}</span>
				<span class="truncate">{{ rel.from?.label ?? rel.source }}</span>
			</a>

			<span class="inline-flex items-center gap-1.5" :style="{ color: rel.meta.color }" :title="rel.meta.hint">
				<svg width="46" height="10" viewBox="0 0 46 10" fill="none" class="shrink-0">
					<path d="M0 5h36" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.6" />
					<path d="M35 1l6 4-6 4z" fill="currentColor" />
				</svg>
				<span class="text-[11px] font-medium">{{ rel.meta.label }}</span>
			</span>

			<a
				:href="`#device-${rel.destination}`"
				class="inline-flex min-w-0 items-center gap-2 rounded-md border border-line bg-raised px-2 py-1 text-xs transition-colors hover:border-amber/40"
			>
				<span v-if="rel.to" class="num text-ink-3">{{ rel.to.binding.device }}</span>
				<span class="truncate">{{ rel.to?.label ?? rel.destination }}</span>
			</a>
		</div>
	</div>
</template>
