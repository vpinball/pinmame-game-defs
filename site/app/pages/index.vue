<script setup lang="ts">
const site = useSite()

useSeo({
	description: 'A browsable reference of every PinMAME-supported pinball machine: switch and lamp addresses, coil functions, displays, mechanisms and the evidence behind them — for table authors.',
})

const { data: featured } = await useAsyncData('home-featured', async () => {
	const machines = await loadMachineIndex()
	const ready = machines.filter(m => m.status === 'author_ready')
	const partial = machines.filter(m => m.status === 'partial')
	return {
		ready: ready.slice(0, 8),
		partial: partial.slice(0, 4),
		readyTotal: ready.length,
	}
}, { default: () => ({ ready: [], partial: [], readyTotal: 0 }) })

// Kept short enough that the 5x7 panel font can render each line at 1x or
// better — the display truncates rather than overflows.
const dmdLines = computed(() => [
	['PINMAME', 'MACHINE REFERENCE'],
	[`${site.counts.drivers} ROM SETS`, `${site.counts.machines} MACHINES`],
	[`${site.counts.authorReady} AUTHOR READY`, `${site.counts.partial} PARTIAL`],
	['SWITCHES LAMPS COILS', 'MECHS AND WIRING'],
])

const readyPct = computed(() => (site.counts.authorReady / site.counts.machines) * 100)
const partialPct = computed(() => (site.counts.partial / site.counts.machines) * 100)

const topPlatforms = computed(() =>
	site.platforms.filter(p => p.machines > 0).sort((a, b) => b.machines - a.machines).slice(0, 6))

const corpus = computed(() => [
	{ label: 'Switches described', value: site.corpus.switches, kind: 'switch' },
	{ label: 'Lamps described', value: site.corpus.lamps, kind: 'lamp' },
	{ label: 'Coils & devices', value: site.corpus.coils, kind: 'coil' },
	{ label: 'Flashers', value: site.corpus.flashers, kind: 'flasher' },
	{ label: 'Mechanisms', value: site.corpus.mechanisms, kind: 'motor' },
	{ label: 'Cited sources', value: site.corpus.sources, kind: 'display' },
])
</script>

