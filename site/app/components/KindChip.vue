<script setup lang="ts">
const props = defineProps<{ kind: string, count?: number }>()

const color = computed(() => kindColor(props.kind))
</script>

<template>
	<span
		class="inline-flex items-center gap-1.5 rounded-md border px-1.5 py-0.5 text-[11px] font-medium whitespace-nowrap"
		:style="{
			color,
			borderColor: `color-mix(in srgb, ${color} 26%, transparent)`,
			background: `color-mix(in srgb, ${color} 9%, transparent)`,
		}"
	>
		<span class="size-1.5 rounded-[2px]" :style="{ background: color }" />
		{{ kindLabel(kind) }}
		<span v-if="count !== undefined" class="num opacity-70">{{ count }}</span>
	</span>
</template>
