"""Reviewed AC/DC Vault Edition normalized playfield placements."""

from __future__ import annotations


INPUT_POSITIONS = {
	1: [(0.082350, 0.568794)], 2: [(0.094800, 0.539655)], 3: [(0.106265, 0.513278)], 4: [(0.118582, 0.486390)],
	5: [(0.128387, 0.461360)], 6: [(0.870273, 0.458149)], 7: [(0.870273, 0.484732)], 8: [(0.870273, 0.511270)],
	9: [(0.870273, 0.537999)], 10: [(0.512028, 0.311990)], 11: [(0.569330, 0.321673)], 12: [(0.628993, 0.331598)],
	13: [(0.057878, 0.097009)], 14: [(0.257677, 0.205595)],
	18: [(0.580000, 0.940000)], 19: [(0.650000, 0.921000)], 20: [(0.720000, 0.903000)], 21: [(0.790000, 0.884000)], 22: [(0.835000, 0.872000)],
	23: [(0.947605, 0.890661)], 24: [(0.051591, 0.763999)], 25: [(0.128560, 0.743684)],
	26: [(0.220215, 0.726524)], 27: [(0.685802, 0.726524)], 28: [(0.775077, 0.743384)], 29: [(0.852337, 0.763147)],
	30: [(0.524113, 0.155556)], 31: [(0.736963, 0.151240)], 32: [(0.639000, 0.235974)], 33: [(0.163467, 0.353290)],
	34: [(0.235358, 0.359817)], 35: [(0.378990, 0.336108)], 36: [(0.399947, 0.145745)], 37: [(0.450843, 0.016417)],
	38: [(0.542534, 0.083160)], 39: [(0.632607, 0.074157)], 40: [(0.722549, 0.064641)], 41: [(0.802046, 0.150042)],
	42: [(0.784142, 0.364083)], 43: [(0.936687, 0.441300)], 44: [(0.104831, 0.106953)], 45: [(0.773227, 0.630580)],
	48: [(0.947901, 0.757156)], 59: [(0.939389, 0.104705)], 61: [(0.720277, 0.695345)], 62: [(0.720277, 0.695345)],
	81: [(0.620752, 0.847281)], 83: [(0.284974, 0.847281)],
}

CABINET_INPUT_ROLES = {
	15: "cabinet.tournament", 16: "cabinet.start", 64: "cabinet.fire",
	65: "cabinet.coin", 66: "cabinet.coin", 67: "cabinet.coin", 68: "cabinet.coin", 69: "cabinet.coin",
	82: "cabinet.flipper", 84: "cabinet.flipper", -7: "cabinet.tilt", -6: "cabinet.tilt", -5: "service.ticket",
	-3: "service.button", -2: "service.button", -1: "service.button", 0: "service.button",
}

CABINET_OUTPUT_ROLES = {
	("pinmame.output.solenoid", 8): "cabinet.shaker",
	("pinmame.output.solenoid", 24): "cabinet.knocker",
	("physical.output.ticket", 33): "service.ticket",
	("physical.output.ticket", 34): "service.ticket",
	("physical.output.ticket", 35): "service.ticket",
}

SOLENOID_POSITIONS = {
	1: [(0.861682, 0.865767)], 2: [(0.947605, 0.890661)], 3: [(0.720277, 0.695345)], 4: [(0.939496, 0.516017)],
	5: [(0.783568, 0.017554)], 9: [(0.524113, 0.155556)], 10: [(0.736963, 0.151240)], 11: [(0.639000, 0.235974)],
	12: [(0.450843, 0.016417)], 13: [(0.220215, 0.726524)], 14: [(0.685802, 0.726524)],
	15: [(0.284974, 0.847281)], 16: [(0.620752, 0.847281)], 17: [(0.085300, 0.064573)],
	20: [(0.268998, 0.232922)], 21: [(0.140206, 0.658291)], 22: [(0.926880, 0.064573)], 23: [(0.340202, 0.012178)],
	25: [(0.524113, 0.155556), (0.736963, 0.151240), (0.639000, 0.235974)], 26: [(0.416532, 0.219762)],
	27: [(0.220513, 0.336352)], 28: [(0.370644, 0.308138)], 29: [(0.799869, 0.345778)],
	30: [(0.768324, 0.258153)], 31: [(0.863152, 0.622217)], 32: [(0.720277, 0.695345)],
}

