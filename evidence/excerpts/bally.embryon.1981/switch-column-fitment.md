# Embryon: five fitted switch columns

The primary visually checked Embryon's native `switch.tif`, W-1192-29c
(playfield wiring), and manual PDF page 22 (printed page 17, Figure V).
The manual's complete switch identification table enumerates 01–40 only; see
[the transcription](manual-page-22.md). The wiring drawing fits five matrix
strobe branches, ST0–ST4, on A4J2 pins 1–5 respectively, across eight returns
I0–I7. It draws no sixth switch-column branch. These five columns account for
the forty listed positions; matrix positions 41–48 have no fitted contacts.

This is a physical fitment conclusion from Embryon's own wiring, not an
emulator read-path limitation. Pinned PinMAME `src/wpc/by35.c:240–249` can read a
sixth column: `(locals.b1 & 0x80)>>2` adds its select bit before
`core_getSwCol(col)`. That PB7 line instead drives Embryon's right outlane
Flipsave coil, public continuous output 20, as drawn on W-1192-29c and the
solenoid sheet (color manual PDF page 51). The manual/no-load wiring controls
physical absence; PinMAME controls the public transport. Host writes to 41–48
would not demonstrate physical fitment.

Original `switch.tif` SHA-256:
`cd75ab89604b39a2b755f46ae2c3d4682ac50f982ef78b028e0cff92c2d0383f`.
Pinned `by35.c` SHA-256:
`91df5b0c8a8ba19c017fec5ea45b7a4e2b911f2a56b9a793de7ad1caddd6f6e2`.
