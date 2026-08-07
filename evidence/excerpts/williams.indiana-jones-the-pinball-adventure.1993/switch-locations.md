# Indiana Jones — Switch Locations

Transcribed from `Indiana_Jones_OPS.pdf`, PDF page 111, printed page 2-47, the Switch Locations
parts list — a two-column parts list (`Item | Switch No. | Where Used`) plus a playfield location
diagram. Read from the rendered page, not the OCR text stream, which is scrambled on this scan.
Optos are identified by an `(LED)` + `(trans.)` part pair; everything else is a single mechanical
part number.

Opto pairs found: 41 (A-16908/A-16909, Left Ramp Enter), 42-45 and 47 (A-14231/A-14232, Right Ramp
Enter/Top Idol Enter/Right Popper/Center Enter/Subway Lockup), 71 (A-14231/A-14232, Captive Ball
Front), 72-73 (A-16908/A-16909, Mini Top/Bottom Hole), 81-87 (A-16927/A-16926, all seven trough
positions), 91-93 (A-14231/A-14232, Wheel Position 1-3, on the 3-sw Opto PCB). F2/F4 (A-16384-1,
"Flipper Opto PCB Assembly" per TOC) and F5-F7 (A-13609, confirmed by TOC as "3-bank Opto Drop
Target") are opto by board/assembly identity even though the parts list prints only one assembly
number for them (no separate LED/trans pair). 94-95 (A-16657, "Motor Opto Switch PCB Assembly (for
mini playfield)" per TOC and its own schematic title on printed page 3-24) are opto as well, despite
the single-part listing. Every other position (11-18, 21-28, 31-38 except the listed optos, 46, 48,
54-58, 61-64, 65-68, 74-78 except 71, 88, F1/F3/F8) is a plain mechanical switch (leaf/rollover/
standup/kicker) or a printed-closed link (24).

## Item 23 is blank

Item 23 is blank — "Not Used" — with no switch or opto part number printed, directly contradicting
the Switch Matrix page's "Ticket Opto" label for the same address. `ij.c` independently defines
`#define swTicketOpto 23`, but that constant is never referenced anywhere else in the driver
(`ij_stateDef`, `ij_handleBallState`, `ij_handleMech`, `ij_inportData`) — it is a vestigial/template
address, not a live game input. Resolution: `availability: "unused"`, citing all three sources.

## Items 94/95 reversed

Items 94/95 read "Mini Pfd Right Limit" / "Mini Pfd Left Limit" here, the opposite of both the
Switch Matrix page (94 Left, 95 Right) and `ij.c`'s own naming (`swLL_PoA` = `CORE_CUSTSWNO(1,4)` =
124 = printed 94; `swRL_PoA` = `CORE_CUSTSWNO(1,5)` = 125 = printed 95 — "LL"/"RL" = Left Limit/
Right Limit). Two sources agree against one; resolved as 124 = Mini Playfield Left Limit, 125 = Mini
Playfield Right Limit, with the Locations page's reversed row disclosed in the knowledge note.

## Custom switch column (printed 91-95, public 121-128)

The 3-sw Opto PCB Assembly schematic (`A-13901-2`, printed page 3-20) labels its own harness "switch
column 9" (`J1-7 Violet-White, switch column 9, from 8-Driver PCB J5-4`) and wires rows 1-3 from
`CPU board J209-1/2/3` to three onboard opto pairs feeding Wheel Position 1/2/3. The Motor Opto
Switch PCB Assembly (`A-16657`, printed page 3-24, "for mini playfield") wires the same column-9
harness (`J1-6 Violet-White, switch column 9, from 8-Driver Board J5-4`) with rows 4/5 from
`J209-4/5` to two more opto pairs feeding the Mini Playfield Left/Right Limit. Both schematics agree
this is the physical column 9 of the switch matrix (as printed), but PinMAME's own fixed
`CORE_CUSTSWCOL = CORE_STDSWCOLS = 12` constant (`src/wpc/core.h`) places the first driver-declared
custom switch column (`ijGameData.hw.swCol = 1`) at internal array index 12, two past the Fliptronic
column (11), which `wpc_m2sw(col,row) = col*10+row+1` reports publicly as 121-128, not 91-98.
`#define swIdolPos1 CORE_CUSTSWNO(1,1)` evaluates to `121`, and the retained script drives
`Controller.Switch(121..125)` directly (never 91-95), confirming the public binding. The printed
"91-95" is captured as a `manual.address` alias only.
