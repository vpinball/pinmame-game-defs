# Pinned Medusa controller contract

Revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450`, repository
https://github.com/vpinball/pinmame . Read from the verified clean checkout;
working bytes spot-checked against HEAD. Transcribed and inspected by GPT Sol.

| File | SHA256 |
| --- | --- |
| src/wpc/by35games.c | 1c00fca170c7549a399a89fb0f76d4318fce08a6620becd4558fe8cb803bf00d |
| src/wpc/by35.c | 91df5b0c8a8ba19c017fec5ea45b7a4e2b911f2a56b9a793de7ad1cadd6f6e2 |
| src/wpc/core.c | 38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00 |

`by35games.c` Medusa block: INITGAME2 arguments are medusa, GEN_BY35,
medusaDisp, FLIP_SW(FLIP_L), 8, SNDBRD_BY61B, 0x10.
Read the macro, not an analogy: 8 is auxiliary lamp-column count, 0x10 is
hw.display, and the macro sets gameSpecific1=BY35GD_NOSOUNDE. There is no
Medusa BY35GD_ALPHA or SWVECTOR flag. `gen.h` GEN_BY35=0x0000000400000.

`medusaa` aliases init_medusa and input_ports_medusa. U2 and all three sound
ROMs are identical to medusa; U6 becomes 7536fn.u6. The driver is an Oliver
free-play revision dated2004, not another physical machine. Debug-only
medusaf is behind MAME_DEBUG and is absent from the pinned public catalog.

`dispBy7` imported by medusaDisp: four7-digit CORE_SEG87F layouts, segment
starts1,9,17,25; two2-digit CORE_SEG7 layouts at35,38. Medusa appends three
2-digit CORE_SEG7 layouts at42,44,46. These are physical display regions;
the extra rendered DMD callback in a native trace is not another fitted DMD.

`by35.c` pia0b_r reads core_getSwCol on ST0-ST4 from PIA0A bits0-4 and ST5
from PIA1B bit7. No Medusa per-input inversion mask is set. The own-game
normally open matrix drawing supplies construction, while the read path
explains public1 as closure. Apply no controller-wide second inversion.
Negative diagnostics -7,-6,-5 remain outside the numbered matrix.

`by35_lampStrobe`: public main address=16*d+a+1; auxiliary adds64. Selector
15 is suppressed, giving main1-15,17-31,33-47,49-63 and auxiliary65-79,
81-95,97-111,113-127. Medusa reserves8 auxiliary columns, not28 independent
emulator bits only. The physical A9 board's28 SCR circuits do not establish
semantics for all60 exported auxiliary slots.

`pia1b_w`: decoded momentary selector0-14 becomes public1-15, selector15 is
masked. Inverted continuous bits PB4-PB7 become17-20. On a rising bit selected
by hw.display&0xf0, bcd[5] is loaded and by35_dispStrobe(0x20) runs: Medusa's
0x10 therefore identifies PB4/public17 as the additional playfield display
data strobe. W-1255-1 wires6A1J1-15 to A4J4-5, wire36. LISY's Medusa case
independently makes J4-5 and J4-8 strobes. Q17's N/U load pin is no dead-state
proof. Public20 mirrors ST5/PB7;18 is coin lockout,19 is K1 enable.

`core_updateSw`, `core.h`: cabinet flipper buttons are internal column11,
public82(right) and84(left) under sequential conversion. FLIP_SW without
FLIP_SWNO copies no button into a matrix switch. The six-column ROM read
path cannot select81-88. When game-enabled,82 synthesizes45/46 together,
84 synthesizes47/48 together; these are duplicate states, not measured
power/hold timing. Other flipper-column bits add no fitted controls.
