# Embryon v2.0.2 modeled bulbs

UnclePaulie's retained VPX release is version 2.0.2, published 2023-10-04:
https://vpuniverse.com/files/file/15595-embryon-bally-1981-w-vr-room/ .
Its release page credits VPW testing and identifies the seven-digit `embryond` ROM.
The retained release capture and exact VPX remain outside Git beside the extraction.

The pinned embedded script directly binds 59 `Lampz.Callback(n)` entries to
`DisableLighting2 bulbN`. Each bulb is a separately modeled primitive, distinct
from its insert and the two nearby `MassAssign` rendering lights. The seed records
each exact callback line and each bulb's world-space OBJ minimum/maximum. The
world-bounds midpoint is its observed socket anchor. The export is produced with
`vpxtool export obj --units vpu`; its SHA-256 is
`4c000a97a2854b770004ec22bcbd7ba926d861a56a45e7af61d511c8029de307`.

The four bumper bindings follow the complete chain, rather than their names alone:
12/28/44/60 call `bumperbulb1flash` through `bumperbulb4flash`; these update
`FlBumperFadeTarget(1..4)`. `FlFadeBumper` applies the fade to `FlBumperBulb(nr)`,
which `FlInitBumper` binds to `Eval("bumperbulb" & nr)` at script line 3722.
These are right-bottom, right-top, left-bottom and left-top, respectively.

Callback 87 calls `TopMidLaneLights`, which drives collection `GIMidLane`.
The collection contains `GI_032`, `GI_033` and their top rendering doubles.
The independently positioned lights sit on separately modeled `Bulb_Prim_016`
and `Bulb_Prim_017`: world-center distances 1.029138 and 0.427491 VPU.
Those two bulbs agree with the factory's left/right blue-shield circuit.

The mesh frame is checked against `l1` and `l119`, positioned independently from
the bulb primitives; their distances from the matching bulbs are under 2 VPU.
The primitives' stored XY positions agree with the exported centers within
0.000071 VPU for the 59 direct bindings. Their stored Z offsets are not socket
heights: use the world export, including its baked mesh offsets.

This supplies 65 bulb positions on 64 outputs. It supplies no socket for the
three star plastics (6/22/38), apron indicators (59/103), captive-ball circuits
(70/86), or flasher/load-lamp circuit 56. Render glows and plastic centers do not
fill those gaps. All positions remain observed; no factory drawing frame has
been independently fitted.
