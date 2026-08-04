<script setup lang="ts">
import type { Device } from '~/types/defs'
import type { PlayfieldCluster } from '~/utils/playfield'

/**
 * Where everything physically sits on the playfield.
 *
 * The address matrices show the *electrical* layout — what number the emulator
 * reports. This is the *physical* one, and the two answer different questions:
 * "which switch is 52" versus "what is that opto beside the left ramp".
 *
 * Coordinates come from the definition in normalised player view (x 0 = left,
 * y 0 = the backglass end), so drawing needs no interpretation beyond scaling.
 * The outline is nominal — the catalog records where devices are, not the shape
 * of the cabinet.
 *
 * Rendering is split into a static base layer and a small highlight layer on
 * top. Nothing in the base layer depends on what is focused, so hovering patches
 * a handful of nodes rather than every marker on the board.
 */
const props = defineProps<{
	devices: Device[]
	highlight?: string | null
}>()

const emit = defineEmits<{ select: [device: Device | null] }>()

const outline = playfieldOutline()

/* -- clustering ---------------------------------------------------------- */

const allPlacements = computed(() => placementsOf(props.devices))

const GROUPS = [
	{ id: 'switches', label: 'Switches', kinds: ['switch'] },
	{ id: 'coils', label: 'Coils', kinds: ['coil', 'magnet', 'motor', 'servo', 'relay'] },
	{ id: 'flashers', label: 'Flashers', kinds: ['flasher'] },
	{ id: 'lamps', label: 'Lamps', kinds: ['lamp', 'rgb_lamp'] },
	{ id: 'gi', label: 'GI', kinds: ['gi'] },
] as const

const active = ref<string[]>(GROUPS.map(g => g.id))

const visibleKinds = computed(() =>
	new Set(GROUPS.filter(g => active.value.includes(g.id)).flatMap(g => g.kinds as readonly string[])))

const clusters = computed(() =>
	clusterPlacements(allPlacements.value.filter(p => visibleKinds.value.has(p.device.kind))))

const groups = computed(() =>
	GROUPS
		.map(group => ({
			...group,
			count: allPlacements.value.filter(p => (group.kinds as readonly string[]).includes(p.device.kind)).length,
			on: active.value.includes(group.id),
			color: kindColor(group.kinds[0]),
		}))
		.filter(group => group.count > 0))

function toggle(id: string) {
	active.value = active.value.includes(id)
		? active.value.filter(g => g !== id)
		: [...active.value, id]
	if (!active.value.length) active.value = GROUPS.map(g => g.id)
	// A pinned cluster may not survive a filter change.
	pinned.value = null
}

/* -- focus and drill-in --------------------------------------------------- */

/**
 * Hovering is transient; clicking pins. A pin survives the pointer leaving, and
 * clicking the same marker again releases it — so a reader can park on a device
 * and go read its row in the table without losing the spot.
 */
const hoveredKey = ref<string | null>(null)
const hoveredDevice = ref<string | null>(null)
const pinned = ref<string | null>(null)

const clusterByKey = computed(() => new Map(clusters.value.map(c => [c.key, c])))

/** Hover wins while it lasts, then focus falls back to the pin. */
const activeKey = computed(() => hoveredKey.value ?? pinned.value)

const focusDevice = computed(() => {
	if (hoveredDevice.value) return hoveredDevice.value
	const cluster = activeKey.value ? clusterByKey.value.get(activeKey.value) : null
	if (cluster && cluster.deviceIds.length === 1) return cluster.deviceIds[0]!
	return activeKey.value ? null : props.highlight ?? null
})

/** The clusters drawn bright on top; everything else dims behind them. */
const litClusters = computed<PlayfieldCluster[]>(() => {
	if (activeKey.value) {
		const cluster = clusterByKey.value.get(activeKey.value)
		return cluster ? [cluster] : []
	}
	if (focusDevice.value) {
		return clusters.value.filter(c => c.deviceIds.includes(focusDevice.value!))
	}
	return []
})

const dimming = computed(() => litClusters.value.length > 0)

