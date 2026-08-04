<script setup lang="ts">
import type { Device, MachineDetail, MachineSummary } from '~/types/defs'

const route = useRoute()
const repoLink = useRepoLink()
const slug = computed(() => String(route.params.slug))

const { data } = await useAsyncData(`machine-${slug.value}`, async () => {
	const detail = await loadMachineDetail(slug.value)
	if (detail) return { detail, summary: null as MachineSummary | null }
	// Stubs have no detail file — fall back to the browse index row.
	const summary = (await loadMachineIndex()).find(m => m.slug === slug.value) ?? null
	return { detail: null as MachineDetail | null, summary }
})

if (!data.value?.detail && !data.value?.summary) {
	throw createError({ statusCode: 404, statusMessage: 'Machine not found', fatal: true })
}

const detail = computed(() => data.value?.detail ?? null)
const summary = computed(() => data.value?.summary ?? null)

const name = computed(() => detail.value?.machine.name ?? summary.value?.name ?? slug.value)
const manufacturer = computed(() => detail.value?.machine.manufacturer ?? summary.value?.manufacturer ?? '')
const year = computed(() => detail.value?.machine.year ?? summary.value?.year ?? null)
const status = computed(() => detail.value?.coverage.status ?? summary.value?.status ?? 'stub')

useSeo({
	title: name,
	description: () => detail.value
		? `${name.value} (${manufacturer.value}, ${year.value}) — ${detail.value.inputs.length} inputs, ${detail.value.outputs.length} outputs, ${detail.value.mechanisms.length} mechanisms and the PinMAME addresses behind them.`
		: `${name.value} is catalogued in PinMAME but not yet described.`,
	// A stub's only unique content is its name and ROM list. Indexing 683 of
	// them would dilute the described machines they share a domain with, so
	// they stay crawlable and linkable but out of the index.
	noindex: () => !detail.value,
})

/* -- derived ------------------------------------------------------------- */

const deviceById = computed(() => {
	const map = new Map<string, Device>()
	for (const device of [...(detail.value?.inputs ?? []), ...(detail.value?.outputs ?? [])]) map.set(device.id, device)
	return map
})

const switches = computed(() => detail.value?.inputs.filter(i => i.kind === 'switch') ?? [])
const dips = computed(() => detail.value?.inputs.filter(i => i.kind === 'dip_switch') ?? [])
const otherInputs = computed(() => detail.value?.inputs.filter(i => !['switch', 'dip_switch'].includes(i.kind)) ?? [])

const outputGroups = computed(() => {
	const outputs = detail.value?.outputs ?? []
	return [
		{ id: 'coils', label: 'Coils, magnets & motors', kinds: ['coil', 'magnet', 'motor', 'servo', 'relay'], matrix: false },
		{ id: 'flashers', label: 'Flashers', kinds: ['flasher'], matrix: false },
		{ id: 'lamps', label: 'Lamps', kinds: ['lamp', 'rgb_lamp'], matrix: true },
		{ id: 'gi', label: 'General illumination', kinds: ['gi'], matrix: false },
		{ id: 'other-out', label: 'Virtual & other outputs', kinds: ['virtual', 'constant', 'display'], matrix: false },
	]
		.map(group => ({ ...group, devices: outputs.filter(o => group.kinds.includes(o.kind)) }))
		.filter(group => group.devices.length)
})

const usedCount = computed(() => {
	const all = [...(detail.value?.inputs ?? []), ...(detail.value?.outputs ?? [])]
	return {
		used: all.filter(d => d.availability === 'used').length,
		unused: all.filter(d => d.availability === 'unused').length,
		optional: all.filter(d => d.availability === 'optional').length,
	}
})

/**
 * One selected device, shared by the playfield map, the address matrices and
 * the device tables — picking an address anywhere highlights it everywhere.
 */
const selected = ref<string | null>(null)
/** Selecting the same device again clears it, everywhere it can be picked. */
const select = (device: Device | null) => {
	selected.value = device && selected.value !== device.id ? device.id : null
}

const placements = computed(() => {
	const devices = [...(detail.value?.inputs ?? []), ...(detail.value?.outputs ?? [])]
	return devices.filter(d => d.spatial && d.spatial.status !== 'not_applicable').length
})

