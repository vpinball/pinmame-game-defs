"""Reviewed Meteor (Stern, 1979) device data, kept apart from the builder so both stay readable.

Every number below was read from this game's own 40-page manual (with its schematic sheets) and its self-test card, or observed in a retained
harness run; none is carried from a sister machine. Where a Stern MPU-200 board drawing is shared with other games, this game's own lettered
copy of the sheet was read.
"""

from __future__ import annotations

from typing import Any

# --- Drivers ---------------------------------------------------------------------------------------------------------

_SIX_DIGIT = ("Identical INITGAME data to the production driver (GEN_STMPU200, six-digit dispst6 displays, FLIP_SW(FLIP_L), no extra lamp columns, Stern ST300 "
	"sound board, input_ports_st), so the controller inventory is unchanged.")
_SEVEN_DIGIT = ("Same game data as the production driver except the display layout: seven-digit dispst7 player displays (segment starts 1, 9, 17 and 25, width 7), "
	"recorded as display overrides. A seven-digit conversion needs replacement player displays; the playfield, matrix, solenoids and lamps are unchanged.")
_NO_SET = "No ROM set for it is in the authorized library, so no harness run was made."
_RUN_DRAIN = ("Across the drain and the next serve taken together it fires meteor's outhole kick (15) and bank resets (3, 7, 9, 13), though not in the same windows: meteor's run fired "
	"them before the served ball left the outhole and only target restores after it, while this run fires them again after it. No METEOR target switch closed before its drain and it "
	"fired no knock-down coil there, where meteor's run, with four METEOR targets down, also restored those four.")
_RUN = ("A retained harness run of it fires the same set of solenoids as the same step of meteor's gameplay run for the thumper, both slingshots, the stand-up target, the right "
	"three-bank and both flipper buttons (only solenoid sets were compared, not firing order, timing or lamps). " + _RUN_DRAIN)
_RUN_SPOT = ("A retained harness run of it fires the same set of solenoids as the same step of meteor's gameplay run for the thumper, both slingshots, the right three-bank and both "
	"flipper buttons (only solenoid sets were compared, not firing order, timing or lamps). Its stand-up target fires one knock-down coil, as meteor's does, but spots a different "
	"METEOR target (knock-down coil {coil} where meteor fired 12); the ROM picks the target it spots, and the harness does not drop a target when its coil fires. " + _RUN_DRAIN)

DRIVERS: dict[str, tuple[str, str, str, str | None, str, bool]] = {
	# id: (description, year, manufacturer, clone_of, notes, seven-digit)
	"meteor": (
		"Meteor", "1979", "Stern", None,
		"Production ROM set (U1, U2, U5 and U6) and the reference for this definition: GEN_STMPU200, six-digit dispst6 displays, FLIP_SW(FLIP_L), Stern ST300 sound board. "
		"The five reference harness runs (self test, solenoid test, switch test, coin bookkeeping and the scripted game) boot this driver; each variant probe boots its own ROM set. Its U1 is Stern's original, which the PinMAME source calls buggy; meteora carries Stern's factory fix.", False,
	),
	"meteora": (
		"Meteor (Bonus Count Offical Fix)", "1979", "Stern", None,
		"Stern's factory bug-fixed U1 (`cpu_u1a.716`; the PinMAME comment: `U1A is Stern's factory bug-fixed version of their original buggy U1`) with the production U5, U2 and U6. "
		"PinMAME declares it as a second root, not as a clone of meteor. " + _SIX_DIGIT + " The source quotes community accounts that the original U1 can count the bonus down from "
		"255X when the collect-all-rockets routine and the bonus collect share a RAM location. " + _RUN, False,
	),
	"meteora2": (
		"Meteor (Bonus Count and Sound Fix)", "2019", "Stern / Idleman", "meteor",
		"Community build of the factory-fixed U1A with a U6 that clears the sound registers at boot (PinMAME comment). " + _SIX_DIGIT + " " + _NO_SET, False,
	),
	"meteorbf": (
		"Meteor (Bonus Count Fix)", "1979", "Stern", "meteor",
		"The production U1 and U5 with a differently fixed U2 and U6 (the PinMAME comment: `before it was known what meteora actually fixed`). " + _SIX_DIGIT + " " + _RUN, False,
	),
	"meteorfp": (
		"Meteor (Free Play)", "1979", "Stern", "meteor",
		"Free-play U1 and U6 with the production U5 and U2. " + _SIX_DIGIT + " " + _RUN_SPOT.format(coil=14), False,
	),
	"meteorns": (
		"Meteor (No Background Sound)", "2011", "Stern / Scott", "meteor",
		"Community patch that removes the background sound (the PinMAME comment quotes a rec.games.pinball posting: U1 bytes at offsets A6 and A9 and U2 bytes at CC-CD, which also drops "
		"the add-a-player sound). " + _SIX_DIGIT + " " + _NO_SET, False,
	),
	"meteore": (
		"Meteor (Bonus Count Fix, MOD, Free Play rev. 64)", "2019", "Stern / Idleman", "meteor",
		"Free-play community rules modification with the bonus count fix, revision 64, in four new ROM images. " + _SIX_DIGIT + " " + _NO_SET, False,
	),
	"meteorf": (
		"Meteor (Bonus Count Fix, MOD, Free Play rev. 65)", "2020", "Stern / Idleman", "meteor",
		"Free-play community rules modification with the bonus count fix, revision 65, in four new ROM images. " + _SIX_DIGIT + " " + _NO_SET, False,
	),
	"meteorg": (
		"Meteor (Bonus Count Fix, MOD, Free Play rev. 66)", "2021", "Stern / Idleman", "meteor",
		"Free-play community rules modification, revision 66, in four new ROM images (PinMAME comment: `Adds some features, fixes endless bonus bug`). " + _SIX_DIGIT + " " + _NO_SET, False,
	),
	"meteorb": (
		"Meteor (7-digit conversion)", "2003", "Stern / Oliver", "meteor",
		"Community seven-digit conversion: the production U1 with new U5, U2 and U6. " + _SEVEN_DIGIT + " Both known-working scripts and the retained table boot this driver. " + _RUN, True,
	),
	"meteorc": (
		"Meteor (7-digit conversion Free Play)", "2003", "Stern / Oliver", "meteor",
		"Free-play build of the seven-digit conversion in four new ROM images. " + _SEVEN_DIGIT + " " + _RUN_SPOT.format(coil=8), True,
	),
	"meteord": (
		"Meteor (/10 Scoring)", "2005", "Stern / Oliver", "meteor",
		"Community build that divides every score by ten, on the seven-digit layout (the production U1, a /10 U5 and the free-play conversion's U2 and U6). " + _SEVEN_DIGIT + " "
		+ _RUN_SPOT.format(coil=8), True,
	),
	"meteore7": (
		"Meteor (Bonus Count Fix, MOD, 7-Digit, Free Play rev. 74)", "2019", "Stern / Idleman", "meteor",
		"Seven-digit build of the free-play community rules modification, revision 74. " + _SEVEN_DIGIT + " " + _NO_SET, True,
	),
	"meteorf7": (
		"Meteor (Bonus Count Fix, MOD, 7-Digit, Free Play rev. 75)", "2020", "Stern / Idleman", "meteor",
		"Seven-digit build of the free-play community rules modification, revision 75. " + _SEVEN_DIGIT + " " + _NO_SET, True,
	),
	"meteorg7": (
		"Meteor (Bonus Count Fix, MOD, 7-Digit, Free Play rev. 76)", "2021", "Stern / Idleman", "meteor",
		"Seven-digit build of the free-play community rules modification, revision 76 (PinMAME comment: `Adds some features, fixes endless bonus bug`). " + _SEVEN_DIGIT + " " + _NO_SET, True,
	),
}

# --- Cabinet and service inputs ---------------------------------------------------------------------------------------

SERVICE_SWITCHES: dict[int, dict[str, Any]] = {
	-7: {
		"id": "switch.self-test-button", "label": "Self Test button (coin door)", "roles": ["service.test"], "availability": "used",
		"location": "Inside the coin door",
		"notes": "The self-test card's `BUTTON LOCATED INSIDE OF COIN DOOR`; the cabinet wiring sheet draws `TEST SWITCH` from A4J3-1 (R) to A3J2-7 (Y-R). Public -7 drives the ROM's tests in the "
			"manual's order: in the retained runs the first press starts the burn-in, the second the lamp test, the third the display test, the fourth the solenoid test and the fifth the switch "
			"test. From the sixth press on, the manual's table (PDF page 5) steps through the bookkeeping functions 01-18 on the match/ball-in-play display; the retained "
			"coin-bookkeeping run's sixteenth press reached function 11.",
		"evidence": "manual-and-harness",
	},
	-6: {
		"id": "switch.mpu-diagnostic-s33", "label": "MPU S33 / CPU diagnostic NMI", "roles": ["service.diagnostic"], "availability": "used",
		"location": "MPU assembly in the backbox (Figure 1)", "manual_address": "S33", "quantity": 1,
		"wiring": {"board": "MPU module M-200 A4", "control_connection": "U9-6 (NMI)", "return_connection": "Ground"},
		"notes": "Figure 1 draws `S33` as a round pushbutton on the MPU assembly. The MPU 200 schematic 12B-602-S (PDF page 30) draws S33 from ground to the node of R11 (1.2K to +5V) and C87 "
			"(.01 MFD), which runs to the NMI input (pin 6) of the 6800 MPU U9: a momentary contact, open at rest, that pulls NMI low. PinMAME routes public -6 to the same NMI line "
			"(BY35_SWCPUDIAG, under `Diagnostic buttons on CPU board`; its LISY build reads that line as `lisy35_get_SW_S33()`), so -6 is this button. A footnote to the first score level of the front-door high score "
			"adjustment gives its one operating instruction: `*Can be quickly set to '00' by pressing S33 on the MPU assembly in the back box.` (PDF page 6). IPDB's schematic "
			"errata add a `Memory Clear Switch; R-Y common to Test Switch, W to A4J3-5 (MPU)` that the switch-matrix page omits; that remote contact is a lead only, because the standard "
			"interboard wiring diagram 12B-STD.-110-2 prints MPU A4J3-5 `N.U`, so no remote contact is recorded. The retained runs never pressed -6, so no ROM response is claimed.",
		"evidence": "mpu-s33",
	},
	-5: {
		"id": "input.sound-diagnostic-voice-select", "label": "ST300 sound diagnostic / voice-select state", "availability": "used", "virtual": True,
		"notes": "PinMAME passes public -5 (BY35_SWSOUNDDIAG) to the ST300 sound board's diagnostic callback on every switch update, and `st300_switch_w` stores it as `voiceSw`: while it is "
			"set, `st300_ctrl_w` sends the next control write to the S14001A speech path instead of the tone generator, so it is a meaningful emulator route. No fitted "
			"sound-diagnostic contact is established for this machine, so no physical contact, polarity or fitment is recorded; do not infer one from the route. Leave it open; the "
			"retained runs never set it.",
		"evidence": "core",
	},
}

