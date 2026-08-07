# High Speed — mechanism assemblies, boards and cabinet parts

Transcribed from `high_speed_instruction_manual.pdf`, Section 2, read from 300 dpi `pdftoppm` renders:
PDF pages 39, 43, 44, 45, 46, 47 and 49 (printed pages 31, 35, 36, 37, 38, 39 and 41) plus the board
list on PDF page 10 (printed page 2). These are the pages that fix mechanism construction, which
switches belong to which assembly, and which devices are backbox or cabinet hardware.

## Board number list, printed page 2 (PDF page 10), verbatim excerpt

> All HIGH SPEED Circuit Boards are in the backbox. They are accessible by removing the backbox glass,
> unlatching the insert board, and swinging it open.
>
> 1 - CPU Board … 9 - Insert Board … 10 - (not assigned)

Connector prefixes therefore read: `1Pxx`/`1Jxx` = CPU Board, `3Pxx`/`3Jxx` = Power Supply Board,
`4Jxx` = Master Display Board, `7Pxx`/`7Jxx` = cabinet, `8Pxx`/`8Jxx` = playfield, `9Pxx`/`9Jxx` =
backbox Insert Board. This is what makes solenoid 10 ("Insert Board Flashers", wired to `9P1-7`) a
**backbox** device and solenoid 16 ("Coin-Lockout Relay", wired to `7P1-7, 7P2-4`) a **cabinet** device.

## Playfield Parts, printed page 31 (PDF page 39), verbatim

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | A-11041 | Outlane Kickback Assembly |
| 2 | B-10898 | Ball Guide |
| 3 | D-11050 | Ball Chute, Lower Left |
| 4 | B-11039 | Ball Guide & Switch Bracket |
| 5 | 01-8325 | Rail Protector |
| 6 | 01-8237 | Clip |
| 7 | D-10863 | Ball Chute, Upper Left |
| 8 | B-11019-2 | Spin Target Assembly |
| 8a | 01-8341 | Spin Target Mounting Bracket |
| 8b | 03-7796 | Target Shaft Washer |
| 8c | 12-6620 | Switch Actuator Wire |
| 8d | 31-1380-2 | "Bayshore Freeway" Decal |
| 8e | 31-1019-541 | HIGH SPEED Screened Target |
| 9 | B-10921 | Traffic Light Assembly |
| 10 | C-10893 | Ball Guide Assembly |
| 11 | 12-6680 | Ball Guide Wire |
| 12 | 17-1086 | Jet Bumper Cap |
| 13 | D-10884 | HIGH SPEED Ramp Gate Assembly |
| 14 | 03-8005 | Main Ramp Cover |
| 15 | D-10905 | HIGH SPEED Ramp Assembly |
| 16 | 01-6933-2 | Metal Eject Shield |
| 17 | C-10894 | Ball Guide Assembly |
| 18 | A-10889 | Ball Guide Assembly |
| 19 | 01-8217 | Ball Deflector |
| 20* | B-11019-1 | Spin Target Assembly |
| 20d | 31-1380-1 | "Santa Monica Freeway" Decal |
| 21* | B-11019-3 | Spin Target Assembly |
| 21a | 01-7649 | Spin Target Mounting Bracket |
| 21d | 31-1380-3 | "San Diego Freeway" Decal |
| 22 | A-10890 | Ball Guide Assembly |
| 23 | D-10862 | Ball Chute, Upper Right |
| 24 | B-11038 | Ball Guide & Switch Bracket |
| 25 | A-10897 | Ball Guide Assembly |
| 26 | D-11049 | Ball Chute, Lower Right |
| 27 | C-10935 | Ball Guide Assembly |
| 28 | B-10896 | Ball Guide Assembly |
| 29 | 10-148-2 | Plunger Spring |

> Notes: * - Complete list of parts (8a through 8e) also applies to items 20 and 21, except for
> lettered items noted with these assemblies.

