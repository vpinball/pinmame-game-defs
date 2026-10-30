"""Reviewed Galaxy (Stern, 1980) device data, kept apart from the builder so both stay readable.

Every number below was read from this game's own manual (whose schematic pages are drawn for Galaxy, game #114) or observed in a retained
harness run; none is carried from a sister machine. Where a Stern MPU-200 board drawing is shared with other games, this game's own copy of
the sheet was read again.
"""

from __future__ import annotations

from typing import Any

# --- Drivers ---------------------------------------------------------------------------------------------------------

_SAME_HARDWARE = ("Identical INITGAME data to the production driver (GEN_STMPU200, six-digit dispst6 displays, FLIP_SW(FLIP_L), no extra lamp columns, "
	"Stern ST300 sound board, input_ports_st), so the controller inventory is unchanged.")
_SEVEN_DIGITS = ("INITGAME differs from the production driver only in its display layout: seven-digit dispst7 player displays (segment starts 1, 9, 17 and 25) "
	"in place of dispst6. It needs seven-digit display hardware and otherwise keeps GEN_STMPU200, FLIP_SW(FLIP_L), the ST300 sound board and the same inputs.")

# driver -> (description, year, manufacturer, parent, physical_compatibility, notes)
DRIVERS: dict[str, tuple[str, str, str, str | None, str, str]] = {
	"galaxy": (
		"Galaxy", "1980", "Stern", None, "identical",
		"Production ROM set (U1, U2, U5 and U6) and the reference for this definition: GEN_STMPU200, six-digit dispst6 displays, FLIP_SW(FLIP_L), Stern ST300 sound board. "
		"Every retained harness run except the clone solenoid test boots this driver.",
	),
	"galaxyfp": (
		"Galaxy (Free Play)", "1980", "Stern", "galaxy", "identical",
		"Free-play build of the production ROM: the same U1 and U5 images with changed U2 and U6. " + _SAME_HARDWARE + " No harness run was made with it.",
	),
	"galaxyps": (
		"Galaxy (Planet Skillshot)", "2011", "Stern / Scott", "galaxy", "identical",
		"Community rules change that replaces U6 only. " + _SAME_HARDWARE + " The ROM was not available for a harness run.",
	),
	"galaxyb": (
		"Galaxy (7-digit conversion)", "2003", "Stern / Oliver", "galaxy", "compatible",
		"Community seven-digit conversion, rev. 2. " + _SEVEN_DIGITS + " Its retained solenoid test fires the same nineteen outputs in the same order as the production ROM's.",
	),
	"galaxyc": (
		"Galaxy (7-Digit conversion, Fixes & modified rules)", "2023", "Stern / Idleman", "galaxy", "compatible",
		"Community seven-digit conversion with fixes and modified rules. " + _SEVEN_DIGITS + " The ROM was not available for a harness run.",
	),
}
SEVEN_DIGIT_DRIVERS = ("galaxyb", "galaxyc")
SEVEN_DIGIT_STARTS = {"display.player-1-score": 1, "display.player-2-score": 9, "display.player-3-score": 17, "display.player-4-score": 25}

# --- Cabinet and service inputs ---------------------------------------------------------------------------------------

SERVICE_SWITCHES: dict[int, dict[str, Any]] = {
	-7: {
		"id": "switch.self-test-button", "label": "Self Test button (coin door)", "roles": ["service.test"], "availability": "used",
		"location": "Inside the coin door",
		"notes": "The Self-Test button inside the coin door (manual Figure 1), drawn on the cabinet sheet as `TEST SWITCH` from A4J3-1 (R) to A3J2-7 (Y-R). Public -7 drives the ROM's tests in the "
			"manual's order: in the retained runs the first press starts the burn-in, the fourth the solenoid test and the fifth the switch test.",
		"evidence": "manual-and-harness",
	},
	-6: {
		"id": "switch.cpu-diagnostic-button", "label": "CPU diagnostic input (MPU NMI)", "roles": ["service.diagnostic"], "availability": "optional",
		"location": "MPU module",
		"notes": "PinMAME routes public -6 to the CPU's NMI line (BY35_SWCPUDIAG). The manual names no button for it; the S33 MEMORY CLEAR pushbutton is a separate contact "
			"(the remote memory-clear input), so the identity of the two is not assumed.",
		"evidence": "core",
	},
	-5: {
		"id": "switch.sound-diagnostic-button", "label": "Sound board diagnostic input", "roles": ["service.diagnostic"], "availability": "optional",
		"location": "Sound module",
		"notes": "PinMAME routes public -5 to the ST300 sound board's diagnostic input (BY35_SWSOUNDDIAG). The manual documents no such button on the C-605 sound module.",
		"evidence": "core",
	},
}

# --- Matrix switches ----------------------------------------------------------------------------------------------------
#
# Public address = strobe * 8 + return + 1 on the five-strobe by eight-return MPU matrix. The playfield wiring diagram (manual page 23) draws
# the whole matrix on A4J2; the cabinet sheet (page 24) redraws it on A4J3 and wires the coin, credit, tilt and slam contacts there.

STROBES = {
	0: ("W-R", "A4J2-1"), 1: ("BRN-W", "A4J2-2"), 2: ("W-BLU", "A4J2-3"), 3: ("W-Y", "A4J2-4"), 4: ("Y-R", "A4J2-5"),
}
RETURNS = {
	0: ("BRN", "A4J2-8"), 1: ("GREY", "A4J2-9"), 2: ("W-O", "A4J2-10"), 3: ("W-B", "A4J2-11"),
	4: ("W-G", "A4J2-12"), 5: ("W-BRN", "A4J2-13"), 6: ("BRN-Y", "A4J2-14"), 7: ("O", "A4J2-15"),
}
CABINET_RETURNS = {0: ("R-W", "A4J3-9"), 1: ("BRN-W", "A4J3-10"), 2: ("BLU", "A4J3-11"), 5: ("BLU-W", "A4J3-14"), 6: ("BLU-O", "A4J3-15"), 7: ("Y", "A4J3-16")}
CABINET_STROBE0 = ("R-Y", "A4J3-2")
# The cabinet sheet draws the CHUTE contacts on returns I1 and I2 without a series diode (the playfield sheet draws a diode on all three).
NO_DIODE_SWITCHES = {2, 3}

