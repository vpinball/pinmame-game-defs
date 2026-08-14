<script setup lang="ts">
import type { CoverageStatus, MachineSummary } from '~/types/defs'

useSeo({
	title: 'Machines',
	description: 'Browse every physical machine PinMAME supports, filtered by coverage, manufacturer, controller platform and playfield hardware.',
})

const router = useRouter()
const site = useSite()

const { data: machines } = await useAsyncData('machine-index', loadMachineIndex, { default: () => [] as MachineSummary[] })

const query = ref('')
const status = ref<CoverageStatus | 'all'>('all')
const manufacturer = ref('all')
const platform = ref('all')
/**
 * External memory-map availability. Orthogonal to `status` on purpose: a stub
 * can have a map and an author-ready machine can lack one, so this is its own
 * axis rather than another coverage value.
 */
const MEMORY_MAP_FILTERS = ['all', 'available', 'unavailable'] as const
type MemoryMapFilter = typeof MEMORY_MAP_FILTERS[number]
const memoryMap = ref<MemoryMapFilter>('all')
const sort = ref<'completion' | 'year' | 'name' | 'size'>('completion')
const view = ref<'grid' | 'table'>('grid')
const limit = ref(60)
const tags = ref<string[]>([])

// Restore shared-link state, then start writing the URL back. Nothing is
// written before the arrival query has been applied, or a deep link would be
// overwritten by this page's own defaults.
const urlReady = ref(false)

onMounted(() => {
	const params = useInitialQuery()
	query.value = params.get('q') ?? ''
	status.value = (params.get('status') as CoverageStatus | null) ?? 'all'
	manufacturer.value = params.get('mfr') ?? 'all'
	platform.value = params.get('platform') ?? 'all'
	// Validated against the allowed set — an arbitrary `?memmap=` from a hand-typed
	// URL must not leave the control showing a value it cannot represent.
	const requestedMemoryMap = params.get('memmap')
	if (requestedMemoryMap && (MEMORY_MAP_FILTERS as readonly string[]).includes(requestedMemoryMap)) {
		memoryMap.value = requestedMemoryMap as MemoryMapFilter
	}
	const requestedSort = params.get('sort')
	if (requestedSort && ['completion', 'year', 'name', 'size'].includes(requestedSort)) sort.value = requestedSort as typeof sort.value
	tags.value = (params.get('tags') ?? '').split(',').filter(Boolean)
	urlReady.value = true
})

const toggleTag = (tag: string) => {
	tags.value = tags.value.includes(tag) ? tags.value.filter(t => t !== tag) : [...tags.value, tag]
}

/**
 * Keep the URL shareable. This writes history directly rather than going
 * through the router: filtering is not a navigation, and a router replace on
 * every keystroke fights the hydration-time route normalisation.
 */
watchEffect(() => {
	const next = new URLSearchParams()
	if (query.value) next.set('q', query.value)
	if (status.value !== 'all') next.set('status', status.value)
	if (manufacturer.value !== 'all') next.set('mfr', manufacturer.value)
	if (platform.value !== 'all') next.set('platform', platform.value)
	if (memoryMap.value !== 'all') next.set('memmap', memoryMap.value)
	if (sort.value !== 'completion') next.set('sort', sort.value)
	if (tags.value.length) next.set('tags', tags.value.join(','))
	if (!urlReady.value || !import.meta.client) return
	const search = next.toString()
	history.replaceState(history.state, '', search ? `?${search}` : window.location.pathname)
})

watch([query, status, manufacturer, platform, memoryMap, sort, tags], () => { limit.value = 60 })

const manufacturers = computed(() => site.manufacturers.filter(m => m.machines >= 3))
const platforms = computed(() => site.platforms.filter(p => p.machines > 0).sort((a, b) => b.machines - a.machines))

/** Everything except the hardware tags — the facet counts are derived from this. */
const preTagged = computed(() => {
	const needle = query.value.trim().toLowerCase()
	return machines.value.filter(m =>
		(status.value === 'all' || m.status === status.value)
		&& (manufacturer.value === 'all' || m.manufacturer === manufacturer.value)
		&& (platform.value === 'all' || m.platform === platform.value)
		&& (memoryMap.value === 'all' || (memoryMap.value === 'available' ? m.memoryMaps > 0 : m.memoryMaps === 0))
		&& (!needle || m.name.toLowerCase().includes(needle) || m.manufacturer.toLowerCase().includes(needle) || String(m.year ?? '').includes(needle)),
	)
})

