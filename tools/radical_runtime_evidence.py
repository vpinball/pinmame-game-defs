"""Build compact Radical service-test evidence from retained, hash-pinned traces.

Set PINMAME_REVIEW_ARTIFACTS_ROOT to the working root's review-artifacts directory.
The external bundle is assembled separately and never contains ROM bytes. Each frame
digest is SHA-256 of compact ASCII JSON containing the cited raw segment rows in order,
as implemented by ``s11_alpha_evidence.frame_digest``. ``--check`` verifies
the bundle, scenarios, frame readings and generated records without writing.
``--draft-frame-readings`` prints candidate readings for inspection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path[:0] = [str(TOOLS), str(ROOT / 'src')]
import build_external_evidence_manifest as manifests
import s11_alpha_evidence as alpha
from pinmame_game_defs.jsonio import canonical_bytes

REVISION = '46e1a01a0f73dc5ce163d98db1ae435883ecc450'
LIBRARY = '8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5'
MACHINES = {'radcl_l1': 'bally.radical.1990', 'radcl_g1': 'bally.radical.1990',
            'radcl_p3': 'bally.radical-prototype.1990'}
GAMES = ('radcl_l1', 'radcl_g1', 'radcl_p3')
NAMES = ('nvram-init', 'coil-test', 'single-lamps', 'switch-levels')
ROM_HASHES = {
    'radcl_l1': 'e5ec9cce808645ad94200a7cab015d416396c51b31412b9f551a533f84ea707d',
    'radcl_g1': '1c55d6317e95c932f4cf6d5d0e0501d8f6190bf441047d80cc1a9400e9eeab1d',
    'radcl_p3': '3e87bba4b1428bef2bd2d35e90e88b20b8efb8bb3278f437beed5aedf7708d02',
}
ROM_MEMBERS = {
    'radcl_l1': [('rad_u26.l1', 'dd01fb9189acd2620c57149921aadb051f7a2412'), ('rad_u27.l1', 'a61055aab97d3fe2ecd0ed4281a9681b1d910269'), ('rad_u4.l1', '27984bbc91dc7593e6a5b42f74dd6ddf58189bec'), ('rad_u19.l1', 'bdeea7517f2adf72b4b642bffb25ba5b98453127'), ('rad_u20.l1', '7da0289cf0a0c93768c0706fdedfc3a5f2101e77')],
    'radcl_g1': [('rad_u26.l1', 'dd01fb9189acd2620c57149921aadb051f7a2412'), ('u27-lg1.rom', 'ff44deded1686cfa0351c4499485d6eb4561cbc1'), ('rad_u4.l1', '27984bbc91dc7593e6a5b42f74dd6ddf58189bec'), ('rad_u19.l1', 'bdeea7517f2adf72b4b642bffb25ba5b98453127'), ('rad_u20.l1', '7da0289cf0a0c93768c0706fdedfc3a5f2101e77')],
    'radcl_p3': [('rad_u26.p1', '4ea6945fa5cfbd33fcdf780814b0bf5cb3faa388'), ('u27-p1.rom', 'b1bd5d8a93f1ab9fb9bf5c268d8530be438448e6'), ('rad_u4.p3', '7ebcc1503fc322909d32c7c8bda8c0b6505919b3'), ('rad_u19.l1', 'bdeea7517f2adf72b4b642bffb25ba5b98453127'), ('rad_u20.p3', '0691a80672fc11d46359f710bd211de7a59de346')],
}
INIT_HASHES = {
    'radcl_l1': '7d41c69401646cc09408618a53b1f5560f536ed02748f4d71c5e73e8b0e42be5',
    'radcl_g1': 'b0e3aaffe09e7a83c0c32800b604c9f97df29c7a018902efe6c037574a2eceb5',
    'radcl_p3': 'd93b2dd53bf5a779fe1b9e36e495a3f906295c6e2d9133544d7ac7d128456815',
    'repeat-g1': '78dfb2dcfa5ea9baf0014d1084fc7e375be99338ce64536cc011ed09dbc469cd',
}
RAW_HASHES = {
    'radcl_l1/nvram-init': 'cf421736f6ea2079d7882512def381bd81bf768143ed6ed978fc36871766ee7c',
    'radcl_l1/coil-test': '31ecb3514379ceaf3042ca5e38914cae02678a0b6479a12f0a26b013d9c3f12d',
    'radcl_l1/single-lamps': '57de982fba7a27e81ed67ca3c254d9e20c10e7386a599c9c015be2a09cc70dd3',
    'radcl_l1/switch-levels': '05bbffaad874ba3529996bd9481b90a86d9cf2b3e83c8b3e6277b89c3ef0ce5c',
    'radcl_g1/nvram-init': 'fa83130b9814d9727d58befba4a481edd5eaad8f3a8d08d25ae09d5e2c513a5f',
    'radcl_g1/coil-test': 'dc3aadde27652046c24c14b63990905841a91b547263a8e6afb1028761bbd34c',
    'radcl_g1/single-lamps': '8f3ea8ef150cb65c809bfb7814b86022505bccc8ae96ef38fc6425ca0708f09d',
    'radcl_g1/repeat-nvram-init': 'f864c5742947255cbd095df022e661df319d0d745f1d782c763c522c3fcd6c37',
    'radcl_g1/switch-levels': '4632bcd60b25ca4fae0f9a4ec2f0c6d8d7a2da6ac574ddcdfb728ea0ec1bddd9',
    'radcl_p3/nvram-init': '100ec7f21b8d80c24f4ecc4a90147b13f9f992c9d8f531f7a744c7bc4991b0af',
    'radcl_p3/coil-test': 'ba089ebcae3821960c30b66dba24f59d0ad51c55a45afa6852024dc3a5171267',
    'radcl_p3/single-lamps': '213d3823c51f36833981032a31b0f1607399fe873db77126ebd4d9a72ea78b43',
    'radcl_p3/switch-levels': '92d85a20296116320f5e2591b74e530b33ae511a8ebdd9d78a6f2fddc9b94eec',
}
SCENARIO_DIR = Path('tools/harness-scenarios/system-11')
SEED = ROOT / 'tools/seeds/bally/radical-1990-frame-readings.json'
BUNDLE_RELATIVE = Path('radical-1990/curation-20261106/session/terra-runtime/bundle')
SOURCE = 'external:pinmame-review-artifacts/' + BUNDLE_RELATIVE.as_posix()
MANIFEST_DESCRIPTION = (
    'SHA-256 of exact manifest.json bytes. tools/build_external_evidence_manifest.py builds compact '
    'UTF-8 JSON with sorted keys and one LF, listing every file recursively by case-sensitive POSIX '
    'relative path, size and SHA-256, excluding manifest.json and manifest.sha256.'
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scenario_path(game: str, name: str) -> Path:
    suffix = ('g1-switch-levels' if game == 'radcl_g1' and name == 'switch-levels'
              else 'nvram-init' if name == 'repeat-nvram-init' else name)
    return SCENARIO_DIR / f'radcl-{suffix}.json'


def raw_path(bundle: Path, game: str, name: str) -> Path:
    if game == 'radcl_g1' and name == 'repeat-nvram-init':
        return bundle / 'repeat/runs/nvram-init.json'
    if game == 'radcl_g1' and name == 'switch-levels':
        return bundle / 'repeat/runs/switch-levels.json'
    return bundle / f'original/runs/{game}-{name}.json'


def load_run(bundle: Path, game: str, name: str) -> dict[str, Any]:
    key = f'{game}/{name}'
    path = raw_path(bundle, game, name)
    if sha(path) != RAW_HASHES[key]:
        raise ValueError(f'{key}: raw run digest mismatch')
    run = json.loads(path.read_bytes())
    if run.get('failure') is not None or run.get('game') != game or run.get('library_sha256') != LIBRARY:
        raise ValueError(f'{key}: unsuccessful run or unexpected game or library')
    scenario = ROOT / scenario_path(game, name)
    if sha(scenario) != run['scenario']['sha256']:
        raise ValueError(f'{key}: scenario drift: {scenario}')
    if len(run['steps']) != run['scenario']['action_count']:
        raise ValueError(f'{key}: incomplete action sequence')
    return run


class Readings:
    def __init__(self, key: str, pins: dict[str, Any], draft: bool):
        self.key, self.pins, self.draft, self.seen = key, pins, draft, set()

    def read(self, label: str, *rows: list[int]) -> list[str]:
        if not rows or any(not row for row in rows):
            raise ValueError(f'{self.key}: missing display frame {label}')
        readings = [alpha.decode_alpha(row) for row in rows]
        entry = {'segments_sha256': alpha.frame_digest(*rows), 'readings': readings}
        if self.draft:
            self.pins[label] = entry
        elif self.pins.get(label) != entry:
            raise ValueError(f'{self.key}: frame-reading mismatch at {label}')
        self.seen.add(label)
        return readings

    def finish(self) -> None:
        if self.seen != set(self.pins):
            raise ValueError(f'{self.key}: pinned frame set differs from cited frame set')


def title(run: dict[str, Any], game: str, name: str, pins: Readings) -> float:
    expected = {
        'coil-test': 'SPULEN TEST' if game == 'radcl_g1' else 'COIL TEST',
        'single-lamps': 'EINZEL LAMPEN' if game == 'radcl_g1' else 'SINGLE LAMPS',
        'switch-levels': 'GESCHLO. KONTAKT' if game == 'radcl_g1' else 'SWITCH LEVELS',
    }[name]
    checkpoint = next((s for s in run['steps'] if s['type'] == 'pulse_until_display'), None)
    target = {'coil-test': ('SPULEN' if game == 'radcl_g1' else 'COIL'),
              'single-lamps': ('EINZEL' if game == 'radcl_g1' else 'SINGLE'),
              'switch-levels': ('GESCHL' if game == 'radcl_g1' else 'LEVELS')}[name]
    if not checkpoint or checkpoint['matched_text'] != target:
        raise ValueError(f'{game}/{name}: unexpected language or menu checkpoint')
    for time, segments in alpha.row_timeline(run, 0):
        if alpha.decode_alpha(segments).strip() == expected:
            pins.read('menu title', segments)
            return time
    raise ValueError(f'{game}/{name}: expected title frame not present: {expected}')


def coils(run: dict[str, Any], start: float, pins: Readings) -> list[dict[str, Any]]:
    rows = alpha.row_timeline(run, 0)
    hits = []
    relay_active = False
    relay_rise = -1.0
    previous_c_rise = -1.0
    for event in run['events']:
        if event['event'] == 'solenoid' and event['number'] == 12:
            relay_active = bool(event['state'])
            if relay_active:
                relay_rise = event['time_s']
        if event['event'] != 'solenoid' or not event['state'] or event['time_s'] <= start or event['number'] == 23:
            continue
        if event['number'] in range(25, 33):
            if not relay_active:
                raise ValueError(f"coil test: C-side output {event['number']} rose while relay 12 was off")
            if relay_rise <= previous_c_rise:
                raise ValueError('coil test: C-side output lacks a preceding relay rise')
            previous_c_rise = event['time_s']
        frame = alpha.frame_at(rows, event['time_s'])
        text = alpha.decode_alpha(frame).strip()
        if event['number'] == 12 and text != 'A/C SELECT':
            continue
        hits.append((event['number'], text, frame))
    period = next((i for i in range(3, len(hits)) if hits[i][0] == hits[0][0]), None)
    if period is None or len(hits) < 2 * period or [(x[0], x[1]) for x in hits[:period]] != [(x[0], x[1]) for x in hits[period:2 * period]]:
        raise ValueError('coil test: two matching complete output/name cycles required')
    result = []
    for i in range(period):
        number, text, row = hits[i]
        pins.read(f'coil {i+1:02d} cycle 1', row)
        pins.read(f'coil {i+1:02d} cycle 2', hits[i+period][2])
        result.append({'step': i + 1, 'address': number, 'display': text})
    return result


def lamps(run: dict[str, Any], start: float, pins: Readings) -> list[dict[str, Any]]:
    rows = alpha.row_timeline(run, 0)
    begin = next(t for t, row in rows if t > start and alpha.decode_alpha(row).strip() not in ('SINGLE LAMPS', 'EINZEL LAMPEN'))
    presses = [e['time_s'] for e in run['events'] if e['event'] == 'switch' and e.get('number') == 3 and e.get('state') == 1]
    steps = [s for s in run['steps'] if s.get('label', '').startswith(('Credit: step to designator', 'first lamp'))]
    bounds = [begin] + presses
    if len(steps) != 64 or len(bounds) != 65:
        raise ValueError('single lamps: incomplete stepping sequence')
    pairs = []
    for i, step in enumerate(steps):
        number = 1 if i == 0 else int(step['label'].rsplit(' ', 1)[1])
        if number != i + 1:
            raise ValueError('single lamps: unexpected step order')
        a, b = bounds[i] + .3, bounds[i+1]
        lit = sorted({e['number'] for e in run['events'] if e['event'] == 'lamp' and e['state'] and a <= e['time_s'] < b})
        if lit != [number]:
            raise ValueError(f'single lamps {number}: active addresses {lit}')
        row = alpha.longest_frame(rows, a, b)
        text = pins.read(f'lamp {number:02d}', row)[0].strip()
        pairs.append({'step': number, 'address': lit[0], 'display': text})
    return pairs


def switches(run: dict[str, Any], pins: Readings) -> list[dict[str, Any]]:
    results = []
    for step in run['steps']:
        label = step.get('label', '')
        if not label.startswith('hold public switch '):
            continue
        number = int(label.rsplit(' ', 1)[1])
        snapshots = [s for s in run['snapshots'] if s['label'] == label + ' (held)']
        if len(snapshots) != 1 or step.get('switch') != number:
            raise ValueError(f'switch {number}: missing unique held snapshot')
        rows = {d['index']: d['segments'] for d in snapshots[0]['displays'] if d['index'] in (0, 1)}
        readings = pins.read(f'switch {number} held', rows[0], rows[1])
        results.append({'address': number, 'upper': readings[0].strip(), 'lower': readings[1].strip()})
    if [r['address'] for r in results] != [*range(1, 65), *range(81, 89)]:
        raise ValueError('switch levels: incomplete held-address sweep')
    return results


def service(run: dict[str, Any], game: str, name: str, pins: Readings) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    start = title(run, game, name, pins)
    checkpoints = alpha.checkpoints(run)
    if name == 'coil-test':
        pairs = coils(run, start, pins)
        note = f"Coil Test: {len(pairs)} steps matched across two cycles. Step: public solenoid address = displayed label: " + '; '.join(f"{p['step']}:{p['address']} = {p['display']}" for p in pairs) + '. Relay 12 rises ahead of C-side pulses and is included as a step only when its own A/C SELECT label is displayed.'
        observation = {'diagnostic_checkpoints': checkpoints, 'ordered_solenoid_on_sequence': [p['address'] for p in pairs], 'note': note, 'limitation': 'A transition is ROM activity under the recorded conditions; it does not establish a fitted load, polarity, or physical identity.'}
    elif name == 'single-lamps':
        pairs = lamps(run, start, pins)
        note = f"Single Lamps: {len(pairs)} steps. Step: active public lamp address = displayed label: " + '; '.join(f"{p['step']}:{p['address']} = {p['display']}" for p in pairs) + '.'
        observation = {'diagnostic_checkpoints': checkpoints, 'note': note, 'limitation': 'A matrix output does not prove a physical lamp is fitted.'}
    else:
        pairs = switches(run, pins)
        note = f"Host held {len(pairs)} public addresses one at a time at level 1; held-snapshot upper / lower display: " + '; '.join(f"{p['address']} = {p['upper']} / {p['lower']}" for p in pairs) + '.'
        observation = {'diagnostic_checkpoints': checkpoints, 'note': note, 'limitation': 'Host writes and their readback are stimulus, not ROM observations. A snapshot can retain an earlier name or reflect another input; it does not prove switch fitment, polarity, or every switch state.'}
        observation['named_action_observations'] = switch_causal_observations(run, game)
    observation['note'] += ' Decoded from raw segments: 1 is 0x0006 and bit 15 is a period; 0/O and 5/S share glyphs and are shown as O and S. Outer display padding is trimmed; the frame-reading seed retains the full decoded rows and their segment digests.'
    return observation, pairs


def switch_causal_observations(run: dict[str, Any], game: str) -> list[dict[str, Any]]:
    """Pair isolated score-contact stimuli with the ROM's actual driver pulses."""
    expected = {50: 22, 52: 17, 53: 19, 54: 21, 55: 18, 56: 20}
    if game == 'radcl_p3':
        expected[49] = 15
    observations = []
    for switch, coil in expected.items():
        steps = [s for s in run['steps'] if s.get('label') == f'hold public switch {switch}' and s.get('switch') == switch]
        if len(steps) != 1:
            raise ValueError(f'causal switch {switch}: missing isolated step')
        transitioned = sorted(t['number'] for t in steps[0]['transitions']['solenoids'] if any(t['states']))
        if transitioned != [coil]:
            raise ValueError(f'causal switch {switch}: expected only driver {coil}, saw {transitioned}')
        observations.append({'label': f'Switch Levels closure {switch} pulses driver {coil}',
                             'input_kind': 'switch', 'input_address': switch,
                             'observed_switch_addresses': [], 'host_stimulus_switch_addresses': [switch],
                             'transitioned_solenoid_addresses': transitioned, 'result': 'observed'})
    return observations


