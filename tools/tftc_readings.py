"""Visually read DMD text from the retained Tales from the Crypt US 3.03 service-test frames.

Every string below was read by a curator from the retained 128x32 frames (rendered at 3x and checked
against the printed manual). The builder in ``build_tftc_runtime_evidence.py`` pairs each reading with the
frame's pixel digest from the retained raw run, so a changed frame no longer matches its reading. A reading
is a curator's transcription, not an OCR result.
"""
from __future__ import annotations

# Switch test: address -> (ROM name, row wire, column wire) as displayed under "-ACTIVE SWITCH TEST-".
# The ROM prints the column wire first ("GRN-BRN") and the row wire second ("WHT-BRN").
SWITCH_READINGS = {
    1: ("PLUMB TILT", "GRN-BRN", "WHT-BRN"), 2: ("4TH COIN", "GRN-BRN", "WHT-RED"),
    3: ("CREDIT BUTTON", "GRN-BRN", "WHT-ORN"), 4: ("RIGHT COIN", "GRN-BRN", "WHT-YEL"),
    5: ("CENTER COIN", "GRN-BRN", "WHT-GRN"), 6: ("LEFT COIN", "GRN-BRN", "WHT-BLU"),
    7: ("SLAM TILT", "GRN-BRN", "WHT-VIO"), 8: ("BUYIN BUTTON", "GRN-BRN", "WHT-GRY"),
    9: ("TROUGH #1 LEFT", "GRN-RED", "WHT-BRN"), 10: ("TROUGH #2 M-L-L", "GRN-RED", "WHT-RED"),
    11: ("TROUGH #3 MID LFT", "GRN-RED", "WHT-ORN"), 12: ("TROUGH #4 MIDDLE", "GRN-RED", "WHT-YEL"),
    13: ("TROUGH #5 MID RGT", "GRN-RED", "WHT-GRN"), 14: ("TROUGH #6 M-R-R", "GRN-RED", "WHT-BLU"),
    15: ("TROUGH #7 RIGHT", "GRN-RED", "WHT-VIO"), 16: ("SHOOTER LANE", "GRN-RED", "WHT-GRY"),
    17: ("LEFT OUTLANE", "GRN-ORN", "WHT-BRN"), 18: ("LEFT RETURN", "GRN-ORN", "WHT-RED"),
    19: ("LEFT SLINGSHOT", "GRN-ORN", "WHT-ORN"), 20: ("LEFT 3 BANK BOTTOM", "GRN-ORN", "WHT-YEL"),
    21: ("LEFT 3 BANK MIDDLE", "GRN-ORN", "WHT-GRN"), 22: ("LEFT 3 BANK TOP", "GRN-ORN", "WHT-BLU"),
    23: ("LEFT BOTTOM ORBIT", "GRN-ORN", "WHT-VIO"), 24: ("LEFT TOP ORBIT", "GRN-ORN", "WHT-GRY"),
    25: ("RIGHT OUTLANE", "GRN-YEL", "WHT-BRN"), 26: ("RIGHT RETURN", "GRN-YEL", "WHT-RED"),
    27: ("RIGHT SLINGSHOT", "GRN-YEL", "WHT-ORN"), 28: ("RIGHT 3 BANK BOTTOM", "GRN-YEL", "WHT-YEL"),
    29: ("RIGHT 3 BANK MIDDLE", "GRN-YEL", "WHT-GRN"), 30: ("RIGHT 3 BANK TOP", "GRN-YEL", "WHT-BLU"),
    31: ("RIGHT BOTTOM ORBIT", "GRN-YEL", "WHT-VIO"), 32: ("RIGHT TOP ORBIT", "GRN-YEL", "WHT-GRY"),
    33: ("UP/DWN BAR - UP", "GRN-BLK", "WHT-BRN"), 34: ("NOT USED", "GRN-BLK", "WHT-RED"),
    35: ("NOT USED", "GRN-BLK", "WHT-ORN"), 36: ("UP/DWN BAR - DOWN", "GRN-BLK", "WHT-YEL"),
    37: ("TOMB STONE", "GRN-BLK", "WHT-GRN"), 38: ("CRYPT VUK (LEFT)", "GRN-BLK", "WHT-BLU"),
    39: ("CAPTIVE BALL", "GRN-BLK", "WHT-VIO"), 40: ("LEFT SPINNER", "GRN-BLK", "WHT-GRY"),
    41: ("DROP TARGET - LEFT", "GRN-BLU", "WHT-BRN"), 42: ("DROP TARGET - MIDDLE", "GRN-BLU", "WHT-RED"),
    43: ("DROP TARGET - RIGHT", "GRN-BLU", "WHT-ORN"), 44: ("LEFT RAMP ENTER", "GRN-BLU", "WHT-YEL"),
    45: ("LEFT RAMP MIDDLE", "GRN-BLU", "WHT-GRN"), 46: ("RIGHT RAMP ENTER", "GRN-BLU", "WHT-BLU"),
    47: ("RIGHT RAMP EXIT", "GRN-BLU", "WHT-VIO"), 48: ("RIGHT SPINNER", "GRN-BLU", "WHT-GRY"),
    49: ("LEFT TURBO BUMPER", "GRN-VIO", "WHT-BRN"), 50: ("BOTTOM TURBO BUMPER", "GRN-VIO", "WHT-RED"),
    51: ("RIGHT TURBO BUMPER", "GRN-VIO", "WHT-ORN"), 52: ("RIGHT SUPER VUK", "GRN-VIO", "WHT-YEL"),
    53: ("SMALL TROUGH", "GRN-VIO", "WHT-GRN"), 54: ("LARGE TROUGH", "GRN-VIO", "WHT-BLU"),
    55: ("POWER SCOOP", "GRN-VIO", "WHT-VIO"), 56: ("MIDDLE SPINNER", "GRN-VIO", "WHT-GRY"),
    57: ("LEFT RAMP EXIT", "GRN-GRY", "WHT-BRN"), 58: ("NOT USED", "GRN-GRY", "WHT-RED"),
    59: ("NOT USED", "GRN-GRY", "WHT-ORN"), 60: ("NOT USED", "GRN-GRY", "WHT-YEL"),
    61: ("NOT USED", "GRN-GRY", "WHT-GRN"), 62: ("LAUNCH BUTTON", "GRN-GRY", "WHT-BLU"),
    63: ("LEFT FLIPPER", "GRN-GRY", "WHT-VIO"), 64: ("RIGHT FLIPPER", "GRN-GRY", "WHT-GRY"),
}
# Flipper column: public 82 and 84 show the flipper switches; 81, 83 and 85-88 show NONE.
FLIPPER_COLUMN_READINGS = {
    81: None, 82: (64, "RIGHT FLIPPER"), 83: None, 84: (63, "LEFT FLIPPER"),
    85: None, 86: None, 87: None, 88: None,
}

