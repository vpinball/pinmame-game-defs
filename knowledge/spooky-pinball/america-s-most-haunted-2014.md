# America's Most Haunted (Spooky Pinball, 2014)

This definition covers the physical machine (IPDB 6161, model AMH01) and its two
PinMAME drivers, `amh_023` and `amh_022`, the V23 and V22 code updates on the Spooky Pinball pinHeck board (PIC32MX795 game CPU, Parallax Propeller
display/sound/media CPU). It is partial: every controller address is enumerated and checked against the ROM's own service
tests and named, but the placements come from one recreation table and are not yet checked against a factory drawing, the mechanisms are inventoried
without their full behaviour, and some outputs keep an unknown fitment.

## Machine

America's Most Haunted was Spooky Pinball's first production game, designed by Ben Heckendorn. It is the only pinHeck game with a raw 128x32 DMD (scanned by a Propeller cog) and the only one whose PIC32 program ships as Intel HEX, so it boots without the flash-and-restart cycle the other three need. Every playfield lamp and the cabinet are LED. Coils 7 and 8 are named PROTO BG 1 by the ROM (a prototype backglass output) and carry nothing on the production wire chart; coils 2-6, 13 and 24 are UNUSED in the ROM's own list. The lamp matrix carries three flashers (40 UPPER LEFT FLASHER, 41 HELL FLASHER, 42 SCOOP FLASHER). The wire chart has no GI header; its GI legend names four playfield strings (Lower red, Mid yellow, Upper purple, Scoop purple/black) on a green common, and with a game started the ROM held 26 and 37-39 steadily lit, but which output feeds which string is not printed anywhere retained.

Editions: IPDB 6161 America's Most Haunted (150 units (confirmed), first produced March 21, 2014, two art packages (Reality Green and Animated Blue)).

## Running it

The romset is AMH_SD_V023.zip from benheck.com with AMH_V023.hex added to the root, as the PinMAME pull request describes; the PIC32 runs the Intel HEX, the Propeller PROP_023.BIN (CRC bd5a99e8) from DMD/, loaded as `amh_023.zip`; `amh_022.zip` holds V22, built the same way from the V22 card and hex. PinMAME before 97aa922b
named it `amh.zip`, and the retained harness scenarios still name that set. pinHeck also needs `pinheck.zip` holding the Propeller's 32 KB mask ROM (`p8x32a.rom`, CRC32 f99b3070).
America's Most Haunted needs no flashing: PinMAME programs the Intel HEX into the PIC32 at every start.

## Controller contract

The platform contract is `controllers/pinmame/pinheck.json`. In short: factory switch and lamp `n` (0-63) are public
`(n / 8 + 1) * 10 + n % 8 + 1` (11-88); cabinet inputs are 1-8 and 91-97; the host drives the flipper buttons at 112 (right) and 114
(left), which PinMAME copies to cabinet inputs 3 and 4; factory coil `n` is public `n + 1` (1-24); GI outputs 0-7 are 25-32 and 8-15
are 37-44; 51-56 are the on-board RGB LEDs, 57-61 the servos (0-255 position), 62-64 the external or third RGB LED; the Start lamp
is 91. On every switch public 1 is the closed contact; no switch is inverted. 50 inputs, 29 solenoid-group
outputs and 64 lamps are used.

## What the ROM itself proves

Every pinHeck game has the same operator menu (Enter, 6, opens it; the right flipper button steps; Back, 5, leaves). Its Switch
Edge test draws each closure in an 8x8 grid laid out like the factory chart, so closing every public address proved the
switch formula for all 64 matrix positions and the cabinet mapping for 2-8 and 91-97. The Solenoid test names each of the 24
coils, and pressing Enter fired exactly coil `n + 1` every time. The Lamp test names the sixteen GI outputs (the playfield group
44 down to 37, the backbox group 32 down to 25) and then every matrix lamp by its factory number, lighting only that address. The
Servo and RGB tests name the servos and LED channels the game uses. A game-start run (trough full, Start pressed) shows the ROM
pulsing its trough feed coil repeatedly while no ball reaches the shooter lane.

## Mechanisms

### Four-ball trough, drain kicker and ball loader

A drained ball lands on the drain switch 88 and the DRAIN KICK coil (22) kicks it into the four-ball trough, sensed by 84-87 (Trough Ball 1-4). BALL LOAD (21) feeds one ball to the shooter lane (82). In the game-start run (all four trough contacts closed, Start pressed) the ROM pulsed 21 about every 1.6 s for 20 s, because no ball ever reached 82 to close it.

### Shooter lane and autolauncher

AUTOPLUNGER (23) kicks the ball resting on the shooter lane switch 82 into play; PinMAME's simulator also offers a manual plunger here.

### Right flipper

