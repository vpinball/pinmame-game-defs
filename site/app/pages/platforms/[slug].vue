<script setup lang="ts">
const route = useRoute()
const platforms = usePlatforms()
const repoLink = useRepoLink()

const platform = computed(() => platforms.find(p => p.slug === route.params.slug))

if (!platform.value) {
	throw createError({ statusCode: 404, statusMessage: 'Platform not found', fatal: true })
}

useSeo({
	title: () => platform.value?.hardwareFamily ?? platform.value?.id ?? 'Platform',
	description: () => platform.value?.profile
		? `${platform.value.hardwareFamily ?? platform.value.id} controller profile: legal address ranges, LibPinMAME transports and the normalisation PinMAME applies, across ${platform.value.machines} machines.`
		: `${platform.value?.id} is referenced by ${platform.value?.machines ?? 0} machines but has no authored controller profile yet.`,
})

const DIRECTION_META: Record<string, { label: string, color: string, icon: string }> = {
	input: { label: 'Input', color: 'var(--color-k-switch)', icon: 'lucide:arrow-down-to-line' },
	controlled_device: { label: 'Controlled device', color: 'var(--color-k-coil)', icon: 'lucide:arrow-up-from-line' },
	configuration: { label: 'Configuration', color: 'var(--color-k-dip)', icon: 'lucide:sliders-horizontal' },
	display: { label: 'Display', color: 'var(--color-k-display)', icon: 'lucide:monitor' },
}

function ruleText(rule: { minimum?: number, maximum?: number, values?: number[] }) {
	if (rule.values) return rule.values.join(', ')
	if (rule.minimum === rule.maximum) return String(rule.minimum)
	return `${rule.minimum} … ${rule.maximum}`
}

/** A missing profile has no file yet, so point at GitHub's new-file form. */
const authorProfileUrl = computed(() =>
	repoLink.create('controllers/pinmame', `${(platform.value?.id ?? '').replace(/^pinmame\./, '')}.json`))

function ruleSize(rule: { minimum?: number, maximum?: number, values?: number[] }) {
	if (rule.values) return rule.values.length
	return (rule.maximum ?? 0) - (rule.minimum ?? 0) + 1
}
</script>

