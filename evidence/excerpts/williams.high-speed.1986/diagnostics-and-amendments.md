# High Speed — diagnostics text and the Amendments sheet

Transcribed from `high_speed_instruction_manual.pdf`, PDF pages 31 and 35 (printed pages 23 and 27,
Section 1 Test/Diagnostic Procedures) and PDF pages 55-58 (the four-page "Amendments and Additions to
the HIGH SPEED Instruction Manual" sheet, dated 040286, bound in reverse order in this copy: PDF 58 is
Amendment Page 1 and PDF 55 is Amendment Page 4). Read from 300 dpi `pdftoppm` renders.

The diagnostics text is transcribed because it is the manual's own statement of the game's display
inventory and of the address ranges the ROM exercises. The Amendments sheet is transcribed because it
contains two corrections that change device identity.

## Display inventory, printed page 23 (PDF page 31), verbatim excerpts

> MUSIC TEST. 1. To initiate the Music Test, press ADVANCE. Observe that the **SPEEDER 1 and 2**
> displays show the message, MUSIC TEST.
>
> DISPLAY TEST. 1. To initiate the Display Test, press ADVANCE. Observe that SPEEDER 1 and 2 displays
> briefly show the message, DISPLAY TEST, and that the **Credits** display shows 00 (the Display Test
> identifier).
>
> 2. Use AUTO-UP. Observe that all displays begin a display cycle of all 0s through all 9s, one digit at
> a time. Verify that the proper comma segments light during display of the odd-numbered digits. Next, a
> special "all segments" character 'walks' from left to right across each display (**SPEEDER 1, 2, 3, 4,
> BALL IN PLAY/MATCH, Credits**).
>
> SOUND TEST. 1. … The **BALL IN PLAY/MATCH** display shows a series of test steps from 00 through 07.

Six displays: SPEEDER 1, SPEEDER 2, SPEEDER 3, SPEEDER 4, BALL IN PLAY/MATCH, Credits. Only SPEEDER 1
and 2 are ever described as showing text messages; SPEEDER 3 and 4 only ever appear in the digit-cycle
list. The Credits and BALL IN PLAY/MATCH displays each show two digits everywhere they are quoted
("shows 00", "steps from 00 through 07", "shows 04 (Solenoid Test identifier)", "shows 05 (Switch Levels
Test identifier)").

## Lamp test text, printed page 23 (PDF page 31), verbatim excerpt

> …and that all feature lamps (playfield and backbox) blink on and off. (Note, however, that the General
> Illumination lamps remain lighted steadily.)

## Switch test range, printed page 25 (PDF page 33), verbatim excerpt

> For HIGH SPEED, switch numbers can range from 01 through 52.

## CPU LED Indicator Codes, printed page 27 (PDF page 35), verbatim

| Code | Code Meaning |
| --- | --- |
| 0 | Test Passed (game goes to Game-Over Mode) |
| 1 | CPU Board lockup; also, check Memory Protect circuit and U25 CMOS RAM for 'stuck' bits |
| 2 | U27 Game ROM 1 faulty (lower ROM, CPU Bd.) |
| 3 | U26 Game ROM 2 faulty (upper ROM, CPU Bd.) |
| 4 | Unused (see "Other or No Indications") |
| 5 | Blanking signal 'stuck'; coin door closed; Memory Protect circuit faulty; or U25 CMOS RAM faulty |
| Other or No Indications | System Failure: Check 5 VDC Power Supply; U26 Game ROM 2 faulty |

> Notes: 1. Zero (0) displayed during Memory Chip Test (using CPU Board switch SW2) indicates that
> Blanking Circuit is NOT functioning. 2. Eight (8) displayed during Memory Chip Test indicates that
> Blanking Circuit is functioning properly.

This single numeric CPU-board LED is the hardware behind pinned PinMAME's `S11_BCDDIAG` display flag for
this game. The diagnostic buttons referenced throughout the section are the coin-door ADVANCE and
AUTO-UP/MANUAL-DOWN switches plus the CPU Board's own SW1 (Sound Diagnostic) and SW2 (CPU Diagnostic).

> SYSTEM-11 SOUND SECTION TEST. Press the Sound Diagnostic Switch (SW 1) on the CPU Board.