/** What the inspector describes: a hovered stack, or the focused device. */
const inspected = computed(() => {
	const cluster = litClusters.value[0]
	if (!cluster) return null
	const members = focusDevice.value
		? cluster.members.filter(m => m.device.id === focusDevice.value)
		: cluster.members
	return { cluster, members: members.length ? members : cluster.members }
})

/* -- the index ------------------------------------------------------------ */

const ROLE_LABEL: Record<string, string> = {
	sensor: 'senses the ball',
	effect: 'moves the ball',
	emitter: 'lights the playfield',
}

const roleCounts = computed(() => {
	const counts = new Map<string, number>()
	for (const { placement } of allPlacements.value) {
		counts.set(placement.role, (counts.get(placement.role) ?? 0) + 1)
	}
	return [...counts.entries()].sort((a, b) => b[1] - a[1])
})

/** A pinned stack narrows the index to its members. */
const openedCluster = computed(() => {
	const cluster = pinned.value ? clusterByKey.value.get(pinned.value) : null
	return cluster && cluster.members.length > 1 ? cluster : null
})

/**
 * One row per device — a GI string is one address lighting forty-five points,
 * and forty-five identical rows would say nothing. Drilling into a stack
 * narrows the list to that stack's members.
 */
const index = computed(() => {
	const source = openedCluster.value ? openedCluster.value.members : clusters.value.flatMap(c => c.members)
	const byDevice = new Map<string, { device: Device, points: number, color: string, role: string }>()
	for (const { device, placement } of source) {
		const entry = byDevice.get(device.id)
		if (entry) entry.points++
		else byDevice.set(device.id, { device, points: 1, color: kindColor(device.kind), role: placement.role })
	}
	return [...byDevice.values()].sort((a, b) =>
		a.device.binding.device - b.device.binding.device || a.device.label.localeCompare(b.device.label))
})

function pick(cluster: PlayfieldCluster) {
	if (pinned.value === cluster.key) {
		pinned.value = null
		emit('select', null)
		return
	}
	pinned.value = cluster.key
	// A stack has no single device to highlight elsewhere; its members are
	// listed instead.
	emit('select', cluster.members.length === 1 ? cluster.members[0]!.device : null)
}

/** Devices the catalog explicitly says have no place on the playfield. */
const notApplicable = computed(() => {
	const counts = new Map<string, number>()
	for (const device of props.devices) {
		if (device.spatial?.status !== 'not_applicable') continue
		counts.set(device.spatial.reason, (counts.get(device.spatial.reason) ?? 0) + 1)
	}
	return [...counts.entries()].sort((a, b) => b[1] - a[1])
})

const stacked = computed(() => clusters.value.filter(c => c.members.length > 1).length)
</script>