# --- Matrix switches ----------------------------------------------------------------------------------------------------
#
# Public address = strobe * 8 + return + 1 on the five-strobe by eight-return MPU matrix. The playfield sheet (manual PDF page 36) draws all forty
# cells on MPU connector A4J2; the cabinet and front door sheet (PDF pages 32-33) draws the cabinet switches on A4J3.

STROBES = {0: ("W-R", "A4J2-1"), 1: ("BRN-W", "A4J2-2"), 2: ("W-BLU", "A4J2-3"), 3: ("W-Y", "A4J2-4"), 4: ("Y-R", "A4J2-5")}
CABINET_STROBE0 = ("R-Y", "A4J3-2")
RETURNS = {
	0: ("BRN", "A4J2-8"), 1: ("GREY", "A4J2-9"), 2: ("W-O", "A4J2-10"), 3: ("W-B", "A4J2-11"),
	4: ("W-G", "A4J2-12"), 5: ("W-BRN", "A4J2-13"), 6: ("BRN-Y", "A4J2-14"), 7: ("O", "A4J2-15"),
}
CABINET_RETURNS = {0: ("R-W", "A4J3-9"), 1: ("BRN-W", "A4J3-10"), 2: ("BLU", "A4J3-11"), 5: ("BLU-W", "A4J3-14"), 6: ("BLU-O", "A4J3-15"), 7: ("Y", "A4J3-16")}
# Cells the playfield sheet draws without a series diode, and cells with a capacitor drawn across the contact.
NO_DIODE_SWITCHES = {1, 2, 3, 6, 9, 25}
CAPACITOR_SWITCHES = {10, 11, 12, 20, 21, 22, 23, 24}
# The cabinet sheet's own diode marks for the cabinet positions (True = drawn).
CABINET_DIODES = {1: True, 2: False, 3: False, 6: True, 7: True, 8: True}
UNUSED_SWITCHES = {17, 18, 25, 26}

_THREE_BANK = {
	"right": ("Right three-bank", "RT. 3-BANK", "3-Bank Drop-Targets (Right)", "public 9"),
	"top-left": ("Top left three-bank", "TOP LEFT 3-BANK", "3-Bank Drop-Target (Top Left)", "public 3"),
	"lower-left": ("Lower left three-bank", "LOWER LFT. 3-BANK", "3-Bank Drop Target (Left Center)", "public 7"),
}

