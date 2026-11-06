"""Derive Phantom of the Opera service-test evidence from two independent direct runs.

Raw alphanumeric segments, not host switch readback, establish each label.  The
second run and every intervening reference closure are checked independently.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import zipfile

from pinmame_game_defs.jsonio import canonical_bytes
from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = Path('tools/harness-scenarios/data-east/poto-a32-service-walk.json')
SEED = Path('tools/seeds/data-east/phantom-of-the-opera-1990-service-readings.json')
OUTPUT = Path('evidence/runtime/data-east/phantom-of-the-opera-service-walk.json')
RUN_ROOT = 'phantom-of-the-opera-1990/runtime'
REVISION = '46e1a01a0f73dc5ce163d98db1ae435883ecc450'
LIBRARY = '8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5'
SCENARIO_SHA = '7ae7fdf1a9c26b347300bd4be5afa5ac67ce1073120f10cf7ac8414968e7d3f1'
INDEX_SHA = 'fe3a6a4b487027ec5d3746a99804ee7722f94d4c8e023acbfd6b22f1779cb4b5'
ROM_SHA = '7e90f6a0547d1a83b6aff8492ba0f0e8767a0f87345b9c2b47095a78764bf4e7'
RUNS = {
    'direct1': ('dfbe5385425458c376a77ea57d9cbe10a551f7a2b47fe2dd24c0205ffec50ba8', '926dd2532a769d43cbf58a0f19dfae56ed2555e6a8af6392f49048fccfcfbb71'),
    'direct2': ('f77026dc75cd9c96a1ed5012f04205156daed3a4ece31dd89e8509380adff80f', 'c5d4fdf555141e4c166bb55794548eff97b0832233a48391380cb66786a2915f'),
}
ROM_MEMBERS = {
    'potob5.3-2': (16384, '67b3f56655ef2cc056912ab6e351cf83352abaa9'),
    'potoc5.3-2': (32768, 'c1441fda6181e9014a8a6f93b7405998a952f508'),
    'potof5.rom': (65536, '26724441d7e2edd7725337b262d95448499151ad'),
    'potof6.rom': (65536, 'f82c706b88f49341bab9014bd83371259eb53b47'),
    'potof7.rom': (32768, '0be89fc9b2c6548392febb35c1ace0eb912fc73f'),
}
EXPECTED_CYCLE = [v for i in range(1, 9) for v in (i, i + 24)] + list(range(9, 17))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decoded(frame: dict) -> str:
    if len(frame['text']) != len(frame['segments']):
        raise ValueError('display text/segment length mismatch')
    return ''.join(({6: '1', 0x0867: '9'}.get(seg, char) if char == '?' else char)
                   for char, seg in zip(frame['text'], frame['segments']))


def normalize_number(s: str) -> str:
    return s.replace('O', '0').replace('S', '5')


def frame_at(events: list[dict], index: int, time: float) -> dict:
    frames = [e for e in events if e['event'] == 'display' and e['index'] == index and e['time_s'] <= time]
    if not frames:
        raise ValueError(f'missing display {index} at {time}')
    return frames[-1]


def pair(frame0: dict, frame1: dict) -> dict:
    return {'name': decoded(frame0), 'name_segments': frame0['segments'],
            'code': decoded(frame1), 'code_segments': frame1['segments']}


def wire_check(frame: dict, number: int, switch: bool) -> None:
    text = decoded(frame)
    code, address = text[3:8], normalize_number(text[14:16])
    if address != f'{number:02d}':
        raise ValueError(f'wrong displayed address for {number}: {text!r}')
    # The ROM's printed wire codes are evidence in their own right, not a
    # calculated wiring pattern: preserve even unexpected digits literally.
    normalized = code[0] + normalize_number(code[1:]) if switch else normalize_number(code)
    if switch:
        valid = normalized[0] == 'S' and normalized[1].isdigit() and normalized[2] == '-' and normalized[3:].isdigit()
    else:
        valid = normalized[0:2].isdigit() and normalized[2] == '-' and normalized[3:].isdigit()
    if not valid:
        raise ValueError(f'invalid displayed wire code for {number}: {code!r}')

def snapshots(run: dict) -> dict:
    result = {}
    for item in run['snapshots']:
        result[item['label']] = item
    return result


def read_snapshot(snap: dict, number: int, switch: bool) -> dict:
    frames = {d['index']: d for d in snap['displays']}
    wire_check(frames[1], number, switch)
    if not switch and snap['active_lamps'] != [number]:
        raise ValueError(f'lamp {number}: output is not solely active in snapshot')
    return pair(frames[0], frames[1])


def walk(run: dict) -> dict:
    shots = snapshots(run)
    steps = {s['label']: s for s in run['steps']}
    names, lamps = {}, {}
    refs = []
    for number in range(1, 65):
        if number == 15:
            label = 'hold the left flipper key in Switch Test'
            ref = 'reference switch 1 before left_flipper probe'
            stimulus = 84
        elif number == 16:
            label = 'hold the right flipper key in Switch Test'
            ref = 'reference switch 1 before right_flipper probe'
            stimulus = 82
        else:
            label = f'close matrix switch {number} in Switch Test'
            ref = f'reference switch {3 if number == 1 else 1} before probe {number}'
            stimulus = number
        for step_label, expected_switch in ((label, stimulus), (ref, 3 if number == 1 else 1)):
            step = steps[step_label]
            if step['type'] != 'pulse' or step['switch'] != expected_switch or step['hold_ms'] != 3000:
                raise ValueError(f'wrong probe schedule: {step_label}')
        reference = read_snapshot(shots[ref + ' (held)'], 3 if number == 1 else 1, True)
        refs.append(reference)
        names[str(number)] = read_snapshot(shots[label + ' (held)'], number, True)
    if refs[0] != names['3'] or any(item != names['1'] for item in refs[1:]):
        raise ValueError('reference display drift or lag')
    if decoded({'text': names['1']['name'], 'segments': names['1']['name_segments']}).strip() != 'PLUMB   TILT':
        raise ValueError('reference switch 1 is not PLUMB TILT')
    for number in range(1, 65):
        label = 'discrete Lamp Test on its first lamp' if number == 1 else f'Start step {number - 1} in the discrete Lamp Test'
        lamps[str(number)] = read_snapshot(shots[label], number, False)
        if number > 1:
            transitions = steps[label]['transitions']['lamps']
            if not any(x['number'] == number and 1 in x['states'] for x in transitions):
                raise ValueError(f'lamp {number} missing on transition')
    events = run['events']
    title = next(e['time_s'] for e in events if e['event'] == 'display' and e['index'] == 0 and ' '.join(decoded(e).split()) == 'COIL TEST')
    coils, sequence = {}, []
    for e in events:
        if e['event'] != 'solenoid' or e['state'] != 1 or e['time_s'] <= title:
            continue
        number = e['number']
        if number not in EXPECTED_CYCLE:
            raise ValueError(f'unexpected coil output {number}')
        f0, f1 = frame_at(events, 0, e['time_s']), frame_at(events, 1, e['time_s'])
        bank = normalize_number(decoded(f1)[11:14])
        expected = f'L{number:02d}' if number <= 8 else f'R{number-24:02d}' if number >= 25 else f' {number:02d}'
        # Output 10 also switches the multiplex relay after each left-bank drive.
        if number == 10 and bank != expected:
            continue
        if bank != expected:
            raise ValueError(f'coil {number}: bank {bank!r} != {expected!r}')
        value = pair(f0, f1)
        if number in coils and value != coils[number]:
            raise ValueError(f'coil {number} changed display reading on repeat')
        coils[number] = value
        sequence.append(number)
    if sequence[:24] != EXPECTED_CYCLE:
        raise ValueError(f'wrong selected coil order: {sequence[:24]}')
    return {'switch_test': names, 'lamp_test': lamps,
            'coil_test': {str(n): coils[n] for n in sorted(coils)}, 'coil_sequence': sequence}


def response(value: dict, number: int, labels: list[str]) -> list[dict]:
    result = []
    for index, key in enumerate(('name', 'code')):
        segments = value[key + '_segments']
        result.append({'snapshot_label': labels[index], 'display_index': index, 'segments': segments,
                       'decoded_segment_positions': [i for i, v in enumerate(segments) if v],
                       'interpreted_text': value[key], 'diagnostic_address': number})
    return result


def frame_labels(run: dict, kind: str, number: int) -> list[str]:
    if kind == 'switch_test':
        label = ('hold the left flipper key in Switch Test' if number == 15 else
                 'hold the right flipper key in Switch Test' if number == 16 else
                 f'close matrix switch {number} in Switch Test') + ' (held)'
        return [label, label]
    if kind == 'lamp_test':
        label = ('discrete Lamp Test on its first lamp' if number == 1 else
                 f'Start step {number - 1} in the discrete Lamp Test')
        return [label, label]
    title = next(e['time_s'] for e in run['events'] if e['event'] == 'display' and e['index'] == 0 and ' '.join(decoded(e).split()) == 'COIL TEST')
    expected = f'L{number:02d}' if number <= 8 else f'R{number-24:02d}' if number >= 25 else f' {number:02d}'
    for e in run['events']:
        if e['event'] != 'solenoid' or e['state'] != 1 or e['number'] != number or e['time_s'] <= title:
            continue
        bank = frame_at(run['events'], 1, e['time_s'])
        if normalize_number(decoded(bank)[11:14]) == expected:
            return [f'display {index} event at {frame_at(run["events"], index, e["time_s"])["time_s"]:.6f}s; output {number} on at {e["time_s"]:.6f}s' for index in (0, 1)]
    raise ValueError(f'missing selected coil {number}')

def load_run(root: Path, name: str, scenario: dict) -> dict:
    directory = root / RUN_ROOT / name
    run_sha, manifest_sha = RUNS[name]
    if check_manifest(directory, 'poto_a32') != manifest_sha or digest(directory / 'run.json') != run_sha:
        raise ValueError(f'raw evidence drift: {directory}')
    run = json.loads((directory / 'run.json').read_bytes())
    if (run['failure'] is not None or run['game'] != 'poto_a32' or run['library_sha256'] != LIBRARY
        or run['scenario']['sha256'] != SCENARIO_SHA or run['scenario']['action_count'] != len(scenario['actions'])
        or run['handle_mechanics'] != 0 or run['initial_switches'] or run['pulses']
        or run['switch_converter'] != 'sequential' or any(e['event'] == 'key' for e in run['events'])):
        raise ValueError(f'invalid run identity or inputs: {name}')
    checks = [(s['matched_text'], s['pulses']) for s in run['steps'] if s['type'] == 'pulse_until_display']
    if checks != [('SWITCH TEST', 10), ('LAMP TEST', 6), ('COIL TEST', 1)]:
        raise ValueError(f'wrong diagnostic checkpoints: {checks}')
    return run


def build(review_root: Path, rom_root: Path | None = None) -> dict:
    if digest(ROOT / SCENARIO) != SCENARIO_SHA:
        raise ValueError('scenario bytes changed')
    scenario = json.loads((ROOT / SCENARIO).read_bytes())
    seed = json.loads((ROOT / SEED).read_bytes())
    index_path = review_root / RUN_ROOT / 'rom-index.json'
    if digest(index_path) != INDEX_SHA:
        raise ValueError('ROM index drift')
    index = json.loads(index_path.read_bytes())
    members = {m['name']: (m['size'], m['sha1']) for m in index['members']}
    if index['archive_sha256'] != ROM_SHA or members != ROM_MEMBERS:
        raise ValueError('wrong ROM index')
    runs = {name: load_run(review_root, name, scenario) for name in RUNS}
    configured_root = rom_root or (Path(os.environ['PINMAME_ROM_LIBRARY_ROOT']) if os.environ.get('PINMAME_ROM_LIBRARY_ROOT') else None)
    for name, run in runs.items():
        archive = (configured_root or Path(run['rom_path'])) / 'poto_a32.zip'
        if digest(archive) != ROM_SHA:
            raise ValueError(f'{name}: ROM archive drift')
        with zipfile.ZipFile(archive) as package:
            infos = package.infolist()
            if len(infos) != len(members) or {item.filename for item in infos} != set(members):
                raise ValueError(f'{name}: ROM archive members differ from the index')
            for item in index['members']:
                data = package.read(item['name'])
                if (len(data) != item['size'] or hashlib.sha1(data).hexdigest() != item['sha1']
                    or hashlib.sha256(data).hexdigest() != item['sha256']):
                    raise ValueError(f'{name}: ROM member drift: {item["name"]}')
    readings = {name: walk(run) for name, run in runs.items()}
    for name, item in readings.items():
        for key in ('switch_test', 'lamp_test', 'coil_test'):
            if item[key] != seed[key]:
                raise ValueError(f'{name}: {key} differs from pinned segment readings')
        if item['coil_sequence'][:24] != EXPECTED_CYCLE:
            raise ValueError('wrong coil cycle')
    raw_runs, observed = [], {}
    for name, run in runs.items():
        raw_runs.append({'name': name, 'sha256': RUNS[name][0], 'scenario_path': SCENARIO.as_posix(),
            'scenario_sha256': SCENARIO_SHA, 'action_count': len(scenario['actions']),
            'watch_switches': run['watch_switches'], 'self_test_pulses': 17,
            'nvram_initialization': 'new empty isolated state directory; no NVRAM inherited',
            'boot_wait_s': 5.0, 'snapshot_count': len(run['snapshots']), 'retained_from': f'{RUN_ROOT}/{name}/run.json'})
        observed[name] = {'diagnostic_checkpoints': [{'matched_text': s['matched_text'], 'after_service_pulses': s['pulses']}
            for s in run['steps'] if s['type'] == 'pulse_until_display'],
            'ordered_solenoid_on_sequence': [e['number'] for e in run['events'] if e['event'] == 'solenoid' and e['state'] == 1 and e['time_s'] > next(x['time_s'] for x in run['events'] if x['event'] == 'display' and x['index'] == 0 and ' '.join(decoded(x).split()) == 'COIL TEST')],
            'solenoid_addresses_seen': sorted(EXPECTED_CYCLE)}
    actions = []
    for key, label, stimulus in [('switch_test', 'Switch Test: each held host input is paired with the ROM name and address/wire frame', list(range(1,15))+list(range(17,65))+[82,84]),
        ('lamp_test', 'Lamp Test: each selected lamp transition is paired with its ROM name and address/wire frame', [3]),
        ('coil_test', 'Coil Test: selected output transitions are paired with the ROM name and bank frame', [-7])]:
        frames = [frame for n, value in seed[key].items() for frame in response(value, int(n), frame_labels(runs['direct1'], key, int(n)))]
        actions.append({'label': label, 'input_kind': 'switch', 'input_address': stimulus[0],
            'host_stimulus_switch_addresses': stimulus, 'observed_switch_addresses': [],
            'display_responses': frames, 'result': 'observed'})
    observed['direct1']['named_action_observations'] = actions
    observed['direct1']['limitation'] = ('Switch values written or read back by the host are stimulus, not ROM observations. Each probe follows a different 3-second reference; every reference frame and address/wire code is checked in both fresh runs. The two cabinet flipper inputs 84 and 82 are copied to matrix addresses 15 and 16. Output transitions establish emulator behavior, not physical fitment, polarity, quantity, or location. The raw solenoid sequence includes relay 10 transitions while an L-bank coil is selected; the selected driver cycle is 1,25,2,26,3,27,4,28,5,29,6,30,7,31,8,32,9,10,11,12,13,14,15,16; 17-22 are not tested, and absence is not proof of an unused output. Names retain the decoder glyphs; 0/O and 5/S share segments, while unknown glyphs remain ?. Segments 0x0006 and 0x0867 decode as 1 and 9.')
    observed['direct2']['note'] = 'Every name, wire/bank frame and segment sequence matches direct1; the frames are retained once.'
    return {'format': 'pinmame-machine-evidence', 'version': 1,
        'extractor': {'id': 'tools/build_phantom_runtime_evidence.py', 'version': 1},
        'source': {'kind': 'runtime_scenario', 'repository': 'https://github.com/vpinball/pinmame',
            'revision': REVISION, 'path': f'external:pinmame-review-artifacts/{RUN_ROOT}', 'sha256': RUNS['direct1'][1],
            'manifest_algorithm': 'source.sha256 is SHA-256 of direct1/manifest.json bytes; direct2/manifest.json SHA-256 is '+RUNS['direct2'][1]+'. Each is sorted compact JSON plus LF listing every file under the run, excluding only manifest.json and manifest.sha256, with path, SHA-256 and size.',
            'license': 'NOASSERTION', 'quality': 'observed', 'attribution': 'Generated from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external.'},
        'driver_ids': ['poto_a32'], 'machine_ids': ['data-east.phantom-of-the-opera.1990'],
        'switches': [], 'outputs': [], 'states': [], 'mechanisms': [], 'recreation_notes': [],
        'runtime': {'game': 'poto_a32', 'rom_archive_sha256': ROM_SHA,
            'emulator': {'binary': 'pinmame64.dll', 'sha256': LIBRARY, 'built_from_revision': REVISION},
            'raw_runs': raw_runs, 'command_template': 'ROM index at external:pinmame-review-artifacts/phantom-of-the-opera-1990/runtime/rom-index.json has SHA-256 '+INDEX_SHA+'. python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game poto_a32 --rom-path <legal-ROM-root> --work-dir <fresh-state> --scenario '+SCENARIO.as_posix()+' --boot-wait 5 --output <external-run>',
            'observations': {'service_language': 'English', 'display_indices_seen': [0, 1, 2], 'runs': observed}}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('review_root', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--rom-root', type=Path, help='ROM library override; defaults to PINMAME_ROM_LIBRARY_ROOT or the retained run path')
    args = parser.parse_args()
    data = canonical_bytes(build(args.review_root, args.rom_root))
    if args.check:
        if (ROOT / OUTPUT).read_bytes() != data:
            raise SystemExit('Phantom runtime evidence drift')
        print('Phantom runtime evidence matches both retained runs.')
    else:
        (ROOT / OUTPUT).write_bytes(data)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
