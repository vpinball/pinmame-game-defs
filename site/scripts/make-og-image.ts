/**
 * Generates the Open Graph card at `public/og.png`.
 *
 * Links to this site get pasted into Discord, VPForums and VPUniverse far more
 * than they get found through search, so the card is worth more than most SEO
 * tags — and a bare link with no preview is the common case today.
 *
 * The card is drawn as a dot-matrix panel using the same 5x7 WPC-style font the
 * site's hero uses, then encoded as a PNG by hand. Node ships zlib, and PNG is
 * a short enough format that this needs no image dependency at all.
 */
import { deflateSync } from 'node:zlib'
import { mkdirSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { drawText, layoutPanel, textWidth } from '../app/utils/dmdfont'

const WIDTH = 1200
const HEIGHT = 630

type RGB = [number, number, number]

const BACKDROP: RGB = [0x0a, 0x0b, 0x0d]
const DOT_OFF: RGB = [0x1a, 0x1d, 0x22]
const DOT_ON: RGB = [0xff, 0x8a, 0x1e]
const INK: RGB = [0xe9, 0xec, 0xf1]
const MUTED: RGB = [0x6b, 0x75, 0x83]

const pixels = Buffer.alloc(WIDTH * HEIGHT * 3)

function fill(colour: RGB) {
	for (let i = 0; i < WIDTH * HEIGHT; i++) {
		pixels[i * 3] = colour[0]
		pixels[i * 3 + 1] = colour[1]
		pixels[i * 3 + 2] = colour[2]
	}
}

function blend(x: number, y: number, colour: RGB, alpha: number) {
	if (x < 0 || y < 0 || x >= WIDTH || y >= HEIGHT || alpha <= 0) return
	const i = (y * WIDTH + x) * 3
	for (let c = 0; c < 3; c++) {
		pixels[i + c] = Math.round(pixels[i + c]! * (1 - alpha) + colour[c]! * alpha)
	}
}

/** A round dot with a soft edge, the way a plasma DMD pixel actually looks. */
function dot(cx: number, cy: number, radius: number, colour: RGB, glow = 0) {
	const reach = Math.ceil(radius + glow)
	for (let y = -reach; y <= reach; y++) {
		for (let x = -reach; x <= reach; x++) {
			const distance = Math.hypot(x, y)
			let alpha = 0
			if (distance <= radius) alpha = 1
			else if (distance <= radius + 1) alpha = radius + 1 - distance
			else if (glow && distance <= radius + glow) alpha = 0.22 * (1 - (distance - radius) / glow)
			blend(Math.round(cx + x), Math.round(cy + y), colour, alpha)
		}
	}
}

/** Renders one dot-matrix panel: lit text on a grid of unlit dots. */
function panel(lines: string[], originX: number, originY: number, cols: number, rows: number, cell: number) {
	const { grid } = layoutPanel(lines, cols, rows)
	for (let row = 0; row < rows; row++) {
		for (let col = 0; col < cols; col++) {
			const lit = grid[row]![col]
			dot(originX + col * cell + cell / 2, originY + row * cell + cell / 2, cell * 0.34, lit ? DOT_ON : DOT_OFF, lit ? cell * 0.9 : 0)
		}
	}
}

/** Small solid-block text for the strapline, drawn from the same font. */
function blockText(text: string, originX: number, originY: number, scale: number, colour: RGB) {
	const grid: boolean[][] = Array.from(
		{ length: 7 * scale + 2 },
		() => Array.from({ length: textWidth(text, scale) + 2 }, () => false),
	)
	drawText(grid, text, 0, 0, scale)
	for (let y = 0; y < grid.length; y++) {
		for (let x = 0; x < grid[y]!.length; x++) {
			if (grid[y]![x]) blend(originX + x, originY + y, colour, 1)
		}
	}
	return textWidth(text, scale)
}

function encodePng(): Buffer {
	// One filter byte (0 = None) in front of every scanline.
	const raw = Buffer.alloc((WIDTH * 3 + 1) * HEIGHT)
	for (let y = 0; y < HEIGHT; y++) {
		raw[y * (WIDTH * 3 + 1)] = 0
		pixels.copy(raw, y * (WIDTH * 3 + 1) + 1, y * WIDTH * 3, (y + 1) * WIDTH * 3)
	}

	const crcTable = Array.from({ length: 256 }, (_, n) => {
		let c = n
		for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1
		return c >>> 0
	})
	const crc = (buf: Buffer) => {
		let c = 0xFFFFFFFF
		for (const byte of buf) c = crcTable[(c ^ byte) & 0xFF]! ^ (c >>> 8)
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
	ihdr.writeUInt32BE(WIDTH, 0)
	ihdr.writeUInt32BE(HEIGHT, 4)
	ihdr[8] = 8 // bit depth
	ihdr[9] = 2 // colour type: truecolour
	return Buffer.concat([
		Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
		chunk('IHDR', ihdr),
		chunk('IDAT', deflateSync(raw, { level: 9 })),
		chunk('IEND', Buffer.alloc(0)),
	])
}

fill(BACKDROP)

// Warm glow behind the panel, as if the backbox were lit.
for (let y = 0; y < HEIGHT; y++) {
	for (let x = 0; x < WIDTH; x++) {
		const d = Math.hypot(x - WIDTH / 2, y - 210) / 520
		if (d < 1) blend(x, y, [0xff, 0x7a, 0x18], 0.14 * (1 - d) ** 2)
	}
}

panel(['PINMAME', 'MACHINE REFERENCE'], 100, 120, 128, 32, 7.8)

const strapline = 'EVERY SWITCH, LAMP AND COIL PINMAME CAN TALK TO'
blockText(strapline, Math.round((WIDTH - textWidth(strapline, 3)) / 2), 470, 3, INK)

const footer = 'SWITCH MAPS / WIRING / MECHANISMS / EVIDENCE'
blockText(footer, Math.round((WIDTH - textWidth(footer, 2)) / 2), 540, 2, MUTED)

const out = join(resolve(dirname(fileURLToPath(import.meta.url)), '..'), 'public', 'og.png')
mkdirSync(dirname(out), { recursive: true })
writeFileSync(out, encodePng())
console.log(`[og]   wrote ${WIDTH}x${HEIGHT} card -> public/og.png`)
