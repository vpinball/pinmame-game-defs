<script setup lang="ts">
import familiesJson from '../../../data/families.json'
import type { MachineFamily } from '~/types/defs'

/**
 * One title, all its editions.
 *
 * Stern shipped most games as a Pro and a Premium/LE with genuinely different
 * playfields, so the catalog holds them as separate machines. Correct — but it
 * leaves four AC/DC entries sitting in search with nothing saying they are one
 * title. This page is the missing parent, and its real job is the comparison:
 * an author choosing which edition to build needs to know that the Premium has
 * two more kickers and a motorised toy the Pro never had.
 */
const route = useRoute()
const families = familiesJson as unknown as MachineFamily[]
const family = computed(() => families.find(f => f.slug === route.params.slug))

if (!family.value) {
	throw createError({ statusCode: 404, statusMessage: 'Family not found', fatal: true })
}

useSeo({
	title: () => family.value!.title,
	description: () => `${family.value!.title} (${family.value!.manufacturer}) shipped in `
		+ `${family.value!.machines.length} editions: ${family.value!.machines.map(m => m.edition).join(', ')}. `
		+ 'Compare their switches, lamps, coils and mechanisms side by side.',
})

const machines = computed(() => family.value!.machines)
const opdbUrl = computed(() =>
	family.value?.opdbId ? `https://opdb.org/search?q=${encodeURIComponent(family.value.opdbId)}` : null)

const COUNTS = [
	{ key: 'switches', label: 'Switches', kind: 'switch' },
	{ key: 'lamps', label: 'Lamps', kind: 'lamp' },
	{ key: 'coils', label: 'Coils', kind: 'coil' },
	{ key: 'flashers', label: 'Flashers', kind: 'flasher' },
	{ key: 'gi', label: 'GI', kind: 'gi' },
	{ key: 'mechanisms', label: 'Mechanisms', kind: 'motor' },
] as const

/** Only rows where the editions actually differ are worth a reader's attention. */
const countRows = computed(() =>
	COUNTS.map(row => ({
		...row,
		values: machines.value.map(m => m.counts[row.key]),
		differs: new Set(machines.value.map(m => m.counts[row.key])).size > 1,
	})).filter(row => row.values.some(v => v > 0)))

const mechanismRows = computed(() => {
	const kinds = [...new Set(machines.value.flatMap(m => Object.keys(m.mechanismKinds)))].sort()
	return kinds.map(kind => ({
		kind,
		values: machines.value.map(m => m.mechanismKinds[kind] ?? 0),
		differs: new Set(machines.value.map(m => m.mechanismKinds[kind] ?? 0)).size > 1,
	}))
})

const displayRow = computed(() => ({
	values: machines.value.map(m => m.displays.join(', ') || '—'),
	differs: new Set(machines.value.map(m => m.displays.join(', '))).size > 1,
}))

const onlyDifferences = ref(true)

const visibleCounts = computed(() => countRows.value.filter(r => !onlyDifferences.value || r.differs))
const visibleMechanisms = computed(() => mechanismRows.value.filter(r => !onlyDifferences.value || r.differs))
const differenceCount = computed(() =>
	countRows.value.filter(r => r.differs).length
	+ mechanismRows.value.filter(r => r.differs).length
	+ (displayRow.value.differs ? 1 : 0))
</script>

