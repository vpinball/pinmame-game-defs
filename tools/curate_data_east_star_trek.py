"""Curate the production Data East Star Trek definition and placement audit."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from urllib.parse import quote

from build_external_evidence_manifest import build_manifest, check_manifest
from drawing_callouts import apply, fit, leave_one_out
from pinmame_flipper_column import flipper_column_inputs, flipper_column_relationships
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json, write_bytes
from pinmame_game_defs.spatial import _item_point, _item_record, _round_point

ROOT = Path(__file__).resolve().parents[1]
MACHINE = "data-east.star-trek.1991"
SLUG = "star-trek-1991"
DRIVER = "trek_201"
GAME_PATH = Path("data-east") / SLUG
TARGET = ROOT / "machines/partial" / GAME_PATH.with_suffix(".json")
AUTHOR_READY = ROOT / "machines/author-ready" / GAME_PATH.with_suffix(".json")
SEED = ROOT / "tools/seeds" / GAME_PATH.with_suffix(".json")
KNOWLEDGE = ROOT / "knowledge" / GAME_PATH.with_suffix(".md")
REPORT = ROOT / "reports/spatial" / GAME_PATH
EXCERPTS = ROOT / "evidence/excerpts" / MACHINE

REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
PINMAME = "https://github.com/vpinball/pinmame"
CORE = "pinmame.core.46e1a01a"
MANUAL = "manual.data-east.star-trek.operations"
SCHEMATIC = "manual.data-east.star-trek.schematics"
SCRIPT = "vpx-script.data-east.star-trek-0.9"
TABLE = "vpx-table.data-east.star-trek-0.9"
TRACE = "runtime.data-east.trek-201-start"
FIRMWARE = "firmware.data-east.star-trek-3"
DISPLAY = "runtime.data-east.star-trek-display"
RESTORATION = "human.data-east.star-trek-trough-restoration"
REAR_PHOTO = "human.data-east.star-trek-rear-panel"
SLING_PHOTO = "human.data-east.star-trek-sling-blades"
SLING_BOARD = "human.data-east.star-trek-sling-apertures"
SLING_TEXTURE_HASH = "225e94db4553e56a847fccf33a3c7826b37ba74358bde1b9c1c27b1ac1d175d9"
MOTOR_SPECS = "manual.stern.star-trek-motor-specifications"
CHASE_ROM = "rom-static.data-east.star-trek-chase"
PA7_ROM = "rom-static.data-east.star-trek-pia2-pa7"
SWITCH_TEST = "runtime.data-east.star-trek-switch-test"
SCRIPT_CORPUS = "https://github.com/sverrewl/vpxtable_scripts"
SCRIPT_CORPUS_PIN = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

MANUAL_REL = Path("by-machine") / MACHINE
SHORT = MANUAL_REL / "arcade-museum-14943/Star_Trek_25th_Anniversary_OPS.pdf"
FULL = MANUAL_REL / "ipdb-2356/Data_East_1991_Star_Trek_English_Manual_with_schematics.pdf"
SHORT_HASH = "07d596a91c75428828fa0c6d42538c4c42d377c86f701018662e3d1ea24a7f57"
FULL_HASH = "14e13f5ab13e5b655c6251f2665b64458bcda485541f5956c17d4a88430fb45d"
VPX = GAME_PATH / "source/Star Trek 25th Anniversary (Data East 1991).vpx"
EXTRACTION = GAME_PATH / "analysis/vpxtool-extract"
VPX_HASH = "77d1617960b6e64b70aa857ddbecf2accd90dfff2b2b5201f92b784d29e9a9e2"
SCRIPT_HASH = "f4b31a47a4178e27b4339f4ed41eb1a34e17dfc820a545280327b5c258dd7214"
EXTRACTION_HASH = "a9386211097848f6209459ace82afd4a4a9a4434f6a296f24f4860ce7d5f8785"
TRACE_REL = Path("data-east-star-trek-1991/runtime-trek-201-start/play-start.json")
TRACE_HASH = "765fed1f3a41323a79ce8d05241da5a65e360a415155fc18277cb660320de805"
TRACE_MANIFEST_HASH = "3a7cb820c31f3ae9a8e9ac9e73323bbdc432c1a4be9bd8e3e1b89b220bc6df40"
SCENARIO = ROOT / "tools/harness-scenarios/data-east/trek-201-start.json"
SCENARIO_HASH = "37e3420ffcf58e72e701ed42eddc7ccdd8dd240fab2d9ec1f01e3d0581b60f3b"
RAW_SCENARIO_HASH = "7ca99f09aaf545005b022b83366ef4bb12b78278fe98b672700d618065c0754c"
DISPLAY_REL = Path("data-east-star-trek-1991/display-probe-20261120/manifest.json")
DISPLAY_HASH = "9894903330ba805b068e9069e100ad03e348653bfcff10069954ffafbe16771b"
RESTORATION_URL = "https://www.enteryourinitials.com/2019/04/23/star-trek-25th-anniversary-repair-service-log-1/"
MOTOR_REL = Path("data-east-star-trek-1991/followup/stern-csi-motor-specs.pdf")
MOTOR_HASH = "bf918873d582f4fbd152db777b8ecef66c77692a88e6ddaf3ce99409e396055e"
CHASE_REL = Path("data-east-star-trek-1991/followup/chase-verification.json")
CHASE_HASH = "c529f2389cd95523622d77685ddab11feff227463e83b2fdd17f4051c283448d"
PA7_REL = Path("data-east-star-trek-1991/follow-up-inputs/pia2-summary.json")
PA7_HASH = "ca0d869311abd720e26d092ae4be0cc82bad47ca138e95e3fa0a7f384b3275cf"
SWITCH_TEST_REL = Path("data-east-star-trek-1991/follow-up-inputs/switch-test-evidence/manifest.json")
SWITCH_TEST_HASH = "c88f4ab0e6dbc6b00e0fc049329a846fc1a4f7cc8dabf7ada0b9fa5368a7d500"
SWITCH_TEST_SCENARIO = ROOT / "tools/harness-scenarios/data-east/trek-201-switch-test.json"
SWITCH_TEST_SCENARIO_HASH = "bbd7d0e576ef9cd07dafc82ecd4e3fd9f0935757491786df19070e6b513f4b90"
MUSEUM = "https://www.arcade-museum.com/Pinball/star-trek--data"
IPDB = "https://www.ipdb.org/machine.cgi?id=2356"
IPDB_MANUAL = "https://www.ipdb.org/files/2356/" + FULL.name
ARCHIVED_MANUAL = "https://web.archive.org/web/20220705145241id_/" + IPDB_MANUAL
BOUNDS = (0, 0, 952, 2162)
FLIP_SWNO = (15, 16)
WIRING_KEYS = ("drive_wire", "drive_connection", "driver_transistor",
               "return_wire", "return_connection", "return_component")
DRAWING_CROPS = {
	"switch-locations": "page 6, crop box 0.12,0.264,0.455,0.8, scanned page rendered at its native resolution (embedded image xref 25, 2544px across 8.48in), rendered at 227 dpi, capped to 645px wide, grayscale, 646x1419 WebP quality 65",
	"lamp-locations": "page 8, crop box 0.138,0.347,0.473,0.847, scanned page rendered at its native resolution (embedded image xref 35, 2544px across 8.48in), rendered at 239 dpi, capped to 680px wide, grayscale, 681x1395 WebP quality 66",
	"flasher-locations": "page 9, crop box 0.112,0.406,0.419,0.863, scanned page rendered at its native resolution (embedded image xref 40, 2544px across 8.48in), rendered at 248 dpi, capped to 645px wide, grayscale, 646x1320 WebP quality 65",
}
J8_CROP = f"{FULL.name} page 56, crop box 0.582,0.217,0.786,0.311, scanned page rendered at its native resolution (embedded image xref 186, 3328px across 11.10in), rendered at 300 dpi, grayscale, rotated 90 degrees counter-clockwise, 480x674 WebP quality 73; tools/render_excerpt_image.py"
BULLETINS = (
	(31, "b/b4", "d8fc29dc0147137ebf903f88f438807781ea4a7238a08a67e64a0299ba3e81e9", "10:18:03", "PDF p. 1, game 1.17 and display 1.09"),
	(32, "f/fa", "3fae08f6cddac0a14a30acd987682b9acab2a306711b2e21f87a104b27fb5a2e", "10:18:01", "PDF p. 1, ramp latch and Ramp Up switch"),
	(33, "e/ea", "937601b4bc45c609b34089cc1d97b4c66945bc3c135fb70aeff12022dd3f1559", "10:18:00", "PDF pp. 2–13, transporter F/X theory, assembly and adjustment"),
	(34, "0/09", "f3bd49208cec496b97abf4152ec2df746975f7424b047baea2e378353ebf10ac", "10:17:59", "PDF p. 1, chase light assembly and insulation revision"),
	(35, "9/9a", "e215e8851b32fb42654548a9bd44a161f7987bd0d3dfb27e3802598fa0537c0b", "10:17:58", "PDF p. 1, game 2.00, ball search and PPB relay"),
)


def bulletin_id(number):
	return f"bulletin.data-east.star-trek-{number}"

CABINET_SWITCHES = {1, 3, 4, 5, 6, 7, 30, 31, 32}
CABINET_LAMPS = {8, 15, 22, 29, 30, 31, 36}
REAR_LAMPS = {44: "Left Ramp Green", 45: "Left Million Red", 63: "Right Million Red", 64: "Right Ramp Green"}
SWITCH_LABELS = {
	3: "Start Button", 11: "Left Trough", 12: "Center Trough", 13: "Right Trough",
	18: "Left Return Lane", 20: "Left Bottom Drop Target", 21: "Left Drop Target 2",
	22: "Left Drop Target 3", 23: "Left Top Drop Target", 24: "Left Stand-Up Target",
	26: "Right Stand-Up Target", 30: "Ball Launch Button", 31: "Transporter Crew Visible",
	32: "Transporter Crew Gone", 39: "Transporter Ramp Up Limit", 40: "Right VUK",
	44: "Right Top Drop Target", 45: "Right Drop Target 2", 46: "Right Drop Target 3",
	47: "Right Bottom Drop Target", 50: "Right Return Lane",
}
COILS = {
	1: ("Outhole Kicker", "coil", "23-840"),
	2: ("Trough Eject", "coil", "23-840"),
	3: ("Turbo Ball Launch", "coil", "090-5023-00"),
	4: ("Left Drop Target Reset", "coil", "23-800"),
	5: ("Transporter Ramp Raise", "coil", "23-840"),
	6: ("Transporter Ramp Lower", "coil", "31-1800"),
	7: ("Right Drop Target Reset", "coil", "23-800"),
	8: ("Knocker", "coil", "090-5001-01"),
	9: ("Flasher Circuit 09", "flasher", None),
	10: ("Left Right Coil Select", "relay", None),
	11: ("General Illumination", "gi", None),
	12: ("Flasher Circuit 12", "flasher", None),
	13: ("Backbox Transporter Motor", "motor", "515-5532-00-14"),
	14: ("Right VUK Eject", "coil", None),
	15: ("Laser Kickback", "coil", "090-5001-01"),
	16: ("Swinging Target Motor", "motor", "515-5534-00"),
	17: ("Left Turbo Bumper", "coil", "23-800"),
	18: ("Center Turbo Bumper", "coil", "23-800"),
	19: ("Right Turbo Bumper", "coil", "23-800"),
	20: ("Left Slingshot", "coil", "23-800"),
	21: ("Right Slingshot", "coil", "23-800"),
	22: ("Upper Ramp Gate Lift", "coil", "31-1800"),
}
FLASH_LOCATIONS = {
	9: "Three playfield bulbs and one backbox insert-panel bulb",
	12: "Two playfield bulbs and two rear playfield back-panel bulbs",
	25: "Four playfield bulbs",
	26: "Two ramp bulbs and two backbox insert-panel bulbs",
	27: "Two playfield bulbs and two backbox insert-panel bulbs",
	28: "Two playfield bulbs and two backbox insert-panel bulbs",
	29: "Two ramp bulbs and two backbox insert-panel bulbs",
	30: "Two ramp bulbs and two backbox insert-panel bulbs",
	31: "One playfield bulb and three backbox insert-panel bulbs",
	32: "One playfield bulb and three backbox insert-panel bulbs",
}
FLASH_BACKBOX = {9: 1, 12: 0, 25: 0, 26: 2, 27: 2, 28: 2, 29: 2, 30: 2, 31: 3, 32: 3}
BACKBOX_5_CONFLICT = {
	"id": "lamp36-additional-playfield-load",
	"path": "outputs.lamp.backbox-5.spatial",
	"status": "unresolved",
	"description": (
		"Printed p. 27 draws lamp 36 in both the backbox inset and the upper-left playfield. "
		"Its list and printed p. 49 identify a backbox lamp. The retained VPX uses lamp 36 for a "
		"playfield red cover and glow. The documented backbox lamp is retained. Fitment and quantity "
		"of any playfield sockets on this circuit remain unresolved. Resolution path: have an owner or "
		"restorer run the discrete lamp 36 test and trace the circuit at both the backbox and "
		"the lower end of the upper-left Transporter assembly."
	),
	"source_refs": [MANUAL, SCHEMATIC, SCRIPT],
}
DEVICE_NOTES = {
	3: "The printed p. 39 parts illustration gives 090-5023-00 (22-600). The printed p. 29 PPB diagram calls the load 22-800.",
	9: "Printed schematic: one INSERT, three PLFD.",
	10: "PPB relay selects the B flasher branches on the shared drivers 1–8. PinMAME publishes those branches as 25–32.",
	11: "Power-supply K-1 is normally on: public 1 drops the switched G.I. feed. The VPX GI collection approximates playfield illumination.",
	13: "CPU Q26 energizes the relay that switches the 28 VAC feed to the backbox motor. The cam closes switch 31 or 32 at the two optical endpoints.",
	14: "Manual calls this coil TRANSPORTER LAUNCH. It serves the right-side vertical up-kicker.",
	16: "CPU Q23 switches the 28 VAC feed to the separate swinging-target motor through a relay.",
	22: "Manual auxiliary table: Gate (See Schematic). The VPX opens s22 from this output.",
}
AUX_WIRES = ("BLU-ORN", "BLU-RED", "BLU-YEL", "BLU-BRN", "BLU-GRN", "BLU-BLK")
AUX_PINS = (3, 4, 6, 7, 8, 9)
PAIR_COLORS = ("BRN", "RED", "ORN", "YEL", "GRN", "BLU", "VIO", "BLK")


def prov(status, *sources):
	return {"status": status, "source_refs": list(sources)}


def no_position(reason, *sources):
	return {"status": "not_applicable", "reason": reason, "provenance": prov("validated", *sources)}


def slug(label):
	return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def rows(path):
	with path.open(encoding="utf-8", newline="") as stream:
		return list(csv.DictReader(stream, delimiter="\t"))


def matrix_rows(stem):
	result = rows(EXCERPTS / (stem + ".tsv"))
	if [int(row["number"]) for row in result] != list(range(1, 65)):
		raise ValueError(f"Expected exactly 64 sequential cells in {stem}")
	return result


def source_excerpt(stem, locator):
	suffix = ".tsv" if stem in {"switch-matrix", "switch-parts", "lamp-matrix"} else ".md"
	path = EXCERPTS / (stem + suffix)
	excerpt = {
		"id": "excerpt.star-trek-data-east." + stem, "locator": locator,
		"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path),
		"method": "manual", "transcribed_by": "Curation session", "reviewed": True,
	}
	if stem in DRAWING_CROPS:
		crop = path.with_suffix(".webp")
		excerpt.update(image=crop.relative_to(ROOT).as_posix(), image_sha256=file_sha256(crop),
		               image_derivation=f"{SHORT.name} {DRAWING_CROPS[stem]}; tools/render_excerpt_image.py")
	if stem == "cpu-j8-wiring":
		crop = path.with_suffix(".webp")
		excerpt.update(image=crop.relative_to(ROOT).as_posix(), image_sha256=file_sha256(crop),
		               image_derivation=J8_CROP)
	return excerpt


def bulletin_sources():
	for number, directory, digest, timestamp, locator in BULLETINS:
		filename = f"Sb{number}.pdf"
		excerpt = source_excerpt("factory-bulletins", f"SB{number} section, {locator}")
		excerpt.update(id=f"{excerpt['id']}-{number}", method="mixed")
		yield {
			"id": bulletin_id(number), "kind": "service_bulletin",
			"uri": f"https://www.pinwiki.com/wiki/images/{directory}/{filename}",
			"source_id": f"{MACHINE}.service-bulletin-{number}.{digest[:12]}",
			"original_filename": filename, "sha256": digest,
			"license": "NOASSERTION", "attribution": "Data East Pinball Service Department, scan hosted by PinWiki",
			"acquired_at": f"2026-11-20T{timestamp}Z", "locator": locator, "excerpts": [excerpt],
		}


def sources(photos):
	attribution = "32assassin, with JPSalas, Grizz, Hassanchop, Bord and cyberpez credited in VPX table information"
	rear_photo = next(photo for photo in photos if photo["retained"].endswith("/pf_ST-Playfield-01.jpg"))
	corpus_scripts = [
		("3.00", "Star Trek 25th Anniversary (Data East 1991).vbs",
		 "b77b57926bf71470bc41020919ffcb49baca8521a3b95edee7f9415ab1d03c83", 40),
		("2.01", "Star Trek 25th Anniversary (Data East 1991)1.2.1.vbs",
		 "67c7f80cb3f4413dee00e16c0d9301f67746fd5716f676e727e60f38c9665926", 42),
	]
	return [
		{"id": CORE, "kind": "pinmame_core", "uri": PINMAME, "revision": REVISION,
		 "license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		 "locator": "src/wpc/degames.c:544–635 (trekGameData, clone and ROM declarations); src/wpc/s11.c (pia2a_r, pia2b_w, setSSSol, updsol, pia4a_r, trek_ PWM typing); src/wpc/s11.h:9–77 (S11_COMPORTS, DE_COMPORTS); src/wpc/core.c (core_getDip, core_nvram and I/O conversions); src/machine/6821pia.c:297–346 (port-A input and direction mask); src/wpc/dedmd.c:371–595 (display board 520-5042-00 model)"},
		{"id": MANUAL, "kind": "manual", "uri": "https://www.arcade-museum.com/manuals-pinball/S/" + SHORT.name,
		 "source_id": "arcade-museum.14943", "original_filename": SHORT.name, "sha256": SHORT_HASH,
		 "license": "NOASSERTION", "attribution": "Data East USA, Inc.; scan hosted by the Museum of the Game",
		 "acquired_at": "2026-11-20T08:31:15Z",
		 "locator": "Operations manual 780-5014-00 selection, PDF pp. 2–13, 20–21",
		 "excerpts": [source_excerpt(name, locator) for name, locator in (
			("switch-matrix", "PDF p. 5, printed p. 24, Switch Matrix Chart"),
			("switch-parts", "PDF p. 6, printed p. 25, Switch Part Numbers"),
			("switch-locations", "PDF p. 6, printed p. 25, Switch Locations"),
			("lamp-matrix", "PDF p. 7, printed p. 26, Lamp Matrix Chart"),
			("lamp-locations", "PDF p. 8, printed p. 27, Lamp Locations"),
			("flasher-locations", "PDF p. 9, printed p. 28, playfield and backbox bulb diagrams"),
			("solenoid-wiring", "PDF pp. 9–10, printed pp. 28–29, auxiliary, flipper and PPB circuits"),
		 )]},
		{"id": SCHEMATIC, "kind": "manual", "uri": ARCHIVED_MANUAL, "source_id": "ipdb.2356",
		 "original_filename": FULL.name, "sha256": FULL_HASH, "license": "NOASSERTION",
		 "attribution": "Data East USA, Inc.; IPDB 2356, Wayback capture 20220705145241",
		 "acquired_at": "2026-11-20T08:36:56Z",
		 "locator": f"{IPDB}; original resource {IPDB_MANUAL}; PDF pp. 2, 27, 36, 43, 45–47, 49–50, 52–53, 56, 70",
		 "excerpts": [
			source_excerpt("cabinet-and-motor", "PDF pp. 27, 43, 46, 49, 52–53"),
			source_excerpt("cpu-j8-wiring", "PDF p. 2 CPU Jumper Table and p. 56, printed p. 52, CPU logic sheet 2"),
		 ]},
		*bulletin_sources(),
		{"id": DISPLAY, "kind": "runtime_scenario",
		 "uri": "external:pinmame-review-artifacts/" + DISPLAY_REL.as_posix(),
		 "sha256": DISPLAY_HASH, "revision": REVISION, "acquired_at": "2026-11-20T10:25:42Z",
		 "locator": "trek_11a and trek_110 A0.27/A1.06 ROM identity, boot and graphical attract frames; discrete lamp labels in the four distinct display ROMs",
		 "excerpts": [
			source_excerpt("display-firmware-comparison", "Retained ROM comparison and visually checked DMD frames; manual PDF pp. 27, 36, 47"),
			source_excerpt("rear-lamp-diagnostics", "DMD diagnostic lamp-name tables, lamp 36 and rear panel"),
		 ]},
		{"id": REAR_PHOTO, "kind": "human_review", "uri": rear_photo["resource"],
		 "sha256": rear_photo["sha256"], "license": "NOASSERTION",
		 "attribution": "Pinside archive gallery", "acquired_at": "2026-11-20T08:35:52Z",
		 "locator": rear_photo["page"] + ", pf_ST-Playfield-01.jpg, rear RAMP and MILLION lenses",
		 "excerpts": [source_excerpt("rear-lamp-diagnostics", "Photograph and factory location drawing, rear-panel lens order")]},
		*[
			{"id": photo["source_id"], "kind": "human_review", "uri": photo["resource"],
			 "sha256": photo["sha256"], "license": "NOASSERTION", "attribution": photo["attribution"],
			 "acquired_at": photo["acquired_at"],
			 "locator": (f"{photo['page']} (Pinside image 4351). {photo['role']}"
			             if photo["source_id"] == SLING_PHOTO else photo["role"]),
			 "excerpts": [source_excerpt("sling-apertures", "Installed blade and bare-board aperture identification")]}
			for photo in photos if photo.get("source_id") in (SLING_PHOTO, SLING_BOARD)
		],
		{"id": RESTORATION, "kind": "human_review", "uri": RESTORATION_URL,
		 "sha256": "7bd62ee30b8c60a38ba6587e868fa02c5883a5495be61298d382f51105e46f92",
		 "license": "NOASSERTION", "attribution": "Andrew Burch",
		 "acquired_at": "2026-11-20T10:21:42Z",
		 "locator": "Repair and service log 1, apron and trough photographs",
		 "excerpts": [source_excerpt("restoration-trough-photos", "Five original photographs and bounds of usable spatial evidence")]},
		{"id": MOTOR_SPECS, "kind": "manual", "uri": "https://www.sternpinball.com/wp-content/uploads/2018/11/CSIManual.pdf",
		 "sha256": MOTOR_HASH, "original_filename": "CSIManual.pdf",
		 "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.",
		 "acquired_at": "2026-11-20T10:27:59Z", "locator": "PDF p. 69, Appendix F:1, Motor Specifications",
		 "excerpts": [source_excerpt("motor-specifications", "Complete motor specification table, including Star Trek 25th Anniversary")]},
		{"id": CHASE_ROM, "kind": "rom_static_analysis", "uri": "external:pinmame-review-artifacts/" + CHASE_REL.as_posix(),
		 "sha256": CHASE_HASH, "revision": REVISION, "acquired_at": "2026-11-20T10:30:01Z",
		 "locator": "Seven distinct Star Trek CPUs, chase pattern tables, startup and service stores; cross-checked with PCB 520-5054-00 revision A, factory PDF p. 70",
		 "excerpts": [source_excerpt("chase-rom", "Decoded pattern arrays, write contexts and transcribed chaser PCB connections")]},
		{"id": PA7_ROM, "kind": "rom_static_analysis", "uri": "external:pinmame-review-artifacts/" + PA7_REL.as_posix(),
		 "sha256": PA7_HASH, "revision": REVISION, "acquired_at": "2026-11-20T10:35:22Z",
		 "locator": "Seven distinct Star Trek CPUs, reset and periodic PIA2 initialization, IRQ acknowledgment and fatal blink; direct-flow and indexed-pointer scope",
		 "excerpts": [source_excerpt("pia2-pa7", "PIA2 port A direction and explicit reads in all seven CPU programs")]},
		{"id": SWITCH_TEST, "kind": "runtime_scenario", "uri": "external:pinmame-review-artifacts/" + SWITCH_TEST_REL.as_posix(),
		 "sha256": SWITCH_TEST_HASH, "revision": REVISION, "acquired_at": "2026-11-20T10:36:01Z",
		 "locator": "Production 2.01 Switch Test, public 18, 28 and 52, separate trials with bank 0 set to 0 and 1",
		 "excerpts": [source_excerpt("upper-left-switch-test", "DMD labels and pixel digests, wiring and VPX pulse timing")]},
		{"id": SCRIPT, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/" + (EXTRACTION / "script.vbs").as_posix(),
		 "sha256": SCRIPT_HASH, "revision": "vpxtool git:v0.33.3", "license": "NOASSERTION",
		 "attribution": attribution, "acquired_at": "2026-11-20T08:29:05Z",
		 "locator": "Embedded script lines 9, 29–145, 184–253, 259–437, 452–633",
		 "excerpts": [source_excerpt("vpx-io", "Embedded v0.9 script, controller and lamp handlers")]},
		{"id": TABLE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/" + VPX.as_posix(),
		 "sha256": VPX_HASH, "revision": "VPX 0.9; vpxtool git:v0.33.3", "license": "NOASSERTION",
		 "attribution": attribution, "acquired_at": "2026-11-20T08:29:05Z",
		 "locator": "Original from the local Tables Archive; gamedata.json bounds and script-selected gameitems; extraction manifest " + EXTRACTION_HASH},
		{"id": TRACE, "kind": "runtime_scenario", "uri": "external:pinmame-review-artifacts/" + TRACE_REL.as_posix(),
		 "sha256": TRACE_HASH, "revision": REVISION, "acquired_at": "2026-11-20T08:33:46Z",
		 "locator": f"trek_201 clean boot and play; steps 4–9, raw scenario SHA-256 {RAW_SCENARIO_HASH}, manifest SHA-256 {TRACE_MANIFEST_HASH}. The repository scenario copy normalizes the final newline.",
		 "excerpts": [source_excerpt("trek-201-start", "Raw trace start, launch and drain steps")]},
		{"id": FIRMWARE, "kind": "human_review", "uri": "https://www.pinballcode.com/trek300",
		 "sha256": "c8403d11b515d0bd8977fc8f717b7c7531715c909ee1a88201aa66ef3759bfe1",
		 "license": "NOASSERTION", "attribution": "Chad at PinballCode",
		 "acquired_at": "2026-11-20T08:49:58Z", "locator": "TREK300 installation and 3.00 / 3.01 release notes",
		 "excerpts": [source_excerpt("firmware-updates", "Declared production-cabinet updates and behavioral changes")]},
		*[
			{"id": "vpx-script.data-east.star-trek-corpus-" + version, "kind": "vpx_script",
			 "uri": f"{SCRIPT_CORPUS}/blob/{SCRIPT_CORPUS_PIN}/{quote(name)}", "revision": SCRIPT_CORPUS_PIN,
			 "sha256": digest, "license": "NOASSERTION", "attribution": "Community script authors and corpus contributors",
			 "locator": f"{name}:{line}; driver declaration; contextual comparison only"}
			for version, name, digest, line in corpus_scripts
		],
	]


def device(group, address, label, kind, availability, *source_refs, identifier=None):
	prefix = group.split(".")[-1]
	return {
		"id": identifier or f"{prefix}.{slug(label)}", "binding": {"group": group, "device": address},
		"aliases": [{"namespace": "pinmame." + prefix, "value": str(address)}],
		"label": label, "kind": kind, "availability": availability,
		"provenance": prov("validated" if availability != "unknown" else "observed", *source_refs),
	}


def matrix_wiring(row):
	return {key: row[key].replace("- ", "-") for key in WIRING_KEYS if row[key] != "[not printed]"}


def inputs():
	result = {}
	part_rows = rows(EXCERPTS / "switch-parts.tsv")
	parts = {int(row["number"].rstrip("*")): row["part_number"] for row in part_rows}
	group = "pinmame.input.switch"
	for row in matrix_rows("switch-matrix"):
		address = int(row["number"])
		unused = row["label"] == "Not Used"
		copy = address in (15, 16)
		label = f"Unused switch {address}" if unused else SWITCH_LABELS.get(address, row["label"])
		if copy:
			label = ("Left" if address == 15 else "Right") + " Flipper Button (matrix copy)"
		record = device(group, address, label, "virtual" if unused or copy else "switch",
		                "unused" if unused else "used", MANUAL, SCHEMATIC, CORE)
		record["aliases"] += [
			{"namespace": "pinmame.switch", "value": f"{address:03d}"},
			{"namespace": "manual.address", "value": str(address)},
		]
		if address < 10:
			record["aliases"].append({"namespace": "pinmame.switch", "value": f"{address:02d}"})
		if unused or copy:
			record["spatial"] = no_position("unused" if unused else "virtual", MANUAL, CORE)
			if copy:
				origin = 84 if address == 15 else 82
				record["physical"] = {"notes": f"PinMAME fills this address from public switch {origin}. The parts list identifies the cabinet contact."}
		else:
			record["wiring"] = matrix_wiring(row)
			record["normally_closed"] = False
			physical = record["physical"] = {"location": "Playfield"}
			if parts[address] != "See Cabinet":
				physical["part_number"] = parts[address]
			if address in (19, 51):
				physical["quantity"] = 2
			if address in CABINET_SWITCHES:
				physical["location"] = "Backbox" if address in (31, 32) else "Cabinet"
				record["spatial"] = no_position("cabinet_or_service", MANUAL, SCHEMATIC)
			if address in (11, 12, 13, 31):
				record["initial_active"] = True
			if address in (28, 52):
				physical["notes"] = (
					f"The 2.01 Switch Test prints UPPER LEFT HOLE at #{address} with this contact's wire pair. "
					"The factory identifies the two contacts as Top (28) and Bottom (52). "
					"The physical passage order and timing remain unmeasured."
				)
				record["provenance"]["source_refs"].append(SWITCH_TEST)
		result[address] = record
	for address, label in ((-7, "Black Step"), (-6, "Green Forward Reverse")):
		record = device(group, address, label, "switch", "used", CORE, SCHEMATIC)
		record["normally_closed"] = False
		record["spatial"] = no_position("cabinet_or_service", CORE, SCHEMATIC)
		record["physical"] = {"location": "Coin door"}
		if address == -6:
			record["physical"]["notes"] = "Maintained selector. Closed in Reverse."
		result[address] = record
	flippers = flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP1516 = FLIP_SWNO(15,16)",
		core_refs=(CORE,), button_refs=(MANUAL, SCHEMATIC),
		button_notes={side: f"The factory cabinet wiring diagram shows the normally open {side} button."
		              for side in ("left", "right")},
		button_normally_closed=False,
	)
	for record in flippers:
		address = record["binding"]["device"]
		if record["availability"] == "used":
			record["physical"]["part_number"] = "180-5067-00"
		result[address] = record
	dip = device("pinmame.input.dip", 0, "CPU PA7 Jumper J8", "dip_switch", "used",
	             SCHEMATIC, CORE, PA7_ROM, SWITCH_TEST,
	             identifier="dip.inherited-pia-configuration-bit")
	dip["physical"] = {
		"location": "CPU board, backbox", "switch_type": "other",
		"notes": "The factory jumper table specifies J8 installed. This grounds PIA 11B PA7 against its RA19-9 pull-up. "
		         "PinMAME supplies PA7 from DIP bank 0 bit 0, with the fresh-state default 0 corresponding to "
		         "installed and 1 to removed. All seven checked CPUs configure PA as output on boot and during "
		         "periodic initialization. The two reviewed reads acknowledge an interrupt or blink PA4 in the "
		         "fatal loop. Both 2.01 switch-test runs gave the same readings with host values 0 and 1. "
		         "The alternate physical jumper position has no documented operator function.",
	}
	dip["initial_active"] = False
	dip["spatial"] = no_position("dip_switch", CORE, SCHEMATIC)
	return [result[address] for address in sorted(result)] + [dip]


def solenoids():
	result = {}
	for address, (label, kind, part) in COILS.items():
		record = device("pinmame.output.solenoid", address, label, kind, "used", MANUAL, CORE,
		                identifier=f"{kind}.{slug(label)}")
		record["aliases"].append({"namespace": "manual.address", "value": str(address)})
		physical = record["physical"] = {}
		if part:
			physical["part_number"] = part
		if address in DEVICE_NOTES:
			physical["notes"] = DEVICE_NOTES[address]
		if address == 8:
			physical.update(location="Cabinet or backbox", assembly_part_number="500-5081-00")
			record["spatial"] = no_position("cabinet_or_service", MANUAL, SCHEMATIC)
		elif address in (10, 13):
			physical["location"] = "Backbox"
			record["spatial"] = no_position("cabinet_or_service", MANUAL, SCHEMATIC)
		elif address in (9, 12):
			physical.update(location=FLASH_LOCATIONS[address], quantity=4)
		elif address == 11:
			physical["location"] = "General illumination on the K-1 controlled feed"
		else:
			physical["location"] = "Playfield"
		if address in (3, 8, 15):
			record["provenance"] = prov("validated", MANUAL, SCHEMATIC, CORE)
		if address == 10:
			record["physical"]["notes"] = (
				"Selects the shared coil or flasher branch. Factory SB35 documents that pitted normally closed "
				"contacts can stick, firing the knocker or shooter-lane kicker in place of the intended flashers. "
				"CPU 2.00 changes relay control to reduce arcing."
			)
			record["provenance"]["source_refs"].append(bulletin_id(35))
		if address <= 8:
			slot = address - 1
			high_voltage = address in (3, 6, 8)
			record["wiring"] = paired_driver(slot)
			record["wiring"].update(
				return_wire=("VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU",
				             "VIO-BLK", "VIO-GRY")[slot],
				power_wire="YEL-VIO" if high_voltage else "BRN",
				nominal_voltage_v=50 if high_voltage else 32, voltage_type="dc",
			)
		if 17 <= address <= 22:
			slot = address - 17
			record["wiring"] = {
				"board": "CPU", "driver_transistor": f"Q{8 + slot}",
				"control_wire": AUX_WIRES[slot], "control_connection": f"CPU CN19-{AUX_PINS[slot]}",
				"power_wire": "RED", "power_connection": "PS CN3-6",
			}
		if 9 <= address <= 16:
			record["wiring"] = {
				"board": "CPU", "driver_transistor": f"Q{39 - address}",
				"control_wire": ("BRN-BLK", "BLK-RED", "BRN-ORN", "BRN-YEL", "BRN-GRN",
				                 "WHT-BLU", "WHT-VIO", "BRN-GRY")[address - 9],
				"control_connection": f"CPU CN12-{(1, 2, 4, 5, 6, 7, 8, 9)[address - 9]}",
			}
		result[address] = record
	for address in range(25, 33):
		branch = address - 24
		label = f"Flasher Circuit {branch}B"
		record = device("pinmame.output.solenoid", address, label, "flasher", "used", MANUAL, CORE,
		                identifier=f"flasher.circuit-{branch}b")
		record["aliases"].append({"namespace": "manual.address", "value": f"{branch}B"})
		record["physical"] = {"quantity": 4, "location": FLASH_LOCATIONS[address]}
		slot = branch - 1
		record["wiring"] = paired_driver(slot)
		record["wiring"].update(
			return_wire="BLK-" + ("GRY" if branch == 8 else PAIR_COLORS[slot]),
			return_connection=f"PPB J2-{(9, 8, 7, 6, 5, 4, 2, 1)[slot]}",
			power_wire="ORN", power_connection="PPB J6-4/5", nominal_voltage_v=32, voltage_type="dc",
		)
		result[address] = record
	for address in (23, 24, 33, 34, 35, 36, *range(37, 51)):
		labels = {
			23: "Flipper and Special Solenoid Enable", 45: "Right Flipper Power Mirror",
			46: "Right Flipper", 47: "Left Flipper Power Mirror", 48: "Left Flipper",
		}
		availability = "unused"
		if address in labels:
			availability = "used"
		elif 37 <= address <= 39:
			labels[address] = f"Chase Line {address - 36} (PIA source)"
			availability = "used"
		elif 40 <= address <= 44:
			labels[address] = f"Auxiliary PIA Line {address}"
		record = device("pinmame.output.solenoid", address, labels.get(address, f"Unused output {address}"),
		                "virtual", availability, CORE, identifier=f"solenoid.{slug(labels.get(address, f'unused-{address}'))}")
		if address in (46, 48):
			record["kind"] = "coil"
			record["provenance"] = prov("validated", CORE, MANUAL, SCRIPT)
			record["physical"] = {
				"part_number": "23-1100", "location": "Playfield",
				"notes": "The public state is synthetic. The factory flipper board drives the physical coil.",
			}
		else:
			record["spatial"] = no_position("unused" if availability == "unused" else "virtual", CORE)
		if 40 <= address <= 44:
			record.update(
				physical={"notes": (
					"The chaser board has three inputs, assigned to public 37–39. The identified animation and "
					"service paths write only those three bits. DDR initialization with a zero latch can briefly "
					"publish 40–44 because PinMAME inverts Port B. This transition has no chaser load."
				)},
				provenance=prov("validated", CORE, SCHEMATIC, CHASE_ROM),
				spatial=no_position("unused", CORE, SCHEMATIC, CHASE_ROM),
			)
		result[address] = record
	for address in range(51, 54):
		line = address - 50
		record = device("pinmame.output.solenoid", address, f"Ramp Chase Lights Phase {line}", "lamp", "used",
		                CORE, MANUAL, SCHEMATIC, TRACE, CHASE_ROM, bulletin_id(34), identifier=f"lamp.ramp-chase-phase-{line}")
		record["physical"] = {"part_number": "165-5009-01",
		                      "notes": f"Phase {line} is a copy of {address - 14}. The chaser board fans each input out to an A/B connector pair. SB34 documents individual bulbs in tubes and an insulation revision on late production machines. The socket count remains open."}
		result[address] = record
	return [result[address] for address in sorted(result)]


def paired_driver(slot):
	return {"board": "CPU / PPB", "driver_transistor": f"Q{46 - slot}",
	        "control_wire": "GRY-" + PAIR_COLORS[slot],
	        "control_connection": f"CPU CN11-{(1, 2, 4, 5, 6, 7, 8, 9)[slot]}"}


def lamps():
	for row in matrix_rows("lamp-matrix"):
		address = int(row["number"])
		label = row["label"].replace("Playfld.", "Playfield").replace("Toplane", "Top Lane")
		label = {6: "Ice Planet Extra Ball", 31: "Cabinet Start Button", 50: "Left and Right Turbo Bumper"}.get(address, label)
		record = device("pinmame.output.lamp", address, REAR_LAMPS.get(address, label), "lamp", "used",
		                MANUAL, CORE, identifier=f"lamp.{slug(label)}")
		record["aliases"].append({"namespace": "manual.address", "value": str(address)})
		record["wiring"] = matrix_wiring(row)
		location = "Cabinet" if address in (30, 31) else "Backbox" if address in CABINET_LAMPS else "Playfield"
		record["physical"] = {"location": location, "quantity": 2 if address == 50 else 1}
		if address in CABINET_LAMPS:
			record["spatial"] = no_position("cabinet_or_service", MANUAL, SCHEMATIC)
		if address in REAR_LAMPS:
			record["physical"]["notes"] = (
				f'The matrix prints "{row["label"]}". All four ROM diagnostics and the installed rear-panel lens '
				"agree on the corrected color. The stable ID retains the original matrix wording."
			)
			record["provenance"]["source_refs"].extend((DISPLAY, REAR_PHOTO, SCRIPT))
		if address == 36:
			record["provenance"] = prov("conflicted", MANUAL, SCHEMATIC, SCRIPT, DISPLAY)
			record["physical"] = {
				"location": "Backbox",
				"notes": "The documented backbox lamp has no playfield coordinate. The additional playfield callout and VPX proxy are tracked in lamp36-additional-playfield-load.",
			}
		yield record


def mechanics(switches, coils):
	data = [
		("ball-trough", "Three-Ball Trough and Outhole", "kicker", (1, 2), (10, 11, 12, 13), "500-5044-00",
		 "The drain places a ball on 10. Outhole coil 1 lifts it into the gravity-fed trough. The three switches sense individual ball positions. Coil 2 ejects the ball at the shooter end. A jam can leave the outhole or release-end switch active while the ROM retries."),
		("turbo-launch", "Turbo Launch", "kicker", (3,), (14, 30), "500-5406-00",
		 "The trough serves the shooter lane. A ball closes 14 in that lane. The cabinet launch command on 30 fires coil 3 in the 2.01 start probe."),
		("transporter-ramp", "Transporter Up/Down Ramp", "diverter", (5, 6), (36, 39, 28, 52), None,
		 "Raise and lower drives act on a two-position ramp. Only the raised position closes switch 39. The lowered position feeds the ramp shot, and the raised position exposes the entry under it to the subway. SB32 traces intermittent failure to return down to the Ramp Up switch or a loose bobbin screw on the latch."),
		("upper-ramp-gate", "Upper Ramp Gate Lift", "gate", (22,), (), "515-5465-00",
		 "A switched coil lifts the gate when energized. The manual identifies a gate-lift plate assembly and the retained script opens s22 only during output 22."),
		("swinging-target", "Swinging Target", "motorized", (16,), (25, 29), "500-5370-00",
		 "A relay-driven motor turns the drive cam and stud to swing the target over the center hole. Stern's later CSI manual lists motor 515-5534-00 at 22½ RPM. Switch 25 signals a target hit. Switch 29 detects a ball in the hole. The table steps hit geometry to approximate the swing."),
		("transporter-fx", "Backbox Transporter F/X", "motorized", (13,), (31, 32), None,
		 "The single powered cam moves a striped sliding grid across the interleaved crew and empty-room artwork. SB33 gives approximately 0.040 inch of total grid travel. Two springs bias the grid and top and bottom guides constrain its travel. The visible and hidden limits close 31 and 32 about half a cam turn apart. Only one limit may close at a time. The backbox motor runs independently of the playfield ramp and VUK. The Data East schematic shows 515-5532-00-14 on a 28 VAC feed. Stern's later CSI manual lists 500-5421-00 at 24 VAC and 3½ RPM in the Star Trek Transporter F/X row. The speed of 515-5532-00-14 remains unverified."),
		("subway-vuk", "Under-Playfield Chutes and Right VUK", "kicker", (14,), (27, 28, 29, 40, 52), "500-5116-05",
		 "The left and center holes feed under-playfield chutes leading to the right VUK. Switch 40 senses a ball waiting in the VUK, and coil 14 ejects it. Upper-left switches 52 and 28 represent separate portions of the path."),
		("laser-kick", "Left Outlane Laser Kick", "kicker", (15,), (17,), "500-5080-00",
		 "The left outlane switch reports the ball and the laser-kick assembly can return it up the outlane when the ROM enables the feature."),
		("left-drop-bank", "Left Four-Bank Drop Targets", "drop_target_bank", (4,), (20, 21, 22, 23), "500-5437-02",
		 "Four independent target contacts report dropped targets. The single reset coil raises the entire bank. Switches 20–23 run bottom to top."),
		("right-drop-bank", "Right Four-Bank Drop Targets", "drop_target_bank", (7,), (44, 45, 46, 47), "500-5437-02",
		 "Four independent target contacts report dropped targets. The single reset coil raises the entire bank. Switches 44–47 run top to bottom."),
	]
	for side, button, output, part in (("left", 84, 48, "500-5177-72"), ("right", 82, 46, "500-5177-71")):
		data.append((side + "-flipper", side.title() + " Flipper", "other", (output,), (button,), part,
		             "Cabinet switch and solid-state flipper board run one flipper assembly when enabled. Use the primary synthetic PinMAME channel for the modeled stroke."))
	for name, address, switch in (("Left Turbo Bumper", 17, 33), ("Center Turbo Bumper", 18, 34),
	                              ("Right Turbo Bumper", 19, 35), ("Left Slingshot", 20, 19), ("Right Slingshot", 21, 51)):
		part = "500-5227-00" if address <= 19 else "500-5226-00"
		data.append((slug(name), name, "kicker", (address,), (switch,), part,
		             "A ball makes the assembly switch. The special-solenoid drive moves the striker to deflect the ball."))
	for key, label, kind, outputs, sensors, part, behavior in data:
		mechanism = {
			"id": "mech." + key, "label": label, "kind": kind, "behavior": behavior,
			"actuators": [coils[n]["id"] for n in outputs], "sensors": [switches[n]["id"] for n in sensors],
			"provenance": prov("observed", MANUAL, SCHEMATIC, SCRIPT),
		}
		if part:
			mechanism["assembly_part_number"] = part
		if key == "transporter-ramp":
			mechanism["provenance"]["source_refs"].append(bulletin_id(32))
		if key in ("swinging-target", "transporter-fx"):
			mechanism["provenance"]["source_refs"].append(MOTOR_SPECS)
		if key == "transporter-fx":
			mechanism["provenance"]["source_refs"].append(bulletin_id(33))
			mechanism["positions"] = [
				{"id": "crew-visible", "label": "Crew visible / TOP", "sensors": [switches[31]["id"]]},
				{"id": "crew-gone", "label": "Crew gone / BOT", "sensors": [switches[32]["id"]]},
			]
		yield mechanism


def normalized(point):
	left, top, right, bottom = BOUNDS
	x, y = point
	return (x - left) / (right - left), (y - top) / (bottom - top)


def drawing_fits(drawings):
	result = {}
	for name, drawing in drawings.items():
		pairs = [(tuple(p["pixel"]), normalized(p["xy"])) for p in drawing["controls"]]
		if len(pairs) < 4 or max(leave_one_out(pairs)) > 0.04:
			raise ValueError(f"Star Trek factory drawing fit exceeds the observed-placement tolerance: {name}")
		result[name] = fit(pairs)
	return result


def locations(data, drawings, devices):
	transforms = drawing_fits(drawings)
	for key, measurements in data.items():
		record = devices[key]
		if "spatial" in record:
			raise ValueError(f"placement was supplied for non-spatial device: {key}")
		group = record["binding"]["group"]
		role = "sensor" if group == "pinmame.input.switch" else "emitter" if record["kind"] in {"lamp", "flasher", "gi"} else "effect"
		placements = []
		for index, point in enumerate(measurements, 1):
			from_table = "object" in point
			if "texture" in point:
				if point["texture"] != "images/Playfield.png":
					raise ValueError(f"unknown playfield texture: {point['texture']}")
				px, py = point["pixel"]
				x, y = px / 1992, py / 4295
				refs = (TABLE, SLING_PHOTO, SLING_BOARD, MANUAL)
			elif from_table:
				x, y = normalized(point["xy"])
				refs = (TABLE, SCRIPT, MANUAL)
			else:
				x, y = apply(transforms[point["drawing"]], point["pixel"])
				refs = (MANUAL, TABLE)
			if not (0 <= x <= 1 and 0 <= y <= 1):
				raise ValueError(f"point outside playfield: {key}: {point}")
			placements.append({
				"id": f"{record['id']}.p{index}", "role": role, "space": "playfield",
				"x": _round_point(x), "y": _round_point(y),
				"provenance": prov("observed", *refs),
			})
		if not placements:
			raise ValueError(f"empty placement list for {key}")
		record["spatial"] = {"status": "observed", "placements": placements}


def build():
	seed = load_json(SEED)
	switch_list = inputs()
	coil_list = solenoids()
	lamp_list = list(lamps())
	switches = {d["binding"]["device"]: d for d in switch_list if d["binding"]["group"] == "pinmame.input.switch"}
	coils = {d["binding"]["device"]: d for d in coil_list}
	devices = {f"{kind}.{d['binding']['device']}": d
	           for kind, records in (("switch", switches.values()), ("solenoid", coil_list), ("lamp", lamp_list))
	           for d in records}
	locations(seed["placements"], seed["drawings"], devices)
	relationships = [
		{"id": f"mirrors.chase-{i}", "kind": "direct", "source": coils[36 + i]["id"],
		 "destination": coils[50 + i]["id"], "provenance": prov("validated", CORE, TRACE)}
		for i in range(1, 4)
	] + flipper_column_relationships(
		flip_swno=FLIP_SWNO, matrix_ids={n: switches[n]["id"] for n in FLIP_SWNO}, refs=(CORE,),
	)
	identity = dict(seed["machine"], playfield={"width": BOUNDS[2], "height": BOUNDS[3], "units": "vpx",
	                                           "provenance": prov("observed", TABLE)})
	definition = {
		"format": "pinmame-machine-definition", "schema_version": 2, "machine": identity,
		"controller": {"platform": "pinmame.dataeast", "inversion_applied_by_emulator": True, "hardware_generation": "0x2000"},
		"coverage": {
			"status": "partial",
			"missing": ["output_semantics", "mechanism_behavior", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {"catalog_identity": "validated", "address_enumeration": "validated",
			               "semantic_naming": "observed", "physical_wiring": "observed", "mechanisms": "observed",
			               "variant_coverage": "validated", "recreation_knowledge": "observed", "spatial_placement": "observed"},
		},
		"drivers": seed["drivers"], "inputs": switch_list, "outputs": coil_list + lamp_list,
		"displays": [{"id": "display.dmd", "label": "128 × 16 Backbox DMD", "kind": "dmd",
		              "controller_index": 0, "width": 128, "height": 16, "physical_location": "cabinet_or_service",
		              "spatial": no_position("cabinet_or_service", CORE, SCHEMATIC),
		              "provenance": prov("validated", CORE, SCHEMATIC, TRACE, DISPLAY)}],
		"mechanisms": list(mechanics(switches, coils)), "relationships": relationships, "sources": sources(seed["photos"]),
		"knowledge": {"path": KNOWLEDGE.relative_to(ROOT).as_posix(), "status": "partial"},
		"conflicts": [BACKBOX_5_CONFLICT],
	}
	return definition, seed


def artifacts():
	definition, seed = build()
	records = definition["inputs"] + definition["outputs"] + definition["displays"]
	unlocated = [r["id"] for r in records if "spatial" not in r]
	located = [r for r in records if r.get("spatial", {}).get("status") == "observed"]
	flashers = {}
	for record in definition["outputs"]:
		if record["kind"] != "flasher":
			continue
		address = record["binding"]["device"]
		backbox = FLASH_BACKBOX[address]
		quantity = record["physical"]["quantity"]
		placed = len(record.get("spatial", {}).get("placements", []))
		outstanding = quantity - backbox - placed
		if outstanding < 0:
			raise ValueError(f"More playfield placements than fitted emitters: {record['id']}")
		flashers[record["id"]] = {"address": address, "total_bulbs": quantity, "backbox_bulbs": backbox,
		                         "placed_playfield_bulbs": placed, "unplaced_playfield_bulbs": outstanding}
	report = {
		"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE,
		"decision": "partial", "bounds": list(BOUNDS),
		"transform": "x = raw_x / 952, y = raw_y / 2162, player view with y=0 at rear. Round to six decimals.",
		"extraction": {"source": VPX.as_posix(), "sha256": VPX_HASH, "tool": "vpxtool git:v0.33.3",
		               "manifest": (EXTRACTION / "manifest.json").as_posix(), "manifest_sha256": EXTRACTION_HASH,
		               "file_count": 813, "total_bytes": 68562091},
		"evidence": seed["placements"],
		"drawings": seed["drawings"], "drawing_transforms": drawing_fits(seed["drawings"]),
		"photo_references": seed["photos"],
		"flasher_inventory": flashers, "conflicts": definition["conflicts"],
		"located_devices": len(located), "unlocated_devices": unlocated, "blockers": seed["blockers"],
	}
	report_text = [
		"# Star Trek (Data East 1991) spatial evidence", "",
		"Coverage stays **partial**. Placement status is observed throughout.", "",
		f"{len(located)} devices have coordinates. {len(unlocated)} have no spatial disposition.", "",
		"The JSON report records each measurement, its object, drawing or texture locator, and the VPX extraction identity. "
		"Each drawing has its own affine fit from independently read pixel controls. The largest allowed "
		"leave-one-out residual is 0.04 normalized. Measurements near the edges or on the under-apron end extrapolate "
		"the controls. All drawing readings and projections are approximate.", "",
		"Four slingshot switch placements project aperture centers from the 1992 × 4295 VPX playfield texture. "
		"The original-machine photo and bare-board reproduction photo identify the matching bores. "
		"The coordinates represent where the blades enter the playfield plane.", "",
		"## Remaining placement work", "",
		*(f"- {paragraph}" for paragraph in seed["blockers"]), "",
		"Lamp 36 has a documented backbox lamp and a disputed additional playfield callout. Its playfield placement and total bulb count remain open.", "",
		"## Flasher bulb accounting", "",
		"The backbox counts are physical lamps on the same circuit. They are exempt from playfield coordinates. Rear-panel bulbs over the playfield count as playfield placements.", "",
		"| Public output | Total bulbs | Backbox | Playfield located | Playfield pending |",
		"| --- | --- | --- | --- | --- |",
		*(f"| {r['address']} | {r['total_bulbs']} | {r['backbox_bulbs']} | {r['placed_playfield_bulbs']} | {r['unplaced_playfield_bulbs']} |"
		  for r in flashers.values()), "",
		"## Devices without coordinates or a spatial exemption", "",
		*(f"- `{name}`" for name in unlocated), "",
	]
	knowledge = "\n".join(seed["knowledge"]) + "\n"
	return {
		TARGET: canonical_bytes(definition), KNOWLEDGE: knowledge.encode("utf-8"),
		REPORT.with_suffix(".json"): canonical_bytes(report),
		REPORT.with_suffix(".md"): "\n".join(report_text).encode("utf-8"),
	}


def verify_vpx(root):
	extracted = root / EXTRACTION
	if check_manifest(extracted, DRIVER) != EXTRACTION_HASH:
		raise ValueError("Unexpected Star Trek VPX extraction manifest")
	manifest = build_manifest(extracted, DRIVER)
	assert len(manifest["files"]) == 813
	assert sum(record["size"] for record in manifest["files"]) == 68562091
	if file_sha256(root / VPX) != VPX_HASH or file_sha256(extracted / "script.vbs") != SCRIPT_HASH:
		raise ValueError("Unexpected Star Trek VPX or script bytes")
	bounds = load_json(extracted / "gamedata.json")
	if bounds["image"].lower() != "playfield" or file_sha256(extracted / "images/Playfield.png") != SLING_TEXTURE_HASH:
		raise ValueError("Star Trek slingshot contact texture changed")
	if tuple(bounds[k] for k in ("left", "top", "right", "bottom")) != BOUNDS:
		raise ValueError("Unexpected Star Trek VPX bounds")
	seed = load_json(SEED)
	groups = seed["placements"] | {name: drawing["controls"] for name, drawing in seed["drawings"].items()}
	for key, measurements in groups.items():
		for point in measurements:
			if "object" not in point:
				continue
			path = extracted / "gameitems" / point["object"]
			item_type, _, value = _item_record(path, load_json(path))
			x, y, _ = _item_point(item_type, value)
			if [x, y] != point["xy"]:
				raise ValueError(f"Star Trek placement drifted: {key}: {point['object']}")


def main():
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	mode.add_argument("--verify-vpx", type=Path)
	args = parser.parse_args()
	if args.verify_vpx:
		verify_vpx(args.verify_vpx)
		return
	if AUTHOR_READY.exists():
		raise RuntimeError("Refusing to supersede an author-ready Star Trek definition")
	if TARGET.is_file() and load_json(TARGET).get("coverage", {}).get("status") == "author_ready":
		raise RuntimeError("Refusing to supersede an author-ready Star Trek definition in the partial folder")
	for path, digest in ((SCENARIO, SCENARIO_HASH), (SWITCH_TEST_SCENARIO, SWITCH_TEST_SCENARIO_HASH)):
		if file_sha256(path) != digest:
			raise RuntimeError(f"Star Trek harness scenario drifted from the retained trace: {path.name}")
	for path, payload in artifacts().items():
		if args.check:
			if not path.is_file() or path.read_bytes() != payload:
				raise RuntimeError(f"Star Trek artifact drifted: {path.relative_to(ROOT)}")
		else:
			write_bytes(path, payload)


if __name__ == "__main__":
	main()
