<script setup lang="ts">
const site = useSite()
const repoLink = useRepoLink()
const generated = computed(() => new Date(site.generatedAt).toISOString().slice(0, 16).replace('T', ' '))
</script>

<template>
	<!--
		No top margin of its own: it stacked on top of the last section's bottom
		padding, so every page ended with far more space below its content than
		above it. Each page's own `py-*` now sets that gap, symmetrically.
	-->
	<footer class="border-t border-line">
		<div class="mx-auto grid max-w-[100rem] gap-8 px-4 py-10 sm:px-6 md:grid-cols-[2fr_1fr_1fr]">
			<div>
				<p class="text-sm font-semibold">
					PinMAME Machine Reference
				</p>
				<p class="mt-2 max-w-md text-xs leading-relaxed text-ink-3">
					A browsable view of the
					<a :href="repoLink.dir('machines')" target="_blank" rel="noopener noreferrer" class="num text-amber hover:underline">pinmame-game-defs</a>
					catalog: the switches, lamps,
					coils, displays and mechanisms needed to recreate a PinMAME-supported machine. Canonical machine facts come
					from that repository; build-time external data is labeled, pinned and attributed separately.
				</p>
				<p class="mt-3 text-xs">
					<NuxtLink to="/about" class="text-amber hover:underline">About this project</NuxtLink>
				</p>
			</div>

			<div>
				<div class="eyebrow mb-3">
					Browse
				</div>
				<ul class="space-y-1.5 text-xs text-ink-3">
					<li><NuxtLink to="/machines" class="hover:text-amber">All machines</NuxtLink></li>
					<li><NuxtLink to="/roms" class="hover:text-amber">ROM set lookup</NuxtLink></li>
					<li><NuxtLink to="/platforms" class="hover:text-amber">Controller platforms</NuxtLink></li>
					<li><NuxtLink to="/coverage" class="hover:text-amber">Coverage report</NuxtLink></li>
					<li><NuxtLink to="/guide" class="hover:text-amber">Reading a definition</NuxtLink></li>
					<li>
						<a :href="repoLink.file('catalog/pinmame.json')" target="_blank" rel="noopener noreferrer" class="num hover:text-amber">catalog/pinmame.json</a>
					</li>
					<li>
						<a :href="repoLink.dir('machines')" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 text-amber hover:underline">
							<Icon name="lucide:git-pull-request-arrow" class="size-3.5" />
							Contribute a correction
						</a>
					</li>
				</ul>
			</div>

			<div>
				<div class="eyebrow mb-3">
					Build
				</div>
				<dl class="space-y-1.5 text-xs">
					<div class="flex justify-between gap-3">
						<dt class="text-ink-4">
							PinMAME
						</dt>
						<dd>
							<a :href="repoLink.pinmame(site.pinmameRevision)" target="_blank" rel="noopener noreferrer" class="num text-ink-3 hover:text-amber">{{ shortHash(site.pinmameRevision) }}</a>
						</dd>
					</div>
					<div class="flex justify-between gap-3">
						<dt class="text-ink-4">
							libpinmame
						</dt>
						<dd class="num text-ink-3">{{ site.libraryVersion }}</dd>
					</div>
					<div class="flex justify-between gap-3">
						<dt class="text-ink-4">
							Schema
						</dt>
						<dd>
							<a :href="repoLink.file('docs/MACHINE_DEFINITIONS_PLAN.md')" target="_blank" rel="noopener noreferrer" class="num text-ink-3 hover:text-amber">v{{ site.schemaVersion }}</a>
						</dd>
					</div>
					<div class="flex justify-between gap-3">
						<dt class="text-ink-4">
							Generated
						</dt>
						<dd class="num text-ink-3">{{ generated }}</dd>
					</div>
				</dl>
			</div>
		</div>

		<div class="border-t border-line px-4 py-4 text-center text-[11px] text-ink-4 sm:px-6">
			Definitions are BSD-3-Clause where derived from PinMAME; manual and table sources keep their own attribution.
			Nothing here redistributes ROMs.
		</div>
	</footer>
</template>
