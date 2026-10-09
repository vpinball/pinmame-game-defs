"""Settle import-legacy label conflicts on bulk-imported records from the game's own ROM.

`import-legacy` recorded a conflict wherever a legacy platform file and a legacy game file named one
public address differently. On several WPC records the platform file's `ROM Started` (legacy alias
`c_game_on`) sits on solenoid 19, where no WPC generation has a game-on output, while the game file
names a flasher there; on others the game file puts playfield sensors on the coin-door switches the
platform file places at 1-4, or, on System 11, calls the game-on line at 23 a tilt output. When a
hash-pinned harness run of the game's own ROM shows what the address is, this tool rewrites that one
device from the run, drops the conflict, cites the run, and keeps `coverage.missing` honest.

Every settlement below names its retained evidence. Several settlements may cite one run; a device
keeps its id unless the settlement gives a new one. A settlement may also cite complete source records
in `extra_sources`, such as the game's own manual or a pinned known-working table script that the
run corroborates; the device cites them after the run. A settlement names the id and label
`import-legacy` gave the device, and the tool refuses a device that carries neither those nor the
settled ones, or whose public-number aliases name another address. The tool edits only the listed
device, conflict, source list and coverage; everything else in the record is left as
`import-legacy` wrote it, and a record whose `coverage.missing` omits `unresolved_conflicts` while
one remains is refused. Run with --check to verify that every listed record already matches what
the tool would write.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402

RUNTIME_PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
ATTRIBUTION = "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"

SKATEBALL_IN_PLAY = {
	"id": "runtime.skateball.skatebll.switch-2-and-19-in-play",
	"uri": "internal:evidence/runtime/by35/skateball-skatebll-switch-2-and-19-in-play.json",
	"locator": (
		"One hash-pinned LibPinMAME harness run of skatebll from empty NVRAM (scenario "
		"tools/harness-scenarios/by35/skatebll-switch-2-and-19-in-play.json) that plays one three-ball game. Public 19 "
		"rises during the start press, stays raised through all three balls and two right flipper button presses, and "
		"drops at game over. With center drop targets 3 and 4 down, pressing public 2 fires the center bank reset (10)."
	),
}

VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
VPW_ATTRIBUTION = "VPW (Visual Pinball Workshop) table authors; pinned copy in sverrewl/vpxtable_scripts"

SPECIAL_FORCE_SWITCH_TEST = {
	"id": "runtime.special-force.specforc.switch-test",
	"uri": "internal:evidence/runtime/by6803/special-force-specforc-switch-test.json",
	"locator": (
		"One hash-pinned LibPinMAME harness run of specforc from empty NVRAM (scenario "
		"tools/harness-scenarios/by6803/specforc-switch-test.json) that holds public 2 and presses Test: the ROM's "
		"stuck-switch check opens its Switch Test, which names every closed switch on the alphanumeric displays. It "
		"names public 2 CHOPPER TOP, 7 RIGHT LAUNCH and 16 RELEASE LEFT, and the controls 5 LEFT LAUNCH, 15 TILT SWITCH "
		"and 14 SLAM SWITCH."
	),
}
SPECIAL_FORCE_SOLENOID_TEST = {
	"id": "runtime.special-force.specforc.solenoid-test",
	"uri": "internal:evidence/runtime/by6803/special-force-specforc-solenoid-test.json",
	"locator": (
		"One hash-pinned LibPinMAME harness run of specforc from empty NVRAM (scenario "
		"tools/harness-scenarios/by6803/specforc-solenoid-test.json) that steps the keypad to SELF TESTING and runs the "
		"ROM's Solenoid Test, which fires one driver at a time and names it. After public 1-12, 14 and 15 it raises "
		"public 19 for 1.7 s and shows FLIPPER with the driver Q07."
	),
}
SPECIAL_FORCE_MANUAL = {
	"id": "manual.special-force.operating-manual",
	"kind": "manual",
	"uri": "external:pinmame-manuals/by-machine/bally.special-force.1986/visual-pinball-manuals/Bally_1986_Special_Force_Manual.pdf",
	"revision": "sha256:3b181618a2b20f1b66e39a687353fbffa78068c50cd020d468ef30bd61ada431",
	"sha256": "3b181618a2b20f1b66e39a687353fbffa78068c50cd020d468ef30bd61ada431",
	"locator": (
		"47-page scanned Bally Midway Special Force Operating Manual, game no. 0E47, form no. 0E47-00300-0100, with "
		"schematics. PDF page 8 (printed 1-2) describes the coin-door keypad, PDF page 17 (printed 1-9) prints the "
		"Solenoid and Switch Assembly Identification Tables, and PDF page 45 lists the solenoid driver locations."
	),
	"license": "NOASSERTION",
	"attribution": "Bally Midway Mfg. Co.; copy supplied by the repository maintainer",
	"original_filename": "Bally_1986_Special_Force_Manual.pdf",
	"rights": "NOASSERTION",
	"excerpts": [
		{
			"id": "excerpt.special-force.identification-tables",
			"locator": "PDF page 17, printed page 1-9: SOLENOID IDENTIFICATION TABLE and SWITCH ASSEMBLY IDENTIFICATION TABLE, both transcribed in full",
			"method": "manual",
			"path": "evidence/excerpts/bally.special-force.1986/identification-tables.md",
			"reviewed": True,
			"sha256": "42eed7abe3e1dc92c65ac3fed97866a48255b2a9c198509d3625e2eb8bbd5b20",
			"transcribed_by": "curator, read from the rendered page",
		},
		{
			"id": "excerpt.special-force.solenoid-driver-locations",
			"locator": "PDF page 45, sheet M051-00E47-A012: the SOLENOID DRIVER LOCATIONS table with its footnote and wire colour legend",
			"method": "manual",
			"path": "evidence/excerpts/bally.special-force.1986/solenoid-driver-locations.md",
			"reviewed": True,
			"sha256": "ada8590b0a121f37578aa2adab3356167cafe63046622c870aab43090c534daa",
			"transcribed_by": "curator, read from the rendered page",
		},
		{
			"id": "excerpt.special-force.keypad-operation",
			"locator": "PDF page 8, printed page 1-2: the OPERATION subsection of III. TAILORING & TESTING THE GAME",
			"method": "manual",
			"path": "evidence/excerpts/bally.special-force.1986/keypad-operation.md",
			"reviewed": True,
			"sha256": "56e4c03a777d15315c35326b776af602c6dcf7c1898ba2463aa99278c5227908",
			"transcribed_by": "curator, read from the rendered page",
		},
	],
}
VPM_6803_LIBRARY = {
	"id": "vpm-script-library.6803-vbs",
	"kind": "vpx_script",
	"uri": "external:pinmame-review-artifacts/vpm-script-libs/6803.vbs",
	"sha256": "472b75fd486282a9533bd5c999d965544cb0803655ecc0f996de01d8a79a38e6",
	"locator": (
		"The VPinMAME script library Bally 6803 tables load (LoadVPM ..., \"6803.VBS\", ...), retained from the "
		"maintainer's working installation together with the core.vbs it executes (SHA-256 "
		"a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69). Line 21 sets GameOnSolenoid = 19, which "
		"core.vbs's vpmFlips takes as the flipper-enable solenoid when a table sets UseSolenoids = 2 (lines 2121-2133); "
		"lines 26-41 put the coin-door keypad on public 1-4, 9-12, 17-20 and 25-28, keypad 0 on 2; lines 42-43 set "
		"swTilt = 15 and swSlamTilt = 14."
	),
	"license": "NOASSERTION",
	"attribution": "VPinMAME / Visual Pinball script-library maintainers",
	"original_filename": "6803.vbs",
	"rights": "NOASSERTION",
	"acquired_at": "2026-10-01T00:00:00Z",
	"excerpts": [
		{
			"id": "excerpt.special-force.vpm-6803-library",
			"locator": "6803.vbs lines 17-51 and core.vbs lines 2121-2133, verbatim",
			"method": "manual",
			"path": "evidence/excerpts/bally.special-force.1986/vpm-6803-library.md",
			"reviewed": True,
			"sha256": "296c5465002e47e1b8f6fbd96175ee757922656aeff059889edddef82dd7a1c7",
			"transcribed_by": "curator, read from the library files",
		},
	],
}
SPECIAL_FORCE_MANUAL_SOURCES = [SPECIAL_FORCE_MANUAL]
SPECIAL_FORCE_LIBRARY_SOURCES = [SPECIAL_FORCE_MANUAL, VPM_6803_LIBRARY]

BEAT_THE_CLOCK_IN_PLAY = {
	"id": "runtime.beat-the-clock.beatclck.drop-bank-and-switch-16-in-play",
	"uri": "internal:evidence/runtime/by6803/beat-the-clock-beatclck-drop-bank-and-switch-16-in-play.json",
	"locator": (
		"One hash-pinned LibPinMAME harness run of beatclck from empty NVRAM (scenario "
		"tools/harness-scenarios/by6803/beatclck-drop-bank-and-switch-16-in-play.json) that plays two balls. Each "
		"closure of drop targets 1, 3, 4 and 5 and of public 2, 7 and 16 scores 3,000; the closure that completes the "
		"six with 1-5 is worth 53,000 when public 7 closes last on ball 1 and 103,000 when public 2 closes last on ball "
		"2, each with a lamp show. Public 19 stays raised throughout and drops when the tilt bob (15) closes twice."
	),
}
BEAT_THE_CLOCK_VPW = {
	"id": "vpx-script.beat-the-clock-vpw-1-0-5",
	"kind": "vpx_script",
	"uri": (
		"https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/"
		"Beat%20The%20Clock%20%28Bally%201985%29%20VPW%20v1.0.5.vbs"
	),
	"revision": VPXTABLE_SCRIPTS_REVISION,
	"sha256": "9aeca46a17050a0515f882b964cfeb0b51753c14c3e0bdb0397902d02098d2a6",
	"locator": (
		"Line 93 runs cGameName beatclc2 (the flasher-support clone of beatclck, which line 94 comments out); line 324 "
		"sets HandleKeyboard=0 and line 342 vpmNudge.TiltSwitch=15. Line 475 binds SolCallback(11), the 1-6 drop target "
		"reset, to SolDropUpDTL, which raises drop targets 1, 2, 3, 4, 5 and 7 (lines 512-519); lines 710-715 hit sw1-sw5 "
		"and sw7 through DTHit, and lines 2724-2733 build them as drop targets. Lines 747-748 write public 16 from the "
		"Hit and UnHit events of the playfield object sw16."
	),
	"license": "NOASSERTION",
	"attribution": VPW_ATTRIBUTION,
	"known_working": True,
}

SPECTRUM_IN_PLAY = {
	"id": "runtime.spectrum.spectru4.flipper-buttons-and-saucer-7",
	"uri": "internal:evidence/runtime/by35/spectrum-spectru4-flipper-buttons-and-saucer-7.json",
	"locator": (
		"One hash-pinned LibPinMAME harness run of spectru4 from empty NVRAM (scenario "
		"tools/harness-scenarios/by35/spectru4-flipper-buttons-and-saucer-7.json) that starts a game. With the drain "
		"saucer switch 8 closed, raising public 2 does nothing, and raising public 1 kicks the saucer (5) 0.1 s later. "
		"Closing public 7 fires the top kicker (1) and scores 10,000. Public 19 stays raised while public 2 is held at "
		"1 and drops when the tilt bob (15) closes."
	),
}
SPECTRUM_VPW = {
	"id": "vpx-script.spectrum-vpw-1-0-1",
	"kind": "vpx_script",
	"uri": (
		"https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/"
		"Spectrum%20%28Bally%201981%29%20VPW%20v1.0.1.vbs"
	),
	"revision": VPXTABLE_SCRIPTS_REVISION,
	"sha256": "a75ff1364624bd79469b547591b9448751a9e86c0d66854acfb47e474220e583",
	"locator": (
		"Line 58 runs cGameName spectru4; line 98 sets HandleKeyboard=0 and line 114 vpmNudge.TiltSwitch = 15. Lines "
		"345-346 write public 1 False for the right flipper key and public 2 False for the left on KeyDown, and lines "
		"362-363 write them True on KeyUp. Lines 538-548 write public 7 from the top kicker sw7, which the top-kicker "
		"callbacks on solenoids 1 and 2 (lines 372-373) kick out. Line 385 binds SolCallback(19) to vpmNudge.SolGameOn."
	),
	"license": "NOASSERTION",
	"attribution": VPW_ATTRIBUTION,
	"known_working": True,
}

SETTLEMENTS: list[dict[str, Any]] = [
	{
		"path": "machines/partial/bally/black-rose-1992.json",
		"machine_id": "bally.black-rose.1992",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Right Bottom Flasher",
		"kind": "flasher",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_game_on"}],
		"source": {
			"id": "runtime.black-rose.br-l4.flasher-test",
			"uri": "internal:evidence/runtime/wpc-fliptronic/black-rose-br_l4-flasher-test.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of br_l4 from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-fliptronic/br-flasher-test.json) that steps T.5 FLASHER TEST through "
				"flashers 17-28 in repeat mode. At step 19 the ROM pulses public solenoid 19 and prints RIGHT BOTTOM "
				"with the wires BLK-ORN RED-WHT."
			),
		},
		"note": (
			"Legacy import labelled this address 'ROM Started' (alias c_game_on) from the legacy WPC platform map, "
			"against the game file's 'Right Bottom Flasher'. The L-4 ROM's own T.5 FLASHER TEST settles it: it pulses "
			"public 19 among flashers 17-28 and prints RIGHT BOTTOM (BLK-ORN RED-WHT). No WPC generation has a "
			"game-on output at 19, so the platform alias is dropped."
		),
	},
	{
		"path": "machines/partial/williams/no-fear-dangerous-sports-1995.json",
		"machine_id": "williams.no-fear-dangerous-sports.1995",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Flasher: No Fear",
		"kind": "flasher",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_game_on"}],
		"source": {
			"id": "runtime.no-fear.nf-23x.flasher-test",
			"uri": "internal:evidence/runtime/wpc-security/no-fear-nf_23x-flasher-test.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of nf_23x from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-security/nf-flasher-test.json) that steps T.5 FLASHER TEST through "
				"flashers 17-28 in repeat mode. At step 19 the ROM pulses public solenoid 19 and prints FLS. NO FEAR "
				"with the wires BLK-ORN RED-WHT."
			),
		},
		"note": (
			"Legacy import labelled this address 'ROM Started' (alias c_game_on) from the legacy WPC platform map, "
			"against the game file's 'Flasher: No Fear (x2)'. The 2.3 X ROM's own T.5 FLASHER TEST settles it: it "
			"pulses public 19 among flashers 17-28 and prints FLS. NO FEAR (BLK-ORN RED-WHT). No WPC generation has a "
			"game-on output at 19, so the platform alias is dropped. The ROM names one output, not a bulb count: the "
			"game file's '(x2)' quantity is not confirmed by the run."
		),
	},
	{
		"path": "machines/partial/williams/red-and-ted-s-road-show-1994.json",
		"machine_id": "williams.red-and-ted-s-road-show.1994",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Ted Motor Direction",
		"kind": "coil",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_game_on"}],
		"source": {
			"id": "runtime.red-and-ted-s-road-show.rs-l6.ted-test",
			"uri": "internal:evidence/runtime/wpc-security/red-and-ted-s-road-show-rs_l6-ted-test.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of rs_l6 from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-security/rs-ted-test.json) that starts T.17 \"TED\" TEST and lets it run two "
				"cycles. As the display reaches 06 MOUTH OPEN the ROM raises public 19 together with 20, drops 20 about "
				"0.33 s and 19 about 0.39 s later, and in 07 MOUTH CLOSED drives 20 alone; 19 never rises without 20."
			),
		},
		"note": (
			"Legacy import labelled this address 'ROM Started' (alias c_game_on) from the legacy WPC platform map, "
			"against the game file's 'Ted Motor Direction'. Pinned rs.c names 19 sTedMotorDrv, and the L-6 ROM's own "
			"T.17 \"TED\" TEST settles it: in step 06 MOUTH OPEN it raises public 19 together with 20 (Ted Mouth Motor) "
			"and releases 19 just after 20, and in step 07 MOUTH CLOSED it drives 20 alone. So 19 sets the direction of "
			"Ted's mouth motor and is set for opening, which is also how rs.c's simulation reads it. No WPC generation "
			"has a game-on output at 19, so the platform alias is dropped."
		),
	},
	{
		"path": "machines/partial/bally/harlem-globetrotters-on-tour-1979.json",
		"machine_id": "bally.harlem-globetrotters-on-tour.1979",
		"conflict_id": "conflict.pinmame-input-switch-2-none",
		"binding": {"group": "pinmame.input.switch", "device": 2},
		"from": {"id": "switch.ball-roll-tilt", "label": "Ball Roll Tilt"},
		"id": "switch.drop-target-2",
		"label": "Drop Target 2",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_ball_roll_tilt"}],
		"source": {
			"id": "runtime.harlem-globetrotters-on-tour.hglbtrtr.switch-2-in-play",
			"uri": "internal:evidence/runtime/by35/harlem-globetrotters-on-tour-hglbtrtr-switch-2-in-play.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of hglbtrtr from empty NVRAM (scenario "
				"tools/harness-scenarios/by35/hglbtrtr-switch-2-in-play.json) that starts a game, closes drop-target "
				"switches 1, 3 and 4 and then public 2. Each closure scores 5,000; closing 2 also lights lamps 2, 8, 44, 53 "
				"and 63, which none of the other closures lit, and the flipper-enable relay (19) stays raised throughout."
			),
		},
		"note": (
			"Legacy import set the legacy Bally platform map's 'Ball Roll Tilt' (alias s_ball_roll_tilt) against the game "
			"file's 'Drop Target 2'. In a hglbtrtr gameplay run the ROM scores public 2 exactly as it scores drop targets "
			"1, 3 and 4 (5,000 each), lights lamps none of their closures lit when 2 completes the four, and keeps the "
			"flipper-enable relay (19) raised, so it does not tilt. The ROM reads 2 as a member of the 1-4 drop-target "
			"bank, and the platform alias is dropped; BY35 games read their tilt on switch 7, where BY35_COMPORTS puts "
			"the Ball Tilt input."
		),
	},
	{
		"path": "machines/partial/bally/skateball-1980.json",
		"machine_id": "bally.skateball.1980",
		"conflict_id": "conflict.pinmame-input-switch-2-none",
		"binding": {"group": "pinmame.input.switch", "device": 2},
		"from": {"id": "switch.ball-roll-tilt", "label": "Ball Roll Tilt"},
		"id": "switch.center-drop-target-1-left",
		"label": "Center Drop Target 1 (Left)",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_ball_roll_tilt"}],
		"source": SKATEBALL_IN_PLAY,
		"note": (
			"Legacy import set the legacy Bally platform map's 'Ball Roll Tilt' (alias s_ball_roll_tilt) against the game "
			"file's 'Center Drop Target 1 (Left)'. In a skatebll gameplay run, closing center drop targets 3 and 4 scores "
			"and fires nothing; pressing public 2 after them makes the ROM fire the center drop-target bank reset (10) "
			"while the flipper-enable relay (19) stays raised, so the ROM does not tilt and reads 2 as the bank member that "
			"completes it. The platform alias is dropped; BY35 games read their tilt on switch 7, where BY35_COMPORTS puts the "
			"Ball Tilt input."
		),
	},
	{
		"path": "machines/partial/bally/skateball-1980.json",
		"machine_id": "bally.skateball.1980",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Flipper Enable Relay",
		"kind": "relay",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_flipper_upper_right"}],
		"source": SKATEBALL_IN_PLAY,
		"note": (
			"Legacy import set the legacy Bally platform map's 'ROM Started' (alias c_game_on) against the game file's "
			"'Upper Right Flipper' (alias c_flipper_upper_right). In a skatebll gameplay run public 19 rises during the "
			"start press, stays raised through three balls and through two presses of the right flipper button switch "
			"(32), and drops when the game ends; it never follows a flipper. The BY35 controller profile, after "
			"lisy35.c, names 19 continuous bit 2, the flipper-enable relay, which is what the trace shows. The flipper "
			"alias is dropped and c_game_on stays, because the relay is held for exactly the game."
		),
	},
	{
		"path": "machines/partial/bally/special-force-1986.json",
		"machine_id": "bally.special-force.1986",
		"conflict_id": "conflict.pinmame-input-switch-2-none",
		"binding": {"group": "pinmame.input.switch", "device": 2},
		"from": {"id": "switch.ball-roll-tilt", "label": "Ball Roll Tilt"},
		"id": "switch.chopper-top",
		"label": "Chopper Top",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_ball_roll_tilt"}],
		"source": SPECIAL_FORCE_SWITCH_TEST,
		"extra_sources": SPECIAL_FORCE_LIBRARY_SOURCES,
		"note": (
			"Legacy import set the legacy Bally platform map's 'Ball Roll Tilt' (alias s_ball_roll_tilt) against the game "
			"file's 'Chopper Top'. The game's own Switch Assembly Identification Table prints switch 2 CHOPPER TOP, and the "
			"ROM's Switch Test names public 2 CHOPPER TOP. The manual says the playfield switches are wired in parallel "
			"with the coin-door keypad, and PinMAME's by6803 port map and the VPinMAME 6803.vbs library put keypad 0 on "
			"this matrix position; with PinMAME keyboard handling on, the keypad port overwrites public 2. The platform "
			"alias is dropped: this game's cabinet tilt is switch 15."
		),
	},
	{
		"path": "machines/partial/bally/special-force-1986.json",
		"machine_id": "bally.special-force.1986",
		"conflict_id": "conflict.pinmame-input-switch-7-none",
		"binding": {"group": "pinmame.input.switch", "device": 7},
		"from": {"id": "switch.tilt", "label": "Tilt"},
		"id": "switch.right-launch-button",
		"label": "Right Launch Button",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_tilt"}],
		"source": SPECIAL_FORCE_SWITCH_TEST,
		"extra_sources": SPECIAL_FORCE_MANUAL_SOURCES,
		"note": (
			"Legacy import set the legacy Bally platform map's 'Tilt' (alias s_tilt) against the game file's 'Right Magna "
			"Save Button'. The game's own Switch Assembly Identification Table prints switch 7 RIGHT LAUNCH (RT. ORANGE "
			"P.B.), an orange push button, and the ROM's Switch Test names public 7 RIGHT LAUNCH. by6803 leaves public 7 "
			"an ordinary matrix switch; the cabinet tilt is switch 15 and the slam switch 14, both named so by the same test. The same table prints switch 5 LEFT LAUNCH "
			"(LT. ORANGE P.B.), where this record still carries the game file's 'Left Magna Save Button'."
		),
	},
	{
		"path": "machines/partial/bally/special-force-1986.json",
		"machine_id": "bally.special-force.1986",
		"conflict_id": "conflict.pinmame-input-switch-16-none",
		"binding": {"group": "pinmame.input.switch", "device": 16},
		"from": {"id": "switch.slam-tilt", "label": "Slam Tilt"},
		"id": "switch.release-left",
		"label": "Release Left",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_slam_tilt"}],
		"source": SPECIAL_FORCE_SWITCH_TEST,
		"extra_sources": SPECIAL_FORCE_MANUAL_SOURCES,
		"note": (
			"Legacy import set the legacy Bally platform map's 'Slam Tilt' (alias s_slam_tilt) against the game file's "
			"'Standup Target'. The game's own Switch Assembly Identification Table prints switch 16 RELEASE LEFT (BEHIND "
			"IN-LINE D.T.), and the ROM's Switch Test names public 16 RELEASE LEFT. by6803 leaves public 16 an ordinary "
			"matrix switch; the slam switch is 14, which the same test names SLAM SWITCH."
		),
	},
	{
		"path": "machines/partial/bally/special-force-1986.json",
		"machine_id": "bally.special-force.1986",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Flipper Relay",
		"kind": "relay",
		"drop_aliases": [],
		"source": SPECIAL_FORCE_SOLENOID_TEST,
		"extra_sources": SPECIAL_FORCE_LIBRARY_SOURCES,
		"note": (
			"Legacy import set the legacy Bally platform map's 'ROM Started' (alias c_game_on) against the game file's "
			"'Unused / Empty'. The ROM's Solenoid Test raises public 19 for 1.7 s at the step it names FLIPPER, driver Q07, "
			"and the manual's Solenoid Driver Locations give Q7 as the FLIPPERS drive, connected through K1, the flipper "
			"relay; its Solenoid Identification Table ends with 24 FLIPPER (BACKBOX). The test prints the connector as "
			"J6-8-9 where the printed table gives J9-8 and J6-9. Public 19 is by6803 continuous bit 2, the bit lisy35.c "
			"calls flipper disable on BY35. The VPinMAME 6803.vbs library makes it GameOnSolenoid, the solenoid core.vbs's "
			"vpmFlips enables the flippers from when a table sets UseSolenoids = 2, so the c_game_on alias stays. No harness "
			"run has started a Special Force game yet, so how the ROM drives it in play is unobserved."
		),
	},
	{
		"path": "machines/partial/bally/beat-the-clock-1985.json",
		"machine_id": "bally.beat-the-clock.1985",
		"conflict_id": "conflict.pinmame-input-switch-2-none",
		"binding": {"group": "pinmame.input.switch", "device": 2},
		"from": {"id": "switch.ball-roll-tilt", "label": "Ball Roll Tilt"},
		"id": "switch.drop-target-2-left-bank",
		"label": "Drop Target 2 (Left Bank)",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_ball_roll_tilt"}],
		"source": BEAT_THE_CLOCK_IN_PLAY,
		"extra_sources": [BEAT_THE_CLOCK_VPW, VPM_6803_LIBRARY],
		"note": (
			"Legacy import set the legacy Bally platform map's 'Ball Roll Tilt' (alias s_ball_roll_tilt) against the game "
			"file's 'Drop Target 2 (Left Bank)'. The known-working VPW table hits public 2 as a drop target and raises it "
			"with targets 1, 3, 4, 5 and 7 from solenoid 11, the 1-6 drop target reset. In a beatclck gameplay run public 2 "
			"scores 3,000 like the other five, and closing it last completes the bank for a 103,000 award, as closing 7 "
			"last does for 53,000; public 19 stays raised, so the ROM does not tilt. The platform alias is dropped: the "
			"cabinet tilt is public 15. PinMAME's by6803 port map and the VPinMAME 6803.vbs library also put coin-door "
			"keypad 0 on this matrix position, and with PinMAME keyboard handling on the keypad port overwrites public 2; "
			"the table runs with HandleKeyboard=0."
		),
	},
	{
		"path": "machines/partial/bally/beat-the-clock-1985.json",
		"machine_id": "bally.beat-the-clock.1985",
		"conflict_id": "conflict.pinmame-input-switch-7-none",
		"binding": {"group": "pinmame.input.switch", "device": 7},
		"from": {"id": "switch.tilt", "label": "Tilt"},
		"id": "switch.drop-target-6-left-bank",
		"label": "Drop Target 6 (Left Bank)",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_tilt"}],
		"source": BEAT_THE_CLOCK_IN_PLAY,
		"extra_sources": [BEAT_THE_CLOCK_VPW],
		"note": (
			"Legacy import set the legacy Bally platform map's 'Tilt' (alias s_tilt) against the game file's 'Drop Target 6 "
			"(Left Bank)'. The known-working VPW table hits public 7 as the sixth drop target of the bank that solenoid 11 "
			"raises with 1-5. In a beatclck gameplay run public 7 scores 3,000 like the other five, and closing it last "
			"completes the bank for a 53,000 award, as closing 2 last does for 103,000; public 19 stays raised. by6803 "
			"leaves public 7 an ordinary matrix switch; the run's tilt bob is public 15, which drops 19 on its second "
			"closure, and the table's vpmNudge.TiltSwitch is 15."
		),
	},
	{
		"path": "machines/partial/bally/beat-the-clock-1985.json",
		"machine_id": "bally.beat-the-clock.1985",
		"conflict_id": "conflict.pinmame-input-switch-16-none",
		"binding": {"group": "pinmame.input.switch", "device": 16},
		"from": {"id": "switch.slam-tilt", "label": "Slam Tilt"},
		"id": "switch.wire-trigger.16",
		"label": "Wire Trigger",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_slam_tilt"}],
		"source": BEAT_THE_CLOCK_IN_PLAY,
		"extra_sources": [BEAT_THE_CLOCK_VPW],
		"note": (
			"Legacy import set the legacy Bally platform map's 'Slam Tilt' (alias s_slam_tilt) against the game file's "
			"'Wire Trigger'. The known-working VPW table writes public 16 from a playfield object, sw16. In a beatclck "
			"gameplay run a pulse and a 3 s hold of public 16 each score 3,000 and the game continues with public 19 raised, "
			"so the ROM does not read it as a slam. by6803 leaves public 16 an ordinary matrix switch and writes Slam Tilt "
			"to public 14."
		),
	},
	{
		"path": "machines/partial/bally/spectrum-1981.json",
		"machine_id": "bally.spectrum.1981",
		"conflict_id": "conflict.pinmame-input-switch-2-none",
		"binding": {"group": "pinmame.input.switch", "device": 2},
		"from": {"id": "switch.ball-roll-tilt", "label": "Ball Roll Tilt"},
		"id": "switch.left-flipper-button",
		"label": "Left Flipper Button",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_ball_roll_tilt"}],
		"source": SPECTRUM_IN_PLAY,
		"extra_sources": [SPECTRUM_VPW],
		"note": (
			"Legacy import set the legacy Bally platform map's 'Ball Roll Tilt' (alias s_ball_roll_tilt) against the game "
			"file's 'Left Flipper Button'. The known-working VPW table writes public 2 from the left flipper key and public "
			"1 from the right one. In a spectru4 gameplay run raising public 1 kicks the drain-saucer ball into play while "
			"raising public 2 kicks nothing, and holding 2 at 1 for 3 s in play leaves public 19, the flipper-enable relay, "
			"raised, while one tilt-bob (15) closure drops it. The platform alias is dropped. The run does not settle the button's polarity: the ROM launches when public "
			"1 rises, and the table writes 1 and 2 low on key down and high on key up."
		),
	},
	{
		"path": "machines/partial/bally/spectrum-1981.json",
		"machine_id": "bally.spectrum.1981",
		"conflict_id": "conflict.pinmame-input-switch-7-none",
		"binding": {"group": "pinmame.input.switch", "device": 7},
		"from": {"id": "switch.tilt", "label": "Tilt"},
		"id": "switch.top-saucer-kicker",
		"label": "Top Saucer Kicker",
		"kind": "switch",
		"drop_aliases": [{"namespace": "vpe-legacy.switch", "value": "s_tilt"}],
		"source": SPECTRUM_IN_PLAY,
		"extra_sources": [SPECTRUM_VPW],
		"note": (
			"Legacy import set the legacy Bally platform map's 'Tilt' (alias s_tilt) against the game file's 'Top Saucer "
			"Kicker'. The known-working VPW table writes public 7 from the top kicker sw7, which its solenoid 1 and 2 "
			"callbacks kick out. In a spectru4 gameplay run closing public 7 fires the top kicker (1) and scores 10,000, "
			"and public 19 stays raised. The platform alias is dropped: the "
			"run's tilt bob is public 15, as the table's vpmNudge.TiltSwitch is."
		),
	},
]


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def settle(document: dict[str, Any], settlement: dict[str, Any]) -> dict[str, Any]:
	result = json.loads(json.dumps(document))
	if result["machine"]["id"] != settlement["machine_id"]:
		raise RuntimeError(f"{settlement['path']} is not {settlement['machine_id']}")
	matches = [device for device in result["outputs"] + result["inputs"] if device["binding"] == settlement["binding"]]
	if len(matches) != 1:
		raise RuntimeError(f"{settlement['path']}: expected one device at {settlement['binding']}, found {len(matches)}")
	device = matches[0]
	source = settlement["source"]
	group, number = settlement["binding"]["group"], settlement["binding"]["device"]
	target_id = settlement.get("id", f"device.{slug(settlement['label'])}")
	pending = [conflict for conflict in result["conflicts"] if conflict["id"] == settlement["conflict_id"]]
	if pending:
		# Unsettled: the conflict must sit on this binding and the device must still be the imported one.
		if [conflict["path"] for conflict in pending] != [f"binding:{group}/{number}/None"]:
			raise RuntimeError(f"{settlement['path']}: {settlement['conflict_id']} is not on {group}/{number}")
		expected = (settlement["from"]["id"], settlement["from"]["label"])
	else:
		expected = (target_id, settlement["label"])
	if (device["id"], device["label"]) != expected:
		raise RuntimeError(f"{settlement['path']}: the device at {group}/{number} is {device['id']} ({device['label']!r}), expected {expected}")
	namespace = "pinmame.coil" if group == "pinmame.output.solenoid" else "pinmame.switch"
	numbers = {alias["value"] for alias in device.get("aliases", []) if alias["namespace"] == namespace}
	if numbers != {str(number)}:
		raise RuntimeError(f"{settlement['path']}: the device at {group}/{number} carries {namespace} aliases {sorted(numbers)}")
	device["id"] = target_id
	device["label"] = settlement["label"]
	device["kind"] = settlement["kind"]
	device["aliases"] = [alias for alias in device.get("aliases", []) if alias not in settlement["drop_aliases"]]
	extra = settlement.get("extra_sources", [])
	cited = [source["id"], *(item["id"] for item in extra)]
	refs = [ref for ref in device["provenance"]["source_refs"] if ref not in cited] + cited
	device["provenance"] = {"source_refs": refs, "status": "observed"}
	device.setdefault("physical", {})["notes"] = settlement["note"]
	identifiers = [item["id"] for item in result["outputs"] + result["inputs"]]
	if identifiers.count(device["id"]) != 1:
		raise RuntimeError(f"{settlement['path']}: {device['id']} would not be unique")
	result["conflicts"] = [conflict for conflict in result["conflicts"] if conflict["id"] != settlement["conflict_id"]]
	record = {
		"id": source["id"],
		"kind": "runtime_scenario",
		"uri": source["uri"],
		"revision": RUNTIME_PINMAME_REVISION,
		"locator": source["locator"],
		"license": "NOASSERTION",
		"attribution": ATTRIBUTION,
	}
	# Replace in place, so that settlements sharing a source leave the source list stable on re-application.
	for item in [record, *extra]:
		positions = [index for index, existing in enumerate(result["sources"]) if existing["id"] == item["id"]]
		if positions:
			result["sources"][positions[0]] = item
		else:
			result["sources"].append(item)
	unresolved = [conflict for conflict in result["conflicts"] if conflict.get("status", "unresolved") == "unresolved"]
	if not unresolved:
		result["coverage"]["missing"] = [item for item in result["coverage"]["missing"] if item != "unresolved_conflicts"]
	elif "unresolved_conflicts" not in result["coverage"]["missing"]:
		raise RuntimeError(f"{settlement['path']}: {len(unresolved)} unresolved conflict(s) remain but coverage.missing omits unresolved_conflicts")
	return result


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	parser.add_argument("--check", action="store_true", help="verify without writing")
	parser.add_argument("--root", type=Path, default=ROOT)
	args = parser.parse_args()
	drift = []
	for settlement in SETTLEMENTS:
		path = args.root / settlement["path"]
		current = json.loads(path.read_text(encoding="utf-8"))
		if any(conflict["id"] == settlement["conflict_id"] for conflict in current["conflicts"]):
			if args.check:
				drift.append(f"{settlement['path']}: {settlement['conflict_id']} is still recorded")
				continue
			path.write_bytes(canonical_bytes(settle(current, settlement)))
			print(f"settled {settlement['conflict_id']} in {settlement['path']}")
			continue
		# Already settled: re-applying must change nothing.
		if canonical_bytes(settle(current, settlement)) != path.read_bytes():
			drift.append(f"{settlement['path']}: record differs from the settlement")
	for line in drift:
		print(line, file=sys.stderr)
	if drift:
		return 1
	print(f"{len(SETTLEMENTS)} legacy label settlement(s) verified" if args.check else "done")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