# address -> spec. ``printed`` is the Switch Identification table's text (manual page 16), ``matrix`` the playfield sheet's cell.
SWITCHES: dict[int, dict[str, Any]] = {
	1: {"id": "switch.coin-chute-1", "label": "Coin chute 1", "type": "other", "cabinet": True, "roles": ["cabinet.coin.1"],
		"printed": "CHUTE", "matrix": "CHUTE #1",
		"notes": "SW1 of the coin-door drawing on the Switch Identification page; the location page lists `1 *CENTER CHUTE`. Cabinet sheet return A4J3-9 (R-W). A coin on it adds one credit in the retained gameplay run."},
	2: {"id": "switch.coin-chute-2", "label": "Coin chute 2", "type": "other", "cabinet": True, "roles": ["cabinet.coin.2"],
		"printed": "CHUTE", "matrix": "CHUTE #2",
		"notes": "SW2 of the coin-door drawing; the location page lists `2 *LEFT CHUTE`. Cabinet sheet return A4J3-10 (BRN-W). A coin on it adds one credit in the retained gameplay run."},
	3: {"id": "switch.coin-chute-3", "label": "Coin chute 3", "type": "other", "cabinet": True, "roles": ["cabinet.coin.3"],
		"printed": "CHUTE", "matrix": "CHUTE #3",
		"notes": "SW3 of the coin-door drawing; the location page lists `3 *RIGHT CHUTE`. Cabinet sheet return A4J3-11 (BLU). A coin on it adds one credit in the retained gameplay run."},
	4: {"id": "switch.drop-target-red", "label": "Drop target 4 (red, lowest)", "type": "leaf", "drop": True,
		"printed": "DROP TARGET (RED)", "matrix": "D.T. (RED)",
		"notes": "Lowest target of the left 4-bank (D-548-4A; location drawing leader 4). Closed while the target is down. Its own knock-down coil is public 9, which the ROM fires to spot it."},
	5: {"id": "switch.spinner", "label": "Spinning target", "type": "other", "pulse": True,
		"printed": "SPIN TARGET", "matrix": "SP. T.",
		"notes": "Spin target assembly A-563-10 across the opening below the eject pocket (location drawing leader 5). Each rotation closes the contact once. The manual: it scores 100 (1,000 when lit) and "
			"changes the eject pocket's value; it scored 1,000 in the retained gameplay run."},
	6: {"id": "switch.credit-button", "label": "Credit button", "type": "button", "cabinet": True, "roles": ["cabinet.start"],
		"printed": "CREDIT BUTTON", "matrix": "CREDIT",
		"notes": "Coin-door credit (start) button, cabinet sheet return A4J3-14 (BLU-W). In the retained gameplay run it starts a game from credits and decrements the credit display."},
	7: {"id": "switch.tilt", "label": "Tilt (roll tilt and pendulum)", "type": "tilt", "cabinet": True, "quantity": 2, "roles": ["cabinet.tilt"],
		"printed": "TILTS", "matrix": "TILTS",
		"notes": "Shared matrix position for two normally open tilt contacts: the location page lists `7 ROLL-TILT` and `7 PENDULUM`, and the cabinet sheet draws two contacts in parallel on return A4J3-15 (BLU-O) "
			"with a capacitor drawn in the row. Closing public 7 in play drops the flipper-enable output 19 and lights TILT (lamp 61) in the retained gameplay run."},
	8: {"id": "switch.slam", "label": "Slam (door, tilt board and playfield)", "type": "tilt", "cabinet": True, "roles": ["cabinet.slam-tilt"],
		"printed": "SLAM & VIB. TILTS", "matrix": "SLAM",
		"notes": "Shared matrix position for the slam contacts. The location page lists `8 TILT BOARD` and `8 DOOR & PLAYFIELD VIB.`; the operating text says there is a slam switch on the front door, one on the tilt board and one on the playfield, and that an operator may fit more. "
			"The cabinet sheet draws one SLAM contact on return A4J3-16 (Y). Because operators may add contacts, no quantity is asserted. In the retained slam run, closing public 8 in play ends the game."},
	9: {"id": "switch.drop-target-black", "label": "Drop target 1 (black, highest)", "type": "leaf", "drop": True,
		"printed": "DROP TARGET (GREEN)", "matrix": "D.T. BLACK",
		"notes": "Highest target of the left 4-bank (location drawing leader 9). The Switch Identification table calls it GREEN, the matrix sheet and the feature text (`Upper right drop target (black)`) BLACK; one target, two colour names. "
			"Closed while down. Its knock-down coil is public 14, which the ROM fires when the upper stand-up target (switch 30) closes."},
	10: {"id": "switch.drop-target-yellow", "label": "Drop target 2 (yellow)", "type": "leaf", "drop": True,
		"printed": "DROP TARGET (YELLOW)", "matrix": "D.T. YEL.",
		"notes": "Second target of the left 4-bank from the top (location drawing leader 10). Closed while down. Its knock-down coil is public 13, which the ROM fires when the middle stand-up target (switch 29) closes."},
	11: {"id": "switch.drop-target-blue", "label": "Drop target 3 (blue)", "type": "leaf", "drop": True,
		"printed": "DROP TARGET (BLUE)", "matrix": "D.T. BLU",
		"notes": "Third target of the left 4-bank from the top (location drawing leader 11). Closed while down. Its knock-down coil is public 10, which the ROM fires when the lower stand-up target (switch 26) closes."},
	12: {"id": "switch.top-thumper-bumper", "label": "Top thumper bumper", "type": "leaf", "pulse": True,
		"printed": "TOP THUMPER", "matrix": "TOP THUMP.",
		"notes": "Closing it in play scores 1,000 (3-ball setting) and fires public output 3 in the retained gameplay run; the manual says it also advances the eject pocket value."},
	13: {"id": "switch.lower-right-thumper-bumper", "label": "Lower right thumper bumper", "type": "leaf", "pulse": True,
		"printed": "LOWER RIGHT THUMPER", "matrix": "LOW. R. THUMP.",
		"notes": "Closing it scores 1,000 and fires public output 7 in the retained gameplay run."},
	14: {"id": "switch.lower-left-thumper-bumper", "label": "Lower left thumper bumper", "type": "leaf", "pulse": True,
		"printed": "LOWER LEFT THUMPER", "matrix": "LOW. L. THUMP.",
		"notes": "Closing it scores 1,000 and fires public output 12 in the retained gameplay run."},
	15: {"id": "switch.right-slingshot", "label": "Right slingshot", "type": "leaf", "pulse": True,
		"printed": "RIGHT SLING-SHOT", "matrix": "R. SLING SHOT",
		"notes": "The long slingshot on the right side of the playfield, below the stand-up targets (location drawing: two leaders numbered 15 end on its rubber). Closing it scores 10 and fires public output 1 in the retained gameplay run."},
	16: {"id": "switch.left-slingshot", "label": "Left slingshot", "type": "leaf", "pulse": True,
		"printed": "LEFT SLING-SHOT", "matrix": "L. SLING SHOT",
		"notes": "The long slingshot on the left side, below the drop-target bank (two leaders numbered 16). Closing it scores 10 and fires public output 2 in the retained gameplay run."},
	18: {"id": "switch.center-roll-over-buttons", "label": "Center star roll-over buttons (two)", "type": "button", "quantity": 2,
		"printed": "CENTER ROLL-OVER BUTTONS (2)", "matrix": "CENTER R.O.B(2)",
		"notes": "Two star roll-over buttons on one address: the table and the matrix sheet print `(2)` and the location drawing has two leaders numbered 18, one left of centre below the thumpers and one "
			"at the centre between the lower lanes. The manual: the star roll-overs score 10 and advance the bonus; the retained gameplay run scored 10 and lit BONUS 4 (lamp 40) after BONUS 2."},
	19: {"id": "switch.right-return-lane", "label": "Right inner return lane (Y)", "type": "leaf",
		"printed": "RIGHT RETURN LANE", "matrix": "R. RETURN LANE",
		"notes": "Right inner return lane, the inner of the two right inlanes (location drawing leader 19). The manual: scores 500, advances the bonus and spots both the letter Y and the red drop target; "
			"in the retained gameplay run it scored 500, lit the Y roll-over and Y kicker lamps (35 and 33) and fired public 9, the red target's knock-down coil."},
	20: {"id": "switch.right-middle-lane", "label": "Right outer return lane (right middle lane)", "type": "leaf",
		"printed": "RIGHT MIDDLE LANE", "matrix": "R. MID. LANE",
		"notes": "Right outer return lane, between the right outlane and the right inner return lane (location drawing leader 20); the feature text calls the pair the outer return lanes. "
			"The manual: scores 2,000, advances the bonus and, when lit, spots the next drop target; it scored 2,000 and fired public 9 in the retained gameplay run with its SPOT lamp (27) lit."},
	21: {"id": "switch.left-return-lane", "label": "Left inner return lane (X)", "type": "leaf",
		"printed": "LEFT RETURN LANE", "matrix": "L. RETURN LANE",
		"notes": "Left inner return lane (location drawing leader 21). The manual: scores 500, advances the bonus and spots both the letter X and the red drop target; in the retained gameplay run it fired public 9 "
			"and lit the X roll-over and X kicker lamps (51 and 49)."},
	22: {"id": "switch.left-middle-lane", "label": "Left outer return lane (left middle lane)", "type": "leaf",
		"printed": "LEFT MIDDLE LANE", "matrix": "L. MID. LANE",
		"notes": "Left outer return lane, between the left outlane and the left inner return lane (location drawing leader 22). Scores 2,000, advances the bonus and, when lit, spots the next drop target; "
			"it scored 2,000 and fired public 9 in the retained gameplay run."},
	23: {"id": "switch.right-outlane", "label": "Right outlane (star roll-over)", "type": "button",
		"printed": "RIGHT OUT-LANE (R.O.B.)", "matrix": "R. OUT-LANE R.O.B.",
		"notes": "Star roll-over button in the right outlane (location drawing leader 23). The manual: scores 5,000 (10,000 when X is spotted) and spots the letter Y; it scored 5,000 in the retained gameplay run."},
	24: {"id": "switch.left-outlane", "label": "Left outlane (star roll-over)", "type": "button",
		"printed": "LEFT OUT-LANE (R.O.B.)", "matrix": "L. OUT-LANE R.O.B.",
		"notes": "Star roll-over button in the left outlane (location drawing leader 24). The manual: scores 5,000 (10,000 when G is spotted) and spots the letter X; it scored 5,000 in the retained gameplay run."},
	26: {"id": "switch.standup-target-lower", "label": "Lower stand-up target (blue star)", "type": "leaf", "pulse": True,
		"printed": "STAND-UP TARGET (BLUE STAR)", "matrix": "S.U.T. BLUE",
		"notes": "Lowest of the three stand-up targets on the right side (location drawing leader 26; Target Ass'y A-469-Y-BL-B). Scores 500 and spots the blue drop target: the ROM fired public 10 in the retained gameplay run."},
	29: {"id": "switch.standup-target-middle", "label": "Middle stand-up target (yellow star)", "type": "leaf", "pulse": True,
		"printed": "STAND-UP TARGET (YELLOW STAR)", "matrix": "S.U.T. YELLOW",
		"notes": "Middle stand-up target on the right side (location drawing leader 29). Scores 500 and spots the yellow drop target: the ROM fired public 13 in the retained gameplay run."},
	30: {"id": "switch.standup-target-upper", "label": "Upper stand-up target (black star)", "type": "leaf", "pulse": True,
		"printed": "STAND-UP TARGET (GREEN STAR)", "matrix": "S.U.T. BLACK",
		"notes": "Upper stand-up target on the right side (location drawing leader 30). The Switch Identification table calls its star GREEN, the matrix sheet BLACK. Scores 500 and spots the black drop target: "
			"the ROM fired public 14 in the retained gameplay run."},
	33: {"id": "switch.outhole", "label": "Out-hole", "type": "leaf", "initial_active": True,
		"printed": "OPEN", "matrix": "OUT-HOLE",
		"notes": "Single-ball out-hole below the flippers. The Switch Identification table prints 33 as OPEN, but the matrix sheet draws `OUT-HOLE` in that cell, the location drawing points leader 33 at the out-hole, "
			"and the ROM kicks the out-hole (public 11) while it is closed (retained gameplay run); the known-working script starts the game with the ball on it."},
	35: {"id": "switch.kicker-lane", "label": "Kicker lane (kickback) switch", "type": "leaf",
		"printed": "BALL KICKER", "matrix": "BALL KICK.",
		"notes": "Roll-over in the upper-left kicker lane (location drawing leader 35). When it closes the ROM scores the lane and then pulses public 5, the ball kicker, which drives the ball back up the lane "
			"(retained gameplay run: about four seconds after the closure). The manual: the lane scores 3,000 plus 2,000 for each letter of G-A-L-A-X-Y spotted."},
	36: {"id": "switch.top-lane-left", "label": "Top left roll-over lane (G)", "type": "leaf",
		"printed": "TOP LEFT ROLL-OVER WIRE", "matrix": "TOP-L. R.O.W.",
		"notes": "Left of the three top lanes, lettered G. Scores 500 (5,000 when the X and Y return lanes are made) and spots G in the kicker lane; in the retained gameplay run it scored 5,000 and lit the G roll-over and G kicker lamps (52 and 50)."},
	37: {"id": "switch.top-lane-middle", "label": "Top middle roll-over lane (A)", "type": "leaf",
		"printed": "TOP MIDDLE ROLL-OVER WIRE", "matrix": "TOP MID. R.O.W.",
		"notes": "Middle top lane, lettered A. Scored 5,000 and lit the A roll-over and A kicker lamps (36 and 34) in the retained gameplay run."},
	38: {"id": "switch.top-lane-right", "label": "Top right roll-over lane (L)", "type": "leaf",
		"printed": "TOP RIGHT ROLL-OVER WIRE", "matrix": "TOP R. R.O.W.",
		"notes": "Right top lane, lettered L. Scored 5,000 and lit the L roll-over and L kicker lamps (20 and 18) in the retained gameplay run."},
	39: {"id": "switch.top-right-roll-over-button", "label": "Top right star roll-over (second A)", "type": "button",
		"printed": "TOP RIGHT ROLL-OVER BUTTON", "matrix": "TOP-R. R.O.W.",
		"notes": "Star roll-over button right of the top lanes at the top of the shooter-lane return (location drawing leader 39 ends on a star). The Switch Identification table calls it a roll-over button, "
			"the matrix sheet repeats `TOP-R. R.O.W.` in its cell; the location drawing and the table model a star button, which is what the definition records. In the retained gameplay run, closed after the three top lanes, it lit the second A "
			"in the kicker lane (lamp 2, `\"A\"2 KICKER`), cleared the roll-over letter lamps and flickered the general-illumination relay (public 17)."},
	40: {"id": "switch.saucer", "label": "Top eject pocket (saucer)", "type": "leaf",
		"printed": "SAUCER", "matrix": "SAUCER",
		"notes": "Switch under the top eject pocket (location drawing leader 40). Held closed while a ball sits in it; the ROM scores the pocket and pulses public 8, the saucer eject, about three seconds after the closure (retained gameplay run). "
			"The pocket scores its lit value, advanced by the top thumper and the spinner and reset to 2,000 at each drain (manual)."},
}
OPEN_SWITCHES = (17, 25, 27, 28, 31, 32, 34)

