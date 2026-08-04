/**
 * Prepares the manufacturer marks in `app/assets/icons` for inlining.
 *
 * They come out of a drawing tool as standalone documents, which is not the
 * same thing as a symbol you can drop into a page several times over. Three
 * problems have to be fixed before they can be:
 *
 *   - **Colour is baked in.** Some carry `fill: #231f20`, and the rest have no
 *     fill at all, so they default to black. Either way they vanish against the
 *     dark theme. Every mark ends up drawn in `currentColor` instead, so it
 *     inherits whatever the surrounding text is using.
 *
 *   - **The class names collide.** Each file styles its shapes with `.cls-1`
 *     via an embedded `<style>`. CSS inside inline SVG is *global*, so with two
 *     marks on the same page the last `.cls-1` wins for both — and since
 *     Midway's is the only one carrying `fill-rule: evenodd`, that is the
 *     difference between a logo and a filled-in blob. The declarations are
 *     moved onto the shapes as presentation attributes and the stylesheet is
 *     dropped.
 *
 *   - **Every file calls its root `id="Layer_1"`.** Duplicate ids in one
 *     document; harmless here, but only by luck.
 *
 * Emits `data/icons.json`. Runs as part of `npm run data`.
 */

import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const projectRoot = resolve(here, '..')
const iconDir = join(projectRoot, 'app/assets/icons')

/** Declarations that describe geometry travel with the shape; colour does not. */
const COLOUR_PROPERTIES = new Set(['fill', 'stroke', 'color', 'stop-color'])

function prepare(name: string, source: string) {
	let svg = source
		.replace(/<\?xml[^>]*\?>\s*/g, '')
		.replace(/<!--[\s\S]*?-->/g, '')
		.trim()

	// class name -> the declarations it carries, colour stripped out
	const rules = new Map<string, Record<string, string>>()
	svg = svg.replace(/<style>([\s\S]*?)<\/style>/g, (_, css: string) => {
		for (const [, selector, body] of css.matchAll(/\.([\w-]+)\s*\{([^}]*)\}/g)) {
			const declarations: Record<string, string> = {}
			for (const part of body!.split(';')) {
				const [property, value] = part.split(':').map(piece => piece.trim())
				if (!property || !value) continue
				if (COLOUR_PROPERTIES.has(property)) continue
				declarations[property] = value
			}
			rules.set(selector!, declarations)
		}
		return ''
	})

	// Anything left in <defs> after the stylesheet is gone would be a gradient or
	// a clip path, which this pass is not equipped to make collision-safe.
	svg = svg.replace(/<defs>\s*<\/defs>\s*/g, '')
	if (/<defs[\s>]/.test(svg))
		console.warn(`[icons] WARNING ${name} keeps a <defs> block — ids inside it are global and may clash`)

	// Fold each class into its element, then drop the attribute.
	svg = svg.replace(/\sclass="([^"]*)"/g, (_, value: string) => {
		const attributes = value
			.split(/\s+/)
			.filter(Boolean)
			.flatMap((selector) => {
				const declarations = rules.get(selector)
				if (!declarations) {
					console.warn(`[icons] WARNING ${name} uses .${selector}, which no rule defines`)
					return []
				}
				return Object.entries(declarations)
			})
		return attributes.map(([property, value]) => ` ${property}="${value}"`).join('')
	})

	svg = svg.replace(/\s(?:id|data-name)="[^"]*"/g, '')

	const viewBox = /viewBox="([^"]*)"/.exec(svg)?.[1]
	if (!viewBox) throw new Error(`[icons] ${name} has no viewBox — it cannot be scaled`)

	// One root, drawn in the inherited colour and hidden from assistive tech:
	// every mark sits next to the name it stands for, so announcing it repeats.
	svg = svg.replace(
		/^<svg[^>]*>/,
		`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${viewBox}" fill="currentColor" aria-hidden="true" focusable="false">`,
	)

	return svg.replace(/>\s+</g, '><').trim()
}

if (!existsSync(iconDir)) {
	console.warn(`[icons] no ${iconDir} — skipping`)
	process.exit(0)
}

const icons: Record<string, string> = {}
for (const file of readdirSync(iconDir).filter(name => name.endsWith('.svg')).sort()) {
	const slug = file.replace(/\.svg$/, '')

	// The filename *is* the key `app/utils/brand.ts` maps to. Anything a
	// duplicate-save or an export dialog leaves behind — "logo copy.svg",
	// "Logo_2.svg" — produces a mark nothing can reference, and silently.
	if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) {
		console.error(`[icons] ${file}: name it in lowercase-kebab-case after the brand, e.g. data-east.svg`)
		process.exit(1)
	}

	icons[slug] = prepare(file, readFileSync(join(iconDir, file), 'utf8'))
}

mkdirSync(join(projectRoot, 'data'), { recursive: true })
writeFileSync(join(projectRoot, 'data', 'icons.json'), JSON.stringify(icons))

const bytes = Object.values(icons).reduce((total, svg) => total + svg.length, 0)
console.log(`[icons] marks         : ${Object.keys(icons).length} (${(bytes / 1024).toFixed(1)} kB) — ${Object.keys(icons).join(', ')}`)
