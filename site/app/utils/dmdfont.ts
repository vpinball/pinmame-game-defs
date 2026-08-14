/**
 * A 5×7 bitmap font in the style of the Bally/Williams WPC system font.
 *
 * Rasterising a vector typeface onto a 128×32 panel and thresholding it gives
 * mushy, uneven glyphs — real DMD text is authored pixel by pixel. Each glyph
 * below is exactly that: seven rows of five cells, so what the panel shows is
 * what was drawn.
 */

export const GLYPH_WIDTH = 5
export const GLYPH_HEIGHT = 7
export const TRACKING = 1

const GLYPHS: Record<string, string> = {
	A: '.###.|#...#|#...#|#####|#...#|#...#|#...#',
	B: '####.|#...#|#...#|####.|#...#|#...#|####.',
	C: '.###.|#...#|#....|#....|#....|#...#|.###.',
	D: '####.|#...#|#...#|#...#|#...#|#...#|####.',
	E: '#####|#....|#....|####.|#....|#....|#####',
	F: '#####|#....|#....|####.|#....|#....|#....',
	G: '.###.|#...#|#....|#.###|#...#|#...#|.###.',
	H: '#...#|#...#|#...#|#####|#...#|#...#|#...#',
	I: '#####|..#..|..#..|..#..|..#..|..#..|#####',
	J: '....#|....#|....#|....#|....#|#...#|.###.',
	K: '#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#',
	L: '#....|#....|#....|#....|#....|#....|#####',
	M: '#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#',
	N: '#...#|##..#|#.#.#|#..##|#...#|#...#|#...#',
	O: '.###.|#...#|#...#|#...#|#...#|#...#|.###.',
	P: '####.|#...#|#...#|####.|#....|#....|#....',
	Q: '.###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#',
	R: '####.|#...#|#...#|####.|#.#..|#..#.|#...#',
	S: '.####|#....|#....|.###.|....#|....#|####.',
	T: '#####|..#..|..#..|..#..|..#..|..#..|..#..',
	U: '#...#|#...#|#...#|#...#|#...#|#...#|.###.',
	V: '#...#|#...#|#...#|#...#|#...#|.#.#.|..#..',
	W: '#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#',
	X: '#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#',
	Y: '#...#|#...#|.#.#.|..#..|..#..|..#..|..#..',
	Z: '#####|....#|...#.|..#..|.#...|#....|#####',

	0: '.###.|#...#|#..##|#.#.#|##..#|#...#|.###.',
	1: '..#..|.##..|..#..|..#..|..#..|..#..|.###.',
	2: '.###.|#...#|....#|...#.|..#..|.#...|#####',
	3: '#####|...#.|..##.|....#|....#|#...#|.###.',
	4: '...#.|..##.|.#.#.|#..#.|#####|...#.|...#.',
	5: '#####|#....|####.|....#|....#|#...#|.###.',
	6: '..##.|.#...|#....|####.|#...#|#...#|.###.',
	7: '#####|....#|...#.|..#..|.#...|.#...|.#...',
	8: '.###.|#...#|#...#|.###.|#...#|#...#|.###.',
	9: '.###.|#...#|#...#|.####|....#|...#.|.##..',

	' ': '.....|.....|.....|.....|.....|.....|.....',
	'·': '.....|.....|.....|..#..|.....|.....|.....',
	'.': '.....|.....|.....|.....|.....|.....|..#..',
	',': '.....|.....|.....|.....|.....|..#..|.#...',
	'-': '.....|.....|.....|#####|.....|.....|.....',
	':': '.....|..#..|..#..|.....|..#..|..#..|.....',
	'/': '....#|....#|...#.|..#..|.#...|#....|#....',
	'×': '.....|.....|#...#|.#.#.|..#..|.#.#.|#...#',
	'!': '..#..|..#..|..#..|..#..|..#..|.....|..#..',
	'?': '.###.|#...#|....#|..##.|..#..|.....|..#..',
	'\'': '..#..|..#..|.....|.....|.....|.....|.....',
	'+': '.....|..#..|..#..|#####|..#..|..#..|.....',
	'%': '##..#|##..#|...#.|..#..|.#...|#..##|#..##',
	'&': '.##..|#..#.|#.#..|.##..|#.#.#|#..#.|.##.#',
	'(': '...#.|..#..|.#...|.#...|.#...|..#..|...#.',
	')': '.#...|..#..|...#.|...#.|...#.|..#..|.#...',
	'#': '.#.#.|#####|.#.#.|.#.#.|#####|.#.#.|.....',
	'*': '.....|#.#.#|.###.|#####|.###.|#.#.#|.....',
}

