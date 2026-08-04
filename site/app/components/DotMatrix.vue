<script setup lang="ts">
/**
 * A dot-matrix display panel. Text is stamped from the 5×7 WPC-style bitmap
 * font in `utils/dmdfont`, then every lit pixel is drawn as a glowing dot —
 * so the panel shows real authored glyphs rather than a thresholded webfont.
 */
const props = withDefaults(defineProps<{
	lines: string[][]
	cols?: number
	rows?: number
	interval?: number
	color?: string
	maxScale?: number
}>(), {
	cols: 128,
	rows: 32,
	interval: 3600,
	color: '#ff8a1e',
	maxScale: 3,
})

const canvas = ref<HTMLCanvasElement | null>(null)
const frame = ref(0)
let timer: ReturnType<typeof setInterval> | undefined

// Wide enough that the largest fitting scale still leaves a visible border —
// text touching the panel edge reads as overflow rather than as a headline.
function paint() {
	const el = canvas.value
	if (!el) return

	const cell = 4
	const width = props.cols * cell
	const height = props.rows * cell
	const dpr = Math.min(window.devicePixelRatio || 1, 2)
	el.width = width * dpr
	el.height = height * dpr
	el.style.aspectRatio = `${props.cols} / ${props.rows}`

	const ctx = el.getContext('2d')!
	ctx.scale(dpr, dpr)
	ctx.clearRect(0, 0, width, height)

	const { grid } = layoutPanel(props.lines[frame.value % props.lines.length] ?? [], props.cols, props.rows, { maxScale: props.maxScale })
	const radius = cell * 0.36

	for (let row = 0; row < props.rows; row++) {
		for (let col = 0; col < props.cols; col++) {
			ctx.beginPath()
			ctx.arc(col * cell + cell / 2, row * cell + cell / 2, radius, 0, Math.PI * 2)
			if (grid[row]![col]) {
				ctx.shadowColor = props.color
				ctx.shadowBlur = cell * 1.6
				ctx.fillStyle = props.color
			}
			else {
				ctx.shadowBlur = 0
				ctx.fillStyle = 'rgba(255,255,255,0.045)'
			}
			ctx.fill()
		}
	}
	ctx.shadowBlur = 0
}

onMounted(() => {
	paint()
	if (props.lines.length > 1) {
		timer = setInterval(() => {
			frame.value++
			paint()
		}, props.interval)
	}
	window.addEventListener('resize', paint)
})

onBeforeUnmount(() => {
	if (timer) clearInterval(timer)
	window.removeEventListener('resize', paint)
})
</script>

<template>
	<div class="relative w-full overflow-hidden rounded-lg bg-[#08090b] ring-1 ring-white/8">
		<canvas ref="canvas" class="block w-full" />
		<!-- glass reflection across the panel -->
		<div class="pointer-events-none absolute inset-0 bg-linear-to-b from-white/6 via-transparent to-transparent" />
	</div>
</template>