# Lamp test: address -> (ROM name, column wire, row wire) under "-LAMP TEST-".
LAMP_READINGS = {
    64: ("EXTRA BALL", "YEL-GRY", "RED-GRY"), 63: ("RIGHT RAMP ENTER", "YEL-GRY", "RED-VIO"),
    62: ("LEFT RAMP ENTER", "YEL-GRY", "RED-BLU"), 61: ("CRYPT M-BALL ARROW", "YEL-GRY", "RED-GRN"),
    60: ("JACKPOT", "YEL-GRY", "RED-YEL"), 59: ("RIGHT TURBO BUMPER", "YEL-GRY", "RED-ORN"),
    58: ("BOTTOM TURBO BUMPER", "YEL-GRY", "RED-BLK"), 57: ("LEFT TURBO BUMPER", "YEL-GRY", "RED-BRN"),
    56: ("RIGHT RAMP - TOP/LT", "YEL-VIO", "RED-GRY"), 55: ("RIGHT RAMP - BOT/LT", "YEL-VIO", "RED-VIO"),
    54: ("RIGHT RAMP - BOT/RT", "YEL-VIO", "RED-BLU"), 53: ("RIGHT RAMP - TOP/RT", "YEL-VIO", "RED-GRN"),
    52: ("DOUBLE JACKPOT", "YEL-VIO", "RED-YEL"), 51: ("DROPS - LOWER RIGHT", "YEL-VIO", "RED-ORN"),
    50: ("DROPS - LOWER MID", "YEL-VIO", "RED-BLK"), 49: ("DROPS - LOWER LEFT", "YEL-VIO", "RED-BRN"),
    48: ('CRYPT #1 - "C"', "YEL-BLU", "RED-GRY"), 47: ('CRYPT #2 - "R"', "YEL-BLU", "RED-VIO"),
    46: ('CRYPT #3 - "Y"', "YEL-BLU", "RED-BLU"), 45: ('CRYPT #4 - "P"', "YEL-BLU", "RED-GRN"),
    44: ('CRYPT #5 - "T"', "YEL-BLU", "RED-YEL"), 43: ("DROPS - UPPER RIGHT", "YEL-BLU", "RED-ORN"),
    42: ("DROPS - UPPER MIDDLE", "YEL-BLU", "RED-BLK"), 41: ("DROPS - UPPER LEFT", "YEL-BLU", "RED-BRN"),
    40: ("LEFT RAMP - TOP/LT", "YEL-GRN", "RED-GRY"), 39: ("LEFT RAMP - BOT/LT", "YEL-GRN", "RED-VIO"),
    38: ("LEFT RAMP - BOT/RT", "YEL-GRN", "RED-BLU"), 37: ("LEFT RAMP - TOP/RT", "YEL-GRN", "RED-GRN"),
    36: ("RIGHT SPINNER BOTTOM", "YEL-GRN", "RED-YEL"), 35: ("RIGHT SPINNER MIDDLE", "YEL-GRN", "RED-ORN"),
    34: ("RIGHT SPINNER TOP", "YEL-GRN", "RED-BLK"), 33: ("LEFT SPINNER BOTTOM", "YEL-GRN", "RED-BRN"),
    32: ("LEFT SPINNER MIDDLE", "YEL-BLK", "RED-GRY"), 31: ("LEFT SPINNER TOP", "YEL-BLK", "RED-VIO"),
    30: ("RIGHT 3 BANK TOP", "YEL-BLK", "RED-BLU"), 29: ("RIGHT 3 BANK MIDDLE", "YEL-BLK", "RED-GRN"),
    28: ("RIGHT 3 BANK BOTTOM", "YEL-BLK", "RED-YEL"), 27: ("CLONE", "YEL-BLK", "RED-ORN"),
    26: ("RETURN LANES X2", "YEL-BLK", "RED-BLK"), 25: ("MIDDLE SPINNER M-BALL", "YEL-BLK", "RED-BRN"),
    24: ("MONSTER JACKPOT", "YEL-ORN", "RED-GRY"), 23: ("COLLECT CREATURE FTR.", "YEL-ORN", "RED-VIO"),
    22: ("LEFT 3 BANK TOP", "YEL-ORN", "RED-BLU"), 21: ("LEFT 3 BANK MIDDLE", "YEL-ORN", "RED-GRN"),
    20: ("LEFT 3 BANK BOTTOM", "YEL-ORN", "RED-YEL"), 19: ("SKULL CRACKIN", "YEL-ORN", "RED-ORN"),
    18: ("MIDDLE SPINNER TOP", "YEL-ORN", "RED-BLK"), 17: ("OUTLANES X2", "YEL-ORN", "RED-BRN"),
    16: ("CREDIT BUTTON", "YEL-RED", "RED-GRY"), 15: ("LAUNCH BUTTON", "YEL-RED", "RED-VIO"),
    14: ("BUYIN BUTTON", "YEL-RED", "RED-BLU"), 13: ("LEFT SCOOP", "YEL-RED", "RED-GRN"),
    12: ("WHEEL - #12", "YEL-RED", "RED-YEL"), 11: ("WHEEL - #11", "YEL-RED", "RED-ORN"),
    10: ("WHEEL - #10", "YEL-RED", "RED-BLK"), 9: ("WHEEL - #9", "YEL-RED", "RED-BRN"),
    8: ("WHEEL - #8", "YEL-BRN", "RED-GRY"), 7: ("WHEEL - #7", "YEL-BRN", "RED-VIO"),
    6: ("WHEEL - #6", "YEL-BRN", "RED-BLU"), 5: ("WHEEL - #5", "YEL-BRN", "RED-GRN"),
    4: ("WHEEL - #4", "YEL-BRN", "RED-YEL"), 3: ("WHEEL - #3", "YEL-BRN", "RED-ORN"),
    2: ("WHEEL - #2", "YEL-BRN", "RED-BLK"), 1: ("WHEEL - #1", "YEL-BRN", "RED-BRN"),
}