The three "Spin Target Assemblies" are the three spinners at switches 44, 45 and 46, and this page is
the only source that names them: they are decal-screened rotating targets labelled **"Bayshore
Freeway"** (B-11019-2), **"Santa Monica Freeway"** (B-11019-1) and **"San Diego Freeway"** (B-11019-3).
The page does not say which decal is on which of the left/centre/right positions. Note also items 3, 7,
23 and 26 — the four ball chutes, upper and lower on each side, which are the physical "hideout" lanes
that switches 39/40 and 47/48 sit in.

## C-9952-R Flipper Assemblies, printed page 35 (PDF page 43), verbatim

| Item | Part No. | Description |
| --- | --- | --- |
| 1 | B-10655-R | Crank Link Assembly |
| 2 | C-9954-R | Flipper Base/Lane Change Assembly |
| 2a | 03-7811 | End of Stroke (EOS) Switch |
| 2b | SW-1A-150 | Lane Change Switch |
| 2c | 03-7568 | Flipper Bushing |
| 2d | A-10280 | Flipper Stock Bracket Assembly |
| 3 | 01-7695 | Solenoid Bracket |
| 4 | 10-376 | Coil Plunger Spring |
| 5 | FL 23/600-30/2600 | Flipper Coil |
| 6 | 23-6577 | Bumper Plug |

`C-9953-L UNIQUE PARTS`: item 1 `B-10655-L` Crank Link Assembly, Left; item 2 `C-9957-L` Flipper Sub
Base Assembly.

Notes, verbatim excerpts:

> 1 Each Flipper Assembly is mounted below the playfield, in conjunction with the plastic flipper and
> shaft (20-9250) and flipper rubber (23-6519) (on the upper side of the playfield).
>
> 2 The tip of the EOS Switch must travel .015 (+.010, -.000 inch) before the contacts fully open with
> the flipper in the actuated position. The EOS Switch contacts must have a gap of .062 (±.015) inch.
> Any adjustment of the EOS Switch must be made at a minimum distance of .25 inch from the switch body.
>
> 3 The Lane Change Switch must have a gap of .046 (±.015) inch, when fully open.
>
> 9 Solid color grey (or blue) wire connects to the bonded end of the diode, mounted on the connector
> end of flipper coil (item 5). Wire with trace color connects to the unbanded end of the diode.

This page is what resolves the switch 37/38 labelling. `SW-1A-150` is the **Lane Change Switch**, and
`SW-1A-150-1` its left-hand variant; the Switches parts list gives exactly those two part numbers for
addresses 37 and 38. The **EOS switch is a different part** (`03-7811`) and carries no matrix address
anywhere in this manual — note 2's wording also makes it a normally-closed contact that *opens* at end
of stroke, which is why it is in the coil circuit rather than the switch matrix.

## B-9414 Jet Bumper Assembly / B-9415 Jet Bumper Coil Assembly, printed page 36 (PDF page 44), verbatim

Jet Bumper Assembly `B-9414`: 1 `A-4754` Bumper Ring Assembly; 2 `03-6009-A5` Bumper Base;
3 `03-6035-5` Bumper Wafer; 4 `03-7443-5` Bumper Body; 5 `10-7` Bumper Spring; 6 `24-6416` Bumper
Socket; 7 `24-6549` **#44 Bulb**.

Jet Bumper Coil Assembly `B-9415`: 1 `B-7417` Bracket and Stop Assembly; 2 `01-1747` Coil Retaining
Bracket; 3 `01-5492` Armature Link Steel; 4 `01-5493` Armature Link Bakelite; 5 `02-3406-1` Coil
Plunger; 6 `10-326` Armature Spring; 7 `SG1-23-850-DC` Solenoid Coil.

Each jet bumper carries its own `#44` bulb in the cap. That bulb is part of the general illumination,
not of the strobed lamp matrix: no lamp-matrix address names a jet bumper.

Note the coil part here (`SG1-23-850-DC`) differs from the `AE-23-800-03` that the Solenoids/Flashers
list gives for items 19/20/21; `B-9415` is the generic Williams sub-assembly page and the game-specific
list is the one of record.

## Traffic Light Assembly, printed page 36 (PDF page 44), verbatim

