import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { test } from 'node:test'
import { extractCompletionNotes } from './completion-notes.ts'
import { COMPLETION_REQUIREMENTS } from '../app/utils/completion.ts'

test('every canonical missing requirement has an action description', () => {
	const schema = JSON.parse(readFileSync(new URL('../../schemas/machine.schema.json', import.meta.url), 'utf8'))
	assert.deepEqual(Object.keys(COMPLETION_REQUIREMENTS).sort(), [...schema.$defs.coverage.properties.missing.items.enum].sort())
})

test('Twilight Zone includes the current playfield and street-lamp survey blockers', () => {
	const report = readFileSync(new URL('../../reports/spatial/bally/twilight-zone-1993.md', import.meta.url), 'utf8')
	const notes = extractCompletionNotes(report)
	assert.ok(notes?.includes('a bulb survey of strings 01 and 05'))
	assert.ok(notes?.includes("a photograph or survey of a stock street lamp's sockets"))
	assert.ok(notes?.includes('## Unresolved spatial evidence'))
	assert.ok(!notes?.includes('Retained evidence'))
})

test('blockers fall back to recorded unresolved details, preserving nested headings and CRLF', () => {
	const report = '# Game\r\n\r\n## Blockers\r\nNeed a bulb survey.\r\n### Evidence needed\r\nCount the sockets.\r\n\r\n## Unresolved records\r\n- Lamp 1\r\n\r\n## Counts\r\n100 placements.\r\n'
	assert.equal(extractCompletionNotes(report), '## Blockers\n\nNeed a bulb survey.\n### Evidence needed\nCount the sockets.\n\n## Unresolved records\n\n- Lamp 1')
})

test('a promotion summary does not hide the evidence needed to resolve each blocker', () => {
	const report = readFileSync(new URL('../../reports/spatial/data-east/time-machine-1988.md', import.meta.url), 'utf8')
	const notes = extractCompletionNotes(report)
	assert.ok(notes?.includes('Keep partial.'))
	assert.ok(notes?.includes('A photographed socket/address survey'))
	assert.ok(notes?.includes('Original-machine captures of each bumper/slingshot switch'))
	assert.ok(!notes?.includes('## Resolver controls'))
})

test('knowledge fallback includes the existing game-specific blocker headings', () => {
	const cases = [
		['stern/twenty-four-2009', 'Suitcase phase causality is incomplete'],
		['stern/avatar-pro-2010', 'Explicit spatial blockers retained'],
		['stern/transformers-limited-edition-2011', 'Starscream, Ironhide'],
		['stern/ripley-s-believe-it-or-not-2004', '## Exact-table spatial evidence and fail-closed blockers'],
		['stern/big-buck-hunter-pro-2010', '## What blocks promotion'],
		['data-east/torpedo-alley-1988', '## What remains unresolved'],
		['bally/judge-dredd-1993', '## Unresolved questions'],
	] as const
	for (const [game, expected] of cases) {
		const knowledge = readFileSync(new URL(`../../knowledge/${game}.md`, import.meta.url), 'utf8')
		assert.ok(extractCompletionNotes(knowledge)?.includes(expected), `${game} must include ${expected}`)
	}
})

test('High Speed spatial report includes its current lamp 40 blocker', () => {
	const report = readFileSync(new URL('../../reports/spatial/williams/high-speed-1986.md', import.meta.url), 'utf8')
	const notes = extractCompletionNotes(report)
	assert.ok(notes?.includes('## Blockers'))
	assert.ok(notes?.includes('Lamp address 40 (Ramp Earns Hideout Jackpot) is a two-bulb circuit'))
	assert.ok(notes?.includes('One bulb is placed; the second has no placement.'))
	assert.ok(notes?.includes('## Promotion decision'))
	const blockers = notes.split('\n\n## Promotion decision')[0]!
	assert.doesNotMatch(blockers, /upper.right flipper|traffic light|stoplight/i)
	assert.ok(!notes?.includes('## Unresolved: which button fires'))
	assert.ok(!notes?.includes('## Spatial gaps that keep this record partial'))
	assert.ok(!notes?.includes('## Retained evidence'))
})

test('spatial gaps and unresolved headings remain supported without matching unrelated gaps', () => {
	const knowledge = '# Game\n\n## Spatial gaps that keep this record partial\nLocate the lamp.\n\n## Unresolved: which button fires\nFind the wiring.\n\n## A gap in the inventory\nAn inventory note.\n'
	assert.equal(extractCompletionNotes(knowledge), '## Spatial gaps that keep this record partial\n\nLocate the lamp.\n\n## Unresolved: which button fires\n\nFind the wiring.')
})

test('absence of completion prose does not invent a blocker', () => {
	assert.equal(extractCompletionNotes('# Game\n\n## Mechanisms\nA motor turns.\n\n## Routes and remaining devices\nMore devices.\n\n## Pinned disagreement, noted but not blocking\nA resolved issue.\n'), null)
})