const sections = computed(() => {
	if (!detail.value) return []
	const items = [
		{ id: 'setup', label: 'Setup', icon: 'lucide:plug-zap', show: true },
		{ id: 'playfield', label: 'Playfield', icon: 'lucide:map-pin', show: placements.value > 0, count: placements.value },
		{ id: 'coverage', label: 'Coverage', icon: 'lucide:shield-check', show: true },
		{ id: 'switches', label: 'Switches', icon: 'lucide:toggle-left', show: switches.value.length > 0, count: switches.value.length },
		{ id: 'outputs', label: 'Outputs', icon: 'lucide:zap', show: (detail.value.outputs.length ?? 0) > 0, count: detail.value.outputs.length },
		{ id: 'mechanisms', label: 'Mechanisms', icon: 'lucide:cog', show: detail.value.mechanisms.length > 0, count: detail.value.mechanisms.length },
		{ id: 'wiring', label: 'Direct wiring', icon: 'lucide:cable', show: detail.value.relationships.length > 0, count: detail.value.relationships.length },
		{ id: 'notes', label: 'Recreation notes', icon: 'lucide:notebook-pen', show: !!detail.value.knowledgeHtml },
		{ id: 'roms', label: 'ROM sets', icon: 'lucide:disc-3', show: true, count: detail.value.catalogDrivers?.length ?? detail.value.drivers.length },
		{ id: 'sources', label: 'Evidence', icon: 'lucide:library-big', show: detail.value.sources.length > 0, count: detail.value.sources.length },
	]
	return items.filter(item => item.show)
})

const activeSection = ref('setup')
onMounted(() => {
	const observer = new IntersectionObserver(
		(entries) => {
			for (const entry of entries) {
				if (entry.isIntersecting) activeSection.value = entry.target.id
			}
		},
		{ rootMargin: '-88px 0px -70% 0px', threshold: 0 },
	)
	for (const section of sections.value) {
		const el = document.getElementById(section.id)
		if (el) observer.observe(el)
	}
	onBeforeUnmount(() => observer.disconnect())
})

// Stubs have no detail payload, but the browse index still knows where their
// generated file lives — so every page links to a file, never the repo root.
const definitionPath = computed(() => detail.value?.sourcePath ?? summary.value?.definition ?? null)
const sourceUrl = computed(() => (definitionPath.value ? repoLink.file(definitionPath.value) : null))
const knowledgeUrl = computed(() =>
	detail.value?.knowledgePath ? repoLink.file(detail.value.knowledgePath) : null)

/** `machines/author-ready/stern/x.json` -> `stern/x.json` for a button label. */
const shortPath = (path: string) => path.split('/').slice(-2).join('/')

/** Every mention of the manufacturer filters the catalog by it. */
const manufacturerUrl = computed(() => `/machines?mfr=${encodeURIComponent(manufacturer.value)}`)

const ipdbUrl = computed(() =>
	detail.value?.machine.ipdb_id ? `https://www.ipdb.org/machine.cgi?id=${detail.value.machine.ipdb_id}` : null)
</script>

