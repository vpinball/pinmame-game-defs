<script setup lang="ts">
import curation from '../../data/curation.json'

useSeo({
	title: 'Coverage',
	description: 'How much of the PinMAME catalog is described well enough to build a table against, measured over unique physical machines rather than ROM count.',
})

const site = useSite()
const repoLink = useRepoLink()

const queue = curation as {
	ordering: string
	pending: number
	entries: { order: number | null, year: number | null, name: string, manufacturer: string, status: string, slug: string }[]
}

const maxDecade = computed(() => Math.max(...site.decades.map(d => d.total), 1))

const topManufacturers = computed(() => site.manufacturers.slice(0, 14))

const readyPct = computed(() => (site.counts.authorReady / site.counts.machines) * 100)
const partialPct = computed(() => (site.counts.partial / site.counts.machines) * 100)
</script>

<template>
	<div class="mx-auto max-w-[100rem] px-4 py-8 sm:px-6">
		<header class="mb-8">
			<h1 class="text-2xl font-semibold tracking-tight">
				Coverage
			</h1>
			<p class="mt-1.5 max-w-3xl text-sm text-ink-3">
				Completion is measured over unique physical machines, not ROM count. A clone contributes only through the fully
				resolved definition it shares. Stubs and partials count for nothing — that is deliberate, so the number never
				overstates what an author can actually build against.
			</p>
		</header>

		<!-- headline -->
		<section class="panel mb-8 p-6">
			<div class="flex flex-wrap items-end justify-between gap-4">
				<div>
					<div class="eyebrow mb-2">
						Author-ready machines
					</div>
					<div class="flex items-baseline gap-3">
						<span class="num text-4xl leading-none text-ready">{{ site.counts.authorReady }}</span>
						<span class="num text-lg text-ink-4">/ {{ site.counts.machines }}</span>
						<span class="num text-sm text-ink-3">{{ readyPct.toFixed(2) }}%</span>
					</div>
				</div>
				<div class="flex items-center gap-2 rounded-lg border border-alert/35 bg-panel px-3 py-2 text-[13px] text-alert">
					<Icon name="lucide:circle-slash" class="size-4" />
					Completion gate: fail
				</div>
			</div>

			<div class="mt-5 flex h-3 overflow-hidden rounded-full bg-line">
				<div class="bg-ready" :style="{ width: `${readyPct}%` }" />
				<div class="bg-partial" :style="{ width: `${partialPct}%` }" />
			</div>

			<dl class="mt-5 grid gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-4">
				<div v-for="item in [
					{ label: 'Author ready', value: site.counts.authorReady, color: 'var(--color-ready)' },
					{ label: 'Partial', value: site.counts.partial, color: 'var(--color-partial)' },
					{ label: 'Stub', value: site.counts.stub, color: 'var(--color-stub)' },
					{ label: 'ROM sets covered', value: site.counts.drivers, color: 'var(--color-ink-2)' },
				]" :key="item.label" class="bg-panel px-4 py-3"
				>
					<dd class="num text-xl leading-none" :style="{ color: item.color }">
						{{ num(item.value) }}
					</dd>
					<dt class="mt-1.5 text-[11px] text-ink-3">
						{{ item.label }}
					</dt>
				</div>
			</dl>
		</section>

		<div class="grid gap-6 lg:grid-cols-2">
			<!-- by decade -->
			<section class="panel p-6">
				<h2 class="text-sm font-semibold">
					Machines by decade
				</h2>
				<p class="mt-1 text-xs text-ink-3">
					The catalog is being worked newest-first, so recent decades fill in before the electromechanical era.
				</p>

				<div class="mt-5 space-y-2.5">
					<div v-for="bucket in site.decades" :key="bucket.decade" class="flex items-center gap-3">
						<span class="num w-12 shrink-0 text-xs text-ink-3">{{ bucket.decade }}s</span>
						<div class="relative h-5 flex-1 overflow-hidden rounded-md bg-raised">
							<div class="absolute inset-y-0 left-0 bg-line" :style="{ width: `${(bucket.total / maxDecade) * 100}%` }" />
							<div class="absolute inset-y-0 left-0 bg-partial/70" :style="{ width: `${((bucket.authorReady + bucket.partial) / maxDecade) * 100}%` }" />
							<div class="absolute inset-y-0 left-0 bg-ready" :style="{ width: `${(bucket.authorReady / maxDecade) * 100}%` }" />
						</div>
						<span class="num w-10 shrink-0 text-right text-xs text-ink-4">{{ bucket.total }}</span>
					</div>
				</div>
			</section>

			<!-- missing requirements -->
			<section class="panel p-6">
				<h2 class="text-sm font-semibold">
					What is missing, catalog-wide
				</h2>
				<p class="mt-1 text-xs text-ink-3">
					Each definition declares its own unmet authoring requirements. These are the totals.
				</p>

				<div class="mt-5 space-y-2">
					<div v-for="item in site.missing" :key="item.requirement" class="flex items-center gap-3">
						<span class="w-44 shrink-0 truncate text-xs text-ink-2">{{ titleCase(item.requirement) }}</span>
						<div class="h-1.5 flex-1 overflow-hidden rounded-full bg-line">
							<div class="h-full rounded-full bg-partial/70" :style="{ width: `${(item.count / site.counts.machines) * 100}%` }" />
						</div>
						<span class="num w-12 shrink-0 text-right text-xs text-ink-3">{{ item.count }}</span>
					</div>
				</div>
			</section>

			<!-- manufacturers -->
			<section class="panel p-6">
				<h2 class="text-sm font-semibold">
					By manufacturer
				</h2>
				<div class="mt-5 space-y-2.5">
					<NuxtLink
						v-for="maker in topManufacturers"
						:key="maker.name"
						:to="`/machines?mfr=${encodeURIComponent(maker.name)}`"
						class="group flex items-center gap-3"
					>
						<span class="w-32 shrink-0 truncate text-xs text-ink-2 transition-colors group-hover:text-amber">{{ maker.name }}</span>
						<div class="relative h-4 flex-1 overflow-hidden rounded bg-raised">
							<div class="absolute inset-y-0 left-0 bg-line" :style="{ width: `${(maker.machines / site.manufacturers[0]!.machines) * 100}%` }" />
							<div class="absolute inset-y-0 left-0 bg-partial/60" :style="{ width: `${((maker.authorReady + maker.partial) / site.manufacturers[0]!.machines) * 100}%` }" />
							<div class="absolute inset-y-0 left-0 bg-ready" :style="{ width: `${(maker.authorReady / site.manufacturers[0]!.machines) * 100}%` }" />
						</div>
						<span class="num w-10 shrink-0 text-right text-xs text-ink-4">{{ maker.machines }}</span>
					</NuxtLink>
				</div>
			</section>

			<!-- queue -->
			<section class="panel overflow-hidden">
				<div class="p-6 pb-4">
					<h2 class="text-sm font-semibold">
						Curation queue · next up
					</h2>
					<p class="mt-1 text-xs text-ink-3">
						Processed newest to oldest, keeping related driver variants together.
						<span class="num text-ink-4">{{ num(queue.pending) }} machines pending.</span>
					</p>
				</div>
				<div class="max-h-96 overflow-y-auto border-t border-line">
					<table class="w-full text-sm">
						<tbody>
							<tr v-for="row in queue.entries" :key="`${row.order}-${row.name}`" class="border-b border-line-soft last:border-0 hover:bg-hover/60">
								<td class="num w-12 px-4 py-2 text-xs text-ink-4">
									{{ row.order }}
								</td>
								<td class="num w-14 px-2 py-2 text-xs text-ink-3">
									{{ row.year ?? '—' }}
								</td>
								<td class="px-2 py-2 text-[13px]">
									<NuxtLink :to="`/machines/${row.slug}`" class="text-ink-2 hover:text-amber">
										{{ row.name }}
									</NuxtLink>
								</td>
								<td class="px-2 py-2 text-right text-[11px] text-ink-4">
									{{ row.manufacturer }}
								</td>
								<td class="w-6 px-2 py-2">
									<StatusChip :status="(row.status as any)" dot-only />
								</td>
							</tr>
							<tr v-if="!queue.entries.length">
								<td class="px-4 py-8 text-center text-sm text-ink-3">
									Queue data not available in this build.
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</section>
		</div>

		<ContributeCard
			class="mt-10"
			tone="author"
			primary-to="/machines?status=stub"
			primary-label="Browse machines needing work"
			hint="Coverage moves one machine at a time. Pick anything from the queue you own, have the manual for, or have already built a table against — each machine page has a one-click edit link to its definition file."
		/>

		<!-- how a definition graduates -->
		<section class="mt-10">
			<h2 class="mb-4 text-lg font-semibold tracking-tight">
				How a definition graduates
			</h2>
			<ol class="grid gap-3 md:grid-cols-3">
				<li v-for="(step, index) in [
					{ status: 'stub', title: 'Stub', body: 'Generated from the PinMAME driver catalog so every supported ROM is reachable. Carries identity and nothing else, and is named stub.pinmame.* so it can never be mistaken for real data.' },
					{ status: 'partial', title: 'Partial', body: 'Evidence has been merged — legacy definitions, a table script, a manual, a simulator run. Enough to be useful, not enough to be trusted end to end. Conflicts stay visible instead of being silently resolved.' },
					{ status: 'author_ready', title: 'Author ready', body: 'The completeness validator found every address named, every mechanism given its actuators and sensors, variants accounted for, provenance attached, and a recreation note written. Only the validator can grant this.' },
				]" :key="step.status" class="panel p-5"
				>
					<div class="flex items-center gap-3">
						<span class="num grid size-7 place-items-center rounded-lg border border-line text-xs text-ink-4">{{ index + 1 }}</span>
						<StatusChip :status="(step.status as any)" />
					</div>
					<h3 class="mt-4 text-sm font-semibold">
						{{ step.title }}
					</h3>
					<p class="mt-1.5 text-[13px] leading-relaxed text-ink-3">
						{{ step.body }}
					</p>
				</li>
			</ol>
		</section>
	</div>
</template>
