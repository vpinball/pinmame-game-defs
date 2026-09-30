# Factory diagrams and corrections

Main manual PDF40/printed36: full coil/flash table and location drawing.
1L 6-Ball Ass'y Lockout; 1R Back Panel X2 LT/RT Crnr.
2L Ball Release (Eject); 2R Right Playfield.
3L Auto Ball Launch 50V; 3R Left Playfield.
4L Kicker Eject; 4R Turbo Bumpers X2.
5L VUK 50V; 5R "R" Ramp Enter.
6L Scoop/Kick Big 50V; 6R "G" Ramp.
7L Ramp Coil Trap Door; 7R Under "R" Ramp.
8L Knocker32V; 8R Under "G" Ramp.
09 Right3-Bank Drop Targets; 10 Left/Right(A/B)Relay; 11 G.I.Relay;
12 Left3-Bank Drop Targets; 13 NotUsed;14 LaserKick50V;15 NotUsed;16 NotUsed;
17 LeftTurboBumper;18 BottomTurboBumper;19 RightTurboBumper;
20 LeftSlingshot;21 RightSlingshot;22 TopSlingshot.
Shaded entries10/11/13/15/16 are not drawn as playfield devices.

Main manual PDF42/printed38 diagram: 7L VIO-BLK PPB J2-7 (table misprints
J2-8); 8L VIO-GRY J2-8. Mux relay10 BLK-RED CPU CN12-2 (table
misprints CN12-5, which belongs to12). VUK coil is25-1240 (table says23-800);
PDF63/printed59 BOM independently confirms25-1240,090-5034-01.
Each of1R-8R has four #89 bulbs. PF/backbox splits:
1R2/2;2R2/2;3R2/2;4R2/2;5R1/3;6R1/3;7R2/2;8R2/2.
The backbox insert bulbs are not playfield sockets.

PDF39/printed35 explicitly excludes GI from the switched-lamp drawing.
It shows two55 bulbs (left-shooter and left-ramp) and cabinet63/64.
PDF37/printed33 draws28/29 on opposite slings from its own table; the
matrix, parts rows and exact scripts establish28 right and29 left.
Upper flipper PDF41/printed37 says25-1100; PDF57/printed53
assembly500-5694-02 says23-1100,090-5030-00. This part conflict remains open.
Gun62 parts row says180-5093-00; gun assembly PDF70 lists180-5143-00.
PDF58 gives two 180-5054-00 leaf switches per lower or upper slingshot;
one matrix number represents the assembly, not one fitted physical contact.
PDF52-53 lamp/socket stock counts are retained in full, including shaded
zero rows and positive-quantity #906 rows. They do not assign every bulb to
a matrix address, GI feed or flasher bank; no GI count is derived by subtraction.

Factory Service Bulletin63, October4,1994, PDF1: failed auto launch can
accumulate balls, overheat the 22-600 coil and blow PPB F5 (5A slow-blow),
disabling the 50V loads including flippers. It specifies 090-5023-01, a
centered white nylon flat-tipped plunger and the improved chrome ramp.
The cabinet already provides the printed 6.5% pitch with leg levelers fully
inserted. Published 3.00 changes: repeated shooter-switch closures after
failed ramp climbs disable auto launch; multiball 50V coil firing turns
magnets off to reduce shared-supply load. This is an official firmware
description, not an independently exercised gameplay observation.
Factory Service Bulletin64, November1,1994, PDF1: lower the rear shooter
ramp mount about half an inch and advance its entrance in the routed slots
to reduce climb pitch. Its second page illustrates the modification; no
unmeasured geometry is transferred to normalized playfield positions.

July18 1994 Addendum No2,780-5029-51, PDF1: hold Start in Magnet Test
to rapidly cycle three center-playfield magnets. Laser Kick Test responds
to left-outlane ball placement and also supports eject and VUK tests.
Addendum PDF2 complete connector block (KEY means no conductor):

| Magnet board520-5068-00 | Net / wire | Other endpoint |
| --- | --- | --- |
| J1-9 | CLOCK BRN-WHT | CPU CN1-7 |
| J1-8 | INPUT3 ORG-BLK | CPU CN3-7 |
| J1-7 | INPUT1 ORG-RED | CPU CN3-8 |
| J1-6 | INPUT2 ORG-BRN | CPU CN3-9 |
| J1-5 | CLR GRY-BLK | CPU CN2-1 |
| J1-4 | +5V GRY | PS CN6-7 |
| J1-3 | KEY | none |
| J1-2 | GND BLK | PS CN4 |
| J1-1 | GND BLK | PS CN4 |
| J2-1 | +50V VIO-YEL | PPB J7-3 |
| J2-2 | KEY | none |
| J2-3 | OUTPUT1 BLU-VIO | MAGNET1 |
| J2-4 | OUTPUT2 BLU-GRY | MAGNET2 |
| J2-5 | GND BLK | PS CN4 |
| J2-6 | GND BLK | PS CN4 |
| J2-7 | OUTPUT3 BLU-WHT | MAGNET3 |

Addendum PDF3:74HCT273 latch drives Q1/Q2/Q3 P20N10 and diode D1/D2/D3
1N4934; unused latch inputs4-8 are grounded. Combining the explicit CPU
pin permutation with s11.c pia2b_w:raw37=Magnet2,38=Magnet1,39=Magnet3.
Both exact scripts identify public51/52/53 left/center/right. Generic source
comments' Magnet3/2/1 nomenclature is not the factory board numbering.

Paginated schematics PDF43, theory of operation: the SSFB uses a timed
50V actuation stage and an8V holding stage. The normally-closed EOS is
an optional knockback retrigger, not required for ordinary operation.
PDF44-45 connector labels: CN1-12 Flipper SwitchC;CN1-11 SwitchB;
CN1-10 ReturnC;CN1-9 EOSB;CN1-8 +5V;CN1-7 SwitchA;CN1-6 GND;
CN1-5 ReturnB;CN1-4 SwitchDrive;CN1-3 ReturnA;CN1-2 KEY;CN1-1 EOSA.
CN2-1/2 CoilC;CN2-3 unused;CN2-4/5 CoilB;CN2-6 KEY;
CN2-7/8 CoilA;CN2-9/10 8VAC;CN2-11/12 +50VDC.
The printed flipper table's power connector cells disagree with these
schematic labels; no unverified power-pin cell is promoted onto a virtual alias.

Transcription method: visually checked native-DPI full-page PDF renders,
primary Sol curator,2026-09-30; candidate OCR used only to find regions.