/**
 * Hardware facets, counted against everything the other filters already allow,
 * so a chip's number is what selecting it would actually yield.
 */
const tagFacets = computed(() => {
	const counts = new Map<string, number>()
	for (const machine of preTagged.value) {
		for (const tag of machine.highlights) counts.set(tag, (counts.get(tag) ?? 0) + 1)
	}
	for (const tag of tags.value) counts.set(tag, counts.get(tag) ?? 0)
	return [...counts.entries()]
		.map(([tag, count]) => ({ tag, count, active: tags.value.includes(tag) }))
		.sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag))
})

const filtered = computed(() => {
	// Tags combine with AND: "drop target bank + diverter" means both present.
	const list = preTagged.value.filter(m => tags.value.every(tag => m.highlights.includes(tag)))
	const rank = { author_ready: 0, partial: 1, stub: 2 }
	return list.sort((a, b) => {
		if (sort.value === 'name') return a.name.localeCompare(b.name)
		if (sort.value === 'size') return (b.switches + b.lamps + b.coils) - (a.switches + a.lamps + a.coils)
		if (sort.value === 'completion') return b.completionScore - a.completionScore || (b.year ?? 0) - (a.year ?? 0) || a.name.localeCompare(b.name)
		return rank[a.status] - rank[b.status] || (b.year ?? 0) - (a.year ?? 0) || a.name.localeCompare(b.name)
	})
})

const visible = computed(() => filtered.value.slice(0, limit.value))

const counts = computed(() => ({
	all: machines.value.length,
	author_ready: machines.value.filter(m => m.status === 'author_ready').length,
	partial: machines.value.filter(m => m.status === 'partial').length,
	stub: machines.value.filter(m => m.status === 'stub').length,
}))

/**
 * Counted against the whole catalog, exactly like the coverage counts above, so
 * the two controls report on the same basis. `available` doubles as the switch
 * that hides the control entirely: a build with no upstream checkout has zero
 * everywhere, and an always-empty filter is worse than no filter.
 */
const memoryMapCounts = computed(() => ({
	all: machines.value.length,
	available: machines.value.filter(m => m.memoryMaps > 0).length,
	unavailable: machines.value.filter(m => m.memoryMaps === 0).length,
}))

function reset() {
	query.value = ''
	status.value = 'all'
	manufacturer.value = 'all'
	platform.value = 'all'
	memoryMap.value = 'all'
	sort.value = 'completion'
	tags.value = []
}

const hasFilters = computed(() =>
	!!query.value || status.value !== 'all' || manufacturer.value !== 'all' || platform.value !== 'all'
	|| memoryMap.value !== 'all' || tags.value.length > 0)

const selectClass = 'rounded-lg border border-line bg-panel px-2.5 py-1.5 text-[13px] text-ink-2 focus:border-amber/50 focus:outline-none'
</script>