## Amendments, Amendment Page 1 (PDF page 58), verbatim excerpts that change device identity

Concerning printed page 47 (the Power Wiring Diagram):

> l. Below the Flipper Power Supply, change the description, **LEFT HIDEOUT RELAY, to LEFT HIDEOUT
> COIL**. (The same change applies to the Right Hideout Relay designator; it should be "coil".) Add the
> word "RELAY" beside the two boxes (slightly below the coils) containing four short dark marks, which
> represent the relay terminals.
>
> g. Add the words, Relay Contacts, near the two sets of contacts in the lower center of the box
> labelled POWER SUPPLY box.
>
> h. Add p/n D-8345-541 above the words POWER SUPPLY along the bottom border of that box.

Concerning printed page 50 (the CPU Board and Power Supply diagrams):

> b. Transistors for Special Solenoids (SS) shown near connector 1J19 should be: **Q73 for SS 3; Q71 for
> SS 2; Q069 for SS 4; Q75 for SS 1; and Q077 for SS 5; Q079 for SS 6.**
>
> a. In the CPU Board diagram, the 1J22 connector is incorrectly shown as a 20-pin unit; it is actually a
> 26-pin connector.
>
> c. In the D-8345-541 Power Supply diagram: Pin 3J6-2 should be labelled -12V UNREG; pin 3J6-6 should be
> +12V UNREG; pins 3J5-2 and 3J5-5 should be labelled NC; terminal 1 of GEN. ILLUM. should have YEL-WHT
> as the wire color; wire color on pin 3J3-4 should be RED-WHT.

Concerning printed page 2:

> Jumpers for Revision A CPU Boards (having only jumpers W1 through W7): W1, W2, W4, W5, and W7 must be
> connected. Jumpers for Revision B CPU Boards (having jumpers W1 through W16): W1, W2, W4, W5, W7, W8,
> W11, W12, W13, W14, W16, W17, and W18 must be connected.

## Amendments, Amendment Page 4 (PDF page 55), verbatim excerpts

> 4. The following assembly replaces the black relay used in the **Left and Right Hideout Kicker** and
> the **Outlane Kickback** circuits.
>
> Relay Snubber Assembly, p/n B-11160 — 1 `A-7438-5` 5-Lug Terminal Strip Assy; 2 `HW-30018-0` Wire 18
> AWG Black; 3 `HW-30018-6` Wire 18 AWG Blue; 4 `01-6968` Relay Holder; 5 `5010-09787-00` Resistor 150 Ω
> 1/2 W; 6 `5040-09070-00` Capacitor 100 µF 100 V; 7 `5070-06258-00` Diode 1N4001; 8 `5070-08785-00`
> Diode 1N4003; 9 `5580-09384-00` Relay 2-Pole, 24 VDC 13 A.
>
> 3. Add the following circuit diagram of the Outlane Kickback to the Power Wiring Diagram appearing on
> page 47. — KICKBACK CIRCUIT WIRING: `8J4 VIO-YEL` (in the 50V DC Circuit) → KICKBACK COIL; `+34 V`
> through `100 Ω 3 W` and `RED`; CPU side `BRN-BLU`.

## What the amendments settle

- **Solenoids 7 and 8 drive hideout kicker coils, not relays.** Both the Solenoid Table and the
  Solenoids/Flashers list print "Left/Right Hideout Relay", and the manufacturer's own amendment
  corrects that wording to "coil"; the part `AE-24-900-02` is a coil in any case. There is a *separate*
  relay in each circuit — the snubbed 2-pole 24 VDC relay of `B-11160` — which the amendment also asks
  to be labelled on the diagram. The same applies to solenoid 14, whose parts-list entry already reads
  "Left Outlane Kickback (w/relay)".
- **The special-solenoid transistor map is confirmed** and matches the Solenoid Table exactly: SS1 = Q75
  (public 17), SS2 = Q71 (18), SS3 = Q73 (19), SS4 = Q69 (20), SS5 = Q77 (21), SS6 = Q79 (22). The
  amendment's "Q069"/"Q077"/"Q079" are the sheet's own zero-padded renderings of Q69/Q77/Q79.
