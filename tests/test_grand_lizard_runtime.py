"""Regression checks for retained Grand Lizard runtime observations."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import grand_lizard_runtime_evidence as evidence
from build_external_evidence_manifest import check_manifest, write_manifest
from pinmame_game_defs.jsonio import canonical_bytes


class CompactEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(evidence.OUT.read_bytes())

    def test_compact_schema_and_assertions_without_external_files(self):
        schema = json.loads((evidence.ROOT / 'schemas/evidence.schema.json').read_bytes())
        jsonschema.Draft202012Validator(schema).validate(self.document)
        evidence.validate_compact(self.document)
        self.assertEqual(self.document['source']['sha256'], evidence.MANIFEST)
        self.assertEqual(self.document['runtime']['rom_archive_sha256'], evidence.ROM)

    def test_mutated_compact_assertion_rejected(self):
        doc = copy.deepcopy(self.document)
        run = doc['runtime']['observations']['runs']['depletion']
        run['note'] = run['note'].replace('"blinking_then_off":44', '"blinking_then_off":45', 1)
        with self.assertRaises(ValueError):
            evidence.validate_compact(doc)

    def test_system_11_segment_punctuation(self):
        self.assertEqual(evidence.glyph(0x1136), 'N')
        self.assertEqual(evidence.glyph(0x9136), 'N.')
        self.assertEqual(evidence.glyph(0x11b6), 'N,')
        self.assertEqual(evidence.glyph(0x91b6), 'N,.')
        self.assertEqual(evidence.glyph(0x8000), ' .')
        self.assertEqual(evidence.glyph(0x0080), ',')

    def test_manifest_detects_content_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / 'trace.json').write_text('one', encoding='utf-8')
            write_manifest(folder, 'grand_l4')
            check_manifest(folder, 'grand_l4')
            (folder / 'trace.json').write_text('two', encoding='utf-8')
            with self.assertRaises(ValueError):
                check_manifest(folder, 'grand_l4')


@unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'external review artifacts not configured')
class RetainedTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        cls.folder = cls.root / evidence.HARNESS
        cls.runs = {name: json.loads((cls.folder / value[0]).read_bytes()) for name, value in evidence.RUNS.items()}

    def test_recomputed_evidence_matches_committed_bytes(self):
        self.assertEqual(canonical_bytes(evidence.build(self.root)), evidence.OUT.read_bytes())

    def test_mutated_coil_frame_rejected(self):
        run = copy.deepcopy(self.runs['coil'])
        frames = [item for item in run['events'] if item['event'] == 'display' and item['index'] == 0 and item['time_s'] <= 25.380385 + .15]
        if not frames:
            self.fail('expected display event absent')
        frames[-1]['segments'][1] = 0
        with self.assertRaises(ValueError):
            evidence.coil_observations(run)

    def test_mutated_gameplay_response_and_parameters_rejected(self):
        run = copy.deepcopy(self.runs['gameplay'])
        evidence.one(run['steps'], 'left sling isolation')['transitions']['solenoids'][0]['number'] = 18
        with self.assertRaises(ValueError):
            evidence.gameplay_observations(run)
        run = copy.deepcopy(self.runs['gameplay'])
        evidence.one(run['steps'], 'left cabinet button held')['type'] = 'pulse'
        with self.assertRaises(ValueError):
            evidence.gameplay_observations(run)

    def test_mutated_depletion_and_switch_frames_rejected(self):
        run = copy.deepcopy(self.runs['depletion'])
        evidence.one(run['snapshots'], 'left Magna-save depletion 3')['active_lamps'].append(42)
        with self.assertRaises(ValueError):
            evidence.depletion_observations(run)
        run = copy.deepcopy(self.runs['switch-levels'])
        snap = evidence.one(run['snapshots'], 'public 45 active hold')
        next(x for x in snap['displays'] if x['index'] == 0)['segments'][2] = 0
        with self.assertRaises(ValueError):
            evidence.switch_observations(run)


if __name__ == '__main__':
    unittest.main()
