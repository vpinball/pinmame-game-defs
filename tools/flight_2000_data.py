"""Reviewed physical crosswalk for Stern Flight 2000."""

SWITCH_LABELS = (
    "Left coin chute", "Center coin chute", "Right coin chute", "Left spinner",
    "Right spinner", "Start / credit button", "Roll and pendulum tilts", "Slam and vibration tilts",
    "Upper left slingshot", "Upper right slingshot", "Lower left slingshot", "Lower right slingshot",
    "Upper thumper bumper", "Lower thumper bumper", "First-stage left kickout", "Second-stage right kickout",
    "B rollover and top stand-up targets", "L upper rollover", "A upper rollover", "S upper rollover",
    "T upper rollover", "O right outer return lane", "F right inner return lane", "F left inner return lane",
    "Right bank top drop target", "Right bank middle drop target", "Right bank bottom drop target",
    "Left bank drop target 1", "Left bank drop target 2", "Left bank drop target 3",
    "Left bank drop target 4", "Left bank drop target 5", "Right out-hole trough contact",
    "Center out-hole trough contact", "Left out-hole trough contact", "Left outlane",
    "Right outlane", "Spot BLAST stand-up target", "Ball launcher contact", "Release Next Rocket rollover",
)
CABINET_SWITCHES = {1, 2, 3, 6, 7, 8}
SCHEMATIC_SWITCH_RETURNS = {12: "W-B", 13: "W-G", 14: "W-BRN", 15: "BRN-Y"}
SWITCH_OBJECTS = {
    4: ("Spinner.sw4",), 5: ("Spinner.sw5",),
    9: ("Wall.LeftSlingShot2",), 10: ("Wall.RightSlingShot2",),
    11: ("Wall.LeftSlingShot1",), 12: ("Wall.RightSlingShot1",),
    13: ("Bumper.sw13",), 14: ("Bumper.sw14",),
    17: ("Trigger.sw17", "HitTarget.sw17a", "HitTarget.sw17a1"),
    38: ("HitTarget.sw38",), 40: ("Trigger.sw40",),
}
SWITCH_OBJECTS.update({n: (f"Trigger.sw{n}",) for n in (*range(15, 17), *range(18, 25), 36, 37)})
SWITCH_OBJECTS.update({n: (f"HitTarget.sw{n}",) for n in range(25, 33)})

# Public ordinal -> transcribed Q, physical label, projected playfield object.
COILS = {
    1: (2, "Upper left slingshot", "Wall.LeftSlingShot2"),
    2: (1, "Upper right slingshot", "Wall.RightSlingShot2"),
    3: (5, "Lower left slingshot", "Wall.LeftSlingShot1"),
    4: (6, "Lower right slingshot", "Wall.RightSlingShot1"),
    5: (7, "Upper thumper bumper", "Bumper.sw13"),
    6: (3, "Lower thumper bumper", "Bumper.sw14"),
    7: (4, "Left drop-target bank reset", "HitTarget.sw30"),
    8: (8, "Left bank individual drop 5", "HitTarget.sw32"),
    9: (13, "Ball launcher / walker release", None),
    10: (14, "Outhole serve kicker", "Kicker.BallRelease"),
    11: (9, "Left bank individual drop 4", "HitTarget.sw31"),
    12: (10, "Left bank individual drop 3", "HitTarget.sw30"),
    13: (12, "Left bank individual drop 1", "HitTarget.sw28"),
    14: (11, "Left bank individual drop 2", "HitTarget.sw29"),
    15: (16, "Right drop-target bank reset", "HitTarget.sw26"),
    17: (17, "Second-stage right kicker", "Trigger.sw16"),
    18: (19, "Coin lockout", None),
    19: (15, "Flipper enable relay", None),
    20: (18, "First-stage left kicker", "Trigger.sw15"),
}
COIL_PARTS = {
    **dict.fromkeys((1, 2, 3, 4, 5, 6, 9, 17, 20), "J-26-1500"),
    **dict.fromkeys((8, 11, 12, 13, 14), "C1-34-3400"),
    7: "B-24-1600", 10: "J-26-1200", 15: "B-27-2300", 18: "C-36-5300",
}