# Flipper buttons: PinMAME synthetic switches 81-84 (FLIP_SW(FLIP_L)): right 82, left 84; 81/83 are the generic upper positions.
FLIPPER_BUTTONS = {
	82: ("switch.right-flipper-button", "Right flipper button", "flipper.button.right", "R", "A3J2-1"),
	84: ("switch.left-flipper-button", "Left flipper button", "flipper.button.left", "BLU", "A3J2-2"),
}
UNUSED_FLIPPER_POSITIONS = {
	81: ("switch.upper-right-flipper-position", "Upper right flipper button position (no upper flipper)"),
	83: ("switch.upper-left-flipper-position", "Upper left flipper button position (no upper flipper)"),
}

# --- Solenoids ----------------------------------------------------------------------------------------------------------
#
# The ROM's own solenoid test pulses physical drivers 1-19 in order and shows each number on the player displays; the public addresses that
# fire are, in that order: 2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18 (retained solenoid-test run).

SELF_TEST_ORDER = (2, 1, 6, 7, 3, 4, 5, 8, 11, 12, 14, 13, 9, 10, 19, 15, 17, 20, 18)
PHYSICAL_TO_PUBLIC = {number: address for number, address in enumerate(SELF_TEST_ORDER, start=1)}

# Solenoid Identification table (manual page 18), by printed number; 11-14 are printed as one row.
PRINTED_SOLENOIDS = {
	1: "LEFT SLING-SHOT", 2: "RIGHT SLING-SHOT", 3: "KNOCKER", 4: "LOWER RIGHT THUMPER", 5: "TOP THUMPER", 6: "DROP TARGET RESET", 7: "BALL KICKER",
	8: "SAUCER EJECT.", 9: "OUT-HOLE", 10: "LOWER LEFT THUMPER", 11: "4-BANK DROP TARGET", 12: "4-BANK DROP TARGET", 13: "4-BANK DROP TARGET", 14: "4-BANK DROP TARGET",
	15: "RIGHT & LEFT FLIPPERS", 16: "OPEN", 17: "OPEN", 18: "OPEN", 19: "COIN LOCK-OUT",
}

SOLENOIDS: dict[int, dict[str, Any]] = {
	1: {"id": "device.right-slingshot", "label": "Right slingshot", "kind": "coil", "part": "J-27-1700", "wire": "BRN", "conn": "A3J2-4",
		"notes": "Fired by the ROM when the right slingshot switch (public 15) closes. The Solenoid Driver Schematic prints `RIGHT SLING-SHOT (-BRN-)` on J2 pin 4 and the playfield sheet `A3J2-4 (BROWN)`."},
	2: {"id": "device.left-slingshot", "label": "Left slingshot", "kind": "coil", "part": "J-27-1700", "wire": "PUR-W", "conn": "A3J2-9",
		"notes": "Fired by the ROM when the left slingshot switch (public 16) closes."},
	3: {"id": "device.top-thumper-bumper", "label": "Top thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "G-R", "conn": "A3J2-10",
		"notes": "Fired by the ROM when the top thumper switch (public 12) closes."},
	4: {"id": "device.drop-target-bank-reset", "label": "4-bank drop-target reset", "kind": "coil", "part": "B-27-2300", "wire": "GREY", "conn": "A3J2-11",
		"notes": "Raises all four targets of the left bank (parts list `Drop Target Reset (1)` B-27-2300; playfield sheet `4-BANK DROP TARG. (RESET)`). Fired at game start, after every drain and when the fourth target "
			"of the bank goes down (retained gameplay run: eight complete cycles each end with a pulse on 4)."},
	5: {"id": "device.ball-kicker", "label": "Kicker lane ball kicker (kickback)", "kind": "coil", "part": "J-28-2300", "wire": "Y-R", "conn": "A3J2-12",
		"notes": "Parts list `Kicker` J-28-2300. Pulsed by the ROM about four seconds after the kicker-lane switch (public 35) closes, driving the ball back up the upper-left lane (retained gameplay run)."},
	6: {"id": "device.knocker", "label": "Knocker", "kind": "coil", "part": "N-26-1200", "wire": "B-Y", "conn": "A3J2-5", "cabinet": True, "roles": ["cabinet.knocker"],
		"notes": "The solenoid location page lists `3-KNOCKER` among the solenoids not on the playfield; the cabinet sheet draws it on `A3J2-5 (B-Y)` beside the coin lockout. "
			"Award events were not exercised, because PinMAME's default option switches leave the awards off."},
	7: {"id": "device.lower-right-thumper-bumper", "label": "Lower right thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "BRN-Y", "conn": "A3J1-5",
		"notes": "Fired by the ROM when the lower right thumper switch (public 13) closes. The Solenoid Driver Schematic brings it out on J1 pin 5 `LOWER R. THUMPER (BRN-Y)`, the only coil on J1."},
	8: {"id": "device.saucer-eject", "label": "Saucer eject", "kind": "coil", "part": "J-28-2300", "wire": "B-Y", "conn": "A3J5-10",
		"notes": "Parts list `Saucer Eject` J-28-2300. The ROM pulses it about three seconds after the saucer switch (public 40) closes (retained gameplay run)."},
	9: {"id": "device.drop-target-red-knock-down", "label": "Red drop target knock-down coil", "kind": "coil", "part": "C1-34-3400", "wire": "O-B", "conn": "A3J5-12",
		"notes": "One of the four per-target coils (parts list `Drop Target Reset (Each Target) 4` C1-34-3400) that knock a target down to spot it: the Solenoid Driver Schematic wires Q13 to J5 pin 12 `DR. TARG. RED (O-B)`. "
			"The ROM fires it when the return lanes spot the red target (retained gameplay run: switches 19, 20, 21 and 22 each fire 9); the known-working script drops target 4 on it."},
	10: {"id": "device.drop-target-blue-knock-down", "label": "Blue drop target knock-down coil", "kind": "coil", "part": "C1-34-3400", "wire": "B", "conn": "A3J5-11",
		"notes": "Q14 to J5 pin 11 `DR. TARG. BLUE (-B-)`. Fired when the lower stand-up target (switch 26) closes in the retained gameplay run; the script drops target 11 on it."},
	11: {"id": "device.out-hole-kicker", "label": "Out-hole kicker", "kind": "coil", "part": "J-26-1000", "wire": "O-R", "conn": "A3J5-9",
		"notes": "Parts list `Outhole Kicker (1)` J-26-1000. Fired when a game starts and after every drain; the ROM repeats the kick while the out-hole switch (public 33) stays closed."},
	12: {"id": "device.lower-left-thumper-bumper", "label": "Lower left thumper bumper", "kind": "coil", "part": "J-26-1200", "wire": "B-BLU", "conn": "A3J5-15",
		"notes": "Fired by the ROM when the lower left thumper switch (public 14) closes."},
	13: {"id": "device.drop-target-yellow-knock-down", "label": "Yellow drop target knock-down coil", "kind": "coil", "part": "C1-34-3400", "wire": "O-W", "conn": "A3J5-13",
		"notes": "Q12 to J5 pin 13 `DR. TARG. YEL. (O-W)` on this game's Solenoid Driver Schematic. Fired when the middle stand-up target (switch 29) closes in the retained gameplay run; the script drops target 10 on it."},
	14: {"id": "device.drop-target-black-knock-down", "label": "Black drop target knock-down coil", "kind": "coil", "part": "C1-34-3400", "wire": "Y-BLU", "conn": "A3J5-14",
		"notes": "Q11 to J5 pin 14 `DR. TARG. BLACK (Y-BLUE)`. Fired when the upper stand-up target (switch 30) closes in the retained gameplay run; the script drops target 9 on it."},
	15: {"id": "device.unused-solenoid-16", "label": "Unused solenoid driver 16", "kind": "coil", "phys": 16, "unused": True,
		"notes": "Printed OPEN in the Solenoid Identification table, and the Solenoid Driver Schematic wires Q16 to J5 pin 8 `OPEN`. The ROM drives it only in its own solenoid test and burn-in. "
			"The known-working script binds it to `BRelease`, a Sub the script never defines; because the ROM never fires 15 in play, that table defect never shows."},
	17: {"id": "device.general-illumination-relay", "label": "General illumination relay", "kind": "relay", "wire": "W-BLU", "conn": "A3J5-7", "cabinet": True,
		"notes": "Printed OPEN in the Solenoid Identification table, but this game's Solenoid Driver Schematic wires Q17 (input PB4 on J4 pin 11, [Y-W]) to J5 pin 7 `GEN. ILLUM. RELAY` [W-BLU], and the cabinet sheet "
			"draws the relay coil `GEN. ILLUM. RELAY` between the coin lock-out and knocker bus A2J2-2 (G) and `A3J5-7 (W-BLU)` beside the coin lockout and the knocker. IPDB notes that Galaxy has computer-controlled general "
			"illumination. In the retained runs the ROM flickers it in pulses of about 0.1 s for some two seconds when a game starts, when the top-right star "
			"completes G-A-L-A, and at game over, plus once in the power-up pulse it gives all four continuous lines; it stays off through 90 s of attract mode. "
			"No sheet draws the relay's contacts; the known-working script turns the playfield general illumination off while this output is on (Sub PFGI)."},
	18: {"id": "device.coin-lockout", "label": "Coin lock-out coil", "kind": "coil", "part": "C-36-5300", "wire": "Y-W", "conn": "A3J2-8", "cabinet": True, "roles": ["cabinet.coin-door"],
		"notes": "Printed solenoid 19 (COIN LOCK-OUT), a continuous output: the ROM energizes it from the end of the power-up test in the retained runs. The cabinet sheet prints `A3J2-8 (Y-W)` and the Solenoid Driver Schematic "
			"`COIN LOCK-OUT [Y-W]` on J2 pin 8."},
	19: {"id": "device.flipper-enable-relay", "label": "Flipper enable relay", "kind": "relay", "wire": "Y-W", "conn": "A3J3-5", "internal": True, "roles": ["internal.flipper-enable"],
		"notes": "Printed solenoid 15 (RIGHT & LEFT FLIPPERS), a continuous output through driver Q15 (input PB6, `FLIPPER DISABLE` [BLU-W]) and the `FLIPPER ENABLE RELAY` (CR20, 43 VDC, J3 pin 5 `To A2J3-8 [Y-W]`). "
			"The ROM raises it when a game starts and drops it when a tilt closes switch 7 (retained gameplay run)."},
	20: {"id": "device.unused-continuous-driver-18", "label": "Unused continuous driver 18", "kind": "relay", "phys": 18, "unused": True,
		"notes": "Printed OPEN in the Solenoid Identification table, and the Solenoid Driver Schematic wires its transistor (Q18, input PB7 on J4 pin 10, [Y-R]) only to pins marked N/U (J5 pin 3, J2 pin 15 and J3 pin 9). "
			"The ROM drives it only in the power-up initialisation pulse it gives all four continuous lines (repeated after a slam) and in its own burn-in and solenoid tests; it stays off through 90 s of "
			"attract mode, play, drain, tilt and game over in the retained runs."},
}

