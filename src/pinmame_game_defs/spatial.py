from __future__ import annotations

import copy
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable
from xml.sax.saxutils import escape

from .errors import DefinitionError
from .jsonio import file_sha256, load_json


PLAYFIELD_SPACE_DESCRIPTION = "playfield is normalized VPX/player view: x=0 left, x=1 right, y=0 rear/backglass end, y=1 front/apron end."
SPATIAL_RETROFIT_PENDING_MACHINE_IDS = (
	"stern.ac-dc-premium-limited-edition-luci.2012",
	"stern.ac-dc-pro.2012",
	"stern.ali.1980",
	"stern.avatar-limited-edition.2010",
	"stern.avatar-pro.2010",
	"stern.avengers-limited-edition.2012",
	"stern.avengers-pro.2012",
	"stern.batman-the-dark-knight-pro.2008",
	"stern.batman-the-dark-knight-standard-home-edition.2010",
	"stern.iron-man.2010",
	"stern.metallica-pro.2013",
	"stern.ripley-s-believe-it-or-not.2004",
	"stern.spider-man.2007",
	"stern.the-rolling-stones-limited-edition.2011",
	"stern.the-rolling-stones-standard.2011",
	"stern.transformers-limited-edition.2011",
	"stern.transformers-pro.2011",
	"stern.tron-legacy-limited-edition.2011",
	"stern.tron-legacy-pro.2011",
	"stern.twenty-four.2009",
	"stern.x-men-limited-edition.2012",
	"stern.x-men-pro.2012",
)

DIRECT_CENTER_TYPES = {
	"bumper",
	"flipper",
	"flasher",
	"gate",
	"hittarget",
	"kicker",
	"light",
	"plunger",
	"spinner",
	"trigger",
}


_SPATIAL_KNOWLEDGE_BANNER = "Coverage: **partial — normalized spatial placements pending.**"
_AUTHOR_READY_KNOWLEDGE_LINE = re.compile(r"^Coverage: \*\*author-ready(?:\s*-\s*(?P<detail>.*?))?\*\*$")


def fail_closed_spatial_knowledge(machine_id: str, text: str) -> str:
	"""Add the temporary spatial-status banner to a pending recreation note."""
	if machine_id not in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		return text
	had_final_newline = text.endswith(("\n", "\r"))
	lines = text.splitlines(keepends=True)
	if not lines:
		return text

	def line_text(line: str) -> str:
		return line.removesuffix("\n").removesuffix("\r")

	h1_index = next((index for index, line in enumerate(lines) if line_text(line).startswith("# ")), None)
	if h1_index is None:
		return text
	banner_index = h1_index + 1
	while banner_index < len(lines) and not line_text(lines[banner_index]):
		banner_index += 1
	if banner_index < len(lines) and line_text(lines[banner_index]) == _SPATIAL_KNOWLEDGE_BANNER:
		return text

	coverage_index = None
	detail = None
	for index, line in enumerate(lines[h1_index + 1:], start=h1_index + 1):
		match = _AUTHOR_READY_KNOWLEDGE_LINE.fullmatch(line_text(line))
		if match:
			coverage_index = index
			detail = match.group("detail")
			break

	line_ending = "\n"
	body = lines[h1_index + 1 :]
	if coverage_index is not None:
		del body[coverage_index - h1_index - 1]
	while body and not line_text(body[0]):
		body.pop(0)
	status_block = [line_ending, _SPATIAL_KNOWLEDGE_BANNER + line_ending]
	if detail:
		status_block.append(f"Previously validated non-spatial scope: **{detail}**{line_ending}")
	status_block.append(line_ending)
	result = "".join(lines[: h1_index + 1] + status_block + body)
	if not had_final_newline:
		result = result.removesuffix(line_ending)
	return result


def fail_closed_spatial_partial(definition: dict[str, Any]) -> dict[str, Any]:
	"""Return the temporary v2 partial form for a pending spatial retrofit.

	The explicit pending tuple is intentionally the sole migration switch: remove one ID
	only when its actual device placements have been reviewed and committed.
	"""
	machine_id = definition.get("machine", {}).get("id")
	if machine_id not in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		return definition
	result = copy.deepcopy(definition)
	result["schema_version"] = 2
	coverage = result["coverage"]
	coverage["status"] = "partial"
	missing = list(coverage.get("missing", []))
	if "spatial_placement" not in missing:
		missing.append("spatial_placement")
	coverage["missing"] = missing
	coverage.setdefault("dimensions", {})["spatial_placement"] = "unknown"
	return result