def raw_entry(bundle: Path, game: str, name: str, run: dict[str, Any]) -> dict[str, Any]:
    original = f'radical-1990/runtime/runs/{game}-{name}.json'
    repeat = game == 'radcl_g1' and name in ('switch-levels', 'repeat-nvram-init')
    init_hash = INIT_HASHES['repeat-g1' if repeat else game]
    initialization = (
        (f'Fresh empty state directory produced radcl_g1.nv, SHA-256 {init_hash}.' if name == 'repeat-nvram-init' else
         f"Fresh isolated repeat inherited only the repeat initialization's radcl_g1.nv, SHA-256 {init_hash}; the copy was checked before the sweep.") if repeat else
        f"The retained initialization run's {game}.nv has SHA-256 {init_hash}. "
        'The recorded scenario says later isolated runs copied that file; the old traces do not record the pre-run copy hash.'
    )
    return {
        'name': name,
        'sha256': sha(raw_path(bundle, game, name)),
        'scenario_path': scenario_path(game, name).as_posix(),
        'scenario_sha256': run['scenario']['sha256'],
        'action_count': run['scenario']['action_count'],
        'watch_switches': run['watch_switches'],
        'self_test_pulses': alpha.service_pulses(run),
        'snapshot_count': len(run['snapshots']),
        'nvram_initialization': initialization,
        'retained_from': (f'radical-1990/curation-20261106/session/terra-runtime/g1-repeat-01/runs/{"nvram-init" if name == "repeat-nvram-init" else name}.json' if repeat else original),
    }


