# Embryon spatial audit — partial

The exact retained VPX is `vpx-sources/bally/embryon-1981/local-v1.4/Embryon(Bally 1980)VPXv1.4.vpx`,
SHA-256 `a759546a3b9f2f9b8fa204ac1c81e25526462abd94c0d757a1063b9acc94a5c2`.
Its extraction has canonical manifest SHA-256
`77e7c44ae196fed770dc82cbf2adedd0f725a409ee5230e10818b02d5b9ccae9`.
The table bounds are left/top 0, right 1257, bottom 1974. For each placement,
normalize with the repository helper as `x/1257`, `y/1974`, rounded to six decimals;
x increases left to right and y from backglass to apron.

Observed switch centers use `Trigger.sw2a`, `Trigger.sw2b` and `Trigger.sw2c`
for the three contacts at 2; `Trigger.sw12`, `sw13`, `sw14`, `sw15`, `sw19`,
`sw23` and `sw24` for their same-numbered inputs; `Kicker.sw4` for 4,
`Spinner.sw18` for 18 and
`Bumper.Bumper4`, `Bumper.Bumper3`, `Bumper.Bumper2`, `Bumper.Bumper1` for
37–40, respectively. The saucer coil is projected to `Kicker.sw4`; the four bumper
coils 10–13 project to `Bumper1`, `Bumper2`, `Bumper3`, `Bumper4`, respectively.
The right outlane flipper 20 uses `Flipper.RightLFlipper`; 46 uses
`Flipper.RightFlipper` and `Flipper.RightUFlipper`; 48 uses `Flipper.LeftFlipper`.
The seed `tools/seeds/bally/embryon-1981-spatial.json` retains every raw object center.
The projections are mechanism-center proxies, not measured coil locations.

Targets use the arithmetic mean of the local collider Wall drag points: `t20/21/22`,
`t25/26/27` and `t28/29/30/31/32/33/34`. The script binds captive triggers to those
standup Walls; their target faces are more meaningful anchors than the speed-threshold
trigger helpers. Switch 17 has two anchors, `t17` and `t17x`, for the drop and back
target. These project the contact assembly to its target face, not the below-playfield
leaf mounting. Coils 1/2/3 project to moving targets `t17/t26/t21`.

Sling switches 35/36 and coils 15/14 project to the midpoint of the script-bound
Wall's active rubber edge: the drag point marked `is_slingshot` and its successor,
wrapping at the last vertex. This is one assembly anchor, not a measured coil-shaft
location or an enumeration of its switch leaves.

The modern table is UnclePaulie's v2.0.2 release from
https://vpuniverse.com/files/file/15595-embryon-bally-1981-w-vr-room/ . Its retained
path is `vpx-sources/bally/embryon-1981/unclepaulie-2.0.2/download/Embryon (Bally 1981) w VR Room v2.0.2.vpx`,
SHA-256 `b825e72293a452017a28f5ece39ed71b8fd6ab28edfdf6d0aef9addb14e5bb83`.
Its embedded script runs compatible seven-digit `embryond`; script SHA-256
`7c4630d1d1805020b24b578013a5ad3255ee943495a6931c69ec2c7a427d503e`.
The extraction has 2,654 files and 175,941,706 bytes, canonical manifest SHA-256
`b54f92817455a7da1716c7929adafab4bf96acfe3a30093d87fa2649eede89d8`.
The local v1.4 extraction has 1,378 files and 40,741,950 bytes. Both manifests use
`tools/build_external_evidence_manifest.py`'s sorted path/size/SHA-256 algorithm.
Optional-root tests recompute them rather than trusting these recorded digests.

The modern world export `unclepaulie-2.0.2/world-obj/Embryon (Bally 1981) w VR Room v2.0.2.obj`
was produced with `vpxtool git:v0.33.3 export obj --units vpu`; SHA-256
`4c000a97a2854b770004ec22bcbd7ba926d861a56a45e7af61d511c8029de307`.
The seed `tools/seeds/bally/embryon-1981-bulbs.json` retains individual world-space
bounds. Use each mesh's own min/max midpoint, including baked offsets. Fifty-nine
direct `Lampz.Callback(n)` bindings name individual `bulbN` primitives. Four bumper
callbacks follow `FlBumperFadeTarget` through `FlFadeBumper` to `FlBumperBulb`, bound
by `FlInitBumper`. Callback 87 drives `GIMidLane`; its lights sit on the separately
modeled `Bulb_Prim_016/017`, matching the factory's two blue-shield circuit.

This supplies 65 bulb anchors on 64 outputs. Independently positioned `l1` and
`l119` check the mesh XY frame (under 2 VPU from their own bulbs); all 59 direct
bulbs agree with stored XY within 0.000071 VPU. Their stored Z offsets are not socket
heights. The four bumper bulbs also agree within 5 VPU with the older table's
corresponding switch/coil centers. These controls check table geometry, not factory
calibration. Rendering doubles, inserts, star plastics, reflections and flasher glows
are excluded; see the [binding excerpt](../../evidence/excerpts/bally.embryon.1981/modeled-bulbs.md).

Cabinet/service inputs 3, 6, 7, 9–11 and 16, the diagnostics, DIP banks and backbox
displays are not playfield locations. Physical cabinet buttons 82/84 and thirteen
backbox-only main lamps are also non-applicable to playfield space. Rebound contacts
at 1 and below-apron contacts at 5/8 still need defensible anchors: the table's extra
rebound handlers and abstract trough do not identify the individual physical contacts.
Still unplaced are lamp circuits 6/22/38 (star bulbs), 56 (four series #921 flasher
lamps and one #44 lamp in the A10 control circuit, whose physical purpose, visibility
and socket location are unknown), 59/103 (apron indicators), and 70/86 (captive-ball circuits).
IPDB full, underside and stripped-playfield photographs did not settle those socket
identities or circuit membership. All placements remain observed; no independent
factory drawing frame has yet been measured and reconciled.

The schematic identifies 117 as unfitted. Selector 7 has no SCR in any A9 group,
but PinMAME captures its shared data writes because it suppresses only selector 15;
these blank-row public pulses occur during boot and normal operation too.
Unfitted 52/63/117 also publish normal-operation states whose firmware use remains
unexplained, so their availability stays unknown. Selectors 8–14 remain semantically
unknown because the A9 hardware omits AD3 while the emulator stores distinct bits. The
A9 and W-1255 drawings disagree on physical lamp quantities at 70 and 86; an owner must
trace A9J2-6 and A9J2-13 and count the sockets. Continuous output 17 is unused:
the solenoid sheet proves no fitted PB4/CONT.2 load, and all four raw runs show
it in the shared 17–20 boot pulse (each edge spread below 1 ms). Pinned
`by35.c:357–359` maps PIA1:B's complemented high nibble to that whole bank; the
compact solenoid seed retains all timestamps and the source hash. This explains
public bank behavior without claiming the untraced firmware initialization's
instruction or intent. See the [fitment excerpt](../../evidence/excerpts/bally.embryon.1981/solenoid-fitment.md).
Fixed 5.9 VAC GI has no public string; the table's output
18/19 GI effects are visual proxies for physical lockout/flipper-enable states.
Those concrete gaps and the lack of independently validated positions keep the game partial.
