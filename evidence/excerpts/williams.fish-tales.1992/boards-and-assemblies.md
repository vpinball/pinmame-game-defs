# Fish Tales — boards and assemblies that fix device construction

Transcribed from `Fish_Tales_OPS.pdf`, printed pages 2-12 through 2-31 and 2-34/2-35 (Section 2
board and mechanism assembly pages) and printed pages 3-15 through 3-19 (Section 3 Fliptronic II
circuit diagrams). Read from the rendered pages, not the OCR text layer.

## Opto/proximity construction boards (printed 2-12/2-13, PDF pages 60-61)

| Part | Name | Bears on |
| --- | --- | --- |
| A-15894 | Flipper Opto Board — two opto interrupters (`OPTO1`, `OPTO2`, part `5490-12451-00`), one 7-pin connector `J1` | the two cabinet flipper buttons (F2 Rt. Flipper Cabinet, F4 Lt. Flipper Cabinet) are opto interrupters, not leaf switches, wired one board per side (per the Fliptronic II Flipper Cabinet Switch Circuit Diagram, printed 3-18, which draws a separate "Left Flipper Opto Switch Board" and "Right Flipper Opto Switch Board") |
| A-13901-1 | Opto Ramp Switch Assembly — a 3-channel opto amplifier board (three connector pairs J5/J6/J7, LM339 quad comparator) | **usage on this game not identified from the pages read.** No switch address in the Switch Locations table cites this board, and the confirmed opto switches (37/38) use discrete parts on the Fish Reel Unit Assembly page instead (below), not this board. Left open for the curator. |
| A-15340 | Motor EMI Board (inductors L1/L2, TIP102 transistor Q1, diode D1) | in series with the Fish Reel gear motor (solenoid 28); listed as sub-item 25b of the Fish Reel Unit on the Playfield Parts page (2-40) |
| A-14316 | Opto Photo/Trans Assy. (2 used) | Fish Reel position sensing, receiver side — matches switch 37 (Reel 1) and 38 (Reel 2) exactly |
| A-14315 | Opto LED Assembly (2 used) | Fish Reel position sensing, emitter side — matches switch 37 (Reel 1) and 38 (Reel 2) exactly |
| 01-10378 / 01-10533 | Opto Bracket, Bottom / Opto Bracket, Top | mounts the two Fish Reel opto pairs above, one bracket per pair |

## A-15472 — Fliptronic II Board (printed 2-14, PDF page 62)

Q1-Q4 heatsinked drive transistors; Q5-Q12 TIP102 NPN opto-input transistors; Q13-Q20 2N4403 PNP;
a second Q1-Q4 set of TIP36C PNP power transistors; connectors J901/J904 (5-pin), J902 (13-pin),
J903 (34-pin ribbon to CPU board J202), J905/J906 (9-pin straight header), J907 (9-pin); F901-F904
fuses (3A S-B 250v). The board's own BOM provisions **four** independent flipper power channels (four
TIP36C output stages, four fuse positions) regardless of how many a given game populates — this is
generic board capacity, not evidence of fitment on any specific machine.

## Fliptronic II Flipper Assembly (printed 2-16/2-17, PDF pages 64-65)

`A-15205-R-2` "Fliptronic II Flipper Assembly (Lower Right)" and `A-15205-L-2` "Fliptronic II
Flipper Assembly (Lower Left)" are the *only* two flipper-assembly part numbers in the entire
manual. No upper-flipper assembly part number appears anywhere in Section 2. Page note 2: "Each
Flipper Assembly is mounted beneath the playfield, in conjunction with the Plastic Flipper & Shaft,
(20-9250-6) and Flipper Rubber (23-6519-4) on the upper side of the playfield" — describing exactly
two flipper paddles total.

## Mechanism assemblies (printed 2-18 to 2-31, PDF pages 66-79)

