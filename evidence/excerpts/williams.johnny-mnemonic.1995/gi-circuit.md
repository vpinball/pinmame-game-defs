# Williams Johnny Mnemonic (1995) — General Illumination Circuit

Source: Williams *Johnny Mnemonic* operations manual (September 1995), IPDB machine 3683 file
`Williams_1995_Johnny_Mnemonic_English_Manual.pdf`, PDF page 118, printed page 3-10. Read from the
native 300 dpi render.

`GENERAL ILLUMINATION CIRCUIT` (inside a box labelled `POWER DRIVER BOARD`):

- Under `Drive`: J113 into an `LS374`, point `A` through `560Ω` and `10K Ω` to a `2N5401` (point `B`),
  whose output through `51Ω` (point `C`) fires a triac. The triac sits between the upper `J120` pin and
  the `J115` pin that goes to the ground symbol.
- Under `Power`: the other `J115` pin runs through a fuse marked `S.B.` to the lower `J120` pin.
- The two `J120` pins run out to `G.I. LIGHTS`, three lamps in parallel.

Caption: `When point "A" toggles low, points, "B" and "C" are high. This turns on the triac and the
desired general illumination string of lights.`

`BLOCK DIAGRAM OF GENERAL ILLUMINATION CIRCUIT`: a `6.3 volt secondary` feeds, through a fuse on the
`Power Driver Board`, a box labelled `Playfield or Backbox G.I. Lights. Up to 18 bulbs per string.`,
whose other side returns to `Triac Drivers` on the `Power Driver Board`, driven by an `LS374 Latch`
from the `CPU Board` `Microprocessor`; a `5 volt secondary` feeds a `Zero Cross Detection Circuit`.

So the fused secondary is the always-on feed to the lamps and the triac switches their return, which
is how the definition records each string's power and control connections.