<template>
	<div v-if="platform" class="mx-auto max-w-5xl px-4 py-8 sm:px-6">
		<nav class="mb-5 flex items-center gap-1.5 text-xs text-ink-4">
			<NuxtLink to="/platforms" class="hover:text-amber">
				Platforms
			</NuxtLink>
			<Icon name="lucide:chevron-right" class="size-3" />
			<span class="num text-ink-3">{{ platform.id }}</span>
		</nav>

		<header class="mb-8">
			<div class="flex flex-wrap items-start justify-between gap-4">
				<div class="flex min-w-0 items-center gap-4">
					<BrandMark :platform="platform.id" size="lg" />
					<div class="min-w-0">
					<h1 class="text-2xl font-semibold tracking-tight sm:text-3xl">
						{{ platform.hardwareFamily ?? platformShort(platform.id) }}
					</h1>
					<p class="num mt-2 text-sm text-ink-3">
						{{ platform.id }}
					</p>
					</div>
				</div>
				<a
					v-if="platform.sourcePath"
					:href="repoLink.file(platform.sourcePath)"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center gap-1.5 rounded-lg border border-line px-3 py-1.5 text-[13px] text-ink-2 transition-colors hover:border-amber/40 hover:text-ink"
				>
					<Icon name="lucide:file-json-2" class="size-3.5" />
					<span class="num">{{ platform.sourcePath }}</span>
				</a>
			</div>

			<dl class="mt-6 grid max-w-xl grid-cols-3 gap-px overflow-hidden rounded-xl border border-line bg-line">
				<div class="bg-panel px-4 py-3">
					<dd class="num text-xl leading-none">
						{{ platform.machines }}
					</dd>
					<dt class="mt-1.5 text-[11px] text-ink-3">
						Machines
					</dt>
				</div>
				<div class="bg-panel px-4 py-3">
					<dd class="num text-xl leading-none text-ready">
						{{ platform.authorReady }}
					</dd>
					<dt class="mt-1.5 text-[11px] text-ink-3">
						Author ready
					</dt>
				</div>
				<div class="bg-panel px-4 py-3">
					<dd class="num text-xl leading-none">
						{{ platform.groupCount || '—' }}
					</dd>
					<dt class="mt-1.5 text-[11px] text-ink-3">
						Address groups
					</dt>
				</div>
			</dl>
		</header>

		<div v-if="!platform.profile" class="panel p-8 text-center">
			<span class="mx-auto grid size-11 place-items-center rounded-xl border border-line bg-raised text-ink-4">
				<Icon name="lucide:file-question" class="size-5" />
			</span>
			<h2 class="mt-4 text-base font-semibold">
				No profile authored yet
			</h2>
			<p class="mx-auto mt-2 max-w-lg text-sm leading-relaxed text-ink-3">
				Definitions already reference this platform, but its address ranges, transports and normalisation rules have not
				been written down. Until they are, treat address bounds on those machines as observed rather than validated.
			</p>
			<a
				:href="authorProfileUrl"
				target="_blank"
				rel="noopener noreferrer"
				class="mt-5 inline-flex items-center gap-2 rounded-lg bg-amber px-3.5 py-2.5 text-[13px] font-medium text-void transition-transform hover:-translate-y-0.5"
			>
				<Icon name="lucide:git-pull-request-arrow" class="size-4" />
				Author this profile
			</a>
			<p class="mt-3 text-[11px] text-ink-4">
				Opens a new file in
				<span class="num">controllers/pinmame/</span> on GitHub — it forks for you and lands on the pull request.
			</p>
		</div>

		<template v-else>
			<div
				v-if="platform.profile.inversion_applied_by_emulator"
				class="mb-8 flex gap-3 rounded-panel border border-line bg-panel p-4"
			>
				<Icon name="lucide:shield-check" class="mt-0.5 size-4 shrink-0 text-amber" />
				<div>
					<h2 class="text-sm font-semibold">
						Polarity is already normalised
					</h2>
					<p class="mt-1 text-[13px] leading-relaxed text-ink-3">
						PinMAME reports logical active state on this platform. A consumer must not invert again. Whether a real
						switch is normally closed stays recorded per device as a physical fact, so a recreation can build the right
						hardware without changing what the emulator reports.
					</p>
				</div>
			</div>

			<section class="space-y-4">
				<h2 class="text-lg font-semibold tracking-tight">
					Address groups
				</h2>

				<article v-for="group in platform.profile.groups" :key="group.id" class="panel overflow-hidden">
					<header class="flex flex-wrap items-center gap-3 border-b border-line px-5 py-3">
						<span
							class="grid size-7 shrink-0 place-items-center rounded-md border"
							:style="{
								color: DIRECTION_META[group.direction]?.color ?? 'var(--color-ink-3)',
								borderColor: `color-mix(in srgb, ${DIRECTION_META[group.direction]?.color ?? 'var(--color-ink-3)'} 30%, transparent)`,
							}"
						>
							<Icon :name="DIRECTION_META[group.direction]?.icon ?? 'lucide:circle'" class="size-3.5" />
						</span>
						<div class="min-w-0">
							<h3 class="text-sm font-semibold">
								{{ group.label }}
							</h3>
							<p class="num mt-0.5 text-[11px] text-ink-4">
								{{ group.id }}
							</p>
						</div>
						<span class="ml-auto flex items-center gap-2">
							<KindChip :kind="group.kind" />
						</span>
					</header>

					<div class="grid gap-px bg-line md:grid-cols-2">
						<div class="bg-panel p-5">
							<div class="eyebrow mb-3">
								Legal addresses
							</div>
							<ul class="space-y-1.5">
								<li v-for="(rule, i) in group.address_rules ?? []" :key="i" class="flex items-baseline gap-3">
									<span class="num text-sm text-ink">{{ ruleText(rule) }}</span>
									<span class="num text-[11px] text-ink-4">{{ ruleSize(rule) }} slot{{ ruleSize(rule) === 1 ? '' : 's' }}</span>
								</li>
								<li v-if="!group.address_rules?.length" class="text-sm text-ink-4">
									Unconstrained
								</li>
							</ul>
						</div>

						<div class="bg-panel p-5">
							<div class="eyebrow mb-3">
								Transports
							</div>
							<ul v-if="Object.keys(group.transports ?? {}).length" class="space-y-2">
								<li v-for="(config, name) in group.transports" :key="name" class="text-[13px]">
									<span class="num text-ink">{{ name }}</span>
									<span class="num ml-2 text-[11px] text-ink-3">
										{{ Object.entries(config).map(([k, v]) => `${k}=${String(v).slice(0, 12)}`).join(' · ') }}
									</span>
								</li>
							</ul>
							<p v-else class="text-[13px] text-ink-4">
								No stable transport — these are physical identities the public API does not carry.
							</p>
						</div>
					</div>

					<p v-if="group.notes" class="border-t border-line px-5 py-3 text-[13px] leading-relaxed text-ink-2">
						{{ group.notes }}
					</p>
				</article>
			</section>

			<section v-if="platform.profile.sources?.length" class="mt-10">
				<h2 class="mb-3 text-lg font-semibold tracking-tight">
					Evidence
				</h2>
				<SourceList :sources="platform.profile.sources" />
			</section>
		</template>

		<ContributeCard
			v-if="platform.sourcePath"
			class="mt-10"
			:definition-path="platform.sourcePath"
			:subject="platform.id"
			hint="Address ranges, transports and normalisation rules live in one profile file. If PinMAME exposes a group this profile does not describe — or describes wrongly — the fix belongs there."
		/>

		<section v-if="platform.examples.length" class="mt-10">
			<h2 class="mb-3 text-lg font-semibold tracking-tight">
				Machines on this platform
			</h2>
			<div class="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
				<NuxtLink
					v-for="example in platform.examples"
					:key="example.slug"
					:to="`/machines/${example.slug}`"
					class="panel group flex items-center gap-3 px-3 py-2.5 transition-colors hover:border-amber/35"
				>
					<span class="min-w-0 flex-1 truncate text-[13px] transition-colors group-hover:text-amber">{{ example.name }}</span>
					<Icon name="lucide:chevron-right" class="size-3.5 shrink-0 text-ink-4" />
				</NuxtLink>
			</div>
			<NuxtLink :to="`/machines?platform=${platform.id}`" class="mt-3 inline-flex items-center gap-1.5 text-sm text-amber hover:underline">
				All {{ platform.machines }} machines
				<Icon name="lucide:arrow-right" class="size-3.5" />
			</NuxtLink>
		</section>
	</div>
</template>