| Assembly | Part | Coil(s) / opto parts | Cross-checked device |
| --- | --- | --- | --- |
| Outhole Kicker Assembly | A-8039-3 | AE-27-1200 | solenoid 09 Outhole |
| Ball Shooter Lane Feeder (Ball Release) | C-9638 | AE-26-1200 (item 9e, assy B-9362-R-3) | solenoid 10 Ball Release |
| Ball Eject Assembly | A-9361-R-11 | AE-26-1200 | solenoid 11 Eject Hole |
| Kicker Bracket Assembly | A-14525 | AE-23-800 | solenoid 01 Ball Shooter |
| Knocker Assembly | B-10686-1 | AE-23-800 | solenoid 07 Knocker |
| Actuator Assembly | A-14422 | A-14406 | solenoid 06 Left Gate |
| Ball Popper Assembly | D-11335-1 | AE-24-900 | solenoid 03 Ball Popper |
| Fish Unit Assembly / Coil Unit Assembly | A-15306 / A-15304 | AE-23-800 (drives a `Bell Armature Assembly`, item 2) | solenoid 08 Backbox Fish |
| Fish Reel Unit Assembly | A-14945 | Gear Motor 50V (14-7967) + 2 opto pairs (A-14315/A-14316) | solenoid 28 Reel Motor; switches 37/38 Reel 1/Reel 2 |
| Catapult Assembly | A-14947 | AL-23-800 | solenoid 02 Catapult (part matches exactly, including the `AL-` prefix) |
| 1-Bank Drop Target Assembly | A-15211 | AE-26-1200 (item 5) + SM1-26-600 (item 28) — **two coils on one target bank** | solenoid 12 Drop Target Up + solenoid 13 Drop Target Down; switch 48 Drop Target (part `5647-12693-31` matches exactly) |
| Back Panel Assembly | A-15208 | — (3-Lamp Board Assy `A-15339`) | lamps 16/17/18 Letter (L)IE / L(I)E / Ll(E) |
| Boat Unit Assembly | A-15109 | — (5-Flash Lamp & Bracket `A-15471`; 5-Lamp PCB `A-15338`; Socket & Bulb Assy (4) `A-11271`; Rollover Switch Assy `A-12688-1`; Standup Target Assy (White) `A-14691-5`) | lamps 11-15 (A-15338), lamps 35-38 (A-11271), switches 43/44 (A-12688-1), switch 41 Captive Ball (A-14691-5) |
| Fishing Reel Handle Assembly | A-15130 | — (item 6, `20-9713-7` "Switch HSI Gaming") | switch 31 Cast |
| Ball Trough Switch Plate Assy. | B-8925 | — (two microswitches, `5647-12693-08` and `5647-09957-00` x2, both with diodes) | switch 16 Trough 1 (`5647-12693-08`), switches 17/18 Trough 2/3 (`5647-09957-00`) |

The 1-Bank Drop Target Assembly is the one genuine dual-coil mechanism found in this pass: a single
physical drop target is both knocked down by its own coil (13, `SM1-26-600`) and popped back up by a
separate coil (12, `AE-26-1200`), rather than resetting on a spring alone.

## Printed 3-15 to 3-19 — Fliptronic II circuit diagrams (generic, not fitment evidence)

PDF pages 109-113. These are the Fliptronic II Board's own circuit-theory diagrams, and every one of
them draws wiring for **all four** possible flipper positions (both lower and both upper), regardless
of which positions any specific game populates:

* **3-15, Fliptronic II Flipper Circuit Diagram**: cabinet-harness wires "Black-Blue U. Left Flipper
  F8", "Blue-Gray L. Left Flipper F4", "Black-Yellow U. Right Flipper F6", "Blue-Violet L. Right
  Flipper F2" (connector J905), board-harness wires "Black-Gray U. Left Flipper F7", "Black-Blue L.
  Left Flipper F3", "Black-Violet U. Right Flipper F5", "Black-Green L. Right Flipper F1" (connector
  J906), and generic "Right Flipper"/"Left Flipper" coil boxes at connector J902.
* **3-16, Fliptronic II Flipper Circuits**: draws a "Left Flipper Circuit" and "Right Flipper
  Circuit" side by side, each with an explicit "Lower Left/Right Flipper" coil AND a separate "Upper
  Left/Right Flipper" coil, each with its own EOS switch box.
* **3-17, Fliptronic II Flipper End-of-Stroke Switches**: legend "F1 Lower Right Flipper / F5 Upper
  Right Flipper", "F3 Lower Left Flipper / F7 Upper Left Flipper"; all four wired into board
  connector J906 (pins 1, 4, 3, 5) with a shared ground on pin 6.
* **3-18, Fliptronic II Flipper Cabinet Switch Circuit Diagram**: a "Left Flipper Opto Switch Board"
  and "Right Flipper Opto Switch Board", each with a full 7-pin `J1` footprint (matching the A-15894
  board's real connector), wired into board connector J905 for all four cabinet-button positions.
* **3-19, Fliptronic II Flipper Cabinet Switches**: legend "F2 Lower Right Flipper / F6 Upper Right
  Flipper", "F4 Lower Left Flipper / F8 Upper Left Flipper", wired into J905 pins 1, 3, 2, 5.

**This is generic board documentation, not game-specific evidence.** The Fliptronic II Board is
designed to drive up to four flippers regardless of what a given playfield/cabinet actually uses.
Every *game-specific* source read for this machine (Switch Locations, above; the Fliptronic II
Flipper Assembly parts list, above; the full Playfield Parts list; the Solenoid Table) independently
agrees Fish Tales has exactly two flippers, both lower, with no upper-flipper placeholder rows at
all. This directly disagrees with the task brief's stated pinned-driver fact that `FLIP_UR` is set
(implying a genuine upper-right flipper); reported here as an open item for the curator, not
resolved.