A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input 3 (host public 112), the ROM fires the RFLIP HIGH (17) winding to lift the bat and holds it on the RFLIP HOLD (18) winding, and the matrix end-of-stroke contact 75 (RIGHT EOS) tells it the stroke is complete. PinMAME publishes no Fliptronic states for this platform: the coil addresses are the flipper.

### Left flipper

A ROM-driven flipper on two board coils: the cabinet button reaches the ROM as cabinet input 4 (host public 114), the ROM fires the LFLIP HIGH (19) winding to lift the bat and holds it on the LFLIP HOLD (20) winding, and the matrix end-of-stroke contact 74 (LEFT EOS) tells it the stroke is complete. PinMAME publishes no Fliptronic states for this platform: the coil addresses are the flipper.

### Left slingshot

Slingshot switch 73 closes and the ROM fires LSLING (9).

### Right slingshot

Slingshot switch 76 closes and the ROM fires RSLING (10).

### Pop bumper 0 (upper left)

Pop bumper 0: skirt switch 56, coil POP BUMP 0 (14), the wire chart's upper left pop.

### Pop bumper 1 (upper right)

Pop bumper 1: skirt switch 67, coil POP BUMP 1 (15), the wire chart's upper right pop.

### Pop bumper 2 (lower)

Pop bumper 2: skirt switch 66, coil POP BUMP 2 (16), the wire chart's lower pop.

### Basement scoop

The basement: lanes 54 (Basement Upper) and 55 (Basement Lower) lead to the basement right scoop (37), which SCOOPKICK (11) ejects; the IPDB features count two vertical up-kickers.

### Spooky Door and the VUK behind it

The Spooky Door is servo 1 (58): the ROM's Servo test sets DOOR OPEN (level 7) and DOOR CLOSE (level 128). Behind it the VUK (12) lifts a ball resting on 38 (VUK LEFT BEHIND DOOR); opto 96 (the Spooky Door opto on the aux board) sees a ball at the door.

### Hellevator

The Hellevator car is servo 0 (57): HELL UP (level 228) and HELL DOWN (level 14) in the Servo test. Switch 64 senses a ball in the car and 46 is the elevator call button target; IPDB describes it carrying the ball to upper and lower levels.

### Ghost loop magnet

LOOP MAGNET (1) on the ghost loop, with the Ghost Loop opto 95 (opto 1 on the aux board) seeing the ball pass.

### Ghost figure

The ghost figure turns on servo 2 (59: GHOST LEFT 14, MIDDLE 128, RIGHT 242 in the Servo test) and glows from on-board WS2801 LED 2. Red is 62; green and blue are 63 and 64 under the RGB test's default GHOST TYPE REV 1 and swap to 64 and 63 under REV 2, an operator setting. IPDB calls it a colour-changing ghost.

### Three-target bank

Ghost targets 1-3 (33-35) on a bank that servo 3 (60) raises and lowers: TARGET UP (level 7) and TARGET DOWN (level 228). IPDB: the 3-target bank drops into the playfield.

### Balcony jump ramp

The balcony jump: 52 senses the approach, 51 a successful jump and 53 a ball that falls short onto the pop path.

## Evidence and remaining work

Factory chart transcriptions, the ROM service-test tables and the IPDB identity are under `evidence/excerpts/spooky-pinball.america-s-most-haunted.2014/`; the runtime
summary is `tools/pinheck_runtime.json` (rebuilt by `tools/pinheck_runtime.py` from the retained runs), the scenarios are
`tools/harness-scenarios/pinheck/amh-*.json`. Remaining: the placements come from the LW recreation table (v2.0), whose layout the operator reviewed as faithful but which no factory location drawing or second independent table checks, so they stay observed. Its script ports the game code and names objects after the factory switch and lamp numbers; each object was taken from what its handler does (`table-placements.md` cites the line), and where the table's names disagree the ROM decides: its top-lane triggers are named out of order, and the lanes run proves the chart's 40 "O", 41 "R", 42 "B". The basement subway switches (54, 55) are modelled off the playfield and the two side RGB strips (51-56) are not tied to an LED, so those stay unplaced;
the mechanism inventory names each mechanism's coils, switches and service-test positions, but no retained source gives its home and startup state, its timing, how the ROM resets it or how it fails, so mechanism behaviour stays open until a manual, a known-working table or a gameplay harness run supplies it. The outputs whose fitment stays unknown: 7 (Proto Bg 1), 8 (Proto Bg 1), 25 (Backbox GI Output 0), 26 (Backbox GI Output 1), 27 (Backbox GI Output 2), 28 (Backbox GI Output 3), 29 (Backbox GI Output 4), 30 (Backbox GI Output 5), 31 (Backbox GI Output 6), 32 (Backbox GI Output 7), 37 (Playfield GI Output 8), 38 (Playfield GI Output 9), 39 (Playfield GI Output 10), 40 (Playfield GI Output 11), 41 (Playfield GI Output 12), 42 (Playfield GI Output 13), 43 (Playfield GI Output 14), 44 (Playfield GI Output 15).