<template>
	<div class="mx-auto max-w-[100rem] px-4 py-8 sm:px-6">
		<header class="mb-6">
			<h1 class="text-2xl font-semibold tracking-tight">
				Machines
			</h1>
			<p class="mt-1.5 max-w-2xl text-sm text-ink-3">
				Every physical machine reachable from a PinMAME driver. Each one resolves the ROM sets that share its playfield,
				and carries whatever the catalog currently knows about it.
			</p>
		</header>

		<!-- filter bar -->
		<div class="panel sticky top-14 z-30 mb-5 p-3 backdrop-blur-xl">
			<div class="flex flex-wrap items-center gap-2">
				<div class="relative min-w-56 flex-1">
					<Icon name="lucide:search" class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-ink-4" />
					<input
						v-model="query"
						type="search"
						placeholder="Filter by name, manufacturer or year…"
						class="w-full rounded-lg border border-line bg-raised py-2 pr-3 pl-9 text-sm text-ink placeholder:text-ink-4 focus:border-amber/50 focus:outline-none"
					>
				</div>

				<div class="flex items-center gap-0.5 rounded-lg border border-line p-0.5">
					<button
						v-for="option in ([
							{ id: 'all', label: 'All' },
							{ id: 'author_ready', label: 'Ready' },
							{ id: 'partial', label: 'Partial' },
							{ id: 'stub', label: 'Stub' },
						] as const)"
						:key="option.id"
						type="button"
						class="flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-[13px] transition-colors"
						:class="status === option.id ? 'bg-raised text-ink' : 'text-ink-3 hover:text-ink'"
						@click="status = option.id"
					>
						<StatusChip v-if="option.id !== 'all'" :status="option.id" dot-only />
						{{ option.label }}
						<span class="num text-[10px] text-ink-4">{{ counts[option.id] }}</span>
					</button>
				</div>

				<select v-model="manufacturer" :class="selectClass">
					<option value="all">
						All manufacturers
					</option>
					<option v-for="m in manufacturers" :key="m.name" :value="m.name">
						{{ m.name }} ({{ m.machines }})
					</option>
				</select>

				<select v-model="platform" :class="selectClass">
					<option value="all">
						All platforms
					</option>
					<option v-for="p in platforms" :key="p.id" :value="p.id">
						{{ platformShort(p.id) }} ({{ p.machines }})
					</option>
				</select>

				<!--
					A select rather than a segmented group: the bar already carries four
					controls plus the view toggle, and a fourth button group wraps it onto
					a second row at laptop widths. Hidden when the build has no upstream
					checkout, where every option would read zero.
				-->
				<select
					v-if="memoryMapCounts.available"
					v-model="memoryMap"
					:class="selectClass"
					aria-label="Filter by external memory-map availability"
				>
					<option value="all">
						External memory map: any
					</option>
					<option value="available">
						External memory map: available ({{ memoryMapCounts.available }})
					</option>
					<option value="unavailable">
						External memory map: none ({{ memoryMapCounts.unavailable }})
					</option>
				</select>

				<select v-model="sort" :class="selectClass">
					<option value="completion">
						Sort: completion
					</option>
					<option value="year">
						Sort: coverage, newest
					</option>
					<option value="name">
						Sort: name
					</option>
					<option value="size">
						Sort: most I/O
					</option>
				</select>

				<div class="flex items-center gap-0.5 rounded-lg border border-line p-0.5">
					<button
						v-for="mode in (['grid', 'table'] as const)"
						:key="mode"
						type="button"
						class="grid size-7 place-items-center rounded-md transition-colors"
						:class="view === mode ? 'bg-raised text-ink' : 'text-ink-4 hover:text-ink'"
						:aria-label="`${mode} view`"
						@click="view = mode"
					>
						<Icon :name="mode === 'grid' ? 'lucide:layout-grid' : 'lucide:list'" class="size-3.5" />
					</button>
				</div>

				<button
					v-if="hasFilters"
					type="button"
					class="rounded-lg px-2 py-1.5 text-[13px] text-ink-3 hover:text-amber"
					@click="reset"
				>
					Clear
				</button>
			</div>

			<!-- hardware facets -->
			<div v-if="tagFacets.length" class="mt-2.5 flex flex-wrap items-center gap-1.5 border-t border-line-soft pt-2.5">
				<span class="eyebrow mr-1">Hardware</span>
				<button
					v-for="facet in tagFacets"
					:key="facet.tag"
					type="button"
					class="inline-flex items-center gap-1.5 rounded-md border px-2 py-1 text-[11px] capitalize transition-colors"
					:class="facet.active
						? 'border-amber/45 bg-amber/12 text-amber'
						: facet.count
							? 'border-line bg-raised text-ink-3 hover:border-amber/30 hover:text-ink'
							: 'border-line-soft text-ink-4'"
					:aria-pressed="facet.active"
					@click="toggleTag(facet.tag)"
				>
					<Icon v-if="facet.active" name="lucide:check" class="size-3" />
					{{ facet.tag }}
					<span class="num opacity-60">{{ facet.count }}</span>
				</button>
				<span v-if="tags.length > 1" class="ml-1 text-[11px] text-ink-4">all selected must be present</span>
			</div>
		</div>

		<p class="mb-4 text-xs text-ink-4">
			<span class="num text-ink-2">{{ num(filtered.length) }}</span> machines
			<span v-if="hasFilters">match</span><span v-else>in the catalog</span>
		</p>

		<!-- grid -->
		<div v-if="view === 'grid'" class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
			<MachineCard v-for="machine in visible" :key="machine.slug" :machine="machine" />
		</div>

		<!-- table -->
		<div v-else class="panel overflow-hidden">
			<div class="overflow-x-auto">
				<table class="w-full text-sm">
					<thead>
						<tr class="border-b border-line text-left">
							<th class="eyebrow px-4 py-2.5 font-semibold">
								Machine
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Manufacturer
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Year
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Platform
							</th>
							<th class="eyebrow px-3 py-2.5 text-right font-semibold">
								Switches
							</th>
							<th class="eyebrow px-3 py-2.5 text-right font-semibold">
								Lamps
							</th>
							<th class="eyebrow px-3 py-2.5 text-right font-semibold">
								Coils
							</th>
							<th class="eyebrow px-3 py-2.5 text-right font-semibold">
								ROMs
							</th>
							<th class="eyebrow px-3 py-2.5 text-right font-semibold">
								Complete
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Coverage
							</th>
						</tr>
					</thead>
					<tbody>
						<tr
							v-for="machine in visible"
							:key="machine.slug"
							class="cursor-pointer border-b border-line-soft last:border-0 hover:bg-hover/60"
							@click="router.push(`/machines/${machine.slug}`)"
						>
							<!--
								The badge sits with the machine's identity, not in the Coverage
								column, so nothing about its position suggests it is a coverage
								value. A plain span, so the row's click handler is untouched.
							-->
							<td class="px-4 py-2">
								<span class="flex flex-wrap items-center gap-x-2 gap-y-1">
									<NuxtLink :to="`/machines/${machine.slug}`" class="hover:text-amber">
										{{ machine.name }}
									</NuxtLink>
									<span v-if="machine.memoryMaps" :class="MEMORY_MAP_BADGE.chip" :title="MEMORY_MAP_BADGE.title">
										<Icon :name="MEMORY_MAP_BADGE.icon" class="size-2.5 shrink-0" />
										{{ MEMORY_MAP_BADGE.label }}
									</span>
								</span>
							</td>
							<td class="px-3 py-2 text-ink-3">
								{{ machine.manufacturer }}
							</td>
							<td class="num px-3 py-2 text-ink-3">
								{{ machine.year ?? '—' }}
							</td>
							<td class="num px-3 py-2 text-xs text-ink-3">
								{{ platformShort(machine.platform) }}
							</td>
							<td class="num px-3 py-2 text-right" :style="{ color: machine.switches ? 'var(--color-k-switch)' : 'var(--color-ink-4)' }">
								{{ machine.switches || '—' }}
							</td>
							<td class="num px-3 py-2 text-right" :style="{ color: machine.lamps ? 'var(--color-k-lamp)' : 'var(--color-ink-4)' }">
								{{ machine.lamps || '—' }}
							</td>
							<td class="num px-3 py-2 text-right" :style="{ color: machine.coils ? 'var(--color-k-coil)' : 'var(--color-ink-4)' }">
								{{ machine.coils || '—' }}
							</td>
							<td class="num px-3 py-2 text-right text-ink-3">
								{{ machine.drivers }}
							</td>
							<td class="num px-3 py-2 text-right text-xs" :style="{ color: STATUS_META[machine.status].color }">
								{{ machine.completionScore }}%
							</td>
							<td class="px-3 py-2">
								<StatusChip :status="machine.status" size="sm" />
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<div v-if="!filtered.length" class="panel px-4 py-16 text-center">
			<p class="text-sm text-ink-3">
				No machine matches those filters.
			</p>
			<button type="button" class="mt-3 text-sm text-amber hover:underline" @click="reset">
				Clear filters
			</button>
		</div>

		<button
			v-if="visible.length < filtered.length"
			type="button"
			class="mt-5 w-full rounded-lg border border-line py-3 text-sm text-ink-3 transition-colors hover:border-amber/35 hover:text-ink"
			@click="limit += 120"
		>
			Show more — {{ num((filtered.length - visible.length)) }} remaining
		</button>
	</div>
</template>
