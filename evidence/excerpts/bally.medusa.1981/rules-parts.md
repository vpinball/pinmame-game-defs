# Medusa rules, settings and assembly evidence

Sources: Bally game1245 FO713 manual SHA256
`6137807222d614505ac923df7acd24c091449cf45f1d4d383ab82939d0df6a7b`,
PDF6-10 printed4-7; Bally1981 Parts Catalog SHA256
`87272502a90b90b6ee77732e230c61f4281af950f4dc1d2a8da07f0bb9cad295`,
PDF25-26 printed46-49, PDF42-43 printed80-82 and PDF39 printed75.
Primary GPT Sol visually inspected cited cells and drawings after Windows OCR.
This excerpt paraphrases operation; complete cited parts tables follow in the
successor transcription section below. Numeric spacing is normalized.

## Feature operation (manual PDF6-7)

Left three targets made in sequence or the right four-drop bank collect the
Colossus award. The Medusa bonus climbs from1 to19, then40, then80 thousand;
the thresholds can be remembered according to options. Top seven targets
advance Olympus red lamps, with lit A/B arrows increasing the build value.
The saucer collects Olympus. The center red back target can subtract one
Olympus lamp; S6 disables subtraction. Each top target closes the movable
flippers. They reopen at timer expiry or when the ball leaves the upper area.
S8 ON accumulates ten-second target awards; OFF resets a ten-second interval.

The Shield post starts with five credits. Left/right lane shots add credits;
unused credits score10000 each at end of ball. The six-digit playfield panel
has three two-digit windows: EXTENDED PLAY/TIME UNITS, LIKE NUMBERS/AWARD
EXTRA BALL, SHIELD OF GODS/BONUS. Three left targets in sequence stop the
left like-number digit; completion of four right drops stops the right digit.
Matching stopped digits awards the extra ball. Unlike digits restart on a lane
shot. Last-ball extended play is qualified at the third Olympus threshold and
collected at the saucer; bonus is deferred until the time units expire.
Time-unit awards: left1-2-3 sequence10; right four-drop completion5; saucer1;
lit A or B arrow1. These are the own manual's values, not a copied instruction
card's120-unit wording. Table angle/speed constants are tuning, not physical facts.

## Complete physical DIP function inventory (manual PDF8-10)

The manual explicitly describes32 switches in four8-position packages on MPU
A4 in the backbox and says to turn off power before adjustment. Pricing is a
multi-bit selection; no single switch is assigned a made-up coin multiplier.

| Switches | Function |
| --- | --- |
| S1-S5 | Coin chute I(left) pricing |
| S6 | Top center back red target subtraction; ON no subtraction, OFF subtract1 |
| S7 | Colossus bonus lamp memory; ON remembers, OFF clears |
| S8 | Movable flipper timer; ON adds10seconds per target, OFF reset interval |
| S9-S13 | Coin chute III(right) pricing |
| S14 | High score feature; score-award feature described on PDF9 |
| S15 | Left target2/3 arrow memory; ON remembers |
| S16 | Medusa special threshold; ON40and80, OFF80 |
| S17-S20 | Coin chute II(center) pricing; allOFF follows chuteI |
| S21-S22 | Olympus red-lamp threshold selections |
| S23 | Flashing like-number memory; ON remembers |
| S24 | Medusa bonus1-19 lamp memory; ON remembers |
| S25-S26 | Maximum credits |
| S27 | Credit display; ON shows credits |
| S28 | Match feature; ON enables |
| S29 | Replay limit; ON all earned replays, OFF one per player/game |
| S30 | Saucer Olympus-arrow memory; ON remembers |
| S31-S32 | Balls per game |

| S26 | S25 | Maximum credits |
| --- | --- | --- |
| OFF | OFF | 10 |
| OFF | ON | 15 |
| ON | OFF | 25 |
| ON | ON | 40 |

| S32 | S31 | Balls per game |
| --- | --- | --- |
| OFF | ON | 5 |
| ON | OFF | 4 |
| OFF | OFF | 3 |
| ON | ON | 2 |

| S22 | S21 | First5 Olympus lamps | Second5 | Third5 | Fourth5 |
| --- | --- | --- | --- | --- | --- |
| ON | ON | 3 | 3 | 3 | 3 |
| ON | OFF | 3 | 3 | 2 | 2 |
| OFF | ON | 3 | 2 | 2 | 2 |
| OFF | OFF | 3 | 2 | 1 | 1 |

Sound is a front-door service adjustment at position18; it is not another
physical DIP. Self-test advances lamps, displays, sound, solenoids and stuck
switches in that order (manual PDF16 printed13). The solenoid test displays
the printed identification number; it does not encode the public address.

## Construction and gaps

The Medusa section of the1981 parts catalog explicitly identifies left target12
as a target (ASW-A10-48), settling the operations table's word KICKER. The own
parts drawing and Figure V pair38/11 top-left,37/12 top-right,40/9 bottom-left,
39/10 bottom-right. The catalog lists the top flipper assembly ASE-2397-4,
seven-memory bank ASE-3038-4, right bank ASE-2795-73, post ASE-2593-7,
saucer ASE-482-53, and four bumper assemblies ASE-2999.

The generic memory assembly on printed80 depicts a FOUR-target variant and
labels four CJ-31-2000 coils. Its suffix is blank. Medusa's own panel chart
specifies the SEVEN-target ASE-3038-4 and CV-31-2000 individual coils. Do not
carry either a pictured four-coil quantity or the generic CJ spelling into this
game silently. The winding/connector difference is retained as a note, not an
unresolved disagreement about whether seven targets are fitted.

W-1187-31 PDF2 draws5.9VAC general illumination with A2J1-4 wire10,
A2J1-1 wire70 and returns A2J1-6 wire40/A2J1-3 wire50. Upper flipper contacts
marked NC switch lower-flipper lighting. Those contacts are separate from
matrix41. W-1255-1 PDF3 draws28 A9 circuits and paired symbols for the five
shooter/Gorgon channels, plus the six-digit feature display. No full GI socket
location/count map is supplied by those schematic regions.