DIP_LABELS = {
    1: "Left chute pricing 1", 2: "Left chute pricing 2", 3: "Left chute pricing 3",
    4: "Left chute pricing 4", 5: "Add-a-ball memory 1", 6: "High score award",
    7: "Balls per game", 8: "Add-a-ball memory 2",
    9: "Center chute pricing 1", 10: "Center chute pricing 2",
    11: "Center chute pricing 3", 12: "Center chute pricing 4",
    13: "Spot one or two F lamps", 14: "Background sound",
    15: "High game to date award 1", 16: "High game to date award 2",
    17: "Talking sound", 18: "Maximum credits 1", 19: "Maximum credits 2", 20: "Credits display",
    21: "Match feature", 22: "Right spinner lamp memory", 23: "MPU DIP 23", 24: "Apollo 1 and 2 lamp startup",
    25: "Right chute pricing 1", 26: "Right chute pricing 2", 27: "Right chute pricing 3",
    28: "Right chute pricing 4", 29: "Special award limit", 30: "Bonus multiplier memory",
    31: "Special award type 1", 32: "Special award type 2",
}

# Printed load-list row numbers ordered by public lamp address. The artwork and
# script distinguish the effects on rows that repeat a printed connection.
LAMP_ROWS = {
    1: (9,), 2: (13,), 3: (17,), 4: (20,), 5: (7,), 6: (4,), 7: (35,), 8: (31,),
    9: (38,), 10: (54,), 11: (45, 46), 12: (42,), 13: (27,), 14: (47,), 15: (50,),
    17: (10,), 18: (14,), 19: (18,), 20: (21,), 21: (8,), 22: (3,), 23: (34,),
    24: (30,), 25: (60,), 26: (55,), 27: (39,), 28: (59,), 29: (48,), 30: (58,), 31: (49,),
    33: (11,), 34: (15,), 35: (37,), 36: (22,), 37: (6,), 38: (2,), 39: (33,), 40: (29,),
    41: (51,), 42: (56,), 43: (40,), 44: (44,), 45: (26,), 46: (43,),
    49: (12,), 50: (16,), 51: (19,), 52: (23,), 53: (5,), 54: (1,), 55: (32,),
    56: (28,), 57: (53,), 58: (57,), 59: (41,), 60: (25,), 61: (52,), 62: (24,), 63: (36,),
}
# Explicit review overrides for duplicated pin assignments and ink that does not
# settle the harness. Entries retain the factory rows as evidence, without
# attaching their pin/wire to the candidate public address.
UNVERIFIED_LAMP_WIRING = {
    29: "The listed J2-30 pin cannot be traced on the drawing. The Special insert beside Spot BLAST and the VPX binding both identify the effect.",
    37: "The chart calls O a top rollover, but the artwork places it at the right outer return. Closing 22 in stock play extinguishes 37. The printed pin is duplicated on the board drawing.",
    44: "The upper stage insert lights after countdown qualification. The load chart repeats J2-5 for both Second Stage Go lamps, while that net also reaches the spinner 1,500 branch.",
    46: "The central stage insert lights on the second walker capture. The load chart repeats J2-5 for both Second Stage Go lamps, while that net also reaches the spinner 1,500 branch.",
    53: "Hitting the upper T in stock play extinguishes 53 and lights the corner T at 55. The load chart repeats J3-4 for both T lamps.",
    55: "The corner T lights on a hit to the upper T rollover. The load chart repeats J3-4 for both T lamps.",
    59: "The factory list and schematic agree on the black J3-13 spinner 1,500 branch. The same SCR has a J2-5 branch whose fitted load remains unverified.",
    60: "The upper stage insert lights after countdown qualification. The load chart repeats J2-7 for both First Stage Go lamps.",
    62: "The central stage insert lights on the first walker capture. The load chart repeats J2-7 for both First Stage Go lamps.",
    63: "The factory load chart gives Match as grey-yellow at J2-1 and the VPX identifies it as Match. The board drawing labels a second J2 endpoint 1 on Q39.",
}
LAMP_RULE_TRACE = {37, 44, 46, 53, 55, 60, 62}
LAMP_CONFIRMED_BRANCHES = {59}
LAMP_LABELS = {
    5: "Left inner return F insert", 6: "Upper S rollover insert",
    7: "Left corner BLASTOFF final F", 8: "Left corner BLASTOFF S",
    11: "Shoot Again (playfield and backbox)",
    15: "Right outlane Special", 21: "Right inner return F insert", 22: "Upper A rollover insert",
    23: "Left corner BLASTOFF first F", 24: "Left corner BLASTOFF A",
    28: "All Systems Go upper insert", 29: "Upper center lane Special",
    30: "All Systems Go center insert", 31: "Left outlane Special",
    37: "Right outer return O insert", 38: "Upper L rollover insert", 39: "Left corner BLASTOFF O",
    40: "Left corner BLASTOFF L", 44: "Second Stage Go upper insert", 46: "Second Stage Go center insert",
    53: "Upper T rollover insert", 54: "Left outer return B insert", 55: "Left corner BLASTOFF T",
    56: "Left corner BLASTOFF B", 60: "First Stage Go upper insert", 62: "First Stage Go center insert",
}
BACKBOX_LAMPS = {13, 45, 61, 63}
MOMENTARY_SWITCHES = {4, 5, 9, 10, 11, 12, 13, 14, 38}

