<script setup lang="ts">
useSeo({
	title: 'Controller platforms',
	description: 'Controller profiles for every PinMAME hardware family: legal address ranges, transports, and the normalisation the emulator applies before you see a value.',
})

const platforms = usePlatforms()
const site = useSite()

const sorted = computed(() =>
	platforms.slice().sort((a, b) => Number(b.hasProfile) - Number(a.hasProfile) || b.machines - a.machines))
</script>

<template>
	<div class="mx-auto max-w-[100rem] px-4 py-8 sm:px-6">
		<header class="mb-6">
			<h1 class="text-2xl font-semibold tracking-tight">
				Controller platforms
			</h1>
			<p class="mt-1.5 max-w-3xl text-sm text-ink-3">
				A platform profile says how PinMAME exposes a hardware family: which address ranges are legal, what each group
				transports over LibPinMAME, and what the emulator normalises before you ever see a value. Machines bind to a
				profile instead of repeating transport knowledge on every device.
			</p>
			<p class="mt-3 text-xs text-ink-4">
				{{ site.counts.profiles }} of {{ platforms.length }} platforms have an authored profile — the rest are referenced
				by definitions but not yet described.
			</p>
		</header>

		<div class="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
			<NuxtLink
				v-for="platform in sorted"
				:key="platform.id"
				:to="`/platforms/${platform.slug}`"
				class="panel group flex min-w-0 flex-col p-5 transition-colors hover:border-amber/35"
				:class="platform.hasProfile ? '' : 'opacity-70'"
			>
				<div class="flex items-start justify-between gap-3">
					<BrandMark :platform="platform.id" size="sm" class="mt-0.5" />
					<div class="min-w-0 flex-1">
						<h2 class="text-[15px] font-semibold text-balance transition-colors group-hover:text-amber">
							{{ platform.hardwareFamily ?? platformShort(platform.id) }}
						</h2>
						<p class="num mt-0.5 text-[11px] break-all text-ink-4">
							{{ platform.id }}
						</p>
					</div>
					<span
						v-if="platform.hasProfile"
						class="num shrink-0 rounded border border-ready/25 bg-ready/8 px-1.5 py-0.5 text-[10px] text-ready"
					>profile</span>
					<span v-else class="shrink-0 rounded border border-line px-1.5 py-0.5 text-[10px] text-ink-4">pending</span>
				</div>

				<dl class="mt-5 flex gap-5">
					<div>
						<dd class="num text-lg leading-none">
							{{ platform.machines }}
						</dd>
						<dt class="mt-1 text-[10px] text-ink-4">
							machines
						</dt>
					</div>
					<div>
						<dd class="num text-lg leading-none text-ready">
							{{ platform.authorReady }}
						</dd>
						<dt class="mt-1 text-[10px] text-ink-4">
							ready
						</dt>
					</div>
					<div v-if="platform.groupCount">
						<dd class="num text-lg leading-none">
							{{ platform.groupCount }}
						</dd>
						<dt class="mt-1 text-[10px] text-ink-4">
							groups
						</dt>
					</div>
				</dl>

				<p v-if="platform.examples.length" class="mt-4 truncate text-[11px] text-ink-4">
					{{ platform.examples.map(e => e.name).join(' · ') }}
				</p>
			</NuxtLink>
		</div>
	</div>
</template>