# address -> spec. ``card`` is the self-test card's switch list, ``matrix`` the playfield sheet's cell (None where the sheet draws the contact without a
# label), ``cabinet_cell`` the cabinet sheet's cell for the cabinet positions.
SWITCHES: dict[int, dict[str, Any]] = {
	1: {"id": "switch.coin-chute-left", "label": "Left coin chute (hinge side)", "type": "other", "cabinet": True, "roles": ["cabinet.coin.1"], "card": "Coin Chute", "matrix": None, "cabinet_cell": "CHUTE #3",
		"notes": "The hinge-side chute: the self-test card numbers the coin switches 1-3 as `SW1 SW2 SW3` from the hinge side on a three-chute door (a two-chute door has SW2 and SW3), and the credit table "
			"gives the chute next to the hinge switches 28-30. The ROM confirms the pairing: in the retained coin-bookkeeping run one coin on public 1 is counted only by bookkeeping function 09 "
			"(`Number of coins thru Chute No. 2`), two coins on public 2 only by 10 (`Chute No. 1`) and three on public 3 only by 11 (`Chute No. 3`), so this chute is the switch-assignment page's "
			"`Coin Chute #1 Germany or #2 All Others` on switches 28-30. The cabinet sheet labels this cell `CHUTE #3`; its chute numbers run from the other side and are labels only."},
	2: {"id": "switch.coin-chute-center", "label": "Center coin chute", "type": "other", "cabinet": True, "roles": ["cabinet.coin.2"], "card": "Coin Chute", "matrix": None, "cabinet_cell": "CHUTE #2",
		"notes": "The center chute (`#2 (CENTER CHUTE)` on switches 1-5 in the credit table, the switch-assignment page's `Coin Chute No. 2 Germany or No. 1 All Others`). In the retained "
			"coin-bookkeeping run, at PinMAME's default option switches (S1-S5 all OFF, the credit table's `3/2 COINS**`), its first coin gave one credit and its second two, and bookkeeping function 10 "
			"(`Chute No. 1`) counted both."},
	3: {"id": "switch.coin-chute-right", "label": "Right coin chute", "type": "other", "cabinet": True, "roles": ["cabinet.coin.3"], "card": "Coin Chute", "matrix": None, "cabinet_cell": "CHUTE #1",
		"notes": "The right chute (`#3 (RIGHT CHUTE)` on switches 9-13); bookkeeping function 11 (`Chute No. 3`) counted its three coins in the retained coin-bookkeeping run. The cabinet sheet labels "
			"this cell `CHUTE #1`."},
	4: {"id": "switch.stand-up-target", "label": "Stationary stand-up target", "type": "leaf", "pulse": True, "card": "Stand-up Target", "matrix": "S.U. TARG.",
		"notes": "The center stationary target (IPDB `Standup target (1)`; playfield parts `TARGET ASS'Y A-461-2Y`). The manual: scores 500, plus 1,500 and a spotted METEOR target when lit, or "
			"awards the WOW or the special when those are lit. In the retained gameplay run, with lamp 5 lit, its closure fired the knock-down coil of the METEOR `O` target (public 12) and put "
			"lamp 5 out."},
	5: {"id": "switch.spinner", "label": "Spinner", "type": "other", "pulse": True, "card": "Spin Target", "matrix": "SPIN. TARG.",
		"notes": "The spinning target (`SPIN TARGET A-563-9`, `TARGET & WIRE ONLY 14A-7-8`). Each rotation closes the contact once; each spin scores 200 plus 600 for each end and 200 for each middle "
			"METEOR target down (manual)."},
	6: {"id": "switch.credit-button", "label": "Credit (start) button", "type": "button", "cabinet": True, "roles": ["cabinet.start"], "card": "Credit Button", "matrix": "CREDIT", "cabinet_cell": "CREDIT",
		"notes": "Coin-door credit button. In the retained runs it starts a game from credits."},
	7: {"id": "switch.tilt", "label": "Tilt (plumb bob, ball and panel tilts)", "type": "tilt", "cabinet": True, "roles": ["cabinet.tilt"], "card": "Tilts", "matrix": "TILTS", "cabinet_cell": "TILT",
		"quantity": 3, "location": "Cabinet (plumb bob and ball tilts) and the underside of the playfield panel (panel tilt)",
		"notes": "Shared matrix position for the tilt contacts. The installation page says `Check adjustment of the three (normally open) tilt switches` and names them: a plumb bob tilt on the left "
			"side of the cabinet near the front door, a ball tilt above it (the smaller `gold 15/16\" dia.` ball) and a panel tilt on the bottom of the playfield panel; Figure 1 labels `PLUMB BOB "
			"TILT` and `INCLINED TILT`, the cabinet sheet draws `TILT` with a second unlabelled contact in parallel, and beside them a capacitor whose two leads both join the same uninterrupted lead from the row line, and the playfield sheet prints `TILTS`. Closing public 7 in play "
			"drops the flipper enable output 19 and lights TILT (lamp 61) in the retained gameplay run. No sheet draws the panel tilt's position under the playfield, and it is a tilt "
			"detector, not a device the ball touches, so the input keeps a cabinet/service spatial record and no placement is asserted for that contact."},
	8: {"id": "switch.slam", "label": "Slam (door, tilt board and playfield)", "type": "tilt", "cabinet": True, "roles": ["cabinet.slam-tilt"], "card": "Slam & Vib. Tilts", "matrix": "SLAM", "cabinet_cell": "SLAM",
		"quantity": 3, "location": "Front door, tilt board and playfield",
		"notes": "Shared matrix position for the slam contacts. The general operation page says `There is a slam switch on the front door, one on the tilt board and one on the playfield`, the three "
			"the game ships with, and adds `(Any number of slam switches could be installed by the operator, to meet his individual requirement)`, so a cabinet may carry more on this position; the "
			"self-test card names it `Slam & Vib. Tilts`. In the retained gameplay run, closing public 8 in play ends the game and the ROM repeats its power-up initialisation of the four "
			"continuous outputs. No sheet draws where the playfield slam switch is mounted, and it is a slam detector, not a device the ball touches, so the input keeps a cabinet/service "
			"spatial record and no placement is asserted for that contact."},
	12: {"id": "switch.upper-right-scoring-bumper", "label": "Upper right scoring bumper", "type": "leaf", "pulse": True, "card": "Bumper (Upper Right)", "matrix": "BUMPER / UP. R.T.",
		"notes": "One of the two passive scoring bumpers (IPDB `Passive bumpers (2)`; playfield parts `BUMPER CAP 13A-32-1 & 3`); no coil. The manual: 500 with no bonus, otherwise the corresponding "
			"missile value, and it advances the missiles when lit. In the retained gameplay run it changed no lamp or solenoid; the score display advanced and sound commands were sent."},
	13: {"id": "switch.upper-left-scoring-bumper", "label": "Upper left scoring bumper", "type": "leaf", "pulse": True, "card": "Bumper (Upper Left)", "matrix": "BUMPER / UP. LFT.",
		"notes": "The other passive scoring bumper; it scores as switch 12 does (manual). In the retained gameplay run it changed no lamp or solenoid; the score display advanced and sound commands were sent."},
	14: {"id": "switch.thumper-bumper", "label": "Thumper bumper", "type": "leaf", "pulse": True, "card": "Thumper Bumper", "matrix": "THUMPER",
		"notes": "The single powered bumper (`Thumper Bumper (1) J-26-1200`; `THUMPER CAP 4A-134-R`). Scores 1,000 in three-ball and 100 in five-ball games (manual); the ROM fires public 2, the "
			"thumper coil, in the retained gameplay and variant runs."},
	15: {"id": "switch.right-slingshot", "label": "Right slingshot", "type": "leaf", "pulse": True, "card": "Right Sling-Shot", "matrix": "RIGHT SLING-ST.",
		"notes": "Scores 10 (manual); the ROM fires public 10, the right slingshot coil, in the retained gameplay and variant runs, and not while the game is tilted."},
	16: {"id": "switch.left-slingshot", "label": "Left slingshot", "type": "leaf", "pulse": True, "card": "Left Sling-Shot", "matrix": "L.SLING-S.",
		"notes": "Scores 10 (manual); the ROM fires public 1, the left slingshot coil, in the retained gameplay and variant runs."},
	33: {"id": "switch.outhole", "label": "Outhole", "type": "leaf", "initial_active": True, "card": "Out-Hole", "matrix": "OUT-HOLE",
		"notes": "The single outhole switch under the apron, where the drained ball rests in front of the outhole kicker. Meteor has no ball trough: one ball is in the machine, and the known-working "
			"scripts model it with one switch (`bsTrough.Initsw 0,33,0,0,0,0,0,0`). In the retained runs the ROM repeats the outhole kick and the bank resets while 33 stays closed at a serve."},
	34: {"id": "switch.right-outlane", "label": "Right outlane", "type": "leaf", "card": "Right Out-Lane", "matrix": "R.OUT-LANE",
		"notes": "The manual: scores 3,000, and when lit 1,000 more for each missile lamp lit."},
	35: {"id": "switch.left-outlane", "label": "Left outlane", "type": "leaf", "card": "Left Out-Lane", "matrix": "LEFT OUT-LANE",
		"notes": "The manual: scores 3,000, and when lit 1,000 more for each missile lamp lit."},
	36: {"id": "switch.right-return-lane", "label": "Right return lane", "type": "leaf", "card": "Right Return Lane", "matrix": "R.RETURN LANE",
		"notes": "The manual: scores 500, and when lit 1,500 more and spots a METEOR target."},
	37: {"id": "switch.left-return-lane", "label": "Left return lane", "type": "leaf", "card": "Left Return Lane", "matrix": "L.RETURN LANE",
		"notes": "The manual: scores 500, and when lit 1,500 more and spots a METEOR target."},
	38: {"id": "switch.upper-rollover-button", "label": "Upper star rollover", "type": "leaf", "card": "Roll-Over Button (Upper)", "matrix": "UPPER R.O.B.",
		"notes": "The rightmost and highest of the three star rollovers on the upper left diagonal (`ROLL-OVER BUTTON 4B-275`; IPDB `Star rollovers (3)`). The manual: 2,000 or 6,000 and a spotted "
			"METEOR target when lit, 500 when not. In the retained gameplay run, with lamp 25 lit, it fired the knock-down coil of the second METEOR `E` (public 11) and put lamp 25 out."},
	39: {"id": "switch.middle-rollover-button", "label": "Middle star rollover", "type": "leaf", "card": "Roll-Over Button (Center)", "matrix": "MIDDLE R.O.B.",
		"notes": "The middle star rollover; it scores as switch 38 does (manual). Its spot lamp (5) was already out in the retained gameplay run, and it fired no coil."},
	40: {"id": "switch.lower-rollover-button", "label": "Lower star rollover", "type": "leaf", "card": "Roll-Over Button (Lower)", "matrix": "LOWER R.O.B.",
		"notes": "The lowest and leftmost star rollover; it scores as switch 38 does (manual). In the retained gameplay run, with lamp 9 lit, it fired the knock-down coil of the METEOR `O` (public 12) and put lamp 9 out."},
}
# Three-target banks: the playfield sheet prints each bank's cells TOP, LOWER and MID in matrix order.
for _bank, _addresses in (("right", (9, 10, 11)), ("top-left", (19, 20, 21)), ("lower-left", (22, 23, 24))):
	_label, _printed, _card, _reset = _THREE_BANK[_bank]
	_suffixes = {"right": ("TOP TARG.", "LOWER TARG.", "MID. TARG."), "top-left": ("TOP TARG.", "LOW. TARG", "MID. TARG"), "lower-left": ("TOP TARG.", "LOW TARG", "MID. TARG")}[_bank]
	for _position, _address, _suffix in zip(("top", "bottom", "middle"), _addresses, _suffixes):
		SWITCHES[_address] = {
			"id": f"switch.{_bank}-bank-{_position}-target", "label": f"{_label} {_position} target", "type": "leaf", "drop": True, "card": _card, "matrix": f"{_printed} / {_suffix}",
			"bank": _bank, "position": _position,
			"notes": f"The {_position} target of the {_label.lower()} drop-target bank (playfield parts `3-BANK TARGET D-580-1 to 3`), raised by its reset coil ({_reset}); it has no knock-down coil. "
				"Closed while the target is down. The playfield sheet prints the bank's three cells in matrix order as top, lower and middle target, which the known-working scripts bind as top, "
				"middle and lower (see the conflict record). Each hit advances the bank's row of missile "
				"lamps and scores the advanced value (manual); the special the bank lights is awarded on its center target (manual, special award chart)."
				+ (" In the retained gameplay run the host closed this address last of the bank's three, and the ROM fired the bank's reset coil." if _position == "middle" else ""),
		}
# The six-target METEOR bank: 32 is M, then E, T, E, O and R (27).
METEOR_LETTERS = {32: ("m", "M", "\"M\" TARG."), 31: ("first-e", "first E", "\"E\" TARG."), 30: ("t", "T", "\"T\" TARG."), 29: ("second-e", "second E", "\"E\" TARG."),
	28: ("o", "O", "\"O\" TARG."), 27: ("r", "R", "\"R\" TARG.")}
for _address, (_slug, _letter, _cell) in METEOR_LETTERS.items():
	SWITCHES[_address] = {
		"id": f"switch.meteor-bank-{_slug}-target", "label": f"METEOR bank {_letter} target", "type": "leaf", "drop": True, "card": "6-Bank Drop Targets", "matrix": f"6-BANK / {_cell}",
		"letter": _letter,
		"notes": f"The {_letter} target of the six-target METEOR drop bank (`6-BANK TARGET D-548-6A`), which reads M-E-T-E-O-R from left to right. Closed while the target is down. "
			+ ("An end target: scores 6,000 and lights the spinner for 600 more (manual)." if _address in (27, 32) else "A middle target: scores 2,000 and lights the spinner for 200 more (manual).")
			+ " It has its own knock-down coil, with which the ROM spots it and restores each player's targets after a drain (the bank's memory)."
			+ (" In the retained gameplay run its fall completed the bank and the ROM fired the bank reset (public 13) about every 1.2 s while the host kept the targets down." if _address == 27 else ""),
	}
for _address in sorted(UNUSED_SWITCHES):
	SWITCHES[_address] = {
		"id": f"switch.unused-matrix-{_address}", "label": f"Unused matrix position {_address}", "type": "other", "unused": True, "card": "Open", "matrix": "N/U",
		"notes": f"The self-test card lists {_address} as `Open` and the playfield sheet prints its cell `N/U` (`N/U = NOT USED`); nothing is wired to it. In the retained switch test the ROM "
			f"shows {_address} when the host closes it, which proves only that the matrix position is scanned.",
	}