FLIPPERS = {
	46: {"id": "device.right-flipper", "label": "Right flipper", "wire": "O", "conn": "A3J1-9", "button_wire": "R", "button_conn": "A3J2-1", "side": "right", "power": 45, "object": "RightFlipper"},
	48: {"id": "device.left-flipper", "label": "Left flipper", "wire": "G", "conn": "A3J1-8", "button_wire": "BLU", "button_conn": "A3J2-2", "side": "left", "power": 47, "object": "LeftFlipper"},
}

# --- Lamps -------------------------------------------------------------------------------------------------------------------
#
# Public lamp address = 16 * k + a + 1 for decoder U<k+1> output S<a>; each output line's resistor R<n> ends at SCR Q<n>. Both tables below are this
# game's Lamp Driver Schematic (12B-431-S-114, GALAXY, 10-11-79, manual page 31).

DECODER = {
	0: [14, 12, 13, 8, 9, 10, 11, 4, 1, 2, 3, 7, 16, 5, 6],
	1: [29, 27, 28, 35, 34, 22, 26, 25, 24, 17, 23, 21, 15, 18, 19],
	2: [36, 38, 44, 49, 48, 37, 32, 20, 42, 41, 40, 39, 33, 30, 31],
	3: [57, 50, 51, 54, 55, 60, 59, 58, 56, 46, 52, 53, 47, 43, 45],
}
LAMP_TO_Q = {16 * k + a + 1: q for k, qs in DECODER.items() for a, q in enumerate(qs)}

# jack -> {pin: SCR}. The J1 rows that carry Q24 and Q23 print pin numbers that collide with other J1 rows (see the excerpt). Q24's flat-topped
# figure is read as pin 5, where the lamp list prints its one load ("L" EXTRA BALL); Q23's J1 pin is left out, because no lamp-list row uses it.
LDA_CONNECTORS = {
	"J1": {18: 14, 19: 12, 17: 13, 23: 8, 14: 9, 15: 10, 16: 11, 28: 4, 24: 1, 25: 2, 26: 3, 27: 7, 1: 29, 9: 27, 8: 28, 3: 35, 2: 34, 10: 22,
		7: 26, 6: 25, 5: 24, 11: 17, 13: 20, 12: 21},
	"J2": {21: 3, 13: 7, 22: 16, 16: 5, 14: 6, 8: 23, 12: 21, 23: 15, 20: 18, 15: 19, 11: 33, 6: 30, 2: 31, 9: 40, 4: 39, 5: 52, 10: 47, 7: 43, 1: 45, 3: 53},
	"J3": {26: 36, 25: 38, 19: 44, 17: 49, 16: 48, 23: 37, 27: 32, 21: 42, 20: 41, 22: 40, 24: 39, 1: 57, 12: 50, 15: 51, 11: 54, 9: 55, 3: 60, 4: 59,
		2: 58, 10: 56, 18: 46, 13: 52, 14: 53},
}

# The typed lamp list, in printed order: description | wire | jack | pin. The playfield wiring diagram (page 22) and the Lamp Driver Schematic
# (page 31) print the same 54 rows; SAME PLAYER SHOOTS AGAIN is one description braced over two jack rows.
LAMP_LIST_TEXT = """"A" ROLL-OVER|Y-BLU|J3|17
"A" ROLL-OVER (2)|BLU-W|J1|23
"G" ROLL-OVER|W|J3|11
BONUS 2|Y-G|J3|2
BONUS 4|W-BLU|J1|13
BONUS 6|BRN-R|J1|6
BONUS 8|B-W|J1|28
BONUS 10|R-W|J3|4
BONUS 20|O-W|J3|27
BONUS 30|Y-G|J1|7
BONUS 40|B|J1|16
GAME OVER|GREY-W|J2|11
HIGH SCORE TO DATE|GREY-O|J2|22
JUPITOR|GREY-Y|J1|15
"A" KICKER|R-Y|J3|25
"A"2 KICKER|GREY-G|J1|19
"G" KICKER|O-R|J3|12
"L" EXTRA BALL|BLU-O|J1|5
"L" KICKER|GREY-|J1|9
"L" ROLL-OVER|R-G|J1|3
L. SPECIAL|GREY-B|J3|10
"X" KICKER|G-R|J3|1
"Y" KICKER|B|J3|26
MARS|GREY-BLU|J1|10
MATCH|GREY-Y|J2|1
MERCURY|G|J3|3
NEPTUNE|PUR-W|J1|2
PLUTO|GREY-O|J1|14
SATURN|W-R|J3|9
R. SPECIAL|B-G|J3|21
R. EXTRA BALL|BRN-BLU|J1|24
SPOT "X"|G-B|J1|8
SPOT "Y"|PUR|J1|17
SPOT No|PUR-Y|J1|8
SAME PLAYER SHOOTS AGAIN|GREY-R|J1|26
SAME PLAYER SHOOTS AGAIN|GREY-R|J2|21
SUN SPECIAL|BLU-R|J1|1
SPIN|BRN-B|J1|18
TILT|GREY-B|J2|10
TOP 2,000|B-W|J2|3
TOP 4,000|PUR-B|J2|4
TOP 6,000|W-Y|J2|12
TOP 8,000|GREY-G|J2|13
TOP 10,000|B-Y|J2|5
10X SCORE|GREY|J2|9
URANUS|R-B|J3|16
VENUS|W-GREY|J3|23
2X|R-BLU|J3|18
3X|W-O|J3|20
4X BONUS|B-O|J1|11
5X BONUS|PUR-B|J1|25
"X" ROLL-OVER|W-B|J3|15
"Y" ROLL-OVER|B-R|J3|19"""
LAMP_LIST = [tuple(row.split("|")) for row in LAMP_LIST_TEXT.splitlines()]
BACKBOX_ROWS = {"GAME OVER", "HIGH SCORE TO DATE", "MATCH", "TILT"}
# The SPOT No row prints J1 pin 8, the pin of SPOT "X" (SCR Q28); the row's SCR is read from the connector block's J2 pin 8, Q23, the only SCR with a
# J2 pin and no row. The ROM and the known-working script agree (knowledge note).
ROW_PIN_CORRECTIONS = {"SPOT No": ("J2", 8)}

