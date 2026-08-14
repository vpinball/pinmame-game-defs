/**
 * Dependency-free Open Graph card renderer shared by the build and its checks.
 *
 * Keeping title wrapping here makes the pixels and the verification agree on
 * the important constraint: a machine title gets at most two DMD lines, with
 * three visible dots when the complete name cannot fit.
 */
import { deflateSync } from 'node:zlib'
import { drawText, GLYPH_HEIGHT, GLYPH_WIDTH, layoutPanel, textWidth, TRACKING } from '../app/utils/dmdfont'

export const OG_WIDTH = 1200
export const OG_HEIGHT = 630

const PANEL_COLS = 128
const PANEL_ROWS = 32
const PANEL_MARGIN_X = 6
const PANEL_USABLE_WIDTH = PANEL_COLS - PANEL_MARGIN_X * 2
export const MAX_DMD_TITLE_CHARS = Math.floor((PANEL_USABLE_WIDTH + TRACKING) / (GLYPH_WIDTH + TRACKING))

type RGB = [number, number, number]

const BACKDROP: RGB = [0x0a, 0x0b, 0x0d]
const DOT_OFF: RGB = [0x1a, 0x1d, 0x22]
const DOT_ON: RGB = [0xff, 0x8a, 0x1e]
const INK: RGB = [0xe9, 0xec, 0xf1]
const MUTED: RGB = [0x6b, 0x75, 0x83]

const CRC_TABLE = Array.from({ length: 256 }, (_, n) => {
	let c = n
	for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1
	return c >>> 0
})

function blendPixel(pixels: Buffer, x: number, y: number, colour: RGB, alpha: number) {
	if (x < 0 || y < 0 || x >= OG_WIDTH || y >= OG_HEIGHT || alpha <= 0) return
	const i = (y * OG_WIDTH + x) * 3
	for (let c = 0; c < 3; c++) pixels[i + c] = Math.round(pixels[i + c]! * (1 - alpha) + colour[c]! * alpha)
}

function makeBackdrop(): Buffer {
	const pixels = Buffer.alloc(OG_WIDTH * OG_HEIGHT * 3)
	for (let i = 0; i < OG_WIDTH * OG_HEIGHT; i++) {
		pixels[i * 3] = BACKDROP[0]
		pixels[i * 3 + 1] = BACKDROP[1]
		pixels[i * 3 + 2] = BACKDROP[2]
	}

	// Warm glow behind the panel, as if the backbox were lit.
	for (let y = 0; y < OG_HEIGHT; y++) {
		for (let x = 0; x < OG_WIDTH; x++) {
			const d = Math.hypot(x - OG_WIDTH / 2, y - 210) / 520
			if (d < 1) blendPixel(pixels, x, y, [0xff, 0x7a, 0x18], 0.14 * (1 - d) ** 2)
		}
	}
	return pixels
}

// The expensive full-frame glow is identical on every card. Copying this
// buffer is considerably cheaper than recalculating it for every machine.
const BASE_PIXELS = makeBackdrop()

class CardCanvas {
	private readonly pixels = Buffer.from(BASE_PIXELS)

	private blend(x: number, y: number, colour: RGB, alpha: number) {
		blendPixel(this.pixels, x, y, colour, alpha)
	}

	/** A round dot with a soft edge, the way a plasma DMD pixel actually looks. */
	private dot(cx: number, cy: number, radius: number, colour: RGB, glow = 0) {
		const reach = Math.ceil(radius + glow)
		for (let y = -reach; y <= reach; y++) {
			for (let x = -reach; x <= reach; x++) {
				const distance = Math.hypot(x, y)
				let alpha = 0
				if (distance <= radius) alpha = 1
				else if (distance <= radius + 1) alpha = radius + 1 - distance
				else if (glow && distance <= radius + glow) alpha = 0.22 * (1 - (distance - radius) / glow)
				this.blend(Math.round(cx + x), Math.round(cy + y), colour, alpha)
			}
		}
	}

	/** Renders one dot-matrix panel: lit text on a grid of unlit dots. */
	panel(lines: string[], originX: number, originY: number, cols: number, rows: number, cell: number) {
		const { grid } = layoutPanel(lines, cols, rows)
		for (let row = 0; row < rows; row++) {
			for (let col = 0; col < cols; col++) {
				const lit = grid[row]![col]
				this.dot(originX + col * cell + cell / 2, originY + row * cell + cell / 2, cell * 0.34, lit ? DOT_ON : DOT_OFF, lit ? cell * 0.9 : 0)
			}
		}
	}

	/** Small solid-block text drawn from the same font as the DMD. */
	blockText(text: string, originX: number, originY: number, scale: number, colour: RGB) {
		const grid: boolean[][] = Array.from({ length: GLYPH_HEIGHT * scale + 2 }, () => Array.from({ length: textWidth(text, scale) + 2 }, () => false))
		drawText(grid, text, 0, 0, scale)
		for (let y = 0; y < grid.length; y++) {
			for (let x = 0; x < grid[y]!.length; x++) {
				if (grid[y]![x]) this.blend(originX + x, originY + y, colour, 1)
			}
		}
	}

	centeredText(text: string, originY: number, scale: number, colour: RGB) {
		this.blockText(text, Math.round((OG_WIDTH - textWidth(text, scale)) / 2), originY, scale, colour)
	}