# Flipper buttons: PinMAME synthetic switches 81-84 (FLIP_SW(FLIP_L)): right 82, left 84; 81/83 are the generic upper positions.
FLIPPER_BUTTONS = {
	82: ("switch.right-flipper-button", "Right flipper button", "flipper.button.right", "R", "A3J2-1"),
	84: ("switch.left-flipper-button", "Left flipper button", "flipper.button.left", "BLU", "A3J2-2"),
}
UNUSED_FLIPPER_POSITIONS = {
	81: ("switch.upper-right-flipper-position", "Upper right flipper button position (no separate button)"),
	83: ("switch.upper-left-flipper-position", "Upper left flipper button position (no separate button)"),
}

# --- Solenoids ----------------------------------------------------------------------------------------------------------
#
# The ROM's own solenoid test pulses drivers 1-19 in order and shows each SDU transistor (Q) number on the player displays; the public addresses that fire
# are, in that order (retained solenoid-test run):
SELF_TEST_ORDER = (2, 1, 6, 7, 3, 4, 5, 8, 11, 12, 14, 13, 9, 10, 19, 15, 17, 20, 18)
PHYSICAL_TO_PUBLIC = {number: address for number, address in enumerate(SELF_TEST_ORDER, start=1)}

# The Solenoid Driver schematic 12B-432-S113 (manual PDF pages 24-25): Q -> (connector, wire, printed load) and the self-test card's solenoid list.
SDU_LOADS: dict[int, tuple[str, str, str]] = {
	1: ("J2-9", "PUR-W", "CENTER THUMPER"), 2: ("J2-4", "BRN", "LEFT SLING-SHOT"), 3: ("J2-5", "B-Y", "KNOCKER"), 4: ("J1-5", "BRN-Y", "LEFT BOTTOM DROP TARGET"),
	5: ("J2-10", "G-R", "LEFT TOP DROP TARGET"), 6: ("J2-11", "GREY", "\"M\" TARGET"), 7: ("J2-12", "Y-B", "M\"E\"T TARGET"), 8: ("J5-10", "B-Y", "\"T\" TARGET"),
	9: ("J5-9", "O-R", "MET\"E\" TARGET"), 10: ("J5-15", "B-BLU", "\"O\" TARGET"), 11: ("J5-14", "Y-BLU", "\"R\" TARGET"), 12: ("J5-13", "O-W", "METEOR DROP TARGET"),
	13: ("J5-12", "O-B", "RT. DROP TARGET"), 14: ("J5-11", "O-W", "RT. SLING-SHOT"), 15: ("J3-5", "Y-W", "FLIPPER ENABLE RELAY"), 16: ("J5-8", "R-B", "OUT-HOLE"),
	17: ("J5-7", "", "N/U"), 18: ("J2-15", "", "N/U"), 19: ("J2-8", "Y-W", "COIN LOCK-OUT"),
}
# The SDU sheet's own wire reading where the structured wire comes from another sheet: Q14's J5-11 legend is struck through, and the playfield coil sheet gives O-W.
SDU_PRINTED_WIRES: dict[int, str] = {14: "a struck-through `(-B-)` wire"}
CARD_SOLENOIDS: dict[int, str] = {
	1: "Thumper Bumper", 2: "Left Sling Shot", 3: "Knocker", 4: "3-Bank Drop Target (L. Bottom)", 5: "3-Bank Drop Target (L. Top)",
	**{number: "6-Bank Drop Targets" for number in range(6, 12)}, 12: "6-Bank Drop Target (Reset)", 13: "3-Bank Drop Target (Right)", 14: "Right Sling-Shot",
	15: "Flippers", 16: "Out-Hole", 19: "Coin Lock-Out",
}

# public address -> spec. ``letter`` is the METEOR target a knock-down coil drops; ``q`` the SDU driver.
SOLENOIDS: dict[int, dict[str, Any]] = {
	1: {"id": "device.left-slingshot", "label": "Left slingshot", "kind": "coil", "part": "J-27-1700",
		"notes": "Fired when the left slingshot switch (public 16) closes in the retained gameplay and variant runs. The playfield coil sheet prints `LEFT SLING SHOT A3J2-4 (BRN-)`. Neither known-working "
			"script has a SolCallback for it: the table's slingshot kicks on its own hit."},
	2: {"id": "device.thumper-bumper", "label": "Thumper bumper", "kind": "coil", "part": "J-26-1200",
		"notes": "Fired when the thumper switch (public 14) closes in the retained gameplay and variant runs. The playfield coil sheet prints `THUMPER A3J2-4 (PUR-W)`; the wire colour is the SDU's J2-9 "
			"and the pin repeats the left slingshot's, so the definition follows the SDU sheet's J2-9, a connector-pin reading only. Neither known-working script has a SolCallback for it: the table's "
			"bumper kicks on its own hit."},
	3: {"id": "device.top-left-bank-reset", "label": "Top left three-bank reset", "kind": "coil", "part": "B-27-2300",
		"notes": "Raises the top left three-target bank (19-21; playfield coil sheet `TOP LFT. 3-BANK DROP TARG.` on A3J2-10 (G-R)). Fired at every serve and when the bank's last target falls "
			"(retained gameplay run)."},
	4: {"id": "device.meteor-m-knock-down", "label": "METEOR M target knock-down coil", "kind": "coil", "part": "C1-34-3400", "letter": 32},
	5: {"id": "device.meteor-first-e-knock-down", "label": "METEOR first E target knock-down coil", "kind": "coil", "part": "C1-34-3400", "letter": 31,
		"wire_note": " The playfield coil sheet prints this coil's wire as (Y-W) on A3-J2-12. A wire-colour reading only; the definition follows the SDU sheet."},
	6: {"id": "device.knocker", "label": "Knocker", "kind": "coil", "part": "N-26-1200", "cabinet": True, "roles": ["cabinet.knocker"],
		"notes": "In the cabinet: the cabinet sheet draws `KNOCKER` on drive A3J2-5 (B-Y) with a diode across it, fed from the A2J2-2 (G) bus. In the retained gameplay run the ROM fired it once about "
			"2.1 s after the last ball drained, as the final score's last two digits matched the match number and the credits went up by one: a match award (option switch 21, ON at "
			"PinMAME's default). No other award event was exercised."},
	7: {"id": "device.lower-left-bank-reset", "label": "Lower left three-bank reset", "kind": "coil", "part": "B-27-2300",
		"notes": "Raises the lower left three-target bank (22-24; playfield coil sheet `LOWER LFT. 3-BANK DR. TARG.` on A3J1-5 (BRN-Y)). Fired at every serve and when the bank's last target falls "
			"(retained gameplay run)."},
	8: {"id": "device.meteor-t-knock-down", "label": "METEOR T target knock-down coil", "kind": "coil", "part": "C1-34-3400", "letter": 30},
	9: {"id": "device.right-bank-reset", "label": "Right three-bank reset", "kind": "coil", "part": "B-27-2300",
		"notes": "Raises the right three-target bank (9-11; playfield coil sheet `RIGHT 3-BANK DROP TARGET` on A3-J5-12 (O-B)). Fired at every serve and when the bank's last target falls; the ROM "
			"repeats it about every 1.2 s while the host holds all three targets down (retained gameplay run)."},
	10: {"id": "device.right-slingshot", "label": "Right slingshot", "kind": "coil", "part": "J-27-1700",
		"wire_note": " The playfield coil sheet prints `RIGHT SLING SHOT A3J5-11 (O-W)`, which the definition follows. A wire-colour "
			"reading only.",
		"notes": "Fired when the right slingshot switch (public 15) closes in the retained gameplay and variant runs, and not while the game is tilted. Neither known-working script has a SolCallback "
			"for it: the table's slingshot kicks on its own hit."},
	11: {"id": "device.meteor-second-e-knock-down", "label": "METEOR second E target knock-down coil", "kind": "coil", "part": "C1-34-3400", "letter": 29},
	12: {"id": "device.meteor-o-knock-down", "label": "METEOR O target knock-down coil", "kind": "coil", "part": "C1-34-3400", "letter": 28},
	13: {"id": "device.meteor-bank-reset", "label": "METEOR six-target bank reset", "kind": "coil", "part": "B-27-2300",
		"notes": "Raises all six METEOR targets (27-32; the SDU sheet's `METEOR DROP TARGET`, the card's `6-Bank Drop Target (Reset)`). The playfield coil sheet does not draw it. Fired at every serve "
			"and when the bank's last target falls; the ROM repeats it about every 1.2 s while the host holds all six targets down (retained gameplay run). Each completion advances the bonus multiplier (manual). "
			"The parts list counts four `Drop Target Reset` coils B-27-2300: the three three-bank resets and this one."},
	14: {"id": "device.meteor-r-knock-down", "label": "METEOR R target knock-down coil", "kind": "coil", "part": "C1-34-3400", "letter": 27},
	15: {"id": "device.outhole-kicker", "label": "Outhole kicker", "kind": "coil", "part": "J-26-1100",
		"notes": "Kicks the ball resting on the outhole (public 33) into the shooter lane (`Outhole Kicker (1) J-26-1100`; playfield coil sheet `OUT HOLE A3J5-8 (R-B)`). Fired when a game starts and "
			"to serve the next ball after a drain while play continues. In the retained gameplay and variant runs the ROM follows each serve with the four bank resets (public 3, 7, 9 "
			"and 13) and repeats the serve and the resets while 33 stays closed: about every 1.7 s at a game start and after the variant runs' drains. After the gameplay run's two drains "
			"in play it also fires the T, second E, O and R knock-down coils (public 8, 11, 12 and 14) after the first serve, and the second serve follows about 3.0 s after the first "
			"(after the first drain as two kicks 0.10 s apart, followed by one set of bank resets). After the last ball's drain the retained gameplay trace records no pulse of it in the 30 s the host then holds 33 closed "
			"before crediting the next game, so the game ends with the ball in the outhole."},
	17: {"id": "device.unused-continuous-driver-q17", "label": "Unused continuous driver Q17", "kind": "relay", "unused": True,
		"notes": "A continuous-section driver (Q17, PIA PB4 on J4 pin 11 [Y-W]) that the SDU sheet wires only to J5 pin 7 marked `N/U`; the self-test card lists no solenoid 17 and the parts list no "
			"load for it. In the retained runs the ROM drives it only in the power-up initialisation pulse it gives all four continuous lines (at power-up and after a slam) and in its own burn-in "
			"and solenoid tests: it stays off in attract mode, play, drain, tilt and game over. With no load fitted and that pulse explained, it is unused."},
	18: {"id": "device.coin-lockout", "label": "Coin lock-out coil", "kind": "coil", "part": "C-36-5300", "cabinet": True, "roles": ["cabinet.coin-door"],
		"notes": "A continuous output (Q19, PIA PB5 on J4 pin 9 [BLU-O]) to J2 pin 8 [Y-W] `COIN LOCK-OUT` (line label `COIN LD.`); the cabinet sheet draws the coil between the A2J2-2 (G) bus and "
			"A3J2-8 (Y-W) with a diode across it. The ROM energizes it about 2.5 s after the power-up pulse and keeps it on in attract mode and play (retained gameplay run), and drops it when the credits reach the maximum: in the retained coin-bookkeeping run it went off with the coin that brought the credits to 5, the maximum-credits setting at PinMAME's default (switches 17-19 OFF)."},
	19: {"id": "device.flipper-enable-relay", "label": "Flipper enable relay", "kind": "relay", "internal": True, "roles": ["internal.flipper-enable"], "on_board_relay": True, "vpm_library": True,
		"notes": "A continuous output through driver Q15 (PIA PB6 on J4 pin 8 [BLU-W], `FLIPPER DISABLE`) to the `FLIPPER ENABLE RELAY` on the SDU itself: Q15's collector drives coil terminal 8 "
			"on the board, and terminal 7 takes the 43 VDC supply from J3 pin 5 [Y-W] (CR20 1N4004 across the coil), so the connector pin is the relay's supply, not its drive. The SDU sheet labels "
			"that pin `TO A2J3-8`; the transformer sheet labels A2J3-9 the `FLIPPER ENABLE RE. BUS` and A2J3-8 11.9 VDC, and the interboard wiring diagram 12B-STD.-110-2 wires A2J3-9 to A3J3-5 "
			"and A2J3-8 to A3J3-12, so the SDU sheet's `A2J3-8` is a misprint for A2J3-9. Its contacts connect each flipper button (J2-2 [BLU] left, J2-1 [R] right) to its flipper coil "
			"(J1-8 [G] left, J1-9 [O] right). The ROM raises it when a game starts and drops it on a tilt and at game over (retained runs). Neither known-working script gives 19 a SolCallback, but both set `UseSolenoids=2` "
			"and load the VPinMAME libraries with `LoadVPM \"01000100\", \"Stern.VBS\", 1.2`: stern.vbs declares `Const GameOnSolenoid = 19`, and core.vbs then hands every change of this output to "
			"`vpmFlips.TiltSol`, whose `EnableFlippers` enables or disables the flippers and, with `TiltObjects` at its default of 1 (no script changes it), calls `vpmNudge.SolGameOn` with the "
			"same state. So on a tilt the table's flippers go dead and the thresholds of `vpmNudge.TiltObj` (the thumper bumper and both slingshots) rise to 100, so those three stop kicking; "
			"in the retained gameplay run the ROM fired nothing for the right slingshot while tilted, the only one of the three it exercised. The library restores the thresholds when the game is on again. The scripts' `SolCallback(16) = \"vpmNudge.SolGameOn\"` hangs on public 16, an address the MPU-200 "
			"never drives, so it never fires: a dead binding that the library makes redundant."},
	20: {"id": "device.unused-continuous-driver-q18", "label": "Unused continuous driver Q18", "kind": "relay", "unused": True,
		"notes": "A continuous-section driver (Q18, PIA PB7 on J4 pin 10 [Y-R]) that the SDU sheet wires only to pins marked `N/U` (J2 pin 15, J5 pin 3 and J3 pin 9); the self-test card lists no "
			"solenoid 18 and the parts list no load for it. In the retained runs the ROM drives it only in the power-up initialisation pulse it gives all four continuous lines (at power-up and "
			"after a slam) and in its own burn-in and solenoid tests: it stays off in attract mode, play, drain, tilt and game over. With no load fitted and that pulse explained, it is unused."},
}
for _address, _spec in SOLENOIDS.items():
	if "letter" in _spec:
		_slug, _letter, _ = METEOR_LETTERS[_spec["letter"]]
		_spec["notes"] = (f"Knocks down the METEOR {_letter} target (switch {_spec['letter']}), one of the six `Drop Target Reset (Each Target)` coils C1-34-3400 of the memory bank; the SDU sheet's "
			f"load name and the playfield coil sheet's `6-DROP TARGETS` row agree on the letter, and both known-working scripts drop target {_spec['letter']} from this address. The ROM fires it to "
			"spot the target, which a lit star rollover, return lane or the stationary target awards (manual; the retained gameplay run exercised the stand-up target and the upper and lower "
			"star rollovers, switches 4, 38 and 40), and, after a drain, to restore each player's made targets (manual: `The status of the target is restored for each player after the ball "
			"enters the outhole and the bonus is collected (memory).`; the retained single-player gameplay run fired the T, second E, O and R knock-down coils after its first drain, the four "
			"targets then down, and exercised no player change).")

