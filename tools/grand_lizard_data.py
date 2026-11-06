"""Reviewed literal Grand Lizard tables; source spellings remain in the excerpts."""

SWITCH_LABELS = [
    "Plumb Bob Tilt", "Ball Roll Tilt", "Credit Button", "Right Coin Chute", "Center Coin Chute", "Left Coin Chute", "Slam Tilt", "High Score Reset",
    "Playfield Tilt", "Outhole", "Ball Shooter Lane", "Ball Trough 1 (Lower Right)", "Ball Trough 2 (Center)", "Ball Trough 3 (Upper Left)", "Turnaround", "Left Return Lane",
    "Right Return Lane", "Left Outlane", "Right Outlane", "4-Bank Left Target 1", "4-Bank Left Target 2", "4-Bank Right Target 1", "4-Bank Right Target 2", "Top Right Stationary Target",
    "3-Bank Target 1", "3-Bank Target 2", "3-Bank Target 3", "Spinner", "Right Ramp", "Right Chute to Top", "Left Ramp", "Multi-Ball 1",
    "Multi-Ball 2", "Multi-Ball 3", "L Stationary Target", "I Stationary Target", "Z Stationary Target", "A Stationary Target", "R Stationary Target", "D Stationary Target",
    "Right Special Arrow", "Ramp Tongue", "Left Kicker (Scoring)", "Right Kicker (Scoring)", "Left Magnet Button", "Right Magnet Button", "Not Used", "Right Flipper Lane Change",
] + ["Not Used"] * 16
SWITCH_PARTS = [
    "A-8476", "B-6572", "SW-1A-126", "904845", "904845", "904845", "904704", "5641-09369-00",
    "SW-1A-117", "17-1067", "SW-1A-138", "5647-09957-00", "5647-09957-00", "5647-09633-00", "SW-1A-124", "SW-1A-124",
    "SW-1A-124", "SW-1A-124", "SW-1A-124", "17-1042", "17-1042", "17-1042", "17-1042", "A-9268",
    "17-1042", "17-1042", "17-1042", "SW-1A-118", "SW-1A-118", "SW-1A-118", "SW-1A-118", "17-1082",
    "5647-09957-00", "17-1075", "A-9270", "A-9270", "A-9270", "A-9268", "A-9268", "A-9268",
    "A-9268", "5647-09633-00", "SW-1A-122", "SW-1A-122", "SW-1A-126", "SW-1A-126", None, "SW-1A-150",
] + [None] * 16
SWITCH_COLUMNS = [
    ("GRN-BRN", "1J8-1", "Q45"), ("GRN-RED", "1J8-2", "Q49"), ("GRN-ORN", "1J8-3", "Q44"), ("GRN-YEL", "1J8-4", "Q48"),
    ("GRN-BLK", "1J8-5", "Q43"), ("GRN-BLU", "1J8-7", "Q47"), ("GRN-VIO", "1J8-8", "Q42"), ("GRN-GRY", "1J8-9", "Q46"),
]
SWITCH_ROWS = [("WHT-BRN", "1J10-9"), ("WHT-RED", "1J10-8"), ("WHT-ORN", "1J10-7"), ("WHT-YEL", "1J10-6"), ("WHT-GRN", "1J10-5"), ("WHT-BLU", "1J10-3"), ("WHT-VIO", "1J10-2"), ("WHT-GRY", "1J10-1")]
LAMP_LABELS = [
    "Game Over (Backglass)", "Match (Backglass)", "Sword 1 (Backglass)", "Sword 2 (Backglass)", "Ball In Play (Backglass)", "Shoot Again (Backglass)", "2X", "3X",
    "4X", "5X", "10X", "Shoot Again (Playfield)", "Bonus 1", "Bonus 2", "Bonus 3", "Bonus 4",
    "Bonus 5", "Bonus 6", "Bonus 7", "Bonus 8", "Bonus 9", "Bonus 10", "Bonus 20", "Extra Ball (Bottom)",
    "All Scores 2X", "All Scores 3X", "Bonus Holdover Collected", "Spinner", "Right Ramp B", "Lane to Top Bonus Holdover Arrow", "Left Ramp A", "Multi-Ball Arrow (Lower)",
    "Multi-Ball Arrow (Middle)", "Multi-Ball Arrow (Upper)", "L", "I", "Z", "A", "R", "D",
    "Special (Bottom Right Stationary Target)", "Left Magnet (Lower)", "Left Magnet (Middle)", "Left Magnet (Upper)", "Right Magnet (Lower)", "Right Magnet (Middle)", "Right Magnet (Upper)", "Right Ramp Mystery",
    "Left Drain", "Right Drain", "Not Used", "Left Ramp Mystery", "Extra Ball (Top)", "Turn 10K", "Turn 20K", "Turn 40K",
    "4-Bank 20K", "4-Bank 40K", "4-Bank 60K", "4-Bank 80K", "4-Bank 100K", "Top Right 50K", "Top Right Release", "3-Bank Special",
]
LAMP_COLUMNS = [(wire, f"1J7-{pin}", f"Q{q}") for wire, pin, q in [
    ("YEL-BRN", 1, 66), ("YEL-RED", 2, 64), ("YEL-ORN", 3, 62), ("YEL-BLK", 4, 60), ("YEL-GRN", 6, 58), ("YEL-BLU", 7, 56), ("YEL-VIO", 8, 54), ("YEL-GRY", 9, 52)]]