	encodePng(): Buffer {
		// One filter byte (0 = None) in front of every scanline.
		const raw = Buffer.alloc((OG_WIDTH * 3 + 1) * OG_HEIGHT)
		for (let y = 0; y < OG_HEIGHT; y++) {
			raw[y * (OG_WIDTH * 3 + 1)] = 0
			this.pixels.copy(raw, y * (OG_WIDTH * 3 + 1) + 1, y * OG_WIDTH * 3, (y + 1) * OG_WIDTH * 3)
		}

		const crc = (buf: Buffer) => {
			let c = 0xFFFFFFFF
			for (const byte of buf) c = CRC_TABLE[(c ^ byte) & 0xFF]! ^ (c >>> 8)
			return (c ^ 0xFFFFFFFF) >>> 0
		}
		const chunk = (type: string, data: Buffer) => {
			const length = Buffer.alloc(4)
			length.writeUInt32BE(data.length)
			const body = Buffer.concat([Buffer.from(type, 'ascii'), data])
			const checksum = Buffer.alloc(4)
			checksum.writeUInt32BE(crc(body))
			return Buffer.concat([length, body, checksum])
		}

		const ihdr = Buffer.alloc(13)
		ihdr.writeUInt32BE(OG_WIDTH, 0)
		ihdr.writeUInt32BE(OG_HEIGHT, 4)
		ihdr[8] = 8 // bit depth
		ihdr[9] = 2 // colour type: truecolour
		return Buffer.concat([
			Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
			chunk('IHDR', ihdr),
			chunk('IDAT', deflateSync(raw, { level: 9 })),
			chunk('IEND', Buffer.alloc(0)),
		])
	}
}

/** Converts typographic punctuation and accented Latin text into DMD glyphs. */
export function normalizeDmdText(value: string): string {
	return value
		.normalize('NFKD')
		.replace(/\p{M}/gu, '')
		.replace(/[‘’]/g, '\'')
		.replace(/[“”]/g, '"')
		.replace(/[–—]/g, '-')
		.replace(/\s+/g, ' ')
		.trim()
		.toUpperCase()
}

function truncateWithDots(value: string, maxChars: number): string {
	if (value.length <= maxChars) return value
	if (maxChars <= 3) return '.'.repeat(maxChars)
	return `${value.slice(0, maxChars - 3).trimEnd()}...`
}

export interface DmdTitleLayout {
	lines: string[]
	truncated: boolean
}

/** Word-wraps a title to two readable 1× DMD rows and marks real truncation. */
export function wrapDmdTitle(value: string, maxChars = MAX_DMD_TITLE_CHARS): DmdTitleLayout {
	const title = normalizeDmdText(value) || 'UNTITLED'
	if (title.length <= maxChars) return { lines: [title], truncated: false }

	const splitCandidates: number[] = []
	for (let i = 1; i < title.length; i++) {
		if (title[i] === ' ') splitCandidates.push(i)
	}
	const fittingSplit = splitCandidates
		.filter(index => index <= maxChars && title.length - index - 1 <= maxChars)
		.sort((a, b) => Math.abs(title.length - a * 2) - Math.abs(title.length - b * 2))[0]
	if (fittingSplit !== undefined) return { lines: [title.slice(0, fittingSplit), title.slice(fittingSplit + 1)], truncated: false }

	let firstBreak = title.lastIndexOf(' ', maxChars)
	if (firstBreak <= 0) firstBreak = maxChars
	const first = title.slice(0, firstBreak).trimEnd()
	const remainder = title.slice(firstBreak).trimStart()
	return { lines: [first, truncateWithDots(remainder, maxChars)], truncated: remainder.length > maxChars }
}

function fitText(value: string, maxWidth: number, preferredScale: number): { text: string, scale: number } {
	for (let scale = preferredScale; scale > 1; scale--) {
		if (textWidth(value, scale) <= maxWidth) return { text: value, scale }
	}
	if (textWidth(value, 1) <= maxWidth) return { text: value, scale: 1 }
	const maxChars = Math.floor((maxWidth + TRACKING) / (GLYPH_WIDTH + TRACKING))
	return { text: truncateWithDots(value, maxChars), scale: 1 }
}

export function renderDefaultOgCard(): Buffer {
	const canvas = new CardCanvas()
	canvas.panel(['PINMAME', 'MACHINE REFERENCE'], 100, 120, PANEL_COLS, PANEL_ROWS, 7.8)
	canvas.centeredText('EVERY SWITCH, LAMP AND COIL PINMAME CAN TALK TO', 470, 3, INK)
	canvas.centeredText('SWITCH MAPS / WIRING / MECHANISMS / EVIDENCE', 540, 2, MUTED)
	return canvas.encodePng()
}

export function renderMachineOgCard(machine: { name: string, manufacturer: string, year: number | null }): Buffer {
	const canvas = new CardCanvas()
	canvas.panel(wrapDmdTitle(machine.name).lines, 100, 120, PANEL_COLS, PANEL_ROWS, 7.8)

	const meta = normalizeDmdText([machine.manufacturer, machine.year].filter(value => value !== null && value !== '').join(' · '))
	const fittedMeta = fitText(meta || 'PINMAME', OG_WIDTH - 160, 3)
	canvas.centeredText(fittedMeta.text, 470, fittedMeta.scale, INK)
	canvas.centeredText('PINMAME MACHINE REFERENCE', 540, 2, MUTED)
	return canvas.encodePng()
}

export function renderPlatformOgCard(platform: { name: string, id: string }): Buffer {
	const canvas = new CardCanvas()
	canvas.panel(wrapDmdTitle(platform.name).lines, 100, 120, PANEL_COLS, PANEL_ROWS, 7.8)
	canvas.centeredText('PINMAME PLATFORM', 470, 3, INK)
	const fittedId = fitText(normalizeDmdText(platform.id), OG_WIDTH - 160, 2)
	canvas.centeredText(fittedId.text, 540, fittedId.scale, MUTED)
	return canvas.encodePng()
}