# public address -> (id, label). The curator checks each against the printed row its SCR reaches.
LAMP_NAMES: dict[int, tuple[str, str]] = {
	1: ("lamp.spinner-value", "Spinner value (SPIN)"),
	2: ("lamp.kicker-lane-a2", "Kicker lane second A"),
	3: ("lamp.spot-y-right-outlane", "Spot Y (right outlane star)"),
	4: ("lamp.roll-over-a2", "Second A roll-over (top right star)"),
	5: ("lamp.planet-pluto", "Planet Pluto"),
	6: ("lamp.planet-jupiter", "Planet Jupiter"),
	7: ("lamp.bonus-40000", "Bonus 40,000"),
	8: ("lamp.bonus-8000", "Bonus 8,000"),
	9: ("lamp.right-extra-ball", "Right extra ball"),
	10: ("lamp.bonus-5x", "5X bonus"),
	11: ("lamp.same-player-shoots-again", "Same player shoots again"),
	12: ("lamp.eject-pocket-8000", "Eject pocket 8,000"),
	13: ("lamp.high-score-to-date", "High score to date (backbox)"),
	17: ("lamp.sun-special", "Sun special"),
	18: ("lamp.kicker-lane-l", "Kicker lane L"),
	19: ("lamp.spot-x-left-outlane", "Spot X (left outlane star)"),
	20: ("lamp.roll-over-l", "L roll-over (top right lane)"),
	21: ("lamp.planet-neptune", "Planet Neptune"),
	22: ("lamp.planet-mars", "Planet Mars"),
	23: ("lamp.bonus-30000", "Bonus 30,000"),
	24: ("lamp.bonus-6000", "Bonus 6,000"),
	25: ("lamp.left-extra-ball", "Left extra ball"),
	26: ("lamp.bonus-4x", "4X bonus"),
	27: ("lamp.spot-drop-target", "Spot (outer return lanes)"),
	28: ("lamp.eject-pocket-6000", "Eject pocket 6,000"),
	33: ("lamp.kicker-lane-y", "Kicker lane Y"),
	34: ("lamp.kicker-lane-a", "Kicker lane A"),
	35: ("lamp.roll-over-y", "Y roll-over (right inner return lane)"),
	36: ("lamp.roll-over-a", "A roll-over (top middle lane)"),
	37: ("lamp.planet-uranus", "Planet Uranus"),
	38: ("lamp.planet-venus", "Planet Venus"),
	39: ("lamp.bonus-20000", "Bonus 20,000"),
	40: ("lamp.bonus-4000", "Bonus 4,000"),
	41: ("lamp.right-special", "Right special"),
	42: ("lamp.bonus-3x", "3X bonus"),
	43: ("lamp.score-10x", "10X score"),
	44: ("lamp.eject-pocket-4000", "Eject pocket 4,000"),
	45: ("lamp.game-over", "Game over (backbox)"),
	49: ("lamp.kicker-lane-x", "Kicker lane X"),
	50: ("lamp.kicker-lane-g", "Kicker lane G"),
	51: ("lamp.roll-over-x", "X roll-over (left inner return lane)"),
	52: ("lamp.roll-over-g", "G roll-over (top left lane)"),
	53: ("lamp.planet-saturn", "Planet Saturn"),
	54: ("lamp.planet-mercury", "Planet Mercury"),
	55: ("lamp.bonus-10000", "Bonus 10,000"),
	56: ("lamp.bonus-2000", "Bonus 2,000"),
	57: ("lamp.left-special", "Left special"),
	58: ("lamp.bonus-2x", "2X bonus"),
	59: ("lamp.eject-pocket-10000", "Eject pocket 10,000"),
	60: ("lamp.eject-pocket-2000", "Eject pocket 2,000"),
	61: ("lamp.tilt", "Tilt (backbox)"),
	63: ("lamp.match", "Match (backbox)"),
}
# Public addresses whose SCR has no printed row; the curator derives the SCR from the decoder table.
UNUSED_LAMP_ADDRESSES = (14, 15, 29, 30, 31, 46, 47, 62)

# --- Option switches -------------------------------------------------------------------------------------------------------
#
# `GALAXY SWITCH ASSIGNMENT` (manual page 9) and the adjustment pages 10-13.

DIPS: dict[int, str] = {
	1: "Coin chute No. 2 credits per coin, selector bit 1 (switches 1-5)",
	2: "Coin chute No. 2 credits per coin, selector bit 2",
	3: "Coin chute No. 2 credits per coin, selector bit 3",
	4: "Coin chute No. 2 credits per coin, selector bit 4",
	5: "Coin chute No. 2 credits per coin, selector bit 5",
	6: "High score feature (OFF = extra ball, ON = replay)",
	7: "Balls per game (OFF = 3, ON = 5)",
	8: "Spot lights feature (OFF = off completely at 4X, ON = off completely at 3X)",
	9: "Coin chute No. 3 credits per coin, selector bit 1 (switches 9-13)",
	10: "Coin chute No. 3 credits per coin, selector bit 2",
	11: "Coin chute No. 3 credits per coin, selector bit 3",
	12: "Coin chute No. 3 credits per coin, selector bit 4",
	13: "Coin chute No. 3 credits per coin, selector bit 5",
	14: "Background sound (OFF = off, ON = on)",
	15: "High game to date feature, selector bit 1 (novelty, 1, 2 or 3 free games)",
	16: "High game to date feature, selector bit 2",
	17: "Extra ball (OFF = no extra ball, ON = award extra ball)",
	18: "Maximum credits, selector bit 1 (10, 15, 25 or 40)",
	19: "Maximum credits, selector bit 2",
	20: "Credit display (ON = yes, OFF = no)",
	21: "Match feature (ON = on, OFF = off)",
	22: "Special replay limit (OFF = 1 per ball, ON = 1 per game)",
	23: "Attract mode sound (OFF = no sounds, ON = sounds)",
	24: "\"A\" feature (OFF = lite each A individually, ON = lite both A's together)",
	25: "Drop target special planet, selector bit 1 (Pluto, Neptune, Uranus or Saturn)",
	26: "Drop target special planet, selector bit 2",
	27: "Coin chute No. 1 credits per coin, selector bit 1 (switches 27-30)",
	28: "Coin chute No. 1 credits per coin, selector bit 2",
	29: "Coin chute No. 1 credits per coin, selector bit 3",
	30: "Coin chute No. 1 credits per coin, selector bit 4",
	31: "Special award, selector bit 1 (no award, extra ball, 100,000 points or replay)",
	32: "Special award, selector bit 2",
}

DISPLAYS = (
	("display.player-1-score", "Player 1 score, six digits", 0, 2, 6),
	("display.player-2-score", "Player 2 score, six digits", 1, 10, 6),
	("display.player-3-score", "Player 3 score, six digits", 2, 18, 6),
	("display.player-4-score", "Player 4 score, six digits", 3, 26, 6),
	("display.credits", "Credits, two digits", 4, 35, 2),
	("display.match-ball-in-play", "Match and ball in play, two digits", 5, 38, 2),
)

# --- Retained table geometry ---------------------------------------------------------------------------------------------
#
# Raw object centres of the retained `Galaxy (Stern 1980).vpx` (Bord, version 1.2; vpxtool extraction), in VPX units; the curator normalizes them by
# the table's own bounds (left 0, top 0, right 952, bottom 1974). Walls use the mean of their drag points. Lamps use the table's bulb light under each
# insert (`L<n>a`, the smaller of the two bulb lights there), never the insert overlay `l<n>`. Every value is re-read from the extraction by the
# retained-evidence test.

TABLE_WIDTH, TABLE_HEIGHT = 952.0, 1974.0

