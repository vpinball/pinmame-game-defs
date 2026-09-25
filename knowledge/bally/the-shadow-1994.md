# The Shadow (Bally 1994)

Coverage: **partial**. Every address is enumerated and named, and construction, polarity, mechanism
and variant facts are validated from the factory operations manual, pinned PinMAME and the retained
VPW table, and no conflict is open. It stays partial on spatial placement alone:

- Every coordinate comes from one table lineage. The VPW build and its older Skitso ancestor share
  most of their geometry, so their agreement does not confirm it independently.
- The manual's location drawings have legible callouts, but the placements have not yet been checked
  against them.
- Flashers 21, 22 and 23 each print two playfield sockets, and the table models one.
- Flashers 17 and 18 and the ramp-ring lamps 81-84 are not placed: the VPW table models no bulb or
  dome for them.
- The playfield G.I. sockets come only from the table's G.I. collections.

## Identity and drivers

- Midway Manufacturing Company under the Bally name, model 50032, November 1994 (IPDB 2528, OPDB
  `G4jPX-M85YZ`). WPC-Security (WPC-S) hardware with a DCS sound board and a 128x32 DMD. A five-ball
  game.
- PinMAME drivers: `ts_lx5` (parent) and nineteen clones, all declared in
  `src/wpc/sims/wpc/prelim/ts.c` with `wpc_mSecurityS` and one shared `tsGameData`:
  - the Bally LX-4/LX-5, LA-2/LA-4/LA-6, LF-4/LF-6 (French), LH-6 and LM-6 ('Mild') game ROMs;
  - the community `d*` LED-ghost-fix builds and the LH-6 text-index patch;
  - the PA-1 prototype (`ts_pa1`, plus its ghost-fix `ts_pa2`), which differs only in its U2 sound ROM.

  All are the same physical machine; no retained source says whether the prototype machines
  differed.

## Evidence used

- **Operations manual** 16-50032-101 (183 pages, IPDB `Manual_Bally_1994_The_Shadow.pdf`, an
  image-only 300 dpi scan that IPDB notes is missing printed pages 2-47 and 3-9), OCR'd with Windows OCR
  for search. The lamp, switch and solenoid/flasher tables, their location lists, the DIP chart and
  the mechanism assembly pages are transcribed with native-resolution crops under
  `evidence/excerpts/bally.the-shadow.1994/`.
- **VPW table** *The Shadow VPW Mod (Bally 1994)* 1.0 (VPU file 31690, submitted September 6):
  runtime bindings and all geometry. It refactors Sixtoe's VR mod of Skitso's detail mod of Alessio's
  original table, with a new physical build and a rebuilt Battlefield.
- **Older Skitso table** (Alessio, Skitso, Markrock76, Bord; Thalamus sound patch): the same bindings;
  its script is the one that ties the ramp-ring lamps 81-84 to their ring flasher objects.
- **Pinned PinMAME** `8371478a`: address routing, the inverted-switch mask, the Battlefield motor
  model and the magnet countdown.

## Controller facts a recreation needs

- Switches use WPC column/row numbering `11-88`, coin door `1-8`, Fliptronic `111-118`. 83 is not
  used, so there is no Mini Right Standup 2 switch, although lamp 73 (Mini Right Standup 2) is fitted.
  The mini-playfield inset of the 2-41 switch drawing labels the right standups 84, 83 and 81 and
  draws no 82; its "83" is a misprint for 82.
- **Opto switches.** The printed shading marks these as optos: 31-33, 36-38, 41-47 and 85-88, plus the
  cabinet flipper optos. PinMAME's mask for this game normalizes exactly the matrix set
  (columns 3 = 0xE7, 4 = 0x7F, 8 = 0xF0), and the Fliptronic column is complemented by the platform, so
  public 1 always means beam broken / ball present / button pressed. Do not invert again.
- **Cabinet buttons.**
  - Gun Trigger 11 launches the ball; there is no plunger.
  - The blue Phurba buttons above the flipper buttons are 34 (left) and 12 (right).
  - Start is 13 and Buy-In 23; their lamps are 88 and 87.
- **Solenoids.** 1-28 follow the printed table.
  - 19 and 20 are printed as flashers but are the Battlefield motor (right and left).
  - The Fliptronic upper-left circuits drive the magnet (35) and the Battle drop target's knock-down
    coil (36). 33/34 are the real upper right flipper.
  - 45-48 are the lower flippers.
  - 51 is a PinMAME simulator channel (the magnet countdown, see below), and 37-44, 49 and 50 are unused.
- **Lamps** 11-88 are all fitted. The ramp rings 81-84 use a 24-8855 bulb that the manual's legend
  does not decode.
- **G.I.** Strings 1 (bottom), 2 (top left) and 5 (top right) are playfield strings with #44 bulbs.
  Strings 3 and 4 ("Insert") are backbox strings with #555 bulbs.
  - The power driver board connector list (printed 3-28) says the opposite: J120 (strings 3 and 4) "to
    playfield" and J121 (strings 1, 2 and 5) "to insert".
  - The G.I. table is recorded. It is printed three times with the same columns, bulbs and names, the
    VPW script lights only strings 1, 2 and 5 on the playfield, and the connector list misprints two
    J121 pins.
