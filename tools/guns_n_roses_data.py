"""Visually checked factory chart transcriptions for Data East Guns N' Roses.

Names retain the chart's spelling; tuple order is public sequential/column-major
address order. None of these tables is inherited from another machine.
"""

SWITCH_NAMES = (
    'Plumb Tilt', '4th Coin', 'Credit Button', 'Right Coin', 'Center Coin',
    'Left Coin', 'Slam Tilt', 'Extra Ball Button',
    '#1 (Left) Ball Trough', '#2 Ball Trough', '#3 Ball Trough', '#4 Ball Trough',
    '#5 Ball Trough', '#6 Ball Trough', '#7 (Right) Ball Trough', 'Shooter Lane',
    'Captive Stand-Up "D" of DUFF', 'Captive Stand-Up "U" of DUFF',
    'Captive Stand-Up "F" of DUFF', 'Captive Stand-Up "F" of DUFF',
    '"J" of JAM Top Lane Left', '"A" of JAM Top Lane Middle',
    '"M" of JAM Top Lane Right', 'Left Shooter Lane',
    'Left Turbo Bumper', 'Bottom Turbo Bumper', 'Right Turbo Bumper',
    'Right Slingshot', 'Left Slingshot', 'Top Slingshot', 'Not Used', 'Not Used',
    'Left Drop Target Bottom', 'Left Drop Target Middle',
    'Right Drop Target Middle', 'Right Drop Target Bottom', 'Eject',
    'Center Scoop', 'VUK', 'Funnel Snake Pit', 'Not Used', 'Not Used',
    'Not Used', 'Not Used', 'Not Used', 'Not Used', 'Not Used',
    'Inner Orbit Bottom', '"R" Ramp Enter', '"R" Ramp Exit',
    '"G" Ramp Enter', '"G" Ramp Exit', 'Left Return Lane', 'Left Outlane',
    'Right Outlane', 'Right Return Lane', 'Right Drop Target Top',
    'Right Orbit Top', 'Left Drop Target Top', 'Left Orbit Top', 'Not Used',
    'Gun Trigger', 'Left Flipper Upr./Lwr.', 'Right Flipper Lower',
)

SWITCH_PARTS = (
    'See Cabinet', '---', '500-5097-02', '180-5024-00', '180-5024-00',
    '180-5024-00', '180-5022-00', '180-5073-00',
    *(['180-5119-00'] * 6), '180-5118-00', '180-5100-01',
    *(['515-5470-08'] * 4), *(['500-5707-00'] * 3), '180-5700-00',
    *(['180-5015-01'] * 3), *(['180-5054-00'] * 3), '--- ---', '--- ---',
    *(['180-5092-01'] * 4), '180-5027-01', '180-5057-00', '180-5116-00',
    '515-6073-00', *(['--- ---'] * 7), '500-5706-00',
    *(['180-5090-00'] * 4), *(['500-5707-00'] * 3), '500-5706-00',
    '180-5092-01', '500-5706-00', '180-5092-01', '500-5706-00',
    '--- ---', '180-5093-00', '180-5124-00', '180-5124-00',
)

# Literal chart headings: drive wire, connector, transistor; return wire, connector.
SWITCH_COLUMNS = (
    ('GRN-BRN', 'CN8-1', 'Q55'), ('GRN-RED', 'CN8-2', 'Q54'),
    ('GRN-ORN', 'CN8-3', 'Q53'), ('GRN-YEL', 'CN8-4', 'Q52'),
    ('GRN-BLK', 'CN8-5', 'Q51'), ('GRN-BLU', 'CN8-7', 'Q50'),
    ('GRN-VIO', 'CN8-8', 'Q49'), ('GRN-GRY', 'CN8-9', 'Q48'),
)
SWITCH_ROWS = tuple(zip(
    ('WHT-BRN', 'WHT-RED', 'WHT-ORN', 'WHT-YEL', 'WHT-GRN', 'WHT-BLU', 'WHT-VIO', 'WHT-GRY'),
    ('CN10-9', 'CN10-8', 'CN10-7', 'CN10-6', 'CN10-5', 'CN10-3', 'CN10-2', 'CN10-1'),
))

