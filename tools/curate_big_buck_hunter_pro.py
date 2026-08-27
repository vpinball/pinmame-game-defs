"""Curate the physical Stern Big Buck Hunter Pro (2010) machine definition.

The builder is side-effect free and deterministic: every reviewed label, construction
detail, and normalized coordinate is embedded as a literal (raw retained-table units with
one documented normalization), so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots.  ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition and its pinned seed.

Evidence reality.  The retained IPDB-hosted manual is a 41-page partial ("Pink" and "Blue"
pages only, poor quality areas": mechanical assemblies and parts identification) with no
text layer and none of Stern's electrical wiring tables.  Pinned sam.c's own game block
says the same thing from the emulator side: "Did not find a complete manual anywhere (even
Stern's downloads do not have the schematics/solenoids) so this is from the VPX table,
completed with the backglass flasher map".  PinMAME's per-game output typing for this
machine is therefore descended from the community VPX table itself, not from factory
documentation.  Runtime semantics come from the retained known-working table's script;
physical construction comes from the partial manual's assembly pages; controller topology
comes from pinned source.  No address is dropped, and no unknown is papered over.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/stern/big-buck-hunter-pro-2010.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/big-buck-hunter-pro-2010.json"
SEED_PATH = ROOT / "tools/seeds/stern/big-buck-hunter-pro-2010.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/big-buck-hunter-pro-2010.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/stern/big-buck-hunter-pro-2010.md"
# The generated stub this definition supersedes. It is deliberately left on disk by this
# worktree: pruning it here would leave the shared catalog (which this branch must not
# regenerate) pointing at a missing file. The integrator's rebuild_catalog call prunes both
# the stub definition and its knowledge note through _prune_generated_stubs once this
# definition claims the bbh_* clone-tree root.
SUPERSEDED_STUB_PATH = ROOT / "machines/stubs/bbh_170.json"
SUPERSEDED_STUB_KNOWLEDGE_PATH = ROOT / "knowledge/stubs/bbh_170.md"

MACHINE_ID = "stern.big-buck-hunter-pro.2010"
KNOWLEDGE_PATH = "knowledge/stern/big-buck-hunter-pro-2010.md"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-sam"
MANUAL_SOURCE = "manual.stern.big-buck-hunter-pro.2010"
IPDB_SOURCE = "ipdb.machine-5513"
VPX_TABLE_SOURCE = "vpx-table.bbh-stern-2010"
VPX_SCRIPT_SOURCE = "vpx-script.bbh-stern-2010"
VPX_EXTRACTION_SOURCE = "vpx-extraction.bbh-stern-2010"
ROM_SOURCE = "rom.stern.big-buck-hunter-pro"

TABLE_SHA256 = "347f5533c2a673611eec9689b8c2ab7456e01db94ea8cae1082eec2545d80626"
SCRIPT_SHA256 = "da706d513c20c0936013e7c76eba6394408b20a6e9c7e9526873c969211b2e5c"
MANUAL_SHA256 = "c35324b36939b315bc0a85e2caad1fcb46e568b7c9f33930f3a67924ab9f7dff"
VPX_GEOMETRY_SHA256 = "7cbd1ece1730ced491bf178d81b0812d8c0ac70721ed1adfb236fc9347f0a88e"

EXTRACTION_RELATIVE_PATH = Path("stern/big-buck-hunter-pro-2010/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("stern/big-buck-hunter-pro-2010/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "3b50291ecc3fe665c082567801ae2319f31b49142153ae24f6e2bfff5d80d9e9"
EXTRACTION_FILE_COUNT = 822
EXTRACTION_TOTAL_BYTES = 100412917

TABLE_BOUNDS = "left=0 top=0 right=979 bottom=2162"
PLAYFIELD_WIDTH = 979.0
PLAYFIELD_HEIGHT = 2162.0

EXCERPT_ROOT = "evidence/excerpts/stern.big-buck-hunter-pro.2010"

# --- Drivers -------------------------------------------------------------------------------------
# 4 drivers: CORE_GAMEDEF(bbh, 170, ...) plus 3 CORE_CLONEDEF(bbh, ...) rows, counted from
# src/wpc/sam.c at the pinned revision. driver.c's comment block dates them 02/10 (1.4),
# 02/10 (1.5), 05/10 (1.6) and 11/10 (1.7).
DRIVER_IDS = ("bbh_170", "bbh_160", "bbh_150", "bbh_140")

DRIVER_NOTE_PARENT = (
	"PinMAME's clone-tree parent and this definition's reference driver for address semantics. "
	"driver.c dates it 11/10. Every bbh_* driver shares the one static bbhGameData struct "
	"produced by sam.c's INITGAME macro, so the choice of parent carries no controller-address, "
	"polarity, or playfield consequence. This is also the driver the retained known-working "
	"table binds (Const cGameName=\"bbh_170\") and the only one for which sam.c sets a "
	"fast-flip watch address (samlocals.fastflipaddr = 0x0106acae), so public solenoid 33, "
	"PinMAME's synthetic game-on state, is only expected to toggle on this revision."
)

DRIVER_NOTE_170_ROM = (
	"The user's authorized ROM library holds a V1.7 dump whose bytes do not match the ROM this "
	"pinned revision loads: bbh_170.zip member BBH_V1-7_A_c.bin is 29,069,268 bytes with "
	"SHA-1 5c292f8093130d2a3aef919aa57d9d8c5f8e7756, while sam.c's ROM_LOAD expects "
	"0x01BB8FD0 bytes with SHA-1 9a71959c57b9a75028e21bce9ee03871f8914138, and neither the "
	"first 29,069,264 bytes nor the byte range past a 4-byte skip hashes to the pinned value. "
	"The same library's 1.4, 1.5 and 1.6 dumps all match their pinned SHA-1s exactly. This is "
	"recorded as evidence provenance, not as a machine fact: the four drivers remain one "
	"physical machine and the definition makes no assertion that depends on which 1.7 dump a "
	"given runtime carries."
)


def _firmware_note(version: str, year: str) -> str:
	return (
		f"Stern V{version} game ROM for the same physical machine, dated {year} in pinned "
		"driver.c's comment block. It shares the one static bbhGameData struct with every other "
		"bbh_* driver, so no controller address, switch polarity, lamp, solenoid, or playfield "
		"fact differs from the reference driver. The user's authorized ROM library copy of this "
		"revision matches pinned sam.c's expected SHA-1 exactly."
	)


DRIVER_COMPATIBILITY: dict[str, tuple[str, str]] = {
	"bbh_170": ("identical", DRIVER_NOTE_PARENT + " " + DRIVER_NOTE_170_ROM)
}
for _driver_id, _version, _year in (
	("bbh_160", "1.6", "05/10"),
	("bbh_150", "1.5", "02/10"),
	("bbh_140", "1.4", "02/10"),
):
	DRIVER_COMPATIBILITY[_driver_id] = ("identical", _firmware_note(_version, _year))

# --- Coordinate normalization --------------------------------------------------------------------
# Raw coordinates below are retained-table units read from the extracted gameitems JSON.
# Normalization is a single documented transform so every placement shares one convention.


def normalize(x: float, y: float) -> tuple[float, float]:
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


def placed(identifier: str, role: str, raw_positions: tuple[tuple[float, float], ...], *source_refs: str, status: str = "validated") -> dict[str, Any]:
	placements = []
	for index, (raw_x, raw_y) in enumerate(raw_positions, start=1):
		nx, ny = normalize(raw_x, raw_y)
		suffix = f".{index}" if len(raw_positions) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": nx,
				"y": ny,
				"provenance": provenance(*source_refs, status=status),
			}
		)
	return {"status": "observed" if status != "validated" else "validated", "placements": placements}


def centroid(raw_points: tuple[tuple[float, float], ...]) -> tuple[float, float]:
	return (sum(point[0] for point in raw_points) / len(raw_points), sum(point[1] for point in raw_points) / len(raw_points))


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Big Buck Hunter Pro retained extraction is missing: {extraction_root}")
	paths = sorted(
		(path for path in extraction_root.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction_root).as_posix(),
	)
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{
				"path": path.relative_to(extraction_root).as_posix(),
				"size": path.stat().st_size,
				"sha256": _file_sha256(path),
			}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Big Buck Hunter Pro extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Big Buck Hunter Pro retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Big Buck Hunter Pro retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Big Buck Hunter Pro retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


# --- Sources -------------------------------------------------------------------------------------

MANUAL_REFS = (MANUAL_SOURCE, CORE_SOURCE)
SCRIPT_REFS = (CORE_SOURCE, VPX_SCRIPT_SOURCE)
GEOMETRY_REFS = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)

# Excerpt records: transcription .md + rendered crop .webp, both digest-pinned. The digests
# below were emitted by tools/make_excerpt.py when each crop was rendered.
EXCERPTS = (
	{
		"id": "excerpt.bbh.trough-assembly",
		"locator": "PDF page 3, printed b 3, 4-Ball Trough Assembly 500-6318-24-ND cut-away drawing with its printed SW. 18 / SW. 19 / SW. 21 / SW. 22 board labels",
		"path": f"{EXCERPT_ROOT}/trough-assembly.md",
		"sha256": "4441c5f72a3cca5cd3dcccd975a0b6af770d72757c55e9da4cd57e5f809eab32",
		"image": f"{EXCERPT_ROOT}/trough-assembly.webp",
		"image_sha256": "2c5c1a4eabee466050567e919781eaeba2c0e29cf111543c6201fd3f95edb24d",
		"image_derivation": "Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf page 3, crop box 0.03,0.32,1.0,0.72 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP",
		"method": "manual",
		"transcribed_by": "curator, read from the 200 dpi rendered page",
		"reviewed": True,
	},
	{
		"id": "excerpt.bbh.cabinet-parts-switches",
		"locator": "PDF page 29, printed p 4, Cabinet Parts & Switches parts table (items 1-16) incl. 3S Start Button, 4T Tournament Button, 5 Flipper Button, 6S/6D Flipper Switch Single/Double",
		"path": f"{EXCERPT_ROOT}/cabinet-parts-switches.md",
		"sha256": "d380ce6afa1fd162b607cc00c62a32b41954b280082bee99faf74fc8cdd58691",
		"image": f"{EXCERPT_ROOT}/cabinet-parts-switches.webp",
		"image_sha256": "85936298c353e5e043c3c8d2b58de7e4be937df29018ea0c1f806045ae75a15c",
		"image_derivation": "Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf page 29, crop box 0.03,0.565,1.0,0.815 of the page, rendered at 300 dpi with pdftoppm, reduced to 900px wide grayscale, quality 75 WebP",
		"method": "manual",
		"transcribed_by": "curator, read from the 200 dpi rendered page; the transcription also covers PDF page 30 (printed p 5, items 17-37), which has no committed crop because no single page can stand for both tables",
		"reviewed": True,
	},
	{
		"id": "excerpt.bbh.ram-kicker-assembly",
		"locator": "PDF page 18, printed b 18, ASSEMBLY RAM KICKER BIG BUCK 500-7166-00 parts table incl. item 5 COIL - 23-800, NO DIODE",
		"path": f"{EXCERPT_ROOT}/ram-kicker-assembly.md",
		"sha256": "1fe9d1b2b4941cd5a4e3157a3b1eb115b8b11378a7821eb98f223a75517e3231",
		"image": f"{EXCERPT_ROOT}/ram-kicker-assembly.webp",
		"image_sha256": "d708481d7e6781eff93fd3728299906d2ad20f3537ebef9bb4393ae9fdf9399a",
		"image_derivation": "Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf page 18, crop box 0.02,0.03,0.98,0.52 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP",
		"method": "manual",
		"transcribed_by": "curator, read from the 150 dpi rendered pages; the transcription also covers PDF pages 16-17 (printed b 16 and b 17, the ram toy and its mount bracket), disclosed there without crops",
		"reviewed": True,
	},
	{
		"id": "excerpt.bbh.spinner-opto",
		"locator": "PDF page 15, printed p 15, MOTOR/BRACKETS ASSEMBLY 511-5224-00 parts table incl. item 8 OPTO DISK 535-0308-00 and item 9 OPTO BOARD ASSEMBLY 511-5209-00",
		"path": f"{EXCERPT_ROOT}/spinner-opto.md",
		"sha256": "e147c33ae76d4d56a5bd51967bae0155f1d1697700add1c6425afd48276e2566",
		"image": f"{EXCERPT_ROOT}/spinner-opto.webp",
		"image_sha256": "df6eb0509e6130acf011c3223f878894d2132f1ee350797e38db3c44f38eaf36",
		"image_derivation": "Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf page 15, crop box 0.0,0.0,0.62,0.80 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP",
		"method": "manual",
		"transcribed_by": "curator, read from the 300 dpi rendered page after a first 150 dpi reading misread six cells; the excerpt records the correction",
		"reviewed": True,
	},
	{
		"id": "excerpt.bbh.up-down-post-assembly",
		"locator": "PDF page 19, printed b 19, Up/Down Post Assembly 500-7153-04 parts table incl. item 3 COIL 26-1200 - NO DIODE and the Q12 drawing label",
		"path": f"{EXCERPT_ROOT}/up-down-post-assembly.md",
		"sha256": "042d4b056b1dfa5a7777b1055e086f6f4ce04fd53d5fbccf33edeae188d3c2de",
		"image": f"{EXCERPT_ROOT}/up-down-post-assembly.webp",
		"image_sha256": "6dd771f67ac24b8027ced7038c0b8d4a8f618cf2fb4707c262da86c108463b9a",
		"image_derivation": "Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf page 19, crop box 0.0,0.0,1.0,0.55 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP",
		"method": "manual",
		"transcribed_by": "curator, read from the 150 dpi rendered page",
		"reviewed": True,
	},
	{
		"id": "excerpt.bbh.ball-guide-optos",
		"locator": "PDF page 24, printed p 24, ball guide assemblies 511-5230-04/-05 with OPTO TRANSEIVER ASSY 15-inch LEADS 500-6775-01",
		"path": f"{EXCERPT_ROOT}/ball-guide-optos.md",
		"sha256": "4d924d1e4bd0a70691db721efc2a44d99ba77f04382813c7dd6594eb2a12f93f",
		"image": f"{EXCERPT_ROOT}/ball-guide-optos.webp",
		"image_sha256": "5338f6d496d276f9dadd2be6bf21036fe407bdbfb14a8feda427c643d52bacf3",
		"image_derivation": "Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf page 24, crop box 0.0,0.0,1.0,1.0 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP",
		"method": "manual",
		"transcribed_by": "curator, read from the 150 dpi rendered page",
		"reviewed": True,
	},
	{
		"id": "excerpt.bbh.back-panel-assembly",
		"locator": "PDF page 25, printed p 25, Back Panel Assembly BBH 500-7164-00 with item 2 SOCKET & BULB ASSY CLEAR qty 5",
		"path": f"{EXCERPT_ROOT}/back-panel-assembly.md",
		"sha256": "a44a02ef341b42eed0fdc011b3678a70b17e7066db9d3c591696dad88f1baaaa",
		"image": f"{EXCERPT_ROOT}/back-panel-assembly.webp",
		"image_sha256": "3ffac976061e0a433ca3b7f11051a6fdb51e56d751502443039d4196d29705e8",
		"image_derivation": "Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf page 25, crop box 0.0,0.0,1.0,1.0 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP",
		"method": "manual",
		"transcribed_by": "curator, read from the 150 dpi rendered page",
		"reviewed": True,
	},
)


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the bbh_* clone tree: CORE_GAMEDEF(bbh, 170, ...) plus 3 CORE_CLONEDEF(bbh, ...) rows in src/wpc/sam.c",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sam.c INITGAME(bbh, GEN_SAM, sam_dmd128x32, SAM_2COL, SAM_NO_AUX) at line 3098, whose macro "
				"expands to bbhGameData = {GEN_SAM, sam_dmd128x32, {FLIP_SW(FLIP_L)|FLIP_SOL(FLIP_L), 0, 2, 16, 0, 0, "
				"0, 0, sam_getSol}} and leaves the trailing wpc/simData/sxx members at their C zero-initialization "
				"default, so wpc.invSw is all zero; grep for invSw across src/wpc/sam.c returns no assignment anywhere. "
				"sam.c's own per-game bbh_ block (lines 1429-1433) sets solenoids 19-22 and 25-32 to "
				"CORE_MODOUT_BULB_89_20V_DC_WPC under the comment 'Did not find a complete manual anywhere (even "
				"Stern's downloads do not have the schematics/solenoids) so this is from the VPX table, completed with "
				"the backglass flasher map' -- a disclosure that the emulator's own typing for this game descends from "
				"the community table retained here, not from factory documentation. sam.c line 1692 sets "
				"samlocals.fastflipaddr = 0x0106acae for bbh_170 only. sam.c line 1390 sets coreGlobals.nLamps = "
				"64 + lampCol * 8 = 80 and line 1391 nSolenoids = CORE_FIRSTCUSTSOL - 1 + 16 = 66; lines 1132-1163 "
				"gate every custom-solenoid write path behind a SAM_GAME_* gameSpecific1 bit, none of which bbh "
				"declares, so nothing writes public 51-66. sam.c's dedswitch_lower_r/dedswitch_upper_r (lines 242-276) "
				"read the dedicated-switch blocks with their own D-1 to D-32 comment map, and lines 455-458 copy each "
				"flipper-button bit to its EOS bit with the comment that SAM uses no standard VPM flipper coils and "
				"the ROM reports technician errors otherwise. driver.c lines 2142-2149 date the four revisions. "
				"src/wpc/core.c MDRV_SWITCH_CONV/MDRV_LAMP_CONV(core_swSeq2m, core_m2swSeq) in the default PinMAME "
				"machine driver (sam.c registers no conversion of its own), with core_swSeq2m(no) = no + 7."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/sam.json",
			"revision": "repository",
			"locator": (
				"Stern S.A.M. public switch, DIP, solenoid, lamp and single-GI address rules, reused unchanged. "
				"Sequential switch numbering with matrix 1-64, dedicated D-1 to D-8 at 65-72, dedicated D-17 to D-24 "
				"at -7 to 0, the flipper column at 81-88, solenoids 1-66 with 33 as the synthetic game-on state, the "
				"51-66 macro-published custom range, and one aggregate GI channel at address 0. Every rule was "
				"re-derived from pinned source for this curation and matched."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/stern.big-buck-hunter-pro.2010/Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf",
			"original_filename": "Stern_2010_Big_Buck_Hunter_Pro_Partial_Manual_Pink_and_Blue_pages_only_poor_quality_areas.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"41-page image-only partial scan (no text layer; pdftotext returns only form feeds) of the Stern Big "
				"Buck Hunter Pro manual's 'Blue Pages' (Major Assemblies & Samples, per PDF page 1) and 'Pink Pages' "
				"(Parts Identification, per PDF page 26), hosted by IPDB with the note 'Partial Manual (Pink and Blue "
				"pages only, poor quality areas)'. It carries none of Stern's electrical wiring tables: no switch "
				"matrix, no lamp matrix, no coil table, and no schematics. PDF page 3 is the 4-ball trough assembly "
				"whose cut-away labels SW. 18/SW. 19 on the roller microswitches and SW. 21/SW. 22 on the dual opto "
				"boards; PDF page 15 the spinner motor assembly with its opto disk and opto board; PDF pages 16-18 "
				"the ram mech and ram kicker assemblies; PDF page 19 the up/down post assembly; PDF page 24 the ball "
				"guide assemblies with opto transceivers; PDF page 25 the back panel with five clear sockets; PDF "
				"pages 29-30 the cabinet parts and switches. Pages 31-32 (playfield location illustrations) and the "
				"remaining pages were rendered and read during the pass but carry no address-bearing table."
			),
			"license": "NOASSERTION",
			"attribution": "Stern Pinball, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [dict(excerpt) for excerpt in EXCERPTS],
		},
		{
			"id": IPDB_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=5513",
			"revision": "2026-08-27",
			"locator": (
				"IPDB machine 5513, retrieved through an authenticated browser session and saved with the contributor's "
				"help after plain fetches returned HTTP 403 behind Cloudflare. Identity facts used: Stern Pinball, "
				"Incorporated, Chicago; S.A.M. Board System; project date 2009; date of manufacture January 2010; "
				"design John Borg; sound Ken Hale; software Lonnie D. Ropp and Lyman F. Sheats Jr.; common "
				"abbreviation BBH; the documentation entry naming the partial manual retained here. Used for identity "
				"only, never for I/O semantics."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Machine Database",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/big-buck-hunter-pro-2010/source/Big%20Buck%20Hunter%20Pro%20%28Stern%202010%29.vpx",
			"original_filename": "Big Buck Hunter Pro (Stern 2010).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working community recreation of the physical machine, from the contributor's own "
				"table collection. Table info credits a VPX rebuild by 32assassin of a VP9 version by 85vette, "
				"released June 2017, table version 1.11. Exact playfield bounds from its own gamedata.json are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT}. Geometry "
				"authority only for named table objects; the full per-object dump is retained at "
				"external:pinmame-review-artifacts/big-buck-hunter-pro-2010/vpx-geometry.json, SHA-256 "
				f"{VPX_GEOMETRY_SHA256}. This is a thin build by this project's standards -- 822 extracted files and "
				"a 37,592-byte script against the 240-290 kB VPW-authored scripts several other games in this project "
				"used -- and it is judged accordingly: its object set is good enough to place many addresses but it "
				"is not treated as authority for any address it does not model."
			),
			"license": "NOASSERTION",
			"attribution": "community table authors (32assassin VPX rebuild of an 85vette VP9 version; no explicit author credit beyond the table info block)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/stern/big-buck-hunter-pro-2010/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"Retained embedded script, 37,592 bytes, 1,147 lines. Runtime and mechanism-causality authority: "
				'Const cGameName = "bbh_170", Const UseSolenoids = 1, Const UseLamps = 0, Const UseGI = 0 with a '
				"GICallback set anyway (its UpdateGI ignores the string index and drives one GI collection for any "
				"index); SolCallback entries for 1, 2, 3, 4, 7, 12, 14, 15, 16, 23 plus the flasher pseudo-lamp "
				"callbacks 19, 20, 21, 22, 25, 26, 27, 29, 31, 32 ('Setlamp 119' through 'Setlamp 132', numbers "
				"above the 80-address lamp transport, so they are table-internal flasher channels, not controller "
				"lamp addresses); SolCallback(5) present but its target sub commented away; SolKickBack's body "
				"commented away; vpmNudge.TiltSwitch = -7; bsTrough as a cvpmBallStack (InitSw 0, 21, 20, 19, 18 "
				"with InitKick BallRelease and Balls = 4) pulsing switch 22 from inside solTrough; a JP-style "
				"ChangedLamps fade loop (LampTimer) whose UpdateLamps binds 57 lamp addresses by name; the "
				"lamp-following Buck driver (BuckTimer/BuckCheckPosition tracking lamps 16-20 and 57, writing "
				"Controller.Switch(71)/(72) at the animation endpoints, with the physical position-opto writes on "
				"37 and 45 commented out); Sub sw85_Hit pulsing 85; and the magna-save keys pulsing switches 37 "
				"and 6."
			),
			"license": "NOASSERTION",
			"attribution": "community table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/big-buck-hunter-pro-2010/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds "
				f"are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": ROM_SOURCE,
			"kind": "rom_static_analysis",
			"uri": "external:pinmame-roms/stern/big-buck-hunter-pro",
			"locator": (
				"The contributor's authorized ROM library (the user's VPinMAME roms folder, treated "
				"read-only): "
				"bbh_140.zip (SHA-256 c621195e182190e02c39fbf70805a84cfb15921f78f00a9a3c16136009ea6a57, member "
				"bbh140.bin SHA-1 0c500c0a5588f8476a71599be70b515ba3e19cab, matching pinned sam.c exactly); "
				"bbh_150.zip (SHA-256 1680fb35c5705e7c1f4f45824cc2e240ad1815e4338ce31744e938d55ae3163c, member "
				"bbh150.bin SHA-1 16e499046107baceda6f6c934d70ba2108915973, matching); bbh_160.zip (SHA-256 "
				"82f0101cc2dc1a8888a7ef6e5ccb0bcdd98eb15257caa3cc864c02b7a3e6b94b, member bbh_160.bin SHA-1 "
				"c58a2ae5c1332390f0d1191ee8ff920ceec23352, matching); bbh_170.zip (SHA-256 "
				"76a35ec46b65fe93667b069d3af4a5df0eeabcc541fc1a84f43f1c3e18ec2ffb, member BBH_V1-7_A_c.bin 29,069,268 "
				"bytes SHA-1 5c292f8093130d2a3aef919aa57d9d8c5f8e7756, NOT matching pinned sam.c's 0x01BB8FD0-byte "
				"9a71959c57b9a75028e21bce9ee03871f8914138; see the bbh_170 driver record). Renamed byte-identical "
				"staging copies for future harness work sit at external:pinmame-roms/stern/big-buck-hunter-pro/ "
				"under the working root; the user's own library was never modified."
			),
			"license": "NOASSERTION",
			"attribution": "Stern Pinball, Inc. firmware, user-authorized local copies",
			"rights": "NOASSERTION",
		},
	]


# --- Inputs --------------------------------------------------------------------------------------
# No printed switch matrix exists for this machine. Dispositions below come from three places
# only: the retained script's own handlers (runtime authority), the manual's assembly pages
# (construction authority for the addresses its drawings label), and pinned sam.c's dedicated-
# switch comment map (structural authority for the non-matrix blocks).

# Maintained (state-following) script handlers: Controller.Switch(n) = 1/0 pairs.
MAINTAINED_SWITCHES = (6, 7, 8, 9, 13, 23, 24, 25, 28, 29, 33, 34, 43)
# Momentary script handlers: vpmTimer.PulseSw / PulseSw(n).
PULSED_SWITCHES = (1, 5, 10, 14, 22, 26, 27, 30, 31, 32, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 85)
# Pulsed only from commented-out code (the Buck drive's position feedback).
COMMENTED_SWITCHES = (37, 45)

# Raw retained-table coordinates for switch objects (x, y in table units).
SWITCH_POSITIONS: dict[int, tuple[float, float]] = {
	5: (187.24147, 497.13535),      # Gate.sw5
	6: (70.079025, 216.28954),      # Trigger.sw6
	7: (577.75, 183.375),           # Trigger.sw7
	8: (663.75, 184.875),           # Trigger.sw8
	9: (752.75, 185.875),           # Trigger.sw9
	10: (660.432, 645.5422),        # HitTarget.sw10 center
	13: (886.765, 158.53545),       # Trigger.sw13
	14: (908.09595, 349.69592),     # Gate.sw14
	23: (920.5, 1914.75),           # Trigger.sw23 (co-located with Trigger.swPlunger)
	24: (45.25, 1625.375),          # Trigger.sw24
	25: (124.75, 1555.375),         # Trigger.sw25
	26: (181.95, 1494.3),           # Wall.LeftSlingShot drag-point centroid
	27: (645.35, 1494.8),           # Wall.RightSlingShot drag-point centroid
	28: (700.75, 1525.375),         # Trigger.sw28
	29: (832.75, 1620.375),         # Trigger.sw29
	30: (797.61285, 349.65323),     # Bumper.Bumper2 (script binds 30)
	31: (680.8386, 558.54584),      # Bumper.Bumper3 (script binds 31)
	32: (558.52405, 344.7493),      # Bumper.Bumper1 (script binds 32)
	33: (767.2182, 1520.375),       # Trigger.sw33
	34: (290.9301, 298.69608),      # Kicker.sw34
	35: (440.8335, 221.62009),      # HitTarget.sw35
	36: (537.26984, 474.73724),     # HitTarget.sw36
	38: (401.7898, 572.07294),      # HitTarget.sw38
	39: (706.3484, 961.35815),      # HitTarget.sw39
	40: (94.9296, 933.41693),       # HitTarget.sw40
	41: (93.819725, 991.0676),      # HitTarget.sw41
	42: (92.33992, 1047.3003),      # HitTarget.sw42
	43: (445.1116, 355.2686),       # Trigger.sw43
	44: (740.02466, 680.4506),      # Spinner.sw44
}

# Addresses whose placement is a documented projection onto a mechanism rather than an
# observed switch object, with the reason recorded in the spatial report.
SWITCH_PROJECTIONS: dict[int, str] = {
	1: "The Buck is a moving target: its hit is detected by the retained table through which of the "
	"thirty-one BuckWall ladder segments is raised at the Buck's current animated position, so the "
	"hit sensor has no single playfield coordinate. Placement projects onto the Buck target's home "
	"position (Primitive.Buck), where the mechanism rests and where the wall ladder begins.",
	18: "Below-playfield trough assembly; the manual's cut-away draws the trough and labels its "
	"switches but gives no playfield-surface coordinate. Placement projects onto the trough's own "
	"ball-release kicker (Kicker.BallRelease), the same documented projection every other thin-table "
	"trough in this project uses.",
	19: "Below-playfield trough assembly; projects onto Kicker.BallRelease like switches 18-22.",
	20: "Below-playfield trough assembly; projects onto Kicker.BallRelease like switches 18-22.",
	21: "Below-playfield trough assembly; projects onto Kicker.BallRelease like switches 18-22.",
	22: "Below-playfield trough assembly; projects onto Kicker.BallRelease like switches 18-22.",
	37: "The Buck drive's position feedback travels with the moving target along the deer-track fiber "
	"assembly; no fixed sensor coordinate exists in any retained source. Placement projects onto the "
	"deer-track ladder's midpoint (the mean of the BuckWall1-31 drag-point centroids), disclosed as a "
	"projection, not an observation.",
	45: "Same Buck-drive position-feedback projection as switch 37.",
}

# Raw coordinates for the two documented switch projections.
SWITCH_PROJECTION_RAW: dict[int, tuple[float, float]] = {
	1: (671.0, 803.0),     # Primitive.Buck home position
	18: (852.172, 1858.0284),   # Kicker.BallRelease
	19: (852.172, 1858.0284),
	20: (852.172, 1858.0284),
	21: (852.172, 1858.0284),
	22: (852.172, 1858.0284),
	37: (495.6, 952.2),    # mean of the BuckWall1-31 drag-point centroids (the deer-track ladder midpoint)
	45: (495.6, 952.2),
}

THROUGH_EXIT_PULSE_NOTE = (
	"The retained script pulses this address from inside solTrough (vpmTimer.PulseSw 22) as the "
	"served ball leaves, which is the ball crossing the exit opto rather than the coil actuating a "
	"switch."
)

TROUGH_SUBSTITUTION_NOTE = (
	"The retained table drives the Buck from lamp events and animates the target itself, so these "
	"writes are the table author's substitute for the machine's own position feedback, not evidence "
	"that the physical sensor sits at this dedicated-switch position. The physical Buck feedback "
	"addresses the ROM actually reads are not settled by any retained source; the commented-out "
	"matrix writes on 37 and 45 are the table author's own record of where those optos belong."
)

# The dedicated-switch blocks, transcribed from sam.c's own comment map over dedswitch_lower_r
# (DED #1-#16) and dedswitch_upper_r (DED #17-#24). Construction facts for the coin-door and
# cabinet buttons come from the manual's cabinet parts pages where they exist.
DEDICATED_SWITCHES: dict[int, tuple[str, str, str]] = {
	# address: (label, manual D-number, notes)
	-7: ("Tilt Pendulum (Plumb Bob)", "D-17",
		"Printed DED #17 in sam.c's dedswitch_upper_r comment map. The physical plumb bob tilt "
		"switch's contact wire form is manual cabinet item 25C (535-7563-01), with bracket 25B, "
		"hanger wire 25H and weight 25W; the manual assigns no matrix or D-number to it. The "
		"retained script confirms the public address directly: vpmNudge.TiltSwitch = -7."),
	-6: ("Slam Tilt", "D-18",
		"Printed DED #18. Coin-door switch hardware per manual cabinet item 19 (180-5024-01 USA, "
		"alt 19C/19J); the manual names no individual switch inside the door."),
	-5: ("Ticket Notch", "D-19",
		"Printed DED #19. No ticket dispenser appears anywhere in the retained manual or script; "
		"the address is read by the platform whether or not a dispenser is fitted."),
	-4: ("Not Used (DED #20)", "D-20",
		"Printed DED #20 with no function in sam.c's comment map and no retaining evidence."),
	-3: ("Back (Coin Door)", "D-21",
		"Printed DED #21. One of the coin-door service buttons on the 4-button bracket (manual "
		"cabinet item 20)."),
	-2: ("Minus (Coin Door)", "D-22",
		"Printed DED #22. sam.c's own descriptive comment block lists D-21 as Plus and D-22 as "
		"Minus, while its executed keyboard input-port table SAM_COMPORTS puts Minus on the bit "
		"that becomes public -2; the same platform-internal disagreement was recorded for Pirates "
		"of the Caribbean, whose printed manual there sided with the input-port table. This "
		"machine's partial manual prints no dedicated-switch block at all, so the resolution here "
		"rests on the executed table alone and is recorded as the same platform-level naming "
		"defect, not as a game-specific conflict."),
	-1: ("Plus (Coin Door)", "D-23",
		"Printed DED #23. See the -2 note for the Plus/Minus ordering caveat."),
	0: ("Select (Coin Door)", "D-24",
		"Printed DED #24. The fourth coin-door service button."),
	65: ("Left Coin Chute", "D-1", None),
	66: ("Center Coin Chute", "D-2", None),
	67: ("Right Coin Chute", "D-3", None),
	68: ("Fourth Coin Chute", "D-4", None),
	69: ("Fifth Coin Chute", "D-5", None),
	70: ("Not Used (DED #6)", "D-6", None),
	71: ("Left Post Save (UK Only) - not fitted; Buck home position in the retained table", "D-7",
		"Printed DED #7, a United Kingdom post-save cabinet switch this US-manufactured machine "
		"does not carry: no such switch or bracket appears in the retained manual's cabinet parts "
		"tables. The retained script writes Controller.Switch(71) = 1 whenever its animated Buck "
		"reaches the start of its travel, repurposing this always-readable dedicated address as "
		"the Buck's home-position feedback. " + TROUGH_SUBSTITUTION_NOTE),
	72: ("Right Post Save (UK Only) - not fitted; Buck end-of-travel in the retained table", "D-8",
		"Printed DED #8, the second UK post-save address, not fitted for the same reason as D-7. "
		"The retained script writes Controller.Switch(72) while the Buck sits at the far end of "
		"its travel and reverses there. " + TROUGH_SUBSTITUTION_NOTE),
	81: ("Left Flipper Button", "D-9", None),
	82: ("Left Flipper End-of-Stroke (emulator-synthesized)", "D-10", None),
	83: ("Right Flipper Button", "D-11", None),
	84: ("Right Flipper End-of-Stroke (emulator-synthesized)", "D-12", None),
	85: ("Elk Diverter Button (upper-left-flipper cabinet position)", "D-13",
		"Printed DED #13, the hardware upper-left-flipper button position. This machine fits no "
		"upper flipper (bbhGameData declares FLIP_SW(FLIP_L)|FLIP_SOL(FLIP_L) only), and the "
		"retained manual's cabinet parts table lists only the two red flipper button assemblies "
		"(item 5, qty 2) with no third side button - so which physical cabinet control feeds this "
		"address on the factory machine is not settled by any retained source. The retained table "
		"binds it to the Elk diverter: Sub sw85_Hit pulses 85 and Sub SolLElk (solenoid 14) "
		"deploys the Elkdiverter while swapping dropped walls sw85/sw85a, and sam.c's EOS mirror "
		"(lines 455-458) copies this bit to D-14 so the ROM's EOS read sees the button."),
	86: ("Elk Diverter Button EOS (emulator-synthesized)", "D-14",
		"Printed DED #14. sam.c's dedswitch_lower_r copies the D-13 button bit into this EOS bit "
		"so the ROM's flipper self-test sees a consistent pair; the physical machine fits no EOS "
		"contact for it (the manual's flipper switch table orders the single-stack assembly 6S "
		"qty 2 and the double-stack 6D qty 0, so no flipper EOS contacts are fitted at all)."),
	87: ("Upper Right Flipper Button (not fitted)", "D-15",
		"Printed DED #15. Structurally unwritten as well as unfitted: bbhGameData's hw.flippers "
		"is FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), so core.c's locals.flipMask never includes the "
		"upper-right button bit, and the retained script never writes address 87."),
	88: ("Upper Right Flipper EOS (not fitted)", "D-16",
		"Printed DED #16. Unfitted and unwritten for the same reason as D-15."),
}

FLIPPER_COLUMN_NOTE = (
	"Read through PinMAME's flipper switch column (CORE_FLIPPERSWCOL = 11). sam.c's "
	"dedswitch_lower_r reverses each nibble of that column to reach the hardware's own D-9 to "
	"D-16 order. sam.c also synthesizes each EOS state from its own flipper-button bit "
	"(data |= (data & (bit8|bit10|bit12|bit14)) << 1, source comment: 'SAM is not using standard "
	"VPM flipper coils, so the EOS simulation does not take place, and the ROM reports technician "
	"errors'), and this machine's parts table fits no EOS contact stack at all (item 6S single "
	"stack qty 2, item 6D double stack qty 0), so the EOS addresses carry emulator-synthesized "
	"copies of their button bits and a recreation does not drive them independently."
)


def matrix_label(address: int) -> tuple[str, str | None, str]:
	"""Return (label, role-note, provenance-status) for a matrix switch from retained evidence."""
	if address == 1:
		return ("Buck Target Hit", "script Buck_Hit and BuckWallIsHit pulse 1", "observed")
	if address == 5:
		return ("Gate switch (upper-left orbit gate)", "script sw5_hit pulses 5; object Gate.sw5", "observed")
	if address == 6:
		return ("Rollover (upper-left lane)", "script SW6_Hit/SW6_unHit; also pulsed by the left magna-save key", "observed")
	if address == 7:
		return ("Rollover (top lane left)", "script SW7_Hit/SW7_unHit", "observed")
	if address == 8:
		return ("Rollover (top lane middle)", "script SW8_Hit/SW8_unHit", "observed")
	if address == 9:
		return ("Rollover (top lane right)", "script SW9_Hit/SW9_unHit", "observed")
	if address == 10:
		return ("Stand-Up Target", "script sw10_hit pulses 10; object HitTarget.sw10", "observed")
	if address == 11:
		return ("Shooter-Lane Launch / Plunger", "script clears Controller.Switch(11) when the plunger fires; nothing in the retained script or manual sets it, so the setter (plunger-lane sensor or key handler in the shared core vbs) is unresolved", "candidate")
	if address == 13:
		return ("Rollover (upper-right)", "script SW13_Hit/SW13_unHit", "observed")
	if address == 14:
		return ("Gate switch (right orbit gate)", "script sw14_hit pulses 14; object Gate.sw14", "observed")
	if address == 15:
		return ("Tournament Start Button", "platform input: sam.c's SAM_COMPORTS assigns the Tournament Start key to the switch-column-2 bit that core_swSeq2m places at public 15; the cabinet button is manual item 4T (500-6587-06-TL, yellow square, switch+lamp)", "validated")
	if address == 16:
		return ("Start Button", "platform input: sam.c's SAM_COMPORTS assigns the Start key to the switch-column-2 bit that core_swSeq2m places at public 16; the cabinet button is manual item 3S (500-6388-44-TL, green round, switch+lamp)", "validated")
	if address == 18:
		return ("Trough #4 (entry, left)", "script trough ball stack order 21,20,19,18; manual cut-away label SW. 18 on a roller microswitch (item 9, 180-5119-02)", "validated")
	if address == 19:
		return ("Trough #3", "script trough order; manual cut-away label SW. 19 on a roller microswitch", "validated")
	if address == 20:
		return ("Trough #2", "script trough order; the manual orders three roller microswitches (item 9, qty 3) and labels two of them SW. 18 and SW. 19, so the third is this position by the assembly's own count and the script's order", "observed")
	if address == 21:
		return ("Trough #1 (kicker position, dual-opto board)", "script trough order; manual cut-away label SW. 21 on the dual opto board pair (items 12/13, 515-0173-00 / 515-0174-00)", "validated")
	if address == 22:
		return ("Trough Exit Opto", "manual cut-away label SW. 22 on the dual opto board pair; " + THROUGH_EXIT_PULSE_NOTE, "validated")
	if address == 23:
		return ("Shooter Lane", "script SW23_Hit/SW23_unHit maintained; Trigger.sw23 sits co-located with Trigger.swPlunger at the shooter lane", "observed")
	if address == 24:
		return ("Rollover (lower-left outlane area)", "script SW24_Hit/SW24_unHit", "observed")
	if address == 25:
		return ("Rollover (left inlane area)", "script SW25_Hit/SW25_unHit", "observed")
	if address == 26:
		return ("Left Slingshot", "script LeftSlingShot_Slingshot pulses 26", "observed")
	if address == 27:
		return ("Right Slingshot", "script RightSlingShot_Slingshot pulses 27", "observed")
	if address == 28:
		return ("Rollover (right inlane area)", "script SW28_Hit/SW28_unHit", "observed")
	if address == 29:
		return ("Rollover (lower-right outlane area)", "script SW29_Hit/SW29_unHit", "observed")
	if address == 30:
		return ("Pop Bumper (script Bumper2)", "script Bumper2_Hit pulses 30", "observed")
	if address == 31:
		return ("Pop Bumper (script Bumper3)", "script Bumper3_Hit pulses 31", "observed")
	if address == 32:
		return ("Pop Bumper (script Bumper1)", "script Bumper1_Hit pulses 32", "observed")
	if address == 33:
		return ("Rollover (right side)", "script SW33_Hit/SW33_unHit", "observed")
	if address == 34:
		return ("Kickback Ram Ball Sense", "script sw34_Hit/sw34_UnHit maintained with the RamFire kick logic; object Kicker.sw34", "observed")
	if address == 35:
		return ("Stand-Up Target", "script sw35_hit pulses 35; object HitTarget.sw35", "observed")
	if address == 36:
		return ("Stand-Up Target", "script sw36_hit pulses 36; object HitTarget.sw36", "observed")
	if address == 37:
		return ("Buck Drive Position Opto A", "named 'opto switch 37' by the retained script's commented-out Buck animation code; the magna-save right key also pulses it as a manual Buck-advance convenience", "candidate")
	if address == 38:
		return ("Stand-Up Target", "script sw38_hit pulses 38; object HitTarget.sw38", "observed")
	if address == 39:
		return ("Stand-Up Target", "script sw39_hit pulses 39; object HitTarget.sw39", "observed")
	if address == 40:
		return ("Stand-Up Target", "script sw40_hit pulses 40; object HitTarget.sw40", "observed")
	if address == 41:
		return ("Stand-Up Target", "script sw41_hit pulses 41; object HitTarget.sw41", "observed")
	if address == 42:
		return ("Stand-Up Target", "script sw42_hit pulses 42; object HitTarget.sw42", "observed")
	if address == 43:
		return ("Rollover (upper playfield)", "script sw43_Hit/sw43_unHit maintained; object Trigger.sw43", "observed")
	if address == 44:
		return ("Spinner", "script sw44_Spin pulses 44; object Spinner.sw44", "observed")
	if address == 45:
		return ("Buck Drive Position Opto B", "named 'opto switch 45' by the retained script's commented-out Buck animation code", "candidate")
	return (f"Unidentified switch {address}", None, "candidate")


UNKNOWN_MATRIX_SWITCHES = frozenset(
	set(range(1, 65)) - set(SWITCH_POSITIONS) - {1, 11, 15, 16, 18, 19, 20, 21, 22, 37, 45}
)


def _matrix_switch(address: int) -> dict[str, Any]:
	label, role_note, status = matrix_label(address)
	device: dict[str, Any] = {
		"id": f"switch.matrix-{address}",
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": address},
		"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
		"provenance": provenance(*(SCRIPT_REFS + (MANUAL_SOURCE,) if address in (18, 19, 20, 21, 22) else SCRIPT_REFS), status=status),
	}
	notes: list[str] = []
	physical: dict[str, Any] = {}
	if address in UNKNOWN_MATRIX_SWITCHES:
		device["availability"] = "unknown"
		notes.append(
			"No retained source names or binds this address: the partial manual carries no switch "
			"matrix table, and the retained script defines no handler for it. The ROM may use it; "
			"failing to observe an address is never proof that it is unused."
		)
	else:
		device["availability"] = "used"
		if role_note:
			notes.append(f"Retained-evidence role: {role_note}.")
		if address in (18, 19, 20):
			physical["part_number"] = "180-5119-02"
			physical["switch_type"] = "microswitch"
			notes.append(
				"Manual PDF page 3: trough item 9 is three Micro Switch (Roller Actuator, Lite-Force) "
				"180-5119-02 with item 10 protect plates, and the cut-away labels two of them SW. 18 "
				"and SW. 19. Mechanical, normally-open-when-rested construction is the roller "
				"actuator's own; the emulator normalizes nothing (see "
				"conflict.sam-invsw-never-populated for the platform-wide polarity caveat)."
			)
		if address in (21, 22):
			physical["part_number"] = "515-0173-00 (TX) / 515-0174-00 (RX)"
			physical["switch_type"] = "opto"
			physical["location"] = "dual opto transmitter/receiver boards at the trough exit"
			notes.append(
				"Manual PDF page 3: trough items 12/13 are the Dual OPTO TRANS (515-0173-00) and Dual "
				"OPTO REC (515-0174-00) board assemblies, and the cut-away labels them SW. 22 and "
				"SW. 21. " + ("Position 21 is the kicker-side opto of the pair; position 22 is the "
				"exit opto the served ball crosses. " if address == 21 else THROUGH_EXIT_PULSE_NOTE + " ")
				+ "Pinned PinMAME normalizes no switch state on this platform, so the public state "
				"carries the raw hardware polarity; see conflict.sam-invsw-never-populated."
			)
		if address in (37, 45):
			physical["switch_type"] = "opto"
			notes.append(
				"Construction opto per the retained script's own commented labels ('opto switch 37', "
				"'opto switch 45'); the manual's deer-track assembly page (PDF page 12) shows the "
				"track's actuator but carries no electrical table, so the switch count and exact "
				"addresses behind the Buck drive are not independently confirmed. The retained table "
				"does not assert either address at runtime; its Buck feedback is the substitute "
				"writes on the unfitted UK post-save addresses 71/72 instead."
			)
		if address == 11:
			notes.append(
				"The retained script's only touch is Controller.Switch(11) = 0 in Table1_KeyUp when "
				"the plunger fires; no handler sets it. Whether the factory sensor is the shooter-lane "
				"opto pair, a plunger-position switch, or a key-mapped cabinet control cannot be "
				"settled from the retained evidence, and no harness trace has been run for it yet."
			)
		if address in (15, 16):
			physical["switch_type"] = "button"
			physical["location"] = "cabinet front"
			physical["part_number"] = "500-6587-06-TL" if address == 15 else "500-6388-44-TL"
			notes.append(
				"A cabinet button, not a playfield switch: it lives inside the matrix numbering only "
				"because the S.A.M. platform reads it through switch column 2. The manual's cabinet "
				"parts table carries the physical assembly (item 4T yellow square / 3S green round, "
				"each switch+lamp with diodes and a 3-lug terminal strip inside the cabinet)."
			)
		if address in (30, 31, 32):
			notes.append(
				"The three pop bumpers are recorded by the retained script's own numeric binding "
				"(Bumper1 -> 32, Bumper2 -> 30, Bumper3 -> 31) together with the objects' geometry; "
				"no manual table exists to name them left/right/bottom, so no such name is asserted."
			)
		if address in SWITCH_PROJECTIONS:
			device["spatial"] = placed(f"switch.matrix-{address}", "sensor", (SWITCH_PROJECTION_RAW[address],), *GEOMETRY_REFS, status="observed")
		elif address in SWITCH_POSITIONS:
			device["spatial"] = placed(f"switch.matrix-{address}", "sensor", (SWITCH_POSITIONS[address],), *GEOMETRY_REFS)
		else:
			device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
	physical["notes"] = " ".join(notes)
	device["physical"] = physical
	return device


def _dedicated_switch(address: int) -> dict[str, Any]:
	label, d_number, extra = DEDICATED_SWITCHES[address]
	if 65 <= address <= 72:
		identifier = f"switch.dedicated-{address}"
		board_note = "Read through sam.c's dedswitch_lower_r, which returns coreGlobals.swMatrix[9] as the low byte of the lower dedicated-switch word."
	elif 81 <= address <= 88:
		identifier = f"switch.flipper-{address}"
		board_note = (
			f"Printed dedicated switch {d_number}. " + FLIPPER_COLUMN_NOTE
		)
	else:
		identifier = f"switch.service-d{24 + address}"
		board_note = "Read through sam.c's dedswitch_upper_r, which returns coreGlobals.swMatrix[0] as the low byte of the upper dedicated-switch word; these are the negative diagnostic addresses."
	unfitted = address in (71, 72, 87, 88)
	unused = address in (-4, 70, 87, 88)
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": address},
		"aliases": [
			{"namespace": "pinmame.switch", "value": str(address)},
			{"namespace": "manual.address", "value": f"SW. {d_number} (sam.c comment map)"},
		],
		"availability": "unused" if unused else "used",
		"provenance": provenance(CORE_SOURCE, status="validated"),
	}
	notes = [board_note]
	physical: dict[str, Any] = {}
	if extra:
		notes.append(extra)
	if unfitted:
		if address in (71, 72):
			device["availability"] = "used"
			notes.append(
				"The address is live: the retained table writes it (see the label note), and the "
				"ROM's dedicated-switch handler reads the byte regardless of whether the optional "
				"hardware is fitted."
			)
		else:
			notes.append(
				"Structurally unwritten as well as unfitted: nothing in the retained script, the "
				"platform input ports, or core.c's flipper mask drives this address on this game."
			)
	if address == 85:
		device["availability"] = "used"
	if address in (-7, -6, -5, -4, -3, -2, -1, 0):
		device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
	elif address in (65, 66, 67, 68, 69, 70):
		device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		if address == 65:
			notes.append(
				"The manual's coin door is a '2-Cht' (two-chute) door (cabinet item 17, 501-5018-172) "
				"with coin door switches item 19 (180-5024-01, qty 2) -- exactly two chute switches. "
				"Which two of the four printed chute functions (left/center/right/fourth) the factory "
				"harness lands on D-1 to D-4 is not stated by any retained source; the platform "
				"structure and this machine's two fitted chutes are both recorded, and the mapping "
				"stays open."
			)
	elif address in (81, 82, 83, 84, 85, 86, 87, 88):
		device["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
	physical["notes"] = " ".join(notes)
	device["physical"] = physical
	return device


def _dip_switch(position: int) -> dict[str, Any]:
	return {
		"id": f"dip.sw1-{position}",
		"label": f"CPU/Sound Board SW1 DIP Position #{position}",
		"kind": "dip_switch",
		"binding": {"group": "pinmame.input.dip", "device": position},
		"aliases": [
			{"namespace": "pinmame.dip", "value": str(position)},
			{"namespace": "manual.address", "value": f"SW. D-{24 + position} (sam.c comment map)"},
		],
		"availability": "used",
		"physical": {
			"location": "CPU/Sound board SW1 bank",
			"notes": (
				f"Read through sam.c's dedswitch_upper_r as the high byte of the upper dedicated-switch "
				f"word (printed DED #{{}} on the platform's own comment map) and exposed on PinMAME's DIP "
				"channel, not as a switch address. sam.c's SAM_COMPORTS declares the low five bits as the "
				"country setting (29 values from USA through Unknown) with positions 6, 7 and 8 as "
				"standalone dips, position 8 defaulting on. This machine's partial manual carries no DIP "
				"block; the platform structure is the whole record."
			).replace("{}", str(24 + position)),
		},
		"spatial": not_applicable("dip_switch", CORE_SOURCE),
		"provenance": provenance(CORE_SOURCE),
	}


def input_devices() -> list[dict[str, Any]]:
	devices = [_dedicated_switch(address) for address in sorted(DEDICATED_SWITCHES) if address <= 0]
	devices += [_matrix_switch(address) for address in range(1, 65)]
	devices += [_dedicated_switch(address) for address in sorted(DEDICATED_SWITCHES) if address > 0]
	devices += [_dip_switch(position) for position in range(1, 9)]
	return devices

# --- Outputs -------------------------------------------------------------------------------------

# Solenoid addresses bound by the retained script (active callbacks only).
SCRIPT_SOLENOIDS = (1, 2, 3, 4, 7, 12, 14, 15, 16, 19, 20, 21, 22, 23, 25, 26, 27, 29, 31, 32)
# Flasher pseudo-lamp channels the script's SolCallback "Setlamp" lines drive; these numbers sit
# above the 80-address lamp transport and are the table's own render channels.
FLASHER_PSEUDO_LAMPS = {19: 119, 20: 120, 21: 121, 22: 122, 25: 125, 26: 126, 27: 127, 29: 129, 31: 131, 32: 132}

SOLENOID_LABELS: dict[int, tuple[str, str, str]] = {
	# address: (label, kind, notes)
	1: ("Trough Up-Kicker", "coil",
		"Retained script SolCallback(1) = solTrough ejects one ball via the cvpmBallStack and pulses "
		"switch 22 on the way out. Manual PDF page 3: the trough coil is item 4, coil 26-1200 with "
		"NO DIODE (part 090-5044-ND), drawn with the label Q1, plunger 515-7309-01 (3.57 inch), "
		"sleeve 545-5076-01, return spring 266-5020-00, on cable harness 038-5508-04 with a 3-pin "
		"connector 045-5007-03 and a 12-pin connector 045-5007-12."),
	2: ("Auto Launch Plunger", "coil",
		"Retained script SolCallback(2) = solAutofire fires the cvpmImpulseP plunger. The cabinet's "
		"ball shooter assembly is manual cabinet item 16 (500-6146-00-04)."),
	3: ("Buck Drive Direction (right or backwards)", "coil",
		"Retained script SolCallback(3) = 'solBuckRight' with the printed comment 'right or "
		"backwards'; the callback body is commented away and the table animates the Buck itself, so "
		"the runtime consequence of this address is observed only through the script's wiring "
		"intent, not through exercised behavior."),
	4: ("Buck Drive Direction (left or forwards)", "coil",
		"Retained script SolCallback(4) = 'solBuckLeft' with the printed comment 'left or forwards'; "
		"body commented away like solenoid 3."),
	5: ("Buck Drive Motor", "motor",
		"Retained script carries SolCallback(5) = \"solBuckMotor\" commented out entirely, naming "
		"the Buck drive motor as the intended device. The physical mechanism's drive is real (the "
		"deer-track assembly page and the ram/toy assemblies exist), but neither the motor's part "
		"number nor its electrical address appears in any retained table, so even the address-to-"
		"device direction of this line rests on the table author alone."),
	7: ("Up/Down Post (bird orbit post)", "coil",
		"Retained script SolCallback(7) = birdorbitpost raises/lowers the BUpPost wall at "
		"(442.5, 462.3). The manual's up/down post assemblies are PDF page 19 (500-7153-04, coil "
		"26-1200 NO DIODE drawn Q12) and the ball-deflect post pages; which assembly number this "
		"address drives is not stated by any retained table."),
	12: ("Kickback Ram Coil", "coil",
		"Retained script SolCallback(12) = SolKickBack whose body is commented away ('Kick is "
		"handled by ramb kicker, so ball does not get stuck in kicker'), with the table kicking via "
		"Kicker.sw34 instead. Manual PDF page 18: the ram kicker's coil is item 5, COIL - 23-800, "
		"NO DIODE (part 090-5001-ND), plunger 515-7726-00, on the 500-7166-00 assembly; PDF page 16 "
		"shows the ram toy itself (860-5110-04-ASY) on its 550-7163-00 prime assembly."),
	14: ("Elk Diverter Flipper", "coil",
		"Retained script SolCallback(14) = SolLElk rotates the Elkdiverter flipper object to End and "
		"swaps dropped walls sw85/sw85a (the diverter gate), driven by the Elk button on switch 85. "
		"The manual's upper mini-flipper assembly (PDF page 9 area of the Blue Pages) is the "
		"physical counterpart; its parts table was rendered and read during the pass but the "
		"assembly page carries no electrical address."),
	15: ("Left Flipper Coil", "coil",
		"S.A.M. flippers are fully CPU-controlled through a single ordinary numbered solenoid each: "
		"sam.c writes only coreGlobals.solenoids and the physical output array and never touches "
		"coreGlobals.solenoids2, so public 45-48 stay dead on this platform. The retained script "
		"confirms the binding directly with SolCallback(15) = SolLFlipper. sam.c drives a 40 ms "
		"power pulse then a 1 ms hold every 12 ms (solenoids 13-16 carry a 14 ms switchDownLatency "
		"for this reason), so the one address carries both phases."),
	16: ("Right Flipper Coil", "coil",
		"Retained script SolCallback(16) = SolRFlipper; same single-address power/hold convention "
		"as solenoid 15."),
	19: ("Flasher String (script lamp channel 119)", "flasher",
		"Retained script SolCallback(19) = 'Setlamp 119'. sam.c's bbh_ block types solenoids 19-22 "
		"as #89 bulbs, under its own comment that this typing was completed from the VPX table plus "
		"a backglass flasher map rather than from a manual. The script's channel-119 visual is the "
		"Light L119 at raw (668.26, 432.33) on the playfield."),
	20: ("Flasher String (script lamp channel 120)", "flasher",
		"Retained script SolCallback(20) = 'Setlamp 120'; script visuals are the dome Primitive l120 "
		"(raw 121.0, 90.75) plus Light l120a (raw 123.14, 91.30), co-located at the playfield's "
		"upper-left edge."),
	21: ("Flasher String (script lamp channel 121)", "flasher",
		"Retained script SolCallback(21) = 'Setlamp 121'; script visual is the Light L121 at raw "
		"(447.58, 297.16), exactly co-located with the l33 lamp insert."),
	22: ("Flasher String (script lamp channel 122)", "flasher",
		"Retained script SolCallback(22) = 'Setlamp 122'; script visuals are dome Primitive l122 "
		"(raw 784.58, 186.36 area) plus Light l122a at the same point, upper-right."),
	23: ("Up/Down Post (top orbit post)", "coil",
		"Retained script SolCallback(23) = orbitpost raises/lowers the UpPost wall at (490.8, 58.0) "
		"at the very top of the playfield. Same up/down post assembly family as solenoid 7."),
	25: ("Flasher String (script lamp channel 125, four bulbs down the left side)", "flasher",
		"Retained script SolCallback(25) = 'Setlamp 125' driving four script lights L125a-d at raw "
		"(60.8, 1050.6), (61.9, 932.3), (60.0, 892.8) and (57.9, 1090.8) -- one driver, four "
		"emitters, so the address carries four placements."),
	26: ("Flasher String (script lamp channel 126)", "flasher",
		"Retained script SolCallback(26) = 'Setlamp 126' with the Flash 126/f126 glow object; the "
		"f126 Flasher's drag points run raw (483.96, 759.12) to (473.27, 1249.42), a tall mid-"
		"playfield shape whose centroid is the placement."),
	27: ("Flasher String (script lamp channel 127, four bulbs upper center-left)", "flasher",
		"Retained script SolCallback(27) = 'Setlamp 127' driving L127a-d at raw (359.5, 269.0), "
		"(376.6, 345.7), (223.7, 309.2) and (248.6, 403.4) -- one driver, four emitters."),
	29: ("Flasher String (script lamp channel 129)", "flasher",
		"Retained script SolCallback(29) = 'Setlamp 129'; visuals are flasher Primitive L129 (raw "
		"858.3, 977.6) plus Light L129a, right side."),
	31: ("Flasher String (script lamp channel 131)", "flasher",
		"Retained script SolCallback(31) = 'Setlamp 131'; visuals are dome Primitive l131 (raw "
		"191.9, 1600.7) plus Light l131a, lower left. Two further unbound lights named f131a1 "
		"(raw 194.5, 1405.7) and f131a2 (raw 630.4, 1412.8) exist in the table and bind to no "
		"callback; they are recorded in the geometry dump and deliberately not promoted."),
	32: ("Flasher String (script lamp channel 132)", "flasher",
		"Retained script SolCallback(32) = 'Setlamp 132'; visuals are dome Primitive l132 (raw "
		"639.2, 1605.1) plus Light l132a, lower right."),
}

# Raw coordinates for placed solenoid effects/emitters.
SOLENOID_POSITIONS: dict[int, tuple[tuple[float, float], ...]] = {
	1: ((852.172, 1858.0284),),
	2: ((922.8474, 2081.804),),
	3: ((671.0, 803.0),),
	4: ((671.0, 803.0),),
	5: ((671.0, 803.0),),
	7: ((442.5243, 462.26132),),
	12: ((290.9301, 298.69608),),
	14: ((784.18024, 1209.82),),
	15: ((252.5, 1794.5),),
	16: ((573.0, 1798.5),),
	19: ((668.2641, 432.33243),),
	20: ((123.138695, 91.298416),),
	21: ((447.58118, 297.16455),),
	22: ((784.5765, 186.35907),),
	23: ((490.7743, 58.011326),),
	25: ((60.83334, 1050.5553), (61.944374, 932.3333), (59.96901, 892.76105), (57.862015, 1090.819)),
	26: ((478.6152, 1004.2683),),
	27: ((359.5, 269.0), (376.6111, 345.66672), (223.72215, 309.22223), (248.61105, 403.4445)),
	29: ((859.0838, 977.35767),),
	31: ((191.5263, 1603.7457),),
	32: ((639.84985, 1608.1324),),
}

SOLENOID_PROJECTIONS: dict[int, str] = {
	1: "Below-playfield coil; placed at its own ball-release kicker's position like the trough "
	"sensors, the standard thin-table trough projection.",
	2: "The auto-launch coil sits behind the plunger assembly; placed at the Plunger object's "
	"position as the assembly's own anchor.",
	3: "The Buck drive's coils and motor live inside the moving-target mechanism below/behind the "
	"track; all three project onto the Buck target's home position (Primitive.Buck), the mechanism's "
	"own fixed anchor, disclosed as a projection rather than a coil-body coordinate.",
	4: "See solenoid 3's projection note.",
	5: "See solenoid 3's projection note.",
	12: "Below-playfield coil; placed at the Kicker.sw34 ball-sense position it serves, disclosed "
	"as an assembly anchor rather than the coil body's own coordinate.",
	14: "The Elk diverter's coil is inside the mini-flipper assembly; placed at the Elkdiverter "
	"flipper object's own pivot.",
	15: "The flipper coil sits inside the flipper assembly below the playfield; placed at the "
	"LeftFlipper object's own pivot as the assembly's anchor, not the coil body's coordinate.",
	16: "See solenoid 15's projection note (RightFlipper pivot).",
	26: "The f126 flasher is a tall shape carried by drag points; placed at the centroid of its "
	"four drag points, recorded as a derivation rather than a measured center.",
}

UNKNOWN_SOLENOIDS = (6, 8, 9, 10, 11, 13, 17, 18, 24, 28, 30)

VIRTUAL_SOLENOIDS: dict[int, tuple[str, str, str]] = {
	33: (
		"PinMAME SAM game-on state",
		"virtual",
		"PinMAME's synthetic S.A.M. game-on state, not a driver-board transistor. sam.c's VBLANK "
		"handler reads one byte of game RAM at samlocals.fastflipaddr -- 0x0106acae, set for bbh_170 "
		"only -- and publishes the result on public solenoid address 33 (SAM_FASTFLIPSOL), with "
		"core.c's own comment '33 SAM fake GameOn sol for fast flips'. sam.c explicitly declares it "
		"CORE_MODOUT_NONE so it carries no bulb or coil physics. Because only the 1.7 parent has a "
		"fast-flip watch address, a consumer should expect this state to toggle on bbh_170 and to "
		"stay low on the three earlier revisions.",
	),
	34: ("Unused (S.A.M. reads the game-on state here)", "virtual", ""),
	35: ("Unused (S.A.M. reads the game-on state here)", "virtual", ""),
	36: ("Unused (S.A.M. reads the game-on state here)", "virtual", ""),
	37: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	38: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	39: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	40: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	41: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	42: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	43: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	44: ("Unused S.A.M. extra-solenoid address", "virtual", ""),
	45: ("Unused legacy lower-right flipper power address", "virtual", ""),
	46: ("Unused legacy lower-right flipper hold address", "virtual", ""),
	47: ("Unused legacy lower-left flipper power address", "virtual", ""),
	48: ("Unused legacy lower-left flipper hold address", "virtual", ""),
	49: ("PinMAME built-in ball simulator output", "virtual", ""),
	50: ("PinMAME reserved simulated output", "virtual", ""),
}

VIRTUAL_SOLENOID_GROUP_NOTES = {
	"34-36": (
		"Enumerated but carries no state a consumer can use. core_getSol's 33-36 branch returns the "
		"same synthetic game-on bit for every address in the range when the generation is GEN_SAM, "
		"but the two aggregate paths a consumer actually reads through -- core_getAllSol and "
		"core_getAllPhysicSols -- publish the game-on state at address 33 only and leave 34-36 at "
		"zero. No driver-board transistor exists behind any of them."
	),
	"37-44": (
		"Enumerated by PinMAME's S.A.M. extra-solenoid range but never written for this platform. "
		"core_getAllSol and core_getAllPhysicSols mirror internal solenoid indices 41-48 into public "
		"37-44 for GEN_ALLS11 | GEN_SAM | GEN_SPA, and sam.c writes nothing to those indices; "
		"core_getSol's own 37-44 branch does not even list GEN_SAM, so it returns zero."
	),
	"45-48": (
		"PinMAME's legacy lower-flipper addresses, dead on this platform. They are computed from "
		"coreGlobals.solenoids2, which sam.c only ever writes as the game-on bit, and "
		"coreGlobals.hasModulatedFlippers is never set for S.A.M. This game's two flipper coils are "
		"the ordinary numbered solenoids 15 and 16."
	),
	"49-50": (
		"PinMAME's own built-in ball simulator outputs (CORE_FIRSTSIMSOL = 49), answered by "
		"sim_getSol. The retained known-working script implements its own ball handling through "
		"cvpmBallStack and cvpmImpulseP instances and never references either address."
	),
}

AUX_SOLENOID_NOTE = (
	"Enumerated because sam.c's INITGAME macro hardcodes hw.custSol = 16 for every Stern S.A.M. "
	"game, so coreGlobals.nSolenoids is always CORE_FIRSTCUSTSOL - 1 + 16 = 66 and LibPinMAME's "
	"ChangedSolenoids contract always covers 51-66. Nothing can write them on this machine: "
	"bbhGameData declares SAM_NO_AUX with gameSpecific1 = 0, and every one of sam.c's auxiliary "
	"write paths (SAM_GAME_AUXSOL8_CSTB, SAM_GAME_AUXSOL8_DSTB, SAM_GAME_AUXSOL6, "
	"SAM_GAME_AUXSOL12, SAM_GAME_ACDC_FLAMES, SAM_GAME_METALLICA_MAGNET, SAM_GAME_IJ4) is gated "
	"behind a gameSpecific1 bit this game does not set (sam.c lines 1127-1163). The partial manual "
	"prints no coil table and no auxiliary driver board."
)


def _solenoid(address: int) -> dict[str, Any]:
	if address in UNKNOWN_SOLENOIDS:
		label, kind, notes_text = (
			f"Unidentified output {address}",
			"coil",
			"No retained source binds or names this address: the partial manual carries no coil "
			"table, and the retained script defines no callback. sam.c's bbh_ block additionally "
			"types addresses 19-22 and 25-32 as #89-bulb flasher strings under a comment "
			"acknowledging the typing was reconstructed from the community table rather than a "
			"manual, so even the emulator's own class metadata is ancestral to the table retained "
			"here and is recorded, not trusted. The device class below is the driver bank's generic "
			"coil record; the ROM may drive this address at runtime. Failing to observe an address "
			"is never proof that it is unused."
		)
		device: dict[str, Any] = {
			"id": f"solenoid.{address}",
			"label": label,
			"kind": kind,
			"binding": {"group": "pinmame.output.solenoid", "device": address},
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
			"availability": "unknown",
			"physical": {"notes": notes_text},
			"provenance": provenance(CORE_SOURCE, status="candidate"),
		}
		return device
	label, kind, notes_text = SOLENOID_LABELS[address]
	device = {
		"id": f"solenoid.{address}",
		"label": label,
		"kind": kind,
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
		"availability": "used",
		"physical": {"notes": notes_text},
		"provenance": provenance(*(SCRIPT_REFS + (MANUAL_SOURCE,) if address in (1, 2, 12) else SCRIPT_REFS),
			status="observed" if address in (3, 4, 5) else "validated"),
	}
	if address in SOLENOID_POSITIONS:
		role = "emitter" if kind == "flasher" else "effect"
		status = "observed" if address in SOLENOID_PROJECTIONS else "validated"
		device["spatial"] = placed(f"solenoid.{address}", role, SOLENOID_POSITIONS[address], *GEOMETRY_REFS, status=status)
	else:
		raise RuntimeError(f"solenoid {address} has no spatial disposition")
	if address in SOLENOID_PROJECTIONS:
		device["physical"]["notes"] = device["physical"]["notes"] + " Placement projection: " + SOLENOID_PROJECTIONS[address]
	return device


def _virtual_solenoid(address: int) -> dict[str, Any]:
	label, kind, note = VIRTUAL_SOLENOIDS[address]
	if not note:
		for span, text in VIRTUAL_SOLENOID_GROUP_NOTES.items():
			low, high = (int(part) for part in span.split("-"))
			if low <= address <= high:
				note = text
				break
	return {
		"id": f"solenoid.{address}",
		"label": label,
		"kind": kind,
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
		"availability": "used" if address == 33 else "unused",
		"physical": {"notes": note},
		"spatial": not_applicable("virtual", CORE_SOURCE),
		"provenance": provenance(CORE_SOURCE),
	}


def _aux_solenoid(address: int) -> dict[str, Any]:
	return {
		"id": f"solenoid.{address}",
		"label": f"Auxiliary driver output {address - 50} (no auxiliary board fitted)",
		"kind": "coil",
		"binding": {"group": "pinmame.output.solenoid", "device": address},
		"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
		"availability": "unused",
		"physical": {"notes": AUX_SOLENOID_NOTE},
		"spatial": not_applicable("unused", CORE_SOURCE),
		"provenance": provenance(CORE_SOURCE),
	}


def solenoid_outputs() -> list[dict[str, Any]]:
	devices = [_solenoid(address) for address in range(1, 33)]
	devices += [_virtual_solenoid(address) for address in sorted(VIRTUAL_SOLENOIDS)]
	devices += [_aux_solenoid(address) for address in range(51, 67)]
	return devices


# --- Lamps ---------------------------------------------------------------------------------------
# The retained script's UpdateLamps binds exactly these 57 lamp addresses by name (JP-style
# ChangedLamps fade loop). Lamp addresses the script never touches are recorded as unknown: no
# lamp matrix table exists to prove them unused.
SCRIPT_BOUND_LAMPS = frozenset(
	{3, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
	 31, 32, 33, 35, 38, 39, 40, 41, 42, 43, 45, 46, 47, 49, 50, 51, 52, 53, 54, 55, 57, 59, 60,
	 61, 62, 63, 65, 66, 67, 68, 69, 70}
)

# Raw retained-table coordinates for bound lamp objects.
LAMP_POSITIONS: dict[int, tuple[tuple[float, float], ...]] = {
	3: ((417.5761, 1940.7324),),
	5: ((51.824547, 1484.6165),),
	6: ((127.31924, 1422.9136),),
	7: ((701.1161, 1409.184),),
	8: ((773.25, 1393.625),),
	9: ((833.3748, 1511.0719),),
	10: ((802.55554, 863.93475),),
	11: ((852.47943, 757.3181),),
	14: ((96.61975, 619.4819),),
	15: ((132.75125, 748.5911),),
	16: ((216.40988, 1355.1029),),
	17: ((311.36407, 1275.3182),),
	18: ((407.1638, 1195.9286),),
	19: ((500.12546, 1112.1036),),
	20: ((594.59467, 1024.9525),),
	21: ((684.5383, 1024.0298),),
	22: ((759.2687, 947.01105),),
	23: ((615.36523, 264.96088),),
	24: ((672.124, 275.77234),),
	25: ((732.04565, 264.57236),),
	26: ((682.25, 1249.625),),
	31: ((465.90936, 554.2706),),
	32: ((335.57117, 522.1159),),
	33: ((447.58118, 297.16455),),
	35: ((359.59793, 675.92175),),
	38: ((162.48294, 835.93243),),
	39: ((189.80449, 491.45508),),
	40: ((209.3053, 572.1995),),
	41: ((290.64902, 888.43536),),
	42: ((387.35382, 767.04944),),
	43: ((270.0342, 799.37427),),
	45: ((169.55843, 922.2237),),
	46: ((166.9535, 1001.3181),),
	47: ((166.71669, 1081.3599),),
	49: ((418.97375, 1746.6807),),
	50: ((417.63367, 1670.2086),),
	51: ((418.60693, 1590.2739),),
	52: ((417.63367, 1498.2897),),
	53: ((413.7701, 1366.748),),
	54: ((549.0824, 537.65784),),
	55: ((470.85788, 642.8634),),
	57: ((774.4212, 606.2197),),
	59: ((413.75552, 628.9425),),
	60: ((557.30774, 346.6057),),
	61: ((796.74426, 351.05814),),
	62: ((681.85297, 560.557),),
	63: ((645.61676, 705.813),),
	65: ((298.74973, 1434.9374),),
	66: ((327.07913, 1534.5922),),
	67: ((301.06604, 1631.1921),),
	68: ((533.08105, 1438.2239),),
	69: ((507.1551, 1535.8687),),
	70: ((536.7309, 1633.2694),),
}

# Lamps whose only retained visuals are four stacked Primitive bulbs sharing one position
# (L27-L30 at raw 401.3, 263.9, z 290) with Flash-glow partners f27-f30 clustered around raw
# (352.5, 250-371). Four physical bulbs cannot share one point and the stack gives no basis
# for four distinct positions, so these four carry no spatial key and the stack is disclosed.
STACKED_PRIMITIVE_LAMPS = frozenset({27, 28, 29, 30})

LAMP_EXTRA_NOTES: dict[int, str] = {
	16: "One of the five Buck path lamps (16-20): the retained table's Buck driver follows whichever "
	"of these is flashing and walks the Buck target to it, so these five addresses are load-bearing "
	"mechanism inputs for the table's substitute Buck animation.",
	17: "Buck path lamp; see lamp 16.",
	18: "Buck path lamp; see lamp 16.",
	19: "Buck path lamp; see lamp 16.",
	20: "Buck path lamp; see lamp 16.",
	57: "The Buck Super Jackpot lamp: the retained table's Buck driver treats a flashing lamp 57 as "
	"a three-position super-jackpot mode and shuttles the Buck between the lamp 16/17/18 columns.",
	60: "Bumper 1 body light, co-located with Bumper.Bumper1 (the object the script binds to switch 32).",
	61: "Bumper 2 body light, co-located with Bumper.Bumper2 (switch 30).",
	62: "Bumper 3 body light, co-located with Bumper.Bumper3 (switch 31).",
	65: "Auxiliary lamp column address: sam.c sets coreGlobals.nLamps = 64 + lampCol * 8 = 80 "
	"(lampCol = SAM_2COL), and rows 9-10 of the lamp transport carry public 65-80. The script binds "
	"six of the sixteen auxiliary addresses (65-70) to named playfield lights; the other ten are "
	"unknown, not unused.",
	66: "Auxiliary lamp column address; see lamp 65.",
	67: "Auxiliary lamp column address; see lamp 65.",
	68: "Auxiliary lamp column address; see lamp 65.",
	69: "Auxiliary lamp column address; see lamp 65.",
	70: "Auxiliary lamp column address; see lamp 65.",
}


def _lamp(address: int) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": f"lamp.{address}",
		"label": f"Lamp {address}" if address not in LAMP_EXTRA_NOTES or address < 60 else f"Lamp {address}",
		"kind": "lamp",
		"binding": {"group": "pinmame.output.lamp", "device": address},
		"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}],
		"availability": "used" if address in SCRIPT_BOUND_LAMPS else "unknown",
		"provenance": provenance(*SCRIPT_REFS, status="observed" if address in SCRIPT_BOUND_LAMPS else "candidate"),
	}
	notes: list[str] = []
	if address in SCRIPT_BOUND_LAMPS:
		notes.append("Bound by the retained script's UpdateLamps fade loop.")
		if address in (27, 28, 29, 30):
			notes.append(
				"The retained table renders this address as a colored bulb Primitive (L27-L30) stacked "
				"with its three siblings at raw (401.3, 263.9, z 290), each paired with a Flash glow "
				"object (f27-f30) clustered around raw (352.5, 250-371). Four physical bulbs cannot "
				"share one point and the stack gives no basis for four distinct positions, so this "
				"record carries no spatial key; the stack is disclosed in the retained geometry dump."
			)
	else:
		notes.append(
			"No retained source binds or names this address: the partial manual carries no lamp "
			"matrix table, and the retained script's UpdateLamps has no entry for it. The ROM may "
			"drive it at runtime; failing to observe an address is never proof that it is unused."
		)
	if address in LAMP_EXTRA_NOTES:
		notes.append(LAMP_EXTRA_NOTES[address])
	if address in STACKED_PRIMITIVE_LAMPS:
		pass
	elif address in LAMP_POSITIONS:
		device["spatial"] = placed(f"lamp.{address}", "emitter", LAMP_POSITIONS[address], *GEOMETRY_REFS)
	elif address in SCRIPT_BOUND_LAMPS:
		raise RuntimeError(f"bound lamp {address} has no placement and no stack disclosure")
	physical: dict[str, Any] = {"notes": " ".join(notes)}
	device["physical"] = physical
	return device


def lamp_outputs() -> list[dict[str, Any]]:
	return [_lamp(address) for address in range(1, 81)]


def gi_outputs() -> list[dict[str, Any]]:
	return [
		{
			"id": "gi.0",
			"label": "General Illumination",
			"kind": "gi",
			"binding": {"group": "pinmame.output.gi", "device": 0},
			"aliases": [{"namespace": "pinmame.gi", "value": "0"}],
			"availability": "used",
			"physical": {
				"notes": (
					"Stern S.A.M. has exactly one general-illumination channel: sam.c sets coreGlobals.nGI "
					"and drives coreGlobals.gi[0] from its GI latch bit. The retained script matches that "
					"shape and then goes further: its UpdateGI ignores the string index entirely and "
					"switches one 27-member GI collection (GI_1..GI_27) plus an empty GI2 collection for "
					"any index, so a consumer cannot distinguish strings through this table. The partial "
					"manual prints no G.I. bulb inventory; its only related fact is the Back Panel "
					"Assembly's five clear socket & bulb assemblies (item 2, 518-5000-00-HF, qty 5), which "
					"it does not tie to any address. No bulb quantity and no placement set is asserted, "
					"so this record carries no spatial key; the 27 retained GI light positions are in the "
					"geometry dump."
				)
			},
			"provenance": provenance(CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE, status="observed"),
		}
	]


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.dmd",
			"label": "128x32 Dot Matrix Display",
			"kind": "dmd",
			"controller_index": 0,
			"width": 128,
			"height": 32,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE),
			"provenance": provenance(CORE_SOURCE),
		}
	]


# --- Mechanisms, relationships and conflicts -----------------------------------------------------


def mechanisms() -> list[dict[str, Any]]:
	return [
		{
			"id": "mech.ball-trough",
			"label": "Four-Ball Trough",
			"kind": "kicker",
			"actuators": ["solenoid.1"],
			"sensors": [
				"switch.matrix-18",
				"switch.matrix-19",
				"switch.matrix-20",
				"switch.matrix-21",
				"switch.matrix-22",
			],
			"behavior": (
				"A four-ball trough below the playfield, assembly 500-6318-24-ND. The manual's cut-away "
				"(PDF page 3) is the only source that labels its switches, and it does so directly: the "
				"three roller microswitches (item 9, Lite-Force roller actuator 180-5119-02, with item "
				"10 protect plates) carry the printed labels SW. 18 and SW. 19 plus one further "
				"unlabelled switch of the same item, and the dual opto boards (items 12/13, transmitter "
				"515-0173-00 and receiver 515-0174-00) carry SW. 22 and SW. 21. The retained script's "
				"cvpmBallStack (InitSw 0, 21, 20, 19, 18, Balls = 4) confirms the rest position order "
				"21-20-19-18 from the kicker backwards, so the third roller microswitch is position 20 "
				"by the assembly's own count. Coil 26-1200 NO DIODE (090-5044-ND, drawn Q1) lifts one "
				"ball to the shooter lane on solenoid 1, on harness 038-5508-04 (3-pin 045-5007-03, "
				"12-pin 045-5007-12). Position 22 is the exit opto the served ball crosses: the script "
				"pulses it from inside solTrough. The four steel balls are 1-1/16 inch (item AP-B). "
				"Default state at rest with a full trough is the four position switches made; the coil "
				"is a single pulse per ball, not a hold. The coil does not actuate any switch."
			),
			"positions": [
				{"id": "trough.ball-4", "label": "Trough #4 (entry, furthest from the kicker)", "sensors": ["switch.matrix-18"]},
				{"id": "trough.ball-3", "label": "Trough #3", "sensors": ["switch.matrix-19"]},
				{"id": "trough.ball-2", "label": "Trough #2", "sensors": ["switch.matrix-20"]},
				{"id": "trough.ball-1", "label": "Trough #1 (at the kicker)", "sensors": ["switch.matrix-21"]},
				{"id": "trough.exit", "label": "Exit path opto crossed by the served ball", "sensors": ["switch.matrix-22"]},
			],
			"provenance": provenance(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
		},
		{
			"id": "mech.auto-launch",
			"label": "Auto Launch",
			"kind": "kicker",
			"actuators": ["solenoid.2"],
			"sensors": ["switch.matrix-11", "switch.matrix-23"],
			"behavior": (
				"An auto-launch coil in the shooter lane fired by the ROM to put a served ball into "
				"play. The retained script wires solenoid 2 to a cvpmImpulseP plunger "
				"(PlungerIM.AutoFire). Public switch 23 (shooter lane, Trigger.sw23 co-located with "
				"Trigger.swPlunger) reports the ball waiting in the lane. The plunger assembly is "
				"manual cabinet item 16 (500-6146-00-04). Public switch 11's physical device is "
				"unresolved (see that switch's record). The coil does not actuate either switch."
			),
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE, status="observed"),
		},
		{
			"id": "mech.kickback-ram",
			"label": "Kickback Ram",
			"kind": "kicker",
			"actuators": ["solenoid.12"],
			"sensors": ["switch.matrix-34"],
			"behavior": (
				"A spring-loaded ram toy at the upper left that kicks a resting ball back into play. "
				"Public switch 34 reports the ball sitting in the kicker (Kicker.sw34); the retained "
				"script's sw34_Hit maintains the switch state and starts its RamFire timer, whose "
				"commented-out kick path shows the coil's intended coupling ('Kick is handled by ramb "
				"kicker'), with the active code kicking via the table's own Kicker.sw34 object "
				"instead. The manual gives the physical construction across three pages: the ram toy "
				"itself (PDF page 16, RAM TOY MODIFIED 860-5110-04-ASY on prime assembly 550-7163-00), "
				"its mount bracket (PDF page 17, 511-5231-00), and the kicker coil assembly (PDF page "
				"18, 500-7166-00) whose item 5 is COIL - 23-800, NO DIODE (090-5001-ND) with plunger "
				"515-7726-00 and conical return spring 266-5020-00. The coil is a pulse device with a "
				"spring return; the ball's weight on switch 34 is what closes it."
			),
			"provenance": provenance(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, status="observed"),
		},
		{
			"id": "mech.buck-target",
			"label": "Buck Target (moving deer)",
			"kind": "motorized",
			"actuators": ["solenoid.3", "solenoid.4", "solenoid.5"],
			"sensors": ["switch.matrix-1", "switch.matrix-37", "switch.matrix-45"],
			"behavior": (
				"The machine's headline mechanism: a deer target that travels along a track across the "
				"upper playfield while the player shoots it. Three driver addresses belong to the "
				"drive per the retained script's own callback names: solenoid 3 ('right or "
				"backwards'), solenoid 4 ('left or forwards') and solenoid 5 (the motor, its "
				"SolCallback line commented out entirely). Position feedback comes from drive-track "
				"optos the same commented code names as 'opto switch 37' (pulsed every few steps) and "
				"'opto switch 45'; the manual's deer-track page shows the track's fiber assembly and "
				"actuator (assembly pages around PDF page 12) but no electrical table exists to "
				"confirm the sensor count. The hit sensor is public switch 1, detected physically "
				"wherever the target currently is; the retained table models the detection through a "
				"ladder of thirty-one wall segments raised one at a time under the animated Buck. The "
				"table does not drive the ROM's feedback path at all: it animates the Buck itself by "
				"following the flashing Buck path lamps (16-20, super jackpot 57), and writes its "
				"endpoints to the unfitted UK post-save addresses 71/72. That substitution is a "
				"property of the retained recreation, not of the machine; a recreation that wants the "
				"ROM's own Buck logic must drive 37/45 and read 3/4/5 the way the ROM expects, which "
				"needs a harness trace of a legal ROM to pin down. Default state is the Buck at home "
				"(track start) with the walls ladder at its first segment."
			),
			"positions": [
				{"id": "buck.home", "label": "Home (track start)", "sensors": []},
				{"id": "buck.travelling", "label": "Travelling (position reported by the drive optos)", "sensors": ["switch.matrix-37", "switch.matrix-45"]},
			],
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE, status="observed"),
		},
		{
			"id": "mech.elk-diverter",
			"label": "Elk Diverter",
			"kind": "diverter",
			"actuators": ["solenoid.14"],
			"sensors": ["switch.flipper-85"],
			"behavior": (
				"A mini-flipper-style gate on the right side of the upper playfield that diverts a "
				"shot into the Elk ramp. The retained script binds the player control to public "
				"switch 85 (the hardware upper-left-flipper cabinet position, D-13): Sub sw85_Hit "
				"pulses it, and Sub SolLElk on solenoid 14 rotates the Elkdiverter flipper object to "
				"its end position while swapping dropped walls sw85 (raw 650.2, 1104.6-1109.1) and "
				"sw85a (raw 793.9-796.6, 1037.7-1038.1), so the gate physically swaps between two "
				"ball guides. Which physical cabinet control the factory wires to D-13 on a machine "
				"that fits no upper flipper is not settled by any retained source (see switch 85). "
				"The manual's upper mini-flipper assembly page (PDF page 9 area) shows the assembly's "
				"mechanical construction. Default state is the diverter retracted (wall sw85 raised, "
		"sw85a dropped per Table1_Init)."
			),
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE, status="observed"),
		},
		{
			"id": "mech.up-down-posts",
			"label": "Up/Down Posts",
			"kind": "other",
			"actuators": ["solenoid.7", "solenoid.23"],
			"sensors": [],
			"behavior": (
				"Two retractable posts that block or open lanes. The retained script binds solenoid 7 "
				"to the BUpPost wall (raw 442.5, 462.3, 'bird orbit post') and solenoid 23 to the "
				"UpPost wall (raw 490.8, 58.0, 'orbit post' at the very top of the playfield), each "
				"a twelve-point wall raised and lowered by its callback. The manual's post "
				"assemblies give the physical construction: Up/Down Post Assembly 500-7153-04 (PDF "
				"page 19) with coil 26-1200 NO DIODE drawn Q12, left-hand-thread capped plunger "
				"515-5198-01 and conical spring 266-5022-00, plus the two-per-playfield ball-deflect "
		"post assemblies (500-7085-00 family) on the following assembly pages. Neither source "
				"states which assembly number each solenoid drives, and the posts carry no position "
				"sensor in any retained source. Default state at game start is both posts lowered "
				"(BUpPost.IsDropped = 1 in Table1_Init; UpPost likewise unraised)."
			),
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE, status="observed"),
		},
		{
			"id": "mech.spinner",
			"label": "Spinner / Spinning Disk",
			"kind": "rotary",
			"actuators": [],
			"sensors": ["switch.matrix-44"],
			"behavior": (
				"Public switch 44 is a spinner the retained script pulses per rotation "
				"(sw44_Spin; Spinner.sw44 at raw 740.0, 680.5). The manual's Blue Pages give the "
				"physical assembly as MOTOR/BRACKETS ASSEMBLY 511-5224-00 (PDF page 15): a spinning-"
				"disk motor (511-5190-00) carrying an opto disk (535-0308-00) read by an opto board "
				"assembly (511-5209-00) on a dedicated mounting bracket -- a motorized disk with "
				"optical position feedback rather than a plain ball-spun spinner wire. The ball-"
				"guide assemblies with opto transceivers (PDF page 24) are the other optical lane "
				"sensors the manual documents; neither page names a switch number, so the mapping "
				"between the assembly's opto board, the ball-guide transceivers and the public "
				"switch addresses (44 and the unbound matrix addresses) is not settled by retained "
				"evidence and needs a harness trace. No actuator address is claimed: the disk "
				"motor's drive, if the ROM pulses one, did not survive into the retained script's "
				"active callbacks."
			),
			"provenance": provenance(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, status="observed"),
		},
	]


def relationships() -> list[dict[str, Any]]:
	return []


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.sam-invsw-never-populated",
			"path": "controller.inversion_applied_by_emulator; inputs[binding.device=21,22,37,45]",
			"description": (
				"The controller profile pinmame.sam declares inversion_applied_by_emulator: true as a "
				"platform capability, matching every WPC profile this project has curated. For Stern "
				"S.A.M. pinned PinMAME applies none: sam.c's INITGAME macro expands to a positional "
				"aggregate initializer that stops at the hw sub-struct, so core_gameData->wpc.invSw is "
				"left at its C zero-initialization default, core.c copies those zeros into "
				"coreGlobals.invSw at machine init, and no Stern S.A.M. game in sam.c ever assigns "
				"invSw. This machine's opto-construction evidence is unusually direct and unusually "
				"incomplete at the same time: the manual's own trough cut-away labels the dual opto "
				"boards SW. 21 and SW. 22, the retained script's commented Buck code names 'opto "
				"switch 37' and 'opto switch 45', and the ball-guide assemblies carry opto "
				"transceivers (500-6775-01) whose switch addresses no retained source states -- so "
				"physical construction is known for 21/22/37/45 and unmapped for at least two more "
				"optos, while the emulator-side normalization is known to be absent for all of them. "
				"The public state of every opto on this machine is raw hardware polarity. Resolution "
				"path: a LibPinMAME gameplay-harness trace of a legal bbh_160 ROM (whose bytes match "
				"the pinned revision exactly) observing the idle public state of switches 21, 22, 37 "
				"and 45 with and without a ball present, plus the boot diagnostic's own switch-status "
				"page for the unmapped ball-guide optos. Unresolved."
			),
			"source_refs": [CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CONTROLLER_SOURCE, ROM_SOURCE],
		},
		{
			"id": "conflict.elk-button-physical-control",
			"path": "inputs[binding.device=85]",
			"description": (
				"The retained table binds the Elk diverter's player control to public switch 85, the "
				"hardware D-13 'upper left flipper' cabinet position, and the ROM demonstrably reads "
				"that bit (sam.c's EOS mirror exists so the ROM's flipper self-test sees D-13/D-14 as "
				"a pair). But this machine fits no upper flipper, and the partial manual's cabinet "
				"parts tables list only two red flipper button assemblies (item 5, qty 2), the start "
				"button (3S) and the tournament button (4T) -- no third side button of any kind. Two "
				"readings fit the evidence: the factory harness parallels the left flipper button's "
				"switch onto D-13 so the Elk fires off the left flipper button, or a cabinet control "
				"exists that the partial manual's tables omit. Nothing retained can distinguish "
				"these, and the answer changes what a cabinet builder must wire. Resolution path: a "
				"photograph of an unrestored machine's cabinet wiring where the D-9 to D-16 return "
				"harness is visible, or a continuity check of the left flipper button switch against "
				"the CPU board's flipper-column connector on real hardware. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE],
		},
	]


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items: list[dict[str, Any]] = []
	for driver_id in DRIVER_IDS:
		record = by_id[driver_id]
		item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		compatibility, notes = DRIVER_COMPATIBILITY[driver_id]
		item["physical_compatibility"] = compatibility
		item["variant_notes"] = notes
		items.append(item)
	return items

# --- Definition ----------------------------------------------------------------------------------

SPATIAL_GAPS = (
	"outputs[binding.device=27,28,29,30] (pinmame.output.lamp) carry no spatial key: the retained "
	"table renders all four as colored bulb Primitives stacked at raw (401.3, 263.9, z 290) with "
	"Flash-glow partners clustered around raw (352.5, 250-371), so four distinct physical bulb "
	"positions cannot be derived from the stack. See the lamp records' own notes.",
	"outputs[binding.device=0] (pinmame.output.gi) has no spatial key: the partial manual prints no "
	"G.I. bulb inventory, and the retained script's UpdateGI drives one 27-light collection for any "
	"string index, so no per-bulb placement set can be asserted. The 27 retained GI positions are in "
	"the geometry dump.",
	"Roughly half the bound-by-ROM address space (matrix switches 2, 3, 4, 12, 17, 46-64; solenoids "
	"6, 8-11, 13, 17, 18, 24, 28, 30; lamps 1, 2, 4, 12, 13, 34, 36, 37, 44, 48, 56, 58, 64, 71-80) "
	"is recorded availability unknown rather than placed or declared unused: the partial manual "
	"carries none of Stern's electrical tables, and no retained source names or binds those "
	"addresses. Failing to observe an address is never proof that it is unused.",
)


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Big Buck Hunter Pro",
			"manufacturer": "Stern",
			"year": 2010,
			"kind": "physical_pinball",
			"ipdb_id": 5513,
			"opdb_id": "G4N6n-MLxER",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": [
				"input_semantics",
				"output_semantics",
				"polarity",
				"recreation_notes",
				"spatial_placement",
				"unresolved_conflicts",
			],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "candidate",
				"physical_wiring": "candidate",
				"mechanisms": "observed",
				"variant_coverage": "validated",
				"recreation_knowledge": "observed",
				"spatial_placement": "observed",
			},
		},
		"controller": {
			"platform": "pinmame.sam",
			"hardware_generation": "0x100000000000",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Big Buck Hunter Pro device identifiers are not unique: {duplicates}")
	placement_ids: list[str] = []
	for device in definition["inputs"] + definition["outputs"]:
		spatial = device.get("spatial")
		if spatial and spatial["status"] != "not_applicable":
			placement_ids += [placement["id"] for placement in spatial["placements"]]
	placement_duplicates = sorted({item for item in placement_ids if placement_ids.count(item) > 1})
	if placement_duplicates:
		raise RuntimeError(f"Big Buck Hunter Pro placement identifiers are not unique: {placement_duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	missing_inputs: list[int] = []
	placement_count = 0
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			missing_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
			placement_count += len(spatial["placements"])
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	missing_outputs: list[dict[str, Any]] = []
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			missing_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "partial",
		"blockers": list(SPATIAL_GAPS),
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/stern/big-buck-hunter-pro-2010/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"geometry_dump_sha256": VPX_GEOMETRY_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, reason in sorted(SOLENOID_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/by-machine/stern.big-buck-hunter-pro.2010/",
			"geometry": {
				"path": "external:pinmame-review-artifacts/big-buck-hunter-pro-2010/vpx-geometry.json",
				"sha256": VPX_GEOMETRY_SHA256,
			},
		},
		"excluded_object_classes": [
			"Stacked bulb Primitives L27-L30 and their Flash partners f27-f30: four lamp addresses "
			"rendered at one position, so no distinct per-address placement exists.",
			"Unbound decorative flasher shapes f1, f2, f5, f6, f7 (above the playfield's top edge) and "
			"unbound lights f131a1/f131a2: no callback binds them to any address.",
			"Ten Timer objects (BuckTimer, LampTimer, ...): editor timers with arbitrary positions, "
			"not physical devices.",
		],
		"unresolved": [
			{"group": binding["group"], "address": binding["address"]}
			for binding in sorted(missing_outputs, key=lambda item: (item["group"], item["address"]))
		]
		+ [{"group": "pinmame.input.switch", "address": address} for address in sorted(missing_inputs)],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Big Buck Hunter Pro (Stern, 2010) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record is `partial` at "
		"`machines/partial/stern/big-buck-hunter-pro-2010.json`. Two conflicts, the stacked-bulb and "
		"G.I. spatial gaps, and the large unknown address set are recorded in the definition itself.",
		"",
		"The matching source is the retained known-working `Big Buck Hunter Pro (Stern 2010).vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact "
		f"playfield bounds from the table's own `gamedata.json` are `{TABLE_BOUNDS}`, so every "
		f"canonical coordinate is x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT} rounded to at most six "
		"fractional places. Note the x divisor: this table is 979 units wide, not the 952 most WPC-"
		"era tables in this project use.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime address and causality authority; the IPDB-hosted "
		"partial manual is the physical construction authority for the addresses its drawings "
		"label; pinned PinMAME owns controller topology; the retained table supplies geometry.",
		"- This manual carries no electrical tables and PinMAME's own game block says none exists; "
		"its per-game output typing was reconstructed from the community table this project "
		"retains. Every unbound address is therefore recorded `unknown`, never `unused`.",
		"- The trough is the one mechanism whose addresses the manual labels directly (SW. 18-22 on "
		"PDF page 3), and it anchors the construction evidence for the switch matrix.",
		"- The Buck target mechanism's table-side substitute animation (lamp-following with 71/72 "
		"writes) is disclosed as a property of the retained recreation, never promoted to machine "
		"behavior.",
		"- Public solenoids 33 to 66 are enumerated because `hw.custSol` is hardcoded 16 for every "
		"Stern S.A.M. game, but nothing on this machine can drive 51-66 (`SAM_NO_AUX`, "
		"gameSpecific1 = 0) and 33 is PinMAME's synthetic game-on state. All carry controlled "
		"`virtual` or `unused` records.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group']} address {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		f"- Devices with no `spatial` key at all: {len(report['unresolved'])}",
		"",
		"## Named spatial gaps",
		"",
	]
	for blocker in report["blockers"]:
		lines.append(f"- {blocker}")
	lines += [
		"",
		"## Excluded retained objects",
		"",
	]
	for entry in report["excluded_object_classes"]:
		lines.append(f"- {entry}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Promotion to `author_ready` is refused. Two conflicts remain unresolved "
		"(`conflict.sam-invsw-never-populated`, `conflict.elk-button-physical-control`); the input "
		"and output semantics of roughly forty addresses are unknown because no electrical table "
		"exists in any retained source; recreation knowledge remains observed until a harness run "
		"exercises the ROM's Buck feedback and the Elk button path; and the stacked-bulb and G.I. "
		"spatial gaps have no honest placement set. The record therefore stays `partial` with "
		"`coverage.missing = [\"input_semantics\", \"output_semantics\", \"polarity\", "
		"\"recreation_notes\", \"spatial_placement\", \"unresolved_conflicts\"]`.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 "
		f"`{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} "
		"bytes.",
		f"- Full per-object geometry dump of the retained extraction, SHA-256 "
		f"`{VPX_GEOMETRY_SHA256}`.",
		f"- Committed, digest-verified manual transcriptions under `{EXCERPT_ROOT}/`.",
		"- ROM identity verification (three exact matches, one mismatching 1.7 dump) recorded in "
		"the `rom.stern.big-buck-hunter-pro` source record and the bbh_170 driver note.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	stale_author_ready = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready.exists():
		stale_author_ready.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale_author_ready_path = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready_path.exists():
		raise RuntimeError(f"Stale Big Buck Hunter Pro author-ready definition is still present: {stale_author_ready_path}")
	for superseded in (SUPERSEDED_STUB_PATH, SUPERSEDED_STUB_KNOWLEDGE_PATH):
		superseded_path = root / superseded.relative_to(ROOT)
		if superseded_path.is_file():
			stub = load_json(superseded_path) if superseded_path.suffix == ".json" else None
			if stub is not None and stub["machine"]["id"] != "stub.pinmame.bbh_170":
				raise RuntimeError(f"Unexpected content at the superseded stub path: {superseded_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Big Buck Hunter Pro definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Big Buck Hunter Pro seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Big Buck Hunter Pro definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Big Buck Hunter Pro seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Big Buck Hunter Pro spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Big Buck Hunter Pro spatial review drifted from its deterministic curator: {markdown_path}")
	print("Big Buck Hunter Pro definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Big Buck Hunter Pro extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Big Buck Hunter Pro retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
