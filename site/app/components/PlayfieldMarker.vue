<script setup lang="ts">
import type { PlayfieldCluster } from '~/utils/playfield'

/**
 * One marker on the playfield.
 *
 * Its own component so the map can render it twice: once in the dimmable base
 * layer and once in the highlight layer on top. That keeps the base layer free
 * of any dependency on what is focused, which is what stops a hover from
 * re-rendering every marker on the board.
 */
defineProps<{
	cluster: PlayfieldCluster
	/** Draws the selection ring — only ever set in the highlight layer. */
	ring?: boolean
}>()
</script>

<template>
	<g>
		<!-- an insert lights an area, not a point -->
		<circle
			v-if="cluster.hasEmitter"
			:cx="cluster.cx"
			:cy="cluster.cy"
			r="30"
			:fill="cluster.color"
			opacity="0.16"
		/>

		<template v-if="cluster.members.length === 1">
			<!-- shape carries the role, colour carries the device kind -->
			<circle
				v-if="cluster.role === 'emitter'"
				:cx="cluster.cx"
				:cy="cluster.cy"
				r="13"
				:fill="cluster.color"
			/>
			<circle
				v-else-if="cluster.role === 'sensor'"
				:cx="cluster.cx"
				:cy="cluster.cy"
				r="12"
				fill="var(--color-pf-center)"
				:stroke="cluster.color"
				stroke-width="6"
			/>
			<rect
				v-else
				:x="cluster.cx - 13"
				:y="cluster.cy - 13"
				width="26"
				height="26"
				rx="4"
				:fill="cluster.color"
				:transform="`rotate(45 ${cluster.cx} ${cluster.cy})`"
			/>
		</template>

		<!-- a stack: several devices in one spot, carrying their count -->
		<template v-else>
			<circle
				:cx="cluster.cx"
				:cy="cluster.cy"
				r="21"
				fill="var(--color-pf-center)"
				:stroke="cluster.color"
				stroke-width="5"
			/>
			<text
				:x="cluster.cx"
				:y="cluster.cy"
				text-anchor="middle"
				dominant-baseline="central"
				font-size="24"
				font-weight="600"
				:fill="cluster.color"
			>{{ cluster.members.length }}</text>
		</template>

		<circle
			v-if="ring"
			:cx="cluster.cx"
			:cy="cluster.cy"
			:r="cluster.members.length > 1 ? 36 : 30"
			fill="none"
			stroke="var(--color-amber)"
			stroke-width="5"
		/>

		<title>{{ cluster.members.map(m => `${m.device.binding.device} ${m.device.label}`).join(' · ') }}</title>
	</g>
</template>