LAMP_NAMES = (
    'Cross Grid Top "Dizzy"', '"R" of ROCK', '"O" of ROCK', '"C" of ROCK',
    '"K" of ROCK', 'COMA', 'Multi-Ball Ready', 'Add Band Members',
    'Same Player Shoots Again', 'Cross Grid Left "Matt"', 'Double Mode',
    '"R" of ROSES', '"O" of ROSES', '1st "S" of ROSES', '"E" of ROSES', '2nd "S" of ROSES',
    'Left Outlane Patience', 'Left Return Lite Rock', 'Cross Grid Upr. Center "Axl"',
    '"G" of GUNS', '"U" of GUNS', '"N" of GUNS', '"S" of GUNS', '"N" of G... N\' R...',
    'Right Outlane Michelle', 'Right Return Lite Guitar', 'Captive Ball',
    'Cross Grid Right "Duff"', '"D" of DUFF', '"U" of DUFF', '1st "F" of DUFF', '2nd "F" of DUFF',
    '"R" Ramp Rose Millions', '"R" Ramp Jackpot', '"R" Ramp Enter', 'Magnets ON',
    'Cross Grid Lwr. Center "Slash"', '"G" Ramp Gun Millions', '"G" Ramp Jackpots', '"G" Ramp Enter',
    'Riot Ball', 'Axl 3-Ball', 'Dizzy Ball', 'Duff Rocks', 'Super Snake Pit',
    'Cross Grid Bottom "Gilby"', 'RIOT Jackpot', 'Super Jackpot', 'Matt Scoring',
    'Slash Solo', 'Lite COMA', 'Gilby Rolls', 'Extra Ball', 'Mystery Scoop',
    'Left Shooter Left Ramp', 'Roll', 'Left Top Lane "J" of JAM',
    'Middle Top Lane "A" of JAM', 'Right Top Lane "M" of JAM', 'Back Stage Pass',
    'Slash', 'Right Shooter Lane', 'Extra-Ball Button', 'Credit',
)
LAMP_COLUMNS = (
    ('YEL-BRN', 'CN7-1', 'Q71'), ('YEL-RED', 'CN7-2', 'Q70'),
    ('YEL-ORN', 'CN7-3', 'Q69'), ('YEL-BLK', 'CN7-4', 'Q68'),
    ('YEL-GRN', 'CN7-6', 'Q67'), ('YEL-BLU', 'CN7-7', 'Q66'),
    ('YEL-VIO', 'CN7-8', 'Q65'), ('YEL-GRY', 'CN7-9', 'Q64'),
)
LAMP_ROWS = tuple(zip(
    ('RED-BRN', 'RED-BLK', 'RED-ORN', 'RED-YEL', 'RED-GRN', 'RED-BLU', 'RED-VIO', 'RED-GRY'),
    ('CN6-1', 'CN6-2', 'CN6-3', 'CN6-5', 'CN6-6', 'CN6-7', 'CN6-8', 'CN6-9'),
    ('Q72', 'Q73', 'Q74', 'Q75', 'Q76', 'Q77', 'Q78', 'Q79'),
))

