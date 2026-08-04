<script setup lang="ts">
import type { Device, Mechanism } from '~/types/defs'

const props = defineProps<{
	mechanism: Mechanism
	deviceById: Map<string, Device>
}>()

const MECH_ICON: Record<string, string> = {
	kicker: 'lucide:log-out',
	drop_target_bank: 'lucide:chevrons-down',
	motorized: 'lucide:cog',
	rotary: 'lucide:rotate-cw',
	diverter: 'lucide:git-fork',
	gate: 'lucide:door-open',
	toy: 'lucide:sparkles',
	other: 'lucide:box',
}

const resolve = (ids: string[] | undefined) =>
	(ids ?? []).map(id => ({ id, device: props.deviceById.get(id) ?? null }))

const actuators = computed(() => resolve(props.mechanism.actuators))
const sensors = computed(() => resolve(props.mechanism.sensors))
</script>

<template>
	<article class="panel flex flex-col p-4">
		<header class="flex items-start gap-3">
			<span class="mt-0.5 grid size-8 shrink-0 place-items-center rounded-lg border border-line bg-raised text-amber">
				<Icon :name="MECH_ICON[mechanism.kind] ?? MECH_ICON.other!" class="size-4" />
			</span>
			<div class="min-w-0">
				<h3 class="text-sm leading-tight font-semibold">
					{{ mechanism.label }}
				</h3>
				<p class="num mt-0.5 text-[11px] text-ink-4">
					{{ mechanism.id }}
				</p>
			</div>
			<span class="ml-auto shrink-0 rounded-md border border-line px-1.5 py-0.5 text-[10px] text-ink-3">
				{{ titleCase(mechanism.kind) }}
			</span>
		</header>

		<p v-if="mechanism.behavior" class="mt-3 text-sm leading-relaxed text-ink-2">
			{{ mechanism.behavior }}
		</p>

		<div v-if="actuators.length || sensors.length" class="mt-4 grid gap-3 sm:grid-cols-2">
			<div v-if="actuators.length">
				<div class="eyebrow mb-1.5">
					Drives
				</div>
				<div class="flex flex-wrap gap-1.5">
					<a
						v-for="item in actuators"
						:key="item.id"
						:href="`#device-${item.id}`"
						class="inline-flex items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px] transition-colors hover:border-amber/40"
					>
						<span v-if="item.device" class="num text-ink-3">{{ item.device.binding.device }}</span>
						<span class="truncate">{{ item.device?.label ?? item.id }}</span>
					</a>
				</div>
			</div>
			<div v-if="sensors.length">
				<div class="eyebrow mb-1.5">
					Senses
				</div>
				<div class="flex flex-wrap gap-1.5">
					<a
						v-for="item in sensors"
						:key="item.id"
						:href="`#device-${item.id}`"
						class="inline-flex items-center gap-1.5 rounded-md border border-line bg-raised px-1.5 py-1 text-[11px] transition-colors hover:border-amber/40"
					>
						<span v-if="item.device" class="num text-ink-3">{{ item.device.binding.device }}</span>
						<span class="truncate">{{ item.device?.label ?? item.id }}</span>
					</a>
				</div>
			</div>
		</div>
	</article>
</template>