FLIPPERS = {
	46: {"id": "device.right-flippers", "label": "Right flippers (lower and upper)", "wire": "O", "conn": "A3J1-9", "button_wire": "R", "button_conn": "A3J2-1", "side": "right", "power": 45,
		"objects": ("RightFlipper", "RightFlipper001"), "parts": "J-25-500/34-4500 (lower); J-25-600/34-4500 (upper)", "quantity": 2},
	48: {"id": "device.left-flipper", "label": "Left flipper", "wire": "G", "conn": "A3J1-8", "button_wire": "BLU", "button_conn": "A3J2-2", "side": "left", "power": 47,
		"objects": ("LeftFlipper",), "parts": "J-25-500/34-4500", "quantity": 1},
}

# --- Lamps -------------------------------------------------------------------------------------------------------------------
#
# Public lamp address = 16 * k + a + 1 for decoder U<k+1> output S<a>; each output line's resistor R<n> ends at SCR Q<n> (Lamp Driver schematic 12B-431S-113,
# manual PDF page 28, lettered for this game).

DECODER = {
	0: [14, 12, 13, 8, 9, 10, 11, 4, 1, 2, 3, 7, 16, 5, 6],
	1: [29, 27, 28, 35, 34, 22, 26, 25, 24, 17, 23, 21, 15, 18, 19],
	2: [36, 38, 44, 49, 48, 37, 32, 20, 42, 41, 40, 39, 33, 30, 31],
	3: [57, 50, 51, 54, 55, 60, 59, 58, 56, 46, 52, 53, 47, 43, 45],
}
LAMP_TO_Q = {16 * k + a + 1: q for k, qs in DECODER.items() for a, q in enumerate(qs)}

# The lamp driver sheet's connector blocks (manual PDF page 29): jack -> [(printed pin, SCR)] in printed order; "?" marks an illegible digit.
CONNECTOR_BLOCKS: dict[str, list[tuple[str, int]]] = {
	"J1": [("18", 14), ("19", 12), ("17", 13), ("23", 8), ("?(4)", 9), ("15", 10), ("16", 11), ("28", 4), ("24", 1), ("25", 2), ("26", 3), ("27", 7), ("1", 29), ("9", 27),
		("8", 28), ("3", 35), ("2", 34), ("10", 22), ("7", 26), ("6", 25), ("5", 24), ("11", 17), ("13", 20), ("14", 23), ("12", 21)],
	"J2": [("2", 3), ("13", 7), ("?2", 16), ("16", 5), ("1?", 6), ("? (3, 5 or 8)", 23), ("12", 21), ("?3", 15), ("20", 18), ("15", 19), ("11", 33), ("?", 30), ("2", 31), ("9", 40),
		("? (4)", 39), ("5", 52), ("10", 47), ("7", 43), ("1", 45), ("3", 53)],
	"J3": [("26", 36), ("25", 38), ("9", 44), ("17", 49), ("6", 48), ("23", 37), ("27", 32), ("21", 42), ("20", 41), ("22", 40), ("24", 39), ("?", 57), ("12", 50), ("15", 51),
		("?", 54), ("? (9)", 55), ("? (3)", 60), ("4", 59), ("2", 58), ("10", 56), ("8", 46), ("3", 52), ("14", 53)],
}

