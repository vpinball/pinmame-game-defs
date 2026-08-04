<script setup lang="ts">
import type { CatalogDriver, DriverVariant } from '~/types/defs'

const props = defineProps<{
	drivers: DriverVariant[]
	catalogDrivers?: CatalogDriver[]
}>()

const showAll = ref(false)

/**
 * The definition's own driver list carries the compatibility notes; the catalog
 * list is the authority on which ROM sets actually resolve here. Merge them so
 * a reader searching for their exact ROM name always finds it.
 */
const rows = computed(() => {
	const notes = new Map(props.drivers.map(d => [d.id, d]))
	const base = props.catalogDrivers?.length
		? props.catalogDrivers.map(d => ({
				id: d.id,
				description: d.description,
				year: d.year,
				clone_of: d.clone_of,
				physical_compatibility: notes.get(d.id)?.physical_compatibility,
				variant_notes: notes.get(d.id)?.variant_notes,
			}))
		: props.drivers
	return base.slice().sort(byNewestFirst)
})

const visible = computed(() => (showAll.value ? rows.value : rows.value.slice(0, 8)))
const parents = computed(() => rows.value.filter(r => !r.clone_of).map(r => r.id))

const COMPAT_COLOR: Record<string, string> = {
	identical: 'var(--color-ready)',
	compatible: 'var(--color-ready)',
	different: 'var(--color-partial)',
}
</script>

<template>
	<div class="panel overflow-hidden">
		<div class="overflow-x-auto">
			<table class="w-full text-sm">
				<thead>
					<tr class="border-b border-line text-left">
						<th class="eyebrow px-4 py-2 font-semibold">
							ROM set
						</th>
						<th class="eyebrow px-3 py-2 font-semibold">
							Description
						</th>
						<th class="eyebrow px-3 py-2 font-semibold">
							Year
						</th>
						<th class="eyebrow px-3 py-2 font-semibold">
							Parent
						</th>
						<th class="eyebrow px-3 py-2 font-semibold">
							Hardware
						</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="row in visible" :key="row.id" class="border-b border-line-soft last:border-0 hover:bg-hover/60">
						<td class="px-4 py-2 whitespace-nowrap">
							<span class="num rounded-md border border-amber/25 bg-amber/8 px-1.5 py-0.5 text-xs text-amber">{{ row.id }}</span>
						</td>
						<td class="px-3 py-2 text-ink-2">
							{{ row.description }}
							<div v-if="row.variant_notes" class="mt-0.5 text-[11px] text-ink-4">
								{{ row.variant_notes }}
							</div>
						</td>
						<td class="num px-3 py-2 text-ink-3">
							{{ row.year ?? '—' }}
						</td>
						<td class="num px-3 py-2 text-xs text-ink-3">
							{{ row.clone_of ?? '—' }}
						</td>
						<td class="px-3 py-2 text-xs whitespace-nowrap">
							<span
								v-if="row.physical_compatibility"
								:style="{ color: COMPAT_COLOR[row.physical_compatibility] ?? 'var(--color-ink-3)' }"
							>{{ row.physical_compatibility }}</span>
							<span v-else class="text-ink-4">—</span>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<button
			v-if="rows.length > 8"
			type="button"
			class="flex w-full items-center justify-center gap-2 border-t border-line px-4 py-2.5 text-xs text-ink-3 transition-colors hover:bg-hover hover:text-ink"
			@click="showAll = !showAll"
		>
			<Icon :name="showAll ? 'lucide:chevron-up' : 'lucide:chevron-down'" class="size-3.5" />
			{{ showAll ? 'Show fewer' : `Show all ${rows.length} ROM sets` }}
		</button>

		<p v-if="parents.length" class="border-t border-line px-4 py-2.5 text-[11px] text-ink-4">
			Parent set{{ parents.length > 1 ? 's' : '' }}:
			<span class="num text-ink-3">{{ parents.join(', ') }}</span>
			— clones share this definition unless a hardware difference is noted.
		</p>
	</div>
</template>
