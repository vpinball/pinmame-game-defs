# Flash Gordon - Figure V switch and solenoid location map

Transcribed from `Flash Gordon Bally 1981 English Manual.pdf`, PDF page 23, printed page 18, headed
`#1215 FLASH GORDON` with the caption `FIGURE V`. Read from a 400 dpi `pdftoppm` render. The
accompanying crop is the right-hand playfield rail, grayscale, which is the region that settles the
switch 12 / switch 15 disagreement between the other two manual sources.

This is a scale line drawing of the playfield with each device's identification number printed on
it. The printed legend:

> (circle) INDICATES SWITCH ASSEMBLY IDENTIFICATION NUMBERS.
> NOTE: CABINET: 07, 16 / DOOR 06, 09, 10, 11, 16
>
> (square) INDICATES SOLENOID IDENTIFICATION NUMBERS.
> NOTE: DOOR: 15 / BACKBOX: 16 / CABINET: 02

The numbers inside the shapes are the same identification numbers the two self-test tables use, not
controller addresses. Only the facts this definition relies on are transcribed:

- Switch 07 (Tilt) and switch 16 (Slam) are marked CABINET. Switch 06 (Credit Button), 09, 10 and 11
  (the three coin chutes) and switch 16 are marked DOOR. Switch 16 appears in both notes because it
  has two contacts.
- Solenoid 15 (Coin Lockout) is marked DOOR, solenoid 16 (K1 Relay) BACKBOX, and solenoid 02
  (Knocker) CABINET. None of the three is a playfield device.
- The two right-rail standup targets are drawn one above the other against the right side of the
  lower playfield, each beside a short heavy bar that is the target itself. **Circle 15 is drawn on
  the upper bar and circle 12 on the lower bar.** That agrees with the printed Switch Assembly
  Self-Test table ("12 LOWER RIGHT SIDE TARGET", "15 UPPER RIGHT SIDE TARGET") and disagrees with
  the Playfield A6 schematic sheet, which labels the same two matrix positions the other way round.
- Four rollover buttons carry circle 01: two in the upper-left corner and two on the right-hand arc.
  Three carry circle 02, spaced down the shooter-alley return arc. Each of those seven is drawn with
  a star-burst symbol beside it, the same symbol the drawing uses for the other lit rollover buttons.
- The outhole kicker coil is marked with square 01 at the ball drain, immediately left of switch
  circle 08 (Outhole). Switch circles 06, 08, 09, 10, 11 and 16 run along the bottom edge below the
  apron, which is the coin door row.
- Square 16 appears beside each of the machine's flipper coils, which are switched by the K1
  flipper-enable relay rather than by a driver-board output. One further square 16 is printed in the
  blank upper-right corner of the drawing with no leader line to any device; this transcription does
  not claim to know what it points at. The flipper-coil count comes from the parts list, not from
  counting these marks - see `parts-list-coils.md`.
