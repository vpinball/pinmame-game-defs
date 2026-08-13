<script setup lang="ts">
import type { CoverageStatus } from '~/types/defs'

const props = withDefaults(defineProps<{
	score: number
	status: CoverageStatus
	compact?: boolean
}>(), { compact: false })

const color = computed(() => STATUS_META[props.status].color)
</script>

<template>
	<div
		role="progressbar"
		:aria-label="`Machine-definition completion: ${score}%`"
		:aria-valuemin="0"
		:aria-valuemax="100"
		:aria-valuenow="score"
		:aria-valuetext="`${score}% complete; coverage status ${STATUS_META[status].label}`"
		:title="`${score}% of the fixed author-readiness requirements are satisfied. Coverage status remains ${STATUS_META[status].label}.`"
	>
		<div class="flex items-center justify-between gap-3" :class="compact ? 'text-[10px]' : 'text-xs'">
			<span class="text-ink-4">Completion</span>
			<span class="num font-medium" :style="{ color }">{{ score }}%</span>
		</div>
		<div aria-hidden="true" class="mt-1 overflow-hidden rounded-full bg-line" :class="compact ? 'h-1' : 'h-1.5'">
			<div class="h-full rounded-full" :style="{ width: `${score}%`, background: color }" />
		</div>
	</div>
</template>
