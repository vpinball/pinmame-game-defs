"""Re-derive Grand Lizard L-4 service and gameplay evidence from retained traces."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, write_json
from run_pinmame_harness import SEGMENT_16_CHARACTERS
from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence/runtime/williams/grand-lizard-l4-service-and-gameplay.json'
HARNESS = 'grand-lizard-1986/harness'
REVISION = '46e1a01a0f73dc5ce163d98db1ae435883ecc450'
LIBRARY = '8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5'
ROM = 'fa577253dd1516318962b3380a93568d2862fbd7c27b4bc7a077c28c8029059b'
NVRAM = '7451e6d5e6b340a55406314bcd7371a65b382755c56e30b6d5ce576c44270b3d'
MANIFEST = 'ea573bd88e2dd63745c1429e49d2f07ab95bc566db81dc6400d9e66f4c360db4'
REPO_SCENARIO_HASHES = {'init': '5a002233e362b14b16fd41a6cc3163e4e3bb7554049fa879a0a6d5b48791f7f0', 'coil': 'fbe812aa5a8e7f69dfb8b2ce6a38f0a26bb4ca4345f5ed7e8e33fdb49c14fb64', 'gameplay': '225d69aa1bca29455a5bdee94deb9fc20719bcf09973f43b83a32d2561d41d62', 'depletion': '50f5b0552cad1bcfd1710bfc2bd52627193cf8c834ea0c5c2b9b6c3ce8c9730e', 'switch-levels': '57ff7b28836af5a8956c36b4585e58f3e97d0729372a1e05a920ab5ed49037f2'}
RUNS = {
    'init': ('init-run.json', 'grand-l4-nvram-init.json', '98a5681712495d2b0e6c2b3d2de45502026ba40b01b57a72725796315a54e0d7', '5a002233e362b14b16fd41a6cc3163e4e3bb7554049fa879a0a6d5b48791f7f0'),
    'coil': ('coil-run.json', 'grand-l4-coil-test.json', '9051a8150e294c772de4f11e26f99be7a5cdb07bd49f2d71b132824ee2f36a56', '59f0e18c869b6be93a8a4b57d1fc31d85781da5edefe1ad19f80008ff104bd52'),
    'gameplay': ('gameplay-run.json', 'grand-l4-gameplay-probe.json', 'f9f31a96b15d10c64755068936c09a2c9966a0f4a123da9b93f69f538c01963c', '0249d8f6d31e3acf25a4992d72f530837e265d2f2e84ec7e7869e94b83ac2e70'),
    'depletion': ('magna-depletion-run.json', 'grand-l4-magna-depletion.json', '98668a3e43c497fc3ad296a4c0f5907c8b00f49d42e8361839b98653f91e29cd', '033304d4933b7f911eee644935d3fd3a974448b7882c23667b18fc48da12bea9'),
    'switch-levels': ('switch-levels-run.json', 'grand-l4-switch-levels.json', 'e0b0dc3bc1c436e8cebe7b88d7aba424adcd2d5984b0763af1ca920c2f97a362', '73c29ed2760e818aff9751d786f62f6cb2cfa86a0e9a9a65f8236f0e5815e0c4'),
}
LABELS = ('TROUGH KICKER', '3 BANK RAISE', '4 BANK RAISE 1', '4 BANK RAISE 2', 'LOCKUP EJECT', 'LOCKUP FLASHER', 'LEFT FLASHER', 'BALL FEED', 'LEFT MAGNET', 'RIGHT MAGNET', 'GENERAL ILLUMIN.', '3 BANK FLASHER', 'LIZARD FLASHER', 'CREDIT KNOCKER', 'BELL', 'COIN LOCKOUT', 'LEFT KICKER', 'RIGHT KICKER', 'RIGHT FLASHER', 'NOT USED', 'NOT USED', 'NOT USED')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def one(items, label):
    matches = [x for x in items if x['label'] == label]
    if len(matches) != 1:
        raise ValueError(f'expected one {label!r}')
    return matches[0]


def glyph(value):
    if value == 6:
        return '1'
    if value in SEGMENT_16_CHARACTERS:
        return SEGMENT_16_CHARACTERS[value]
    # CORE_SEG16: PIA3A's high bit is dot, PIA3B's high bit is comma
    # (pinned s11.c:462-486,736-738; core.c:192-200,273-294).
    if value & 0x8080:
        base = value & ~0x8080
        char = '1' if base == 6 else SEGMENT_16_CHARACTERS.get(base)
        if char is not None:
            return char + (',' if value & 0x0080 else '') + ('.' if value & 0x8000 else '')
    return '?'


def coil_observations(run):
    start = one(run['snapshots'], 'locate COIL TEST')['time_s']
    finish = one(run['snapshots'], 'observe all controlled and special solenoid test steps')['time_s']
    events = run['events']
    pulses = [e for e in events if e['event'] == 'solenoid' and e['state'] == 1 and start < e['time_s'] < finish]
    # The selector repeats each output four times (the final three received only three pulses).
    expected = list(range(1, 23)) * 3 + list(range(1, 20))
    if [e['number'] for e in pulses] != expected:
        raise ValueError('coil sequence differs')
    rows = []
    for number, expected_label in enumerate(LABELS, 1):
        frames = []
        for pulse in (p for p in pulses if p['number'] == number):
            lines = []
            for index in (0, 1):
                current = [e for e in events if e['event'] == 'display' and e['index'] == index and e['time_s'] <= pulse['time_s'] + .15]
                if not current:
                    raise ValueError('missing display frame')
                lines.append(current[-1]['segments'])
            text = ' '.join(''.join(map(glyph, line)).strip() for line in lines).strip()
            if text != expected_label:
                raise ValueError(f'coil {number} reads {text!r}, expected {expected_label!r}')
            frames.append(lines)
        if any(f != frames[0] for f in frames):
            raise ValueError(f'coil {number} display changed across pulses')
        rows.append({'address': number, 'label': expected_label, 'display_segments': frames[0], 'pulse_count': len(frames)})
    return rows


def transition(step, channel):
    return {item['number']: item['states'] for item in step['transitions'][channel]}


def require_step(run, label, switch, kind, expected):
    step = one(run['steps'], label)
    if step['switch'] != switch or step['type'] != kind:
        raise ValueError(f'bad stimulus {label}')
    got = transition(step, 'solenoids')
    if got != expected:
        raise ValueError(f'unexpected solenoids for {label}: {got}')
    return step


def gameplay_observations(run):
    for label, switch, states in (
        ('left sling isolation', 43, {17: [1, 0]}), ('right sling isolation', 44, {18: [1, 0]}),
        ('left cabinet button held', 84, {47: [1], 48: [1]}), ('left cabinet button released', 84, {47: [0], 48: [0]}),
        ('right cabinet button held', 82, {45: [1], 46: [1]}), ('right cabinet button released', 82, {45: [0], 46: [0]}),
    ):
        require_step(run, label, switch, 'set_switch' if 'cabinet' in label else 'pulse', states)
    for label, states in [('left cabinet button held', {47: 0, 48: 0}), ('left cabinet button released', {47: 0, 48: 0}), ('right cabinet button held', {47: 0, 48: 1}), ('right cabinet button released', {47: 0, 48: 0})]:
        got = {x['number']: x['state'] for x in one(run['snapshots'], label)['watched_switches'] if x['number'] in states}
        if got != states:
            raise ValueError(f'matrix readback differs: {label}')
    for label, switch, needed in [('left magna-save button after LIZ', 45, {7, 9}), ('right magna-save button after ARD', 46, {10, 19})]:
        step = one(run['steps'], label)
        got = transition(step, 'solenoids')
        if step['switch'] != switch or not all(1 in got.get(n, []) for n in needed):
            raise ValueError(f'missing gameplay output: {label}')
    return ('Switch 43 pulsed solenoid 17; 44 pulsed 18. Once-written 84 held/released synthetic 47 and 48 high/low; once-written 82 held/released synthetic 45 and 46 high/low. Matrix 48 readback followed 82, while 47 and 48 remained low during 84. Readback is informational emulator state, not ROM evidence. Switch 45 fired 9 and 7; switch 46 fired 10 and 19. Initial charge was already full: the LIZ probe does not establish a charge gain.')


def depletion_observations(run):
    result = []
    exhausted = set()
    for side, switch, pair, order in [('left', 45, (7, 9), (44, 43, 42)), ('right', 46, (10, 19), (47, 46, 45))]:
        for i in range(1, 6):
            label = f'{side} Magna-save depletion {i}'
            step = one(run['steps'], label)
            if step['type'] != 'pulse' or step['switch'] != switch or step['hold_ms'] != 800:
                raise ValueError(f'bad depletion stimulus: {label}')
            coils = transition(step, 'solenoids')
            lamps = transition(step, 'lamps')
            if i <= 3:
                active = order[i-1]
                if not all(1 in coils.get(n, []) for n in pair) or 1 not in lamps.get(active, []) or 0 not in lamps.get(active, []):
                    raise ValueError(f'missing depletion response: {label}')
                exhausted.add(active)
            elif coils:
                raise ValueError(f'unexpected solenoids after exhaustion: {label}')
            if exhausted & set(one(run['snapshots'], label)['active_lamps']):
                raise ValueError(f'exhausted lamps remain lit: {label}')
            if (exhausted - ({order[i-1]} if i <= 3 else set())) & set(lamps):
                raise ValueError(f'exhausted lamps changed again: {label}')
            result.append({'side': side, 'press': i, 'switch': switch, 'blinking_then_off': order[i-1] if i <= 3 else None, 'solenoids': sorted(n for n, states in coils.items() if 1 in states)})
    return result


def switch_observations(run):
    addresses = list(range(1, 48)) + list(range(49, 65)) + [84, 82]
    rows = []
    for number in addresses:
        label = f'public {number} active hold'
        step = one(run['steps'], label)
        if step['type'] != 'set_switch' or step['switch'] != number or step['state'] != 1 or step['settle_s'] != 1:
            raise ValueError(f'bad switch probe {number}')
        snap = one(run['snapshots'], label)
        displays = {x['index']: x for x in snap['displays']}
        segments = [displays[index]['segments'] for index in (0, 1)]
        text = [''.join(map(glyph, line)).strip() for line in segments]
        rows.append({'address': number, 'text': text, 'segments': segments})
    expected = {35: ['LIZARD', 'L'], 36: ['LIZARD', 'I'], 37: ['LIZARD', 'Z'], 38: ['LIZARD', 'A'], 39: ['LIZARD', 'R'], 40: ['LIZARD', 'D'], 43: ['KICKER', 'LEFT'], 44: ['KICKER', 'RIGHT'], 45: ['MAGNET', 'LEFT'], 46: ['MAGNET', 'RIGHT'], 47: ['INVALID', 'INVALID']}
    for row in rows:
        if row['address'] in expected and row['text'] != expected[row['address']]:
            raise ValueError(f"switch display changed at {row['address']}")
    return rows


def build(review_root: Path):
    folder = review_root / HARNESS
    if check_manifest(folder, 'grand_l4') != MANIFEST:
        raise ValueError('external harness manifest differs from pin')
    runs = {}
    raw = []
    for name, (filename, scenario, digest, scenario_hash) in RUNS.items():
        path = folder / filename
        external_scenario = (folder.parent if name == 'init' else folder) / scenario
        repo_scenario = ROOT / 'tools/harness-scenarios/system-11' / scenario
        if sha(path) != digest or sha(external_scenario) != scenario_hash or sha(repo_scenario) != REPO_SCENARIO_HASHES[name] or json.loads(external_scenario.read_bytes()) != json.loads(repo_scenario.read_bytes()):
            raise ValueError(f'raw run or scenario drift: {name}')
        run = json.loads(path.read_bytes())
        if run['failure'] is not None or run['game'] != 'grand_l4' or run['library_sha256'] != LIBRARY or run['handle_mechanics'] != 0 or run['scenario']['sha256'] != scenario_hash:
            raise ValueError(f'invalid run parameters: {name}')
        runs[name] = run
        raw.append({'name': name, 'sha256': digest, 'self_test_pulses': sum((s.get('pulses', 0) if s['type'] == 'pulse_until_display' else 1) for s in run['steps'] if s.get('switch') == -7 and s['type'] in ('pulse', 'pulse_until_display')), 'scenario_path': f"external:pinmame-review-artifacts/grand-lizard-1986/{'' if name == 'init' else 'harness/'}{scenario}", 'scenario_sha256': scenario_hash, 'action_count': run['scenario']['action_count'], 'snapshot_count': len(run['snapshots']), 'watch_switches': run['watch_switches'], 'initial_switches': run['initial_switches'], 'retained_from': f'external:pinmame-review-artifacts/{HARNESS}/{filename}', 'nvram_initialization': 'Empty state, 30 second boot.' if name == 'init' else f'Fresh state seeded only with init-state/nvram/grand_l4.nv SHA-256 {NVRAM}, from the retained 30 second empty-state boot.'})
    if sha(folder / 'init-state/nvram/grand_l4.nv') != NVRAM:
        raise ValueError('initial NVRAM drift')
    coil = coil_observations(runs['coil'])
    gameplay = gameplay_observations(runs['gameplay'])
    depletion = depletion_observations(runs['depletion'])
    switch_levels = switch_observations(runs['switch-levels'])
    # The schema's run notes carry the exact decoded frames and transitions without adding ad hoc fields.
    notes = {
        'coil': {'note': 'Automatic COIL TEST; frames sampled 0.15 s after each pulse, identical on each repeat. Raw segments and pulse counts: ' + json.dumps(coil, separators=(',', ':')), 'limitation': 'ROM labels and output activity do not establish fitted physical loads. PinMAME s11.c lines 462-486 and 736-738 and core.c lines 192-200 and 273-294 identify 0x8000 as the dot and 0x0080 as the comma for this CORE_SEG16 layout. GENERAL ILLUMIN. ends with N plus dot, raw mask 0x9136.'},
        'gameplay': {'note': gameplay, 'limitation': 'No activity in a matrix 47 pulse does not prove that address unused. Physical sides require independent manual evidence.'},
        'depletion': {'note': 'Charge lamp order and active solenoids per isolated press: ' + json.dumps(depletion, separators=(',', ':')), 'limitation': 'Blinking is observed during each charge consumption. The test pairs output groups with inputs; it does not establish physical lamp positions.'},
        'switch-levels': {'note': 'SWITCH LEVELS once-written holds; raw segment frames at the end of each hold: ' + json.dumps(switch_levels, separators=(',', ':')), 'limitation': 'Some frames are blank or transient (especially 82), and question marks retain undecoded glyphs; do not infer names from them. The ROM showing INVALID or failing to respond does not prove physical fitment.'},
    }
    return {'format': 'pinmame-machine-evidence', 'version': 1, 'machine_ids': ['williams.grand-lizard.1986'], 'driver_ids': ['grand_l4'], 'extractor': {'id': 'tools/grand_lizard_runtime_evidence.py', 'version': 1}, 'switches': [], 'outputs': [], 'states': [], 'mechanisms': [], 'recreation_notes': [], 'source': {'kind': 'runtime_scenario', 'quality': 'observed', 'path': f'external:pinmame-review-artifacts/{HARNESS}', 'sha256': MANIFEST, 'manifest_algorithm': "SHA-256 of canonical manifest.json bytes with one LF; tools/build_external_evidence_manifest.py lists every file recursively except root manifest.json and manifest.sha256, sorted by case-sensitive POSIX path.", 'revision': REVISION, 'repository': 'https://github.com/vpinball/pinmame', 'license': 'NOASSERTION', 'attribution': 'Generated locally from pinned PinMAME and user-authorized ROM; ROM bytes and NVRAM remain external. Source hash is the external harness manifest. Scenario hashes in raw_runs refer to retained original bytes; repository scenarios under tools/harness-scenarios/system-11/ are LF-normalized, semantically identical JSON; SHA-256 keyed by run name: ' + json.dumps(REPO_SCENARIO_HASHES, sort_keys=True) + '.'}, 'runtime': {'game': 'grand_l4', 'emulator': {'binary': 'pinmame64.dll', 'built_from_revision': REVISION, 'sha256': LIBRARY}, 'rom_archive_sha256': ROM, 'command_template': 'python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game grand_l4 --rom-path <read-only-roms> --work-dir <fresh-state> --handle-mechanics 0 --scenario <committed-scenario> --output <external-run.json>. Initialize empty NVRAM first, then copy only its NVRAM into a separate fresh state for each later run. ROM ZIP member size/SHA-1: lzrd_u21.l1 16384/08429b9e6a3b3007815373dc280b985e3441aa9f; lzrd_u22.l1 16384/b44ab499128300175bdb57f07ffe2992c82e47e4; lzrd_u26.l4 8192/7e2adfefce5c33ad605606574dbdfb2642aa0e85; lzrd_u27.l4 32768/0ebfa998d3cefc213ada9ed815d44977120e5d6d; lzrd_u4.l1 32768/3507f5f37e02688fa56cf5bb303eaccdcedede06. Pinned s11games.c lines 205-211 specifies the same U26 hash under filename lzrd_u26.l3; the ZIP uses lzrd_u26.l4.', 'raw_runs': raw, 'observations': {'service_language': 'English', 'runs': notes}}}


def validate_compact(document):
    """Check core assertions even when the external evidence root is unavailable."""
    if document['source']['sha256'] != MANIFEST or document['runtime']['game'] != 'grand_l4':
        raise ValueError('wrong compact source or driver')
    observations = document['runtime']['observations']['runs']
    coil_rows = json.loads(observations['coil']['note'].split(': ', 1)[1])
    depletion_rows = json.loads(observations['depletion']['note'].split(': ', 1)[1])
    switches = json.loads(observations['switch-levels']['note'].split(': ', 1)[1])
    if [(r['address'], r['label']) for r in coil_rows] != list(enumerate(LABELS, 1)):
        raise ValueError('compact coil names differ')
    if [r['blinking_then_off'] for r in depletion_rows] != [44, 43, 42, None, None, 47, 46, 45, None, None]:
        raise ValueError('compact depletion order differs')
    if [r['address'] for r in switches] != list(range(1, 48)) + list(range(49, 65)) + [84, 82]:
        raise ValueError('compact switch sweep differs')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review-root', type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = args.review_root or (Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT']) if os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT') else None)
    if root is None:
        if args.write:
            raise SystemExit('review root required for generation')
        if not OUT.is_file():
            raise SystemExit('missing compact runtime evidence')
        validate_compact(json.loads(OUT.read_bytes()))
        print('External evidence root not configured; retained trace check skipped.')
        return
    document = build(root)
    validate_compact(document)
    if args.write:
        write_json(OUT, document)
    elif not OUT.is_file() or OUT.read_bytes() != canonical_bytes(document):
        raise SystemExit('Grand Lizard runtime evidence drift')
    else:
        print('Grand Lizard runtime evidence matches retained traces.')


if __name__ == '__main__':
    main()