- **DIP bank SW1-SW8** sets the country (America, European, French, German, Spain) per the chart on
  PDF page 2.

## Mechanisms

### Trough and gun launch

- Five balls sit on the trough optos 41-45 with Top Trough 46 above them. Ball Release (13) ejects
  one into the shooter lane, onto the Shooter switch (48).
- Pulling the gun trigger (11) makes the ROM fire the auto launch (1).

### Phurba ramp diverters

- Each ramp has a dagger-shaped diverter with one coil per direction: left 3/4, right 5/6.
- Each side's blue button toggles it.
- The branch the ball takes is reported by 75/76 (left ramp) or 77/78 (right ramp).

### Inner Sanctum

- The center wall target is an extended target raised by solenoid 8 and pulled down by 16. Switch 51
  closes while it is down.
- Behind it a magnet (35) sits under an opto (33) that sees the ball.
- **Locks.** Hitting the wall target lights them; three balls in the rear-right lockup (63-65,
  kickout 2) start Shadow Multi-ball.

### Battle drop and Battle popper

- A single drop target is raised by 25 and knocked down by 36. Switch 55 closes while it is down.
- Behind it, the Battle popper (68, solenoid 14) lifts the ball onto the Battlefield.

### Battlefield mini-playfield

- **Kicker head.** It rides a slide driven by a DC motor through the A-16120 motor control board:
  solenoid 19 drives it right and 20 left. Opto boards under the assembly mark the left (37) and
  right (38) ends.
- **Kick.** The head carries its own coil (15) and an opto (36) that sees a ball in front of it.
- **Play.**
  - The player steers the head with the flipper buttons, and it fires automatically.
  - Targets: the side standups 71-74 (left) and 81, 82, 84 (right), then the four back drop targets
    85-88, reset by 24.
  - The ball leaves through the Mini Exit Tube (58).
- **PinMAME model.** A 19-step linear mech: 19 alone moves toward position 18 and closes 38, and 20
  alone moves toward 0 and closes 37. It runs only when mechanics bit 0 is enabled, as the retained
  tables do with `HandleMechanics = 1`.
- **Table simplification.** The tables show the head at one of nineteen positions from
  `Controller.GetMech(0)` and pulse 36 from walls at those positions. They never fire solenoid 15.

### Other devices

- Left and right ejects (66/12 and 67/11).
- Slingshots (61/9 and 62/10).
- Three Fliptronic flippers (lower pair and upper right).
- A backbox knocker (7).

## Manual and table quirks worth knowing

- **Lamp grid misprints.** Cells 62 and 63 print "MINI LEFT STANDUP 23" (number box "2") and
  "…12". The locations list names them standups 3 and 2.
- **Magnet and knock-down transistors.** The main solenoid table prints 35 on Q2 and 36 on Q7. The
  flipper block prints the same connectors on Q1 and Q5, and gives Q2/Q7 to the upper right flipper.
- **Coil and assembly numbers.**
  - Item 08's coil is printed AL-23-800 in the locations list and the extended-target parts list, and
    AE-23-800 in the solenoid table.
  - The back flashers print bulb number 22-8802 where the legend reads 24-8802 (#906).
  - The slingshot assembly lists B-9362-R-3 as the left coil and B-9362-L-2 as the right.
- **Solenoid 51.** PinMAME publishes a magnet countdown there (8 frames after the magnet drops), but
  only when mechanics bit 1 is enabled. The retained tables use bit 0 only, so it stays 0 for them and
  for LibPinMAME's default.
- **Table quirks.**
  - Both retained scripts pulse the Always Closed switch 24 when a Battlefield drop target falls.
  - The older Skitso script swings the upper right flipper from the lower right callback; the VPW
    script gives it its own `sURFlipper` callback.
  - The VPW table maps the ring lamps 81-84 and flashers 17, 18 and 26-28 to helper lights off the
    playfield.
  - Flashers 21-23 and 26-28 are placed on the VPW table's Flupper dome bases. Flashers 17 and 18 have no
    dome or bulb object; only the older Skitso script binds them, to the glow images F117 and F118,
    which are not sockets.
  - The ring lamps 81-84 have no bulb object either; the Skitso script binds them to the glow sprites
    F181-F184, which are not placed.
  - The diverter, Battlefield kicker-head, slide-motor and mini drop-target reset coils are projections
    derived from the geometry of the parts they move.

## What would complete the record

- A least-squares fit of the lamp (2-39), switch (2-41) and solenoid/flasher (2-43) location drawings,
  with each callout checked against its placement, to validate the positions.
- The positions of the second sockets of flashers 21, 22 and 23, of the sockets of flashers 17 and 18
  (measured on the printed 2-43 drawing), and of the ramp-ring lamps 81-84 (on the 2-39 drawing).
- A playfield G.I. socket list or a survey of a real machine.
