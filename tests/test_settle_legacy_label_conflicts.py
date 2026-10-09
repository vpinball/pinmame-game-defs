from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import settle_legacy_label_conflicts as tool  # noqa: E402

PINNED_LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
# The ROM's own printed name for each settled address, as the evidence summary transcribes it.
ROM_NAMES = {
	("runtime.black-rose.br-l4.flasher-test", 19): "RIGHT BOTTOM",
	("runtime.no-fear.nf-23x.flasher-test", 19): "FLS. NO FEAR",
}
# Settlements read from a mechanism test rather than a name: the address, the output it always rises with, and the
# display text of the step in which it does.
PAIRED = {
	("runtime.red-and-ted-s-road-show.rs-l6.ted-test", 19): (20, "MOUTH OPEN / T.17 06 RUNNING"),
}
# Settlements read from a drop-target bank in play: the bank's other members and the raw step that closes each, the
# step that closes the address, and the relay that drops if the ROM tilts. Each closure must score. "points" requires
# every closure to score the same; "award" requires the address's closure to light lamps no member's closure lit;
# "reset" names the bank reset coil that only the address's closure fires.
BANKS = {
	("runtime.harlem-globetrotters-on-tour.hglbtrtr.switch-2-in-play", 2): {
		"members": {1: "drop target 1 down", 3: "drop target 3 down", 4: "drop target 4 down"},
		"step": "public 2 closed",
		"relay": 19,
		"points": 5000,
		"award": True,
	},
	("runtime.skateball.skatebll.switch-2-and-19-in-play", 2): {
		"members": {3: "center drop target 3 down", 4: "center drop target 4 down"},
		"step": "public 2 closed fires 10",
		"relay": 19,
		"reset": 10,
	},
}
SEVEN_SEGMENT = {0: "", 63: "0", 6: "1", 91: "2", 79: "3", 102: "4", 109: "5", 125: "6", 7: "7", 127: "8", 111: "9"}
# by6803.c CORE_SEG98 glyphs: bits 0-6 are segments a-g, 0x80 the comma, 0x300 the centre bar. The ROM's font draws O
# and 0, and S and 5, alike.
BY6803_ALPHA = {
	0x000: " ", 0x077: "A", 0x34F: "B", 0x039: "C", 0x30F: "D", 0x079: "E", 0x071: "F", 0x06F: "G", 0x076: "H",
	0x309: "I", 0x01E: "J", 0x038: "L", 0x337: "M", 0x307: "N", 0x03F: "O", 0x073: "P", 0x36B: "Q", 0x347: "R",
	0x06D: "S", 0x301: "T", 0x03E: "U", 0x30E: "V", 0x33E: "W", 0x040: "-", 0x006: "1", 0x05B: "2", 0x04F: "3",
	0x066: "4", 0x07D: "6", 0x007: "7", 0x07F: "8", 0x067: "9",
}
# Settlements read from a Bally 6803 service test on the alphanumeric displays: the top and bottom rows the ROM shows
# for the address (displays 0-1 and 2-4, each row's two seven-character modules joined with a space).
ALPHA_NAMES = {
	("runtime.special-force.specforc.switch-test", 2): ("CHOPPER TOP", "CLOSED"),
	("runtime.special-force.specforc.switch-test", 7): ("RIGHT LAUNCH", "CLOSED"),
	("runtime.special-force.specforc.switch-test", 16): ("RELEASE LEFT", "CLOSED"),
	("runtime.special-force.specforc.solenoid-test", 19): ("FLIPPER", "QO7 J6-8-9"),
}
BTC = "runtime.beat-the-clock.beatclck.drop-bank-and-switch-16-in-play"
SPECTRUM = "runtime.spectrum.spectru4.flipper-buttons-and-saucer-7"
BTC_TILT = {"tilt bob 15 #1": ([], None, True), "tilt bob 15 #2": ([19], None, False)}
SPECTRUM_TILT = {"tilt bob 15 #1": ([19], None, False)}
# Settlements read from gameplay: for each raw step, the solenoids that change in it, the score change it causes
# (None: not checked), and whether the flipper-enable relay 19 is raised after it. Controls are steps of other inputs.
PLAY = {
	(BTC, 2): {
		"ball 1: drop target 5 down": ([], 3000, True),
		"ball 1: public 2 closed": ([], 3000, True),
		"ball 2: drop target 5 down": ([], 3000, True),
		"ball 2: public 2 closed last": ([], 103000, True),
		**BTC_TILT,
	},
	(BTC, 7): {
		"ball 1: public 2 closed": ([], 3000, True),
		"ball 1: public 7 closed last": ([], 53000, True),
		"ball 2: public 7 closed": ([], 3000, True),
		**BTC_TILT,
	},
	(BTC, 16): {
		"ball 1: public 16 pulsed": ([], 3000, True),
		"ball 2: public 16 held": ([], 3000, True),
		**BTC_TILT,
	},
	(SPECTRUM, 2): {
		"public 2 to 1 with the ball on the saucer": ([], 0, True),
		"public 2 back to 0": ([], 0, True),
		"public 1 to 1 with the ball on the saucer": ([5], 0, True),
		"public 2 held at 1 in play": ([], 0, True),
		**SPECTRUM_TILT,
	},
	(SPECTRUM, 7): {
		"public 7 closed in play": ([1], 10000, True),
		**SPECTRUM_TILT,
	},
}
# Settlements read from a gameplay timeline: each raw step in which the address changes, and its states there, in order.
TIMELINES = {
	("runtime.skateball.skatebll.switch-2-and-19-in-play", 19): [
		("boot", [1, 0, 1, 0]),
		("start button changes 19", [1]),
		("checkpoint: game over changes 19", [0]),
	],
}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def timeline_mismatches(run: dict, address: int, timeline: list[tuple[str, list[int]]]) -> list[str]:
	"""Every change of the address must happen in the listed step, in the listed direction, in the listed order."""
	steps = {step["label"]: step for step in run["steps"]}
	problems = []
	states = [event["state"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == address]
	if states != [state for _, listed in timeline for state in listed]:
		problems.append(f"transitions {states}")
	for label, listed in timeline:
		changed = [item["states"] for item in steps[label]["transitions"]["solenoids"] if item["number"] == address]
		if changed != [listed]:
			problems.append(f"{label}: {changed}")
	return problems


def seven_segment(values: list[int]) -> int:
	# Bit 7 is the digit's comma.
	return int("".join(SEVEN_SEGMENT[value & 0x7F] for value in values) or "0")


def alpha(values: list[int]) -> str:
	return "".join(BY6803_ALPHA[value & ~0x80] + ("," if value & 0x80 else "") for value in values)


def alpha_rows(responses: list[dict]) -> tuple[str, str]:
	text = {item["display_index"]: alpha(item["segments"]) for item in responses}
	top = " ".join(part for part in (text[0].strip(), text[1].strip()) if part)
	bottom = " ".join(part for part in (text[2].strip(), (text[3] + text[4]).strip()) if part)
	return top, bottom


def alpha_frames(observation: dict) -> dict[str, list[dict]]:
	frames: dict[str, list[dict]] = {}
	for item in observation.get("display_responses", []):
		frames.setdefault(item["snapshot_label"], []).append(item)
	return frames


class LegacyLabelSettlementTests(unittest.TestCase):
	def test_every_settlement_is_applied_exactly(self) -> None:
		for settlement in tool.SETTLEMENTS:
			with self.subTest(machine=settlement["machine_id"]):
				path = ROOT / settlement["path"]
				record = load_json(path)
				self.assertNotIn(settlement["conflict_id"], {conflict["id"] for conflict in record["conflicts"]})
				# Re-applying the settlement is a no-op on the committed bytes.
				from pinmame_game_defs.jsonio import canonical_bytes

				self.assertEqual(path.read_bytes(), canonical_bytes(tool.settle(record, settlement)))
				(device,) = [item for item in record["outputs"] + record["inputs"] if item["binding"] == settlement["binding"]]
				self.assertEqual(settlement["label"], device["label"])
				self.assertEqual(settlement["kind"], device["kind"])
				self.assertEqual(settlement.get("id", f"device.{tool.slug(settlement['label'])}"), device["id"])
				for alias in settlement["drop_aliases"]:
					self.assertNotIn(alias, device["aliases"])
				self.assertEqual("observed", device["provenance"]["status"])
				self.assertIn(settlement["source"]["id"], device["provenance"]["source_refs"])
				unresolved = [item for item in record["conflicts"] if item.get("status", "unresolved") == "unresolved"]
				self.assertEqual(bool(unresolved), "unresolved_conflicts" in record["coverage"]["missing"])
				sources = {item["id"]: item for item in record["sources"]}
				self.assertEqual("runtime_scenario", sources[settlement["source"]["id"]]["kind"])
				# A manual or known-working script the run corroborates is recorded whole and cited after the run.
				refs = device["provenance"]["source_refs"]
				for item in settlement.get("extra_sources", []):
					self.assertEqual(item, sources[item["id"]])
					self.assertGreater(refs.index(item["id"]), refs.index(settlement["source"]["id"]))

	def test_each_settlement_is_tied_to_its_rom_run(self) -> None:
		for settlement in tool.SETTLEMENTS:
			source = settlement["source"]
			with self.subTest(source=source["id"]):
				evidence = load_json(ROOT / source["uri"][len("internal:"):])
				runtime = evidence["runtime"]
				self.assertEqual(PINNED_LIBRARY_SHA256, runtime["emulator"]["sha256"])
				self.assertEqual([settlement["machine_id"]], evidence["machine_ids"])
				# The last raw run is the evidentiary one; any earlier run only initialized its NVRAM.
				*setup, raw = runtime["raw_runs"]
				for item in runtime["raw_runs"]:
					scenario = ROOT / item["scenario_path"]
					self.assertEqual(hashlib.sha256(scenario.read_bytes()).hexdigest(), item["scenario_sha256"])
				self.assertEqual(raw["sha256"], evidence["source"]["sha256"])
				address = settlement["binding"]["device"]
				paired = PAIRED.get((source["id"], address))
				timeline = TIMELINES.get((source["id"], address))
				bank = BANKS.get((source["id"], address))
				rows = ALPHA_NAMES.get((source["id"], address))
				play = PLAY.get((source["id"], address))
				switch = settlement["binding"]["group"] == "pinmame.input.switch"
				observations = runtime["observations"]
				if rows:
					# The service test shows the address's rows in a frame the evidence keeps as raw segments.
					shown = []
					for item in observations["named_action_observations"]:
						for label, responses in alpha_frames(item).items():
							for response in responses:
								self.assertEqual(alpha(response["segments"]), response["interpreted_text"])
							if alpha_rows(responses) == rows:
								shown.append((item, label))
					self.assertTrue(shown)
					for item, _ in shown:
						if switch:
							self.assertIn(address, item["host_stimulus_switch_addresses"])
							self.assertEqual([], item["transitioned_solenoid_addresses"])
						else:
							self.assertIn(address, item["transitioned_solenoid_addresses"])
							self.assertIn(address, item["active_solenoid_addresses"])
					if not switch:
						self.assertEqual(1, observations["ordered_solenoid_on_sequence"].count(address))
				elif play:
					# Each listed step's observation, found by its label, reports the step's solenoid changes and relay.
					steps = {}
					for step, (changed, delta, raised) in play.items():
						(item,) = [obs for obs in observations["named_action_observations"] if obs["label"].startswith(f"{step}: ")]
						steps[step] = item
						self.assertEqual(changed, item["transitioned_solenoid_addresses"], step)
						self.assertEqual(raised, 19 in item["active_solenoid_addresses"], step)
						if delta:
							self.assertIn(f"rises by {delta:,} ", item["label"], step)
					self.assertTrue(any(item["input_address"] == address for item in steps.values()))
				elif bank:
					# Every closure keeps the relay raised, and the address's closure says the ROM did not tilt.
					closures = {item["input_address"]: item for item in observations["named_action_observations"] if item["input_kind"] == "switch"}
					for number in [*bank["members"], address]:
						self.assertIn("rises by", closures[number]["label"])
						if "points" in bank:
							self.assertIn(f"rises by {bank['points']:,}", closures[number]["label"])
						self.assertIn(bank["relay"], closures[number]["active_solenoid_addresses"])
					for number in bank["members"]:
						self.assertEqual([], closures[number]["transitioned_solenoid_addresses"])
					self.assertEqual([bank["reset"]] if "reset" in bank else [], closures[address]["transitioned_solenoid_addresses"])
					self.assertIn("does not tilt", closures[address]["label"])
				elif timeline:
					# Named actions report the address's changes; numeric and alphanumeric displays leave no frames.
					changes = [item for item in observations["named_action_observations"] if address in item["transitioned_solenoid_addresses"]]
					self.assertTrue(changes)
					self.assertNotIn("diagnostic_snapshots", observations)
				elif paired:
					partner, text = paired
					sequence = observations["ordered_solenoid_on_sequence"]
					self.assertIn(address, sequence)
					# Every rise of the address is immediately followed by its partner's, and the partner also runs alone.
					self.assertTrue(all(index + 1 < len(sequence) and sequence[index + 1] == partner for index, number in enumerate(sequence) if number == address))
					self.assertGreater(sequence.count(partner), sequence.count(address))
					frames = [item for item in observations["diagnostic_snapshots"] if item["interpreted_text"] == text]
					self.assertTrue(frames)
					frame = frames[0]
				elif switch:
					# A switch is named on the ROM's top line while the host holds it at 1.
					steps = [item for item in observations["named_action_observations"] if item["host_stimulus_switch_addresses"] == [address]]
					self.assertTrue(steps)
					self.assertTrue(all(not item["transitioned_solenoid_addresses"] for item in steps))
					frames = [item for item in observations["diagnostic_snapshots"] if f"after public {address} (" in item["label"] and "set to 1" in item["label"]]
				else:
					steps = [item for item in observations["named_action_observations"] if item["transitioned_solenoid_addresses"] == [address]]
					self.assertTrue(steps)
					frames = [item for item in observations["diagnostic_snapshots"] if item["label"].endswith(f" {address}")]
				if not paired and not timeline and not bank and not rows and not play:
					name = ROM_NAMES[(source["id"], address)]
					if switch:
						self.assertTrue(all(f"names it {name} " in item["label"] for item in steps))
					else:
						self.assertTrue(any(f"prints {name} " in item["label"] for item in steps))
					(frame,) = frames
					self.assertTrue(frame["interpreted_text"].startswith(f"{name} / "))
				root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
				if not root:
					continue
				import build_external_evidence_manifest as manifest

				game = runtime["game"]
				for item in runtime["raw_runs"]:
					retained = Path(root) / item["retained_from"][len("external:pinmame-review-artifacts/"):]
					self.assertEqual(item["sha256"], hashlib.sha256(retained.read_bytes()).hexdigest())
					digest = manifest.check_manifest(retained.parent, game)
					self.assertIn(f"{retained.parent.name}/manifest.json SHA-256 {digest}", evidence["source"]["attribution"])
					self.assertEqual(item["scenario_sha256"], load_json(retained)["scenario"]["sha256"])
				for item in setup:
					# The evidentiary run started from only the .nv file this run wrote, cited by its hash.
					written = Path(root) / item["retained_from"][len("external:pinmame-review-artifacts/"):]
					nv = written.parent / "state" / "nvram" / f"{game}.nv"
					self.assertIn(f"SHA-256 {hashlib.sha256(nv.read_bytes()).hexdigest()}", raw["nvram_initialization"])
				path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
				run = load_json(path)
				self.assertIsNone(run["failure"])
				self.assertEqual(PINNED_LIBRARY_SHA256, run["library_sha256"])
				# The summary and the raw run agree on driver, library and scenario.
				self.assertEqual(game, run["game"])
				self.assertEqual(runtime["emulator"]["sha256"], run["library_sha256"])
				self.assertEqual(raw["scenario_sha256"], run["scenario"]["sha256"])
				by_label = {snap["label"]: snap for snap in run["snapshots"]}
				raw_steps = {step["label"]: step for step in run["steps"]}
				for item in runtime["observations"].get("diagnostic_snapshots", []):
					matches = [snap for snap in run["snapshots"] if snap["displays"] and snap["displays"][0]["pixel_sha256"] == item["pixel_sha256"]]
					self.assertTrue(matches, item["label"])
				if rows:
					for item, label in shown:
						snap = by_label[label]
						for response in alpha_frames(item)[label]:
							(display,) = [entry for entry in snap["displays"] if entry["index"] == response["display_index"]]
							self.assertEqual(display["segments"], response["segments"])
						if switch:
							# Only the address is held when the frame is taken; the Test switch was a pulse.
							held = {entry["number"] for entry in snap["watched_switches"] if entry["state"]}
							self.assertEqual({address}, held)
							self.assertEqual([], raw_steps[label]["transitions"]["solenoids"])
						else:
							self.assertIn(address, snap["active_solenoids"])
					if not switch:
						# After boot the address rises once, in the service test, and drops again.
						boot = by_label["boot"]["time_s"]
						states = [event["state"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == address and event["time_s"] > boot]
						self.assertEqual([1, 0], states)
				elif play:
					labels = list(raw_steps)
					for step, (changed, delta, raised) in play.items():
						self.assertEqual(changed, sorted({item["number"] for item in raw_steps[step]["transitions"]["solenoids"]}), step)
						self.assertEqual(raised, 19 in by_label[step]["active_solenoids"], step)
						if delta is not None:
							before = by_label[labels[labels.index(step) - 1]]
							gained = seven_segment(by_label[step]["displays"][0]["segments"]) - seven_segment(before["displays"][0]["segments"])
							self.assertEqual(delta, gained, step)
				elif bank:
					def score(label: str) -> int:
						return seven_segment(by_label[label]["displays"][0]["segments"])

					def lit(label: str) -> set[int]:
						return {item["number"] for item in raw_steps[label]["transitions"]["lamps"] if item["states"][-1]}

					labels = [*bank["members"].values(), bank["step"]]
					positions = [list(raw_steps).index(label) for label in labels]
					self.assertEqual(sorted(positions), positions)
					previous = score(list(raw_steps)[positions[0] - 1])
					for label in labels:
						self.assertGreater(score(label), previous, label)
						if "points" in bank:
							self.assertEqual(bank["points"], score(label) - previous, label)
						previous = score(label)
						self.assertIn(bank["relay"], by_label[label]["active_solenoids"])
					for label in bank["members"].values():
						self.assertEqual([], raw_steps[label]["transitions"]["solenoids"], label)
					fired = raw_steps[bank["step"]]["transitions"]["solenoids"]
					if "reset" in bank:
						# Only the address's closure completes the bank, so only it fires the reset.
						self.assertEqual([bank["reset"]], [item["number"] for item in fired if 1 in item["states"]])
					else:
						self.assertEqual([], fired)
					if bank.get("award"):
						# The address's closure lights lamps that no member's closure lit.
						award = lit(bank["step"])
						self.assertTrue(award)
						for label in bank["members"].values():
							self.assertFalse(award & lit(label), label)
					# The relay stays raised from the start of play until the ball drains.
					rises = [event["time_s"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == bank["relay"] and event["state"]]
					drops = [event["time_s"] for event in run["events"] if event["event"] == "solenoid" and event["number"] == bank["relay"] and not event["state"]]
					start, end = by_label[labels[0]]["time_s"], by_label[bank["step"]]["time_s"]
					self.assertTrue(any(time < start for time in rises))
					self.assertFalse(any(start - 3 <= time <= end for time in drops))
				elif timeline:
					self.assertEqual([], timeline_mismatches(run, address, timeline))
				elif paired:
					rises = [event for event in run["events"] if event["event"] == "solenoid" and event["state"]]
					self.assertEqual(observations["ordered_solenoid_on_sequence"], [event["number"] for event in rises][-len(observations["ordered_solenoid_on_sequence"]):])
					times = {number: [event["time_s"] for event in rises if event["number"] == number] for number in (address, partner)}
					self.assertTrue(times[address])
					self.assertTrue(set(times[address]) <= set(times[partner]))
					self.assertTrue(set(times[partner]) - set(times[address]))
					# The step frame is the snapshot taken right after a step in which the address rose.
					steps = run["steps"]
					after = [
						steps[index + 1]["label"] for index in range(len(steps) - 1)
						if any(t["number"] == address and any(t["states"]) for t in steps[index]["transitions"]["solenoids"])
					]
					self.assertTrue(any(by_label[label]["displays"][0]["pixel_sha256"] == frame["pixel_sha256"] for label in after))
				elif switch:
					# The frame that names the switch is the one taken while only it was held at 1.
					held = by_label[f"{address} -> 1"]
					self.assertEqual(frame["pixel_sha256"], held["displays"][0]["pixel_sha256"])
					self.assertEqual(1, raw_steps[f"{address} -> 1"]["observed_state"])
					self.assertEqual({address}, {item["number"] for item in held["watched_switches"] if item["state"] and item["number"] in run["watch_switches"]})
					self.assertEqual([], raw_steps[f"{address} -> 1"]["transitions"]["solenoids"])
				else:
					# The frame that names the address was taken after the press that selected it and before the next
					# press: repeat mode blinks the name, so it may come from a later frame than the selecting step's.
					steps = run["steps"]
					presses = [index for index, step in enumerate(steps) if step["type"] == "pulse"]
					windows = []
					for index in presses:
						if {t["number"] for t in steps[index]["transitions"]["solenoids"] if any(t["states"])} == {address}:
							following = [later for later in presses if later > index]
							windows.append(range(index, following[0] if following else len(steps)))
					self.assertTrue(windows)
					self.assertTrue(any(
						by_label[steps[position]["label"]]["displays"][0]["pixel_sha256"] == frame["pixel_sha256"]
						for window in windows for position in window
					))

	def test_the_tool_refuses_the_wrong_device_and_inconsistent_coverage(self) -> None:
		settlement = tool.SETTLEMENTS[0]
		settled = load_json(ROOT / settlement["path"])
		binding = settlement["binding"]

		# Swapping the settled device with its neighbour's binding puts another device at the address.
		swapped = json.loads(json.dumps(settled))
		(target,) = [item for item in swapped["outputs"] if item["binding"] == binding]
		(neighbour,) = [item for item in swapped["outputs"] if item["binding"] == {**binding, "device": binding["device"] - 1}]
		target["binding"], neighbour["binding"] = neighbour["binding"], target["binding"]
		with self.assertRaisesRegex(RuntimeError, "expected"):
			tool.settle(swapped, settlement)

		# A device that kept the settled id but whose public-number alias names another address.
		aliased = json.loads(json.dumps(settled))
		(target,) = [item for item in aliased["outputs"] if item["binding"] == binding]
		target["aliases"] = [{**alias, "value": "18"} if alias["namespace"] == "pinmame.coil" else alias for alias in target["aliases"]]
		with self.assertRaisesRegex(RuntimeError, "aliases"):
			tool.settle(aliased, settlement)

		# An unsettled record whose device is no longer the one import-legacy wrote.
		renamed = json.loads(json.dumps(settled))
		renamed["conflicts"].append({"id": settlement["conflict_id"], "path": f"binding:{binding['group']}/{binding['device']}/None", "description": "x", "source_refs": []})
		renamed["coverage"]["missing"].append("unresolved_conflicts")
		with self.assertRaisesRegex(RuntimeError, "expected"):
			tool.settle(renamed, settlement)

		# A conflict recorded on another binding is not this settlement's.
		misplaced = json.loads(json.dumps(renamed))
		misplaced["conflicts"][-1]["path"] = f"binding:{binding['group']}/18/None"
		with self.assertRaisesRegex(RuntimeError, "is not on"):
			tool.settle(misplaced, settlement)

		# An unresolved conflict remaining while coverage.missing omits it.
		inconsistent = json.loads(json.dumps(settled))
		inconsistent["conflicts"].append({"id": "conflict.other", "path": "binding:pinmame.output.solenoid/18/None", "description": "x", "source_refs": []})
		with self.assertRaisesRegex(RuntimeError, "omits unresolved_conflicts"):
			tool.settle(inconsistent, settlement)

	def test_the_timeline_check_rejects_a_reversed_transition(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
		for (source_id, address), timeline in TIMELINES.items():
			with self.subTest(source=source_id):
				settlement = next(item for item in tool.SETTLEMENTS if item["source"]["id"] == source_id)
				evidence = load_json(ROOT / settlement["source"]["uri"][len("internal:"):])
				raw = evidence["runtime"]["raw_runs"][-1]
				run = load_json(Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):])
				self.assertEqual([], timeline_mismatches(run, address, timeline))
				# The checkpoints accept either direction, so the check must catch a rise where a drop belongs.
				label, listed = timeline[-1]
				reversed_step = json.loads(json.dumps(run))
				for step in reversed_step["steps"]:
					if step["label"] == label:
						for item in step["transitions"]["solenoids"]:
							if item["number"] == address:
								item["states"] = [1 - state for state in listed]
				self.assertTrue(timeline_mismatches(reversed_step, address, timeline))
				reversed_event = json.loads(json.dumps(run))
				(last,) = [event for event in reversed_event["events"] if event["event"] == "solenoid" and event["number"] == address][-1:]
				last["state"] = 1 - last["state"]
				self.assertTrue(timeline_mismatches(reversed_event, address, timeline))

	def test_the_tool_check_mode_passes(self) -> None:
		import subprocess

		result = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "settle_legacy_label_conflicts.py"), "--check"], capture_output=True, text=True, cwd=ROOT)
		self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
	unittest.main()
