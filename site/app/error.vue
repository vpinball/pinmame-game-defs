<script setup lang="ts">
import type { NuxtError } from '#app'

defineProps<{ error: NuxtError }>()

useHead({
	script: [{
		innerHTML: `try{var t=localStorage.getItem('pmg-theme');document.documentElement.dataset.theme=t==='light'?'light':'dark'}catch(e){document.documentElement.dataset.theme='dark'}`,
		tagPosition: 'head',
	}],
})
</script>

<template>
	<div class="dotfield flex min-h-screen flex-col items-center justify-center px-6 text-center">
		<div class="num text-6xl text-amber">
			{{ error.statusCode }}
		</div>
		<h1 class="mt-4 text-xl font-semibold">
			{{ error.statusCode === 404 ? 'No definition at this address' : 'Something went wrong' }}
		</h1>
		<p class="mt-2 max-w-md text-sm text-ink-3">
			{{ error.statusCode === 404
				? 'That machine or platform is not in the catalog. Try searching for the ROM set instead — every supported driver resolves somewhere.'
				: error.message }}
		</p>
		<div class="mt-6 flex flex-wrap justify-center gap-3">
			<NuxtLink to="/" class="rounded-lg bg-amber px-4 py-2 text-sm font-medium text-void">
				Home
			</NuxtLink>
			<NuxtLink to="/roms" class="rounded-lg border border-line px-4 py-2 text-sm text-ink-2 hover:text-ink">
				ROM lookup
			</NuxtLink>
		</div>
	</div>
</template>
