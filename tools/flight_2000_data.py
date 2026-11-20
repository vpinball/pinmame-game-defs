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
    21: "Match feature", 22: "Right spinner lamp memory", 24: "Apollo 1 and 2 lamp startup",
    25: "Right chute pricing 1", 26: "Right chute pricing 2", 27: "Right chute pricing 3",
    28: "Right chute pricing 4", 29: "Special award limit", 30: "Bonus multiplier memory",
    31: "Special award type 1", 32: "Special award type 2",
}

# Printed load-list row numbers ordered by public lamp address. The specification
# gives one candidate row for each effect where the drawing and script disagree.
# A row claimed by both candidates is intentionally retained on both until traced.
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
    29: "The listed J2-30 pin cannot be traced on the drawing. The script and traced insert locate the Special lamp beside Spot BLAST.",
    37: "The harness list says J3-16 but calls the O insert a top rollover. The board draws an ambiguous duplicate pin number. The table places the O insert in the right outer return lane.",
    44: "The staged inserts are separate in the VPX script. The print repeats J2-5 for both Second Stage Go lamps; it also lists Q52's J3 branch as spinner 1,500.",
    46: "The staged inserts are separate in the VPX script. The print repeats J2-5 for both Second Stage Go lamps; it also lists Q52's J3 branch as spinner 1,500.",
    53: "The print repeats J3-4 for both T lamps. The VPX drives the upper rollover insert at 53 and the corner insert at 55.",
    55: "The print repeats J3-4 for both T lamps. The VPX drives the upper rollover insert at 53 and the corner insert at 55.",
    59: "The print joins the spinner 1,500 load to a Q52 branch also claimed by the two stage lamps. The table shows the spinner insert at this address.",
    60: "The print repeats J2-7 for both First Stage Go lamps. The VPX separately binds the top and center inserts at 60 and 62.",
    62: "The print repeats J2-7 for both First Stage Go lamps. The VPX separately binds the top and center inserts at 60 and 62.",
    63: "The board drawing labels two J2 endpoints 1. The load table says J2-1 and the VPX comments identify public 63 as Match.",
}
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
    "flightfp": "Free-play U5 and U6 replacements use the production U1, U2 and VSU-100 U9.",
    "flight2m": "Idleman 3335 modified rules CPU set. Production VSU-100 U9 speech ROM.",
    "flight2mb": "Idleman 3347 modified CPU and speech set. Install both U9 and U10 on a VSU-100 board with the documented two ROM positions. Upstream notes changes to multiball relocking, speech and gameplay.",
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
     "The upper-left channel banks up to three balls. The captive walker meters them and the launcher releases them toward the staged kickout lanes. The release rollover is separate from the launcher ball contact. The VPX uses three virtual kickers driven together, so it supplies neither the physical linkage dimensions nor release timing."),
    ("first-stage", "First-stage Apollo kickout", "kicker", None, (20,), (15,),
     "The first stage holds the ball at the left kickout contact and propels it toward the next stage when the ROM drives the left kicker."),
    ("second-stage", "Second-stage Apollo kickout", "kicker", None, (17,), (16,),
     "The second stage holds the ball at the right kickout contact and propels it toward the upper arch when the ROM drives the right kicker."),
    ("outhole-serve", "Three-position out-hole and shooter feed", "kicker", None, (10,), (33, 34, 35),
     "The three switches report remaining ball positions in the trough. A common kicker serves one ball toward the shooter lane. Surviving units show the serve actuator both above the wood under the apron and below the wood."),
)
