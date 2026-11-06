"""Catacomb's independent table/address oracles and retained-evidence gates."""
from __future__ import annotations

import copy
import bisect
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import catacomb_data as data
import curate_catacomb as curator
from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]
MANUAL_PHYSICAL_TO_PUBLIC = dict(enumerate((2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18),1))
EXPECTED_MISSING = ['output_semantics', 'mechanism_behavior', 'spatial_placement']
SEGMENT_DIGITS = {0x3f:'0',0x06:'1',0x5b:'2',0x4f:'3',0x66:'4',0x6d:'5',0x7d:'6',0x07:'7',0x7f:'8',0x6f:'9',0:' '}


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def display_text(segments):
    return ''.join(SEGMENT_DIGITS.get(n & 0x7f, '?') for n in segments).strip()


class RawEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = data.load_raw()

    def test_decoder_independent_literal_oracle(self):
        rows = self.raw['lamp_rows']
        self.assertEqual(set(map(int, rows)), {n for n in range(1, 64) if n % 16})
        self.assertEqual({int(n) for n, row in rows.items() if row['printed_table_row'] is None}, {2, 29})
        for number, transistor in {2:'Q12', 29:'Q15', 24:'Q25', 25:'Q24', 42:'Q41', 58:'Q46'}.items():
            self.assertEqual(rows[str(number)]['diagram']['transistor'], transistor)
        self.assertEqual(rows['2']['diagram']['connector'], 'J1-19')
        self.assertEqual(rows['29']['diagram']['connector'], 'J2-23')

    def test_lamps_require_collection_and_timer(self):
        self.assertEqual({x['object'] for x in data.mapped_lights(self.raw, 15)}, {'l15', 'l15a'})
        self.assertEqual({x['object'] for x in data.mapped_lights(self.raw, 2)}, {'l2'})
        self.assertEqual(data.mapped_lights(self.raw, 29), [])
        bad = copy.deepcopy(self.raw)
        bad['collections']['AllLamps'].remove('l15')
        with self.assertRaises(ValueError):
            data.validate_raw(bad)

    def test_script_coordinates_are_tied_to_actual_objects(self):
        lines = '\n'.join(row['text'] for row in self.raw['script_lines']).lower()
        self.assertIn('sub bumper1_hit(): randomsoundbumpertop bumper1: vpmtimer.pulsesw 9', lines)
        self.assertIn('sub bumper2_hit(): randomsoundbumpermiddle bumper2: vpmtimer.pulsesw 10', lines)
        objects = {row['object'].lower(): row for row in self.raw['objects']}
        self.assertEqual(objects['sw4']['type'], 'Spinner')
        self.assertEqual(objects['sw5']['type'], 'Trigger')
        self.assertEqual(objects['sw27']['type'], 'HitTarget')
        self.assertEqual(objects['bumper1']['center'], {'x': 560.01685, 'y': 622.7359})
        self.assertEqual(data.normalize(self.raw, 560.01685, 622.7359), (0.587672, 0.315075))
        with self.assertRaises(ValueError):
            data.normalize(self.raw, -1, 1)

    def test_modern_and_older_flipper_key_paths_are_distinct(self):
        for field, key in (('script_lines', 'LeftFlipperKey'), ('archive_script_lines', 'RightFlipperKey')):
            text = '\n'.join(row['text'] for row in self.raw[field])
            for state in (1, 0):
                self.assertRegex(text, rf'(?is)If keycode = {key} Then\s+(?:(?!If keycode).)*Controller\.Switch\(8\)\s*=\s*{state}')
        modern = '\n'.join(row['text'] for row in self.raw['script_lines'])
        self.assertNotRegex(modern, r'(?is)If keycode = RightFlipperKey Then\s+(?:(?!If keycode).)*Controller\.Switch\(8\)')

    def test_unnamed_rows_cannot_be_removed(self):
        bad = copy.deepcopy(self.raw)
        del bad['lamp_rows']['2']
        with self.assertRaises(ValueError):
            data.validate_raw(bad)
        bad = copy.deepcopy(self.raw)
        bad['lamp_rows']['29']['printed_table_row'] = {'description': 'invented'}
        with self.assertRaises(ValueError):
            data.validate_raw(bad)

    def test_retained_sources_if_supplied(self):
        roots = [os.environ.get('PINMAME_VPX_SOURCES_ROOT'), os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT')]
        if not any(roots):
            self.skipTest('no external evidence roots provided')
        for root in roots:
            if root and not Path(root).is_dir():
                self.fail(f'provided evidence root does not exist: {root}')
        data.verify_sources(
            self.raw,
            vpx_root=Path(roots[0]) if roots[0] else None,
            review_root=Path(roots[1]) if roots[1] else None,
        )


class CanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = read_json(ROOT / curator.DEFINITION)
        cls.facts = read_json(ROOT / curator.FACTS)
        cls.raw = data.load_raw()
        cls.by_id = {d['id']:d for key in ('inputs','outputs','displays','mechanisms') for d in cls.definition[key]}
        cls.inputs = {d['binding']['device']:d for d in cls.definition['inputs'] if d['binding']['group']=='pinmame.input.switch'}
        cls.coils = {d['binding']['device']:d for d in cls.definition['outputs'] if d['binding']['group']=='pinmame.output.solenoid'}
        cls.lamps = {d['binding']['device']:d for d in cls.definition['outputs'] if d['binding']['group']=='pinmame.output.lamp'}

    def test_exact_identity_and_driver_ownership(self):
        machine = self.definition['machine']
        self.assertEqual((machine['id'],machine['name'],machine['manufacturer'],machine['year'],machine['ipdb_id'],machine['model_number'],machine['opdb_id']),
                         ('stern.catacomb.1981','Catacomb','Stern',1981,469,'147','GRoQ6-MLx0X'))
        drivers = {x['id']:x for x in self.definition['drivers']}
        self.assertEqual(set(drivers), {'catacomb','catacofp','cataconb'})
        self.assertEqual({d['physical_compatibility'] for d in drivers.values()}, {'identical'})
        self.assertIn('suppresses',drivers['cataconb']['variant_notes'])
        catalog = read_json(ROOT/'catalog/pinmame.json')
        claims = [x for x in catalog['drivers'] if x['id'] in drivers]
        self.assertEqual(len(claims),3)
        self.assertEqual({x['machine_id'] for x in claims},{machine['id']})
        self.assertEqual({x['definition'] for x in claims},{curator.DEFINITION.as_posix()})

    def test_full_legal_address_disposition(self):
        self.assertEqual(tuple(len(self.definition[k]) for k in ('inputs','outputs','displays','mechanisms')),(84,85,6,17))
        self.assertEqual(set(self.inputs),{-7,-6,-5}|set(range(1,41))|set(range(81,85)))
        self.assertEqual(set(self.coils),set(range(1,16))|set(range(17,21))|set(range(45,49)))
        self.assertEqual(set(self.lamps),{n for n in range(1,64) if n%16})
        dips = {d['binding']['device']:d for d in self.definition['inputs'] if d['kind']=='dip_switch'}
        self.assertEqual(set(dips),set(range(1,33)))
        self.assertEqual({n for n,d in dips.items() if d['availability']=='unused'},{5,13,14,29,30})
        self.assertEqual({n for n,d in self.inputs.items() if d['availability']=='unused'},{-5,81,83})
        self.assertEqual({n for n,d in self.coils.items() if d['availability']=='unused'},{15,17,18})
        for d in self.definition['inputs']+self.definition['outputs']:
            self.assertIn(d['availability'], {'used','unused','unknown','optional'})

    def test_numeric_compatibility_aliases_and_polarity(self):
        for n in range(1,41):
            d=self.inputs[n]
            self.assertFalse(d['normally_closed'])
            old={a['value'] for a in d['aliases'] if a['namespace']=='vpe-legacy.switch'}
            self.assertEqual(old,{str(n),f'{n:02}',f'{n:03}'})
        direct={d['binding']['device']:d for d in self.definition['inputs'] if d['binding']['group']=='physical.input.direct'}
        self.assertEqual(set(direct),{1,2,3,4,5})
        self.assertEqual({n for n,d in direct.items() if d['normally_closed']},{1,2,4})
        self.assertEqual(direct[3]['spatial']['reason'],'cabinet_or_service')
        self.assertEqual(direct[5]['wiring']['control_connection'],'A4J4-13')
        self.assertEqual(direct[5]['wiring']['return_connection'],'A3J2-7')
        self.assertEqual(self.inputs[8]['label'],'L. Flipper Button')
        self.assertIn('modern 2.0.1 script asserts and clears matrix input 8 from LeftFlipperKey', self.inputs[8]['physical']['notes'])
        self.assertIn('Only the older archive table uses RightFlipperKey', self.inputs[8]['physical']['notes'])
        self.assertTrue({'script.catacomb', 'archive-table.catacomb'} <= set(self.inputs[8]['provenance']['source_refs']))
        self.assertNotIn('return_wire',self.inputs[10]['wiring'])

    def test_separate_physical_memory_clear_buttons(self):
        mpu = self.inputs[-6]
        self.assertEqual((mpu['kind'], mpu['availability'], mpu['physical']['switch_type']), ('switch', 'used', 'button'))
        self.assertEqual(mpu['physical']['location'], 'MPU board in backbox')
        self.assertFalse(mpu['normally_closed'])
        self.assertEqual(mpu['spatial']['reason'], 'cabinet_or_service')
        self.assertEqual(mpu['wiring'], {'board':'MPU-200 A4', 'control_connection':'U9-6 (NMI)', 'return_connection':'Ground'})
        self.assertEqual(set(mpu['provenance']['source_refs']), {'core.catacomb', 'manual.catacomb', 'schematic.catacomb'})
        door = self.by_id['switch.direct-3']
        self.assertEqual(door['label'], 'Door memory-clear contact')
        self.assertEqual(door['binding'], {'group':'physical.input.direct', 'device':3})
        self.assertEqual(door['physical']['location'], 'Inside coin door')
        self.assertFalse(door['normally_closed'])
        self.assertEqual(door['wiring'], {'board':'MPU-200 A4 / SDU A3', 'control_connection':'A4J3-5', 'control_wire':'W', 'return_connection':'A3J2-7', 'return_wire':'Y-R'})

    def test_shared_contact_quantities_and_backbox_boundary(self):
        shared={14,15,16,22,23,24,30,31,32,38,39,40}
        for n in shared:
            d=self.inputs[n]
            self.assertEqual(d['physical']['quantity'],2)
            self.assertEqual(len(d['spatial']['placements']),1)
            self.assertIn('Backbox',d['label'])
            self.assertNotIn('triggerb',json.dumps(d['spatial']).lower())
        self.assertTrue(all(self.inputs[n]['initial_active'] for n in (33,34,35)))

    def test_physical_to_public_solenoid_mapping(self):
        oracle={1:('top thumper','Q2'),2:('bottom thumper','Q1'),3:('top slingshot','Q5'),4:('left slingshot','Q6'),5:('right slingshot','Q7'),
                6:('knocker','Q3'),7:('left kickout','Q4'),8:('right kickout','Q8'),9:('reflex','Q13'),10:('turnstyle','Q14'),
                11:('bank a','Q9'),12:('bank b','Q10'),13:('bank c','Q12'),14:('bank d','Q11'),19:('enable relay','Q15'),20:('backbox','Q18')}
        for n,(name,q) in oracle.items():
            self.assertIn(name,self.coils[n]['label'].lower())
            self.assertEqual(self.coils[n]['wiring']['driver_transistor'],q)
        for physical,public in MANUAL_PHYSICAL_TO_PUBLIC.items():
            self.assertIn({'namespace':'manual.self-test','value':str(physical)},self.coils[public]['aliases'])
        self.assertEqual(self.coils[19]['wiring'], {'board':'SDU-100 A3', 'driver_transistor':'Q15'})
        self.assertIn('on-board K1', self.coils[19]['physical']['notes'])
        self.assertEqual(self.coils[20]['provenance']['status'],'observed')
        self.assertNotIn('device.backbox-whip-coil',{r['destination'] for r in self.definition['relationships']})

    def test_lamp_semantics_from_independent_distinctive_rows(self):
        labels={1:'bank a lamp',17:'bank b lamp',33:'bank c lamp',49:'bank d lamp',3:'green 14',19:'blue 9',35:'amber 1',51:'red 6',
                15:'spinner 1000 point lamp top',31:'spinner 1000 point lamp middle',47:'spinner 1000 point lamp bottom',
                14:'left return lane',30:'right return lane',46:'left out lane',62:'right out lane',13:'high score',45:'game over',61:'tilt',63:'match'}
        for n,part in labels.items():self.assertIn(part,self.lamps[n]['label'].lower())
        self.assertEqual({n for n,d in self.lamps.items() if d['availability']=='unknown'},{2,29})
        self.assertEqual(self.lamps[2]['wiring']['control_connection'],'A5J1-19')
        self.assertEqual(self.lamps[29]['wiring']['control_connection'],'A5J2-23')
        for n in (2,29):
            self.assertNotIn('spatial',self.lamps[n])
            self.assertNotIn('quantity',self.lamps[n]['physical'])
        self.assertEqual(self.lamps[11]['physical']['quantity'],2)
        self.assertEqual(len(self.lamps[11]['spatial']['placements']),1)
        for n in (13,45,61,63):self.assertEqual(self.lamps[n]['spatial']['reason'],'cabinet_or_service')

    def test_mechanism_ownership_references_and_gi_open_inventory(self):
        owners={}
        for m in self.definition['mechanisms']:
            for identifier in m['actuators']:
                self.assertNotIn(identifier,owners)
                owners[identifier]=m['id']
                self.assertIn(identifier,self.by_id)
            for identifier in m['sensors']:self.assertIn(identifier,self.by_id)
        banks=[m for m in self.definition['mechanisms'] if m['kind']=='drop_target_bank']
        self.assertEqual(len(banks),4)
        self.assertEqual({len(m['sensors']) for m in banks},{3})
        gi=self.by_id['gi.transformer-illumination']
        self.assertEqual(len(gi['spatial']['placements']),23)
        self.assertNotIn('quantity',gi['physical'])
        self.assertEqual(gi['binding'],{'group':'physical.output.gi','device':1})
        self.assertIn('lower-post',gi['physical']['notes'])

    def test_exact_positions_meshes_projections_and_displays(self):
        p=self.inputs[9]['spatial']['placements'][0]
        self.assertEqual((p['x'],p['y']),(0.587672,0.315075))
        p=self.lamps[1]['spatial']['placements'][0]
        x,y=data.mesh_center(next(m for m in self.raw['meshes'] if m['object']=='bulb1'))
        self.assertEqual((p['x'],p['y']),data.normalize(self.raw,x,y))
        self.assertIn('bulb1',p['id'])
        pts=[curator.point(self.raw,f'sw{n}') for n in (14,15,16)]
        p=self.coils[11]['spatial']['placements'][0]
        self.assertEqual((p['x'],p['y']),data.normalize(self.raw,sum(x for x,y in pts)/3,sum(y for x,y in pts)/3))
        displays=self.definition['displays']
        self.assertEqual([(d['controller_index'],d['segment_start'],d['width']) for d in displays],[(0,1,7),(1,9,7),(2,17,7),(3,25,7),(4,35,2),(5,38,2)])
        self.assertTrue(all(d['spatial']['reason']=='cabinet_or_service' for d in displays))
        self.assertFalse(any(d.get('kind')=='video' for d in displays))
        note = (ROOT/curator.NOTE).read_text(encoding='utf-8')
        self.assertIn('automatically adds a synthetic 128 × 32 DMD for segment-only games', note)
        self.assertNotIn('video layout renders the backbox playfield', note)

    def test_pinned_provenance_and_fail_closed_promotion(self):
        sources={s['id']:s for s in self.definition['sources']}
        self.assertEqual(sources['manual.catacomb']['sha256'],'5219dc4d4791b0d4cff12ee0b8b48ca80c7afb9150bdb5a2b6c49a991f1202be')
        self.assertEqual(sources['schematic.catacomb']['sha256'],'45fd3691ca719eab243553b98967aef4fb7cbe6c1ce7340e3342ecf0a1d24294')
        self.assertEqual(sources['table.catacomb']['sha256'],'aa4566613123d8e511228497715d8c0bec0e68cc2ebc5fd2fb584e9c36a4628c')
        for source in sources.values():
            self.assertIn('license',source)
            for e in source.get('excerpts',[]):self.assertEqual(data.sha256(ROOT/e['path']),e['sha256'])
        self.assertTrue({'excerpt.catacomb.mpu-nmi', 'excerpt.catacomb.door-service'} <= {e['id'] for e in sources['schematic.catacomb']['excerpts']})
        self.assertIn('excerpt.catacomb.service-locations', {e['id'] for e in sources['manual.catacomb']['excerpts']})
        self.assertEqual(self.definition['coverage']['status'],'partial')
        self.assertEqual(self.definition['coverage']['missing'],EXPECTED_MISSING)
        bad=copy.deepcopy(self.definition);bad['coverage']['status']='author_ready';bad['coverage']['missing']=[]
        self.assertTrue(validate_machine(bad,ROOT))
        self.assertEqual(validate_machine(self.definition,ROOT),[])

    def test_drift_guard_and_byte_identical_seed(self):
        expected=curator.build()
        before={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in expected}
        curator.check();curator.check()
        self.assertEqual(before,{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in expected})
        self.assertEqual((ROOT/curator.SEED).read_bytes(),(ROOT/curator.DEFINITION).read_bytes())
        real=data.sha256
        def changed_excerpt(path):
            return '0'*64 if Path(path).name=='manual-tables.md' else real(path)
        with mock.patch.object(data,'sha256',side_effect=changed_excerpt):
            with self.assertRaisesRegex(ValueError,'excerpt digest mismatch'):curator.build()

    def test_no_sibling_machine_contamination(self):
        catalog=read_json(ROOT/'catalog/pinmame.json')
        text=(ROOT/curator.DEFINITION).read_text()+(ROOT/curator.NOTE).read_text()
        for machine in catalog['machines']:
            if machine['id']!='stern.catacomb.1981':self.assertNotIn(machine['id'],text)

    def test_external_artifacts_and_runtime_content_when_supplied(self):
        if not any(os.environ.get(e) for e in ('PINMAME_VPX_SOURCES_ROOT','PINMAME_MANUALS_ROOT','PINMAME_REVIEW_ARTIFACTS_ROOT')):
            self.skipTest('no external evidence roots supplied')
        curator.verify_external()
        review=os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT')
        if not review:return
        traces={name:read_json(Path(review)/record['path']) for name,record in self.facts['runtime'].items()}
        available = {e['index']:e for e in traces['self-test']['events'] if e['event']=='display_available'}
        self.assertEqual(set(available), set(range(7)))
        self.assertEqual(tuple(available[6][k] for k in ('type','width','height')), (14,128,32))
        self.assertEqual(len(self.definition['displays']), 6)
        trace=traces['coil-test']
        displays=[e for e in trace['events'] if e['event']=='display' and e['index']==0]
        times=[e['time_s'] for e in displays]
        pairs=[]
        for event in trace['events']:
            if event['event']=='solenoid' and event['state'] and event['time_s']>29:
                e=displays[bisect.bisect_right(times,event['time_s']+.25)-1]
                number=display_text(e['segments'])
                self.assertTrue(number.isdigit(),number)
                pairs.append((int(number),event['number']))
        for physical,public in pairs:self.assertEqual(MANUAL_PHYSICAL_TO_PUBLIC[physical],public)
        self.assertGreaterEqual(len(pairs),38)
        trace=traces['switch-test']
        for n in range(1,41):
            stimulus=[e for e in trace['events'] if e['event']=='switch' and e['number']==n]
            start=next(e['time_s'] for e in stimulus if e['state']==1)
            stop=next(e['time_s'] for e in stimulus if e['state']==0)
            texts={display_text(e['segments']) for e in trace['events'] if e['event']=='display' and e['index']==0 and start<e['time_s']<stop}
            self.assertIn(f'{n:02}',texts)
        actions={s['label']:s for s in traces['gameplay']['steps']}
        for sw,sol in ((9,1),(10,2),(11,3),(12,4),(13,5)):
            transitions=actions[f'isolated switch {sw}']['transitions']['solenoids']
            self.assertIn(sol,{x['number'] for x in transitions if 1 in x['states']})
        phases={s['label']:s for s in traces['bagatelle']['steps']}
        changes={x['number']:x['states'] for x in phases['bonus and bagatelle enable']['transitions']['solenoids']}
        self.assertEqual(changes[19],[0]);self.assertEqual(changes[20],[1])
        self.assertNotIn(20,{x['number'] for x in phases['bagatelle phase input 82']['transitions']['solenoids']})

    def test_supplied_bad_root_is_not_skipped(self):
        with mock.patch.dict(os.environ,{'PINMAME_VPX_SOURCES_ROOT':str(ROOT/'no-such-catacomb-root')}):
            with self.assertRaisesRegex(ValueError,'invalid evidence root'):curator.verify_external()


if __name__ == '__main__':
    unittest.main()
