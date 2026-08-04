<script setup lang="ts">
const searchOpen = ref(false)

useHead({
	titleTemplate: title => (title ? `${title} · PinMAME Machine Reference` : 'PinMAME Machine Reference'),
	script: [{
		// Applied before first paint so the chosen theme never flashes. The query
		// string is snapshotted here too: on a prerendered page the router
		// normalises the URL during hydration, so by the time a page component
		// mounts, `?status=…&tags=…` is already gone.
		innerHTML: `try{var t=localStorage.getItem('pmg-theme');document.documentElement.dataset.theme=t==='light'?'light':'dark'}catch(e){document.documentElement.dataset.theme='dark'}window.__pmgQuery=location.search;window.__pmgPath=location.pathname`,
		tagPosition: 'head',
	}],
})

function onKeydown(event: KeyboardEvent) {
	if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
		event.preventDefault()
		searchOpen.value = !searchOpen.value
	}
	else if (event.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test((event.target as HTMLElement)?.tagName ?? '')) {
		event.preventDefault()
		searchOpen.value = true
	}
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))
</script>

<template>
	<div class="flex min-h-screen flex-col">
		<AppHeader v-model:search-open="searchOpen" />
		<main class="flex-1">
			<NuxtPage />
		</main>
		<AppFooter />
		<SearchPalette v-model="searchOpen" />
	</div>
</template>