LAMP_POSITIONS = {
	3: [(0.051196, 0.689776)], 4: [(0.129113, 0.677336)], 5: [(0.234637, 0.675286)], 6: [(0.669840, 0.673464)],
	7: [(0.773183, 0.676316)], 8: [(0.851702, 0.688299)], 9: [(0.205410, 0.467186)], 10: [(0.194818, 0.494780)],
	11: [(0.182945, 0.521927)], 12: [(0.171577, 0.549355)], 13: [(0.159593, 0.576496)],
	18: [(0.176836, 0.382324)], 19: [(0.249102, 0.383727)], 20: [(0.319156, 0.371832)], 21: [(0.385290, 0.360157)],
	22: [(0.490126, 0.345101)], 23: [(0.548768, 0.354897)], 24: [(0.609506, 0.365405)], 25: [(0.504132, 0.402215)],
	26: [(0.693897, 0.380765)], 27: [(0.883718, 0.302332)], 28: [(0.853487, 0.354285)], 29: [(0.815417, 0.408785)],
	30: [(0.810210, 0.456092)], 31: [(0.810557, 0.483704)], 32: [(0.810557, 0.511518)], 33: [(0.811142, 0.539268)],
	34: [(0.701395, 0.470890)], 35: [(0.415790, 0.223289)], 36: [(0.430513, 0.281517)], 37: [(0.542605, 0.044275)],
	38: [(0.631802, 0.034929)], 39: [(0.722618, 0.025580)], 40: [(0.634728, 0.009639)], 41: [(0.324593, 0.763245)],
	42: [(0.365233, 0.788881)], 43: [(0.385618, 0.820375)], 44: [(0.450544, 0.758364)], 45: [(0.452709, 0.784999)],
	46: [(0.452292, 0.806801)], 47: [(0.452909, 0.830226)], 48: [(0.453572, 0.855999)], 49: [(0.577164, 0.762689)],
	50: [(0.539155, 0.790352)], 51: [(0.521402, 0.820196)], 52: [(0.126360, 0.300005)],
	53: [(0.417017, 0.007329)], 54: [(0.417017, 0.007329)], 55: [(0.417017, 0.007329)], 56: [(0.417017, 0.007329)],
	57: [(0.344369, 0.009803)], 58: [(0.724697, 0.009803)], 60: [(0.523187, 0.157771)], 61: [(0.734840, 0.151549)],
	62: [(0.637734, 0.236849)], 64: [(0.762463, 0.390665)], 65: [(0.417017, 0.007329)], 66: [(0.417017, 0.007329)],
	67: [(0.558824, 0.007329)], 68: [(0.558824, 0.007329)], 69: [(0.558824, 0.007329)], 70: [(0.558824, 0.007329)],
	71: [(0.558824, 0.007329)], 72: [(0.558824, 0.007329)],
}

GI_POSITIONS = [
	(0.900285, 0.469020), (0.874862, 0.583358), (0.042912, 0.489004), (0.786737, 0.291340), (0.048016, 0.289073),
	(0.147091, 0.159873), (0.051867, 0.020208), (0.835677, 0.052008), (0.692302, 0.824228), (0.216433, 0.825743),
	(0.891462, 0.415710), (0.833431, 0.124491), (0.949749, 0.005717), (0.370579, 0.032017), (0.187581, 0.045169),
	(0.348518, 0.211355), (0.541245, 0.282769), (0.355565, 0.270940), (0.206599, 0.288832), (0.758747, 0.802286),
	(0.720491, 0.724956), (0.181816, 0.698841), (0.151883, 0.803504), (0.757544, 0.228868), (0.498101, 0.087248),
	(0.587316, 0.077237), (0.677718, 0.068298), (0.768350, 0.059083), (0.497783, 0.091346), (0.588134, 0.083212),
	(0.677903, 0.074554), (0.766505, 0.063271), (0.653348, 0.275933), (0.033099, 0.599149), (0.896912, 0.524478),
	(0.697530, 0.758900), (0.206559, 0.759480), (0.100182, 0.411436),
	(0.026665, 0.029661), (0.337830, 0.029661), (0.643099, 0.029661), (0.972992, 0.030127),
	(0.175828, 0.029661), (0.485041, 0.029661), (0.820140, 0.029661),
]


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]], source_refs: tuple[str, ...]) -> None:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{device['id']}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": _provenance(*source_refs)})
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def apply_vault_spatial(
	inputs: list[dict[str, object]],
	outputs: list[dict[str, object]],
	*,
	table_source: str,
	script_source: str,
	manual_source: str,
	core_source: str,
) -> None:
	"""Apply the fail-closed, manually reviewed spatial disposition to every Vault device."""
	located_sources = (table_source, script_source, manual_source)
	for device in inputs:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", manual_source)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", manual_source)
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], located_sources)
		elif address in CABINET_INPUT_ROLES:
			device["roles"] = [CABINET_INPUT_ROLES[address]]
			_not_applicable(device, "cabinet_or_service", manual_source)
		else:
			raise ValueError(f"Vault input {group} {address} has no reviewed spatial disposition")
		if group == "pinmame.input.switch" and address in {18, 19, 20, 21, 22}:
			device.setdefault("physical", {})["location"] = "Under-apron four-ball trough assembly 500-6318-24-ND"
		if group == "pinmame.input.switch" and address in {61, 62}:
			device.setdefault("physical", {})["location"] = "Rotating cannon motor-and-switch assembly"

	for device in outputs:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if device["availability"] == "unused":
			_not_applicable(device, "unused", manual_source)
		elif kind == "virtual":
			_not_applicable(device, "virtual", core_source)
		elif group == "pinmame.output.lamp" and address in {1, 2, 63}:
			device["roles"] = [{1: "cabinet.start", 2: "cabinet.tournament", 63: "cabinet.fire"}[address]]
			_not_applicable(device, "cabinet_or_service", manual_source)
		elif (group, address) in CABINET_OUTPUT_ROLES:
			device["roles"] = [CABINET_OUTPUT_ROLES[(group, address)]]
			_not_applicable(device, "cabinet_or_service", manual_source)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			_located(device, "emitter" if kind == "flasher" else "effect", SOLENOID_POSITIONS[address], located_sources)
			if address == 25:
				device.setdefault("physical", {})["quantity"] = 3
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			_located(device, "emitter", LAMP_POSITIONS[address], located_sources)
		elif group == "pinmame.output.gi" and address == 0:
			_located(device, "emitter", GI_POSITIONS, located_sources)
			device.setdefault("physical", {}).update({"quantity": 45, "notes": "One conventional GI channel drives 38 reviewed playfield bulbs and seven back-panel bulbs."})
		else:
			raise ValueError(f"Vault output {group} {address} ({kind}) has no reviewed spatial disposition")
