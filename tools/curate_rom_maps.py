"""Generate the ROM maps under rom-maps/ from pinned inputs.

A ROM map is supplemental firmware knowledge for one memory layout of one physical machine: game
and mode state, operator adjustments, audits, replay levels, sound commands and mode-replay
recipes. Its `memory_map` is a complete Pinball Memory Maps document (tomlogic/pinball-memory-maps,
fileformat 0.8) so it can be compared with, or contributed back to, that project unchanged; what
that format has no section for goes under `extensions`, and `evidence` grades every descriptor.

Inputs are in-repository and pinned by SHA-256: the vendored upstream maps and schema under
rom-maps/_vendor/, and the bulk tables under tools/rom-map-inputs/, which were transcribed once from
contributor evidence retained in the working root (each source record names it). Nothing is read
from outside the repository, so `--check` reproduces the files byte for byte anywhere.

The maps are ODbL-1.0 (see rom-maps/README.md): the memory maps they extend are, and an extension
of an ODbL database is a derived database.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes  # noqa: E402

VENDOR = ROOT / "rom-maps" / "_vendor"
INPUTS = ROOT / "tools" / "rom-map-inputs"
TOMLOGIC_COMMIT = "7e63610464453e1902d6de2f90529a0705fdc2a2"
TOMLOGIC_REPO = "https://github.com/tomlogic/pinball-memory-maps"
TOMLOGIC_ATTRIBUTION = "This program makes use of content from the Pinball Memory Maps project. Copyright (C) Tom Collins and contributors."
ODBL = "ODbL-1.0 (contents DbCL-1.0)"

PINNED = {
	VENDOR / "map.schema.json": "5930c97fd30903fbba782930d7e194da98e75c01581b42941907dd6f5c43225a",
	VENDOR / "lw3_208.map.json": "e500263849de0ebf401213b2a728fea8ab982b0962e152469a88bf1bff3e20a1",
	VENDOR / "afm_113.map.json": "0323b3f62fb89fc1b456272cbce755842b9f814619c9e3a184aaf47a4059f32e",
	VENDOR / "LICENSE-ODbL.md": "607680718977f6f6c9607972afd98f208573f19251315ed1362a8589b51beaf5",
	VENDOR / "LICENSE-DbCL": "9dc0e8f2916dddaea5774747d8715de88eeb60d09104c25c53cb1573bac4d3cc",
}


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _pinned_input(path: Path) -> Any:
	expected = PINNED.get(path)
	if expected is None:
		raise RuntimeError(f"unpinned ROM-map input: {path}")
	actual = _sha256(path)
	if actual != expected:
		raise RuntimeError(f"ROM-map input drifted: {path} is {actual}, expected {expected}")
	return load_json(path)


def _hex(value: int, width: int = 4) -> str:
	return f"0x{value:0{width}X}"


def d(label: str, start: int, encoding: str, **extra: Any) -> dict[str, Any]:
	"""A Pinball Memory Maps descriptor with a hex CPU address."""
	return {"label": label, "start": _hex(start), "encoding": encoding, **extra}


def _tomlogic_source(source_id: str, path: str, sha256: str, version: int) -> dict[str, Any]:
	return {
		"id": source_id,
		"kind": "memory_map",
		"uri": f"{TOMLOGIC_REPO}/blob/{TOMLOGIC_COMMIT}/{path}",
		"revision": TOMLOGIC_COMMIT,
		"sha256": sha256,
		"locator": f"{path}, map version {version}; vendored as rom-maps/_vendor/{Path(path).name}",
		"license": "ODbL-1.0 (contents DbCL-1.0)",
		"attribution": TOMLOGIC_ATTRIBUTION,
		"acquired_at": "2026-10-04T13:32:00Z",
	}


def _ev(status: str, proof: list[str], verified_on: list[str], sources: list[str], note: str | None = None,
	applies_to: list[str] | None = None) -> dict[str, Any]:
	entry: dict[str, Any] = {"status": status, "proof": proof, "verified_on": verified_on, "sources": sources}
	if applies_to:
		entry["applies_to"] = applies_to
	if note:
		entry["note"] = note
	return entry


# --- Lethal Weapon 3 ----------------------------------------------------------------------------------

LW3_ROMS = ["lw3_208", "lw3_208p", "lw3_300", "lw3_301"]
LW3_RIG = "rom-state.lw3-301.totalrecall-2026-10-03"
LW3_TOMLOGIC = "memory-map.tomlogic.lw3-208"
LW3_ROM301 = "rom.lw3-301"


def _lw3_sources() -> list[dict[str, Any]]:
	return [
		_tomlogic_source(LW3_TOMLOGIC, "maps/dataeast/version3/lw3_208.map.json", PINNED[VENDOR / "lw3_208.map.json"], 9),
		{
			"id": LW3_RIG,
			"kind": "rom_analysis",
			"uri": "pinmame-game-defs-working-dir/review-artifacts/lethal-weapon-3-rom-state-2026-10-03/MANIFEST.sha256",
			"revision": "2026-10-03",
			"sha256": "2c70ccd9801a1e0296d503b45cc3c1024b13735fbc335020476614b056599a56",
			"locator": "docs/LW3_BLIND_SPOTS_ROM.md, docs/project_knowledge.md sections 4d-4x, docs/lw3_301.map.json, docs/AUDIT_NAMES.md, docs/LEO_AWARDS.md, docs/MUSIC_SELECT.md, docs/SOUND_LATCH.md, docs/PAYLOAD_lw1_at_sw32.md, docs/TR_SOUND_MAP.csv (transcribed into tools/rom-map-inputs/lethal-weapon-3-1992.sound-commands.json), rig recordings under rec/; the prose reading is knowledge/data-east/lethal-weapon-3-1992.md",
			"license": "contributor evidence, retained outside Git; facts only",
			"attribution": "Total Recall re-theme ROM campaign (Manuel), 5 Sep - 3 Oct 2026",
			"acquired_at": "2026-10-03T16:43:00Z",
		},
		{
			"id": LW3_ROM301,
			"kind": "rom_archive",
			"uri": "VPinMAME roms/lw3_301.zip (contributor ROM library)",
			"revision": "3.01 unofficial fan patch (CPU 3.01, display 3.00, 2.08 sound ROMs)",
			"sha256": "094935aa2f525c3bd46faab5c9de87a94c1bb13cde4238e5d62222d819ed8f13",
			"locator": "LW3CPUU.301 (CRC32 e6a44d10), lw3drom1.300 (CRC32 38f0ab03), Changelog-LW301.txt",
			"license": "ROM bytes not redistributed; identified by hash only",
			"attribution": "Data East Pinball; 3.01 patch by pinballcode.com",
			"acquired_at": "2026-10-03T16:43:00Z",
		},
	]


def _lw3_memory_map(upstream: dict[str, Any]) -> dict[str, Any]:
	game_state = copy.deepcopy(upstream["game_state"])
	game_state.update({
		"match": d("Match", 0x04D6, "bcd"),
		"bonus": d("Bonus", 0x142B, "bcd", scale=10000, _notes="Unmultiplied end-of-ball bonus in units of 10,000; zeroed the moment it is paid."),
		"bonusX": d("Bonus X", 0x1429, "int", special_values={"0": 1}),
		"extra_balls": d("Extra Balls", 0x01C5, "int"),
	})
	adjustments = {
		"Standard Adjustments": {
			"_notes": "Keys are the operations manual's menu numbers as read by the contributor (Ad 01 to E Ad 56), not re-checked here.",
			"03": d("Replay Levels", 0x1E16, "int"),
			"04": d("Game Awards", 0x1E17, "int", special_values={"0": "None", "1": "Extra Ball"}, _notes="Any other value awards a credit."),
			"05": d("Limit Freegame", 0x1E18, "int"),
			"06": d("Limit Extra Balls", 0x1E19, "int"),
			"39": d("Tournament Mode", 0x1E53, "bool", _notes="3.01 meaning; on 2.08 this entry is Next Game Promo."),
		},
		"Expanded Adjustments": {
			"15": d("Balls Per Game", 0x1E0D, "bcd"),
			"16": d("Tilt Warnings", 0x1E0E, "int"),
			"42": d("Extra Ball Percentage", 0x1E1A, "int"),
		},
	}
	names = [
		"DRAINS LEFT", "DRAINS CENTER", "DRAINS RIGHT", "EXBALL LIT FROM RAMP", "EXBALL LIT FROM LEO",
		"# OF 2X MADE", "# OF 4X MADE", "# OF 6X MADE", "# OF 8X MADE", "# OF BONUS HOLDS", "LASER KICK USED",
		"# SUPER LEO EXBALL", "FREEZE USED", "TRI-BALL LIT", "TRI-BALL AWARD", "RERACE AWARD", "JACKPOT LIT",
		"1 JACKPOT AWARD", "2 JACKPOT AWARDS", "3 JACKPOT AWARDS", "4 OR MORE JACKPOTS", "RAMP DOUBLE JACKPOT",
		"TIMER DOUBLE JACKPOT", "QUAD JACKPOT", "STUNT 1", "STUNT 2", "STUNT 3", "STUNT 4", "STUNT 5", "SUPER STUNT",
		"SUPER SPINNER READY", "CRAZY RIGGS", "LEO GETZ AWARD", "SUPER LEO GETZ", "GETAWAY AWARD", "LOOPING AWARD",
		"MAX # OF RAMPS", "SUPER LETHAL WEAPON", "MPLUS TO 5M AWARD", "START FIGHT", "LEFT ORBITS", "RIGHT ORBITS",
		"SHOOTOUT VICTORYS", "SHOOTOUT DEFEATS", "SHOOTOUT BONUS", "VIDEO MODE", "VICTORY RAMPS AWARDED",
		"MUSIC 1", "MUSIC 2", "MUSIC 3", "WON FIGHT",
	]
	feature = {"_notes": "Keys are indices into the display ROM's audit-name table (lw3drom1.300, 0x163E9), not menu numbers; address = 0x1D4C + 4 x (index - 58), validated over 0x1D14-0x1DE0 only."}
	for offset, name in enumerate(names):
		index = 44 + offset
		feature[f"{index:02d}"] = d(name, 0x1D4C + 4 * (index - 58), "bcd", length=4)
	return {
		"_notes": [
			"Lethal Weapon 3 [Data East, 1992]: tomlogic's lw3_208 map (version 9) extended by pinmame-game-defs.",
			"game_state and high_scores below come from tomlogic unchanged, except the four game_state keys added here.",
		],
		"_fileformat": upstream["_fileformat"],
		"_metadata": {
			"version": 1,
			"roms": LW3_ROMS,
			"copyright": ["Copyright (C) 2026 by Tom Collins <tom@scorbit.io>", "Copyright (C) 2026 pinmame-game-defs contributors"],
			"license": "Open Data Commons Open Database License (ODbL) v1.0",
			"platform": upstream["_metadata"]["platform"],
		},
		"game_state": game_state,
		"high_scores": copy.deepcopy(upstream["high_scores"]),
		"adjustments": adjustments,
		"audits": {"Feature Audits": feature},
	}


def _lw3_extensions() -> dict[str, Any]:
	commands = load_json(INPUTS / "lethal-weapon-3-1992.sound-commands.json")
	return {
		"addressing": {
			"controller_nvram_index_equals_cpu_address": True,
			"basis": "Data East keeps its 8 KB RAM at CPU 0x0000-0x1FFF and Controller.NVRAM returns it from index 0 (8238 bytes with a trailer); tomlogic's offsets read correctly unshifted and wrong when shifted by 46 (rig, lw3_301).",
		},
		"mode_state": {
			"stunt_rung": d("Stunt rung", 0x140F, "int", min=0, max=6, _notes="Between stunts: stunts completed this ball, next = value + 1 wrapping 6 to 1. During a stunt: the current rung."),
			"lw_latches": {"label": "Lethal Weapon 1/2/3 collect latches", "offsets": ["0x1406", "0x1407", "0x1408"], "encoding": "raw",
				"_notes": "Each byte: 0x80 next, 0x01 collected, 0x00 idle. 0x8F82 arms 0x1407 on the LW1 collect; 0x8FB7 arms 0x1408 on the LW2 collect."},
			"drop_bank_completions": {"label": "Drop-bank completions", "offsets": ["0x1400", "0x1401", "0x1402", "0x1403", "0x1404", "0x1405"], "encoding": "raw",
				"_notes": "Any bank in any order: 1st sets 0x1400+0x1403, 2nd 0x1401+0x1404, 3rd 0x1402+0x1405 and 0x1019."},
			"multiball_gate": d("Multiball gate", 0x1018, "int", _notes="0x81 while multiball runs; entry 0x7A8F needs 0 here and 0x1019 non-zero."),
			"multiball_pending": d("Multiball pending", 0x1019, "int"),
			"multiball_status": d("Multiball status", 0x1420, "int"),
			"jackpots_collected": d("Jackpots this multiball", 0x1421, "int"),
			"replays_this_game": d("Replays this game", 0x1422, "int"),
			"specials_this_game": d("Specials this game", 0x1423, "int"),
			"extra_balls_this_game": d("Extra balls earned this game", 0x1424, "int"),
			"freeway_ramps": d("Freeway ramps made", 0x1426, "bcd"),
			"freeway_next_award_at": d("Ramp count of the next ramp award", 0x10FD, "int"),
			"freeway_next_award_code": d("Code of the next ramp award", 0x10FE, "int"),
			"freeway_extra_ball_target": d("Ramps needed for EXTRA BALL LIT", 0x16F1, "int", _notes="0 when the limit or lamp 40 forbids it. The same source also names 0x16F2; unresolved."),
			"extra_ball_lit": d("EXTRA BALL lit (lamp 40 blink plane)", 0x0024, "bool", mask="0x80"),
			"ball_save_state": d("Start-of-ball save state", 0x01C6, "int", _notes="0x01 armed, 0x09 expired, bit 7 spent; seconds left = 10 - BCD(0x0813) while 0x01."),
			"ball_time": d("Ball time (seconds)", 0x0810, "bcd", length=4),
			"music_track": d("Music track", 0x1409, "int", min=0, max=2),
			"music_select_countdown": d("Music-selection countdown", 0x10FA, "bcd", length=2),
			"leo_award": d("Leo Getz award index", 0x109D, "int", min=0, max=20, _notes="Final about 50 ms after 0x10A4 rises; 0 is real only with the 0x1D24 audit step."),
			"leo_busy": d("Leo Getz award in progress", 0x10A4, "bool"),
			"leo_choice_window": d("Super-wheel choice window", 0x10A1, "int"),
			"leo_choice_left": d("Super-wheel left award", 0x10A2, "int"),
			"leo_choice_right": d("Super-wheel right award", 0x10A3, "int"),
			"balls_per_game_live": d("Balls per game (live)", 0x142E, "int"),
		},
		"replay_levels": [
			d(f"Replay {level + 1}", 0x1668 + 5 * level, "bcd", length=5) for level in range(4)
		],
		"sound_commands": {
			"protocol": {
				"width_bits": 8,
				"stream": "PinMAME sound-command stream (Controller.NewSoundCommands)",
				"latch": "0x3402",
				"notes": [
					"Written at 0x46AD from 0x0184; a byte equal to the last one sent (0x0185) or equal to 0xFF is suppressed.",
					"A routine plays a sound by posting a display record [count, id, parameter, duration]; the command is its parameter.",
				],
			},
			"label_source": "Labels are the Total Recall project's names (mus_, sfx_, voc_, ctl_, sys_; unk_ = never heard in play, _dup = duplicate audio); each note gives that project's evidence grade.",
			"commands": commands,
		},
		"notes": [
			"Uzi clip count, Million Plus count and the Getaway hurry-up value have no RAM byte found; likely task-local (inferred).",
			"0x0183 is a byte staged for the display board; earlier meanings drawn from it were retracted after watching play.",
		],
	}


def _lw3_evidence() -> dict[str, Any]:
	both = [LW3_TOMLOGIC, LW3_RIG]
	ev = {
		"/memory_map/game_state": _ev("observed", ["map"], ["lw3_208"], [LW3_TOMLOGIC], "tomlogic's fields; current_player, current_ball, player_count and credits also read correctly on lw3_301 in the rig."),
		"/memory_map/game_state/match": _ev("observed", ["code", "rig"], ["lw3_301"], [LW3_RIG], "Written at 0xDA78; one rig sighting."),
		"/memory_map/game_state/bonus": _ev("observed", ["prediction"], ["lw3_301"], [LW3_RIG], "Paid = BCD x 10,000 x multiplier, 3 of 3 predictions."),
		"/memory_map/game_state/bonusX": _ev("observed", ["rig"], ["lw3_301"], [LW3_RIG]),
		"/memory_map/game_state/extra_balls": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG]),
		"/memory_map/high_scores": _ev("observed", ["map"], ["lw3_208"], [LW3_TOMLOGIC]),
		"/memory_map/adjustments": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG], "Each byte tied to its menu entry by the code that reads or writes it."),
		"/memory_map/adjustments/Expanded Adjustments/15": _ev("observed", ["code", "map"], ["lw3_208", "lw3_301"], both),
		"/memory_map/adjustments/Standard Adjustments/39": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG], "Tournament Mode exists only in the 3.01 patch.", applies_to=["lw3_301"]),
		"/memory_map/audits": _ev("observed", ["code", "rig", "rom_text"], ["lw3_301"], [LW3_RIG, LW3_ROM301], "Names are the display ROM's; addresses derived and validated over 0x1D14-0x1DE0 by multi-counter routines and a rig run."),
		"/extensions/addressing": _ev("observed", ["rig", "map"], ["lw3_301"], both),
		"/extensions/mode_state": _ev("observed", ["code", "rig"], ["lw3_301"], [LW3_RIG]),
		"/extensions/mode_state/stunt_rung": _ev("observed", ["prediction", "code"], ["lw3_301"], [LW3_RIG], "9 of 9 predictions over 10 cycles."),
		"/extensions/mode_state/replays_this_game": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG], "Supersedes a 5 Sep reading as 'double jackpot armed'."),
		"/extensions/mode_state/specials_this_game": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG]),
		"/extensions/mode_state/extra_balls_this_game": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG]),
		"/extensions/mode_state/freeway_ramps": _ev("observed", ["code", "rig"], ["lw3_301"], [LW3_RIG], "Supersedes a 5 Sep reading as 'jackpot level'."),
		"/extensions/mode_state/freeway_next_award_at": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG], "Table at 0xB0F5; counts against values not checked in the rig."),
		"/extensions/mode_state/freeway_next_award_code": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG]),
		"/extensions/mode_state/freeway_extra_ball_target": _ev("conflicted", ["code"], ["lw3_301"], [LW3_RIG], "Named 0x16F1 and 0x16F2 by one source; the rig image holds 0x23 against the changelog's 17."),
		"/extensions/mode_state/ball_save_state": _ev("observed", ["code", "rig"], ["lw3_301"], [LW3_RIG, LW3_ROM301], "Fan-patch code at 0xFCE1; 2.08 has no such save.", applies_to=["lw3_301"]),
		"/extensions/mode_state/ball_time": _ev("observed", ["code", "rig"], ["lw3_301"], [LW3_RIG], applies_to=["lw3_301"]),
		"/extensions/mode_state/music_select_countdown": _ev("observed", ["code", "rig"], ["lw3_208", "lw3_301"], [LW3_RIG]),
		"/extensions/mode_state/balls_per_game_live": _ev("candidate", ["rig"], ["lw3_301"], [LW3_RIG], "Medium confidence; not varied against the operator menu."),
		"/extensions/replay_levels": _ev("candidate", ["code"], ["lw3_301"], [LW3_RIG], "0xDF60 computes 5i; four levels per the four replay audits."),
		"/extensions/sound_commands": _ev("observed", ["rig", "code"], ["lw3_208", "lw3_301"], [LW3_RIG], "Per-command grade in each note; captures before 5 Sep 2026 are lw3_208."),
		"/extensions/notes": _ev("candidate", ["rig"], ["lw3_301"], [LW3_RIG]),
	}
	return ev


def build_lw3() -> dict[str, Any]:
	upstream = _pinned_input(VENDOR / "lw3_208.map.json")
	return {
		"format": "pinmame-rom-map",
		"schema_version": 1,
		"machine_id": "data-east.lethal-weapon-3.1992",
		"map_id": "lw3_208",
		"roms": LW3_ROMS,
		"license": "ODbL-1.0",
		"memory_map": _lw3_memory_map(upstream),
		"extensions": _lw3_extensions(),
		"evidence": _lw3_evidence(),
		"sources": _lw3_sources(),
	}


# --- Attack From Mars ---------------------------------------------------------------------------------

AFM_ROMS = ["afm_113", "afm_113b"]
AFM_TOMLOGIC = "memory-map.tomlogic.afm-113"
AFM_RIG = "rom-state.afm-113b.wpc-emu-2026-09-05"
AFM_NOTE = "knowledge.attack-from-mars-1995"


def _afm_sources() -> list[dict[str, Any]]:
	return [
		_tomlogic_source(AFM_TOMLOGIC, "maps/williams/wpc/afm_113.map.json", PINNED[VENDOR / "afm_113.map.json"], 5),
		{
			"id": AFM_RIG,
			"kind": "rom_analysis",
			"uri": "pinmame-game-defs-working-dir/review-artifacts/attack-from-mars-rom-state-2026-09-05/MANIFEST.sha256",
			"revision": "2026-09-05",
			"sha256": "1c39954f6de4f2b5be9b7589867ddc31859faa0324ce61da56d829c78f1a7c97",
			"locator": "rammap/afm_adjustments_named.json (transcribed into tools/rom-map-inputs/attack-from-mars-1995.game-adjustments.json), rammap/afm_modes.json (into ...mode-replay.json), rammap/afm_player_block.md, rammap/afm_rules_from_rom.md, rammap/afm_rammap.md, raw game recordings rammap/rec/, VPinMAME polling log rammap/nvram_probe_log_2026-09-05.txt; headless wpc-emu 0.36.7 on afm_113b.zip SHA-256 378102edfd80d650bf6810d5e521fd08cfd972f8732f3c2204f5929d2266358d",
			"license": "contributor evidence, retained outside Git; facts only",
			"attribution": "Attack From Mars ROM-state campaign (Manuel), 5-6 Sep 2026",
			"acquired_at": "2026-09-05T17:33:49Z",
		},
		{
			"id": AFM_NOTE,
			"kind": "knowledge_note",
			"uri": "knowledge/bally/attack-from-mars-1995.md",
			"revision": "0ebe305e7f",
			"sha256": "fcbde8e85d7ea1f79ada1b186e5c044ba93598e4df93445dca0460c0240cd29c",
			"locator": "Controller interactions - DCS sound commands, Opcode reference (586 ids); transcribed into tools/rom-map-inputs/attack-from-mars-1995.dcs-commands.json",
			"license": "MIT (this repository); sample names from the community altsound package for afm_113b",
			"attribution": "pinmame-game-defs contributors",
			"acquired_at": "2026-10-04T13:40:00Z",
		},
	]


def _afm_game_adjustments() -> dict[str, Any]:
	group: dict[str, Any] = {"_notes": "Names, defaults and ranges read from the ROM's own descriptors and menu strings (bank 55 0x67AC, English names bank 28). Keys assume the menu number equals the descriptor index, as standard adjustment 01 does in tomlogic's map; not checked against the manual. Start follows tomlogic's convention (two bytes ending at the value byte)."}
	for entry in load_json(INPUTS / "attack-from-mars-1995.game-adjustments.json"):
		name = entry.get("name")
		if not name:
			continue
		descriptor = d(name, entry["addr"] - 1, "int", length=2, default=entry["default"], min=entry["min"], max=entry["max"])
		if entry.get("kind") == "option":
			descriptor["_notes"] = "Option list in ROM (option pointer " + entry["optptr"] + "); value is the option index."
		if entry["index"] == 0x04:
			descriptor["_notes"] = "Name, default and range from the ROM; its effect was not established, because the ball save never armed in the emulator."
		group[f"{entry['index']:02d}"] = descriptor
	return group


def _afm_memory_map(upstream: dict[str, Any]) -> dict[str, Any]:
	memory_map = copy.deepcopy(upstream)
	memory_map["_notes"] = list(upstream["_notes"]) + ["Extended by pinmame-game-defs: A.2 game adjustments and player_state from the 5 Sep 2026 ROM-state campaign."]
	metadata = memory_map["_metadata"]
	metadata["version"] = 1
	metadata["copyright"] = list(metadata["copyright"]) + ["Copyright (C) 2026 pinmame-game-defs contributors"]
	memory_map["adjustments"]["A.2 Feature Adjustments"] = _afm_game_adjustments()
	memory_map["player_state"] = {
		"_notes": "One block per player: player n at 0x0870 + 0x50 x (n - 1). Fields for player 1.",
		"stride": "0x50",
		"fields": {
			"super_jets_requirement": d("Super Jets requirement", 0x0876, "int"),
			"super_jets_remaining": d("Jet hits remaining", 0x0877, "int"),
			"super_jets_collected": d("Super Jets collected this game", 0x0878, "int"),
			"hurry_up_lanes": {"label": "Hurry-up lane counters (left ramp, right ramp, left orbit, right orbit)", "start": "0x0879", "length": 4, "encoding": "raw"},
			"total_annihilation_started": d("Total Annihilation started", 0x087D, "int"),
			"locks_remaining": d("Locks remaining", 0x087E, "int"),
			"locks_made": d("Locks made", 0x087F, "int"),
			"three_bank_mask": d("3-bank target bitmask", 0x0887, "int"),
			"attack_wave_required": d("Attack-wave hits required", 0x0889, "int"),
			"attack_wave_remaining": d("Attack-wave hits remaining", 0x088A, "int"),
			"attack_wave_value_millions": d("Attack-wave hit value (millions)", 0x088C, "int"),
			"final_wave_counter": d("Final-wave mothership counter", 0x088D, "int"),
			"martian_mask": d("MARTIAN standup bitmask", 0x088E, "int"),
		},
	}
	return memory_map


def _afm_extensions() -> dict[str, Any]:
	replay = load_json(INPUTS / "attack-from-mars-1995.mode-replay.json")
	return {
		"addressing": {
			"controller_nvram_index_equals_cpu_address": True,
			"basis": "PinMAME's WPC-95 NVRAM handler saves wpc_ram from 0x0000 for 0x3000 bytes, so the image index is the CPU address; confirmed live on VPinMAME (847 Controller.NVRAM polls).",
		},
		"mode_state": {
			"game_running": d("Game running", 0x0080, "int"),
			"running_mode_word": {"label": "Running-mode word", "offsets": ["0x0294", "0x0295"], "encoding": "raw", "_notes": "Bit array; stacked modes OR together. See mode_replay.mode_word."},
		},
		"sound_commands": {
			"protocol": {
				"width_bits": 16,
				"stream": "PinMAME sound-command stream, DCS commands as big-endian byte pairs",
				"notes": [
					"Parse against the known-id list; naive byte splitting desynchronizes on the 0x03D2/0x03D3 heartbeat pair.",
					"The current background-music command is re-asserted roughly twice per second during play.",
				],
			},
			"label_source": "sample_name is the community altsound package's; label is a contributor runtime annotation where one exists; class is music or system from the knowledge note's group, else unknown, with the group in note.",
			"commands": load_json(INPUTS / "attack-from-mars-1995.dcs-commands.json"),
		},
		"mode_replay": replay,
	}


def _afm_evidence() -> dict[str, Any]:
	return {
		"/memory_map": _ev("observed", ["map"], ["afm_113"], [AFM_TOMLOGIC], "tomlogic's map unchanged except the two extensions below."),
		"/memory_map/adjustments/A.2 Feature Adjustments": _ev("candidate", ["code", "rom_text"], ["afm_113b"], [AFM_RIG], "Two entries (0x0C, 0x11) were changed in the emulator and behaved as named; the rest rest on the descriptor and string alignment. What 0x04 BALL SAVE TIME does was not established: the save never armed in the emulator."),
		"/memory_map/player_state": _ev("candidate", ["rig", "code"], ["afm_113b"], [AFM_RIG], "Raw game recordings retained (rammap/rec/); Super Jets and attack-wave formulas were prediction-checked."),
		"/extensions/addressing": _ev("observed", ["rig"], ["afm_113b"], [AFM_RIG]),
		"/extensions/mode_state": _ev("candidate", ["rig", "code"], ["afm_113b"], [AFM_RIG]),
		"/extensions/sound_commands": _ev("observed", ["rig"], ["afm_113b"], [AFM_NOTE], "Runtime-verified protocol; per-command annotations are contributor observations."),
		"/extensions/mode_replay": _ev("observed", ["rig", "rom_text"], ["afm_113b"], [AFM_RIG], "Every recipe was replayed against the ROM in wpc-emu and its verification recorded per mode; not run on hardware."),
	}


def build_afm() -> dict[str, Any]:
	upstream = _pinned_input(VENDOR / "afm_113.map.json")
	return {
		"format": "pinmame-rom-map",
		"schema_version": 1,
		"machine_id": "bally.attack-from-mars.1995",
		"map_id": "afm_113",
		"roms": AFM_ROMS,
		"license": "ODbL-1.0",
		"memory_map": _afm_memory_map(upstream),
		"extensions": _afm_extensions(),
		"evidence": _afm_evidence(),
		"sources": _afm_sources(),
	}


ARTIFACTS = {
	ROOT / "rom-maps/data-east/lethal-weapon-3-1992.lw3_208.json": build_lw3,
	ROOT / "rom-maps/bally/attack-from-mars-1995.afm_113.json": build_afm,
}


def _check() -> None:
	_pinned_input(VENDOR / "map.schema.json")
	for name in ("LICENSE-ODbL.md", "LICENSE-DbCL"):
		if _sha256(VENDOR / name) != PINNED[VENDOR / name]:
			raise RuntimeError(f"vendored licence text drifted: {name}")
	for path, builder in ARTIFACTS.items():
		if not path.is_file():
			raise RuntimeError(f"ROM map is missing: {path}")
		if path.read_bytes().replace(b"\r\n", b"\n") != canonical_bytes(builder()):
			raise RuntimeError(f"ROM map does not match the deterministic curator: {path}")
	print(f"{len(ARTIFACTS)} ROM maps match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and rom-maps/.")
	mode.add_argument("--regenerate", action="store_true", help="Write every ROM map.")
	arguments = parser.parse_args()
	if arguments.regenerate:
		for path, builder in ARTIFACTS.items():
			write_bytes(path, canonical_bytes(builder()))
			print(f"Wrote {path.relative_to(ROOT).as_posix()}")
	_check()


if __name__ == "__main__":
	main()