# Printed page 37/PDF 41. No pin, transistor or wire is filled from a pattern.
# no, name, DT, board, control wire, control connection, power wire,
# power connection, voltage description, coil/flash type.
COIL_CHART = (
    ('1L', '6-Ball Assembly Lockout', 'Q46', 'CPU', 'VIO-BRN', 'PPB J2-1', 'BRN', 'PPB J6-1,2', '32V L', '25-1240'),
    ('1R', 'Back Pnl-P/F LT/RT Corners Flash; X2 Backpanel, X2 P/F', 'Q46', 'CPU', 'BLK-BRN', 'PPB J9-1', 'ORG', 'PPB J6-4,5', '32V R', 'Bulb #89'),
    ('2L', 'Ball Release (Eject)', 'Q45', 'CPU', 'VIO-RED', 'PPB J2-2', 'BRN', 'PPB J6-1,2', '32V L', '23-800'),
    ('2R', 'Right Playfield Flash; X2 P/F, Insert X2', 'Q45', 'CPU', 'BLK-RED', 'PPB J9-2', 'ORG', 'PPB J6-4,5', '32V R', 'Bulb #89'),
    ('3L', 'Auto Ball Launch 50v', 'Q5', 'PPB', 'VIO-ORG', 'PPB J8-2', 'YEL/VIO', 'PPB J7-8', '50v L', '22-600'),
    ('3R', 'Left Playfield Flash; X2 P/F, Insert X2', 'Q44', 'CPU', 'BLK-ORG', 'PPB J9-3', 'ORG', 'PPB J6-4,5', '32V R', 'Bulb #89'),
    ('4L', 'Kicker, Eject', 'Q43', 'CPU', 'VIO-YEL', 'PPB J2-4', 'BRN', 'PPB J6-1,2', '32V L', '24-940'),
    ('4R', '"C"aptive Ball Flash; X2 P/F, Insert X2', 'Q43', 'CPU', 'BLK-YEL', 'PPB J9-4', 'ORG', 'PPB J6-4,5', '32V R', 'Bulb #89'),
    ('5L', 'VUK 50v', 'Q4', 'PPB', 'VIO-GRN', 'PPB J8-4', 'YEL/VIO', 'PPB J7-8', '50v L', '23-800'),
    ('5R', '"R" Ramp Enter Flash; X1 P/F, Insert X3', 'Q42', 'CPU', 'BLK-GRN', 'PPB J9-5', 'ORG', 'PPB J6-4,5', '32V R', 'Bulb #89'),
    ('6L', 'Kick Big/Scoop 50v', 'Q3', 'PPB', 'VIO-BLU', 'PPB J8-7', 'YEL/VIO', 'PPB J7-8', '50v L', '23-800'),
    ('6R', '"G" Ramp Enter Flash; X1 P/F, Insert X3', 'Q41', 'CPU', 'BLK-BLU', 'PPB J9-6', 'ORG', 'PPB J6-4,5', '32V R', 'Bulb #89'),
    ('7L', 'Ramp Trap Door', 'Q40', 'CPU', 'VIO-BLK', 'PPB J2-8', 'BRN', 'PPB J6-1,2', '32V L', '28-1050'),
    ('7R', 'Under "R" Ramp Flash; X2 P/F, Insert X2', 'Q40', 'CPU', 'BLK-VIO', 'PPB J9-7', 'ORG', 'PPB J6-4,5', '32V R', 'Bulb #89'),
    ('8L', 'Knocker (In Cabinet)', 'Q39', 'CPU', 'VIO-GRY', 'PPB J2-8', 'BRN', 'PPB J6-1,2', '32V L', '23-800'),
    ('8R', 'Under "G" Ramp Flash; X2 P/F, Insert X2', 'Q39', 'CPU', 'BLK-GRY', 'PPB J9-8', 'ORG', 'PPB J6-4,5', '32V R', 'Bulb #89'),
    ('09', 'Right 3-Bank Drop Target', 'Q30', 'CPU', 'BRN-BLK', 'CPU CN12-1', 'RED', 'PS CN3-6,7', '32v', '23-800'),
    ('10', 'Left & Right Relay; Located on PPB In Backbox', 'Q29', 'CPU', 'BLK-RED', 'CPU CN12-5', 'RED', 'PS CN6-7', '32v', '24v DC 10A DPDT'),
    ('11', 'G.I. Relay; Located on Power Supply Bd.', 'Q28', 'CPU', 'BRN-ORG', 'CPU CN12-4', 'RED', 'PS CN3-6,7', '32v', '24v DC 10A DPDT'),
    ('12', 'Left 3-Bank Drop Target', 'Q27', 'CPU', 'BRN-YEL', 'CPU CN12-5', 'RED', 'PS CN3-6,7', '32v', '23-800'),
    ('13', 'Not Used', '---', '---', '---', '---', '---', '---', '---', '---'),
    ('14', 'Laser Kick 50v', 'Q2', 'PPB', 'BRN-BLU', 'PPB J8-8', 'VIO-YEL', 'PPB J7-2', '50v', '23-800'),
    ('15', 'Not Used', '---', '---', '---', '---', '---', '---', '---', '---'),
    ('16', 'Not Used', '---', '---', '---', '---', '---', '---', '---', '---'),
    ('17', 'Left Turbo Bumper', 'Q11', 'CPU', 'BLU-BRN', 'CPU CN19-7', 'RED', 'PS CN3-6', '32v', '23-800'),
    ('18', 'Bottom Turbo Bumper', 'Q9', 'CPU', 'BLU-RED', 'CPU CN19-4', 'RED', 'PS CN3-6', '32v', '23-800'),
    ('19', 'Right Turbo Bumper', 'Q8', 'CPU', 'BLU-ORG', 'CPU CN19-3', 'RED', 'PS CN3-6', '32v', '23-800'),
    ('20', 'Left Slingshot', 'Q10', 'CPU', 'BLU-YEL', 'CPU CN19-6', 'RED', 'PS CN3-6', '32v', '23-800'),
    ('21', 'Right Slingshot', 'Q12', 'CPU', 'BLU-GRN', 'CPU CN19-8', 'RED', 'PS CN3-6', '32v', '23-800'),
    ('22', 'Top Slingshot', 'Q13', 'CPU', 'BLU-BLK', 'CPU CN19-9', 'RED', 'PS CN3-6', '32v', '23-800'),
)

