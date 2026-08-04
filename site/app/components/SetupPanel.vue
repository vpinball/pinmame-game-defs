<script setup lang="ts">
import type { Display, MachineDetail } from '~/types/defs'

const props = defineProps<{ machine: MachineDetail }>()

/** The ROM an author should bind first: a parent set, newest revision wins. */
const primaryRoms = computed(() => {
	const drivers = props.machine.catalogDrivers?.length ? props.machine.catalogDrivers : props.machine.drivers
	const parents = drivers.filter(d => !d.clone_of)
	return (parents.length ? parents : drivers).map(d => d.id)
})

const roleFor = (prefixes: string[]) =>
	props.machine.inputs.filter(input => input.roles?.some(role => prefixes.some(p => role.startsWith(p))))

const cabinet = computed(() => roleFor(['cabinet.']))
const flippers = computed(() => roleFor(['flipper.']))
const ballPositions = computed(() =>
	props.machine.inputs.filter(input => input.roles?.includes('ball.position')))

const gi = computed(() => props.machine.outputs.filter(o => o.binding.group === 'pinmame.output.gi'))

/** A DMD reports pixels; a segment panel reports how many digits it has. */
function displaySize(display: Display) {
	if (display.width && display.height) return `${display.width}×${display.height}`
	if (display.width) return `${display.width} digit${display.width === 1 ? '' : 's'}`
	return null
}

const addressRange = (group: string, list: { binding: { group: string, device: number } }[]) => {
	const values = list.filter(d => d.binding.group === group).map(d => d.binding.device).sort((a, b) => a - b)
	if (!values.length) return null
	const min = values[0]!
	const max = values.at(-1)!
	return { min, max, count: values.length }
}

const ranges = computed(() => [
	{ label: 'Switches', group: 'pinmame.input.switch', kind: 'switch', range: addressRange('pinmame.input.switch', props.machine.inputs) },
	{ label: 'Solenoids', group: 'pinmame.output.solenoid', kind: 'coil', range: addressRange('pinmame.output.solenoid', props.machine.outputs) },
	{ label: 'Lamps', group: 'pinmame.output.lamp', kind: 'lamp', range: addressRange('pinmame.output.lamp', props.machine.outputs) },
	{ label: 'GI', group: 'pinmame.output.gi', kind: 'gi', range: addressRange('pinmame.output.gi', props.machine.outputs) },
	{ label: 'DIP', group: 'pinmame.input.dip', kind: 'dip_switch', range: addressRange('pinmame.input.dip', props.machine.inputs) },
].filter(item => item.range))
</script>

