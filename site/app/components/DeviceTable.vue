<script setup lang="ts">
import type { Device } from '~/types/defs'

const props = withDefaults(defineProps<{
	devices: Device[]
	direction: 'input' | 'output'
	highlight?: string | null
}>(), { highlight: null })

const query = ref('')
const hideUnused = ref(false)

const hasWiring = computed(() => props.devices.some(d => d.wiring && Object.keys(d.wiring).length))
// A column of 88 identical "Switch" chips carries no information — the address
// pill is already tinted by kind, so only show the column when kinds differ.
const hasMixedKinds = computed(() => new Set(props.devices.map(d => d.kind)).size > 1)
const hasRoles = computed(() => props.devices.some(d => d.roles?.length))
const unusedCount = computed(() => props.devices.filter(d => d.availability === 'unused').length)

const rows = computed(() => {
	const needle = query.value.trim().toLowerCase()
	return props.devices
		.filter(d => !(hideUnused.value && d.availability === 'unused'))
		.filter(d => !needle
			|| d.label.toLowerCase().includes(needle)
			|| d.id.toLowerCase().includes(needle)
			|| String(d.binding?.device ?? '').includes(needle)
			|| (d.roles ?? []).some(r => r.toLowerCase().includes(needle)))
		.slice()
		.sort((a, b) => (a.binding?.device ?? 0) - (b.binding?.device ?? 0))
})

/** Wiring is board-specific; show the pair that matters for this direction. */
function wiringCells(device: Device) {
	const w = device.wiring ?? {}
	return props.direction === 'input'
		? [
				{ label: w.drive_connection, code: w.drive_wire },
				{ label: w.return_connection, code: w.return_wire },
			].filter(x => x.label || x.code)
		: [
				{ label: w.driver_transistor ?? w.connector, code: w.control_wire },
			].filter(x => x.label || x.code)
}

const PROVENANCE_COLOR: Record<string, string> = {
	validated: 'var(--color-ready)',
	observed: 'var(--color-k-switch)',
	candidate: 'var(--color-partial)',
	conflicted: 'var(--color-alert)',
	unknown: 'var(--color-ink-4)',
}
</script>

<template>
	<div class="panel overflow-hidden">
		<div class="flex flex-wrap items-center gap-3 border-b border-line px-4 py-3">
			<div class="relative min-w-0 flex-1">
				<Icon name="lucide:search" class="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-ink-4" />
				<input
					v-model="query"
					type="search"
					:placeholder="`Filter ${devices.length} ${direction === 'input' ? 'inputs' : 'outputs'} by name, address or role…`"
					class="w-full rounded-lg border border-line bg-raised py-1.5 pr-3 pl-8 text-sm text-ink placeholder:text-ink-4 focus:border-amber/50 focus:outline-none"
				>
			</div>
			<label v-if="unusedCount" class="flex shrink-0 cursor-pointer items-center gap-2 text-xs text-ink-3 select-none">
				<input v-model="hideUnused" type="checkbox" class="accent-amber">
				Hide {{ unusedCount }} unused
			</label>
			<span class="num shrink-0 text-xs text-ink-4">{{ rows.length }} shown</span>
		</div>

		<div class="overflow-x-auto">
			<table class="w-full text-sm">
				<thead>
					<tr class="border-b border-line text-left">
						<th class="eyebrow px-4 py-2 font-semibold">
							#
						</th>
						<th class="eyebrow px-3 py-2 font-semibold">
							Name
						</th>
						<th class="eyebrow px-3 py-2 font-semibold">
							Device ID
						</th>
						<th v-if="hasMixedKinds" class="eyebrow px-3 py-2 font-semibold">
							Kind
						</th>
						<th v-if="hasRoles" class="eyebrow px-3 py-2 font-semibold">
							Role
						</th>
						<th v-if="hasWiring" class="eyebrow px-3 py-2 font-semibold">
							Wiring
						</th>
						<th class="eyebrow px-3 py-2 text-right font-semibold">
							Evidence
						</th>
					</tr>
				</thead>
				<tbody>
					<tr
						v-for="device in rows"
						:id="`device-${device.id}`"
						:key="device.id"
						class="border-b border-line-soft transition-colors last:border-0 hover:bg-hover/60"
						:class="highlight === device.id ? 'bg-amber/8' : ''"
					>
						<td class="num px-4 py-2 align-top whitespace-nowrap">
							<span
								class="inline-block min-w-7 rounded-[5px] px-1.5 py-0.5 text-center text-xs"
								:style="{
									background: `color-mix(in srgb, ${kindColor(device.kind)} 14%, transparent)`,
									color: `color-mix(in srgb, ${kindColor(device.kind)} 88%, var(--color-ink))`,
								}"
							>{{ device.binding?.device }}</span>
						</td>
						<td class="px-3 py-2 align-top">
							<div class="flex items-center gap-2">
								<span :class="device.availability === 'unused' ? 'text-ink-4 italic' : 'text-ink'">{{ device.label }}</span>
								<span v-if="device.normally_closed" class="rounded border border-line px-1 text-[10px] text-ink-3" title="Normally closed in hardware">NC</span>
								<span v-if="device.availability === 'optional'" class="rounded border border-line px-1 text-[10px] text-ink-3">opt</span>
							</div>
							<div v-if="device.physical?.switch_type && device.physical.switch_type !== 'unknown'" class="mt-0.5 text-[11px] text-ink-4">
								{{ titleCase(device.physical.switch_type) }}
							</div>
						</td>
						<td class="num px-3 py-2 align-top text-xs break-all text-ink-3">
							{{ device.id }}
						</td>
						<td v-if="hasMixedKinds" class="px-3 py-2 align-top">
							<KindChip :kind="device.kind" />
						</td>
						<td v-if="hasRoles" class="px-3 py-2 align-top">
							<div class="flex flex-wrap gap-1">
								<span
									v-for="role in device.roles ?? []"
									:key="role"
									class="num rounded border border-line bg-raised px-1.5 py-0.5 text-[10px] text-ink-2"
								>{{ role }}</span>
							</div>
						</td>
						<td v-if="hasWiring" class="px-3 py-2 align-top">
							<div class="flex flex-col gap-1">
								<div v-for="(cell, i) in wiringCells(device)" :key="i" class="flex items-center gap-2 whitespace-nowrap">
									<span v-if="cell.label" class="num text-[11px] text-ink-3">{{ cell.label }}</span>
									<WireCode :code="cell.code" />
								</div>
								<span v-if="device.wiring?.board" class="text-[10px] text-ink-4">{{ device.wiring.board }}</span>
							</div>
						</td>
						<td class="px-3 py-2 text-right align-top">
							<span
								v-if="device.provenance?.status"
								class="inline-flex items-center gap-1.5 text-[11px] whitespace-nowrap"
								:style="{ color: PROVENANCE_COLOR[device.provenance.status] ?? 'var(--color-ink-3)' }"
								:title="(device.provenance.source_refs ?? []).join('\n')"
							>
								<span class="size-1.5 rounded-full" :style="{ background: 'currentColor' }" />
								{{ device.provenance.status }}
							</span>
						</td>
					</tr>
					<tr v-if="!rows.length">
						<td colspan="8" class="px-4 py-8 text-center text-sm text-ink-3">
							Nothing matches “{{ query }}”.
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>
