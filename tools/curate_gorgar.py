"""Build Gorgar from the checked factory excerpts and pinned local evidence."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from build_external_evidence_manifest import check_manifest, sha256_file
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.spatial import _round_point

ROOT = Path(__file__).resolve().parents[1]
MACHINE = "williams.gorgar.1979"
SLUG = "gorgar-1979"
SEED = Path(f"tools/seeds/williams/{SLUG}.json")
DEFINITION = Path(f"machines/partial/williams/{SLUG}.json")
KNOWLEDGE = Path(f"knowledge/williams/{SLUG}.md")
REPORT = Path(f"reports/spatial/williams/{SLUG}.json")
EXCERPTS = Path(f"evidence/excerpts/{MACHINE}")
RUNTIME = Path(f"evidence/runtime/{MACHINE}/gameplay.json")
BOOK, WIRING, BULLETIN, ROM, CORE, TABLE, SCRIPT, RUN, RETRO_TABLE, RETRO_SCRIPT = (
	"manual.gorgar-booklet", "manual.gorgar-schematics", "bulletin.gorgar-ss20",
	"pinmame.gorgar-drivers", "pinmame.system-6", "vpx.gorgar-table", "vpx.gorgar-script",
	"runtime.gorgar-l1", "vpx.gorgar-retro-table", "vpx.gorgar-retro-script",
)
SWITCH, LAMP, SOLENOID, DIP = (
	"pinmame.input.switch", "pinmame.output.lamp", "pinmame.output.solenoid", "pinmame.input.dip",
)
BOARD = "Williams System 6 driver board"
STANDUPS = {13, 16, 17, 22, 24, 25, 40}
SPECIAL = {17: 38, 18: 37, 19: 39, 20: 12, 21: 36}
BACKBOX_LAMPS = {*range(50, 56), *range(57, 65)}
TWO_BACKBOX_BULBS = {62, 63, 64}


def slug(label):
	return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def provenance(*refs, status="validated"):
	return {"source_refs": list(dict.fromkeys(refs)), "status": status}


def not_applicable(reason, *refs):
	return {"reason": reason, "status": "not_applicable", "provenance": provenance(*refs)}


def device(identifier, label, kind, group, address, *refs, availability="used"):
	namespace = group.replace(".input", "").replace(".output", "")
	values = [str(address)]
	if group == SWITCH and address > 0:
		values = list(dict.fromkeys([str(address), f"{address:02}", f"{address:03}"]))
	return {"id": identifier, "label": label, "kind": kind,
		"binding": {"group": group, "device": address}, "availability": availability,
		"aliases": [{"namespace": namespace, "value": value} for value in values],
		"provenance": provenance(*refs)}


def rows(root, name, columns):
	for line in (root / EXCERPTS / name).read_text(encoding="utf-8").splitlines():
		if line.startswith("|"):
			fields = line.strip("|").split("|")
			if len(fields) == columns:
				yield tuple(cell.strip() for cell in fields)


def matrix(root, name, numbered):
	labels = {}
	for row, *cells in rows(root, name, 9):
		if not row[0].isdigit():
			continue
		for col, cell in enumerate(cells):
			address = 8 * col + int(row[0])
			if numbered:
				printed, cell = cell.split(" ", 1)
				if int(printed) != address:
					raise ValueError(f"{name}: expected printed address {address}, found {printed}")
			labels[address] = cell
	if sorted(labels) != list(range(1, 65)):
		raise ValueError(f"{name}: incomplete matrix")
	return labels


def matrix_wiring(address, lamp=False):
	col, row = divmod(address - 1, 8)
	if lamp:
		drive = (8, 9, 6, 7, 3, 5, 1)
		pin = "9J1-7" if col == 7 else f"2J5-{drive[col]}"
		drive_wires = ("BRN", "RED", "ORN", "BLK", "GRN", "BLU", "VIO", "GRY")
		return_wires = ("BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY")
		return {"board": BOARD, "drive_wire": f"YEL-{drive_wires[col]}", "drive_connection": pin,
			"return_wire": f"RED-{return_wires[row]}", "return_connection": f"2J7-{(1, 2, 3, 4, 5, 6, 9, 8)[row]}"}
	wires = ("BRN", "RED", "ORN", "YEL", "BLK", "BLU", "VIO", "GRY")
	return_wires = ("BRN", "RED", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY")
	return {"board": BOARD, "drive_wire": f"GRN-{wires[col]}", "drive_connection": f"2J2-{(9, 8, 7, 6, 5, 3, 2, 1)[col]}",
		"return_wire": f"WHT-{return_wires[row]}", "return_connection": f"2J3-{(9, 8, 7, 6, 5, 4, 3, 1)[row]}"}


def switches(root):
	service = ("Advance", "Auto-Up / Manual-Down", "CPU Diagnostic", "Sound Diagnostic", "Master Command Enter")
	for address, label in enumerate(service, -7):
		d = device(f"switch.{slug(label)}", label, "switch", SWITCH, address, BOOK, CORE)
		d["spatial"] = not_applicable("cabinet_or_service", BOOK, CORE)
		d["physical"] = {"location": "coin door" if address <= -6 else "backbox"}
		if address == -6:
			d["physical"]["notes"] = "Two-position service selector. Public 1 is Auto-Up."
		else:
			d["normally_closed"] = False
		yield d

	for address, printed in sorted(matrix(root, "switch-matrix.md", True).items()):
		used = printed != "NOT USED"
		label = printed.replace('"', "").title() if used else f"Unused matrix switch {address}"
		if address in {18, 19, 20}:
			label = "G-O-R " + label
		elif address in {41, 42, 43}:
			label = "G-A-R " + label
		d = device(f"switch.{slug(label)}", label, "switch", SWITCH, address, BOOK, WIRING, CORE,
			availability="used" if used else "unused")
		d["wiring"] = matrix_wiring(address)
		d["aliases"].append({"namespace": "manual.address", "value": f"{address:02}"})
		if used:
			d["normally_closed"] = False
			d["physical"] = {"location": "cabinet" if address <= 8 else "playfield"}
			if address <= 8:
				d["spatial"] = not_applicable("cabinet_or_service", WIRING)
			if address in (1, 2, 7, 29):
				d["physical"]["switch_type"] = "tilt"
			if address in (21, 44):
				d["physical"]["notes"] = "Bank all-down series input for the three drop targets."
			if address == 23:
				d["physical"].update(switch_type="leaf", notes="SS20 specifies contact gap and followthrough for this magnet switch.")
				d["provenance"] = provenance(BOOK, WIRING, BULLETIN, CORE)
		else:
			d["spatial"] = not_applicable("unused", BOOK, WIRING)
		yield d

	for address in range(81, 89):
		side = {82: "right", 84: "left"}.get(address)
		label = f"{side.title()} Flipper Button" if side else f"Unused flipper-column position {address}"
		d = device(f"switch.{slug(label)}", label, "virtual", SWITCH, address, CORE, ROM,
			availability="used" if side else "unused")
		d["spatial"] = not_applicable("virtual", CORE, ROM)
		if side:
			d["roles"] = [f"flipper.lower.{side}.button"]
			d["physical"] = {"location": "cabinet", "notes": "Host button state for synthesized flipper outputs. Gorgar declares no matrix copy for this button."}
		yield d


def dips():
	commands = {17: "Zero Audit Totals", 18: "Restore Factory Settings", 19: "Auto-Cycle Mode"}
	sound = {1: "Speech Enable (DS1 switch 2)", 2: "Sound Select (DS1 switch 1)"}
	for address in [1, 2, *range(9, 25)]:
		label = sound.get(address) or commands.get(address)
		active = label is not None
		label = label or (f"CPU Lower Bank F{address - 8}" if address <= 16 else f"Master Command D{address - 16}")
		d = device(f"dip.{slug(label)}", label, "dip_switch", DIP, address, BOOK, CORE,
			availability="used" if active else "unused")
		d["spatial"] = not_applicable("dip_switch", BOOK, CORE)
		d["physical"] = {"location": "backbox", "switch_type": "dip"}
		if address in sound:
			d["physical"]["notes"] = "Public 0 enables speech." if address == 1 else "Public 0 selects musical notes. Public 1 selects synthesized sounds."
		if address in commands:
			d["physical"]["notes"] = f"Master Command position {25 - address}; sampled while Master Command Enter is held."
		yield d


def lamps(root):
	for address, printed in sorted(matrix(root, "lamp-matrix.md", False).items()):
		used = printed != "NOT USED"
		label = printed.replace('"', "").title() if used else f"Unused lamp {address}"
		if address == 47:
			label = "Unfitted lamp 47"
		label = re.sub(r"\b(Gor|Gar)\b", lambda match: match.group().upper(), label)
		d = device(f"lamp.{slug(label)}", label, "lamp", LAMP, address, BOOK, WIRING, CORE,
			availability="used" if used else "unused")
		d["wiring"] = matrix_wiring(address, lamp=True)
		if used:
			backbox = address in BACKBOX_LAMPS
			d["physical"] = {"location": "backbox insert board" if backbox else "playfield",
				"quantity": 2 if address in TWO_BACKBOX_BULBS else 1}
			if backbox:
				d["spatial"] = not_applicable("cabinet_or_service", WIRING)
				d["physical"]["notes"] = f"Insert board column at 9J1-{6 if address <= 55 else 7}; return at 9J1-{(address - 1) % 8 + 8}."
		else:
			d["spatial"] = not_applicable("unused", BOOK, WIRING)
			if address == 47:
				d["availability"] = "unknown"
				d["physical"] = {"notes": "Figure 6 and the wiring sheet leave this matrix position unfitted. The L-1 ROM asserted it for 78 ms shortly after G-A-R all-down switch 44 closed in gameplay. Its firmware purpose is unresolved."}
				d["provenance"] = provenance(BOOK, WIRING, CORE, RUN, status="observed")
		yield d


def solenoids(root):
	labels = {5: "Magnet Relay", 6: "Snake Pit Flash Lamps"}
	for addr, printed, wire, connections, transistor, part in rows(root, "solenoid-connections.md", 6):
		if not addr.strip("*").isdigit():
			continue
		address = int(addr.strip("*"))
		used = printed != "Not Used"
		kind = {5: "relay", 6: "flasher"}.get(address, "coil")
		if 9 <= address <= 13:
			kind, label = "control_signal", f"Sound Command Line {address - 8}"
		else:
			label = labels.get(address, printed.replace('"', "")) if used else f"Unused solenoid {address}"
		d = device(f"{kind}.{slug(label)}", label, kind, SOLENOID, address, BOOK, WIRING, CORE,
			availability="used" if used else "unused")
		d["wiring"] = {"board": BOARD, "drive_wire": wire, "drive_connection": connections, "driver_transistor": transistor}
		d["aliases"].append({"namespace": "manual.address", "value": f"{address:02}"})
		if address in SPECIAL:
			d["physical"] = {"notes": f"Separate physical direct-drive contact 8SW{address + 48}; PinMAME derives this output from scoring switch {SPECIAL[address]} while game-on is enabled."}
		if part != "--":
			d.setdefault("physical", {})["part_number"] = "89" if address == 6 else part
		if address == 5:
			d["physical"]["notes"] = "Relay 8L5 closes the ground path of the separate 20-8991 magnet (8L27)."
		if address == 6:
			d["physical"].update(quantity=2, notes="Schematic shows two type 89 bulbs, 8B65 and 8B66.")
		if not used:
			d["spatial"] = not_applicable("unused", BOOK, WIRING)
		elif kind == "control_signal":
			d["spatial"] = not_applicable("internal_nonvisual", WIRING, CORE)
		elif address in {14, 16}:
			d["spatial"] = not_applicable("cabinet_or_service", WIRING)
		else:
			d.setdefault("physical", {})["location"] = "playfield"
		yield d

	d = device("relay.game-on", "Game-On / Flipper Enable", "relay", SOLENOID, 23, WIRING, CORE)
	d["spatial"] = not_applicable("cabinet_or_service", WIRING, CORE)
	d["physical"] = {"location": "backbox driver board", "notes": "Z1 enables the flipper return and game-on also gates the special solenoids."}
	yield d
	for address in range(45, 49):
		side = "right" if address <= 46 else "left"
		label = f"{side.title()} Flipper {'Power' if address % 2 else 'Hold'} (Synthetic)"
		d = device(f"virtual.{slug(label)}", label, "virtual", SOLENOID, address, CORE, ROM, RUN)
		d["spatial"] = not_applicable("virtual", CORE)
		d["physical"] = {"notes": "The power/hold pair follows the single button state while game-on is set. The synthetic states do not model winding or EOS timing."}
		yield d


def displays():
	for index, (name, start, width) in enumerate([
		("Player 1 Score", 0, 6), ("Player 2 Score", 8, 6), ("Player 3 Score", 20, 6),
		("Player 4 Score", 28, 6), ("Credits", 14, 2), ("Ball in Play / Match", 6, 2),
	]):
		yield {"id": f"display.{slug(name)}", "label": name, "kind": "segment", "controller_index": index,
			"segment_start": start, "width": width, "physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE, WIRING), "provenance": provenance(CORE, WIRING)}


def mechanisms(ids):
	def mids(group, addresses):
		return [ids[group, address] for address in addresses]

	specs = [
		("Outhole and Ball Release", "kicker", (1,), (9,), "The drained ball closes 9. Release 1 feeds it to the manual shooter lane. Start and drain both reset the drop banks before the serve."),
		("Eject Hole", "kicker", (2,), (15,), "The left saucer holds the ball on switch 15, awards the selected value or extra ball and ejects on 2."),
		("G-O-R Drop Bank", "drop_target_bank", (4,), (18, 19, 20, 21), "Each dropped target stays down. All three down closes the series circuit at 21, and coil 4 resets the bank. Completing the bank advances the magnet award."),
		("G-A-R Drop Bank", "drop_target_bank", (3,), (41, 42, 43, 44), "The three dropped targets close 41–43 and the all-down series circuit at 44. Coil 3 lifts all three together. The bank advances the jets and the GAR award."),
		("Snake Pit", "other", (5, 6), (23,), "The pit leaf triggers relay 5, which grounds the separate magnet. Output 6 flashes the two type 89 bulbs on its own timing. When 5 opens the magnet releases the ball back to the playfield."),
		("Right Flipper", "other", (45, 46), (82,), "Cabinet button and flipper relay Z1 gate the dual-wound SFL-20-300 30-800-DC assembly, with a physical EOS contact. PinMAME presents a synthetic output pair."),
		("Left Flipper", "other", (47, 48), (84,), "Cabinet button and flipper relay Z1 gate the dual-wound SFL-20-300 30-800-DC assembly, with a physical EOS contact. PinMAME presents a synthetic output pair."),
	]
	for output, sensor in SPECIAL.items():
		label = {17: "Top Jet Bumper", 18: "Left Jet Bumper", 19: "Bottom Jet Bumper", 20: "Left Kicker", 21: "Right Kicker"}[output]
		specs.append((label, "other", (output,), (sensor,), "A separate normally open special switch triggers the drive with game-on enabled. The matrix scoring switch reports the hit; PinMAME uses it to synthesize the same drive."))
	for label, kind, actuators, sensors, behavior in specs:
		yield {"id": f"mech.{slug(label)}", "label": label, "kind": kind, "actuators": mids(SOLENOID, actuators),
			"sensors": mids(SWITCH, sensors), "behavior": behavior, "provenance": provenance(BOOK, WIRING, SCRIPT, RUN)}


def raw_point(spec, objects):
	points = []
	for name in spec["objects"]:
		item = objects[name]
		if spec["method"] == "active_edge_midpoint":
			drag = item["drag_points"]
			[(i, p)] = [(i, p) for i, p in enumerate(drag) if p["is_slingshot"]]
			points.extend((p, drag[(i + 1) % len(drag)]))
		elif "drag_points" in item:
			points.extend(item["drag_points"])
		else:
			points.append(item["point"])
	return [sum(p[axis] for p in points) / len(points) for axis in ("x", "y")]


def spatial(devices, seed):
	bounds = seed["table"]["bounds"]
	placed = []
	for spec in seed["placements"]:
		group, address = spec["group"], spec["address"]
		d = devices[group, address]
		if "spatial" in d:
			raise ValueError(f"duplicate placement or non-playfield device: {d['id']}")
		raw = raw_point(spec, seed["objects"])
		x = _round_point((raw[0] - bounds["left"]) / (bounds["right"] - bounds["left"]))
		y = _round_point((raw[1] - bounds["top"]) / (bounds["bottom"] - bounds["top"]))
		if not (0 <= x <= 1 and 0 <= y <= 1):
			raise ValueError(f"out-of-range placement for {d['id']}: {raw}")
		table_ref, script_ref = (RETRO_TABLE, RETRO_SCRIPT) if spec["table"] == "retro" else (TABLE, SCRIPT)
		ref = provenance(table_ref, script_ref, BOOK, status="observed")
		placement_id = f"placement.{group.rsplit('.', 1)[-1]}-{address}"
		d["spatial"] = {"status": "observed", "placements": [{"id": placement_id,
			"role": "sensor" if group == SWITCH else "effect", "space": "playfield",
			"x": x, "y": y, "provenance": ref}]}
		placed.append({**spec, "device_id": d["id"], "placement_id": placement_id, "status": "observed",
			"raw_point": raw, "x": x, "y": y})
	return placed


def build(root, seed):
	sources = seed["sources"]
	for source in sources:
		for excerpt in source.get("excerpts", ()):
			if sha256_file(root / excerpt["path"]) != excerpt["sha256"]:
				raise ValueError(f"excerpt changed: {excerpt['path']}")
	if sha256_file(root / RUNTIME) != next(s["sha256"] for s in sources if s["id"] == RUN):
		raise ValueError("runtime evidence changed")
	inputs = [*switches(root), *dips()]
	outputs = [*lamps(root), *solenoids(root)]
	display_list = list(displays())
	devices = {(d["binding"]["group"], d["binding"]["device"]): d for d in inputs + outputs}
	if len(devices) != len(inputs) + len(outputs):
		raise ValueError("duplicate binding")
	placed = spatial(devices, seed)
	ids = {key: d["id"] for key, d in devices.items()}
	relationships = [
		{"id": f"relationship.special-{sensor}-{drive}", "kind": "direct", "source": ids[SWITCH, sensor],
			"destination": ids[SOLENOID, drive], "provenance": provenance(CORE, ROM, RUN)}
		for drive, sensor in SPECIAL.items()
	]
	return {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE, "name": "Gorgar", "manufacturer": "Williams", "year": 1979,
			"model_number": "496", "kind": "physical_pinball", "ipdb_id": 1062, "opdb_id": "G5zd6-MJVo4",
			"playfield": {"width": 952, "height": 1974, "units": "vpx", "provenance": provenance(TABLE, status="observed")}},
		"controller": {"platform": "pinmame.system-6", "hardware_generation": "0x20000", "inversion_applied_by_emulator": True},
		"drivers": seed["drivers"], "inputs": inputs, "outputs": outputs, "displays": display_list,
		"mechanisms": list(mechanisms(ids)), "relationships": relationships, "sources": sources, "conflicts": [],
		"coverage": {"status": "partial", "missing": ["output_semantics", "spatial_placement", "variant_differences"],
			"dimensions": {"catalog_identity": "validated", "address_enumeration": "validated",
				"semantic_naming": "observed", "physical_wiring": "observed", "mechanisms": "observed",
				"variant_coverage": "observed", "recreation_knowledge": "observed", "spatial_placement": "observed"}},
		"knowledge": {"path": KNOWLEDGE.as_posix(), "status": "partial"},
	}, placed


def report(definition, placed, seed):
	not_located = [d for section in ("inputs", "outputs", "displays") for d in definition[section] if "spatial" not in d]
	reasons = {d["id"]: seed["unplaced"][f"{d['binding']['group']}:{d['binding']['device']}"] for d in not_located}
	counts = Counter(item["group"].rsplit(".", 1)[-1] for item in placed)
	return {"format": "pinmame-spatial-blockers", "version": 2, "machine_id": MACHINE, "decision": "partial",
		"table_geometry": seed["table"], "extraction_manifest": seed["table"]["manifest"],
		"retro_table_geometry": seed["retro_table"], "retro_lamp_candidates": seed["retro_lamp_candidates"],
		"gi_modelled_bulbs": seed["gi_modelled_bulbs"],
		"coordinate_convention": "x 0 left to 1 right and y 0 rear to 1 apron; VPX bounds normalized to six decimal places.",
		"counts": dict(counts), "placements": placed, "unplaced_devices": sorted(reasons), "unplaced_reasons": reasons,
		"not_applicable": {d["id"]: d["spatial"]["reason"] for section in ("inputs", "outputs", "displays")
			for d in definition[section] if d.get("spatial", {}).get("status") == "not_applicable"},
		"blockers": seed["blockers"]}


def verify_external(seed, vpx_root=None, manuals_root=None, review_root=None):
	from pinmame_game_defs.jsonio import file_sha256

	for base, name in ((vpx_root, "vpx"), (manuals_root, "manuals"), (review_root, "review")):
		if base is None:
			continue
		for path, expected in seed["external"][name].items():
			if file_sha256(base / path) != expected:
				raise ValueError(f"retained {name} evidence changed: {path}")
	if vpx_root is not None:
		extractions = {}
		for key, table in (("archive", seed["table"]), ("retro", seed["retro_table"])):
			extract = vpx_root / table["extraction"]
			if check_manifest(extract, "grgar_l1") != table["manifest"]["sha256"]:
				raise ValueError(f"VPX extraction manifest changed: {key}")
			actual = load_json(extract / "gamedata.json")
			if any(actual[axis] != value for axis, value in table["bounds"].items()):
				raise ValueError(f"VPX bounds changed: {key}")
			extractions[key] = extract
		table_by_item = {name: row["table"] for row in seed["placements"] for name in row["objects"]}
		for name, expected in seed["objects"].items():
			kind = name.split(".", 1)[0]
			extract = extractions[table_by_item[name]]
			item = load_json(extract / "gameitems" / name)[kind]
			if "drag_points" in expected:
				actual = {"drag_points": [{key: p[key] for key in ("x", "y", "is_slingshot")} for p in item["drag_points"]]}
			else:
				point = item["center"] if "center" in item else item["position"]
				actual = {"point": {key: point[key] for key in ("x", "y")}}
			if actual != expected:
				raise ValueError(f"VPX seed object disagrees with the extraction: {name}")
	if review_root is not None:
		runtime = load_json(ROOT / RUNTIME)
		manifest = runtime["source"]
		retained = review_root / Path(manifest["path"].split("/", 1)[1]).parent
		if check_manifest(retained, "grgar_l1") != manifest["sha256"]:
			raise ValueError("Gorgar runtime manifest changed")


def artifacts(root):
	seed = load_json(root / SEED)
	definition, placed = build(root, seed)
	audit = report(definition, placed, seed)
	summary = (
		"# Gorgar spatial audit\n\n"
		f"The retained VPX supplies {audit['counts']['switch']} switch and {audit['counts']['solenoid']} solenoid effect placements. "
		"Solenoid placements project to the intended gameplay effect. Switch placements distinguish direct geometry from projections. "
		"See the JSON for raw coordinates, methods and unresolved addresses.\n\n"
		+ "".join(f"- {blocker}\n" for blocker in audit["blockers"])
	)
	return {DEFINITION: canonical_bytes(definition), REPORT: canonical_bytes(audit),
		REPORT.with_suffix(".md"): summary.encode("utf-8"), KNOWLEDGE: seed["knowledge"].encode("utf-8")}


def curate(root=ROOT, *, check=False):
	if (root / "machines/author-ready/williams" / DEFINITION.name).exists():
		raise ValueError("refusing to overwrite an author-ready Gorgar")
	for relative, content in artifacts(root).items():
		path = root / relative
		if check:
			if not path.is_file() or path.read_bytes() != content:
				raise ValueError(f"Gorgar generated artifact is missing or stale: {relative}")
		else:
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_bytes(content)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true")
	parser.add_argument("--vpx-root", type=Path)
	parser.add_argument("--manuals-root", type=Path)
	parser.add_argument("--review-root", type=Path)
	args = parser.parse_args()
	verify_external(load_json(ROOT / SEED), args.vpx_root, args.manuals_root, args.review_root)
	curate(check=args.check)
