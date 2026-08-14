<script setup lang="ts">
import type { DriverEntry } from '~/types/defs'

useSeo({
	title: 'ROM sets',
	description: 'Look up any PinMAME driver id — mtl_180h, t2_l8, afm_113b — and follow it to the physical machine it belongs to.',
})

const site = useSite()

const drivers = shallowRef<DriverEntry[]>([])
const loading = ref(true)
const query = ref('')
// See useInitialQuery: the arrival query has to be snapshotted before the
// router rewrites the URL during hydration.
const urlReady = ref(false)
const onlyDescribed = ref(false)
const limit = ref(80)

onMounted(async () => {
	query.value = useInitialQuery().get('q') ?? ''
	urlReady.value = true
	try {
		drivers.value = await loadDrivers()
	}
	finally {
		loading.value = false
	}
})

// Written directly to history — see the machines list for why.
watchEffect(() => {
	const next = query.value
	if (!urlReady.value || !import.meta.client) return
	history.replaceState(history.state, '', next ? `?q=${encodeURIComponent(next)}` : window.location.pathname)
})

watch([query, onlyDescribed], () => { limit.value = 80 })

const filtered = computed(() => {
	const needle = query.value.trim().toLowerCase()
	let list = drivers.value
	if (onlyDescribed.value) list = list.filter(d => d.status !== 'stub')
	if (needle) {
		list = list.filter(d =>
			d.id.includes(needle)
			|| d.description.toLowerCase().includes(needle)
			|| d.machineName.toLowerCase().includes(needle)
			|| (d.manufacturer ?? '').toLowerCase().includes(needle))
	}
	// Unsearched, the table reads as a catalog: newest revisions first.
	if (!needle) return list.slice().sort(byNewestFirst)
	// Once searching, exact and prefix hits on the driver name float to the top.
	return list.slice().sort((a, b) => score(a, needle) - score(b, needle) || byNewestFirst(a, b))
})

function score(driver: DriverEntry, needle: string) {
	if (driver.id === needle) return 0
	if (driver.id.startsWith(needle)) return 1
	if (driver.description.toLowerCase().startsWith(needle)) return 2
	return 3
}

const visible = computed(() => filtered.value.slice(0, limit.value))

/**
 * Where a ROM's memory-map badge points.
 *
 * Straight at the panel when the machine has a detail page, and at the page
 * itself when it does not: a stub renders no `#memory-maps` section, so the
 * fragment would silently do nothing and leave the reader at the top of the
 * page wondering what they had missed.
 */
const memoryMapLink = (driver: DriverEntry) =>
	`/machines/${driver.machineSlug}${driver.status === 'stub' ? '' : '#memory-maps'}`
</script>

<template>
	<div class="mx-auto max-w-[100rem] px-4 py-8 sm:px-6">
		<header class="mb-6">
			<h1 class="text-2xl font-semibold tracking-tight">
				ROM set lookup
			</h1>
			<p class="mt-1.5 max-w-2xl text-sm text-ink-3">
				All {{ num(site.counts.drivers) }} drivers the pinned PinMAME build reports, mapped to the physical
				machine they belong to. Paste the ROM name your table binds and follow it through.
			</p>
		</header>

		<div class="panel sticky top-14 z-30 mb-5 flex flex-wrap items-center gap-3 p-3">
			<div class="relative min-w-56 flex-1">
				<Icon name="lucide:search" class="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-ink-4" />
				<input
					v-model="query"
					type="search"
					placeholder="mtl_180h, t2_l8, afm_113b…"
					class="num w-full rounded-lg border border-line bg-raised py-2 pr-3 pl-9 text-sm text-ink placeholder:text-ink-4 focus:border-amber/50 focus:outline-none"
					autocomplete="off"
					spellcheck="false"
				>
			</div>
			<label class="flex cursor-pointer items-center gap-2 text-[13px] text-ink-3 select-none">
				<input v-model="onlyDescribed" type="checkbox" class="accent-amber">
				Only described machines
			</label>
			<span class="num text-xs text-ink-4">{{ num(filtered.length) }} / {{ num(drivers.length) }}</span>
		</div>

		<div v-if="loading" class="panel px-4 py-16 text-center text-sm text-ink-3">
			Loading the driver catalog…
		</div>

		<div v-else class="panel overflow-hidden">
			<div class="overflow-x-auto">
				<table class="w-full text-sm">
					<thead>
						<tr class="border-b border-line text-left">
							<th class="eyebrow px-4 py-2.5 font-semibold">
								ROM set
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Description
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Year
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Parent
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Resolves to
							</th>
							<th class="eyebrow px-3 py-2.5 font-semibold">
								Coverage
							</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="driver in visible" :key="driver.id" class="border-b border-line-soft last:border-0 hover:bg-hover/60">
							<td class="px-4 py-2">
								<span class="flex flex-wrap items-center gap-x-2 gap-y-1">
									<span class="num rounded-md border border-amber/25 bg-amber/8 px-1.5 py-0.5 text-xs whitespace-nowrap text-amber">{{ driver.id }}</span>
									<NuxtLink
										v-if="driver.memoryMap"
										:to="memoryMapLink(driver)"
										class="transition-colors hover:border-amber/40 hover:text-amber"
										:class="MEMORY_MAP_BADGE.chip"
										:title="`${MEMORY_MAP_BADGE.title} Platform ${driver.memoryMap?.platform}.`"
										:aria-label="`${MEMORY_MAP_BADGE.label} for ${driver.id} on ${driver.machineName}`"
									>
										<Icon :name="MEMORY_MAP_BADGE.icon" class="size-2.5 shrink-0" />
										{{ MEMORY_MAP_BADGE.label }}
									</NuxtLink>
								</span>
							</td>
							<td class="px-3 py-2 text-ink-2">
								{{ driver.description }}
							</td>
							<td class="num px-3 py-2 text-ink-3">
								{{ driver.year ?? '—' }}
							</td>
							<td class="num px-3 py-2 text-xs text-ink-4">
								{{ driver.cloneOf ?? '—' }}
							</td>
							<td class="px-3 py-2">
								<NuxtLink :to="`/machines/${driver.machineSlug}`" class="inline-flex items-center gap-1.5 hover:text-amber">
									{{ driver.machineName }}
									<Icon name="lucide:arrow-up-right" class="size-3 opacity-60" />
								</NuxtLink>
							</td>
							<td class="px-3 py-2">
								<StatusChip :status="driver.status" size="sm" />
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<div v-if="!filtered.length" class="px-4 py-16 text-center text-sm text-ink-3">
				No ROM set matches “{{ query }}”.
			</div>

			<button
				v-if="visible.length < filtered.length"
				type="button"
				class="w-full border-t border-line py-3 text-sm text-ink-3 transition-colors hover:bg-hover hover:text-ink"
				@click="limit += 200"
			>
				Show more — {{ num((filtered.length - visible.length)) }} remaining
			</button>
		</div>
	</div>
</template>
