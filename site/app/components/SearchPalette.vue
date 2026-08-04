<script setup lang="ts">
import type { SearchRow } from '~/types/defs'

const open = defineModel<boolean>({ default: false })

const query = ref('')
const rows = shallowRef<SearchRow[] | null>(null)
const loading = ref(false)
const cursor = ref(0)
const input = ref<HTMLInputElement | null>(null)
const router = useRouter()

async function ensureIndex() {
	if (rows.value || loading.value) return
	loading.value = true
	try {
		rows.value = await loadSearchIndex()
	}
	finally {
		loading.value = false
	}
}

/**
 * Ranking: exact ROM-set hit first (an author usually pastes a driver name),
 * then prefix matches, then anything containing the term. Author-ready
 * definitions outrank stubs at equal relevance.
 */
const results = computed(() => {
	const needle = query.value.trim().toLowerCase()
	if (!needle || !rows.value) return []
	const scored: { row: SearchRow, score: number }[] = []
	for (const row of rows.value) {
		const name = row.n.toLowerCase()
		let score = -1
		if (name === needle) score = 0
		else if (name.startsWith(needle)) score = 1
		else if (row.k.includes(` ${needle}`)) score = 2
		else if (row.k.includes(needle)) score = 3
		if (score < 0) continue
		if (row.c === 'author_ready') score -= 0.4
		else if (row.c === 'partial') score -= 0.2
		// A family answers "which AC/DC?" better than any one of its editions.
		if (row.t === 'f') score -= 0.3
		else if (row.t === 'm') score -= 0.1
		scored.push({ row, score })
		if (scored.length > 4000) break
	}
	return scored.sort((a, b) => a.score - b.score || a.row.n.length - b.row.n.length).slice(0, 30).map(s => s.row)
})

watch(query, () => { cursor.value = 0 })

watch(open, async (value) => {
	if (!value) return
	await ensureIndex()
	await nextTick()
	input.value?.focus()
})

function go(row: SearchRow | undefined) {
	if (!row) return
	open.value = false
	query.value = ''
	router.push(row.t === 'f' ? `/families/${row.s}` : `/machines/${row.s}`)
}

function onKey(event: KeyboardEvent) {
	if (event.key === 'ArrowDown') {
		event.preventDefault()
		cursor.value = Math.min(cursor.value + 1, results.value.length - 1)
	}
	else if (event.key === 'ArrowUp') {
		event.preventDefault()
		cursor.value = Math.max(cursor.value - 1, 0)
	}
	else if (event.key === 'Enter') {
		event.preventDefault()
		go(results.value[cursor.value])
	}
	else if (event.key === 'Escape') {
		open.value = false
	}
}
</script>

<template>
	<Teleport to="body">
		<Transition
			enter-active-class="transition duration-150 ease-out"
			enter-from-class="opacity-0"
			leave-active-class="transition duration-100 ease-in"
			leave-to-class="opacity-0"
		>
			<div v-if="open" class="fixed inset-0 z-100 flex items-start justify-center px-4 pt-[12vh]">
				<div class="absolute inset-0 bg-void/75 backdrop-blur-sm" @click="open = false" />

				<div class="panel relative flex max-h-[70vh] w-full max-w-2xl flex-col overflow-hidden shadow-2xl shadow-black/60">
					<div class="flex items-center gap-3 border-b border-line px-4">
						<Icon name="lucide:search" class="size-4 shrink-0 text-ink-4" />
						<input
							ref="input"
							v-model="query"
							type="text"
							placeholder="Search machines and ROM sets — try “mtl_180h” or “Twilight Zone”"
							class="w-full bg-transparent py-4 text-sm text-ink placeholder:text-ink-4 focus:outline-none"
							@keydown="onKey"
						>
						<kbd class="num shrink-0 rounded border border-line px-1.5 py-0.5 text-[10px] text-ink-4">esc</kbd>
					</div>

					<div class="min-h-0 flex-1 overflow-y-auto">
						<p v-if="loading" class="px-4 py-8 text-center text-sm text-ink-3">
							Loading index…
						</p>
						<p v-else-if="!query.trim()" class="px-4 py-8 text-center text-sm text-ink-4">
							{{ rows ? num(rows.length) : '' }} machines and ROM sets indexed.
						</p>
						<p v-else-if="!results.length" class="px-4 py-8 text-center text-sm text-ink-3">
							No match for “{{ query }}”.
						</p>
						<ul v-else class="py-1.5">
							<li v-for="(row, index) in results" :key="`${row.t}-${row.n}-${index}`">
								<button
									type="button"
									class="flex w-full items-center gap-3 px-4 py-2 text-left transition-colors"
									:class="index === cursor ? 'bg-hover' : 'hover:bg-hover/60'"
									@click="go(row)"
									@mouseenter="cursor = index"
								>
									<span
										class="num w-9 shrink-0 rounded px-1 py-0.5 text-center text-[10px]"
										:class="row.t === 'd'
										? 'border border-amber/25 bg-amber/8 text-amber'
										: row.t === 'f' ? 'border border-ink-3/30 text-ink-2' : 'border border-line text-ink-4'"
									>{{ row.t === 'd' ? 'rom' : row.t === 'f' ? 'group' : 'game' }}</span>
									<span class="min-w-0 flex-1">
										<span class="block truncate text-sm" :class="row.t === 'd' ? 'num text-ink' : 'text-ink'">{{ row.n }}</span>
										<span class="block truncate text-xs text-ink-4">{{ row.d }}</span>
									</span>
									<Icon v-if="row.t === 'f'" name="lucide:layers" class="size-3.5 shrink-0 text-ink-4" />
									<StatusChip v-else :status="row.c" size="sm" dot-only />
								</button>
							</li>
						</ul>
					</div>

					<div class="flex items-center gap-4 border-t border-line px-4 py-2 text-[11px] text-ink-4">
						<span class="flex items-center gap-1"><kbd class="num rounded border border-line px-1">↑</kbd><kbd class="num rounded border border-line px-1">↓</kbd> navigate</span>
						<span class="flex items-center gap-1"><kbd class="num rounded border border-line px-1">↵</kbd> open</span>
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>