def spatial_partial_path(path: Path) -> Path:
	"""Map a legacy author-ready output path to its fail-closed partial location."""
	parts = list(path.parts)
	try:
		index = parts.index("author-ready")
	except ValueError:
		return path
	parts[index] = "partial"
	return Path(*parts)


def _casefold_mapping(value: dict[str, Any]) -> dict[str, Any]:
	return {str(key).casefold(): nested for key, nested in value.items()}


def _unwrap_json(value: Any) -> Any:
	while isinstance(value, dict):
		keys = _casefold_mapping(value)
		for key in ("data", "value", "item", "gameitem", "gamedata"):
			nested = keys.get(key)
			if isinstance(nested, (dict, list)) and (len(value) == 1 or key in {"gameitem", "gamedata"}):
				value = nested
				break
		else:
			return value
	return value


def _number(mapping: dict[str, Any], *names: str) -> float | None:
	values = _casefold_mapping(mapping)
	for name in names:
		value = values.get(name.casefold())
		if isinstance(value, bool):
			continue
		if isinstance(value, (int, float)) and math.isfinite(float(value)):
			return float(value)
	return None


def _text(mapping: dict[str, Any], *names: str) -> str | None:
	values = _casefold_mapping(mapping)
	for name in names:
		value = values.get(name.casefold())
		if isinstance(value, str) and value.strip():
			return value.strip()
	return None


def _json_documents(extracted_directory: Path) -> list[tuple[Path, Any]]:
	if not extracted_directory.is_dir():
		raise DefinitionError(f"VPX extraction directory does not exist: {extracted_directory}")
	documents: list[tuple[Path, Any]] = []
	for path in sorted(extracted_directory.rglob("*.json"), key=lambda candidate: candidate.relative_to(extracted_directory).as_posix().casefold()):
		try:
			documents.append((path, load_json(path)))
		except (OSError, json.JSONDecodeError) as error:
			raise DefinitionError(f"Could not read extracted VPX JSON {path}: {error}") from error
	if not documents:
		raise DefinitionError(f"VPX extraction directory has no JSON documents: {extracted_directory}")
	return documents


def _gamedata(documents: Iterable[tuple[Path, Any]]) -> dict[str, Any]:
	candidates: list[tuple[Path, dict[str, Any]]] = []
	for path, document in documents:
		value = _unwrap_json(document)
		if not isinstance(value, dict):
			continue
		fields = _casefold_mapping(value)
		if {"left", "top", "right", "bottom"} <= set(fields):
			candidates.append((path, value))
	if not candidates:
		raise DefinitionError("Extracted VPX JSON has no gamedata object with left, top, right, and bottom bounds")
	candidates.sort(key=lambda candidate: (candidate[0].name.casefold() != "gamedata.json", candidate[0].as_posix().casefold()))
	return candidates[0][1]


def _item_record(path: Path, document: Any) -> tuple[str | None, str | None, dict[str, Any] | None]:
	value = document
	wrapper_type: str | None = None
	if isinstance(value, dict) and len(value) == 1:
		key, nested = next(iter(value.items()))
		if isinstance(nested, dict) and key.casefold() in DIRECT_CENTER_TYPES:
			wrapper_type = key
			value = nested
		else:
			value = _unwrap_json(value)
	else:
		value = _unwrap_json(value)
	if not isinstance(value, dict):
		return (None, None, None)
	item_type = wrapper_type or _text(value, "type", "item_type", "game_item_type", "kind")
	name = _text(value, "name", "item_name")
	stem_parts = path.stem.split(".", 1)
	if item_type is None and len(stem_parts) == 2:
		item_type = stem_parts[0]
	if name is None and len(stem_parts) == 2:
		name = stem_parts[1]
	if item_type is None:
		for parent in path.parents:
			if parent.name.casefold() == "gameitems":
				break
			if parent.parent.name.casefold() == "gameitems":
				item_type = parent.name
				break
	return (item_type, name, value)


def _item_point(value: dict[str, Any]) -> tuple[float | None, float | None]:
	x = _number(value, "x", "center_x", "centerx", "pos_x", "posx")
	y = _number(value, "y", "center_y", "centery", "pos_y", "posy")
	if x is not None and y is not None:
		return (x, y)
	fields = _casefold_mapping(value)
	for field_name in ("center", "position"):
		nested = fields.get(field_name)
		if not isinstance(nested, dict):
			continue
		x = _number(nested, "x")
		y = _number(nested, "y")
		if x is not None and y is not None:
			return (x, y)
	return (None, None)