FLIPPER_CHART = (
    ('Lwr. Rt. Flipper', '22-1080', 'BLU-VIO / SSFB CN1-7', 'GRN-GRY / CPU CN8-9 / SSFB CN1-4', 'WHT-GRY / CPU CN10-1 / SSFB CN1-3', 'BRN-VIO / Rt. EOS SW. to CN1-1', 'BLK / CPU CN5 to CN1-6', 'BLK-WHT / PPB J7-1,5 to SSFB CN2-8,-9', 'GRY-GRN-GRY / P/S CN1-10,-11 to SSFB CN2-7,-8', '50v Q2,Q3 CN2-7,8; 8vAC SR1', 'BLU/YEL ORG/VIO'),
    ('Lwr. Lt. Flipper', '22-1080', 'BLU-GRY / SSFB CN1-11', 'GRN-GRY / CPU CN8-9 / SSFB CN1-4', 'WHT-VIO / CPU CN10-2 / SSFB CN1-5', 'BRN-GRY / Lt. EOS SW. to CN1-9', 'BLK / CPU CN5 to CN1-6', 'BLK-WHT / PPB J7-1,5 to SSFB CN2-8,-9', 'GRY-GRN-GRY / P/S CN1-10,-11 to SSFB CN2-7,-8', '50v Q10,Q9 CN2-4,5; 8vAC SR2', 'GRY/YEL ORG/GRY'),
    ('Upr. Lt. Flipper', '25-1100', 'GRY-VIO / SSFB CN1-12', 'GRN-GRY / CPU CN8-9 / SSFB CN1-4', 'WHT-VIO / CPU CN10-2 / SSFB CN1-10', 'Not Used', 'BLK / CPU CN5 to CN1-6', 'BLK-WHT / PPB J7-1,5 to SSFB CN2-8,-9', 'GRY-GRN-GRY / P/S CN1-10,-11 to SSFB CN2-7,-8', '50v Q16,Q15 CN2-1,2; 8vAC SR3', 'BLU/YEL ORG/GRY'),
)

