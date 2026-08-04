<script setup lang="ts">
import type { Device } from '~/types/defs'

const props = defineProps<{
	devices: Device[]
	label: string
	hint?: string
}>()

const emit = defineEmits<{ pick: [device: Device] }>()

const matrix = computed(() => buildMatrix(props.devices))
const selected = ref<Device | null>(null)
const hovered = ref<Device | null>(null)

const active = computed(() => hovered.value ?? selected.value)

function cellStyle(device: Device | null) {
	if (!device) {
		return { background: 'transparent', borderColor: 'var(--color-line-soft)', color: 'var(--color-ink-4)' }
	}
	const color = kindColor(device.kind)
	if (device.availability === 'unused') {
		return { background: 'transparent', borderColor: 'var(--color-line)', color: 'var(--color-ink-4)' }
	}
	return {
		background: `color-mix(in srgb, ${color} 16%, transparent)`,
		borderColor: `color-mix(in srgb, ${color} 45%, transparent)`,
		color: `color-mix(in srgb, ${color} 85%, var(--color-ink))`,
	}
}

function pick(device: Device | null) {
	if (!device) return
	selected.value = device
	emit('pick', device)
}
</script>

<template>
	<div v-if="matrix" class="panel p-4 sm:p-5">
		<div class="mb-3 flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
			<div>
				<h3 class="text-sm font-semibold">
					{{ label }}
				</h3>
				<p class="mt-0.5 text-xs text-ink-3">
					{{ hint ?? (matrix.mode === 'wpc' ? 'Column × row matrix — the address is column·row.' : 'Sequential addresses, grouped in columns of eight.') }}
				</p>
			</div>
			<div class="flex items-center gap-3 text-[11px] text-ink-3">
				<span class="inline-flex items-center gap-1.5"><span class="size-2 rounded-[3px]" style="background: color-mix(in srgb, var(--color-k-switch) 45%, transparent)" /> used</span>
				<span class="inline-flex items-center gap-1.5"><span class="size-2 rounded-[3px] border border-line" /> unused</span>
			</div>
		</div>

		<div class="-mx-1 overflow-x-auto px-1 pb-1">
			<div class="flex gap-1.5">
				<!-- row gutter: WPC rows are the second digit of the address, a
				     sequential platform's are the offset inside the column -->
				<div class="sticky left-0 z-10 flex shrink-0 flex-col gap-1.5 bg-panel pr-1">
					<div class="num h-3 text-[10px] leading-none">
						&nbsp;
					</div>
					<div
						v-for="row in 8"
						:key="row"
						class="num flex h-7 items-center justify-end pr-0.5 text-[10px] text-ink-4"
					>
						{{ matrix.mode === 'wpc' ? row : `+${row - 1}` }}
					</div>
				</div>

				<div v-for="column in matrix.columns" :key="column.label" class="flex flex-col gap-1.5">
					<div class="num h-3 text-center text-[10px] leading-none text-ink-4">
						{{ column.label }}
					</div>
					<button
						v-for="cell in column.cells"
						:key="cell.address"
						type="button"
						class="num flex h-7 w-11 items-center justify-center rounded-[5px] border text-[11px] transition-colors"
						:class="cell.device ? 'cursor-pointer hover:brightness-140' : 'cursor-default'"
						:style="cellStyle(cell.device)"
						:aria-label="cell.device ? `${cell.address} — ${cell.device.label}` : `${cell.address} — not assigned`"
						@mouseenter="hovered = cell.device"
						@mouseleave="hovered = null"
						@focus="hovered = cell.device"
						@blur="hovered = null"
						@click="pick(cell.device)"
					>
						{{ cell.address }}
					</button>
				</div>
			</div>
		</div>

		<div class="mt-3 flex min-h-9 items-center gap-2 rounded-lg border border-line-soft bg-raised px-3 py-2 text-sm">
			<template v-if="active">
				<span class="num shrink-0 text-xs text-ink-3">{{ active.binding.device }}</span>
				<span class="truncate" :class="active.availability === 'unused' ? 'text-ink-3 italic' : ''">{{ active.label }}</span>
				<KindChip :kind="active.kind" class="ml-auto shrink-0" />
			</template>
			<span v-else class="text-xs text-ink-4">Hover or tap an address to identify it.</span>
		</div>

		<p v-if="matrix.extras.length" class="mt-3 text-xs text-ink-3">
			<span class="eyebrow">Outside the matrix</span>
			<span class="num ml-2">{{ matrix.extras.map(d => d.binding.device).join(', ') }}</span>
			— dedicated, diagnostic or flipper-column addresses. See the table below.
		</p>
	</div>
</template>
