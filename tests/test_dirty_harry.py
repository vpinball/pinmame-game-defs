"""Dirty Harry's evidence, public contract and deterministic curation guards."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import curate_dirty_harry as curator
import dirty_harry_harness as headers
from pinmame_game_defs.jsonio import canonical_bytes,load_json
from pinmame_game_defs.schema_validation import validate_against_schema

class DirtyHarryTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.definition=curator.build()
		cls.seed=curator.load_seed()
		cls.switches={d['binding']['device']:d for d in cls.definition['inputs'] if d['binding']['group']==curator.SW}
		cls.outputs={group:{d['binding']['device']:d for d in cls.definition['outputs'] if d['binding']['group']==group} for group in (curator.SOL,curator.LAMP,curator.GI)}

	def test_identity_variants_and_no_stale_stub(self):
		d=self.definition
		self.assertEqual((d['machine']['id'],d['machine']['ipdb_id'],d['machine']['opdb_id'],d['machine']['model_number']),('williams.dirty-harry.1995',684,'GrJ2Z-M61Xd','50030'))
		self.assertEqual({x['id'] for x in d['drivers']},{'dh_lx2','dh_dx2','dh_lf2'})
		self.assertTrue(all(x['physical_compatibility']=='identical' for x in d['drivers']))
		attached=[x for x in load_json(ROOT/'catalog/pinmame.json')['drivers'] if x.get('machine_id')==curator.MACHINE_ID]
		self.assertEqual({x['id'] for x in attached},{'dh_lx2','dh_dx2','dh_lf2'})
		self.assertTrue(all(x['definition']==curator.MACHINE.as_posix() and x['coverage_status']=='partial' for x in attached))
		for p in (ROOT/'machines/stubs').rglob('*.json'):
			self.assertFalse({'dh_lx2','dh_dx2','dh_lf2'} & {x['id'] for x in load_json(p)['drivers']},p)

	def test_full_address_disposition_and_ranges(self):
		expected=set(range(1,9))|set(curator.MATRIX)|set(range(91,99))|set(range(101,109))|set(range(111,119))
		self.assertEqual(set(self.switches),expected)
		self.assertEqual({d['binding']['device'] for d in self.definition['inputs'] if d['kind']=='dip_switch'},set(range(1,9)))
		self.assertEqual(set(self.outputs[curator.SOL]),set(range(1,51)))
		self.assertEqual(set(self.outputs[curator.LAMP]),set(curator.MATRIX))
		self.assertEqual(set(self.outputs[curator.GI]),set(range(5)))
		self.assertEqual([d['binding'] for d in self.definition['inputs']+self.definition['outputs'] if d['availability']=='unknown'],[])
		self.assertEqual(self.outputs[curator.SOL][30]['label'],'J111 GPIO Bit 6')
		self.assertEqual(self.outputs[curator.SOL][30]['roles'],['internal.wpc-state'])
		self.assertEqual(self.outputs[curator.SOL][30]['spatial']['reason'],'virtual')
		self.assertEqual({a for a,d in self.outputs[curator.LAMP].items() if d['availability']=='unused'},set(range(71,77)))

	def test_public_polarity_and_physical_construction_are_separate(self):
		masked={a for a in curator.MATRIX if curator.MASK[a//10] & (1<<(a%10-1))}
		self.assertEqual(masked,set(range(31,39))|set(range(41,48)))
		for a in curator.SWITCHES:
			if a!=24:self.assertEqual(self.switches[a]['normally_closed'],a in masked,a)
		self.assertEqual(self.switches[24]['kind'],'constant')
		self.assertTrue(self.switches[24]['constant_active'])
		for a in (111,112,113,114,115,116,118):self.assertFalse(self.switches[a]['normally_closed'],a)
		self.assertEqual(self.switches[117]['availability'],'unused')
		for a in (76,77):self.assertEqual(self.switches[a]['physical']['switch_type'],'microswitch')

	def test_amendment_overrules_stale_sample_names(self):
		for a in (6,25,36):
			d=self.outputs[curator.SOL][a]
			self.assertEqual((d['availability'],d['spatial']['reason']),('unused','unused'))
			self.assertIn(curator.AMENDMENT,d['provenance']['source_refs'])
			self.assertIn('sample',d['physical']['notes'].lower())
		for a in (53,88):self.assertEqual(self.switches[a]['availability'],'unused')
		self.assertEqual(self.outputs[curator.SOL][4]['physical']['part_number'],'AE-23-800')
		self.assertEqual({x['id'] for x in self.definition['drivers']},{'dh_lx2','dh_lf2','dh_dx2'})

	def test_flipper_numbering_and_mechanism_topology(self):
		for public,printed in ((45,29),(46,30),(47,31),(48,32)):
			self.assertIn({'namespace':'manual.address','value':str(printed)},self.outputs[curator.SOL][public]['aliases'])
		self.assertEqual(self.outputs[curator.SOL][35]['kind'],'magnet')
		gun=next(x for x in self.definition['mechanisms'] if x['id']=='mechanism.gun')
		self.assertEqual(set(gun['actuators']),{f'device.solenoid-{n}' for n in (3,5,8,16,20)})
		self.assertEqual(set(gun['sensors']),{f'switch.matrix-{n}' for n in (11,44,45,76,77)})
		self.assertIn('substitution',self.switches[77]['physical']['notes'])
		self.assertNotIn(('device.solenoid-20','switch.matrix-77'),{(x['source'],x['destination']) for x in self.definition['relationships']})
		self.assertEqual(self.definition['displays'][0]['width'],128)
		self.assertEqual(self.definition['displays'][0]['height'],32)
		# Every fitted physical actuator, including ordinary jets/slings and the
		# cabinet knocker, belongs to the recreation mechanism inventory.
		owned={a for m in self.definition['mechanisms'] for a in m['actuators']}
		physical={d['id'] for d in self.outputs[curator.SOL].values() if d['availability']=='used' and d['kind'] in ('coil','motor','magnet')}
		self.assertTrue(physical<=owned,physical-owned)
		for sw,coil,identifier in ((61,9,'left-slingshot'),(62,10,'right-slingshot'),(63,11,'left-jet'),(64,12,'middle-jet'),(65,13,'right-jet')):
			m=next(m for m in self.definition['mechanisms'] if m['id']=='mechanism.'+identifier)
			self.assertEqual((m['sensors'],m['actuators']),([f'switch.matrix-{sw}'],[f'device.solenoid-{coil}']))

	def test_literal_tables_preserve_blanks_shading_and_misprints(self):
		text=(ROOT/'evidence/excerpts/williams.dirty-harry.1995/matrix-and-switches.md').read_text(encoding='utf-8')
		self.assertIn('| 5 | Red-Green | J134-6 | Q87 |',text)
		self.assertIn('| 6 | Red-Blue | J134-7 | Q86 |',text)
		self.assertIn('31 Trough Jam [shaded]',text)
		self.assertIn('| 53 | [blank] | Not Used |',text)
		self.assertEqual(self.seed['wiring']['switch']['38']['drive_connection'],'J207-3')
		self.assertEqual(self.seed['wiring']['switch']['38']['return_connection'],'J209-9')

	def test_spatial_provenance_precision_and_projection_roles(self):
		for coll in self.seed['placements'].values():
			for a,entries in coll.items():
				for e in entries:
					for k in ('x','y'):self.assertTrue(0<=e[k]<=1);self.assertEqual(e[k],round(e[k],6))
					if m:=e.get('measurement'):
						x,y=m['pixel'];l,t,r,b=m['frame']
						self.assertEqual((e['x'],e['y']),(round((x-l)/(r-l),3),round((y-t)/(b-t),3)))
		self.assertEqual(self.outputs[curator.SOL][17]['physical']['quantity'],2)
		self.assertEqual(len(self.outputs[curator.SOL][17]['spatial']['placements']),2)
		self.assertTrue(all('Projection' in self.switches[a]['physical']['notes'] for a in range(31,36)))
		self.assertNotIn('spatial',self.outputs[curator.GI][0])
		self.assertEqual([len(self.seed['placements']['gi'].get(str(a),[])) for a in (0,1,4)],[0,3,8])
		for a in (1,4):self.assertNotIn('quantity',self.outputs[curator.GI][a]['physical'])

	def test_sources_excerpts_and_honest_partial_gate(self):
		self.assertEqual(validate_against_schema(self.definition,ROOT/'schemas/machine.schema.json','Dirty Harry'),[])
		for source in self.definition['sources']:
			self.assertIn('license',source);self.assertIn('attribution',source)
			for e in source.get('excerpts',[]):
				self.assertEqual(hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest(),e['sha256'])
		self.assertEqual(self.definition['coverage']['missing'],['spatial_placement'])
		self.assertEqual(self.definition['coverage']['status'],'partial')
		self.assertEqual(curator.report(self.definition)['format'],'pinmame-spatial-blockers')

	def test_deterministic_artifacts_and_failure_guards(self):
		with patch.dict(os.environ,{},clear=True):curator.check();curator.check()
		with tempfile.TemporaryDirectory() as temp:
			r=Path(temp)
			paths=[curator.SEED,curator.CIRCUIT_SEED,curator.SPATIAL_SEED,curator.NOTE_SEED,*curator.artifacts()]
			paths += [Path(p) for p in self.seed['committed_artifacts']]
			paths += [Path(e[k]) for s in self.definition['sources'] for e in s.get('excerpts',[]) for k in ('path','image') if k in e]
			for p in set(paths):(r/p).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p,r/p)
			with patch.dict(os.environ,{},clear=True):curator.check(r)
			scenario=r/'tools/harness-scenarios/wpc-security/dh-mechanisms.json'
			scenario.write_bytes(scenario.read_bytes()+b' ')
			with self.assertRaisesRegex(ValueError,'committed evidence drift'):curator.build(r)
			shutil.copyfile(ROOT/scenario.relative_to(r),scenario)
			excerpt=r/'evidence/excerpts/williams.dirty-harry.1995/mechanisms.md'
			excerpt.write_text('drift',encoding='utf-8')
			with self.assertRaisesRegex(ValueError,'excerpt drift'):curator.build(r)
			shutil.copyfile(ROOT/excerpt.relative_to(r),excerpt)
			p=r/'machines/author-ready/williams/dirty-harry-1995.json';p.parent.mkdir(parents=True);p.write_text('{}')
			with self.assertRaisesRegex(ValueError,'author-ready'):curator.artifacts(r)
		with patch.dict(os.environ,{'PINMAME_VPX_SOURCES_ROOT':'Z:/missing-dirty-harry-root'},clear=True):
			with self.assertRaisesRegex(ValueError,'retained artifact mismatch'):curator.verify_external()

	def test_dmd_masks_match_one_verified_title_only(self):
		for title,t in headers.TEMPLATES.items():
			frame=bytearray(4096);first,last=t['rows'];frame[first*128:(last+1)*128]=base64.b64decode(t['mask'])
			self.assertEqual(headers.match_titles(frame,128,32),[title])
		self.assertEqual(headers.match_titles(bytes(4096),128,32),[])
		self.assertEqual(headers.match_titles(bytes(4096),64,64),[])

	def test_runtime_ledger_covers_named_causal_probes(self):
		ledger=load_json(ROOT/'tools/seeds/williams/dirty-harry-1995-runtime.json')
		self.assertEqual(set(ledger['runs']),{'dh-switch-edges','dh-solenoid-test','dh-flasher-test','dh-gun-explore','dh-mechanisms','dh-lighting-flippers','dh-gun-feedback','dh-gun-static'})
		steps=ledger['runs']['dh-mechanisms']['steps']
		for label,outputs in [('Up starts gun motor',{20}),('Down stops gun motor',{20}),('42 -> 1',{35}),('gun trigger requests test serve',{1,8,16}),('15 -> 1',{2}),('45 -> 1',{5})]:
			self.assertEqual({x['number'] for x in next(s for s in steps if s['label']==label)['solenoid_transitions']},outputs)
		chamber=[s for s in steps if s['label']=='44 -> 1']
		self.assertEqual(len(chamber),2)
		self.assertNotEqual(chamber[0]['step'],chamber[1]['step'])
		for s in chamber:self.assertEqual(s['solenoid_transitions'],[{'number':3,'states':[1,0]}])
		self.assertAlmostEqual(ledger['runs']['dh-gun-feedback']['motor20_intervals_s'][-1],24.600,places=3)
		self.assertAlmostEqual(ledger['runs']['dh-gun-static']['motor20_intervals_s'][-1],24.600,places=3)
		for run in ledger['runs'].values():
			self.assertEqual(hashlib.sha256((ROOT/run['scenario']['path']).read_bytes()).hexdigest(),run['scenario']['sha256'])

	def test_runtime_guards_reject_changed_observation_and_timing(self):
		pinned={'library_sha256':'library','scenario':{'sha256':'scenario'},'motor20_intervals_s':[24.0,24.6],
			'steps':[{'step':1,'label':'motor start','solenoid_transitions':[{'number':20,'states':[1]}],'active_solenoids':[20],'display_pixel_sha256':'pixels'}]}
		run={'failure':None,'game':'dh_lx2','handle_mechanics':0,'library_sha256':'library','scenario':{'sha256':'scenario'},
			'steps':[{'step':1,'label':'motor start','transitions':{'solenoids':[{'number':20,'states':[1]}]}}],
			'snapshots':[{}, {'label':'motor start','active_solenoids':[20],'displays':[{'pixel_sha256':'pixels'}]}],
			'events':[{'event':'solenoid','number':20,'state':v,'time_s':t} for v,t in [(1,0.0),(0,24.0),(1,100.0),(0,124.6)]]}
		curator.verify_run(pinned,run,'fixture')
		for key,value in [('failure',{'message':'incomplete'}),('game','dh_lf2'),('handle_mechanics',1),('library_sha256','changed')]:
			changed=copy.deepcopy(run);changed[key]=value
			with self.assertRaises(ValueError):curator.verify_run(pinned,changed,'fixture')
		changed=copy.deepcopy(run);changed['steps'][0]['transitions']['solenoids']=[]
		with self.assertRaisesRegex(ValueError,'observation drift'):curator.verify_run(pinned,changed,'fixture')
		changed=copy.deepcopy(run);changed['snapshots'][1]['displays'][0]['pixel_sha256']='changed'
		with self.assertRaisesRegex(ValueError,'observation drift'):curator.verify_run(pinned,changed,'fixture')
		changed=copy.deepcopy(run);changed['events'][-1]['time_s']+=1
		with self.assertRaisesRegex(ValueError,'timeout drift'):curator.verify_run(pinned,changed,'fixture')

	def test_geometry_guard_rejects_displaced_or_glow_only_light(self):
		point={'method':'center','source_path':'bulb.json','x':96.4,'y':216.2}
		seed={'placements':{'gi':{'1':[{'object':'bulb','object_type':'Light','table_point':point,'x':.1,'y':.1}]}}}
		with tempfile.TemporaryDirectory() as temp:
			folder=Path(temp);path=folder/'bulb.json'
			item={'Light':{'center':{'x':96.4,'y':216.2},'show_bulb_mesh':True}}
			path.write_text(json.dumps(item));curator.verify_table_points(seed,folder)
			item['Light']['center']['x']+=1;path.write_text(json.dumps(item))
			with self.assertRaisesRegex(ValueError,'point drift'):curator.verify_table_points(seed,folder)
			item['Light']['center']['x']=96.4;item['Light']['show_bulb_mesh']=False;path.write_text(json.dumps(item))
			with self.assertRaisesRegex(ValueError,'not an explicit bulb'):curator.verify_table_points(seed,folder)

	@unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'),'retained VPX evidence root not configured')
	def test_complete_retained_extraction_and_source_hashes(self):
		curator.verify_external()

if __name__=='__main__':unittest.main()
