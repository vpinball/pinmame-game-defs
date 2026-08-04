<script setup lang="ts">
const props = defineProps<{ code?: string | null }>()
const parts = computed(() => wireParts(props.code))
</script>

<template>
	<span v-if="parts.length" class="inline-flex items-center gap-1.5" :title="`Wire ${code}`">
		<span class="flex overflow-hidden rounded-[3px] ring-1 ring-black/40 dark:ring-white/15">
			<span
				v-for="part in parts"
				:key="part.code"
				class="h-3 w-2"
				:style="{ background: part.color }"
			/>
		</span>
		<span class="num text-[11px] text-ink-3">{{ code }}</span>
	</span>
</template>