`B-10921`: 1 `01-8231` Light Housing Plate; 2 `C-10915` Light Socket & Cable Assembly; 3 `B-10999`
Housing Subassembly; 4 `20-9505-4` PCB Mounting Standoff.

This is the playfield fixture holding lamps 42, 43 and 44 (Ramp Stoplight Red/Yellow/Green). The parts
list gives no bulb type and no bulb count; "Light Socket & Cable Assembly" is one part covering all
three sockets.

## HIGH SPEED Ramp Gate Assembly, printed page 37 (PDF page 45), verbatim

`D-10884`: 1 `23-6577` Plug Bumper, 5/8 dia.; 2 `20-8712-25` E-Ring, 1/4 in. shaft; 3 `A-10886` Drive
Arm Assembly; 4 `20-8712-18` E-Ring, 3/16 in. shaft; 5 `01-8201` Drive Link; 6 `10-389` Gate Mech.
Spring; 7 `02-4241` Plunger, Coil; 8 `20-8712-43` E-Ring, 7/16 in. shaft; 9 `4008-01017-06` Mach.
Screw; 10 `AL-23-800-01` **Coil Assembly**; 11 `4006-01003-06` Mach. Screw; 12 `10-303` Master Spring;
13 `03-7974` Spacer, Nylon; 14 `4700-00073-00` Flat Washer; 15 `20-8716-2` Roll Pin; 16 `D-10885`
**Gate Mech. Subassembly**; 17 `03-7973` Spacer, Nylon; 18 `C-10888` **Gate**; 19 `20-8716-5` Roll Pin;
20 `01-8-508-S` Solenoid Bracket; 21 `B-10932` Solenoid Bracket Assembly.

Note on the same page: *"ADD ONE DROP OF SILICON OIL ON ALL ROTATING SHAFTS. DO NOT ADD OIL TO
SOLENOID."* The Amendments sheet corrects "silicon" to "SILICONE" on printed page 37.

One coil, one drive arm, one drive link, one gate. The Solenoid Table's plural "Ramp Gates" is not
matched by a second gate part anywhere in this assembly, and the assembly appears once (item 13) in the
Playfield Parts list. **The mechanism has no switch of any kind** — no item in this parts list is a
switch, and no matrix address names the ramp gate.

## Kicker Arm Assembly, printed page 37 (PDF page 45), verbatim

`B-11051-R`: 1 `A-5103` Coil Plunger Assembly; 2 `A-5652-1` Kicker Crank Assembly, Right; 3 `12-6227`
Hair Pin Clip; 4 `B-11052` Kicker Mounting Assembly; 5 `4700-00030-00` Washer.

## Police Light Assembly, printed page 38 (PDF page 46), verbatim

`C-10933`: 1 `5791-09111-00` Connector Shell; 2 `5820-09080-00` Connector Pin; 3 `14-7939` **Motor,
100 rpm, 24VAC**; 4 `4004-01003-05` Mach. Screw; 5 `4006-01076-04` Cap Screw; 6 `02-4239` Motor Shaft
Collar; 7 `24-8771` **Bulb, #1683, 28V**; 8 `B-10917` Reflector Assembly; 9 `B-10934` Motor Plate &
Socket Assembly; 10* `03-7981` Red Lens; 11* `A-11053` Lens Clip Assembly; 12* `4700-00023-00` Washer;
13* `4408-01120-00` Wing Nut.

> Note: Items marked with asterisk (*) are not part of C-10933.

This is the machine's police beacon: a continuously rotating 100 rpm motor turning a reflector in front
of a single `#1683` 28 V bulb under a red lens, mounted with a wing nut. The Solenoid Table puts its
relay (`5580-10883-00`, solenoid 4) in the **Backbox**, and the Solenoids/Flashers parts list repeats
"(Backbox)" in the item description. It is not a playfield device and has no coordinate.

Pinned PinMAME's own comment for this address in `MACHINE_INIT(s11)` reads *"In fact, this is a relay
controlling police light which is a #1628 28V bulb"* — the same fact with the bulb number's last two
digits transposed against this parts list's `#1683`.