def evidence_record(game: str, manifest: bytes, entries: list[dict[str, Any]], observations: dict[str, Any]) -> dict[str, Any]:
    return {
        'format': 'pinmame-machine-evidence', 'version': 1,
        'extractor': {'id': 'radical-runtime-service', 'version': 1},
        'source': {'kind': 'runtime_scenario', 'repository': 'https://github.com/vpinball/pinmame',
                   'revision': REVISION, 'path': SOURCE, 'sha256': hashlib.sha256(manifest).hexdigest(),
                   'license': 'NOASSERTION', 'quality': 'observed', 'manifest_algorithm': MANIFEST_DESCRIPTION,
                   'attribution': 'Generated from pinned PinMAME and user-authorized ROMs; ROMs and NVRAM remain external.'},
        'driver_ids': [game], 'machine_ids': [MACHINES[game]], 'switches': [], 'outputs': [], 'states': [],
        'mechanisms': [], 'recreation_notes': [],
        'runtime': {
            'game': game, 'rom_archive_sha256': ROM_HASHES[game],
            'emulator': {'binary': 'pinmame64.dll', 'sha256': LIBRARY, 'built_from_revision': REVISION},
            'raw_runs': entries,
            'command_template': 'python -B tools/run_pinmame_harness.py --library <pinned-library> --game <set> --rom-path <authorized-rom-root> --work-dir <new-isolated-state> --scenario <committed-scenario> --boot-wait <seconds> --output <external-run.json>. The retained German repeat used --boot-wait 0; the older traces do not record the boot-wait argument. Initialization and NVRAM provenance are recorded per run.',
            'observations': observations,
        },
    }