# The lamp list (manual PDF page 37, its copy on page 29 adds the handwritten Tilt row): row, description, wire, jack, pin, public address.
LAMP_LIST_TEXT = """1|BOT. LT. BANK "WOW"|R-G|J-2|7|62
2|BOT. LT. D.T. SPECIAL|BRN-B|J-1|18|1
3|GAME OVER|GREY-W|J-2|11|45
4|HIGH SCORE TO DATE|GREY-O|J-2|22|13
5|LT. OUT LANE & RT. BUMPER|B-BLU|J-2|23|29
6|LT. R/O & RETURN LANE|BRN-BLU|J-1|24|9
7|MATCH|GREY-Y|J-2|1|63
8|METEOR "DROP" E|PUR-B|J-1|25|10
9|METEOR "DROP #1E|W-O|J-3|20|42
10|METEOR "DROP" R|B-G|J-3|21|41
11|METEOR "DROP" T|B-O|J-1|11|26
12|METEOR "DROP" M|R-BLU|J-3|18|58
13|METEOR "DROP "O"|GREY-B|J-3|10|57
14|METEOR "WOW" E|W-BLUE|J-1|13|40
15|METEOR "WOW" 2E|B-W|J-1|28|8
16|METEOR "WOW" M|Y-G|J-3|2|56
17|METEOR "WOW" O|R-W|J-3|4|55
18|METEOR "WOW" R|O-W|J-3|27|39
19|METEOR "WOW" T|BRN-R|J-1|6|24
20|#1 (L) ROCKET 1K|O-R|J-3|12|50
21|#1 (L) ROCKET 2K|R-Y|J-3|25|34
22|#1 (L) ROCKET 3K|GREY|J-1|9|18
23|#1 (L) ROCKET 4K|GREY-G|J-1|19|2
24|#1 (L) ROCKET 5K|G-R|J-3|1|49
25|#1 (L) ROCKET 6K|-B-|J-3|26|33
26|#1 (L) ROCKET 7K|BLU-R|J-1|1|17
27|1X|BLU-R|J-2|14|15
28|#2 (M) ROCKET 1K|-W-|J-3|11|52
29|#2 (M) ROCKET 2K|Y-BLUE|J-3|17|36
30|#2 (M) ROCKET 3K|R-G|J-1|3|20
31|#2 (M) ROCKET 4K|BLU-W|J-1|23|4
32|#2 (M) ROCKET 5K|W-B|J-3|15|51
33|#2 (M) Rocket 6K|B-R|J-3|19|35
34|#2 (M) ROCKET 7K|G-B|J-1|8|19
35|2X|O-B|J-3|15|31
36|#3 (R) ROCKET 1K|W-BLU|J-3|3|54
37|#3 (R) ROCKET 2K|W-GREY|J-3|23|38
38|#3 (R) ROCKET 3K|GREY-BLU|J-1|10|22
39|#3 (R) ROCKET 4K|GREY-Y|J-1|15|6
40|#3 (R) ROCKET 5K|W-R|J-3|9|53
41|#3 (R) ROCKET 6K|R-B|J-3|16|37
42|#3 (R) ROCKET 7K|PUR-W|J-1|2|21
43|4X|R-BLU|J-2|2|47
44|RT. BANK SPECIAL|Y-G|J-1|7|23
45|RT. BANK "WOW"|Y-B|J-2|20|30
46|RT. OUT-LANE & LT. BUMPER|PUR-Y|J-1|4|27
47|RT. R/O & LT. RETURN LANE|BLU-O|J-1|5|25
48|M . R/O TAR. & S.U. SPOT METEOR|GREY-O|J-1|14|5
49|SHOOT AGAIN (INSERT)|GREY-R|J-2|21|11
50|SPIN #1|B-W|J-3|14|60
51|SPIN #2|GREY-W|J-3|24|44
52|SPIN #3|W-Y|J-1|12|28
53|SPIN #4|GREY-B|J-1|27|12
54|SPIN #5|B-Y|J-3|13|59
55|SPIN #6|GREY|J-3|22|43
56|S.P.S.A.|GREY-R|J-1|26|11
57|S.U. TAR. SPECIAL|-B-|J-1|16|7
58|S.U. TAR."WOW|Y-BLU|J-2|16|14
59|BOT LT. BANK "WOW"|R-G|J-3|7|62
60|TOP LT. BANK "WOW"|BLU-W|J-2|6|46
61|TOP LT. D.T.SPECIAL|-PUR-|J-1|17|3
62|Tilt|grey-blk|J-2|10|61"""
LAMP_LIST = [(int(row), text, wire, jack, pin, int(public)) for row, text, wire, jack, pin, public in (line.split("|") for line in LAMP_LIST_TEXT.splitlines())]
BACKBOX_LAMPS = {13, 45, 61, 63}