OBJECTS: dict[str, tuple[str, float, float, str]] = {
	"Bumper1": ("Bumper", 695.4585, 242.21129, "Bumper.Bumper1.json"),
	"Bumper2": ("Bumper", 634.21063, 722.84436, "Bumper.Bumper2.json"),
	"Bumper3": ("Bumper", 462.42618, 794.0181, "Bumper.Bumper3.json"),
	"leftslingshot": ("Wall", 84.10880942857143, 1030.0086071428573, "Wall.leftslingshot.json"),
	"rightslingshot": ("Wall", 772.8367385714286, 1027.2256857142856, "Wall.rightslingshot.json"),
	"sw4": ("Wall", 92.5484725, 843.97484, "Wall.sw4.json"),
	"sw9": ("Wall", 155.8528975, 695.98167, "Wall.sw9.json"),
	"sw10": ("Wall", 134.757795, 744.64696, "Wall.sw10.json"),
	"sw11": ("Wall", 114.763929, 792.1538575, "Wall.sw11.json"),
	"sw5": ("Spinner", 356.0758, 559.7046, "Spinner.sw5.json"),
	"sw18": ("Trigger", 267.7202, 1008.7612, "Trigger.sw18.json"),
	"sw18a": ("Trigger", 426.31302, 1396.7115, "Trigger.sw18a.json"),
	"sw19": ("Trigger", 663.91315, 1445.1216, "Trigger.sw19.json"),
	"sw20": ("Trigger", 725.79095, 1421.7662, "Trigger.sw20.json"),
	"sw21": ("Trigger", 191.13486, 1446.824, "Trigger.sw21.json"),
	"sw22": ("Trigger", 127.97601, 1420.506, "Trigger.sw22.json"),
	"sw23": ("Trigger", 807.67926, 1413.0405, "Trigger.sw23.json"),
	"sw24": ("Trigger", 47.580505, 1412.5138, "Trigger.sw24.json"),
	"sw26": ("HitTarget", 805.10126, 869.4077, "HitTarget.sw26.json"),
	"sw29": ("HitTarget", 803.62463, 773.05145, "HitTarget.sw29.json"),
	"sw30": ("HitTarget", 803.3856, 676.1414, "HitTarget.sw30.json"),
	"Drain": ("Kicker", 436.94592, 1907.5042, "Kicker.Drain.json"),
	"kicker": ("Kicker", 95.38158, 573.0997, "Kicker.kicker.json"),
	"sw35": ("Trigger", 95.65024, 527.75464, "Trigger.sw35.json"),
	"sw36": ("Trigger", 483.00327, 501.58743, "Trigger.sw36.json"),
	"sw37": ("Trigger", 583.14825, 477.88934, "Trigger.sw37.json"),
	"sw38": ("Trigger", 682.1112, 454.18564, "Trigger.sw38.json"),
	"sw39": ("Trigger", 802.41187, 436.90912, "Trigger.sw39.json"),
	"sw40": ("Trigger", 426.94522, 221.7935, "Trigger.sw40.json"),
	"LeftFlipper": ("Flipper", 259.9252, 1633.0419, "Flipper.LeftFlipper.json"),
	"RightFlipper": ("Flipper", 591.3068, 1632.3584, "Flipper.RightFlipper.json"),
	"L1a": ("Light", 357.16803, 648.1124, "Light.L1a.json"),
	"L2a": ("Light", 205.46365, 369.27435, "Light.L2a.json"),
	"L3a": ("Light", 807.6565, 1411.427, "Light.L3a.json"),
	"L4a": ("Light", 785.90656, 534.1873, "Light.L4a.json"),
	"L5a": ("Light", 693.0375, 826.4539, "Light.L5a.json"),
	"L6a": ("Light", 459.8213, 965.21466, "Light.L6a.json"),
	"L7a": ("Light", 512.3162, 1132.2784, "Light.L7a.json"),
	"L8a": ("Light", 561.80524, 1296.8693, "Light.L8a.json"),
	"L9a": ("Light", 676.1747, 1230.1431, "Light.L9a.json"),
	"L10a": ("Light", 485.24167, 1482.7467, "Light.L10a.json"),
	"L11a": ("Light", 427.36557, 1551.1926, "Light.L11a.json"),
	"L12a": ("Light", 362.9757, 110.79895, "Light.L12a.json"),
	"L17a": ("Light", 570.7378, 855.3879, "Light.L17a.json"),
	"L18a": ("Light", 204.77557, 306.96274, "Light.L18a.json"),
	"L19a": ("Light", 47.793064, 1411.9451, "Light.L19a.json"),
	"L20a": ("Light", 681.0951, 557.4281, "Light.L20a.json"),
	"L21a": ("Light", 664.31696, 898.3342, "Light.L21a.json"),
	"L22a": ("Light", 399.83868, 919.2465, "Light.L22a.json"),
	"L23a": ("Light", 428.70694, 1103.792, "Light.L23a.json"),
	"L24a": ("Light", 562.9697, 1206.2863, "Light.L24a.json"),
	"L25a": ("Light", 182.37317, 1229.6724, "Light.L25a.json"),
	"L26a": ("Light", 366.58157, 1483.6033, "Light.L26a.json"),
	"L27a": ("Light", 145.16782, 1296.5175, "Light.L27a.json"),
	"L27b": ("Light", 711.13446, 1294.8071, "Light.L27b.json"),
	"L28a": ("Light", 427.74634, 81.457085, "Light.L28a.json"),
	"L33a": ("Light", 207.33655, 496.63055, "Light.L33a.json"),
	"L34a": ("Light", 159.682, 266.6819, "Light.L34a.json"),
	"L35a": ("Light", 662.7174, 1344.3116, "Light.L35a.json"),
	"L36a": ("Light", 582.037, 581.4663, "Light.L36a.json"),
	"L37a": ("Light", 606.41565, 948.4505, "Light.L37a.json"),
	"L38a": ("Light", 345.95682, 865.78284, "Light.L38a.json"),
	"L39a": ("Light", 344.7276, 1132.4634, "Light.L39a.json"),
	"L40a": ("Light", 292.12445, 1207.3263, "Light.L40a.json"),
	"L41a": ("Light", 702.26605, 1158.0085, "Light.L41a.json"),
	"L42a": ("Light", 527.92285, 1396.1223, "Light.L42a.json"),
	"L43a": ("Light", 582.8836, 167.60977, "Light.L43a.json"),
	"L44a": ("Light", 493.76553, 81.613144, "Light.L44a.json"),
	"L49a": ("Light", 205.67175, 433.78485, "Light.L49a.json"),
	"L50a": ("Light", 110.3627, 307.26105, "Light.L50a.json"),
	"L51a": ("Light", 191.1181, 1345.5146, "Light.L51a.json"),
	"L52a": ("Light", 482.58002, 606.5869, "Light.L52a.json"),
	"L53a": ("Light", 535.9506, 976.2831, "Light.L53a.json"),
	"L54a": ("Light", 279.54068, 831.6649, "Light.L54a.json"),
	"L55a": ("Light", 428.5219, 1250.6631, "Light.L55a.json"),
	"L56a": ("Light", 290.75583, 1294.7833, "Light.L56a.json"),
	"L57a": ("Light", 154.85495, 1156.1824, "Light.L57a.json"),
	"L58a": ("Light", 327.31543, 1395.323, "Light.L58a.json"),
	"L59a": ("Light", 346.11975, 172.91617, "Light.L59a.json"),
	"L60a": ("Light", 563.29535, 81.3626, "Light.L60a.json"),
}