# Cycling Coils: public solenoid -> ROM text under "-CYCLING COILS-". Flash-lamp steps print "FL:" with
# the bulb composition; the Left/Right relay (public 10) fires with each of them and has no step of its own.
COIL_READINGS = {
    1: "COIL: LOCK OUT", 2: "COIL: BALL RELEASE", 3: "COIL: AUTO LAUNCH 50V", 4: "COIL: DROP TARGET",
    5: "COIL: SCOOP", 6: "COIL: LEFT VUK 50V", 7: "COIL: TOP VUK 50V", 8: "COIL: KNOCKER",
    9: "COIL: DIVERTER", 11: "RELAY: G.I. RELAY", 12: "COIL: NOT USED", 13: "COIL: NOT USED",
    14: "COIL: NOT USED", 15: "COIL: MOTOR UP/DWN", 16: "COIL: SHAKER MOTOR", 17: "COIL: LEFT TURBO",
    18: "COIL: BOTTOM TURBO", 19: "COIL: RIGHT TURBO", 20: "COIL: LEFT SLING", 21: "COIL: RIGHT SLING",
    22: "COIL: LASER KICK 50V",
}
FLASHER_READINGS = {
    25: "FL: 1-INS 2-PLFD 1-BP", 26: "FL: 1-INS 3-PLFD", 27: "FL: 2-INS 2-PLFD", 28: "FL: 1-INS 2-PLFD 1-BP",
    29: "FL: 1-INS 3-PLFD", 30: "FL: 1-INS 2-PLFD 1-BP", 31: "FL: 3-PLFD 1-BP", 32: "FL: 1-INS 2-PLFD 1-BP",
}