# public -> (id, label); the name a recreation author reads.
LAMP_NAMES: dict[int, tuple[str, str]] = {
	1: ("lamp.lower-left-bank-special", "Lower left bank special"), 2: ("lamp.rocket-1-4k", "Left missile 4K"), 3: ("lamp.top-left-bank-special", "Top left bank special"),
	4: ("lamp.rocket-2-4k", "Middle missile 4K"), 5: ("lamp.middle-rollover-and-stand-up-spot-meteor", "Middle rollover and stand-up target spot METEOR"), 6: ("lamp.rocket-3-4k", "Right missile 4K"),
	7: ("lamp.stand-up-target-special", "Stand-up target special"), 8: ("lamp.meteor-wow-second-e", "METEOR WOW second E"), 9: ("lamp.lower-rollover-and-right-return-lane", "Lower rollover and right return lane"),
	10: ("lamp.meteor-drop-second-e", "METEOR drop second E"), 11: ("lamp.shoot-again", "Shoot again (playfield insert and backglass)"), 12: ("lamp.spinner-4", "Spinner 4"),
	13: ("lamp.high-score-to-date", "High score to date (backbox)"), 14: ("lamp.stand-up-target-wow", "Stand-up target WOW"), 15: ("lamp.multiplier-1x", "Bonus multiplier 1X"),
	17: ("lamp.rocket-1-7k", "Left missile 7K"), 18: ("lamp.rocket-1-3k", "Left missile 3K"), 19: ("lamp.rocket-2-7k", "Middle missile 7K"), 20: ("lamp.rocket-2-3k", "Middle missile 3K"),
	21: ("lamp.rocket-3-7k", "Right missile 7K"), 22: ("lamp.rocket-3-3k", "Right missile 3K"), 23: ("lamp.right-bank-special", "Right bank special"),
	24: ("lamp.meteor-wow-t", "METEOR WOW T"), 25: ("lamp.upper-rollover-and-left-return-lane", "Upper rollover and left return lane"), 26: ("lamp.meteor-drop-t", "METEOR drop T"),
	27: ("lamp.right-outlane-and-left-bumper", "Right outlane and upper left scoring bumper"), 28: ("lamp.spinner-3", "Spinner 3"), 29: ("lamp.left-outlane-and-right-bumper", "Left outlane and upper right scoring bumper"),
	30: ("lamp.right-bank-wow", "Right bank WOW"), 31: ("lamp.multiplier-2x", "Bonus multiplier 2X"), 33: ("lamp.rocket-1-6k", "Left missile 6K"), 34: ("lamp.rocket-1-2k", "Left missile 2K"),
	35: ("lamp.rocket-2-6k", "Middle missile 6K"), 36: ("lamp.rocket-2-2k", "Middle missile 2K"), 37: ("lamp.rocket-3-6k", "Right missile 6K"), 38: ("lamp.rocket-3-2k", "Right missile 2K"),
	39: ("lamp.meteor-wow-r", "METEOR WOW R"), 40: ("lamp.meteor-wow-first-e", "METEOR WOW first E"), 41: ("lamp.meteor-drop-r", "METEOR drop R"), 42: ("lamp.meteor-drop-first-e", "METEOR drop first E"),
	43: ("lamp.spinner-6", "Spinner 6"), 44: ("lamp.spinner-2", "Spinner 2"), 45: ("lamp.game-over", "Game over (backbox)"), 46: ("lamp.top-left-bank-wow", "Top left bank WOW"),
	47: ("lamp.multiplier-4x", "Bonus multiplier 4X"), 49: ("lamp.rocket-1-5k", "Left missile 5K"), 50: ("lamp.rocket-1-1k", "Left missile 1K"), 51: ("lamp.rocket-2-5k", "Middle missile 5K"),
	52: ("lamp.rocket-2-1k", "Middle missile 1K"), 53: ("lamp.rocket-3-5k", "Right missile 5K"), 54: ("lamp.rocket-3-1k", "Right missile 1K"), 55: ("lamp.meteor-wow-o", "METEOR WOW O"),
	56: ("lamp.meteor-wow-m", "METEOR WOW M"), 57: ("lamp.meteor-drop-o", "METEOR drop O"), 58: ("lamp.meteor-drop-m", "METEOR drop M"), 59: ("lamp.spinner-5", "Spinner 5"),
	60: ("lamp.spinner-1", "Spinner 1"), 61: ("lamp.tilt", "Tilt (backbox)"), 62: ("lamp.lower-left-bank-wow", "Lower left bank WOW"), 63: ("lamp.match", "Match (backbox)"),
}
# Script lights bound to each playfield lamp (both known-working scripts and the table: NFadeLm <address>, <light>), used to settle a pairing the printed
# pins leave open; raw VPX light centres from the retained extraction.
SCRIPT_LIGHTS: dict[int, tuple[tuple[str, float, float], ...]] = {
	5: (("L5", 575.817, 914.63), ("L5a", 275.93, 251.941)), 9: (("L9", 737.622, 1273.782), ("L9a", 218.044, 317.644)), 11: (("L11", 433.821, 1467.506),),
	13: (), 25: (("L25", 129.371, 1266.439), ("L25a", 335.382, 188.941)), 27: (("L27", 811.263, 1478.441), ("L27A", 94.8, 326.324)),
	29: (("L29", 57.742, 1462.068), ("L29A", 649.386, 223.358)),
}
# Lamps whose pairing the printed pins leave open, and what settles it: public -> note.
PAIRING_NOTES: dict[int, str] = {
	5: "The connector block prints SCR Q9 on J1 pin `?(4)`, a blot over the digit before the 4, and the list's J-1 pin 14 also lands on Q23's block entry; the ROM settles the row: in the retained gameplay run "
		"the stationary target (switch 4) put this lamp out as it spotted a METEOR target, and the scripts bind it to lights at the stand-up target's insert column and the middle star rollover.",
	11: "The list prints two rows on this output: `SHOOT AGAIN (INSERT)` on J-2 pin 21 and `S.P.S.A.` (same player shoots again) on J-1 pin 26; the connector block prints Q3 on J1 pin 26 and on J2 "
		"pin 2. Both rows name the shoot-again feature, the playfield insert and the backglass; the table draws the insert `L11` and its VR backglass a shoot-again light on the same lamp.",
	13: "The connector block prints SCR Q16 on J2 pin `?2` with the first digit illegible; the list's J-2 pin 22 is the only reading, and the scripts bind no playfield light to this lamp; they show it only on the backglass.",
	44: "The list's J-3 pin 24 is the connector block's J3 entry for SCR Q39. The block also prints Q39 on J2 pin `? (4)`, a bold smudge that reads 4, a branch no lamp-list row uses; "
		"no bulb is asserted on it.",
	15: "The connector block prints SCR Q6 on J2 pin `1?`; the list's J-2 pin 14 agrees with the legible digit, and the scripts bind it to `L15`, the lowest of the three multiplier inserts.",
	27: "The list prints J-1 pin 4, which the connector block gives to no SCR legibly: it prints this output's SCR Q23 on J1 pin 14 and on J2 pin `? (3, 5 or 8)`, "
		"a single ambiguous glyph, and Q9 on J1 pin `?(4)`. The scripts bind this lamp to `L27` at the right outlane and `L27A` "
		"at the upper left scoring bumper, the row's two features.",
	28: "The connector block prints SCR Q21 on J1 pin 12 with an X drawn through the triangle column between pin 12 and Q21, a mark that may cancel that entry, and also on J2 pin 12, "
		"a branch no lamp-list row uses; no bulb is asserted on it. The structured drive connection follows the list's J-1 pin 12, the game's own row for this lamp, whatever the X means.",
	29: "The list prints J-2 pin 23; the connector block prints SCR Q15 on J2 pin `?3` with the first digit illegible. The scripts bind this lamp to `L29` at the left outlane and `L29A` at the upper "
		"right scoring bumper, the row's two features.",
	31: "The list prints `2X` on J-3 pin 15, which repeats its own `#2 (M) ROCKET 5K` row; the connector block prints SCR Q51 (lamp 51) on J3 pin 15 and SCR Q19 on J2 pin 15, and the scripts bind this lamp to `L31`, the middle "
		"multiplier insert. The list's jack is a misprint; the definition follows the connector block.",
	35: "The list prints `#2 (M) Rocket 6K` on J-3 pin 19, a pin the connector block gives to no SCR; the block prints SCR Q44, this output's, on J3 pin 9, and the scripts bind this lamp to `L35` "
		"in the middle missile column at the 6K row.",
	37: "The list prints J-3 pin 16; the connector block prints SCR Q48 on J3 pin 6. The scripts bind this lamp to `L37` in the right missile column at the 6K row.",
	46: "The list prints J-2 pin 6; the connector block prints SCR Q30 on J2 pin `?`, smudged with nothing legible. The scripts bind this lamp to `L46` in front of the top left three-bank.",
	47: "The list prints J-2 pin 2, where the connector block prints both Q3 and Q31; the scripts bind this lamp to `L47`, the highest multiplier insert.",
	49: "The list prints J-3 pin 1; the connector block prints SCR Q57 on J3 pin `?`, a blank pin cell but for a stray dot. The scripts bind this lamp to `L49` in the left missile column at the 5K row.",
	52: "The list prints J-3 pin 11; the connector block prints SCR Q54 on J3 pin `?`, a blank pin cell. The scripts bind this lamp to `L52` in the middle missile column at the 1K row.",
	53: "The list prints J-3 pin 9; the connector block prints SCR Q55 on J3 pin `? (9)`, a smudged blob that reads 9 (and Q44 on pin 9 as well). The scripts bind this lamp to `L53` in the right missile column at the 5K row.",
	54: "The list prints J-3 pin 3; the connector block prints SCR Q60 on J3 pin `? (3)`, a smudged blob that reads 3 (and Q52 on pin 3 as well). The scripts bind this lamp to `L54` in the right missile column at the 1K row.",
	58: "The list prints J-3 pin 18; the connector block prints SCR Q46 on J3 pin 8. The scripts bind this lamp to `L58`, the M of the METEOR drop inserts.",
	59: "The list prints J-3 pin 13; the connector block prints SCR Q52 on J3 pin 3 (and on J2 pin 5). The scripts bind this lamp to `L59` among the spinner inserts.",
	61: "The typed list on page 37 has no Tilt row; the page 29 copy adds a handwritten `Tilt` / `grey-blk` / `J-2` / `10` row, and the connector block prints SCR Q47 on J2 pin 10. The ROM "
		"lit this lamp when the tilt switch closed in the retained gameplay run.",
	62: "The list prints `BOT. LT. BANK \"WOW\"` on J-2 pin 7 and `BOT LT. BANK \"WOW\"` on J-3 pin 7, both R-G; the connector block prints SCR Q43 on J2 pin 7 and nothing on J3 pin 7, so "
		"the second row repeats the first with a misprinted jack. The scripts bind this lamp to `L62` in front of the lower left three-bank.",
}

# --- Option switches -------------------------------------------------------------------------------------------------------
#
# `METEOR SWITCH ASSIGNMENT` (manual PDF page 10) and the adjustment pages (PDF pages 11-15).
DIPS: dict[int, str] = {
	**{n: f"Center coin chute credits per coin, selector bit {n} (switches 1-5)" for n in range(1, 6)},
	6: "High score feature award (ON = replay, OFF = extra ball)",
	7: "Balls per game (ON = 5, OFF = 3)",
	8: "Missile WOWs: missile values that light the WOW when all three are equal (ON = 1000 thru 7000, OFF = 1000 thru 6000)",
	**{n: f"Right coin chute credits per coin, selector bit {n - 8} (switches 9-13)" for n in range(9, 14)},
	14: "Special award, selector bit 1 (chart with switches 31 and 32)",
	15: "High game to date feature, selector bit 1 (chart with switch 16)",
	16: "High game to date feature, selector bit 2",
	17: "Maximum credits, selector bit 1 (5 to 40 in steps of 5)",
	18: "Maximum credits, selector bit 2",
	19: "Maximum credits, selector bit 3",
	20: "Credit display (ON = yes, OFF = no)",
	21: "Match feature (ON = on, OFF = off)",
	22: "Replays per ball (ON = 3, OFF = 1)",
	23: "METEOR bank WOW lites at 6X (ON with switch 24 OFF)",
	24: "METEOR bank WOW lites at 7X (ON with switch 23 OFF)",
	25: "Slingshots move the WOW, special, spot, METEOR, outlane and bumper lites (ON = no movement, OFF = movement)",
	26: "Spot METEOR lamps lit per multiplier (ON = 6 for 1X-3X, 4 for 4X, 2 for 5X; OFF = 6 for 1X-2X, 4 for 3X, 2 for 4X)",
	27: "Spot METEOR lanes (ON = liberal, stay on; OFF = conservative)",
	**{n: f"Left (hinge-side) coin chute credits per coin, selector bit {n - 27} (switches 28-30)" for n in range(28, 31)},
	31: "Special award, selector bit 2",
	32: "Special award, selector bit 3",
}
DIP_NOTES: dict[int, str] = {
	8: " The switch-assignment page names it `Extra Ball On` and the adjustment page `MISSILE WOWS` (`Wow (Extra Ball) lamp comes on when all three missile values are equal`): one setting, the extra-ball WOW.",
	23: " The chart prints only switch 23 ON with 24 OFF (6X) and 23 OFF with 24 ON (7X); the other two combinations are not printed.",
	24: " The chart prints only switch 23 ON with 24 OFF (6X) and 23 OFF with 24 ON (7X); the other two combinations are not printed.",
	14: " The switch-assignment page prints it `14xx` twice, once braced with 31 and 32; the special award chart (PDF page 15) gives switch 14 as its lowest bit: all OFF no award, 14 alone 90,000 "
		"special and extra-ball WOW, up to all three ON replay special and extra-ball WOW.",
}

DISPLAYS = (
	("display.player-1-score", "Player 1 score, six digits", 0, 2, 6),
	("display.player-2-score", "Player 2 score, six digits", 1, 10, 6),
	("display.player-3-score", "Player 3 score, six digits", 2, 18, 6),
	("display.player-4-score", "Player 4 score, six digits", 3, 26, 6),
	("display.credits", "Credits, two digits", 4, 35, 2),
	("display.match-ball-in-play", "Match and ball in play, two digits", 5, 38, 2),
)
SEVEN_DIGIT_STARTS = {"display.player-1-score": 1, "display.player-2-score": 9, "display.player-3-score": 17, "display.player-4-score": 25}