<template>
	<div v-if="allPlacements.length" class="panel overflow-hidden">
		<header class="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-line px-5 py-3">
			<h3 class="text-sm font-semibold">
				Playfield map
			</h3>
			<p class="text-[11px] text-ink-4">
				{{ allPlacements.length }} placements<span v-if="stacked"> · {{ stacked }} stacked</span> · normalised player
				view · outline is nominal
			</p>
		</header>

		<div class="grid lg:grid-cols-[minmax(0,24rem)_minmax(0,1fr)]">
			<div class="flex flex-col gap-3 bg-panel p-5">
				<svg
					:viewBox="`-30 -30 ${PF_WIDTH + 60} ${PF_HEIGHT + 60}`"
					class="mx-auto block h-auto w-full max-w-[19rem]"
					role="img"
					aria-label="Playfield layout with a marker per device placement"
					@mouseleave="hoveredKey = null"
				>
					<defs>
						<radialGradient id="pf-surface" cx="50%" cy="32%" r="72%">
							<stop offset="0%" stop-color="var(--color-pf-center)" />
							<stop offset="100%" stop-color="var(--color-pf-edge)" />
						</radialGradient>
					</defs>

					<path :d="outline" fill="url(#pf-surface)" stroke="var(--color-line)" stroke-width="4" />

					<!-- base layer: independent of focus, so it is not re-rendered by a hover -->
					<g :class="dimming ? 'pf-dim' : ''">
						<PlayfieldMarker
							v-for="cluster in clusters"
							:key="cluster.key"
							:cluster="cluster"
							class="cursor-pointer"
							@mouseenter="hoveredKey = cluster.key"
							@mouseleave="hoveredKey = null"
							@click="pick(cluster)"
						/>
					</g>

					<!-- highlight layer: only ever a few nodes -->
					<g class="pointer-events-none">
						<PlayfieldMarker
							v-for="cluster in litClusters"
							:key="`lit-${cluster.key}`"
							:cluster="cluster"
							ring
						/>
					</g>
				</svg>

				<div class="min-h-[4.75rem] rounded-lg border border-line-soft bg-raised p-3">
					<template v-if="inspected">
						<div
							v-for="{ device, placement } in inspected.members.slice(0, 4)"
							:key="`${device.id}-${placement.id}`"
							class="flex items-center gap-2 py-0.5"
						>
							<span
								class="num rounded px-1.5 py-0.5 text-xs"
								:style="{ background: `color-mix(in srgb, ${kindColor(device.kind)} 16%, transparent)`, color: `color-mix(in srgb, ${kindColor(device.kind)} 88%, var(--color-ink))` }"
							>{{ device.binding.device }}</span>
							<span class="min-w-0 flex-1 truncate text-sm">{{ device.label }}</span>
							<span class="num shrink-0 text-[10px] text-ink-4">{{ placement.role }}</span>
						</div>
						<p v-if="inspected.members.length > 4" class="mt-1 text-[11px] text-ink-4">
							and {{ inspected.members.length - 4 }} more here — click the stack to list them
						</p>
						<div v-else class="num mt-1 flex flex-wrap gap-x-3 text-[11px] text-ink-4">
							<span>x {{ inspected.members[0]!.placement.x.toFixed(3) }}</span>
							<span>y {{ inspected.members[0]!.placement.y.toFixed(3) }}</span>
							<span v-if="inspected.members[0]!.placement.provenance?.status">
								· {{ inspected.members[0]!.placement.provenance!.status }}
							</span>
						</div>
					</template>
					<p v-else class="text-xs text-ink-4">
						Hover a marker to identify it, or click to keep it selected. Numbered markers are several devices in one
						spot — clicking lists them.
					</p>
				</div>
			</div>

			<div class="flex flex-col gap-5 border-t border-line bg-panel p-5 lg:border-t-0 lg:border-l">
				<div>
					<div class="eyebrow mb-2">
						Show
					</div>
					<div class="flex flex-wrap gap-1.5">
						<button
							v-for="group in groups"
							:key="group.id"
							type="button"
							class="inline-flex items-center gap-1.5 rounded-md border px-2 py-1 text-[11px] transition-colors"
							:style="group.on
								? { color: group.color, borderColor: `color-mix(in srgb, ${group.color} 40%, transparent)`, background: `color-mix(in srgb, ${group.color} 12%, transparent)` }
								: { color: 'var(--color-ink-4)', borderColor: 'var(--color-line-soft)' }"
							:aria-pressed="group.on"
							@click="toggle(group.id)"
						>
							<span class="size-1.5 rounded-full" :style="{ background: group.on ? group.color : 'var(--color-ink-4)' }" />
							{{ group.label }}
							<span class="num opacity-60">{{ group.count }}</span>
						</button>
					</div>
				</div>

				<div>
					<div class="eyebrow mb-2">
						Marker shape
					</div>
					<ul class="space-y-1.5">
						<li v-for="[role, count] in roleCounts" :key="role" class="flex items-center gap-2.5 text-[12px]">
							<svg width="16" height="16" viewBox="-8 -8 16 16" class="shrink-0 text-ink-2">
								<circle v-if="role === 'emitter'" r="5" fill="currentColor" />
								<circle v-else-if="role === 'sensor'" r="4.5" fill="none" stroke="currentColor" stroke-width="2.5" />
								<rect v-else x="-5" y="-5" width="10" height="10" rx="1.5" fill="currentColor" transform="rotate(45)" />
							</svg>
							<span class="text-ink-2 capitalize">{{ role }}</span>
							<span class="text-ink-4">{{ ROLE_LABEL[role] }}</span>
							<span class="num ml-auto text-ink-4">{{ count }}</span>
						</li>
						<li v-if="stacked" class="flex items-center gap-2.5 text-[12px]">
							<svg width="16" height="16" viewBox="-8 -8 16 16" class="shrink-0 text-ink-2">
								<circle r="6" fill="none" stroke="currentColor" stroke-width="1.6" />
								<text x="0" y="0" text-anchor="middle" dominant-baseline="central" font-size="8" fill="currentColor">n</text>
							</svg>
							<span class="text-ink-2">Stack</span>
							<span class="text-ink-4">several devices in one spot</span>
							<span class="num ml-auto text-ink-4">{{ stacked }}</span>
						</li>
					</ul>
				</div>

				<div class="flex min-h-0 flex-1 flex-col">
					<div class="mb-2 flex items-center gap-2">
						<span class="eyebrow">
							{{ openedCluster ? `Stack of ${openedCluster.members.length}` : `${index.length} device${index.length === 1 ? '' : 's'} shown` }}
						</span>
						<button
							v-if="openedCluster"
							type="button"
							class="text-[11px] text-amber hover:underline"
							@click="pinned = null; emit('select', null)"
						>
							show all
						</button>
					</div>
					<ul class="max-h-[26rem] min-h-0 flex-1 divide-y divide-line-soft overflow-y-auto rounded-lg border border-line-soft">
						<li
							v-for="row in index"
							:key="`row-${row.device.id}`"
							v-memo="[focusDevice === row.device.id]"
						>
							<button
								type="button"
								class="flex w-full items-center gap-2.5 px-2.5 py-1.5 text-left transition-colors"
								:class="focusDevice === row.device.id ? 'bg-hover' : 'hover:bg-hover/60'"
								@mouseenter="hoveredDevice = row.device.id"
								@mouseleave="hoveredDevice = null"
								@click="emit('select', row.device)"
							>
								<span
									class="num w-9 shrink-0 rounded px-1 py-0.5 text-center text-[10px]"
									:style="{ background: `color-mix(in srgb, ${row.color} 14%, transparent)`, color: `color-mix(in srgb, ${row.color} 88%, var(--color-ink))` }"
								>{{ row.device.binding.device }}</span>
								<span class="min-w-0 flex-1 truncate text-[12px] text-ink-2">{{ row.device.label }}</span>
								<span v-if="row.points > 1" class="num shrink-0 text-[10px] text-ink-4">{{ row.points }}×</span>
								<svg width="12" height="12" viewBox="-8 -8 16 16" class="shrink-0" :style="{ color: row.color }">
									<circle v-if="row.role === 'emitter'" r="5" fill="currentColor" />
									<circle v-else-if="row.role === 'sensor'" r="4.5" fill="none" stroke="currentColor" stroke-width="2.5" />
									<rect v-else x="-5" y="-5" width="10" height="10" rx="1.5" fill="currentColor" transform="rotate(45)" />
								</svg>
							</button>
						</li>
					</ul>
				</div>

				<p v-if="notApplicable.length" class="text-[11px] leading-relaxed text-ink-4">
					<span class="eyebrow">Not on the playfield</span>
					<span class="ml-2">
						{{ notApplicable.map(([reason, count]) => `${count} ${reason.replace(/_/g, ' ')}`).join(', ') }}
						— declared rather than missing.
					</span>
				</p>
			</div>
		</div>
	</div>
</template>

<style scoped>
/*
 * Dimming is one class on the container rather than a binding per marker, so a
 * hover does not invalidate the whole base layer.
 */
.pf-dim > :deep(g) {
	opacity: 0.22;
}

:deep(g) {
	transition: opacity 0.12s ease;
}
</style>
