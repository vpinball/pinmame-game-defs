# Grand Lizard: pinned emulator contract

Source: PinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`,
`src/wpc/s11games.c` lines 38-41 and 202-230; `src/wpc/s11.c`;
`src/wpc/core.c`, `src/wpc/core.h`, `src/wpc/s11.h`, `src/wpc/gen.h`.
Method: curator read of the exact pinned source, with the macro expanded against
`core_tGameData` field order. This is emulator evidence, not a physical wiring table.

```c
INITGAMEFULL(grand, GEN_S11X, s11_dispS11, 0, FLIP_SWNO(0,48),
             S11_BCDDIAG,0,0,0, 43,44,0,0,0,0)
```

The expansion declares `hw.swCol = hw.lampCol = hw.custSol = 0`,
`hw.display = S11_BCDDIAG`, `hw.gameSpecific1 = hw.gameSpecific2 = 0`,
`wpc.invSw = {0}`, `sxx.muxSol = 0`, and `sxx.ssSw = {43,44,0,0,0,0}`.
The three drivers are `grand_l4`, `grand_l3` and `grand_l1`. All share
`grandGameData`, the `s11_mS11XS` module and the same three sound ROMs.
The root L-4 uses U26 L-3 and U27 L-4; L-3 uses U26 L-3 and U27 L-3;
L-1 uses its own U26/U27 L-1. No different physical edition is declared.

`pia4a_r` reads `core_getSwCol(locals.swCol)` without complementation.
The eight-bit strobe reaches matrix columns 1-8 only. The sequential converter
`core_swSeq2m(n) = n + 7` publishes the matrix as 1-64 and the diagnostic nibble
as -7 (Advance), -6 (Auto-Up/Manual-Down), -5 (CPU diagnostic), -4 (sound diagnostic).
Country is the single jumper bit exposed in DIP bank 0 and read on PIA2 PA7.
No per-game inversion bits are installed.

The special-solenoid VBLANK loop maps each nonzero `ssSw[ii]` directly to
`CORE_FIRSTSSSOL + ii` when enabled: switch 43 drives output 17 and switch 44
drives output 18. The remaining entries have no switch-driven synthesis.
PIA writes independently reach public 17-22 through the Williams permutation
`ssSolNo[0] = {5,4,1,2,0,3}`. The PIA handlers in order are
`pia1ca2_w`, `pia1cb2_w`, `pia3ca2_w`, `pia3cb2_w`, `pia4ca2_w`,
`pia4cb2_w`; therefore their public addresses are 22,21,18,19,17,20.

`S11_GAMEONSOL = 23` is the switched-solenoid/flipper enable. Public 24 is a gap.
The A/C-copy path 25-32 is inactive because `muxSol = 0`. No upper-flipper
coil state is published at 33-36 on `GEN_S11X`. The sound-overlay/printer
paths at 37-44 are disabled by the zero game-specific flags. Public 49 is the
generic simulator ball-shooter slot; this game installs no simulator. Public 50
is a gap and 51-64 has no custom outputs because `custSol = 0`.

`FLIP_SWNO(0,48)` sets cabinet-wired lower flippers without `FLIP_SOL`.
`core_updateSw` consumes the lower button bits at public 82 (right) and 84
(left). It copies 82 to matrix 48 on each update. Zero is the left-side sentinel,
so it makes no left matrix copy: matrix 47 is an independently writable input.
With the enable on, 82 synthesizes both 45/46 and 84 synthesizes both 47/48.
Those are virtual states, not four CPU-driven coil circuits, and do not measure
power/hold winding or EOS timing. The other six positions 81,83,85-88 survive
host writes but have no consumer in the eight-column ROM read path.

`s11_dispS11` has four seven-character player layouts at segment starts
1,9,21,29, then **four separate one-digit layouts**, indices 4-7 at segment
starts 0,8,20,28. The first two player rows use 16-segment alphanumeric digits;
the next two use seven-segment digits with comma. The smaller four digits are
`CORE_SEG7S`; physical pairing, labels and locations require the game's manual.