# Complete regions, including generic/unused parts: do not collapse a BOM to
# only the part used by the definition. Dashes and duplicated item numbers are
# retained. Visually checked against the native-DPI full-page renders.
ASSEMBLY_TABLES = {
    52: """PLAYFIELD - LAMPS WITH SOCKETS
Item | Description (1 bulb per socket) | Qty. | Part No.
A | #44 Bulb | 91 | 165-5000-44
1A | 2-Lug Staple Down Socket | 68 | 077-5000-00
2A | 2-Lug Stand-Up Short Socket | 0 | 077-5002-00
3A | 3-Lug Stand-Up Short Socket | 2 | 077-5008-00
4A | 3-Lug Laydown Socket | 3 | 077-5006-00
5A | 3-Lug Stand-Up Long Socket | 19 | 077-5009-00
6A | 3-Lug Staple Down Socket | 0 | 077-5001-00
7A | 2-Lug Stand-Up Long Socket | 1 | 077-5005-00
B | #89 Bulb | 34 | 165-5000-89
1B | Laydown Standard Socket | 1 | 077-5100-00
2B | Stand-Up, Short Socket | 24 | 077-5101-00
3B | Stand-Up, Long Socket | 7 | 077-5102-00
4B | Straight Leg Socket | 2 | 077-5107-00
C | #455 Bulb (Twinkle) | 0 | 165-5003-00
1C | 1-Lug Stand-Up Long Socket | 0 | 077-5012-00
Lamps with Sockets Shown Actual Size.
Shaded zero-quantity rows are retained. This stock table is not a circuit/socket map.""",
    53: """PLAYFIELD - LAMPS WITH SOCKETS
Item | Description (1 bulb per socket) | Qty. | Part No.
D | #555 Wedge Base Bulb * | 48 | 165-5002-00
1D | 555 Wedge Base Socket ** | 37 | 077-5007-00
2D | Laydown Wedge Base L/R BLK | 6 | 077-5026-01
3D | Wedge Offset Bracket Socket | 0 | 077-5029-00
4D | Laydown Wedge Base Black | 0 | 077-5026-00
E | #906 Wedge Base Bulb | 2 | 165-5004-00
1E | 906 Wedge Base Socket | 2 | 077-5016-00
* - 3 extra #555 Bulb located 1 per Pop Bumper.
** This socket used only on Lamp Bds.
Note the notch in the bracket. (Used with Reflectors.)

Item | Lamp Board P.N.
A | 520-5079-01
B | 520-5079-02
C | 520-5079-04
D | 520-5079-05
E | 520-5079-06
F | 520-5079-07
G | 520-5079-08
H | 520-5079-09
I | 520-5079-11
(Please Note: Boards -03, -10, Not Used.)
UNDER PLAYFIELD: BOTTOM VIEW.
Lamps with Sockets Shown Actual Size.
Shading includes the E/1E rows despite their positive quantity; no inferred removal.""",
    55: """Lock Ball Assembly 500-5684-01
Deflector 535-6606-01
6-Ball Switch Assembly 500-5683-01
Item | Description | Part No.
1 | Outhole Mounting Bracket | 535-6621-01
2 | Coil Mounting Bracket | 535-6622-01
3 | Switch Mounting Bracket | 535-6623-00
4 | #4-40 PPH X .62 LG (2) | 237-5832-00
5 | Switch, Miniature | 180-5118-00
6 | #8-32 PPH w/SEM X .25 LG (8) | 232-5300-00
7 | Spring | 266-5020-00
8 | Rubber Bumper | 545-5105-00
9 | Plunger Assembly | 515-5000-02
10 | Coil Retaining Bracket | 535-5203-01
11 | Coil, 23-800 | 090-5001-00
12 | Coil Sleeve | 545-5076-00
13 | Switch, Subminiature (6) | 180-5119-00
14 | Wire Harness | 036-5301-00
15 | #2-56 PPH X .5 LG (12) | 237-5806-00
16 | #2 Split LW (12) | 244-5001-00
17 | Switch Protector (6) | 535-6539-00
18 | Core Stop Assembly | 515-5088-00
19 | Coil Sleeve | 545-5411-00
20 | Plunger ø7/16 X 2-1/4 LG | 530-5250-01
21 | Spacer | 545-5400-00
22 | #8-32 PPH X 1 inch LG | 232-1104-16
23 | Rubber Bumper | 545-5105-00
24 | E-Ring ø.44 Shaft | 270-5005-00
25 | Link, Lock Ball | 535-6649-00
26 | E-Ring, .25 Shaft (2) | 250-0008-00
27 | Lock Ball Cam Assembly | 515-5815-01
28 | Spring | 266-5000-00
29 | Coil Retaining Bracket | 535-6658-00
30 | Coil, 25-1240 | 090-5034-00
31 | Lock Ball Bracket Assembly | 515-5817-01
32 | Wire Harness | 036-5301-01
33 | #6-32 HWH TC X .38 LG (4) | 237-5898-00
34 | Deflector (Trough Entry Scoop) | 535-6606-01""",
    56: """Flipper Assembly, Lower
500-5755-01 (Right), 500-5755-02 (Left)
Item | Description | Part No.
1 | Flipper Bushing | 545-5070-00
2 | #6-32 X .38 LG HWH (3) | 237-5910-00
3 | #10-32 SOC HD X .75 LG | 237-5864-00
4 | Spring Bracket (Left) | 535-6663-02
5 | Flipper Return Spring | 265-5029-02
6 | Switch Mounting Bracket | 535-6664-00
7 | Flipper Base (Left) | 515-5077-02
8 | Flipper Base (Right) | 515-5077-01
9 | Coil Stop Bracket | 515-5346-00
10 | 1/4-20 SOC HD X .38 LG (2) | 237-5861-00
11 | Spring Washer | 269-5002-00
12 | Coil 22-1080 | 090-5032-00
13 | Front Bracket | 535-6453-00
14 | #8-32 X .38 LG HWH (6) | 237-5903-00
15 | Plunger and Link Assembly | 515-5822-00
16 | Roll Pin | 251-5000-00
17 | Pawl | 530-5070-00
18 | #10-32 X .75 LG Shoulder Bolt | 231-5019-00
19 | Plunger Stop Bracket | 535-5279-01
20 | Nylon Stop | 545-5445-01
21 | Spring Bracket (Right) | 535-6663-01
22 | Bushing | 530-5139-00
23 | #10-32 Elastic Stop Nut | 240-5203-00
24 | Coil Sleeve | 545-5388-00
25 | Flipper Link | 545-5401-00
26 | Power Switch | 180-5124-01
27 | Plastic Cap | 545-5084-00
28 | #6-32 X 1 inch LG PPH | 237-5506-00
29 | #6-32 X .63 LG PPH | 237-5899-00
30 | #6-32 Elastic Stop Nut | 240-5005-00
31 | Switch Plate | 535-5045-00
32 | 1/4 Hex Spacer (3/8 inch Long) | 254-5008-12""",
    58: """Lower Slingshot Assemblies 500-5226-00
Item | Description | Part No.
1 | Slingshot Bracket | 515-5339-00
2 | S. S. Arm & Tip Assembly | 515-5340-00
3 | Plunger & Link Assembly | 515-5338-00
4 | 1/4 Retaining Ring (2) | 270-5002-00
5 | Spring | 266-5020-00
6 | Coil 23-800 | 090-5001-00
7 | Coil Sleeve | 260-0004-00
8 | Coil Retainer | 535-5203-03
9 | #8-32 X 1/4 inch Screw (2) | 232-5300-00
10 | Slingshot Switch (2) | 180-5054-00
11 | Tension Plate (2) | 535-5846-00
12 | #4-40 X 1/2 inch Screw (4) | 237-5837-00
13 | Diode 1N4004 (2) | 112-5003-00
14 | Link | 545-5062-00

Upper Slingshot Assembly 500-5226-01
(Note coil is rotated 90°)
Item | Description | Part No.
1 | Slingshot Bracket | 515-5339-00
2 | S. S. Arm & Tip Assembly | 515-5340-00
3 | Plunger & Link Assembly | 515-5338-00
4 | 1/4 Retaining Ring (2) | 270-5002-00
5 | Spring | 266-5020-00
6 | Coil 23-800 | 090-5001-00
7 | Coil Sleeve | 260-0004-00
8 | Coil Retainer | 535-5203-03
9 | #8-32 X 1/4 inch Screw (2) | 232-5300-00
10 | Slingshot Switch (2) | 180-5054-00
11 | Tension Plate (2) | 535-5846-00
12 | #4-40 X 1/2 inch Screw (4) | 237-5837-00
13 | Diode 1N4004 (2) | 112-5003-00
14 | Link | 545-5062-00""",
    59: """Turbo Bumper Assembly 500-5227-00
Item | Description | Part No.
1 | Rod & Ring Assembly | 515-5085-00
2 | Bumper Skirt | 545-5098-00
3 | Bumper Housing | 545-5100-00
4 | Plunger Bracket | 535-5277-00
5 | Fiber Yoke | 545-5120-00
6 | Bumper Body | 545-5197-00
7 | Diode 1N4004 | 112-5003-00
8 | Switch | 180-5015-01
9 | Plunger | 530-5062-00
10 | Spring | 266-5009-00
11 | Metal Yoke | 535-5877-00
12 | Coil 23-800 | 090-5001-00
13 | Coil Sleeve | 260-0004-00
14 | Coil Stop Assembly | 515-5088-00
Bumper Cover (not shown) is not included with above assembly.
Bumper Cover (Red), 550-5057-02, Qty. 3, must be ordered separately.""",
    60: """Ball Kicker (Auto Launch) Assembly 500-5477-03
Item | Description | Part No.
1 | Coil Mounting Bracket | 535-6385-00
2 | 8-32 X 1/4 SEMS (2) | 232-5300-00
3 | Coil 22-600 | 090-5023-01
4 | Spring | 266-5020-00
5 | Plunger Assembly | 515-5000-02
6 | Grommet (Bumper Pad) | 545-5105-00
7 | Diode 1N4004 | 112-5003-00
8 | Coil Retaining Bracket | 535-5203-03
9 | Spring Washer | 269-5002-00

Knocker Assembly 500-5081-00
Item | Description | Part No.
1 | Coil 23-800 | 090-5001-01
2 | Coil Sleeve | 545-5076-00
3 | Spring | 266-5020-00
4 | Spring Washer | 269-5002-00
5 | Kickback/Knocker Bracket | 535-5265-00
6 | Coil Retainer Bracket | 535-5203-01
7 | Bumper Pad | 545-5105-00
8 | Screw #8-32 X 1/4 SEMS (2) | 232-5300-00
9 | Plunger Assembly | 515-5000-02
10 | Diode 1N4004 | 112-5003-00""",
    65: """Drop Target (D.T.) 3-Bank Assembly 500-5799-03
Item | Description | Part No.
1 | Target End Plate (2) | 535-6162-00
2 | Target Frame for 4-Bank [shaded] | 535-6159-04
2 | Target Frame for 3-Bank | 535-6159-03
2 | Target Frame for 2-Bank [shaded] | 535-6159-02
3 | 8-32 X 3/8 (6) | 237-5879-00
4 | Spring Mount. Plate for 4-Bank [shaded] | 535-6510-04
4 | Spring Mount. Plate for 3-Bank | 535-6510-03
4 | Spring Mount. Plate for 2-Bank [shaded] | 535-6510-02
5 | Target (Specify Game) | 545-5048-01
6 | Trgt. Retaining Brkt. for 4-Bank [shaded] | 535-5042-04
6 | Trgt. Retaining Brkt. for 3-Bank | 535-5042-03
6 | Trgt. Retaining Brkt. for 2-Bank [shaded] | 535-5042-02
7 | 6-32 X 3/8 SHWHTCS Type 23 (6) | 237-5891-00
8 | Target Reset Spring | 265-5003-00
9 | Coil Support Bracket | 535-6154-00
10 | --- | ---
11 | 23-700 Coil for 4-Bank [shaded] | 090-5022-00
11 | 23-800 Coil for 3-Bank | 090-5001-02
11 | 23-800 Coil for 2-Bank [shaded] | 090-5001-02
12 | Coil Sleeve | 545-5031-00
13 | Plunger Stop Bracket | 515-5008-00
14 | Plunger/Link Assembly | 515-5338-00
15 | Target Lift Bracket for 4-Bank [shaded] | 535-6509-04
15 | Target Lift Bracket for 3-Bank | 535-6509-03
15 | Target Lift Bracket for 2-Bank [shaded] | 535-6509-02
16 | Target Shaft for 4-Bank [shaded] | 530-5179-04
16 | Target Shaft for 3-Bank | 530-5179-03
16 | Target Shaft for 2-Bank [shaded] | 530-5179-02
17 | E-Ring (1/4 inch) | 270-5002-00
18 | Pivot Shaft for 4-Bank [shaded] | 530-5180-04
18 | Pivot Shaft for 3-Bank | 530-5180-03
18 | Pivot Shaft for 2-Bank [shaded] | 530-5180-02
19 | E-Ring (1/8 inch) | 270-5000-00
20 | Switch Assembly | 180-5092-01
21 | Switch Plate | 535-5045-00
22 | 6-32 X 1/2 | 237-5878-00
23 | Diode 1N4004 | 112-5003-00
24 | Plunger Link | 545-5293-00
25 | Adjustment Bracket | 535-6508-00
26 | 8-32 X 7/8 (1) | 237-5890-00
27 | 8-32 Nyloc | 240-5102-00
Note: common and unique parts for 2, 3 & 4 Bank assemblies.
Shaded X-Bank parts are not used in this game.
Quantity is designated by bank size; one diode per target.
Reference game number for proper decals.
The preceding PDF64 drawing is headed 500-5621-03 (Left & Right);
this table's printed 500-5799-03 title is retained, not substituted.

Stand-Up Target Assembly (1 inch Circle) 500-5835-08 (White)
Item | Description | Part No.
1 | Switch & Target Ass'y | 515-5966-08
2 | Mounting Bracket | 535-6896-00
3 | Back Plate | 535-5116-00
4 | 6-32 Nyloc (2) | 240-5010-00
5 | 6-32 X 3/4 HWH MS (2) | 237-5893-00

Target Color | 500-5835-XX
Clear | -01
Red | -02
Amber | -03
Green | -04
Blue | -05
Yellow | -06
Orange | -07
White | -08
Purple | -09""",
    57: """Flipper Assembly, Upper 500-5694-02 (Left)
1 | Flipper Bushing | 545-5070-00
2 | #6-32 X .38 LG HWH (3) | 234-5000-00
3 | #10-32 SOC HD X .75 LG | 237-5864-00
4 | Spring Bracket (Left) | 535-6663-02
5 | Flipper Return Spring | 265-5029-02
6 | Switch Mounting Bracket | 535-6664-00
7 | Flipper Base (Left) | 515-5077-02
8 | Flipper Base (Right) | 515-5077-01
9 | Coil Stop Bracket | 515-5346-00
10 | 1/4-20 SOC HD X .38 LG (2) | 237-5861-00
11 | Spring Washer | 269-5002-00
12 | Coil 23-1100 | 090-5030-00
13 | Front Bracket | 535-6453-00
14 | #8-32 X .38 LG HWH (6) | 234-5010-00
15 | Plunger and Link Assembly | 515-5822-00
16 | Roll Pin | 251-5000-00
17 | Pawl | 530-5070-00
18 | #10-32 X .75 LG Shoulder Bolt | 231-5019-00
19 | Plunger Stop Bracket | 535-5279-01
20 | Nylon Stop | 545-5445-01
21 | Spring Bracket (Right) | 535-6663-01
22 | Bushing | 530-5139-00
23 | #10-32 Elastic Stop Nut | 240-5026-00
24 | Coil Sleeve | 545-5388-00
25 | Flipper Link | 545-5401-00""",
    61: """Rose Handle Shooter Assembly (Long Shaft) 500-5836-01-02
1 | Housing | 535-5067-00
2 | Spring Large Red | 266-5001-02
3 | Spring Small Red | 266-5010-02
4 | Red Rose Rod Assembly | 515-6067-01
5 | Bushing (2) | 280-5010-00
6 | Retaining Ring | 270-5012-00
7 | Washer (3) | 242-5014-00
8 | Plunger Tip | 545-5276-00

Laser Kick Assembly 500-5838-00
1 | Plunger Assembly | 515-5000-02
2 | Coil Retainer Bracket | 535-5203-03
3 | #8-32 X 5/16 inch LG Phil. Pan. (2) | 232-5300-00
4 | Coil 23-800 | 090-5001-01
5 | 1N4004 Diode | 112-5003-00
6 | Spring | 266-5020-00
7 | Grommet (Bumper Pad) | 545-5105-00
8 | Kick Back/Knocker Bracket | 535-5265-00
9 | Crescent Spring Washer | 269-5002-00""",
    62: """Power Scoop Assembly 500-5809-00
These two assemblies work in conjunction with each other but are separate assemblies.
1 | Power Scoop Weld Assembly | 515-6022-00
2 | Micro Switch | 180-5057-00
2 | Switch Protect Plate | 535-6539-00
2 | #2 Lockwasher (2) | 244-5001-00
2 | 2-56 Hex Nut (2) | 240-5301-00
2 | Micro Bracket | 535-6163-00
2 | 2-56 PHMS (2) | 237-5806-00
2 | 6-32 PHMS (2) | 232-5200-00
3 | Diode 1N4004 | 112-5003-00

Kick Big Assembly 500-5740-00
1 | Coil 23-800 | 090-5001-01
2 | Coil Sleeve | 545-5076-00
3 | Diode 1N4004 | 112-5003-00
4 | Bracket | 535-5203-01
5 | Frame | 535-6730-00
6 | Plunger Assembly | 515-5000-02
7 | Rubber Grommet | 545-5105-00
8 | Spring | 266-5020-00
9 | 8-32 X 1/4 SEMS (2) | 232-5300-04
10 | Spring Washer | 269-5002-00""",
    63: """Ball Eject Assembly 500-5664-01
1 | Bracket & Stop Assembly | 515-5011-00
2 | Coil 24-940 | 090-5036-01
3 | Coil Retainer Bracket | 535-5203-01
4 | Coil Sleeve | 545-5031-00
5 | 8-32 X 1/4 SEMS (2) | 232-5300-04
6 | Plunger & Link Assembly | 515-5338-00
7 | E Ring (2) | 270-5002-00
8 | Eject Cam Assembly | 515-5042-00
9 | Spring Plate Assembly | 515-5009-00
10 | Ext. Spring | 265-5017-00
11 | Fulcrum Bracket | 535-6446-01
12 | Fulcrum Pin | 530-5207-00
13 | Plunger Spring | 266-5000-00
14 | Shim Washer (If Required) (2) | 242-5013-00
15 | Diode 1N4004 | 112-5003-00

Vertical Up-Kicker (VUK) 500-5839-00
1 | Switch | 180-5116-00
2 | Screw (2) | 237-5806-00
3 | Washer (2) | 244-5001-00
3 | Protector | 535-6539-00
4 | Diode 1N4001 | 112-5001-00
5 | Insulation | 545-5431-00
6 | Bracket | 535-6607-01
7 | Coil 25-1240 | 090-5034-01
8 | Bracket | 535-5203-01
9 | Screw (2) | 232-5300-00
10 | Plunger | 515-5941-01
11 | Spring | 266-5020-00
12 | Bumper Pad | 545-5105-00""",
    67: """"G" Ramp Trap Door Assembly 500-5830-00
1 | Bracket | 535-6998-00
2 | Trap Door Flap Assembly | 515-6056-00
3 | Nylon Flange Bearing (2) | 545-5492-00
4 | Retaining Ring 3/16 (4) | 270-5001-00
5 | Trap Door Linkage Clip | 535-6999-00
6 | Trap Door Linkage Pin | 530-5300-00
7 | Plunger Assembly | 515-6057-00
8 | #6-32 X 3/16 PHS (2) | 232-5209-00
9 | Coil Bracket | 535-6784-00
10 | Coil Sleeve | 545-5500-00
11 | Coil 28-1050 | 090-5046-00
12 | #10-32 X 3/4 SHCS | 232-2206-12
13 | #10 Washer (.090 THK) (2) | 242-5023-00
14 | #10-32 Nyloc Nut | 240-5023-00""",
    70: """6-Shooter Gun Assembly 500-5834-00
1 | Gun Body (Left) | 535-6280-00
2 | Gun Body (Right) | 535-6280-01
3 | Gun Grip (Left) Black | 545-5531-00
4 | Gun Grip (Right) Black | 545-5531-01
5 | Trigger Spring | 265-5037-00
6 | Microswitch | 180-5143-00
7 | Trigger | 535-6282-00
8 | Grip Mtg. Screw #4 X .42-39 | 237-5929-00
9 | Nyliner (3L2-FF) (Bushing) | 545-5532-00
10 | 8-32 X 5/8 Scw. Type F PPHMS | 237-5930-00
11 | Microswitch Mounting Screw | 237-5931-00
12 | Switch Protect Plate | 535-6281-00
13 | Wire Harness Assembly | 036-5350-06
14 | Diode 1N4004 | 535-5203-03
Wire harness / diode soldered to assembly included.""",
}