# --- Retained table geometry ---------------------------------------------------------------------------------------------
#
# Raw object centres of the retained `Meteor (Stern 1979).vpx` (vpxtool git:v0.33.3 extraction), in VPX units; the curator normalizes them by the
# table's own bounds (left 0, top 0, right 952.9412, bottom 1976.4706). Walls use the mean of their drag points; the two baked-mesh dead-bumper primitives
# use the world-space bounding-box centre of their mesh in the vpxtool export of the visibility-only derivative (the curator's BUMPERS_VISIBLE_* files),
# which equals their local mesh's bounding-box centre times the size (185.274, position 0,0,0) within 0.0001. The retained-evidence tests re-read each value.

TABLE_WIDTH, TABLE_HEIGHT = 952.9412, 1976.4706

OBJECTS: dict[str, tuple[str, float, float, str]] = {
	"tsw4": ("HitTarget", 574.09564, 679.9727, "HitTarget.tsw4.json"),
	"sw5": ("Spinner", 778.1002, 547.5702, "Spinner.sw5.json"),
	"sw9": ("Wall", 750.70353, 926.7393075, "Wall.sw9.json"),
	"sw10": ("Wall", 768.8181675, 977.9306575, "Wall.sw10.json"),
	"sw11": ("Wall", 785.61753, 1026.962725, "Wall.sw11.json"),
	"bumper2": ("Primitive", 649.0404, 223.295375, "Primitive.bumper2.obj"),
	"bumper3": ("Primitive", 96.105515, 326.79741, "Primitive.bumper3.obj"),
	"bumper1": ("Bumper", 336.26477, 683.08307, "Bumper.bumper1.json"),
	"rightslingshot": ("Wall", 632.688025, 1357.82505, "Wall.rightslingshot.json"),
	"leftslingshot": ("Wall", 234.53972, 1348.75105, "Wall.leftslingshot.json"),
	"sw19": ("Wall", 146.730925, 584.6136725, "Wall.sw19.json"),
	"sw20": ("Wall", 139.60397749999998, 638.095155, "Wall.sw20.json"),
	"sw21": ("Wall", 131.8238025, 689.3398425, "Wall.sw21.json"),
	"sw22": ("Wall", 129.5142915, 914.2977875, "Wall.sw22.json"),
	"sw23": ("Wall", 111.7839065, 965.2883775, "Wall.sw23.json"),
	"sw24": ("Wall", 93.06598125, 1016.79705, "Wall.sw24.json"),
	"sw27": ("Wall", 532.535815, 231.9161375, "Wall.sw27.json"),
	"sw28": ("Wall", 488.2459225, 264.909915, "Wall.sw28.json"),
	"sw29": ("Wall", 445.9436375, 296.68367, "Wall.sw29.json"),
	"sw30": ("Wall", 401.02445, 328.56248500000004, "Wall.sw30.json"),
	"sw31": ("Wall", 354.8704175, 361.9038975, "Wall.sw31.json"),
	"sw32": ("Wall", 310.2502625, 394.61215, "Wall.sw32.json"),
	"sw34": ("Trigger", 814.3071, 1378.4664, "Trigger.sw34.json"),
	"sw35": ("Trigger", 59.41719, 1363.4543, "Trigger.sw35.json"),
	"sw36": ("Trigger", 741.61566, 1386.5431, "Trigger.sw36.json"),
	"sw37": ("Trigger", 130.5283, 1384.2605, "Trigger.sw37.json"),
	"sw38": ("Trigger", 334.62967, 190.58527, "Trigger.sw38.json"),
	"sw39": ("Trigger", 274.38525, 253.79514, "Trigger.sw39.json"),
	"sw40": ("Trigger", 216.63794, 319.19003, "Trigger.sw40.json"),
	"LeftFlipper": ("Flipper", 257.53403, 1607.5018, "Flipper.LeftFlipper.json"),
	"RightFlipper": ("Flipper", 603.1166, 1610.8662, "Flipper.RightFlipper.json"),
	"RightFlipper001": ("Flipper", 602.295, 565.0425, "Flipper.RightFlipper001.json"),
	"DRAIN": ("Kicker", 504.56784, 1880.942, "Kicker.DRAIN.json"),
	"BallRelease": ("Kicker", 831.38416, 1669.1064, "Kicker.BallRelease.json"),
}
# The seventeen connected pieces of the baked bulb mesh `layer1bulbs` (position 0,0,0, size 185.274): piece centre, and the table light within
# 3.6 VPX units of it.
GI_BULBS: tuple[tuple[float, float, str], ...] = (
	(56.424177693, 234.82599448500002, "Light002"), (427.30576353000004, 235.57913329499996, "Light017"), (342.882145224, 312.873315444, "Light019"),
	(806.9599806299999, 367.14812946300003, "Light003"), (825.9601072410001, 423.801213183, "Light004"), (64.889902575, 564.890699115, "Light005"),
	(574.4212863119999, 653.8613119290001, "Light6"), (61.332827049, 737.669820555, "Light016"), (824.8056649470001, 790.982784603, "Light009"),
	(59.207271084000006, 884.768483403, "Light015"), (823.374145386, 893.53110987, "Light008"), (58.68665114400001, 1148.4269104050002, "Light014"),
	(816.737167521, 1160.876767383, "Light001"), (187.34925407400002, 1276.612340148, "Light012"), (683.953607646, 1282.381679871, "Light013"),
	(227.648387088, 1433.167665867, "Light011"), (640.227461454, 1440.064861065, "Light010"),
)

# Matrix switch -> the table object(s) placed for it, and the note for a projection or a defective binding.
_MID_LOW = ("The retained table and both known-working scripts bind the middle and the lower target of this bank the other way round: their object `{obj}` at the bank's {where} writes this "
	"switch. The definition follows the playfield sheet's wiring and places this switch on the bank's {place} target object, but which reading is right is an open conflict (see the "
	"conflict record): the special the ROM awards on a bank's center target follows the switch number.")
SWITCH_OBJECTS: dict[int, tuple[list[str], str | None]] = {
	4: (["tsw4"], "The retained table's stand-up target handler also pulses switch 12 (`PrimStandupTgtHit 12, Tsw4, PrimT4` before `vpmTimer.PulseSw 4`), so in that table every hit on the stand-up "
		"target also scores the upper right scoring bumper; a defect of the table."),
	5: (["sw5"], None),
	9: (["sw9"], None), 10: (["sw11"], _MID_LOW.format(obj="sw10", where="middle", place="bottom")), 11: (["sw10"], _MID_LOW.format(obj="sw11", where="bottom", place="middle")),
	12: (["bumper2"], "Placed on the world-space centre of the table's collidable dead-bumper mesh `bumper2` (its `Bumper2_Hit` pulses 12), taken from the export of the visibility-only derivative that makes it visible; it coincides within 0.4 VPX units with the bumper's light `L29A`."),
	13: (["bumper3"], "Placed on the world-space centre of the table's collidable dead-bumper mesh `bumper3` (its `Bumper3_Hit` pulses 13), taken from the export of the visibility-only derivative that makes it visible; it coincides within 1.3 VPX units with the bumper's light `L27A`."),
	14: (["bumper1"], None),
	15: (["rightslingshot"], "Placed at the mean of the right slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position; the script reports the switch from the wall's own slingshot event."),
	16: (["leftslingshot"], "Placed at the mean of the left slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position; the script reports the switch from the wall's own slingshot event."),
	19: (["sw19"], None), 20: (["sw21"], _MID_LOW.format(obj="sw20", where="middle", place="bottom")), 21: (["sw20"], _MID_LOW.format(obj="sw21", where="bottom", place="middle")),
	22: (["sw22"], None), 23: (["sw24"], _MID_LOW.format(obj="sw23", where="middle", place="bottom")), 24: (["sw23"], _MID_LOW.format(obj="sw24", where="bottom", place="middle")),
	**{address: ([f"sw{address}"], None) for address in range(27, 33)},
	34: (["sw34"], None), 35: (["sw35"], None), 36: (["sw36"], None), 37: (["sw37"], None), 38: (["sw38"], None), 39: (["sw39"], None), 40: (["sw40"], None),
}
# Solenoid -> object(s) and, for a projection, why.
SOLENOID_OBJECTS: dict[int, tuple[list[str], str | None]] = {
	1: (["leftslingshot"], "Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	2: (["bumper1"], None),
	3: (["sw19", "sw20", "sw21"], "Projected onto the top left three-bank it resets: the mean of the table's own three target objects. The reset coil sits under the bank and has no object."),
	7: (["sw22", "sw23", "sw24"], "Projected onto the lower left three-bank it resets: the mean of the table's own three target objects."),
	9: (["sw9", "sw10", "sw11"], "Projected onto the right three-bank it resets: the mean of the table's own three target objects."),
	10: (["rightslingshot"], "Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	13: ([f"sw{n}" for n in range(27, 33)], "Projected onto the METEOR bank it resets: the mean of the table's own six target objects."),
	**{address: ([f"sw{spec['letter']}"], f"Placed on the METEOR target it knocks down (table `sw{spec['letter']}`); the coil sits behind the target and has no object.")
		for address, spec in SOLENOIDS.items() if "letter" in spec},
}
# Each side's end-of-stroke contacts are placed on that side's flipper pivots.
DIRECT_OBJECTS = {1: ("LeftFlipper",), 2: ("RightFlipper", "RightFlipper001")}