const UNKNOWN = GLYPHS[' ']!

const cache = new Map<string, boolean[][]>()

/** Seven rows of five booleans for one character. */
export function glyph(char: string): boolean[][] {
	const key = char.toUpperCase()
	let bitmap = cache.get(key)
	if (!bitmap) {
		bitmap = (GLYPHS[key] ?? UNKNOWN).split('|').map(row => [...row].map(cell => cell === '#'))
		cache.set(key, bitmap)
	}
	return bitmap
}

export const textWidth = (text: string, scale: number) =>
	text.length ? (text.length * GLYPH_WIDTH + (text.length - 1) * TRACKING) * scale : 0

/**
 * Stamps a string into a lit-pixel grid at integer scale. Integer scaling is
 * the only kind a dot-matrix panel can actually do — every lit dot stays a dot.
 */
export function drawText(grid: boolean[][], text: string, originX: number, originY: number, scale: number) {
	let x = originX
	for (const char of text) {
		const bitmap = glyph(char)
		for (let row = 0; row < GLYPH_HEIGHT; row++) {
			for (let col = 0; col < GLYPH_WIDTH; col++) {
				if (!bitmap[row]![col]) continue
				for (let dy = 0; dy < scale; dy++) {
					const targetRow = grid[originY + row * scale + dy]
					if (!targetRow) continue
					for (let dx = 0; dx < scale; dx++) {
						const targetX = x + col * scale + dx
						if (targetX >= 0 && targetX < targetRow.length) targetRow[targetX] = true
					}
				}
			}
		}
		x += (GLYPH_WIDTH + TRACKING) * scale
	}
}

export interface PanelLayout {
	/** `rows` x `cols` of lit pixels. */
	grid: boolean[][]
	/** Integer scale chosen per line. */
	scales: number[]
}

/**
 * Lays a stack of lines onto a panel, giving each the largest integer scale it
 * fits at and then shrinking the biggest until the whole stack fits the height.
 * A real display driver picks between its small and large fonts the same way.
 *
 * Shared by the hero panel and the Open Graph card so they cannot drift.
 */
export function layoutPanel(
	lines: string[],
	cols: number,
	rows: number,
	{ marginX = 6, lineGap = 2, maxScale = 3 } = {},
): PanelLayout {
	const usableWidth = cols - marginX * 2
	const scales = lines.map((line) => {
		for (let scale = maxScale; scale > 1; scale--) {
			if (textWidth(line, scale) <= usableWidth) return scale
		}
		return 1
	})

	const stackHeight = () =>
		scales.reduce((sum, scale) => sum + GLYPH_HEIGHT * scale, 0) + lineGap * (lines.length - 1)

	while (stackHeight() > rows - 2) {
		const biggest = scales.indexOf(Math.max(...scales))
		if (scales[biggest]! <= 1) break
		scales[biggest]!--
	}

	const grid: boolean[][] = Array.from({ length: rows }, () => Array.from({ length: cols }, () => false))
	let y = Math.max(0, Math.round((rows - stackHeight()) / 2))

	lines.forEach((line, index) => {
		const scale = scales[index]!
		// Drop trailing characters rather than overflow if even 1x is too wide.
		let text = line
		while (text.length && textWidth(text, scale) > usableWidth) text = text.slice(0, -1)
		drawText(grid, text, Math.round((cols - textWidth(text, scale)) / 2), y, scale)
		y += GLYPH_HEIGHT * scale + lineGap
	})

	return { grid, scales }
}
