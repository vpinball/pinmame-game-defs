import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { test } from 'node:test'
import { loadPinballMemoryMaps, PINBALL_MEMORY_MAPS_ATTRIBUTION } from './memory-maps.ts'

const ODBL = 'Open Data Commons Open Database License (ODbL) v1.0'

/** A minimal upstream checkout as a committed Git repository, minus `omit`. */
function fixture(options: { omit?: string[], mapLicense?: string | null } = {}) {
	const root = mkdtempSync(join(tmpdir(), 'memory-maps-'))
	const checkout = join(root, 'checkout')
	const files: Record<string, string> = {
		'index.json': JSON.stringify({ _comment: 'fixture', tz_92: 'maps/wpc/tz.map.json' }),
		'maps/wpc/tz.map.json': JSON.stringify({
			_fileformat: 1,
			_metadata: {
				version: 1,
				platform: 'wpc',
				roms: ['tz_92'],
				...(options.mapLicense === null ? {} : { license: options.mapLicense ?? ODBL }),
			},
			game_state: {},
		}),
		'platforms/wpc.json': JSON.stringify({ name: 'WPC' }),
		'LICENSE-ODbL.md': '## ODC Open Database License (ODbL)\n',
		'LICENSE-DbCL': 'Database Contents License (DbCL)\n',
	}
	for (const path of options.omit ?? []) delete files[path]
	for (const [path, body] of Object.entries(files)) {
		mkdirSync(dirname(join(checkout, path)), { recursive: true })
		writeFileSync(join(checkout, path), body)
	}
	// Inherited GIT_* variables (a test run from a hook exports GIT_DIR and
	// GIT_INDEX_FILE) would point these commands at the outer repository, and
	// user or system config could add hooks or rewrite line endings.
	const env = Object.fromEntries(Object.entries(process.env).filter(([name]) => !name.startsWith('GIT_')))
	Object.assign(env, { GIT_CONFIG_NOSYSTEM: '1', GIT_CONFIG_GLOBAL: join(root, 'empty.gitconfig') })
	writeFileSync(env.GIT_CONFIG_GLOBAL!, '')
	const git = (...args: string[]) => execFileSync('git', [
		'-C', checkout,
		'-c', 'core.autocrlf=false', '-c', 'commit.gpgsign=false',
		'-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
		...args,
	], { encoding: 'utf8', env }).trim()
	git('init', '-q')
	git('add', '-A')
	git('commit', '-q', '--no-verify', '-m', 'fixture')
	return { root, checkout, output: join(root, 'out'), commit: git('rev-parse', 'HEAD') }
}

test('memory maps carry the ODbL/DbCL licences and mirror both texts', () => {
	const { root, checkout, output, commit } = fixture()
	try {
		const data = loadPinballMemoryMaps(checkout, commit, new Set(['tz_92']), output)
		assert.ok(data)
		assert.equal(data.source.license, 'ODbL-1.0')
		assert.equal(data.source.contentsLicense, 'DbCL-1.0')
		assert.equal(data.source.attribution, PINBALL_MEMORY_MAPS_ATTRIBUTION)
		assert.deepEqual(data.source.licenseFiles.map(file => [file.license, file.sourcePath, file.dataUrl]), [
			['ODbL-1.0', 'LICENSE-ODbL.md', 'data/memory-maps/LICENSE-ODbL.md'],
			['DbCL-1.0', 'LICENSE-DbCL', 'data/memory-maps/LICENSE-DbCL'],
		])
		assert.equal(data.source.licenseFiles[0]!.sourceUrl, `https://github.com/tomlogic/pinball-memory-maps/blob/${commit}/LICENSE-ODbL.md`)
		assert.equal(readFileSync(join(output, 'memory-maps', 'LICENSE-ODbL.md'), 'utf8'), '## ODC Open Database License (ODbL)\n')
		assert.equal(readFileSync(join(output, 'memory-maps', 'LICENSE-DbCL'), 'utf8'), 'Database Contents License (DbCL)\n')
		assert.ok(!existsSync(join(output, 'memory-maps', 'LICENSE')))
		assert.equal(data.byDriver.get('tz_92')?.sourcePath, 'maps/wpc/tz.map.json')
	} finally {
		rmSync(root, { recursive: true, force: true })
	}
})

test('the pinned commit is mirrored, never a converted or edited working tree', () => {
	const { root, checkout, output, commit } = fixture()
	try {
		// What a Windows checkout with core.autocrlf=true holds, plus a local edit
		// and a deleted file: none of it is in the commit.
		writeFileSync(join(checkout, 'LICENSE-ODbL.md'), '## ODC Open Database License (ODbL)\r\n')
		writeFileSync(join(checkout, 'maps', 'wpc', 'tz.map.json'), '{"edited": true}')
		rmSync(join(checkout, 'LICENSE-DbCL'))
		const data = loadPinballMemoryMaps(checkout, commit, new Set(['tz_92']), output)
		assert.equal(data?.maps[0]?.sections.join(), 'game_state')
		assert.equal(readFileSync(join(output, 'memory-maps', 'LICENSE-ODbL.md'), 'utf8'), '## ODC Open Database License (ODbL)\n')
		assert.equal(readFileSync(join(output, 'memory-maps', 'LICENSE-DbCL'), 'utf8'), 'Database Contents License (DbCL)\n')
		assert.ok(!readFileSync(join(output, 'memory-maps', 'maps', 'wpc', 'tz.map.json'), 'utf8').includes('edited'))
	} finally {
		rmSync(root, { recursive: true, force: true })
	}
})

for (const missing of ['LICENSE-ODbL.md', 'LICENSE-DbCL']) {
	test(`a checkout without ${missing} fails closed`, () => {
		const { root, checkout, output, commit } = fixture({ omit: [missing] })
		try {
			assert.throws(() => loadPinballMemoryMaps(checkout, commit, new Set(['tz_92']), output), new RegExp(missing.replace('.', '\\.')))
			assert.ok(!existsSync(join(output, 'memory-maps', 'maps')), 'no map is mirrored without both licence texts')
		} finally {
			rmSync(root, { recursive: true, force: true })
		}
	})
}

for (const [label, mapLicense] of [
	['an LGPL', 'GNU Lesser General Public License v3.0'],
	['a mixed', `LGPL-3.0 or ${ODBL}`],
	['no', null],
] as const) {
	test(`a map declaring ${label} licence fails closed`, () => {
		const { root, checkout, output, commit } = fixture({ mapLicense })
		try {
			assert.throws(() => loadPinballMemoryMaps(checkout, commit, new Set(['tz_92']), output), /does not declare the ODbL v1\.0/)
		} finally {
			rmSync(root, { recursive: true, force: true })
		}
	})
}
