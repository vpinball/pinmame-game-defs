from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import unittest
from unittest import mock

import jsonschema
import build_phantom_runtime_evidence as builder

ROOT = Path(__file__).resolve().parents[1]


class PhantomRuntimeEvidenceTests(unittest.TestCase):
    def test_portable_evidence_and_pins(self):
        evidence = json.loads((ROOT / builder.OUTPUT).read_bytes())
        jsonschema.Draft202012Validator(json.loads((ROOT / 'schemas/evidence.schema.json').read_bytes())).validate(evidence)
        self.assertEqual(evidence['driver_ids'], ['poto_a32'])
        self.assertEqual(evidence['machine_ids'], ['data-east.phantom-of-the-opera.1990'])
        self.assertEqual(evidence['source']['path'], 'external:pinmame-review-artifacts/' + builder.RUN_ROOT)
        self.assertEqual(evidence['source']['sha256'], builder.RUNS['direct1'][1])
        self.assertIn(builder.RUNS['direct2'][1], evidence['source']['manifest_algorithm'])
        self.assertEqual(builder.digest(ROOT / builder.SCENARIO), builder.SCENARIO_SHA)
        self.assertEqual(evidence['runtime']['rom_archive_sha256'], builder.ROM_SHA)
        runs = evidence['runtime']['raw_runs']
        self.assertEqual([r['name'] for r in runs], list(builder.RUNS))
        for run in runs:
            self.assertEqual(run['sha256'], builder.RUNS[run['name']][0])
            self.assertEqual(run['scenario_sha256'], builder.SCENARIO_SHA)
            self.assertEqual(run['retained_from'], f'{builder.RUN_ROOT}/{run["name"]}/run.json')
        observations = evidence['runtime']['observations']['runs']['direct1']['named_action_observations']
        self.assertTrue(all(item['observed_switch_addresses'] == [] for item in observations))
        self.assertEqual([len(item['display_responses']) for item in observations], [128, 128, 48])
        for item, expected in zip(observations, [set(range(1, 65)), set(range(1, 65)), set(builder.EXPECTED_CYCLE)]):
            self.assertEqual({x['diagnostic_address'] for x in item['display_responses']}, expected)

    def test_decoder_keeps_unknowns(self):
        self.assertEqual(builder.decoded({'text': '???', 'segments': [6, 0x0867, 0x1234]}), '19?')
        with self.assertRaises(ValueError):
            builder.decoded({'text': '??', 'segments': [6]})

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'external evidence root not configured')
    def test_external_runs_and_mutation_guards(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        self.assertEqual(builder.canonical_bytes(builder.build(root)), (ROOT / builder.OUTPUT).read_bytes())
        scenario = json.loads((ROOT / builder.SCENARIO).read_bytes())
        run = builder.load_run(root, 'direct1', scenario)
        archive_root = Path(os.environ.get('PINMAME_ROM_LIBRARY_ROOT') or run['rom_path'])
        # An explicit location takes precedence over the environment; an
        # unavailable configured archive must never fall back silently.
        with mock.patch.dict(os.environ, {'PINMAME_ROM_LIBRARY_ROOT': str(root / 'missing-rom-root')}):
            with self.assertRaises(FileNotFoundError):
                builder.build(root)
            self.assertEqual(builder.canonical_bytes(builder.build(root, archive_root)), (ROOT / builder.OUTPUT).read_bytes())
        with mock.patch.dict(os.environ, {'PINMAME_ROM_LIBRARY_ROOT': str(archive_root)}):
            self.assertEqual(builder.canonical_bytes(builder.build(root)), (ROOT / builder.OUTPUT).read_bytes())
        seed = json.loads((ROOT / builder.SEED).read_bytes())
        original = builder.walk(run)
        for key in seed:
            self.assertEqual(original[key], seed[key])
        self.assertEqual(original['coil_sequence'][:24], builder.EXPECTED_CYCLE)

        def check_mutation(mutator):
            changed = copy.deepcopy(run)
            mutator(changed)
            with self.assertRaises((ValueError, KeyError)):
                builder.walk(changed)

        def reference(r):
            snap = next(s for s in r['snapshots'] if s['label'] == 'reference switch 1 before probe 4 (held)')
            snap['displays'][0]['segments'][1] ^= 1
        def address(r):
            snap = next(s for s in r['snapshots'] if s['label'] == 'close matrix switch 4 in Switch Test (held)')
            snap['displays'][1]['text'] = snap['displays'][1]['text'][:-1] + '3'
        def hold(r):
            next(s for s in r['steps'] if s['label'] == 'close matrix switch 4 in Switch Test')['hold_ms'] = 10
        def lamp(r):
            next(s for s in r['snapshots'] if s['label'] == 'Start step 1 in the discrete Lamp Test')['active_lamps'] = [3]
        def missing_coil(r):
            for e in r['events']:
                if e['event'] == 'solenoid' and e['number'] == 32:
                    e['state'] = 0
        for mutator in (reference, address, hold, lamp, missing_coil):
            with self.subTest(mutator=mutator.__name__):
                check_mutation(mutator)

        real_digest = builder.digest
        for suffix in (str(builder.SCENARIO), 'rom-index.json', 'poto_a32.zip'):
            def bad_digest(path, suffix=suffix):
                return '0' * 64 if str(path).endswith(suffix) else real_digest(path)
            with self.subTest(drift=suffix), mock.patch.object(builder, 'digest', side_effect=bad_digest):
                with self.assertRaises(ValueError):
                    builder.build(root)
        changed_readings = copy.deepcopy(original)
        changed_readings['switch_test']['4']['name'] = 'WRONG'
        with mock.patch.object(builder, 'walk', return_value=changed_readings):
            with self.assertRaises(ValueError):
                builder.build(root)
        # A client-side success label cannot override invalid identity fields.
        for key, value in [('failure', {'error': 'failed'}), ('game', 'wrong'),
                           ('library_sha256', '0' * 64), ('handle_mechanics', 1), ('scenario', {'sha256': '0' * 64, 'action_count': 202})]:
            changed = copy.deepcopy(run)
            changed[key] = value
            with self.subTest(field=key), mock.patch.object(builder, 'check_manifest', return_value=builder.RUNS['direct1'][1]), \
                 mock.patch.object(builder, 'digest', return_value=builder.RUNS['direct1'][0]), \
                 mock.patch.object(builder.json, 'loads', return_value=changed):
                with self.assertRaises(ValueError):
                    builder.load_run(root, 'direct1', scenario)


if __name__ == '__main__':
    unittest.main()
