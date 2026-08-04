<script setup lang="ts">
import type { CoverageStatus } from '~/types/defs'

const props = withDefaults(defineProps<{
	status: CoverageStatus
	size?: 'sm' | 'md'
	dotOnly?: boolean
}>(), { size: 'md', dotOnly: false })

const meta = computed(() => STATUS_META[props.status])
</script>

<template>
	<span
		v-if="dotOnly"
		class="inline-block size-2 rounded-full"
		:style="{ background: meta.color, boxShadow: `0 0 8px -1px ${meta.color}` }"
		:title="meta.label"
	/>
	<span
		v-else
		class="inline-flex items-center gap-1.5 rounded-full border font-medium whitespace-nowrap"
		:class="size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-2.5 py-1 text-xs'"
		:style="{
			color: meta.color,
			borderColor: `color-mix(in srgb, ${meta.color} 30%, transparent)`,
			background: `color-mix(in srgb, ${meta.color} 10%, transparent)`,
		}"
		:title="meta.blurb"
	>
		<span class="size-1.5 rounded-full" :style="{ background: meta.color }" />
		{{ size === 'sm' ? meta.short : meta.label }}
	</span>
</template>