DRIVER_NOTES = {
    "flight2k": "Production CPU set with VSU-100 U9 speech ROM.",
    "flightfp": "Always-free-play U5 and U6 replacements use the production U1, U2 and VSU-100 U9. The stock all-DIPs-off boot test is retained.",
    "flight2m": (
        "Hardware compatibility for the documented replay-knocker setup requires moving the former coin-lockout lead "
        "at A3J2-8 (public 18) to the knocker. Keep the walker at A3J5-12 (public 9) and the stock VSU-100 U9 speech ROM. "
        "The DIP 14 routing selection is documented from subversion 39 onward. In 3335, DIP 18 selects a countdown reset, "
        "DIP 19 selects free play and DIP 23 selects a center-Special extra ball. The revised switch test cycles closed contacts."
    ),
    "flight2mb": (
        "Hardware compatibility requires the revised VSU-100 speech ROMs and wiring that matches DIP 14. "
        "With DIP 14 ON, keep the walker at A3J5-12 (public 9) and move the former coin-lockout lead at A3J2-8 "
        "(public 18) to the replay knocker. With DIP 14 OFF, swap those leads so A3J2-8 (public 18) drives the walker "
        "and A3J5-12 (public 9) drives the knocker. The author allows omitting the knocker on the unswapped harness "
        "with DIP 14 ON. A DIP/wiring mismatch can damage the driver board. PinMAME loads two revised 2716 speech images "
        "at U9 and U10. The author also documents one 2532 at U9 with U10 empty on physical hardware. "
        "DIP 17 selects attract speech, DIP 19 selects free play and DIP 23 selects a center-Special extra ball. "
        "Adjustments 19–22 set tilt warnings, high-score replays, maximum credits and multiball difficulty."
    ),
}

MECHANISMS = (
    ("left-five-bank", "Left five-target memory bank", "drop_target_bank", "D-548-9A",
     (7, 8, 11, 12, 13, 14), range(28, 33),
     "The common reset raises all five targets. Five individual actuators trip targets down to spot the lit countdown target. The controller follows each leaf switch when its target is down."),
    ("right-three-bank", "Right three-target bank", "drop_target_bank", "D-580-3-1",
     (15,), range(25, 28),
     "Hitting the three targets closes their individual contacts. A single reset raises the bank. Completing the bank advances the multiplier and right spinner value."),
    ("ball-walker", "Ball walker and launcher", "other", "B-758",
     (9,), (39, 40),
     "One coil retracts a common bar, moving alternate pivoted fingers in the covered lane. The spring brings the entry finger fully up between strokes. Switch 39 closes on arrival and clears once the ball parks past the wireform. Two balls can remain staged between fingers. When qualified, the next ball initiates staged release via the left and right kickouts. Switch 40 is the separate release rollover used after qualification. With 35 open, the 65-second stock boot probe observed repeated right kickout, left kickout and walker commands with no coin or Start input. A bowed bar can trap the first finger halfway, causing an incoming ball to overshoot and eject back down the entrance."),
    ("first-stage", "First-stage Apollo kickout", "kicker", None, (20,), (15,),
     "The first stage holds the ball at the left kickout contact and propels it toward the next stage when the ROM drives the left kicker."),
    ("second-stage", "Second-stage Apollo kickout", "kicker", None, (17,), (16,),
     "The second stage holds the ball at the right kickout contact and propels it toward the upper arch when the ROM drives the right kicker."),
    ("outhole-serve", "Three-position out-hole and shooter feed", "kicker", None, (10,), (33, 34, 35),
     "The three switches report ball occupancy under the apron. With all three closed at power-up the stock ROM skips the recovery cycle. A common kicker serves one ball toward the shooter lane. Release the appropriate occupancy contact as the stack settles after each real serve. Surviving units show the shared feed effect with above-wood and below-wood serve actuator mountings."),
)