<template>
	<div>
		<!-- ── hero ───────────────────────────────────────────────────────── -->
		<section class="dotfield relative overflow-hidden border-b border-line">
			<div
				class="pointer-events-none absolute -top-40 left-1/2 h-80 w-[46rem] -translate-x-1/2 rounded-full opacity-45 blur-[110px]"
				style="background: radial-gradient(closest-side, var(--color-plasma), transparent)"
			/>

			<div class="relative mx-auto grid max-w-[100rem] items-center gap-10 px-4 pt-8 pb-8 sm:px-6 lg:grid-cols-[1.1fr_1fr] lg:pt-12 lg:pb-12">
				<div class="rise">
					<div class="eyebrow mb-4 flex items-center gap-2">
						<span class="size-1.5 rounded-full bg-amber" />
						PinMAME {{ shortHash(site.pinmameRevision) }} · libpinmame {{ site.libraryVersion }}
					</div>

					<h1 class="text-4xl leading-[1.05] font-semibold tracking-tight text-balance sm:text-5xl lg:text-[3.4rem]">
						Every switch, lamp and coil
						<span class="text-amber">PinMAME can talk to.</span>
					</h1>

					<p class="mt-5 max-w-xl text-[15px] leading-relaxed text-ink-2">
						A machine-by-machine reference for pinball table authors. Look up a ROM set, get the exact addresses the
						emulator uses, what each one is on the real playfield, how the mechanisms behave — and the evidence every
						claim came from.
					</p>

					<div class="mt-8 flex flex-wrap items-center gap-3">
						<NuxtLink
							to="/machines?status=author_ready"
							class="inline-flex items-center gap-2 rounded-lg bg-amber px-4 py-2.5 text-sm font-medium text-void transition-transform hover:-translate-y-0.5"
						>
							<Icon name="lucide:library" class="size-4" />
							Browse {{ site.counts.authorReady }} complete machines
						</NuxtLink>
						<NuxtLink
							to="/roms"
							class="inline-flex items-center gap-2 rounded-lg border border-line px-4 py-2.5 text-sm text-ink-2 transition-colors hover:border-amber/40 hover:text-ink"
						>
							<Icon name="lucide:file-search" class="size-4" />
							Look up a ROM set
						</NuxtLink>
					</div>

					<dl class="mt-10 grid max-w-lg grid-cols-3 gap-px overflow-hidden rounded-xl border border-line bg-line">
						<div v-for="stat in [
							{ label: 'ROM sets', value: site.counts.drivers },
							{ label: 'Physical machines', value: site.counts.machines },
							{ label: 'Controller platforms', value: site.counts.platforms },
						]" :key="stat.label" class="bg-panel px-4 py-3.5"
						>
							<dd class="num text-2xl leading-none text-ink">
								{{ num(stat.value) }}
							</dd>
							<dt class="mt-1.5 text-[11px] text-ink-3">
								{{ stat.label }}
							</dt>
						</div>
					</dl>
				</div>

				<div class="rise" style="animation-delay: 90ms">
					<ClientOnly>
						<DotMatrix :lines="dmdLines" />
						<template #fallback>
							<div class="aspect-[4/1] w-full rounded-lg bg-void ring-1 ring-white/8" />
						</template>
					</ClientOnly>

					<div class="panel mt-4 p-4">
						<div class="mb-3 flex items-baseline justify-between">
							<span class="eyebrow">Catalog coverage</span>
							<span class="num text-xs text-ink-3">{{ readyPct.toFixed(1) }}% author ready</span>
						</div>
						<div class="flex h-2.5 overflow-hidden rounded-full bg-line">
							<div class="bg-ready transition-all" :style="{ width: `${readyPct}%` }" />
							<div class="bg-partial transition-all" :style="{ width: `${partialPct}%` }" />
						</div>
						<div class="mt-3 flex flex-wrap gap-x-5 gap-y-1.5 text-[11px] text-ink-3">
							<span class="flex items-center gap-1.5"><span class="size-2 rounded-full bg-ready" />{{ site.counts.authorReady }} author ready</span>
							<span class="flex items-center gap-1.5"><span class="size-2 rounded-full bg-partial" />{{ site.counts.partial }} partial</span>
							<span class="flex items-center gap-1.5"><span class="size-2 rounded-full bg-stub" />{{ site.counts.stub }} stub</span>
						</div>
						<p class="mt-3 text-[11px] leading-relaxed text-ink-4">
							Coverage is fail-closed: a definition only becomes author-ready once every address is named, every
							mechanism has its actuators and sensors, and the recreation note exists.
						</p>
					</div>
				</div>
			</div>
		</section>

		<!-- ── how to use it ──────────────────────────────────────────────── -->
		<section class="mx-auto max-w-[100rem] px-4 py-14 sm:px-6">
			<div class="grid gap-4 md:grid-cols-3">
				<NuxtLink
					v-for="card in [
						{ to: '/roms', icon: 'lucide:file-search', title: 'I have a ROM name', body: 'Paste a driver like mtl_180h or t2_l8 and jump straight to the machine it belongs to, with every sibling revision listed.' },
						{ to: '/machines?status=author_ready', icon: 'lucide:list-checks', title: 'I am building a table', body: 'Start from a complete definition: numbered switches and lamps, coil functions, mechanism causality and initial ball state.' },
						{ to: '/guide', icon: 'lucide:compass', title: 'What am I looking at?', body: 'How addresses, roles, polarity, coverage states and provenance work — and which source wins when two of them disagree.' },
					]"
					:key="card.to"
					:to="card.to"
					class="panel group p-5 transition-colors hover:border-amber/35"
				>
					<span class="grid size-9 place-items-center rounded-lg border border-line bg-raised text-amber">
						<Icon :name="card.icon" class="size-4" />
					</span>
					<h3 class="mt-4 text-sm font-semibold transition-colors group-hover:text-amber">
						{{ card.title }}
					</h3>
					<p class="mt-1.5 text-[13px] leading-relaxed text-ink-3">
						{{ card.body }}
					</p>
				</NuxtLink>
			</div>
		</section>

		<!-- ── featured ───────────────────────────────────────────────────── -->
		<section class="mx-auto max-w-[100rem] px-4 pb-14 sm:px-6">
			<header class="mb-5 flex flex-wrap items-end justify-between gap-3">
				<div>
					<h2 class="text-lg font-semibold tracking-tight">
						Complete definitions
					</h2>
					<p class="mt-1 text-sm text-ink-3">
						Validated end to end — safe to build a table against.
					</p>
				</div>
				<NuxtLink to="/machines?status=author_ready" class="inline-flex items-center gap-1.5 text-sm text-amber hover:underline">
					All {{ featured.readyTotal }}
					<Icon name="lucide:arrow-right" class="size-3.5" />
				</NuxtLink>
			</header>

			<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
				<MachineCard v-for="machine in featured.ready" :key="machine.slug" :machine="machine" />
			</div>
		</section>

		<!-- ── what a definition contains ─────────────────────────────────── -->
		<section class="border-y border-line bg-panel/40">
			<div class="mx-auto max-w-[100rem] px-4 py-14 sm:px-6">
				<h2 class="text-lg font-semibold tracking-tight">
					What the catalog already describes
				</h2>
				<p class="mt-1 max-w-2xl text-sm text-ink-3">
					Totals across every definition in the repository, stubs excluded.
				</p>

				<dl class="mt-6 grid gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-3 lg:grid-cols-6">
					<div v-for="item in corpus" :key="item.label" class="bg-panel px-4 py-4">
						<dd class="num text-2xl leading-none" :style="{ color: kindColor(item.kind) }">
							{{ num(item.value) }}
						</dd>
						<dt class="mt-2 text-[11px] leading-snug text-ink-3">
							{{ item.label }}
						</dt>
					</div>
				</dl>
			</div>
		</section>

		<!-- ── platforms ──────────────────────────────────────────────────── -->
		<section class="mx-auto max-w-[100rem] px-4 py-14 sm:px-6">
			<header class="mb-5 flex flex-wrap items-end justify-between gap-3">
				<div>
					<h2 class="text-lg font-semibold tracking-tight">
						Controller platforms
					</h2>
					<p class="mt-1 text-sm text-ink-3">
						Address ranges, transports and normalisation rules per hardware family.
					</p>
				</div>
				<NuxtLink to="/platforms" class="inline-flex items-center gap-1.5 text-sm text-amber hover:underline">
					All platforms
					<Icon name="lucide:arrow-right" class="size-3.5" />
				</NuxtLink>
			</header>

			<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
				<NuxtLink
					v-for="platform in topPlatforms"
					:key="platform.id"
					:to="`/platforms/${platform.slug}`"
					class="panel group flex items-center gap-4 p-4 transition-colors hover:border-amber/35"
				>
					<BrandMark :platform="platform.id" />
					<div class="min-w-0">
						<div class="truncate text-sm font-medium transition-colors group-hover:text-amber">
							{{ platform.hardwareFamily ?? platformShort(platform.id) }}
						</div>
						<div class="mt-0.5 text-xs text-ink-3">
							{{ platform.machines }} machine{{ platform.machines === 1 ? '' : 's' }}
							<span v-if="platform.authorReady" class="text-ready">· {{ platform.authorReady }} ready</span>
							<span v-if="!platform.hasProfile" class="text-ink-4">· profile pending</span>
						</div>
					</div>
					<Icon name="lucide:chevron-right" class="ml-auto size-4 shrink-0 text-ink-4 transition-transform group-hover:translate-x-0.5" />
				</NuxtLink>
			</div>
		</section>
	</div>
</template>
