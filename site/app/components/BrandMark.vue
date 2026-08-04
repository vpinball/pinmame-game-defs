<script setup lang="ts">
import marks from '../../data/icons.json'

/**
 * The manufacturer's mark for a platform or a maker, in a tile.
 *
 * The tile used to hold the platform's short id as text, which is what pushed
 * `DATAEAST` past its own border — and `STERN-MPU200` would have been hopeless
 * at any size that stayed readable. Since the tile always sits beside the name
 * it stands for, nothing is lost by dropping the text: where a mark exists it
 * carries the identity, and where none does a neutral glyph keeps the row
 * aligned without pretending to say more.
 */
const props = withDefaults(defineProps<{
	platform?: string | null
	manufacturer?: string | null
	/** `plain` drops the tile — for a mark sitting inline with running text. */
	variant?: 'tile' | 'plain'
	size?: 'sm' | 'md' | 'lg'
}>(), { variant: 'tile', size: 'md' })

const brand = computed(() =>
	brandForPlatform(props.platform) ?? brandForManufacturer(props.manufacturer))

const svg = computed(() => (brand.value ? (marks as Record<string, string>)[brand.value] : null))

/** Falls back by kind: a platform is a board, a manufacturer is a company. */
const fallbackIcon = computed(() => (props.platform ? 'lucide:cpu' : 'lucide:factory'))

const TILE = { sm: 'size-8 rounded-md', md: 'size-11 rounded-lg', lg: 'size-14 rounded-xl' }

/*
 * The marks are drawn inset inside their own 48x48 box, so at the size a
 * Lucide glyph wants they read noticeably smaller than one. Giving them a
 * larger box puts the ink at a matching weight.
 */
const MARK = { sm: 'size-6', md: 'size-8', lg: 'size-10' }
const GLYPH = { sm: 'size-4', md: 'size-5', lg: 'size-7' }
</script>

<template>
	<span
		v-if="variant === 'tile'"
		class="grid shrink-0 place-items-center border border-line bg-raised"
		:class="[TILE[size], svg ? 'text-ink-2' : 'text-ink-4']"
	>
		<!-- eslint-disable-next-line vue/no-v-html -- build-time output of scripts/prepare-icons.ts -->
		<span v-if="svg" :class="MARK[size]" class="block [&>svg]:size-full" v-html="svg" />
		<Icon v-else :name="fallbackIcon" :class="GLYPH[size]" />
	</span>

	<!-- eslint-disable-next-line vue/no-v-html -- build-time output of scripts/prepare-icons.ts -->
	<span
		v-else-if="svg"
		class="inline-block shrink-0 [&>svg]:size-full"
		:class="MARK[size]"
		v-html="svg"
	/>
</template>