## HIGH SPEED Ramp Assembly, printed page 38 (PDF page 46), verbatim

`D-10905`: 1 `A-11063` Ramp Wire & Bracket Assembly; 2 `D-10950` Main Ramp Assembly; 3 `H-10909` Top
Ramp Cable; 4 `SW-1A-160` **Rollover Switch**; 5 `01-3670-1` Switch Plate, Flat; 6 `01-8227` Switch
Cover Bracket; 7 `03-8005` Main Ramp Cover; 8-10 screws and a hex nut.

`SW-1A-160` is the part the Switches parts list gives for both switch 42 (Left Ramp) and switch 43
(Right Ramp), so both ramp rollovers are part of this one ramp assembly.

## Outlane Kickback Assembly, printed page 39 (PDF page 47), verbatim

`A-11041`: 1 `A-6306-2` Bell Armature Assembly; 2 `B-7409-2` Mounting Bracket Assembly; 3 `01-8-508-T`
Solenoid Bracket; 4 `10-135` Solenoid Spring; 5 `23-6420` Rubber Grommet; 6 `AE-24-900-01` **Coil
Assembly, Complete**; 7 `4008-01017-05` Mach. Screw.

Notes on the drawing, verbatim: *"1. ITEM 1 TO HIT AGAINST ITEM 3 WHEN FULLY ENERGIZED. 2. FLANGE ON
COIL TUBING MUST BE BETWEEN ITEMS 3 & 4."*

The Amendments sheet adds a **Kickback Circuit Wiring** diagram for this device (Amendment Page 4): the
kickback coil sits in the 50 V DC circuit fed via `8J4 VIO-YEL`, with a `100 Ω 3 W` resistor and `+34 V`
on the drive side and `BRN-BLU` as the CPU-side line, matching the Solenoid Table's Brn-Blu / 1P12-7 /
8P3-14 row for solenoid 14. The same amendment page replaces the black relay used in this circuit and
in the Left and Right Hideout Kicker circuits with a `Relay Snubber Assembly, p/n B-11160`.

## Alphanumeric Master Display Board and backbox cables

`C-10877` Alphanumeric Master Display Board, printed page 41 (PDF page 49). Its connector list gives
`J8, J10, J12` 26-pin, `J4, J6, J7` 20-pin, `J1` 12-pin, `J2, J3` 9-pin, `J11` 6-pin headers, and its
segment/digit drivers are `U9, U12-U14` `UDN7180A` Cathode Segment Drivers and `U1, U2, U5, U6`
`UDN6118A or 6184` Anode/Digit Drivers. The board drawing labels four display connectors `4J5 PLAYER
4`, `4J7 PLAYER 3`, `4J8 PLAYER 2`, `4J10 PLAYER 1`.

Backbox Cables list, from the Amendments sheet (Amendment Page 4, "Add the following list of game parts
in Section 2"), verbatim:

| Part No. | Location or To-from Connections |
| --- | --- |
| 5795-10938-22 | CPU Bd. to Master Display Board |
| 5795-10937-06 | CPU Bd. to Background Sound Board |
| 5795-10868-14 | Master Display Bd. to Player 1 Display |
| 5795-10868-14 | Master Display Bd. to Player 2 Display |
| 5795-09453-00 | Master Display Bd. to Player 3 Display |
| 5795-09453-00 | Master Display Bd. to Player 4 Display |
| 5795-09453-00 | Master Display Bd. to Ball In Play/Match Display |
| H-8527 | Volume Control Cable |
| H-11035 | CPU Bd. to Speaker (backbox & cabinet) |

The Player 1 and Player 2 displays take a different cable part (`5795-10868-14`) from Players 3 and 4
(`5795-09453-00`), which is the physical counterpart of the emulator's display layout: the two upper
displays are 16-segment alphanumeric and the two lower ones 7-segment numeric. There is no separate
Credits cable, so the credit digits share the `C-8365 Ball In Play/Match Display Panel` (named on
printed page 39).