<template>
	<div class="mx-auto max-w-[100rem] px-4 py-6 sm:px-6">
		<!-- ── header ─────────────────────────────────────────────────────── -->
		<nav class="mb-5 flex items-center gap-1.5 text-xs text-ink-4">
			<NuxtLink to="/machines" class="hover:text-amber">
				Machines
			</NuxtLink>
			<Icon name="lucide:chevron-right" class="size-3" />
			<NuxtLink :to="manufacturerUrl" class="text-ink-3 transition-colors hover:text-amber">
				{{ manufacturer }}
			</NuxtLink>
		</nav>

		<header class="mb-6 flex flex-wrap items-start justify-between gap-x-6 gap-y-4">
			<div class="min-w-0">
				<div class="flex flex-wrap items-center gap-3">
					<h1 class="text-2xl font-semibold tracking-tight text-balance sm:text-3xl">
						{{ name }}
					</h1>
					<StatusChip :status="status" />
				</div>
				<p class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-ink-3">
					<NuxtLink :to="manufacturerUrl" class="inline-flex items-center gap-1.5 transition-colors hover:text-amber">
						<BrandMark :manufacturer="manufacturer" variant="plain" size="sm" />
						{{ manufacturer }}
					</NuxtLink>
					<span v-if="year" class="num">{{ year }}</span>
					<NuxtLink
						v-if="detail?.controller?.platform"
						:to="`/platforms/${platformSlug(detail.controller.platform)}`"
						class="num rounded border border-line px-1.5 py-0.5 text-[11px] transition-colors hover:border-amber/40 hover:text-amber"
					>
						{{ platformShort(detail.controller.platform) }}
					</NuxtLink>
					<span v-if="detail" class="num text-[11px] text-ink-4">{{ detail.machine.id }}</span>
					<NuxtLink
						v-if="detail?.family"
						:to="`/families/${detail.family.slug}`"
						class="inline-flex items-center gap-1.5 rounded border border-amber/25 bg-amber/8 px-1.5 py-0.5 text-[11px] text-amber transition-colors hover:border-amber/50"
					>
						<Icon name="lucide:layers" class="size-3" />
						1 of {{ detail.family.editions }} editions
					</NuxtLink>
				</p>
			</div>

			<div class="flex flex-wrap items-center gap-2">
				<a
					v-if="ipdbUrl"
					:href="ipdbUrl"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center gap-1.5 rounded-lg border border-line px-3 py-1.5 text-[13px] text-ink-2 transition-colors hover:border-amber/40 hover:text-ink"
				>
					<Icon name="lucide:database" class="size-3.5" />
					IPDB
				</a>
				<a
					v-if="knowledgeUrl"
					:href="knowledgeUrl"
					:title="detail!.knowledgePath!"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center gap-1.5 rounded-lg border border-line px-3 py-1.5 text-[13px] text-ink-2 transition-colors hover:border-amber/40 hover:text-ink"
				>
					<Icon name="lucide:notebook-pen" class="size-3.5" />
					<span class="num">{{ shortPath(detail!.knowledgePath!) }}</span>
				</a>
				<a
					v-if="sourceUrl"
					:href="sourceUrl"
					:title="definitionPath!"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center gap-1.5 rounded-lg border border-line px-3 py-1.5 text-[13px] text-ink-2 transition-colors hover:border-amber/40 hover:text-ink"
				>
					<Icon name="lucide:file-json-2" class="size-3.5" />
					<span class="num">{{ shortPath(definitionPath!) }}</span>
				</a>
			</div>
		</header>

		<!-- ── stub state ─────────────────────────────────────────────────── -->
		<template v-if="!detail">
			<div class="panel mx-auto max-w-3xl p-8 text-center">
				<span class="mx-auto grid size-12 place-items-center rounded-xl border border-line bg-raised text-stub">
					<Icon name="lucide:file-question" class="size-5" />
				</span>
				<h2 class="mt-5 text-lg font-semibold">
					Catalogued, not yet described
				</h2>
				<p class="mx-auto mt-2 max-w-xl text-sm leading-relaxed text-ink-3">
					PinMAME supports this machine and the catalog can reach it, but nothing about its playfield has been
					extracted yet — no switch names, no coil functions, no mechanisms. The generated stub exists so the driver is
					never silently missing, and it contributes zero completed coverage.
				</p>
				<div v-if="summary" class="mx-auto mt-6 grid max-w-md grid-cols-2 gap-px overflow-hidden rounded-xl border border-line bg-line">
					<div class="bg-panel px-4 py-3">
						<div class="num text-xl">
							{{ summary.drivers }}
						</div>
						<div class="mt-1 text-[11px] text-ink-3">
							ROM sets waiting
						</div>
					</div>
					<div class="bg-panel px-4 py-3">
						<div class="num text-xl">
							{{ summary.year ?? '—' }}
						</div>
						<div class="mt-1 text-[11px] text-ink-3">
							Year
						</div>
					</div>
				</div>
				<div v-if="summary?.roms?.length" class="mt-6 text-left">
					<div class="eyebrow mb-2 text-center">
						ROM sets that resolve here
					</div>
					<div class="flex flex-wrap justify-center gap-1.5">
						<span
							v-for="rom in summary.roms"
							:key="rom"
							class="num rounded-md border border-line bg-raised px-1.5 py-1 text-[11px] text-ink-3"
						>{{ rom }}</span>
					</div>
				</div>
				<div class="mt-6 flex flex-wrap justify-center gap-3">
					<NuxtLink to="/coverage" class="text-sm text-amber hover:underline">
						See the curation queue
					</NuxtLink>
					<span class="text-ink-4">·</span>
					<NuxtLink to="/machines?status=author_ready" class="text-sm text-amber hover:underline">
						Browse complete machines
					</NuxtLink>
				</div>
			</div>

			<ContributeCard
				class="mx-auto mt-6 max-w-3xl"
				tone="author"
				:definition-path="definitionPath"
				:subject="name"
			/>
		</template>

		<!-- ── full definition ────────────────────────────────────────────── -->
		<div v-else class="grid gap-8 xl:grid-cols-[13rem_minmax(0,1fr)]">
			<!-- section rail -->
			<aside class="hidden xl:block">
				<nav class="sticky top-20 space-y-0.5">
					<a
						v-for="section in sections"
						:key="section.id"
						:href="`#${section.id}`"
						class="flex items-center gap-2.5 rounded-lg px-2.5 py-1.5 text-[13px] transition-colors"
						:class="activeSection === section.id ? 'bg-raised text-ink' : 'text-ink-3 hover:text-ink'"
					>
						<Icon :name="section.icon" class="size-3.5 shrink-0" :class="activeSection === section.id ? 'text-amber' : ''" />
						<span class="truncate">{{ section.label }}</span>
						<span v-if="section.count" class="num ml-auto text-[10px] text-ink-4">{{ section.count }}</span>
					</a>

					<div v-if="usedCount.used || usedCount.unused" class="mt-5 border-t border-line pt-4">
						<div class="eyebrow mb-2">
							Address health
						</div>
						<dl class="space-y-1 text-[11px]">
							<div class="flex justify-between">
								<dt class="text-ink-4">
									Used
								</dt>
								<dd class="num text-ready">
									{{ usedCount.used }}
								</dd>
							</div>
							<div class="flex justify-between">
								<dt class="text-ink-4">
									Unused
								</dt>
								<dd class="num text-ink-3">
									{{ usedCount.unused }}
								</dd>
							</div>
							<div v-if="usedCount.optional" class="flex justify-between">
								<dt class="text-ink-4">
									Optional
								</dt>
								<dd class="num text-partial">
									{{ usedCount.optional }}
								</dd>
							</div>
						</dl>
					</div>
				</nav>
			</aside>

			<div class="min-w-0 space-y-10">
				<!-- conflicts first: they change what an author should trust -->
				<div v-if="detail.conflicts.length" class="rounded-panel border border-alert/35 bg-panel p-4">
					<div class="flex items-center gap-2">
						<Icon name="lucide:triangle-alert" class="size-4 text-alert" />
						<h2 class="text-sm font-semibold text-alert">
							{{ detail.conflicts.length }} unresolved conflict{{ detail.conflicts.length === 1 ? '' : 's' }}
						</h2>
					</div>
					<ul class="mt-3 space-y-2">
						<li v-for="conflict in detail.conflicts" :key="conflict.id" class="text-[13px] leading-relaxed text-ink-2">
							{{ conflict.description }}
							<span v-if="conflict.path" class="num ml-1 text-[11px] text-ink-4">{{ conflict.path }}</span>
						</li>
					</ul>
				</div>

				<section id="setup" class="scroll-mt-20">
					<SetupPanel :machine="detail" />
				</section>

				<section v-if="placements" id="playfield" class="scroll-mt-20">
					<header class="mb-3">
						<h2 class="text-xl font-semibold tracking-tight">
							Playfield
						</h2>
						<p class="mt-1 max-w-3xl text-sm text-ink-3">
							Where each address physically sits. The switch and lamp maps below show the electrical layout — this
							shows the same devices as the player sees them.
						</p>
					</header>
					<PlayfieldMap
						:devices="[...detail.inputs, ...detail.outputs]"
						:highlight="selected"
						@select="select"
					/>
				</section>

				<section id="coverage" class="scroll-mt-20">
					<h2 class="mb-3 text-xl font-semibold tracking-tight">
						Coverage
					</h2>
					<CoveragePanel :status="detail.coverage.status" :dimensions="detail.coverage.dimensions" :missing="detail.coverage.missing" />
				</section>

				<section v-if="switches.length" id="switches" class="scroll-mt-20 space-y-4">
					<header class="flex flex-wrap items-end justify-between gap-3">
						<div>
							<h2 class="text-xl font-semibold tracking-tight">
								Switches
							</h2>
							<p class="mt-1 text-sm text-ink-3">
								The addresses PinMAME reports as closed. Numbers are the public API values, not matrix hardware pins.
							</p>
						</div>
						<span class="num text-xs text-ink-4">{{ switches.length }} addresses</span>
					</header>
					<AddressMatrix :devices="switches" label="Switch map" @pick="select" />
					<DeviceTable :devices="switches" direction="input" :highlight="selected" />
				</section>

				<section v-if="detail.outputs.length" id="outputs" class="scroll-mt-20 space-y-8">
					<header>
						<h2 class="text-xl font-semibold tracking-tight">
							Controlled devices
						</h2>
						<p class="mt-1 text-sm text-ink-3">
							Everything the ROM can energise, grouped the way a table author builds it.
						</p>
					</header>

					<div v-for="group in outputGroups" :key="group.id" class="space-y-3">
						<div class="flex items-center gap-3">
							<h3 class="text-base font-semibold">
								{{ group.label }}
							</h3>
							<span class="num text-sm text-ink-4">{{ group.devices.length }}</span>
							<div class="h-px flex-1 bg-line" />
						</div>
						<AddressMatrix v-if="group.matrix && group.devices.length > 16" :devices="group.devices" label="Lamp map" @pick="select" />
						<DeviceTable :devices="group.devices" direction="output" :highlight="selected" />
					</div>
				</section>

				<section v-if="dips.length || otherInputs.length" class="scroll-mt-20 space-y-3">
					<div class="flex items-center gap-3">
						<h3 class="text-base font-semibold">
							Configuration & other inputs
						</h3>
						<div class="h-px flex-1 bg-line" />
					</div>
					<DeviceTable :devices="[...dips, ...otherInputs]" direction="input" :highlight="selected" />
				</section>

				<section v-if="detail.mechanisms.length" id="mechanisms" class="scroll-mt-20">
					<header class="mb-3">
						<h2 class="text-xl font-semibold tracking-tight">
							Mechanisms
						</h2>
						<p class="mt-1 text-sm text-ink-3">
							Logical assemblies with their actuators, sensors and observed behaviour. Click a chip to jump to the
							address it refers to.
						</p>
					</header>
					<div class="grid gap-3 lg:grid-cols-2">
						<MechanismCard
							v-for="mechanism in detail.mechanisms"
							:key="mechanism.id"
							:mechanism="mechanism"
							:device-by-id="deviceById"
						/>
					</div>
				</section>

				<section v-if="detail.relationships.length" id="wiring" class="scroll-mt-20">
					<header class="mb-3">
						<h2 class="text-xl font-semibold tracking-tight">
							Direct wiring
						</h2>
						<p class="mt-1 text-sm text-ink-3">
							Connections that exist in copper, not in the ROM. These fire whether or not a game is running.
						</p>
					</header>
					<RelationshipMap :relationships="detail.relationships" :device-by-id="deviceById" />
				</section>

				<section v-if="detail.knowledgeHtml" id="notes" class="scroll-mt-20">
					<header class="mb-3 flex flex-wrap items-end justify-between gap-3">
						<div>
							<h2 class="text-xl font-semibold tracking-tight">
								Recreation notes
							</h2>
							<p class="mt-1 text-sm text-ink-3">
								Working knowledge that has no schema field yet — edition differences, tuning values, pitfalls.
							</p>
						</div>
					</header>
					<div class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_14rem]">
						<div class="min-w-0 space-y-3">
							<!-- the note's own `Coverage: **…**` lead-in, lifted out of the
							     prose so it reads as a summary rather than a stray sentence -->
							<dl v-if="detail.knowledgeSummary.length" class="panel divide-y divide-line-soft overflow-hidden">
								<div
									v-for="(item, index) in detail.knowledgeSummary"
									:key="item.label"
									class="flex flex-wrap items-baseline gap-x-3 gap-y-1 px-4 py-3"
								>
									<dt class="eyebrow w-full sm:w-auto sm:shrink-0">
										{{ item.label }}
									</dt>
									<dd class="flex min-w-0 flex-1 items-baseline gap-2 text-[13px] leading-relaxed">
										<span
											v-if="index === 0"
											class="mt-1.5 size-1.5 shrink-0 rounded-full"
											:style="{ background: STATUS_META[detail!.coverage.status].color }"
										/>
										<span :class="index === 0 ? 'text-ink' : 'text-ink-2'">{{ item.value }}</span>
									</dd>
								</div>
							</dl>

							<article class="knowledge panel min-w-0 p-5 sm:p-6" v-html="detail.knowledgeHtml" />
						</div>
						<nav v-if="detail.knowledgeHeadings.length" class="hidden lg:block">
							<div class="sticky top-20">
								<div class="eyebrow mb-2">
									In this note
								</div>
								<ul class="space-y-1 border-l border-line">
									<li v-for="heading in detail.knowledgeHeadings" :key="heading.id">
										<a :href="`#${heading.id}`" class="-ml-px block border-l border-transparent py-1 pl-3 text-xs text-ink-3 transition-colors hover:border-amber hover:text-ink">
											{{ heading.text }}
										</a>
									</li>
								</ul>
							</div>
						</nav>
					</div>
				</section>

				<section id="roms" class="scroll-mt-20">
					<header class="mb-3">
						<h2 class="text-xl font-semibold tracking-tight">
							ROM sets
						</h2>
						<p class="mt-1 text-sm text-ink-3">
							Every driver that resolves to this physical machine.
						</p>
					</header>
					<DriverTable :drivers="detail.drivers" :catalog-drivers="detail.catalogDrivers" />
				</section>

				<section v-if="detail.sources.length" id="sources" class="scroll-mt-20">
					<header class="mb-3">
						<h2 class="text-xl font-semibold tracking-tight">
							Evidence
						</h2>
						<p class="mt-1 max-w-3xl text-sm text-ink-3">
							Every claim above traces to one of these. When they disagree: a known-working VPX script wins on
							controller addresses and causality, the manual wins on wiring and construction, pinned PinMAME wins on
							emulator routing and display layout.
						</p>
					</header>
					<SourceList :sources="detail.sources" />
				</section>

				<ContributeCard
					:definition-path="definitionPath"
					:knowledge-path="detail.knowledgePath"
					:subject="name"
					:hint="detail.coverage.missing.length
						? `This definition still has ${detail.coverage.missing.length} unmet requirement${detail.coverage.missing.length === 1 ? '' : 's'}, listed under Coverage above. Fixes belong in the definition itself — editing on GitHub forks it for you and opens the pull request.`
						: null"
				/>

				<section v-if="detail.family" class="scroll-mt-20">
					<header class="mb-3">
						<h2 class="text-xl font-semibold tracking-tight">
							Other editions
						</h2>
						<p class="mt-1 max-w-3xl text-sm text-ink-3">
							{{ detail.family.title }} shipped in {{ detail.family.editions }} editions with different playfields.
							Compare what each one actually has before building against this definition.
						</p>
						<p v-if="detail.family.differences" class="mt-2 max-w-3xl text-[13px] leading-relaxed text-ink-2">
							{{ detail.family.differences }}
						</p>
					</header>
					<NuxtLink
						:to="`/families/${detail.family.slug}`"
						class="panel group flex items-center gap-3 px-4 py-3 transition-colors hover:border-amber/35"
					>
						<Icon name="lucide:layers" class="size-4 shrink-0 text-amber" />
						<span class="min-w-0 flex-1 text-[13px] transition-colors group-hover:text-amber">
							All {{ detail.family.editions }} editions of {{ detail.family.title }}, side by side
						</span>
						<Icon name="lucide:arrow-right" class="size-3.5 shrink-0 text-ink-4" />
					</NuxtLink>
				</section>

				<section v-if="detail.related?.length">
					<header class="mb-3">
						<h2 class="text-xl font-semibold tracking-tight">
							Same platform
						</h2>
					</header>
					<div class="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
						<NuxtLink
							v-for="item in detail.related"
							:key="item.slug"
							:to="`/machines/${item.slug}`"
							class="panel group flex items-center gap-3 px-3 py-2.5 transition-colors hover:border-amber/35"
						>
							<StatusChip :status="item.status" dot-only />
							<span class="min-w-0 flex-1">
								<span class="block truncate text-[13px] transition-colors group-hover:text-amber">{{ item.name }}</span>
								<span class="block truncate text-[11px] text-ink-4">{{ item.manufacturer }} · {{ item.year }}</span>
							</span>
							<Icon name="lucide:chevron-right" class="size-3.5 shrink-0 text-ink-4" />
						</NuxtLink>
					</div>
				</section>
			</div>
		</div>
	</div>
</template>
