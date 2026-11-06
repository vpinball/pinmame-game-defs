"""Reviewed Radical geometry and drawing measurements; every placement stays observed."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]
SEED = Path("tools/seeds/bally/radical-1990-spatial.json")
DRAWING_SOURCE = "manual.radical.lamp-location"
SOLENOID_DRAWING_SOURCE = "manual.radical.solenoid-location"
SWITCH_DRAWING_SOURCE = "manual.radical.switch-location"
TABLE_SOURCE = "vpx-table.radical.spatial"
EXTRACTION_SOURCE = "vpx-extraction.radical.spatial"
VPW_TABLE_SOURCE = "vpx-table.radical.vpw"
VPW_SCRIPT_SOURCE = "vpx-script.radical.vpw-retained"
DRAWING_EXCERPT = "evidence/excerpts/bally.radical.1990/lamp-location-measurements.md"


def provenance(*refs: str, status: str = "observed") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def _placement(device: dict[str, Any], points: list[dict[str, Any]], role: str, refs: list[str]) -> None:
	device["spatial"] = {
		"status": "observed",
		"placements": [
			{"id": f"{device['id']}.placement-{index}", "role": role, "space": "playfield",
			 "x": point["x"], "y": point["y"], "provenance": provenance(*refs)}
			for index, point in enumerate(points, 1)
		],
	}


def _note(device: dict[str, Any], text: str) -> None:
	physical = device.setdefault("physical", {})
	physical["notes"] = (physical.get("notes", "") + " " + text).strip()


def apply_spatial(definition: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
	seed = load_json(root / SEED)
	prototype = definition["machine"]["id"] == "bally.radical-prototype.1990"
	manual_refs = [source["id"] for source in definition["sources"] if source["kind"] == "manual"]
	refs = [TABLE_SOURCE, EXTRACTION_SOURCE, *manual_refs[:1]]
	for device in definition["inputs"]:
		if device["binding"]["group"] != "pinmame.input.switch":
			continue
		address = device["binding"]["device"]
		point = seed["inputs"].get(str(address))
		if address == 16 and not prototype:
			point = seed["production_switch_16"]
		if address == 20:
			point = seed["bowtie_sensor_projection"]
		if address == 27:
			point = seed["switch_drawing"]["switch27"]
		vpw_point = prototype and address in (16, 49)
		if vpw_point:
			point = seed["vpw"]["prototype_sensor16" if address == 16 else "prototype_sling49"]
		if point and device.get("availability") not in ("unused", "unknown"):
			placement_refs = [SWITCH_DRAWING_SOURCE, TABLE_SOURCE, *manual_refs[:1]] if address == 27 else [VPW_TABLE_SOURCE, VPW_SCRIPT_SOURCE, *manual_refs[:1]] if vpw_point else refs
			_placement(device, [point], "sensor", placement_refs)
			if address == 27:
				_note(device, "Observed factory-actuator projection onto the midpoint of the distinct horizontal blade immediately below27 on PDF82, separate from the diagonal top sling beside49. A page-specific six-control fit is used. The point is outside its control convex hull and explicitly extrapolated; it is not the text center or a surveyed microswitch body. The function remains Middle Man; no ramp-entry behavior is inferred from the appearance.")
			elif vpw_point:
				if address == 16:
					_note(device, "Observed sensor projection onto the VPW popper entry kicker sw16a (ball stack 16). The output kicker sw16 at the far rear-left is a distinct return location, not the sensor center. No physical switch-body survey is claimed.")
				else:
					_note(device, "Observed scoring-contact projection onto the VPW top sling's RightSlingshot1 rubber-wall vertex mean (pulse 49), not a measured leaf-contact position. The DisableUpperSling option suppresses this sling's hit response by default.")
			elif address == 20:
				_note(device, "Observed projection of the bowtie microswitch onto the vertex mean of its own DiverterDown wall. The table toggles this physical feedback with coil 7; this is not a measured sensor center.")
			elif address in (39, 40):
				_note(device, f"Observed ball-lock sensor projection onto its own script-bound kicker {point['name']}; no separate microswitch mesh is present.")
			elif address in (55, 56):
				_note(device, f"Observed scoring-contact projection onto the shared spatial helper's vertex mean of the {point['name']} rubber wall; not a measured leaf-contact position.")
			else:
				_note(device, f"Observed retained-table object {point['name']} ({point['type']}); its source coordinate is normalized against 0,0,952,1974. Physical location has not been independently surveyed.")
	for device in definition["outputs"]:
		group, address = device["binding"]["group"], device["binding"]["device"]
		if group == "pinmame.output.lamp" and str(address) in seed["drawing"]["lamps"]:
			_placement(device, [seed["drawing"]["lamps"][str(address)]], "emitter", [DRAWING_SOURCE, TABLE_SOURCE, *manual_refs[:1]])
			_note(device, "Observed projection of the bulb onto the center of its numbered insert on the game's own lamp-location drawing, reconciled with six retained-table mechanism controls. The drawing shows the illuminated insert, not a measured socket below it. Measured positions are rounded to 0.001; no physical socket survey or validation is claimed.")
		elif group == "pinmame.output.solenoid" and address == 10:
			_placement(device, seed["gi_bulbs"], "emitter", refs)
			_note(device, f"The retained aGiLights collection contains {len(seed['gi_bulbs'])} distinct modeled bulb centers after exact-center render doubles are collapsed by show_bulb_mesh, smallest falloff radius and name. These are observed table emitters. The table's grouping is not the machine's wiring and does not establish fitted GI quantity or complete coverage; quantity is deliberately omitted.")
		elif group == "pinmame.output.solenoid" and address == 16:
			_placement(device, [seed["solenoid_drawing"]["flasher16"]], "emitter", [SOLENOID_DRAWING_SOURCE, TABLE_SOURCE, *manual_refs[:1]])
			_note(device, "Observed projection from the round factory location symbol immediately above16 inside the left curl ramp on PDF84. A separate six-control fit is used for this page; the symbol is slightly outside its control convex hull and explicitly extrapolated. The bulbless table f16 glow does not supply a socket coordinate. No independent physical survey or validated socket location is claimed.")
		elif group == "pinmame.output.solenoid" and str(address) in seed["vpw"]["flasher_bases"]:
			_placement(device, seed["vpw"]["flasher_bases"][str(address)], "emitter", [VPW_TABLE_SOURCE, VPW_SCRIPT_SOURCE, "vpx-world.radical.vpw", *manual_refs[:1]])
			_note(device, "Observed VPW Flupper dome-base center(s), traced through this table's own SolCallback and ObjLevel-to-Flasherbase array. These are modeled dome locations, not Flasher glow sprites. The table is descended from JPSalas and supplies geometry, not independent validation. Physical photographs corroborate domes; no photographed pixel coordinate is used as a measurement.")
		elif group == "pinmame.output.solenoid" and prototype and address in (3, 15):
			point = seed["vpw"]["prototype_popper_exit" if address == 3 else "prototype_sling49"]
			_placement(device, [point], "effect", [VPW_TABLE_SOURCE, VPW_SCRIPT_SOURCE, *manual_refs[:1]])
			if address == 3:
				_note(device, "Observed effect projection onto the prototype popper return outlet sw16. The popper entry/sensor is sw16a; this remote outlet projection is not the under-playfield coil body or switch center.")
			else:
				_note(device, "Observed effect projection onto the prototype top sling's RightSlingshot1 rubber-wall vertex mean, not the under-playfield coil body.")
		elif group == "pinmame.output.solenoid" and str(address) in seed["solenoids"] and device.get("availability") != "unused":
			point = seed["solenoids"][str(address)]
			_placement(device, [point], "effect", refs)
			_note(device, f"Observed mechanism-effect projection onto {point['name']} ({point['type']}); this marks the acted-on bank, gate, bumper, sling rubber, lock or kickback lane rather than the under-playfield coil body. No measured coil center or travel time is claimed.")
	definition["machine"]["playfield"] = {"width": 952, "height": 1974, "units": "vpx", "provenance": provenance(TABLE_SOURCE)}
	definition["sources"].extend(spatial_sources(seed, root))
	return definition


def spatial_sources(seed: dict[str, Any], root: Path = ROOT) -> list[dict[str, Any]]:
	sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
	return [
		_location_drawing_source(seed["solenoid_drawing"], root, "solenoid"),
		_location_drawing_source(seed["switch_drawing"], root, "switch"),
		{"id": TABLE_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/radical-1990/source/Radical! (Bally 1990).vpx", "sha256": seed["table_sha256"], "license": "NOASSERTION; user-supplied table retained for research, not redistributed", "attribution": "JPSalas; Radical! table header 1.0.0 and SplashInfo v1.0.2, 2018", "locator": "Retained exact VPX table, bounds left=0 top=0 right=952 bottom=1974; vpxtool git:v0.33.3. Table geometry represents the prototype layout while script selects radcl_l1; unchanged production mechanisms are observed proxies, never independent validation."},
		{"id": EXTRACTION_SOURCE, "kind": "human_review", "uri": "external:pinmame-vpx-sources/bally/radical-1990/extracted-vpxtool", "sha256": sha(root / SEED), "license": "NOASSERTION; compact derived factual coordinates", "attribution": "JPSalas; vpxtool contributors; primary curator", "locator": "The digest identifies the committed coordinate register tools/seeds/bally/radical-1990-spatial.json, not the external directory. Each selected object's exact file path and SHA256 are retained there. Shared extract_spatial_candidates normalization, stored centers or polygon vertex means; render doubles collapsed only at exact bulb centers. Extraction integrity is separately checked against its full-file manifest."},
		{"id": DRAWING_SOURCE, "kind": "manual", "uri": "https://www.ipdb.org/files/1904/Bally_1990_Radical_Operator_Handbook.pdf", "source_id": "1904", "original_filename": "Bally_1990_Radical_Operator_Handbook.pdf", "sha256": "a5085eb4c9088f3cba48949dba9f30a72c8aa3f30208d4f65150cc6e1f777cb6", "license": "NOASSERTION; manufacturer copyright, compact drawing excerpt only", "attribution": "Midway Manufacturing Company / Bally, 1990; hosted by the Internet Pinball Database", "locator": "Verified Radical! IPDB machine page https://www.ipdb.org/machine.cgi?id=1904; handbook PDF page 80, printed 2-26. New derived crop and measurements retained/reviewed 2026-11-06; original download time unrecorded.", "excerpts": [{"id": "lamp-location-measurements", "locator": "PDF page 80 (2-26), numbered lamp-location drawing; six independent mechanism controls", "path": DRAWING_EXCERPT, "sha256": sha(root / DRAWING_EXCERPT), "image": seed["drawing"]["image"], "image_sha256": seed["drawing"]["sha256"], "image_derivation": seed["drawing"]["image_derivation"], "method": "manual", "transcribed_by": "primary curator, 2026-11-06", "reviewed": True}]},
		{"id": VPW_TABLE_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/radical-1990/vpw-1.0.1/source/Radical (Bally 1990) Prototype _VPWmod_v1.0.1.vpx", "sha256": seed["vpw"]["table_sha256"], "acquired_at": seed["vpw"]["acquired_at"], "license": "NOASSERTION; original authors' community table, research only; VPX not redistributed", "attribution": "JPSalas, 32assassin, VPinWorkshop; benji, iaakki, Sixtoe and contributors", "locator": "Authenticated VPU acquisition from " + seed["vpw"]["source_url"] + "; vpxtool git:v0.33.3. Same 952x1974 bounds. Descendant of the old retained JPSalas table, not independent corroboration; full extraction manifest is pinned separately."},
		{"id": VPW_SCRIPT_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/bally/radical-1990/vpw-1.0.1/extracted-vpxtool/script.vbs", "sha256": seed["vpw"]["script_sha256"], "acquired_at": seed["vpw"]["acquired_at"], "known_working": True, "license": "NOASSERTION; original community authors retain copyright", "attribution": "JPSalas, 32assassin, VPinWorkshop and contributors", "locator": "Exact script of retained VPW1.0.1; source selection radcl_l1, prototype mechanism geometry, default DisableUpperSling=1, forced popper eject. Used for its own bindings, never unmeasured factory timing.", "excerpts": [{"id": "vpw-retained-bindings", "path": "evidence/excerpts/bally.radical.1990/vpw-retained-bindings.md", "sha256": sha(root / "evidence/excerpts/bally.radical.1990/vpw-retained-bindings.md"), "locator": "Exact numbered script spans for prototype mechanisms, callback/dome binding and Flupper initialization", "method": "mixed", "transcribed_by": "primary curator from exact script bytes", "reviewed": True}]},
	]


def _location_drawing_source(drawing: dict[str, Any], root: Path, category: str) -> dict[str, Any]:
	name = f"{category}-location-measurements"
	path = f"evidence/excerpts/bally.radical.1990/{name}.md"
	part = "left curl flasher 16 factory symbol" if category == "solenoid" else "Middle Man 27 actuator blade"
	return {
		"id": f"manual.radical.{category}-location", "kind": "manual",
		"uri": "https://www.ipdb.org/files/1904/Bally_1990_Radical_Operator_Handbook.pdf",
		"source_id": "1904", "original_filename": "Bally_1990_Radical_Operator_Handbook.pdf",
		"sha256": "a5085eb4c9088f3cba48949dba9f30a72c8aa3f30208d4f65150cc6e1f777cb6",
		"acquired_at": "2026-11-06T08:42:02.203570Z",
		"license": "NOASSERTION; manufacturer copyright, compact factual drawing only",
		"attribution": "Midway Manufacturing Company / Bally, 1990; IPDB hosting",
		"locator": f"Verified machine page https://www.ipdb.org/machine.cgi?id=1904; PDF {drawing['pdf_page']} / printed {drawing['printed_page']}, {part}. Exact fresh acquisition recorded on manual.radical; independent page-specific fit, not a copied lamp-page transform.",
		"excerpts": [{"id": name, "locator": f"PDF {drawing['pdf_page']} {part} and six independently read mechanism controls",
			"path": path, "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest(),
			"image": drawing["image"], "image_sha256": drawing["sha256"],
			"image_derivation": drawing["image_derivation"], "method": "manual",
			"transcribed_by": "primary curator, 2026-11-06", "reviewed": True}],
	}


def verify_spatial_evidence(root: Path = ROOT) -> None:
	seed = load_json(root / SEED)
	for key in ("drawing", "solenoid_drawing", "switch_drawing"):
		drawing = seed[key]
		if hashlib.sha256((root / drawing["image"]).read_bytes()).hexdigest() != drawing["sha256"]:
			raise RuntimeError(f"Radical {key} image drifted")
	vpx_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not vpx_root:
		return
	extracted = Path(vpx_root) / "bally/radical-1990/extracted-vpxtool"
	points = [*seed["inputs"].values(), seed["production_switch_16"], *seed["solenoids"].values(), seed["bowtie_sensor_projection"], *seed["gi_bulbs"]]
	for point in points:
		path = extracted / point["artifact"]
		if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != point["sha256"]:
			raise RuntimeError(f"Radical coordinate evidence missing or changed: {path}")
	vpw_extracted = Path(vpx_root) / seed["vpw"]["relative_root"] / "extracted-vpxtool"
	vpw_points = [seed["vpw"]["prototype_sensor16"], seed["vpw"]["prototype_popper_exit"], seed["vpw"]["prototype_sling49"], *[p for ps in seed["vpw"]["flasher_bases"].values() for p in ps]]
	for point in vpw_points:
		path = vpw_extracted / point["artifact"]
		if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != point["sha256"]:
			raise RuntimeError(f"Radical VPW geometry evidence missing or changed: {path}")
	verify_world_mesh(Path(vpx_root), seed)


def verify_world_mesh(vpx_root: Path, seed: dict[str, Any]) -> None:
	"""Check primitive origins against actual exported vertices and Bumper controls."""
	mesh = seed["vpw"]["world_mesh"]
	path = vpx_root / mesh["relative_path"]
	if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != mesh["sha256"]:
		raise RuntimeError(f"Radical world mesh missing or changed: {path}")
	objects = {o["name"]: o for o in mesh["objects"]}
	actual = {name: {"count": 0, "min": [float("inf")] * 3, "max": [float("-inf")] * 3} for name in objects}
	name = None
	with path.open(encoding="utf-8") as stream:
		for line in stream:
			if line.startswith("o "):
				name = line[2:].strip()
			elif name in actual and line.startswith("v "):
				value = actual[name]
				value["count"] += 1
				for axis, coordinate in enumerate(map(float, line.split()[1:])):
					value["min"][axis] = min(value["min"][axis], coordinate)
					value["max"][axis] = max(value["max"][axis], coordinate)
	for name, expected in objects.items():
		value = actual[name]
		if (value["count"], value["min"], value["max"]) != (expected["vertex_count"], expected["bounds_min"], expected["bounds_max"]):
			raise RuntimeError(f"Radical mesh bounds differ: {name}")
		center = [(a + b) / 2 for a, b in zip(value["min"], value["max"])]
		origin = expected["stored_origin"]
		if max(abs(center[0] - origin["x"]) / 952, abs(center[1] - origin["y"]) / 1974) >= 0.001:
			raise RuntimeError(f"Radical primitive origin is displaced from mesh: {name}")
		if name.startswith("bumperbulb"):
			number = name.removeprefix("bumperbulb")
			bumper = load_json(vpx_root / seed["vpw"]["relative_root"] / f"extracted-vpxtool/gameitems/Bumper.Bumper{number}.json")["Bumper"]["center"]
			if max(abs(center[0] - bumper["x"]) / 952, abs(center[1] - bumper["y"]) / 1974) >= 0.000001:
				raise RuntimeError(f"Radical independent bumper control differs: {number}")


def build_report(definition: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
	seed = load_json(root / SEED)
	located, omitted, not_applicable = [], [], []
	count = 0
	for collection in ("inputs", "outputs"):
		for device in definition[collection]:
			entry = {"id": device["id"], **device["binding"]}
			spatial = device.get("spatial")
			if spatial is None:
				omitted.append(entry)
			elif spatial["status"] == "not_applicable":
				not_applicable.append({**entry, "reason": spatial["reason"]})
			else:
				located.append({**entry, "placements": spatial["placements"]})
				count += len(spatial["placements"])
	prototype = definition["machine"]["id"] == "bally.radical-prototype.1990"
	blockers = [
		"All placements remain observed. The lamp drawing provides insert-center projections, not socket centers; measurements outside its six-control convex hull are extrapolated. Table geometry and manual drawings are potentially related evidence, not independent factory measurements.",
		"The 39 modeled playfield GI bulb centers are table observations. No own-machine wiring or complete GI socket diagram assigns/counts every physical emitter; the fitted count and completeness remain unproved.",
		"Flasher16 now has an observed factory-symbol projection from its own solenoid-location drawing; the point is extrapolated and not independently surveyed. Other playfield flashers use the VPW dome bases; backbox emitters sharing these circuits do not receive invented playfield coordinates.",
		"The table's Drain kicker is a ball-disposal helper, not an outhole sensor/coil center. Trough switches 11 and 12 and the outhole switch 10 / coil 1 lack defensible table coordinates. A measured underside/location drawing or physical survey is needed.",
		"Middle Man 27 now has an observed factory-actuator projection onto its own horizontal blade on the switch-location drawing. This point is extrapolated and does not claim the hidden microswitch body center or independent placement validation.",
	]
	if prototype:
		blockers.append("Prototype popper and top sling now have observed VPW projections. The popper's entry switch, under-playfield coil and remote return outlet are distinct; no precise physical sensor/coil survey is claimed.")
	return {
		"format": "pinmame-spatial-blockers", "version": 1,
		"machine_id": definition["machine"]["id"], "coverage_status": "partial",
		"coordinate_convention": seed["coordinate_convention"], "table_bounds": seed["bounds"],
		"source_hashes": {"table": seed["table_sha256"], "script": seed["script_sha256"],
			"vpw_table": seed["vpw"]["table_sha256"], "vpw_world_obj": seed["vpw"]["world_mesh"]["sha256"],
			"spatial_seed": hashlib.sha256((root / SEED).read_bytes()).hexdigest()},
		"drawing_reconciliation": seed["drawing"], "solenoid_drawing_reconciliation": seed["solenoid_drawing"], "switch_drawing_reconciliation": seed["switch_drawing"],
		"placement_count": count, "placement_status_counts": {"observed": count},
		"located": located, "omitted": omitted, "not_applicable": not_applicable,
		"blockers": blockers, "promotion_decision": "Remain partial; no author-ready promotion is justified.",
	}


def report_markdown(report: dict[str, Any]) -> str:
	lines = [f"# {report['machine_id']} spatial evidence", "", "Coverage: **partial**. Every located placement remains **observed**.", "", report["coordinate_convention"], "", f"Placements: {report['placement_count']}; omitted device spatial records: {len(report['omitted'])}.", "", "## Evidence and transformation", "", "Exact hashes, every selected VPX object and source coordinate, diagram pixels, six controls and affine coefficients are retained in `tools/seeds/bally/radical-1990-spatial.json`. Full extraction integrity is checked separately. VPX normalization uses the shared helper against bounds 0,0,952,1974. The manual lamp-location drawing is projected through `tools/drawing_callouts.py` and rounded to 0.001; these are insert-center projections and no socket survey is claimed. The maximum control leave-one-out error is 0.014408 normalized. All extrapolated measurements stay observed. The 0.07 callout convention is only a cross-check limit; it does not promote these projections.", "", "## Projection classes", "", "- Matrix lamps: center of each numbered illuminated insert in the manual drawing, projected to the playfield plane.", "- Lock sensors: their own script-bound ball kickers, not separate switch bodies.", "- Bowtie sensor: vertex mean of its own mechanism wall, not a measured microswitch.", "- Sling scoring contacts: own rubber-wall vertex means, not leaf-contact bodies.", "- Coils: effect anchors on their own mechanism/ball path; no under-playfield coil location is asserted.", "- GI: one bulb-mesh light per exact center; retain the smallest falloff-radius render double, then lexical name.", "", "## Remaining evidence", ""]
	lines[-3:-3] = [
		"- Flashers 9/25..32: the callback-bound VPW dome bases, whose origins were checked against actual exported world-mesh bounds; independent Bumper controls verify that coordinate plane.",
		"- Flasher 16: the factory's own numbered symbol on PDF 84, projected by a separate six-control fit (maximum leave-one-out error 0.008251), explicitly extrapolated and observed. The table's bulbless glow is not the coordinate source.",
		"- Middle Man 27: midpoint of the distinct factory-marked horizontal actuator blade on PDF 82, projected by that page's own six-control fit (maximum leave-one-out error 0.006349), explicitly extrapolated and observed; no precise contact-body center is claimed.",
	]
	lines.extend(f"- {blocker}" for blocker in report["blockers"])
	lines += ["", "## Omitted spatial records", "", *[f"- `{item['id']}`: `{item['group']}` {item['device']}" for item in report["omitted"]], "", report["promotion_decision"], ""]
	return "\n".join(lines)