<template>
	<div v-if="family" class="mx-auto max-w-[100rem] px-4 py-8 sm:px-6">
		<nav class="mb-5 flex items-center gap-1.5 text-xs text-ink-4">
			<NuxtLink to="/machines" class="hover:text-amber">
				Machines
			</NuxtLink>
			<Icon name="lucide:chevron-right" class="size-3" />
			<NuxtLink :to="`/machines?mfr=${encodeURIComponent(family.manufacturer)}`" class="hover:text-amber">
				{{ family.manufacturer }}
			</NuxtLink>
		</nav>

		<header class="mb-8">
			<div class="flex flex-wrap items-start justify-between gap-4">
				<h1 class="text-2xl font-semibold tracking-tight sm:text-3xl">
					{{ family.title }}
				</h1>
				<a
					v-if="opdbUrl"
					:href="opdbUrl"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center gap-1.5 rounded-lg border border-line px-3 py-1.5 text-[13px] text-ink-2 transition-colors hover:border-amber/40 hover:text-ink"
				>
					<Icon name="lucide:database" class="size-3.5" />
					OPDB
					<Icon name="lucide:external-link" class="size-3" />
				</a>
			</div>
			<p class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-ink-3">
				<span>{{ family.manufacturer }}</span>
				<span class="num">{{ family.years[0] === family.years[1] ? family.years[0] : `${family.years[0]}–${family.years[1]}` }}</span>
				<span
					v-if="family.driverPrefix"
					class="num rounded border border-line px-1.5 py-0.5 text-[11px]"
				>{{ family.driverPrefix }}_*</span>
			</p>
			<p class="mt-3 max-w-3xl text-sm leading-relaxed text-ink-3">
				{{ machines.length }} editions of one title, held as separate machines because their playfields differ.
				<template v-if="!family.authored">
					Grouped by the PinMAME driver prefix they share — the catalog has no family record for this title, so the
					relationship is derived rather than authored.
				</template>
			</p>
		</header>

		<!-- the catalog's own account of the differences, when it has one -->
		<article v-if="family.overviewHtml" class="knowledge panel mb-8 max-w-3xl p-5 sm:p-6" v-html="family.overviewHtml" />

		<!-- the editions -->
		<section class="mb-8 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
			<NuxtLink
				v-for="machine in machines"
				:key="machine.slug"
				:to="`/machines/${machine.slug}`"
				class="panel group relative flex min-w-0 flex-col overflow-hidden p-4 transition-colors hover:border-amber/35"
			>
				<span
					class="absolute inset-y-0 left-0 w-0.5"
					:style="{ background: STATUS_META[machine.status].color, opacity: machine.status === 'stub' ? 0.35 : 0.9 }"
				/>
				<div class="flex items-start justify-between gap-3">
					<div class="min-w-0">
						<h2 class="truncate text-[15px] font-semibold transition-colors group-hover:text-amber">
							{{ machine.edition }}
						</h2>
						<p class="num mt-0.5 text-xs text-ink-3">
							{{ machine.year }} · {{ machine.drivers }} ROM{{ machine.drivers === 1 ? '' : 's' }}
						</p>
					</div>
					<StatusChip :status="machine.status" size="sm" />
				</div>

				<!-- the catalog's own account of this edition, when it has one -->
				<p v-if="machine.differences" class="mt-3 text-[13px] leading-relaxed text-ink-3">
					{{ machine.differences }}
				</p>

				<dl class="mt-auto flex flex-wrap gap-x-4 gap-y-2 pt-4">
					<div v-for="stat in COUNTS.filter(s => machine.counts[s.key] > 0)" :key="stat.key">
						<dd class="num text-sm leading-none" :style="{ color: kindColor(stat.kind) }">
							{{ machine.counts[stat.key] }}
						</dd>
						<dt class="mt-1 text-[10px] text-ink-4">
							{{ stat.label.toLowerCase() }}
						</dt>
					</div>
				</dl>
			</NuxtLink>
		</section>

		<!-- what actually differs -->
		<section>
			<header class="mb-3 flex flex-wrap items-end justify-between gap-3">
				<div>
					<h2 class="text-xl font-semibold tracking-tight">
						What differs, by the numbers
					</h2>
					<p class="mt-1 text-sm text-ink-3">
						{{ differenceCount }} of the compared properties differ. Counted from each edition's own definition, so
						this holds whether or not anyone has written the differences down.
					</p>
				</div>
				<label class="flex cursor-pointer items-center gap-2 text-[13px] text-ink-3 select-none">
					<input v-model="onlyDifferences" type="checkbox" class="accent-amber">
					Differences only
				</label>
			</header>

			<div class="panel overflow-hidden">
				<div class="overflow-x-auto">
					<table class="w-full text-sm">
						<thead>
							<tr class="border-b border-line text-left">
								<th class="eyebrow px-4 py-2.5 font-semibold">
									Property
								</th>
								<th
									v-for="machine in machines"
									:key="machine.slug"
									class="eyebrow px-3 py-2.5 text-right font-semibold"
								>
									{{ machine.edition }}
								</th>
							</tr>
						</thead>
						<tbody>
							<tr v-if="!onlyDifferences || displayRow.differs" class="border-b border-line-soft">
								<td class="px-4 py-2 text-ink-2">
									Displays
								</td>
								<td
									v-for="(value, i) in displayRow.values"
									:key="i"
									class="num px-3 py-2 text-right text-xs"
									:class="displayRow.differs ? 'text-ink' : 'text-ink-3'"
								>
									{{ value }}
								</td>
							</tr>

							<tr v-for="row in visibleCounts" :key="row.key" class="border-b border-line-soft">
								<td class="px-4 py-2">
									<span class="inline-flex items-center gap-2 text-ink-2">
										<span class="size-1.5 rounded-[2px]" :style="{ background: kindColor(row.kind) }" />
										{{ row.label }}
									</span>
								</td>
								<td
									v-for="(value, i) in row.values"
									:key="i"
									class="num px-3 py-2 text-right"
									:class="row.differs ? 'text-ink' : 'text-ink-4'"
								>
									{{ value }}
								</td>
							</tr>

							<tr v-if="visibleMechanisms.length">
								<td class="eyebrow px-4 pt-4 pb-1" :colspan="machines.length + 1">
									Mechanisms by kind
								</td>
							</tr>
							<tr v-for="row in visibleMechanisms" :key="row.kind" class="border-b border-line-soft last:border-0">
								<td class="px-4 py-2 text-ink-2 capitalize">
									{{ row.kind.replace(/_/g, ' ') }}
								</td>
								<td
									v-for="(value, i) in row.values"
									:key="i"
									class="num px-3 py-2 text-right"
									:class="value === 0 ? 'text-ink-4' : row.differs ? 'text-ink' : 'text-ink-3'"
								>
									{{ value || '—' }}
								</td>
							</tr>
						</tbody>
					</table>
				</div>

				<p class="border-t border-line px-4 py-2.5 text-[11px] leading-relaxed text-ink-4">
					Counts come from each edition's own definition. A zero means the definition records none — for a
					<NuxtLink to="/machines?status=stub" class="text-ink-3 hover:text-amber">
						stub
					</NuxtLink>
					or partial edition that may mean nobody has described it yet rather than that the machine lacks it.
				</p>
			</div>
		</section>
	</div>
</template>
