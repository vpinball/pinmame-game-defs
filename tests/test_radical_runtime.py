from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
import radical_runtime_evidence as builder


class RadicalRuntimeTests(unittest.TestCase):
    def test_schemas_and_distinct_drivers(self):
        evidence_validator = Draft202012Validator(json.loads((ROOT / 'schemas/evidence.schema.json').read_bytes()))
        scenario_validator = Draft202012Validator(json.loads((ROOT / 'schemas/harness-scenario.schema.json').read_bytes()))
        for name in ('nvram-init', 'coil-test', 'single-lamps', 'switch-levels', 'g1-switch-levels'):
            scenario_validator.validate(json.loads((ROOT / f'tools/harness-scenarios/system-11/radcl-{name}.json').read_bytes()))
        for game in builder.GAMES:
            path = ROOT / f'evidence/runtime/system-11/radical-{game.split("_")[1]}-service-tests.json'
            evidence = json.loads(path.read_bytes())
            evidence_validator.validate(evidence)
            self.assertEqual(evidence['driver_ids'], [game])
            self.assertEqual(evidence['machine_ids'], [builder.MACHINES[game]])
            self.assertEqual(evidence['runtime']['rom_archive_sha256'], builder.ROM_HASHES[game])
            self.assertEqual(evidence['runtime']['emulator']['sha256'], builder.LIBRARY)

    def test_frames_decode_actual_glyphs_and_fail_on_mutation(self):
        self.assertEqual(builder.alpha.decode_alpha([0x0006, 0x8006]), '11.')
        seed = json.loads(builder.SEED.read_bytes())['runs']['radcl_l1/coil-test']
        row = [0x0006]
        value = {'segments_sha256': builder.alpha.frame_digest(row), 'readings': ['1']}
        reader = builder.Readings('test', {'example': value}, False)
        self.assertEqual(reader.read('example', row), ['1'])
        reader.finish()
        with self.assertRaisesRegex(ValueError, 'frame-reading mismatch'):
            builder.Readings('test', {'example': {**value, 'readings': ['O']}}, False).read('example', row)
        with self.assertRaisesRegex(ValueError, 'frame-reading mismatch'):
            builder.Readings('test', {'example': value}, False).read('example', [0x8006])
        self.assertIn('menu title', seed)

    def test_c_side_coil_without_relay_is_rejected(self):
        trace = {'events': [{'event': 'solenoid', 'number': 25, 'state': 1, 'time_s': 1.0}]}
        with self.assertRaisesRegex(ValueError, 'relay 12 was off'):
            builder.coils(trace, 0, builder.Readings('test', {}, True))
        trace['events'] = [{'event': 'solenoid', 'number': 12, 'state': 1, 'time_s': .5},
                           {'event': 'solenoid', 'number': 25, 'state': 1, 'time_s': 1.0},
                           {'event': 'solenoid', 'number': 26, 'state': 1, 'time_s': 2.0}]
        with self.assertRaisesRegex(ValueError, 'lacks a preceding relay rise'):
            builder.coils(trace, 0, builder.Readings('test', {}, True))

    def test_score_contact_response_must_match_the_actual_driver(self):
        pairs = {50: 22, 52: 17, 53: 19, 54: 21, 55: 18, 56: 20}
        trace = {'steps': [{'label': f'hold public switch {switch}', 'switch': switch,
                            'transitions': {'solenoids': [{'number': coil, 'states': [1, 0]}]}}
                           for switch, coil in pairs.items()]}
        observations = builder.switch_causal_observations(trace, 'radcl_l1')
        self.assertEqual([(switch, [coil]) for switch, coil in pairs.items()],
                         [(o['input_address'], o['transitioned_solenoid_addresses']) for o in observations])
        self.assertTrue(all(not o['observed_switch_addresses'] for o in observations))
        trace['steps'][0]['transitions']['solenoids'][0]['number'] = 17
        with self.assertRaisesRegex(ValueError, 'expected only driver 22'):
            builder.switch_causal_observations(trace, 'radcl_l1')

    def test_power_up_observation_requires_the_whole_byte_cluster(self):
        events = [{'event': 'solenoid', 'number': n, 'state': state,
                   'time_s': at + (n - 9) * .000005}
                  for state, at in ((1, .216), (0, .266)) for n in range(9, 17)]
        self.assertIn('whole-byte transient', builder.initialization_observation({'events': events}, 'radcl_l1')['note'])
        with self.assertRaisesRegex(ValueError, 'controlled-driver byte transient'):
            builder.initialization_observation({'events': [e for e in events if e['number'] != 15]}, 'radcl_l1')
        events[7]['time_s'] += .01
        with self.assertRaisesRegex(ValueError, 'not one rise/clear cluster'):
            builder.initialization_observation({'events': events}, 'radcl_l1')

    def test_service_differences_are_retained_as_display_readings(self):
        def runs(suffix):
            path = ROOT / f'evidence/runtime/system-11/radical-{suffix}-service-tests.json'
            return json.loads(path.read_bytes())['runtime']['observations']['runs']
        production, german, prototype = runs('l1'), runs('g1'), runs('p3')
        for old, new in [('5:3 = NOT USED', '5:3 = BALL POPPER'), ('23:15 = NOT USED', '23:15 = TOP SLING')]:
            self.assertIn(old, production['coil-test']['note'])
            self.assertIn(new, prototype['coil-test']['note'])
        for old, new in [('16 = SNAKE RUN', '16 = BALL POPPER'), ('28 = SPOT LETTER', '28 = ADV BONUS X'), ('49 = NOT USED', '49 = TOP SLING')]:
            self.assertIn(old, production['switch-levels']['note'])
            self.assertIn(new, prototype['switch-levels']['note'])
        self.assertIn('GESCHLO. KONTAKT', german['switch-levels']['note'])
        self.assertIn('Host writes and their readback are stimulus', german['switch-levels']['limitation'])

    def test_raw_hash_mutation_and_scenario_drift_are_rejected(self):
        # Synthetic run exercises the same loader without needing external evidence roots.
        with tempfile.TemporaryDirectory(dir=os.environ.get('RADICAL_TEST_TMP')) as temp:
            root = Path(temp)
            scenario = root / builder.SCENARIO_DIR / 'radcl-nvram-init.json'
            scenario.parent.mkdir(parents=True)
            scenario.write_bytes((ROOT / builder.SCENARIO_DIR / scenario.name).read_bytes())
            scenario_hash = hashlib.sha256(scenario.read_bytes()).hexdigest()
            run = {'game': 'radcl_l1', 'failure': None, 'library_sha256': builder.LIBRARY,
                   'scenario': {'sha256': scenario_hash, 'action_count': 1}, 'steps': [{}]}
            path = root / 'original/runs/radcl_l1-nvram-init.json'
            path.parent.mkdir(parents=True)
            original = json.dumps(run).encode()
            path.write_bytes(original)
            digest = hashlib.sha256(original).hexdigest()
            with mock.patch.object(builder, 'ROOT', root), mock.patch.dict(builder.RAW_HASHES, {'radcl_l1/nvram-init': digest}):
                self.assertEqual(builder.load_run(root, 'radcl_l1', 'nvram-init')['game'], 'radcl_l1')
                path.write_bytes(original + b' ')
                with self.assertRaisesRegex(ValueError, 'raw run digest mismatch'):
                    builder.load_run(root, 'radcl_l1', 'nvram-init')
                path.write_bytes(original)
                scenario.write_bytes(scenario.read_bytes() + b' ')
                with self.assertRaisesRegex(ValueError, 'scenario drift'):
                    builder.load_run(root, 'radcl_l1', 'nvram-init')

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'external review-artifacts root is unset')
    def test_recompute_retained_evidence_and_manifest(self):
        review_root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        manifest, records, _ = builder.build(review_root)
        bundle = review_root / builder.BUNDLE_RELATIVE
        builder.manifests.check_manifest(bundle, 'radcl_l1')
        self.assertEqual((bundle / 'manifest.json').read_bytes(), manifest)
        for game, evidence in records.items():
            path = ROOT / f'evidence/runtime/system-11/radical-{game.split("_")[1]}-service-tests.json'
            self.assertEqual(path.read_bytes(), builder.canonical_bytes(evidence))

    @unittest.skipUnless(os.environ.get('PINMAME_ROM_LIBRARY_ROOT'), 'authorized ROM root is unset')
    def test_authorized_rom_archive_members_match_pinned_source(self):
        root = Path(os.environ['PINMAME_ROM_LIBRARY_ROOT'])
        for game in builder.GAMES:
            archive = root / f'{game}.zip'
            self.assertEqual(builder.sha(archive), builder.ROM_HASHES[game])
            with zipfile.ZipFile(archive) as zf:
                for name, expected in builder.ROM_MEMBERS[game]:
                    self.assertEqual(hashlib.sha1(zf.read(name)).hexdigest(), expected, f'{game}/{name}')


if __name__ == '__main__':
    unittest.main()
