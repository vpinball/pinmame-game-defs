<script setup lang="ts">
useSeo({
	title: 'About',
	description: 'How a freezy side project, evidence-backed AI curation and spare inference are turning PinMAME machine data into better tooling for VPE table authors.',
})

const repoLink = useRepoLink()
</script>

<template>
	<div class="mx-auto max-w-[100rem] px-4 py-8 sm:px-6">
		<header class="max-w-3xl">
			<div class="eyebrow mb-3">
				About
			</div>
			<h1 class="text-2xl font-semibold tracking-tight sm:text-3xl">
				A small side project with a large switch matrix
			</h1>
			<p class="mt-4 text-[15px] leading-relaxed text-ink-2">
				This project is one of <a href="https://github.com/freezy" target="_blank" rel="noopener noreferrer" class="text-amber hover:underline">freezy</a>’s side projects. It began with a practical observation: VPE can offer table authors much better tools when it knows what is connected to each switch, lamp and coil. The premise is small; the number of machines is less so.
			</p>
		</header>

		<div class="mt-10 grid gap-5 lg:grid-cols-3">
			<section class="panel p-6">
				<div class="eyebrow mb-3">
					What it enables
				</div>
				<h2 class="text-lg font-semibold tracking-tight">
					Better data, better authoring tools
				</h2>
				<p class="mt-3 text-[14px] leading-relaxed text-ink-2">
					A trustworthy machine definition will let VPE resolve ROMs, populate managers, map switches, lamps and coils, understand mechanisms, and suggest spatial assignments. The aim is to save table authors from repeatedly transcribing information that can be shared once.
				</p>
			</section>

			<section class="panel p-6">
				<div class="eyebrow mb-3">
					How it is made
				</div>
				<h2 class="text-lg font-semibold tracking-tight">
					AI handles much of the repetitive work
				</h2>
				<p class="mt-3 text-[14px] leading-relaxed text-ink-2">
					Most of this catalog is created and curated with AI agents. Repetitive extraction, large comparisons, address-by-address bookkeeping and cross-referencing are a good fit for them. They can work through the long lists; people can concentrate on judgment and the awkward exceptions.
				</p>
			</section>

			<section class="panel p-6">
				<div class="eyebrow mb-3">
					How it stays useful
				</div>
				<h2 class="text-lg font-semibold tracking-tight">
					Evidence before confidence
				</h2>
				<p class="mt-3 text-[14px] leading-relaxed text-ink-2">
					AI can also be confidently wrong. To keep hallucinations from becoming catalog entries, facts are tied to manuals, PinMAME source, known-working VPX scripts or runtime observations. Unknowns stay unknown, disagreements remain visible, and claims carry enough evidence for someone else to check them.
				</p>
			</section>
		</div>

		<section class="panel mt-6 overflow-hidden">
			<div class="grid gap-6 p-6 md:grid-cols-[minmax(0,1fr)_auto] md:items-center">
				<div class="max-w-3xl">
					<div class="eyebrow mb-3">
						Contributions welcome
					</div>
					<h2 class="text-lg font-semibold tracking-tight">
						Spare inference has a useful home
					</h2>
					<p class="mt-2 text-[14px] leading-relaxed text-ink-2">
						Anyone with spare inference is invited to help make the database more complete. Pick a stub or partial machine, point an agent at the contribution workflow, require sources for its claims, and send the result as a pull request. The repetitive work can be delegated; contributors and reviewers still make the final calls.
					</p>
				</div>
				<div class="flex flex-wrap gap-3 md:justify-end">
					<NuxtLink to="/coverage" class="rounded-lg bg-amber px-4 py-2 text-sm font-medium text-void transition-opacity hover:opacity-90">
						Find a machine to improve
					</NuxtLink>
					<a :href="repoLink.file('CONTRIBUTING.md')" target="_blank" rel="noopener noreferrer" class="rounded-lg border border-line px-4 py-2 text-sm text-ink-2 transition-colors hover:border-amber/35 hover:text-ink">
						Contribution guide
					</a>
				</div>
			</div>
		</section>
	</div>
</template>