def _round_point(value: float) -> float:
	return round(value, 6)


def extract_spatial_candidates(extracted_directory: Path, source_vpx: Path, vpxtool_version: str | None = None) -> dict[str, Any]:
	"""Produce candidate geometry only; this never names or maps canonical devices."""
	documents = _json_documents(extracted_directory)
	gamedata = _gamedata(documents)
	left = _number(gamedata, "left")
	top = _number(gamedata, "top")
	right = _number(gamedata, "right")
	bottom = _number(gamedata, "bottom")
	if None in {left, top, right, bottom} or right <= left or bottom <= top:
		raise DefinitionError("VPX gamedata bounds must be finite and have right > left and bottom > top")
	if not source_vpx.is_file():
		raise DefinitionError(f"VPX source file does not exist: {source_vpx}")
	objects: list[dict[str, Any]] = []
	for path, document in documents:
		item_type, name, value = _item_record(path.relative_to(extracted_directory), document)
		if item_type is None or item_type.casefold() not in DIRECT_CENTER_TYPES or value is None:
			continue
		fields = _casefold_mapping(value)
		if fields.get("is_backglass") is True or fields.get("backglass") is True:
			continue
		x, y = _item_point(value)
		if x is None or y is None:
			continue
		normalized_x = (x - left) / (right - left)
		normalized_y = (y - top) / (bottom - top)
		if not math.isfinite(normalized_x) or not math.isfinite(normalized_y) or not 0 <= normalized_x <= 1 or not 0 <= normalized_y <= 1:
			continue
		objects.append(
			{
				"type": item_type,
				"name": name or path.stem,
				"x": _round_point(normalized_x),
				"y": _round_point(normalized_y),
			}
		)
	objects.sort(key=lambda item: (item["type"].casefold(), item["name"].casefold(), item["x"], item["y"]))
	result: dict[str, Any] = {
		"format": "pinmame-vpx-spatial-candidates",
		"version": 1,
		"coordinate_space": "playfield",
		"source": {
			"vpx_sha256": file_sha256(source_vpx),
			"vpx_size": source_vpx.stat().st_size,
		},
		"bounds": {"left": left, "top": top, "right": right, "bottom": bottom},
		"objects": objects,
	}
	if vpxtool_version is not None:
		result["source"]["vpxtool_version"] = vpxtool_version
	return result


def _uses_wsl(executable: Path) -> bool:
	if os.name != "nt":
		return False
	try:
		with executable.open("rb") as stream:
			return stream.read(4) == b"\x7fELF"
	except OSError:
		return False


def _wsl_path(path: Path) -> str:
	try:
		result = subprocess.run(["wsl.exe", "--exec", "wslpath", "-a", str(path.resolve())], check=False, capture_output=True, text=True, timeout=30)
	except (OSError, subprocess.TimeoutExpired) as error:
		raise DefinitionError(f"Could not translate path for WSL: {path}: {error}") from error
	if result.returncode != 0 or not result.stdout.strip():
		detail = (result.stderr or result.stdout).strip()
		raise DefinitionError(f"Could not translate path for WSL: {path}: {detail}")
	return result.stdout.strip()


def _vpxtool_command(executable: Path, arguments: list[str | Path]) -> list[str]:
	if _uses_wsl(executable):
		converted = [_wsl_path(argument) if isinstance(argument, Path) else argument for argument in arguments]
		return ["wsl.exe", "--exec", _wsl_path(executable), *converted]
	return [str(executable), *(str(argument) for argument in arguments)]


def _vpxtool_version(executable: Path) -> str:
	try:
		result = subprocess.run(_vpxtool_command(executable, ["--version"]), check=False, capture_output=True, text=True, timeout=30)
	except (OSError, subprocess.TimeoutExpired) as error:
		raise DefinitionError(f"Could not execute vpxtool {executable}: {error}") from error
	if result.returncode != 0:
		return "unknown"
	text = (result.stdout or result.stderr).strip()
	return text or "unknown"