def initialization_observation(run: dict[str, Any], game: str) -> dict[str, str]:
    rises = [e for e in run['events'] if e['event'] == 'solenoid' and 9 <= e['number'] <= 16 and e['state']][:8]
    falls = [e for e in run['events'] if e['event'] == 'solenoid' and 9 <= e['number'] <= 16 and not e['state']][:8]
    if [e['number'] for e in rises] != list(range(9, 17)) or [e['number'] for e in falls] != list(range(9, 17)):
        raise ValueError('initialization lacks the controlled-driver byte transient')
    # Native callbacks serialize the eight bits, with microseconds between them.
    # This 1ms trace-clustering bound is not a machine response-time measurement.
    if any(events[-1]['time_s'] - events[0]['time_s'] >= 0.001 for events in (rises, falls)) or rises[-1]['time_s'] >= falls[0]['time_s']:
        raise ValueError('initialization byte transitions are not one rise/clear cluster')
    return {'note': 'Retained initialization run. The controlled-driver byte 9-16 rises together then clears at power-up; output15 is part of this whole-byte transient, not proof of a fitted top sling. First rise/clear host times are ' + str(rises[0]['time_s']) + '/' + str(falls[0]['time_s']) + ' seconds. ROM archive members checked against src/wpc/s11games.c SHA-1: ' + '; '.join(f'{n} {h}' for n, h in ROM_MEMBERS[game]) + '.'}


