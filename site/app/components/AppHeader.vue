<script setup lang="ts">
const searchOpen = defineModel<boolean>('searchOpen', { default: false })
const { theme, toggle } = useTheme()
const mobileOpen = ref(false)
const route = useRoute()

const links = [
	{ to: '/machines', label: 'Machines' },
	{ to: '/roms', label: 'ROM sets' },
	{ to: '/platforms', label: 'Platforms' },
	{ to: '/coverage', label: 'Coverage' },
	{ to: '/guide', label: 'Guide' },
	{ to: '/schema', label: 'Schema' },
]

const isActive = (to: string) => route.path === to || route.path.startsWith(`${to}/`)

watch(() => route.fullPath, () => { mobileOpen.value = false })

const isMac = ref(false)
onMounted(() => {
	isMac.value = /mac/i.test(navigator.platform || navigator.userAgent)
})
</script>

<template>
	<header class="sticky top-0 z-50 border-b border-line bg-canvas/85 backdrop-blur-xl">
		<div class="mx-auto flex h-14 max-w-[100rem] items-center gap-4 px-4 sm:px-6">
			<NuxtLink to="/" class="flex shrink-0 items-center gap-2.5" aria-label="Home">
				<svg width="26" height="26" viewBox="0 0 26 26" fill="none" aria-hidden="true">
					<rect x="0.75" y="0.75" width="24.5" height="24.5" rx="6" stroke="var(--color-line)" />
					<g fill="var(--color-amber)">
						<circle cx="7" cy="8" r="1.6" /><circle cx="13" cy="8" r="1.6" /><circle cx="19" cy="8" r="1.6" opacity="0.35" />
						<circle cx="7" cy="13" r="1.6" opacity="0.35" /><circle cx="13" cy="13" r="1.6" /><circle cx="19" cy="13" r="1.6" />
						<circle cx="7" cy="18" r="1.6" /><circle cx="13" cy="18" r="1.6" opacity="0.35" /><circle cx="19" cy="18" r="1.6" />
					</g>
				</svg>
				<span class="hidden text-[13px] leading-none font-semibold tracking-tight sm:block">
					PinMAME<span class="text-ink-3"> Machine Reference</span>
				</span>
			</NuxtLink>

			<nav class="hidden items-center gap-0.5 md:flex">
				<NuxtLink
					v-for="link in links"
					:key="link.to"
					:to="link.to"
					class="rounded-lg px-2.5 py-1.5 text-[13px] transition-colors"
					:class="isActive(link.to) ? 'bg-raised text-ink' : 'text-ink-3 hover:text-ink'"
				>
					{{ link.label }}
				</NuxtLink>
			</nav>

			<div class="ml-auto flex items-center gap-2">
				<button
					type="button"
					class="flex items-center gap-2 rounded-lg border border-line bg-raised py-1.5 pr-1.5 pl-2.5 text-ink-3 transition-colors hover:border-amber/35 hover:text-ink"
					@click="searchOpen = true"
				>
					<Icon name="lucide:search" class="size-3.5" />
					<span class="hidden text-[13px] sm:block">Search</span>
					<kbd class="num hidden rounded border border-line px-1.5 py-0.5 text-[10px] sm:block">{{ isMac ? '⌘' : 'Ctrl ' }}K</kbd>
				</button>

				<button
					type="button"
					class="grid size-8 place-items-center rounded-lg border border-line text-ink-3 transition-colors hover:text-ink"
					:aria-label="`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`"
					@click="toggle"
				>
					<Icon :name="theme === 'dark' ? 'lucide:sun' : 'lucide:moon'" class="size-4" />
				</button>

				<a
					href="https://github.com/vpinball/pinmame-game-defs"
					target="_blank"
					rel="noopener noreferrer"
					class="hidden size-8 place-items-center rounded-lg border border-line text-ink-3 transition-colors hover:text-ink sm:grid"
					aria-label="Repository"
				>
					<Icon name="lucide:github" class="size-4" />
				</a>

				<button
					type="button"
					class="grid size-8 place-items-center rounded-lg border border-line text-ink-3 md:hidden"
					aria-label="Menu"
					@click="mobileOpen = !mobileOpen"
				>
					<Icon :name="mobileOpen ? 'lucide:x' : 'lucide:menu'" class="size-4" />
				</button>
			</div>
		</div>

		<nav v-if="mobileOpen" class="border-t border-line px-4 py-2 md:hidden">
			<NuxtLink
				v-for="link in links"
				:key="link.to"
				:to="link.to"
				class="block rounded-lg px-3 py-2 text-sm"
				:class="isActive(link.to) ? 'bg-raised text-ink' : 'text-ink-3'"
			>
				{{ link.label }}
			</NuxtLink>
		</nav>
	</header>
</template>