def extract_from_vpx(vpx: Path, vpxtool: Path) -> dict[str, Any]:
	if not vpx.is_file():
		raise DefinitionError(f"VPX source file does not exist: {vpx}")
	if not vpxtool.is_file():
		raise DefinitionError(f"vpxtool executable does not exist: {vpxtool}")
	with tempfile.TemporaryDirectory(prefix="pinmame-vpxtool-") as temporary:
		workspace = Path(temporary)
		copied_vpx = workspace / "source.vpx"
		destination = workspace / "extracted"
		try:
			shutil.copyfile(vpx, copied_vpx)
		except OSError as error:
			raise DefinitionError(f"Could not copy VPX source into the extraction workspace: {vpx}: {error}") from error
		command = _vpxtool_command(vpxtool, ["extract", "--force", "--output-dir", destination, copied_vpx])
		try:
			result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=600, cwd=workspace)
		except (OSError, subprocess.TimeoutExpired) as error:
			raise DefinitionError(f"vpxtool extraction failed: {error}") from error
		if result.returncode != 0:
			detail = (result.stderr or result.stdout).strip()
			raise DefinitionError(f"vpxtool extraction failed with exit code {result.returncode}: {detail}")
		return extract_spatial_candidates(workspace, vpx, _vpxtool_version(vpxtool))


def _marker_svg(role: str, x: float, y: float, label: str) -> str:
	color, shape = {
		"sensor": ("#1769aa", "circle"),
		"effect": ("#b04a00", "diamond"),
		"emitter": ("#8a1c46", "square"),
	}[role]
	if shape == "circle":
		marker = f'<circle cx="{x:.3f}" cy="{y:.3f}" r="7" fill="{color}" />'
	elif shape == "diamond":
		marker = f'<path d="M {x:.3f} {y - 8:.3f} L {x + 8:.3f} {y:.3f} L {x:.3f} {y + 8:.3f} L {x - 8:.3f} {y:.3f} Z" fill="{color}" />'
	else:
		marker = f'<rect x="{x - 7:.3f}" y="{y - 7:.3f}" width="14" height="14" fill="{color}" />'
	return f'<g>{marker}<text x="{x + 10:.3f}" y="{y - 9:.3f}" class="label">{escape(label)}</text></g>'


def render_spatial_overlay(definition: dict[str, Any]) -> str:
	"""Render canonical placements without a licensed playfield background image."""
	width, height, margin = 1000, 1600, 80
	playfield_width, playfield_height = width - (2 * margin), height - (2 * margin)
	machine = definition.get("machine", {})
	title = str(machine.get("name", machine.get("id", "Machine")))
	markers: list[tuple[str, str, float, float, str]] = []
	not_applicable: Counter[str] = Counter()
	for collection_name in ("inputs", "outputs"):
		for device in definition.get(collection_name, []):
			if not isinstance(device, dict):
				continue
			spatial = device.get("spatial")
			if not isinstance(spatial, dict):
				continue
			if spatial.get("status") == "not_applicable":
				not_applicable[str(spatial.get("reason", "unknown"))] += 1
			for placement in spatial.get("placements", []):
				if not isinstance(placement, dict):
					continue
				role, x, y, placement_id = placement.get("role"), placement.get("x"), placement.get("y"), placement.get("id")
				if role not in {"sensor", "effect", "emitter"} or not isinstance(x, (int, float)) or not isinstance(y, (int, float)) or not isinstance(placement_id, str):
					continue
				markers.append((str(device.get("id", "unknown")), placement_id, float(x), float(y), role))
	markers.sort(key=lambda item: (item[0], item[1], item[4], item[2], item[3]))
	lines = [
		'<?xml version="1.0" encoding="UTF-8"?>',
		f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
		"<style>.title{font:700 22px sans-serif}.label{font:12px sans-serif;paint-order:stroke;stroke:#fff;stroke-width:3;stroke-linejoin:round}.note{font:14px sans-serif}</style>",
		f'<text x="{margin}" y="34" class="title">{escape(title)} spatial overlay</text>',
		f'<rect x="{margin}" y="{margin}" width="{playfield_width}" height="{playfield_height}" fill="#f6f6f1" stroke="#222" stroke-width="2" />',
		f'<text x="{margin}" y="{margin - 12}" class="note">rear / backglass end</text>',
		f'<text x="{margin}" y="{height - margin + 24}" class="note">front / apron end</text>',
	]
	for device_id, placement_id, normalized_x, normalized_y, role in markers:
		x = margin + (normalized_x * playfield_width)
		y = margin + (normalized_y * playfield_height)
		lines.append(_marker_svg(role, x, y, f"{device_id}:{placement_id}"))
	na_text = ", ".join(f"{reason}={count}" for reason, count in sorted(not_applicable.items())) or "none"
	lines.extend(
		[
			f'<text x="{margin}" y="{height - 20}" class="note">N/A devices: {escape(na_text)}</text>',
			"</svg>",
		]
	)
	return "\n".join(lines) + "\n"