# Matrix switch -> the table object(s) its known-working script binds, plus what kind of point it is.
SWITCH_OBJECTS: dict[int, tuple[list[str], str | None]] = {
	4: (["sw4"], "Placed at the mean of the drop-target wall's own drag points, the target face the script drops; the leaf switch under the bank has no object."),
	9: (["sw9"], "Placed at the mean of the drop-target wall's own drag points, the target face the script drops."),
	10: (["sw10"], "Placed at the mean of the drop-target wall's own drag points, the target face the script drops."),
	11: (["sw11"], "Placed at the mean of the drop-target wall's own drag points, the target face the script drops."),
	5: (["sw5"], None), 12: (["Bumper1"], None), 13: (["Bumper2"], None), 14: (["Bumper3"], None),
	15: (["rightslingshot"], "Placed at the mean of the right slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position."),
	16: (["leftslingshot"], "Placed at the mean of the left slingshot wall's own drag points, a projection onto the rubber, not a measured leaf-switch position."),
	18: (["sw18", "sw18a"], "One placement per star, on the two triggers the script binds to this address (sw18 left of centre, sw18a at the centre between the lower lanes)."),
	19: (["sw19"], None), 20: (["sw20"], None), 21: (["sw21"], None), 22: (["sw22"], None), 23: (["sw23"], None), 24: (["sw24"], None),
	26: (["sw26"], None), 29: (["sw29"], None), 30: (["sw30"], None),
	33: (["Drain"], "Placed on the table's Drain kicker, its ball-collection proxy for the out-hole; the out-hole switch itself is not modelled."),
	35: (["sw35"], None), 36: (["sw36"], None), 37: (["sw37"], None), 38: (["sw38"], None), 39: (["sw39"], None), 40: (["sw40"], None),
}
# Each side's end-of-stroke contact is placed on that side's flipper pivot.
DIRECT_OBJECTS = {1: "LeftFlipper", 2: "RightFlipper"}
# Solenoid -> object(s) and, for a projection, why.
SOLENOID_OBJECTS: dict[int, tuple[list[str], str | None]] = {
	1: (["rightslingshot"], "Placed at the mean of the right slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	2: (["leftslingshot"], "Placed at the mean of the left slingshot wall's drag points, the rubber the coil kicks; the coil sits under it."),
	3: (["Bumper1"], None), 7: (["Bumper2"], None), 12: (["Bumper3"], None),
	4: (["sw9", "sw10", "sw11", "sw4"], "Projected onto the 4-bank it resets: the mean of the table's own four drop-target walls. The reset coil sits under the bank and has no object."),
	5: (["kicker"], None),
	8: (["sw40"], "Placed on the saucer's switch trigger, the pocket the coil ejects from; the table's saucer has no separate kicker object."),
	9: (["sw4"], "Projected onto the red drop target it knocks down: its own coil sits under that target and has no object."),
	10: (["sw11"], "Projected onto the blue drop target it knocks down."),
	13: (["sw10"], "Projected onto the yellow drop target it knocks down."),
	14: (["sw9"], "Projected onto the black drop target it knocks down."),
	11: (["Drain"], "Placed on the table's Drain kicker, the ball-collection proxy where the ball enters the out-hole; the out-hole coil is not modelled."),
}

# Public lamp -> the bulb light(s) under the insert(s) its script binding and printed row name.
LAMP_OBJECTS: dict[int, list[str]] = {address: [f"L{address}a"] for address in (
	1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
	49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60)}
LAMP_OBJECTS[27] = ["L27a", "L27b"]

# --- Curator details -------------------------------------------------------------------------------------------------------

FLIPPER_PART = "J-25-450/34-4500"
FLIPPER_PART_ROW = "Flipper Left & Right (2)"

# Public solenoids the retained gameplay or game-over runs fire, and those the known-working script binds a callback to.
GAMEPLAY_SOLENOIDS = (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19)
SCRIPT_SOLENOIDS = (4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 17, 19)

# Public lamps the ROM drove outside its own tests in the retained gameplay and game-over runs.
GAMEPLAY_LAMPS = (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45,
	49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 63)

LAMP_NOTES: dict[int, str] = {
	4: "The row `\"A\" ROLL-OVER (2)` is the second A of G-A-L-A-X-Y, the insert at the top-right star roll-over (switch 39); the first A is lamp 36 at the top middle lane.",
	6: "The lists spell the planet `JUPITOR`.",
	9: "Never lit outside the ROM's own tests in the retained runs: PinMAME's default option switches leave the extra-ball award off.",
	11: "The list braces one description over two jack rows, J1 pin 26 and J2 pin 21, and the connector block gives both pins to SCR Q3, so one output feeds two printed loads. "
		"Only the playfield insert is placed; the lists do not say where the second load is, and no quantity is asserted.",
	25: "The row prints the description in quotes, `\"L\" EXTRA BALL`, like the letter rows; the table puts the insert at the left side, the mirror of the right extra ball (lamp 9), and the "
		"definition reads it as the left extra ball. The connector block's J1 pin for SCR Q24 is a blotted figure that reads 3, 5 or 8; pin 3 belongs to Q35 and pin 8 to Q28, whose rows the ROM "
		"confirms, and the lamp list prints this row on J1 pin 5, which no other row uses. Never lit outside the ROM's own tests in the retained runs.",
	34: "The connector block prints SCR Q38's J3 pin as an overprinted figure that reads 29; the lamp list prints `\"A\" KICKER` on J3 pin 25, which no other row uses, and the ROM lit public 34 "
		"with the A roll-over lamp when the top middle lane closed (retained gameplay run).",
	35: "The connector block prints SCR Q44's J3 pin as a blotted figure that reads 19 or 15; the lamp list prints `\"Y\" ROLL-OVER` on J3 pin 19, and the ROM lit public 35 when the right "
		"inner return lane (Y) closed (retained gameplay run).",
	40: "The connector block prints SCR Q20's J1 pin as 13 or 15; the lamp list prints `BONUS 4` on J1 pin 13 (pin 15 is JUPITOR's), and the ROM lit public 40 when the bonus advanced from 2 to 4 "
		"(retained gameplay run).",
	27: "Both lists print `SPOT No` on J1 pin 8, the pin of `SPOT \"X\"` (SCR Q28, public 19). The connector block's J2 pin 8 carries SCR Q23, the only SCR with a pin and no printed row, and "
		"the ROM and the known-working script both treat public 27 as the spot lamp of the two outer return lanes: the right outer lane (switch 20) spotted a drop target with public 27 lit in "
		"the retained gameplay run. The row is therefore read as J2 pin 8. It lights two inserts, one at each outer return lane (the table's two bulb lights on this address).",
	41: "Never lit outside the ROM's own tests in the retained runs: PinMAME's default option switches leave the special award off.",
	57: "Never lit outside the ROM's own tests in the retained runs: PinMAME's default option switches leave the special award off.",
}

GATE_NOTES = ("Two gates with no coil or switch (playfield parts drawing): `BALL GATE A-104-R2` (callout 5), where the shooter lane meets the top arch, which lets the plunged ball out and keeps it "
	"from falling back, and `1-WAY GATE ASS'Y A-644` (callout 6, wire form 6A-257), a short wire at the left end of the top-lane group below the eject pocket's loop. They route the ball by its "
	"own motion; do not invent a powered diverter. The retained table models them as `Gate1` and `Gate2`.")

EXCLUDED_OBJECT_CLASSES = [
	"l<n> insert overlays, l<n>z and l27c glows: render helpers drawn over or under the inserts; every lamp is placed on its bulb light L<n>a (and L27b) instead",
	"GI1 collection lights, flashers and the VR backglass objects: render and general-illumination helpers; the general illumination has no bulb inventory in any retained source",
	"Gate1, Gate2: the two passive gates of the mechanism record, carrying no controller binding; Gate7 is a hidden gate in the shooter lane",
	"Drain: the table's ball-collection kicker, used only as the projection point of the out-hole switch and kicker",
]

EOS_NOTES = ("Hard-wired contact of the side's dual-winding flipper coil, not a PinMAME switch address. The playfield wiring diagram draws each flipper as two windings in series with a "
	"contact across the lower one, which conducts at rest and opens at the end of the stroke to put the second winding in series (normally closed); the sheet prints no `EOS` text.")

GI_NOTES = ("Transformer-fed general illumination, switched by the general-illumination relay (public 17). The playfield wiring diagram draws `GEN. ILLUM` from A2J1-8 (W) at 6 VAC "
	"returning on A2J1-1 (R), the cabinet sheet draws `FRONT DOOR LITES` from A2J2-1 (Y-B) returning on A2J2-5 (G-R), and the general-use Transformer Schematic brings out `GEN. ILL. BUS` "
	"on A2J1-8, A2J2-1, A2J3-10 and A2J3-11 with `GEN. ILL. RETURN` on A2J2-5, A2J3-1 and A2J3-2. None of these sheets draws a relay contact in the circuit; the cabinet sheet draws only "
	"the `GEN. ILLUM. RELAY` coil, and no sheet shows which strings its contacts switch. The known-working script switches all of the table's general illumination, playfield and backglass, "
	"off while public 17 is on, and IPDB records the machine's computer-controlled general illumination. Bulb quantity and positions are not established.")
GI_WIRING = {"board": "Transformer/rectifier A2 general-illumination buses, switched by the general-illumination relay", "nominal_voltage_v": 6, "voltage_type": "ac",
	"power_connection": "A2J1-8 (playfield); A2J2-1 (front door); A2J3-10, A2J3-11 (backbox)", "return_connection": "A2J1-1; A2J2-5; A2J3-1, A2J3-2"}

REMOTE_MEMORY_CLEAR_NOTES = ("The `S33` of Figure 1, which marks one on the MPU assembly in the back box and one on the open front door beside the credit button; the cabinet sheet draws "
	"`S33 MEMORY CLEAR` from A4J3-5 (-W-) to A3J2-7 (Y-R), the same return as the Self Test button. It reaches the MPU's external memory-clear input rather than a matrix position; the "
	"manual's high-score text uses S33 to set a level quickly to `00`. This profile-local physical binding has no controller transport, and no ROM effect is claimed from a host write.")


CROP_DERIVATIONS: dict[str, str] = {
	"switch-locations": "Stern_1980_Galaxy_Manual.pdf page 17, crop box 0,0,1,1, scanned page rendered at its native resolution (embedded image xref 94, 2550px across 8.50in), rendered at 106 dpi, capped to 900px wide, grayscale, 900x1165 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"solenoid-locations": "Stern_1980_Galaxy_Manual.pdf page 19, crop box 0,0,1,1, scanned page rendered at its native resolution (embedded image xref 104, 2550px across 8.50in), rendered at 106 dpi, capped to 900px wide, grayscale, 900x1165 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"playfield-parts": "Stern_1980_Galaxy_Manual.pdf page 15, crop box 0,0,1,1, scanned page rendered at its native resolution (embedded image xref 83, 2550px across 8.50in), rendered at 106 dpi, capped to 900px wide, grayscale, 900x1165 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"playfield-switch-matrix": "Stern_1980_Galaxy_Manual.pdf page 23, crop box 0.08,0.09,0.67,0.73, scanned page rendered at its native resolution (embedded image xref 125, 2550px across 8.50in), rendered at 259 dpi, capped to 1300px wide, grayscale, 1301x1826 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"playfield-coil-wiring": "Stern_1980_Galaxy_Manual.pdf page 23, crop box 0.66,0.1,1,0.76, scanned page rendered at its native resolution (embedded image xref 125, 2550px across 8.50in), rendered at 242 dpi, capped to 700px wide, grayscale, 701x1759 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"lamp-driver-connector-labels": "Stern_1980_Galaxy_Manual.pdf page 31, crop box 0.42,0.1,0.54,0.8, scanned page rendered at its native resolution (embedded image xref 166, 2550px across 8.50in), rendered at 300 dpi, grayscale, 306x2310 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"lamp-driver-decoder-outputs": "Stern_1980_Galaxy_Manual.pdf page 30, crop box 0.07,0.15,0.87,0.8, scanned page rendered at its native resolution (embedded image xref 161, 2550px across 8.50in), rendered at 206 dpi, capped to 1400px wide, grayscale, 1401x1473 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"cabinet-wiring": "Stern_1980_Galaxy_Manual.pdf page 24, crop box 0.02,0.05,0.97,0.78, scanned page rendered at its native resolution (embedded image xref 130, 2550px across 8.50in), rendered at 161 dpi, capped to 1300px wide, grayscale, 1301x1294 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
	"solenoid-driver": "Stern_1980_Galaxy_Manual.pdf page 26, crop box 0,0.08,1,0.8, scanned page rendered at its native resolution (embedded image xref 140, 2550px across 8.50in), rendered at 176 dpi, capped to 1500px wide, grayscale, 1500x1398 WebP quality 80, PyMuPDF 1.28.2 via tools/render_excerpt_image.py",
}

KNOWLEDGE = """# Galaxy (Stern, 1980)

Coverage: **partial - the controller inventory, wiring, mechanisms and rules are documented and the public addresses proved by the ROM's own tests; every placement rests on one community table with no independent check, and general illumination is unplaced**

## Identity and evidence precedence

This is the one physical Stern Galaxy (IPDB 980, January 1980, model 114, Stern M-200 MPU, 4,947 units; LAI built it under licence in Australia from knock-down kits). PinMAME `galaxy` is the production
root and `galaxyfp` its free-play build; `galaxyps` (Planet Skillshot, 2011) changes the rules only. All three use the same game-data line (`GEN_STMPU200`, six-digit `dispst6` displays,
`FLIP_SW(FLIP_L)`, no extra lamp columns, ST300 sound). `galaxyb` (2003) and `galaxyc` (2023) are seven-digit conversions: the same machine with seven-digit display hardware (`dispst7`, recorded
as display overrides).

Evidence order is the runbook's. The pinned corpus script (bord's table 1.2, byte-identical to the retained table's own script) gives runtime bindings, this game's own manual gives construction and
wiring (its Playfield Wiring Diagram, Solenoid Driver and Lamp Driver sheets are drawn for Galaxy; the cabinet and transformer sheets are standard and general-use drawings), pinned PinMAME gives the
controller topology, and six retained harness runs (burn-in, solenoid test, switch test, a scripted game, and a game-over and slam run of `galaxy`, plus the solenoid test of `galaxyb`) pair the
printed numbers with public addresses. The manual prints each schematic in two halves on consecutive pages.

## Address translations

**Switches.** The matrix is five strobes by eight returns, public 1-40, and the ROM's switch test shows the closed address's own number for every one of the forty, so the Switch Identification numbers
are the public addresses. Positions 17, 25, 27, 28, 31, 32 and 34 are printed `OPEN` (`N/U` on the matrix sheet) and are unused. Position 33 is printed `OPEN` in the identification table, but the
matrix sheet labels it `OUT-HOLE`, the location drawing points at the out-hole, and the ROM kicks the out-hole while it is closed: it is the out-hole switch. Every matrix contact is normally open; the
playfield sheet draws a series diode on every cell, and the cabinet sheet draws coin chutes 2 and 3 without one. Service inputs are -7 (Self Test), -6 (CPU diagnostic NMI) and -5 (sound diagnostic); the
last two are PinMAME routes with no documented button. The flipper buttons are PinMAME's synthetic 84 (left) and 82 (right); 81 and 83 are unused. The flippers' end-of-stroke contacts and the door's S33
memory-clear button are hard-wired and have only profile-local identities (physical direct inputs 1-3).

**Solenoids.** The printed solenoid numbers are SDU driver transistor positions, and the public addresses do not follow them. The ROM's solenoid test shows each driver number while it fires, pairing them
as `1->2, 2->1, 3->6, 4->7, 5->3, 6->4, 7->5, 8->8, 9->11, 10->12, 11->14, 12->13, 13->9, 14->10, 15->19, 16->15, 17->17, 18->20, 19->18` over three identical cycles, and the `galaxyb` test gives the
same pairs. In public terms: 1 right slingshot, 2 left slingshot, 3 top thumper, 4 drop-target bank reset, 5 kicker-lane ball kicker, 6 knocker, 7 lower right thumper, 8 saucer eject, 9 red, 10 blue,
13 yellow and 14 black drop-target knock-down coils, 11 out-hole kicker, 12 lower left thumper, 17 general-illumination relay, 18 coin lockout, 19 flipper enable relay. Public 15 (driver 16) is printed
OPEN and unused; 16 is an unaddressable decoder slot; 20 (driver 18) is wired only to N/U pins and is driven only in the power-up pulse and the tests, so it is unused. The gameplay run independently
confirms 1-5, 7-14, 17 and 19.

**Lamps.** The Lamp Driver module has sixty discrete SCR outputs. A public lamp is `16 * k + a + 1` for decoder `U(k+1)` output `S(a)`, and each output line's resistor `R<n>` ends at SCR `Q<n>`; this
game's own sheet was read for all sixty lines. The connector blocks give each SCR its pin; several of their hand-written pin numbers are blotted, and each is settled by the lamp list and the ROM
(the device notes say which). The two typed lamp lists, on the Playfield Wiring Diagram and the Lamp Driver Schematic, print the same 53 lines; they land on 52 public addresses (SAME PLAYER SHOOTS AGAIN is
braced over two pins of one SCR). `SPOT No` prints J1 pin 8, which is the pin of `SPOT "X"`; it is read as J2 pin 8 (SCR Q23, public 27), the only connected SCR without a row, which the ROM and the
script agree on. The eight SCRs without a row, public 14, 15, 29, 30, 31, 46, 47 and 62, change only in the burn-in and lamp tests and are unused. Four backbox lamps are listed with the rest: GAME OVER
45, HIGH SCORE TO DATE 13, MATCH 63 and TILT 61.

**General illumination.** IPDB notes that Galaxy has computer-controlled general illumination, perhaps the first machine to have it. The Solenoid Driver Schematic wires continuous driver Q17 (public 17) to
J5 pin 7 `GEN. ILLUM. RELAY`, and the cabinet sheet draws the relay coil beside the coin lockout and the knocker. No sheet draws the relay's contacts: the playfield sheet draws the 6 VAC `GEN. ILLUM`
string, the cabinet sheet the front-door lamp and the transformer sheet the backbox strings, all straight from the transformer. The known-working script switches all of the table's general illumination off
while 17 is on, and the ROM flickers 17 for about two seconds when a game starts, when the top-right star completes G-A-L-A and at game over. The definition records 17 as a relay that turns the general
illumination off while energized (relationship `inverted`); which strings the real relay switches is not documented.

## Ball lifecycle

Galaxy is a single-ball game with no trough. The ball starts on the out-hole switch (33). When a game starts the ROM resets the drop-target bank (4) and kicks the out-hole (11), repeating the kick for as
long as 33 stays closed; a real ball leaves 33 on the first kick and rolls to the shooter lane, where the player launches it through the ball gate at the top of the lane. After a drain the bonus is
added, the ball-in-play digit advances and the kick repeats. Tilt drops the flipper enable relay (19) and lights TILT; a slam (8) ends the game and the ROM restarts through its power-up test.

## Mechanisms

- **Four-bank drop targets** on the left, top to bottom black (switch 9), yellow (10), blue (11) and red (4). One reset coil (4) raises the bank; each target also has its own knock-down coil (14 black,
  13 yellow, 10 blue, 9 red) that the ROM fires to spot it: the upper, middle and lower stand-ups (30, 29, 26) knock down black, yellow and blue, and the return lanes knock down red. The ROM resets the bank
  when its fourth target goes down and at every serve; each completion advances the planet ladder Mercury (54), Venus (38), Mars (22), Jupiter (6), Saturn (53), Uranus (37), Neptune (21), Pluto (5).
- **Eject pocket (saucer)** at the top, inside the loop: switch 40, eject coil 8, about three seconds after the closure. Its value (2,000 to 10,000, lamps 60, 12, 28, 44, 59) is advanced by the top
  thumper and the spinner.
- **Kicker lane (kickback)** at the upper left: switch 35, kicker coil 5 about four seconds after the closure; it scores 3,000 plus 2,000 for each G-A-L-A-X-Y letter spotted.
- **Spinner** across the passage below the eject pocket: switch 5, no coil.
- **Thumper bumpers** 12 (top), 13 (lower right), 14 (lower left) fire public 3, 7 and 12; **slingshots** 16 (left) and 15 (right) fire 2 and 1.
- **Flippers**: one per side, each a dual-winding coil on its cabinet button, gated by the flipper enable relay. PinMAME publishes one callback per side (46 right, 48 left, with 45 and 47 alongside).
- **Passive gates**: the ball gate where the shooter lane meets the top arch and a one-way gate at the left end of the top lanes.

## Rules summary

From the manual's feature pages: spotting G-A-L-A-X-Y lights the letters in the kicker lane; the top lanes and the top-right star spot G-A-L-A, and the left and right inner return lanes spot X and Y. The
outer return lanes score 2,000 and spot a drop target when lit; the outlane stars score 5,000 (10,000 when lit). Completing the drop-target bank advances the planets; the drop-target special lights at the
planet the option switches choose. The stand-ups score 500 and spot their drop target; the star roll-overs score 10 and advance the bonus. Option switch 24 lets the two A's light together.

## Scoring checkpoints from the retained gameplay run

Thumpers 1,000; slingshots 10; top lanes 5,000 with X and Y made; stand-ups 500; the spinner 1,000 when lit; the outer return lanes 2,000; the inner return lanes 500; the outlanes 5,000; the
center stars 10. These are first-ball ROM scores and only checkpoints.

## Option switches

The thirty-two MPU option switches are S1-8, S9-16, S17-24 and S25-32 (Figure 1, page 9). Coin chutes 2, 3 and 1 take S1-5, S9-13 and S27-30. S6 high-score award, S7 balls per game, S8 spot lights,
S14 background sound, S15-16 high game to date, S17 extra ball, S18-19 maximum credits, S20 credit display, S21 match, S22 special replay limit, S23 attract sound, S24 the A feature, S25-26 the planet
that lights the drop-target special, S31-32 special award. S33 on the MPU is a memory-clear pushbutton, repeated on the coin door.

## Displays and sound

Four six-digit player displays (indices 0-3, segment starts 2, 10, 18 and 26), a two-digit credit display (index 4, start 35) and a two-digit match/ball-in-play display (index 5, start 38): PinMAME
`dispst6`. The seven-digit conversions move the player displays to starts 1, 9, 17 and 25. Sound is the Stern C-605 sound module (ST300); sound commands add no playfield devices.

## Disagreements between this game's own documents

- The Switch Identification table calls drop target 9 and stand-up 30 GREEN; the matrix sheet calls both BLACK, and the feature text calls the upper target black. One colour, two names.
- The Switch Identification table prints 33 as OPEN; the matrix sheet, the location drawing and the ROM make it the out-hole.
- Both lamp lists print `SPOT No` on the pin of `SPOT "X"`; see the address translations.
- The credit text says coin chute 1 uses switches 28-30; the switch assignment braces 27-30 and the chute 1 table has four columns, 30 to 27.

## Recreation checklist

- Build the full inventory: 33 used and seven unused matrix positions, three service inputs, four flipper-button positions, 32 option switches, the solenoid addresses 1-15 and 17-20 with the two
  flipper callbacks, the sixty SCR lamp addresses and the six displays.
- Start with the ball on the out-hole switch, all four drop targets up, the saucer empty and the flipper enable relay off until a game starts.
- Reproduce the ROM-fired thumpers and slingshots, the bank reset and the four knock-down coils, the saucer eject, the kicker-lane kickback, the out-hole serve loop and the tilt behaviour as the harness runs show.
- Turn the general illumination off while public 17 is on.
- Treat the manual and the ROM as the rules authority; the community ROMs change rules or displays, not the playfield.
- Placements come from the retained table only; the spatial report lists what still needs an independent check.

## Sources

- `manual.stern.galaxy.1980`: the 35-page IPDB manual, with transcribed excerpts of its identification tables, location drawings, parts pages, option switches, operating text and wiring sheets.
- `vpx-script.galaxy-bord-1-2`: the pinned corpus script.
- `vpx-table.galaxy-bord-1-2`, its embedded script and its retained extraction: the geometry of every placement.
- `runtime.galaxy.*` and `runtime.galaxyb.solenoid-test`: six isolated harness runs on the pinned `pinmame64.dll`; ROM bytes and raw NVRAM remain outside the repository.
- `pinmame.core.46e1a01a0f73`: driver declarations, MPU-200 implementation, public-address conversion and display layout.
"""
