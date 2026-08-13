<script setup lang="ts">
import type { MachineSummary } from '~/types/defs'

const props = defineProps<{ machine: MachineSummary }>()

const stats = computed(() => [
	{ label: 'switches', value: props.machine.switches, kind: 'switch' },
	{ label: 'lamps', value: props.machine.lamps, kind: 'lamp' },
	{ label: 'coils', value: props.machine.coils, kind: 'coil' },
	{ label: 'mechs', value: props.machine.mechanisms, kind: 'motor' },
].filter(s => s.value > 0))
</script>

<template>
	<NuxtLink
		:to="`/machines/${machine.slug}`"
		class="panel group relative flex flex-col overflow-hidden p-4 transition-all hover:border-amber/35 hover:bg-raised"
	>
		<!-- status rail -->
		<span
			class="absolute inset-y-0 left-0 w-0.5"
			:style="{ background: STATUS_META[machine.status].color, opacity: machine.status === 'stub' ? 0.35 : 0.9 }"
		/>

		<div class="flex items-start justify-between gap-3">
			<div class="min-w-0">
				<h3 class="truncate text-[15px] leading-snug font-semibold transition-colors group-hover:text-amber">
					{{ machine.name }}
				</h3>
				<p class="mt-0.5 truncate text-xs text-ink-3">
					{{ machine.manufacturer }}<span v-if="machine.year"> · {{ machine.year }}</span>
				</p>
			</div>
			<StatusChip :status="machine.status" size="sm" />
		</div>

		<div v-if="machine.highlights.length" class="mt-3 flex flex-wrap gap-1.5">
			<span
				v-for="tag in machine.highlights"
				:key="tag"
				class="rounded border border-line bg-raised px-1.5 py-0.5 text-[10px] text-ink-3 capitalize"
			>{{ tag }}</span>
		</div>

		<CompletionMeter v-if="machine.status !== 'author_ready'" class="mt-3" :score="machine.completionScore" :status="machine.status" compact />

		<div class="mt-auto flex items-end justify-between gap-3 pt-4">
			<dl v-if="stats.length" class="flex gap-3">
				<div v-for="stat in stats" :key="stat.label">
					<dd class="num text-sm leading-none" :style="{ color: kindColor(stat.kind) }">
						{{ stat.value }}
					</dd>
					<dt class="mt-1 text-[10px] text-ink-4">
						{{ stat.label }}
					</dt>
				</div>
			</dl>
			<span v-else class="text-[11px] text-ink-4">Not yet described</span>

			<div class="flex items-center gap-2 text-[10px] text-ink-4">
				<span v-if="machine.platform" class="num rounded border border-line px-1.5 py-0.5">{{ platformShort(machine.platform) }}</span>
				<span class="num">{{ machine.drivers }} ROM{{ machine.drivers === 1 ? '' : 's' }}</span>
			</div>
		</div>
	</NuxtLink>
</template>
