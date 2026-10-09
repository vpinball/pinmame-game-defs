# Black Hole (Gottlieb 1981)

Coverage: **partial**. Every controller address is enumerated with a semantic disposition and its wiring, the mechanisms
and their behaviour are documented, and the driver variants are settled. Three requirements stay open:

- `input_semantics`: the fitment of return-7 matrix positions 57, 67 and 77 is unknown. The cabinet wiring sheet
  (printed page 47) is cut off in both retained manual scans.
- `spatial_placement`: every placement is the retained community table's object at `observed`, with no registered fit
  against the manual's location drawings (see the spatial report).
- `unresolved_conflicts`: the manual disagrees with itself on whether the pop bumper lamps stay lit on a tilt (see
  "Two playfields on one pair of flipper buttons" below).

Black Hole is Gottlieb game #668, built in October 1981 (IPDB 307). It is a widebody System 80 machine with a second,
lower playfield below a window in the upper one. The lower playfield slopes away from the player, so its flippers are
at the backbox end. It was the first Gottlieb machine with a two-level playing area. It is also the first System 80
record in this repository, and it introduced the `pinmame.gts80` controller profile.

## Sources

- **Instruction manual, two scans of the same final edition** ("applicable to all games not having the letter S in
  their serial number"):
  - The Scribd copy (document 223467608, 53 pages, about 110 dpi) is complete. Its fold-out sheets are cut off at the
    right edge.
  - The idoc.pub copy (30 pages, about 145 dpi) is sharper but ends after printed page 28.
  - Both are retained as page images under the working root's
    `manuals/by-machine/gottlieb.black-hole.1981/`, with page manifests. IPDB lists the manual only as "availability
    limited by copyright".
- **The known-working table** `Black Hole (Gottlieb 1981) vpx 1.1.vpx` by cyberpez. Its default ROM set is `blkhole7`.
- **Pinned PinMAME source** (`src/wpc/gts80*.c`).
- **Seventeen LibPinMAME harness runs**, under `runtime-evidence/black-hole-1981/`:
  - the ROM's lamp-driver test, solenoid test and switch test (in five parts);
  - a gameplay run, a high-game-to-date run, three tilt probes and a slam probe;
  - a self-test check of each variant driver.

## Platform facts that matter here (System 80)

- **Switch numbers.** A switch's number is the factory's two-digit matrix number: tens = strobe, units = return
  (`GTS80_sw2m`). The manual's "SW.nn" is the public address.
  - The ROM scans returns 0-7 of strobes 0-7.
  - Return 7 carries the cabinet switches: 07 Self/Test, 17/27/37 coin chutes, 47 Credit.
  - The slam switch is not in the matrix. It is public -1, read on RIOT U5 PA7, and public 1 means slammed (contact
    open).
  - The sound board's test button is -4.
- **Flipper buttons.** The buttons are never read by the CPU. PinMAME keeps them at 112 (right) and 114 (left) and
  fabricates synthetic outputs 45/46 and 47/48 from them while solenoid 10 is set.
- **Solenoids.** There are nine solenoid drivers, 1-9. Solenoid 10 is synthetic: lamp 0 (the Q game-over relay) gated
  by lamp 1 (the T tilt relay), which is the game-on and flipper-enable state. Solenoid 11 is synthetic too: lamp 1.
  PinMAME publishes both only in binary solenoid mode. With physical or modulated solenoid output enabled they read 0,
  and a consumer takes game on as lamp 0 on while lamp 1 is off, and the tilt state as lamp 1.
- **Lamps.** Lamps are twelve latched four-bit columns, numbered 0-47 exactly as the manual's "L" numbers. Lamps 48-51
  are the inverted outputs of the latch that holds 44-47. That inversion is real driver-board hardware (Z12's Q-bar
  outputs), not an emulator artefact.
- **Polarity.** Every matrix switch reads 1 when its contact is closed; there are no optos. The slam switch (-1) is the
  exception: it reads 1 when its normally closed contact opens.

## Address map in brief

**Upper playfield switches:**

| Switches | Devices |
| --- | --- |
| 00, 10, 20 | top rollovers |
| 01, 11, 21, 31 | yellow spot targets |
| 03, 13, 23, 04, 14 | B-L-A-C-K bank |
| 02, 12, 22, 32 | H-O-L-E bank |
| 05 | capture hole |
| 06 | the four pop bumpers |
| 15 | outhole |
| 16 | spinner |
| 24 | top lane rollunder |
| 25 | trough, third position |
| 26 | playboard tilt |
| 30 | right side rollover |
| 33 | black hole rollover |
| 34 | ten-point switches |
| 35 | right return |

**Lower playfield switches:**

| Switches | Devices |
| --- | --- |
| 40, 50, 60, 70 | yellow bank |
| 41, 51, 61 | white bank |
| 42 | capture hole |
| 43 | ball tube kicker |
| 52 | rollunder gate |
| 53 | track |
| 62 | return rollover |
| 71 | lower pop bumpers |
| 72 | ten-point switches and kicking target |

There are no switches at 36, 44-46, 54-56, 63-66 or 73-76. The ROM still scans these positions and shows their numbers
in the switch test.

**Solenoids:**

| Solenoid | Device |
| --- | --- |
| 1 | upper 4-bank (H-O-L-E) reset |
| 2 | upper 5-bank (B-L-A-C-K) reset |
| 3, 4, 7 | coin counters (left, right, center chute) |
| 5 | lower yellow 4-bank reset |
| 6 | lower white 3-bank reset |
| 8 | knocker |
| 9 | outhole kicker |

The manual's Note A list of solenoid assignments (page 13) is wrong. The ROM's own solenoid test shows 1, 2, 5, 6, 8
and 9 as it pulses exactly those public addresses, and the driver-board and playfield schematics wire them as listed
above. PinWiki's Black Hole page (a secondary lead, not retained) records the same correction.

**Lamp drivers that are not lamps:**

| Lamp | Device |
| --- | --- |
| 0 | Q (game over) relay |
| 1 | T (tilt) relay |
| 2 | coin lockout coil |
| 8 | lower ball gate |
| 9 | Sound 16 command line |
| 12 | lower hole kicker |
| 13 | upper hole kicker |
| 14 | ball lift kicker |
| 15 | trough ball gate |
| 16 | U relay |
| 17 | L relay |
| 18 | re-entry wireform gate |

The six lamp-driven coils hang on remote 2N5875 transistors Q1-Q5 under the playfields or directly on the driver
board, at 24 V DC.

**Light box lamps:**

- **Lamp 10: High Game to Date.** It lights for 2.5 s at each ball release, exactly while every score display shows the
  high game to date.
- **Lamp 11: Game Over.** It flashes through attract mode.
- **Lamp 3** feeds both the playfield and the light box SHOOT AGAIN bulbs.

## Two playfields on one pair of flipper buttons

The defining mechanism is the pair of relays on lamps 16 (U) and 17 (L):

- The U relay's normally closed contacts carry the cabinet flipper buttons to the four upper flippers, and the 6.3 V AC
  to the upper pop bumper, hole and playfield lamps.
- The L relay's normally open contacts carry the buttons to the two lower flippers, the lower playfield's illumination
  (#313 lamps) and its two pop bumper lamps, and the switched +24 V DC to its kicking rubber and kicking target.

When the ball rolls through the black hole rollover (33), the ROM energizes both relays. The upper playfield goes dark,
its flippers go dead, and the lower one comes alive. The ball runs down a track to the lower ball gate (lamp 8), which
releases it from the track switch (53) into play.

Lower-playfield drains run past its flippers at the backbox end into the ball tube kicker (43). There the ball lift
(lamp 14, a heavy A-4893 coil on a 6 1/4 A fuse) fires the ball up the clear re-entry tube, and the ROM releases U and
L. The re-entry wireform gate (lamp 18) decides what happens at the top of the tube:

- If the gate is energized, the ball is directed onto the upper playfield. The manual opens it when a lower bank is
  completed or the flashing right return rollover is crossed, and keeps it open in 3-ball play.
- If it is not, the ball is lost to the outhole.

A recreation must therefore gate the synthetic flipper outputs 45-48 with lamps 16 and 17. The retained table does
exactly that.

What a tilt does to the pop bumper lamps is unresolved. The manual's tilt mode says all the playfield lamps go off except
the pop bumper lights, but its page 45 feeds every pop bumper lamp from the 6.3 V AC string that the T relay's normally
closed contact opens on a tilt (the upper four through U, the lower two through L), and T's other side lights the light
box TILT lamp. The definition records this as a conflict until someone watches a working machine tilt.

## Other mechanisms

- **Trough.** Three balls. The outhole (15) is kicked by solenoid 9 into the ball return trough. The trough has one
  switch, at its third position (25). The trough ball gate (lamp 15) releases a ball to the shooter. A game can start
  only with all three balls home.
- **Upper capture hole (05, lamp 13).**
  - Until the four yellow spot targets are completed, the hole kicks the ball straight back out.
  - After they are completed, the blue capture lamp (37) flashes and the next ball in the hole is held while a new ball
    is served.
  - The captured ball is ejected at the end of the player's turn.
- **Lower capture hole (42, lamp 12).** It is always active and holds a ball from ball to ball. Multiball starts when a
  ball reaches the lower playfield while both holes are occupied: the lower ball is released first (2-ball), and the
  upper one after both lower balls are lost (3-ball). All captive balls are ejected at game over.
- **Drop banks.**
  - The upper banks reset on completion.
  - The lower banks reset only when the ball leaves the lower playfield (the gameplay run shows the resets as 43
    closes).
  - Lamps 44-47 light the yellow bank's inserts, and their inverses (48-51) light the matching spot-target inserts.
- **Switch-fired devices, which are not controller outputs.**
  - Six pop bumpers, each on its own pop-bumper driver board (A8). The matrix sees only their shared scoring contacts,
    06 and 71.
  - Two upper kicking rubbers, and on the lower playfield one kicking rubber and a kicking target, fired by their own
    switches through relay contacts.
  - The right outlane ball-detour gate's switch lights the RETURN or OUTLANE lamp directly from +6 V DC through a T
    contact (page 45).
- **Backglass.** The rotating backglass disc (non-export games) is not a controller output; PinWiki, a secondary lead
  not retained as a source, says its 3 RPM motor runs continuously on 6 V DC whenever the game is powered. The light box's 28 animated lamps are chased by the stand-alone auxiliary lamp driver board (A11, a 555
  timer and decade counter), also not a controller output.

## Tilt, slam and the cabinet

- **Tilt (26).** The playboard tilt switch tilts the game on one closure: lamp 1 and solenoid 11 rise, and solenoid 10
  drops. The retained table writes its nudge tilt there.
- **Tilt (57).** The return-7 position PinMAME and sys80.vbs call Tilt tilts the game in the same way, and closing it
  leaves the self test (the manual's "close tilt switch" exit). PinWiki says Black Hole's tilt is assigned to 26 rather
  than the usual 57. Without the cabinet sheet it stays open whether Black Hole's plumb-bob and ball-roll tilts are wired
  to 57 or alongside 26.
- **Return-7 position 77.** Closing it also leaves the self test. During play it blanks the status displays and then
  freezes every output; what, if anything, is wired there is unknown.
- **Self test.** Self/Test (07) enters bookkeeping, and Credit (47) starts the self test:
  - Step 16, the lamp-driver test: Q, T and coin lockout pulsed, then the 3-47 chase.
  - Step 17, the solenoid test.
  - Step 18, the switch test: 99 with every switch open, otherwise the closed switch's number, held about 4.4 s.
  - Step 19, the display test.
  - Step 20, the memory test.

  The test leaves itself after about two minutes without Self/Test, or on a tilt.

## Displays

- **Score displays.** Four six-digit player displays in the light box.
- **Status display.** A four-digit status display (A5), credits left and ball in play/status right, mounted on the
  playfield at the lower left above the apron. PinMAME publishes it as four one-digit entries (memory 40-43).
- **Lower playfield display.** A fifth six-digit display (memory 50) along the window's front edge. It shows the lower
  playfield bonus and, at each serve, the high game to date.

## Variants

| Driver | Build | Differences from `blckhole` |
| --- | --- | --- |
| `blckhole` (rev. 4) | game PROM 668-4 with sound/speech, the PinMAME root | — |
| `blkhole2` (rev. 2, the manual's 668/2) | same hardware | identical |
| `blkholea` (668A, sound only) | sound-only board in the sound/speech board's connector, A7 supply removed (manual page 29) | IPDB says export games lack multiball, speech and the backglass disc. Outputs and switches number identically in its self tests. Reads DIPs 41-42 instead of 33-40. |
| `blkhole7`, `blkhol7s` | Oliver 2008 seven-digit conversions of the speech and sound-only builds | seven-digit player displays; display overrides only |

The sound-only drivers had their own residual record, which is now folded into this one.

## Known table defects (retained cyberpez v1.1)

- It drives the four upper pop-bumper cap lights from lamp 2, the coin lockout coil.
- It pulses drop-target and target switches briefly rather than holding them.
- Its solenoid constants `sSaucer=12`, `sGate=17`, `sEnable=19` and its `SolCallback(42)` are template leftovers that
  System 80 never publishes.
- It names the right return trigger `Tri_LeftInlane`, and its RomSet comment calls LTD's `bhol_ltd` a "Gottlieb Limited
  Edition".