def build(review_root: Path, draft: bool = False) -> tuple[bytes, dict[str, Any], dict[str, Any]]:
    bundle = review_root / BUNDLE_RELATIVE
    failed = bundle / 'original/runs/radcl_g1-switch-levels.json'
    if sha(failed) != 'e6a8cc722485d25b3038887063eed41058ab476587b823aa99e5497911e1a922':
        raise ValueError('original German failed trace digest mismatch')
    manifest = manifests.canonical_bytes(manifests.build_manifest(bundle, 'radcl_l1')) + b'\n'
    saved = {} if draft else json.loads(SEED.read_bytes())['runs']
    records, drafted, all_pairs = {}, {}, {}
    for game in GAMES:
        entries, observations, pairs_by_name = [], {}, {}
        nv = bundle / f'original/initial-nvram/{game}.nv'
        if sha(nv) != INIT_HASHES[game]:
            raise ValueError(f'{game}: initialization NVRAM digest mismatch')
        for name in NAMES:
            run = load_run(bundle, game, name)
            entries.append(raw_entry(bundle, game, name, run))
            if name == 'nvram-init':
                observations[name] = initialization_observation(run, game)
                continue
            key = f'{game}/{name}'
            pins = Readings(key, {} if draft else saved.get(key, {}), draft)
            observation, pairs = service(run, game, name, pins)
            pins.finish()
            drafted[key] = pins.pins
            observations[name], pairs_by_name[name] = observation, pairs
        if game == 'radcl_g1':
            repeated_init = load_run(bundle, game, 'repeat-nvram-init')
            entries.append(raw_entry(bundle, game, 'repeat-nvram-init', repeated_init))
            observations['repeat-nvram-init'] = {'note': 'Fresh empty-state initialization for the German switch sweep; its NVRAM was copied and hashed before that sweep.'}
        all_pairs[game] = pairs_by_name
        records[game] = (entries, observations)
    if sha(bundle / 'repeat/initial-nvram/radcl_g1.nv') != INIT_HASHES['repeat-g1']:
        raise ValueError('German repeat initialization NVRAM digest mismatch')
    # Comparison uses complete ordered observations, including both display rows.
    for game in GAMES:
        entries, observations = records[game]
        for name in NAMES[1:]:
            reference, observed = all_pairs['radcl_l1'][name], all_pairs[game][name]
            if len(reference) != len(observed):
                raise ValueError(f'{game}/{name}: incomplete comparison')
            differences = [(a, b) for a, b in zip(reference, observed) if a != b]
            observations[name]['note'] += f' Compared with radcl_l1: {len(differences)} differing ordered readings.'
        if game == 'radcl_g1':
            observations['switch-levels']['limitation'] += ' The original German sweep failed its display checkpoint; its preserved raw trace is original/runs/radcl_g1-switch-levels.json, SHA-256 e6a8cc722485d25b3038887063eed41058ab476587b823aa99e5497911e1a922.'
        records[game] = evidence_record(game, manifest, entries, {
            'service_language': 'German menus' if game == 'radcl_g1' else 'English menus',
            'runs': observations,
        })
    if not draft and set(saved) != set(drafted):
        raise ValueError('frame-reading seed contains missing or extraneous runs')
    return manifest, records, drafted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--draft-frame-readings', action='store_true')
    args = parser.parse_args()
    root = os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT')
    if not root:
        raise SystemExit('PINMAME_REVIEW_ARTIFACTS_ROOT is required')
    review_root = Path(root).resolve()
    manifest, records, pins = build(review_root, args.draft_frame_readings)
    if args.draft_frame_readings:
        print(json.dumps({'runs': pins}, indent=2, ensure_ascii=False, sort_keys=True))
        return
    bundle = review_root / BUNDLE_RELATIVE
    if args.check:
        manifests.check_manifest(bundle, 'radcl_l1')
        if (bundle / 'manifest.json').read_bytes() != manifest:
            raise SystemExit('external manifest mismatch')
    else:
        manifests.write_manifest(bundle, 'radcl_l1')
    for game, record in records.items():
        path = ROOT / f'evidence/runtime/system-11/radical-{game.split("_", 1)[1]}-service-tests.json'
        data = canonical_bytes(record)
        if args.check:
            if path.read_bytes() != data:
                raise SystemExit(f'{path}: generated evidence drift')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print('Radical runtime evidence matches retained traces.' if args.check else 'Wrote Radical runtime evidence.')


if __name__ == '__main__':
    main()