<template>
	<section class="panel overflow-hidden">
		<header class="flex items-center gap-2 border-b border-line px-5 py-3">
			<Icon name="lucide:plug-zap" class="size-4 text-amber" />
			<h2 class="text-sm font-semibold">
				Wire it up
			</h2>
			<span class="ml-auto text-[11px] text-ink-4">what an authoring tool needs first</span>
		</header>

		<div class="grid md:grid-cols-2 xl:grid-cols-3">
			<!-- ROM binding -->
			<div class="cell">
				<div class="eyebrow mb-3">
					Bind this ROM
				</div>
				<div class="flex flex-wrap gap-1.5">
					<span
						v-for="rom in primaryRoms.slice(0, 6)"
						:key="rom"
						class="num rounded-md border border-amber/25 bg-amber/8 px-2 py-1 text-xs text-amber"
					>{{ rom }}</span>
				</div>
				<p class="mt-3 text-[11px] leading-relaxed text-ink-4">
					{{ (machine.catalogDrivers?.length ?? machine.drivers.length) }} ROM set{{ (machine.catalogDrivers?.length ?? machine.drivers.length) === 1 ? '' : 's' }}
					resolve to this machine. Clones share the definition unless a hardware difference is listed.
				</p>
			</div>

			<!-- platform -->
			<div class="cell">
				<div class="eyebrow mb-3">
					Controller platform
				</div>
				<NuxtLink
					v-if="machine.controller?.platform"
					:to="`/platforms/${platformSlug(machine.controller.platform)}`"
					class="num inline-flex items-center gap-1.5 text-sm text-ink transition-colors hover:text-amber"
				>
					{{ machine.controller.platform }}
					<Icon name="lucide:arrow-up-right" class="size-3.5" />
				</NuxtLink>
				<span v-else class="text-sm text-ink-4">Not determined</span>
				<p v-if="machine.controller?.inversion_applied_by_emulator" class="mt-3 flex gap-2 text-[11px] leading-relaxed text-ink-4">
					<Icon name="lucide:info" class="mt-0.5 size-3.5 shrink-0" />
					PinMAME already reports logical active state. Do not invert again in the table — normally-closed is a physical
					fact recorded per switch, not a runtime transform.
				</p>
			</div>

			<!-- displays -->
			<div class="cell">
				<div class="eyebrow mb-3">
					Displays
				</div>
				<ul v-if="machine.displays.length" class="space-y-2">
					<li v-for="display in machine.displays" :key="display.id" class="flex items-center gap-2 text-sm">
						<Icon name="lucide:monitor" class="size-3.5 shrink-0 text-k-display" />
						<span class="min-w-0 truncate">{{ display.label }}</span>
						<span v-if="displaySize(display)" class="num ml-auto shrink-0 text-xs whitespace-nowrap text-ink-3">
							{{ displaySize(display) }}
						</span>
					</li>
				</ul>
				<p v-else class="text-sm text-ink-4">
					No display inventory recorded yet.
				</p>
			</div>

			<!-- address ranges -->
			<div class="cell">
				<div class="eyebrow mb-3">
					Address space
				</div>
				<dl class="space-y-1.5">
					<div v-for="item in ranges" :key="item.label" class="flex items-center gap-3 text-sm">
						<dt class="flex w-24 shrink-0 items-center gap-1.5 text-xs text-ink-3">
							<span class="size-1.5 rounded-[2px]" :style="{ background: kindColor(item.kind) }" />
							{{ item.label }}
						</dt>
						<dd class="num text-xs text-ink-2">
							{{ item.range!.min }}–{{ item.range!.max }}
							<span class="ml-1 text-ink-4">({{ item.range!.count }})</span>
						</dd>
					</div>
				</dl>
				<p v-if="gi.length === 1 && gi[0]!.binding.device === 0" class="mt-3 text-[11px] leading-relaxed text-ink-4">
					A single aggregate GI channel — the whole string switches together.
				</p>
			</div>

			<!-- initial ball state -->
			<div v-if="ballPositions.length" class="cell">
				<div class="eyebrow mb-3">
					Ball positions at start
				</div>
				<div class="flex flex-wrap gap-1.5">
					<span
						v-for="input in ballPositions"
						:key="input.id"
						class="inline-flex items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px]"
						:title="input.label"
					>
						<span class="num text-k-switch">{{ input.binding.device }}</span>
						<span class="max-w-32 truncate text-ink-3">{{ input.label }}</span>
					</span>
				</div>
				<p class="mt-3 text-[11px] text-ink-4">
					Create balls on these switches so the ROM finds a full trough at boot.
				</p>
			</div>

			<!-- cabinet + flippers -->
			<div v-if="cabinet.length || flippers.length" class="cell">
				<div class="eyebrow mb-3">
					Cabinet & flipper inputs
				</div>
				<div class="flex flex-wrap gap-1.5">
					<span
						v-for="input in [...flippers, ...cabinet].slice(0, 14)"
						:key="input.id"
						class="inline-flex items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px]"
						:title="input.label"
					>
						<span class="num text-k-switch">{{ input.binding.device }}</span>
						<span class="num max-w-36 truncate text-ink-3">{{ input.roles?.[0] }}</span>
					</span>
				</div>
				<p class="mt-3 text-[11px] text-ink-4">
					Portable roles — the consuming engine maps them to its own input actions.
				</p>
			</div>
		</div>
	</section>
</template>

<style scoped>
/*
 * Hairline dividers drawn by the cells themselves rather than by grid gaps, so
 * a hidden panel leaves no visible hole in the last row.
 */
.cell {
	padding: 1.25rem;
	border-top: 1px solid var(--color-line);
	border-left: 1px solid var(--color-line);
	margin-top: -1px;
	margin-left: -1px;
}
</style>