LAMP_ROWS = [(wire, f"1J6-{pin}", f"Q{q}") for wire, pin, q in [
    ("RED-BRN", 1, 80), ("RED-BLK", 2, 81), ("RED-ORN", 3, 82), ("RED-YEL", 5, 83), ("RED-GRN", 6, 84), ("RED-BLU", 7, 85), ("RED-VIO", 8, 86), ("RED-GRY", 9, 87)]]

# Public address, semantic label, kind, wire, CPU plug, harness plug, transistor, part.
SOLENOIDS = [
    (1, "Trough Kicker (Outhole)", "coil", "GRY-BRN", "1P11-1", "8P3-1", "Q33", "AE-23-800-01"),
    (2, "3-Bank Raise", "coil", "GRY-RED", "1P11-3", "8P3-2", "Q25", "AE-23-800-04"),
    (3, "4-Bank Raise 1 (Left Two Targets)", "coil", "GRY-ORN", "1P11-4", "8P3-3", "Q32", "AE-23-800-04"),
    (4, "4-Bank Raise 2 (Right Two Targets)", "coil", "GRY-YEL", "1P11-5", "8P3-4", "Q24", "AE-23-800-04"),
    (5, "Lockup Eject (Multi-Ball)", "coil", "GRY-GRN", "1P11-6", "8P3-5", "Q31", "AE-23-800-03"),
    (6, "Lockup Flasher", "flasher", "GRY-BLU", "1P11-7", "8P3-6", "Q23", "#63 flashlamps"),
    (7, "Left Magnet Flasher", "flasher", "GRY-VIO", "1P11-8", "8P3-7", "Q30", "#63 flashlamps"),
    (8, "Ball Feed", "coil", "GRY-BLK", "1P11-9", "8P3-8", "Q22", "AE-23-800-03"),
    (9, "Left Magna-Save Magnet Relay", "relay", "BRN-BLK", "1P12-1", "8P3-9", "Q17", "5580-09613-00"),
    (10, "Right Magna-Save Magnet Relay", "relay", "BRN-RED", "1P12-2", "8P3-10", "Q9", "5580-09613-00"),
    (11, "Backbox and Cabinet General Illumination", "gi", "BRN-ORN", "1P12-4", "3P7-1", "Q16", "5580-09555-00"),
    (12, "3-Bank Flasher", "flasher", "BRN-YEL", "1P12-5", "8P3-12", "Q8", "#63 flashlamps"),
    (13, "Eyes (Backbox and Head)", "flasher", "BRN-GRN", "1P12-6", "8P3-13, 9P1-13", "Q15", "#63 flashlamps"),
    (14, "Credit Knocker (or Token Dispenser)", "coil", "BRN-BLU", "1P12-7", "Backbox", "Q7", "AE-23-800-02"),
    (15, "Bell", "coil", "BRN-VIO", "1P12-8", "7P1-17", "Q14", "SM-29-1000-DC"),
    (16, "Coin-Lockout Relay", "relay", "BRN-GRY", "1P12-9", "7P1-18, 7P4-4", "Q6", "404603-2"),
    (17, "Left Kicker (Slingshot)", "coil", "BLU-BRN", "1P19-7", "8P3-17", "Q75", "AE-23-800-03"),
    (18, "Right Kicker (Slingshot)", "coil", "BLU-RED", "1P19-4", "8P3-18", "Q71", "AE-23-800-03"),
    (19, "Right Magnet Flasher", "flasher", "BLU-ORN", "1P19-3", "8P3-19", "Q73", "#63 flashlamps"),
]

TABLES = [
    {"build": "build-01", "directory": "williams/grand-lizard-1986/build-01-grand-lizard-williams-1986", "filename": "Grand Lizard (Williams 1986).vpx", "sha256": "eba3f271bd338801d9307841618ca2d9a03da230b2bc8a914eb7e528efd87f4e", "script_sha256": "13576dd5caaf0e356d8a752ca055a0b35c57caaf0417a7bd4e283899fda4af35", "manifest_sha256": "cd6f24f1124565013850ddeb209edbbf8c8af7aa34c9b5280b01e00e3b48708a", "file_count": 940, "total_bytes": 296811871},
    {"build": "build-02", "directory": "williams/grand-lizard-1986/build-02-grandlizard-v1.5", "filename": "GrandLizardV1.5.vpx", "sha256": "a1ff6ed01846b3e35bbde887d1e54ce9e546686cfd7d854c405ac3da4ec85d2f", "script_sha256": "a897397da209f0cfcaf47a8a852f080d0f1473ea213381a715aaf6c920e2f326", "manifest_sha256": "75d894c1f17699fcb2e435af8c1db5d34579f5e86c689285f9e5dca86ed81e22", "file_count": 978, "total_bytes": 255493870},
]
