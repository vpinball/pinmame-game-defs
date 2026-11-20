# Bad Cats spatial audit

Coverage is partial. Positions use x=0 at left and y=0 at the rear.

VPX `Bad Cats (Williams, 1989).vpx` SHA-256 `c8a84d685da8f96f3ee5cebcfc8e687e82b6eef7cf75965721c4fea9e9568df5`.
Embedded script SHA-256 `438d33220db843a3cbe5d55b46037a7a45581ac42a8ccc18d7cf68517eae56e6`.
Factory operations manual SHA-256 `79306ef2f40e5c67c6e8ea3693562525934a348fd0659858a8e1ef9bdd921274`.
vpxtool git:v0.33.3 extracted 2113 files and 100952057 bytes.
Full manifest SHA-256 `7d50fa597a283882390ade80c8ffd3af56eeb967c256ccf9a63b1a9db3e553ac`. The manifest uses case-sensitive relative POSIX paths, file sizes and SHA-256, serialized as compact sorted-key JSON plus a final LF.

VPX bounds are (0, 0) to (952, 2042). The normalization subtracts the left/top bounds and divides by width/height, rounded to six places.

The second local BadCats v1.0 build has the same authors and shared geometry. It was used to check omissions and carries no independent validation weight.
The wheel object rotates about its stored XY. Its extracted mesh has symmetric local XY bounds from -0.5 to 0.5 and no XY translation. The three wheel coordinates are shared assembly projections.
The factory switch and lamp top views identify positions. The photographs corroborate arrangement and visible domes. No control-point registration ties the photos or the drawings to the VPX frame, so these placements remain observed.
IPDB 51895 and 51896 show the dome and rear-display placement. IPDB 32758/32759 show the underside, but socket wiring is obscured. IPDB 32753 shows the two backbox figures. Pinside 4086234 corroborates the backbox display and includes aftermarket lighting.
A feature's flat VPX light is used only as an insert or assembly projection. The Tiger Ramp and rear panel lamps, jackpot socket and GI bulbs still need surveyed centers. Discarded flare sprites, glows, and overlapping flasher sources do not establish distinct sockets.
Both lower flipper pivots are visible on the VPX playfield. Their separate cabinet-wired coil assemblies have no hardware solenoid binding in PinMAME. The synthetic button mirrors have no separate physical emitter.
The listed flasher quantities include the backbox bulb on each mixed circuit. The playfield half is unplaced for 25, 29, and 32, and the three 06C Seafood sockets need separate locations.

## Observed placements (90)

| Group | Address | VPX item | Raw x, y | Normalized x, y | Evidence role |
| --- | --- | --- | --- | --- | --- |
| pinmame.input.switch | 11 | `gameitems/Trigger.sw11.json` | 607.77905, 256.80927 | 0.638423, 0.125764 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 12 | `gameitems/Trigger.sw12.json` | 692.5273, 258.63644 | 0.727445, 0.126658 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 13 | `gameitems/Trigger.sw13.json` | 776.7291, 258.7453 | 0.815892, 0.126712 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 14 | `gameitems/Trigger.sw14.json` | 895.5304, 1801.4213 | 0.940683, 0.882185 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 16 | `gameitems/Gate.sw16.json` | 509.02127, 519.98755 | 0.534686, 0.254646 | Script-bound ramp-entry gate center |
| pinmame.input.switch | 19 | `gameitems/Wall.sw19w11.json` | 274.9018066666667, 328.5532 | 0.288762, 0.160898 | Projection to the front stop of the staged linear target |
| pinmame.input.switch | 22 | `gameitems/Kicker.Ralfie.json` | 802.7174, 850.1262 | 0.843191, 0.41632 | Projection to occupied Doghouse pocket |
| pinmame.input.switch | 23 | `gameitems/Gate.sw23.json` | 155.35733, 830.326 | 0.16319, 0.406624 | Script-bound ramp-entry gate center |
| pinmame.input.switch | 24 | `gameitems/Kicker.Bin.json` | 82.01469, 448.8373 | 0.08615, 0.219803 | Projection to occupied garbage-can saucer |
| pinmame.input.switch | 25 | `gameitems/HitTarget.sw25.json` | 103.19754, 1133.0664 | 0.108401, 0.554881 | Projection from the target face to the opto housed in the bank |
| pinmame.input.switch | 26 | `gameitems/HitTarget.sw26.json` | 103.19754, 1079.2499 | 0.108401, 0.528526 | Projection from the target face to the opto housed in the bank |
| pinmame.input.switch | 27 | `gameitems/HitTarget.sw27.json` | 103.19754, 1025.9662 | 0.108401, 0.502432 | Projection from the target face to the opto housed in the bank |
| pinmame.input.switch | 28 | `gameitems/HitTarget.sw28.json` | 103.19754, 972.14966 | 0.108401, 0.476077 | Projection from the target face to the opto housed in the bank |
| pinmame.input.switch | 29 | `gameitems/HitTarget.sw29.json` | 103.19754, 918.86597 | 0.108401, 0.449983 | Projection from the target face to the opto housed in the bank |
| pinmame.input.switch | 30 | `gameitems/Trigger.sw30.json` | 125.752266, 1469.6986 | 0.132093, 0.719735 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 31 | `gameitems/Trigger.sw31.json` | 737.2322, 1470.5502 | 0.774404, 0.720152 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 33 | `gameitems/Wall.sw33.json` | 522.766655, 316.750665 | 0.549125, 0.155118 | Script-bound rubber contact collider centroid |
| pinmame.input.switch | 34 | `gameitems/Wall.sw34.json` | 432.33221000000003, 652.31154 | 0.45413, 0.319447 | Script-bound rubber contact collider centroid |
| pinmame.input.switch | 35 | `gameitems/Trigger.sw35.json` | 55.028015, 1475.6661 | 0.057803, 0.722657 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 36 | `gameitems/Trigger.sw36.json` | 807.71606, 1470.2755 | 0.848441, 0.720017 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 37 | `gameitems/HitTarget.sw37.json` | 677.9265, 954.2315 | 0.712108, 0.467302 | Projection from the target face to the opto housed in the bank |
| pinmame.input.switch | 38 | `gameitems/HitTarget.sw38.json` | 671.2054, 891.82086 | 0.705048, 0.436739 | Projection from the target face to the opto housed in the bank |
| pinmame.input.switch | 39 | `gameitems/HitTarget.sw39.json` | 665.7644, 836.1315 | 0.699332, 0.409467 | Projection from the target face to the opto housed in the bank |
| pinmame.input.switch | 40 | `gameitems/Wall.sw40.json` | 193.98045000000002, 643.8149175 | 0.203761, 0.315286 | Script-bound rubber contact collider centroid |
| pinmame.input.switch | 41 | `gameitems/Trigger.sw41.json` | 842.66547, 190.6399 | 0.885153, 0.093359 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 43 | `gameitems/Trigger.sw43.json` | 603.99963, 218.00342 | 0.634453, 0.10676 | Script-bound rollover or gate sensor center |
| pinmame.input.switch | 44 | `gameitems/Primitive.SFWheel.json` | 428.88892, 1041.4445 | 0.450514, 0.510012 | Projection to wheel axis. The opto is off-axis and its board orientation is not registered. |
| pinmame.input.switch | 60 | `gameitems/Bumper.sw60.json` | 599.1217, 476.03604 | 0.62933, 0.233122 | Script-bound bumper center |
| pinmame.input.switch | 61 | `gameitems/Bumper.sw61.json` | 792.36743, 467.13986 | 0.832319, 0.228766 | Script-bound bumper center |
| pinmame.input.switch | 62 | `gameitems/Bumper.sw62.json` | 731.79803, 657.8835 | 0.768695, 0.322176 | Script-bound bumper center |
| pinmame.input.switch | 63 | `gameitems/Wall.LeftSlingshot.json` | 222.79187000000002, 1464.198225 | 0.234025, 0.717041 | Sling event wall centroid, projected to the paired contacts |
| pinmame.input.switch | 64 | `gameitems/Wall.RightSlingshot.json` | 640.49155, 1465.9808 | 0.672785, 0.717914 | Sling event wall centroid, projected to the paired contacts |
| pinmame.output.lamp | 1 | `gameitems/Light.l1.json` | 432.08807, 1748.0181 | 0.453874, 0.856032 | Projection to the script-bound insert center |
| pinmame.output.lamp | 2 | `gameitems/Light.l2.json` | 316.73053, 1581.74 | 0.3327, 0.774603 | Projection to the script-bound insert center |
| pinmame.output.lamp | 3 | `gameitems/Light.l3.json` | 362.85406, 1581.0563 | 0.381149, 0.774269 | Projection to the script-bound insert center |
| pinmame.output.lamp | 4 | `gameitems/Light.l4.json` | 408.13657, 1651.5946 | 0.428715, 0.808812 | Projection to the script-bound insert center |
| pinmame.output.lamp | 5 | `gameitems/Light.l5.json` | 455.53085, 1652.0125 | 0.478499, 0.809017 | Projection to the script-bound insert center |
| pinmame.output.lamp | 6 | `gameitems/Light.l6.json` | 499.12363, 1581.9242 | 0.52429, 0.774694 | Projection to the script-bound insert center |
| pinmame.output.lamp | 7 | `gameitems/Light.l7.json` | 544.8779, 1580.27 | 0.572351, 0.773883 | Projection to the script-bound insert center |
| pinmame.output.lamp | 8 | `gameitems/Light.l8.json` | 158.79161, 323.33258 | 0.166798, 0.158341 | Projection to the script-bound insert center |
| pinmame.output.lamp | 14 | `gameitems/Light.l14.json` | 606.0204, 346.94354 | 0.636576, 0.169904 | Projection to the script-bound insert center |
| pinmame.output.lamp | 15 | `gameitems/Light.l15.json` | 691.6423, 411.4609 | 0.726515, 0.201499 | Projection to the script-bound insert center |
| pinmame.output.lamp | 16 | `gameitems/Light.l16.json` | 777.7369, 346.88608 | 0.816951, 0.169876 | Projection to the script-bound insert center |
| pinmame.output.lamp | 21 | `gameitems/Light.l21.json` | 541.7114, 683.97473 | 0.569025, 0.334953 | Projection to the script-bound insert center |
| pinmame.output.lamp | 22 | `gameitems/Light.l22.json` | 494.80768, 683.84955 | 0.519756, 0.334892 | Projection to the script-bound insert center |
| pinmame.output.lamp | 23 | `gameitems/Light.l23.json` | 495.20187, 636.96484 | 0.52017, 0.311932 | Projection to the script-bound insert center |
| pinmame.output.lamp | 24 | `gameitems/Light.l24.json` | 542.4935, 637.24036 | 0.569846, 0.312067 | Projection to the script-bound insert center |
| pinmame.output.lamp | 25 | `gameitems/Light.l25.json` | 643.55646, 608.934 | 0.676005, 0.298205 | Projection to the script-bound insert center |
| pinmame.output.lamp | 26 | `gameitems/Light.l26.json` | 194.27496, 1598.665 | 0.20407, 0.782892 | Projection to the script-bound insert center |
| pinmame.output.lamp | 27 | `gameitems/Light.l27.json` | 53.95695, 1358.1558 | 0.056677, 0.665111 | Projection to the script-bound insert center |
| pinmame.output.lamp | 28 | `gameitems/Light.l28.json` | 806.8581, 1362.1046 | 0.84754, 0.667044 | Projection to the script-bound insert center |
| pinmame.output.lamp | 29 | `gameitems/Light.l29.json` | 665.13934, 1602.1709 | 0.698676, 0.784609 | Projection to the script-bound insert center |
| pinmame.output.lamp | 30 | `gameitems/Light.l30.json` | 732.77765, 1059.795 | 0.769724, 0.518999 | Projection to the script-bound insert center |
| pinmame.output.lamp | 31 | `gameitems/Light.l31.json` | 790.3705, 875.4449 | 0.830221, 0.428719 | Projection to the script-bound Doghouse feature |
| pinmame.output.lamp | 33 | `gameitems/Light.l33.json` | 369.65436, 1403.7102 | 0.388292, 0.687419 | Projection to the script-bound insert center |
| pinmame.output.lamp | 34 | `gameitems/Light.l34.json` | 431.88684, 1401.7041 | 0.453663, 0.686437 | Projection to the script-bound insert center |
| pinmame.output.lamp | 35 | `gameitems/Light.l35.json` | 493.8738, 1404.5814 | 0.518775, 0.687846 | Projection to the script-bound insert center |
| pinmame.output.lamp | 36 | `gameitems/Light.l36.json` | 339.8837, 1474.6111 | 0.357021, 0.722141 | Projection to the script-bound insert center |
| pinmame.output.lamp | 37 | `gameitems/Light.l37.json` | 399.90976, 1465.6655 | 0.420073, 0.71776 | Projection to the script-bound insert center |
| pinmame.output.lamp | 38 | `gameitems/Light.l38.json` | 463.2987, 1465.8286 | 0.486658, 0.71784 | Projection to the script-bound insert center |
| pinmame.output.lamp | 39 | `gameitems/Light.l39.json` | 523.9446, 1475.5293 | 0.550362, 0.72259 | Projection to the script-bound insert center |
| pinmame.output.lamp | 40 | `gameitems/Light.l40.json` | 249.35452, 603.5649 | 0.261927, 0.295575 | Projection to the script-bound insert center |
| pinmame.output.lamp | 41 | `gameitems/Light.l41.json` | 515.5597, 860.3435 | 0.541554, 0.421324 | Projection to the script-bound insert center |
| pinmame.output.lamp | 42 | `gameitems/Light.l42.json` | 623.45374, 975.1069 | 0.654888, 0.477525 | Projection to the script-bound insert center |
| pinmame.output.lamp | 43 | `gameitems/Light.l43.json` | 620.0843, 1132.5278 | 0.651349, 0.554617 | Projection to the script-bound insert center |
| pinmame.output.lamp | 44 | `gameitems/Light.l44.json` | 504.34756, 1241.4481 | 0.529777, 0.607957 | Projection to the script-bound insert center |
| pinmame.output.lamp | 45 | `gameitems/Light.l45.json` | 348.14352, 1238.5198 | 0.365697, 0.606523 | Projection to the script-bound insert center |
| pinmame.output.lamp | 46 | `gameitems/Light.l46.json` | 238.72603, 1123.3779 | 0.250763, 0.550136 | Projection to the script-bound insert center |
| pinmame.output.lamp | 47 | `gameitems/Light.l47.json` | 242.7427, 964.8735 | 0.254982, 0.472514 | Projection to the script-bound insert center |
| pinmame.output.lamp | 48 | `gameitems/Light.l48.json` | 357.6272, 856.702 | 0.375659, 0.419541 | Projection to the script-bound insert center |
| pinmame.output.lamp | 49 | `gameitems/Light.l49.json` | 345.0073, 662.7814 | 0.362403, 0.324575 | Projection to the script-bound insert center |
| pinmame.output.lamp | 50 | `gameitems/Light.l50.json` | 332.6532, 601.5061 | 0.349426, 0.294567 | Projection to the script-bound insert center |
| pinmame.output.lamp | 51 | `gameitems/Light.l51.json` | 321.1375, 544.88153 | 0.337329, 0.266837 | Projection to the script-bound insert center |
| pinmame.output.lamp | 52 | `gameitems/Light.l52.json` | 309.24683, 487.27255 | 0.324839, 0.238625 | Projection to the script-bound insert center |
| pinmame.output.lamp | 53 | `gameitems/Light.l53.json` | 294.34833, 408.85144 | 0.309189, 0.200221 | Projection to the script-bound insert center |
| pinmame.output.solenoid | 3 | `gameitems/Kicker.Ralfie.json` | 802.7174, 850.1262 | 0.843191, 0.41632 | Under-board actuator projected to eject pocket |
| pinmame.output.solenoid | 4 | `gameitems/HitTarget.sw38.json` | 671.2054, 891.82086 | 0.705048, 0.436739 | Reset actuator projected to the center blade of its bank |
| pinmame.output.solenoid | 5 | `gameitems/Kicker.Bin.json` | 82.01469, 448.8373 | 0.08615, 0.219803 | Under-board actuator projected to eject pocket |
| pinmame.output.solenoid | 6 | `gameitems/HitTarget.sw27.json` | 103.19754, 1025.9662 | 0.108401, 0.502432 | Reset actuator projected to the center blade of its bank |
| pinmame.output.solenoid | 15 | `gameitems/Primitive.SFWheel.json` | 428.88892, 1041.4445 | 0.450514, 0.510012 | Two electrical phases projected to the same physical shaft |
| pinmame.output.solenoid | 16 | `gameitems/Primitive.SFWheel.json` | 428.88892, 1041.4445 | 0.450514, 0.510012 | Two electrical phases projected to the same physical shaft |
| pinmame.output.solenoid | 17 | `gameitems/Bumper.sw60.json` | 599.1217, 476.03604 | 0.62933, 0.233122 | Under-board coil projected to the driven jet |
| pinmame.output.solenoid | 18 | `gameitems/Wall.LeftSlingshot.json` | 222.79187000000002, 1464.198225 | 0.234025, 0.717041 | Under-board coil projected to the driven sling wall |
| pinmame.output.solenoid | 19 | `gameitems/Bumper.sw61.json` | 792.36743, 467.13986 | 0.832319, 0.228766 | Under-board coil projected to the driven jet |
| pinmame.output.solenoid | 20 | `gameitems/Wall.RightSlingshot.json` | 640.49155, 1465.9808 | 0.672785, 0.717914 | Under-board coil projected to the driven sling wall |
| pinmame.output.solenoid | 21 | `gameitems/Bumper.sw62.json` | 731.79803, 657.8835 | 0.768695, 0.322176 | Under-board coil projected to the driven jet |
| pinmame.output.solenoid | 26 | `gameitems/Light.f26.json` | 877.9508, 136.16057 | 0.922217, 0.06668 | VPX modeled bulb corroborated by the photographed dome; other bulb is in the backbox |
| pinmame.output.solenoid | 27 | `gameitems/Light.f27.json` | 40.992348, 979.6731 | 0.043059, 0.479762 | VPX modeled bulb corroborated by the photographed dome; other bulb is in the backbox |
| pinmame.output.solenoid | 28 | `gameitems/Light.f28.json` | 76.76543, 125.09885 | 0.080636, 0.061263 | VPX modeled bulb corroborated by the photographed dome; other bulb is in the backbox |
| pinmame.output.solenoid | 31 | `gameitems/Light.f31.json` | 800.9923, 1128.117 | 0.841378, 0.552457 | VPX modeled bulb corroborated by the photographed dome; other bulb is in the backbox |

## Used or unresolved addresses without a placement

- pinmame.input.switch 9 · Playfield Tilt
- pinmame.input.switch 10 · Outhole
- pinmame.output.solenoid 1 · Outhole Kicker
- pinmame.output.solenoid 10 · Playfield General Illumination Relay
- pinmame.output.solenoid 25 · Fish and Trash Flashers
- pinmame.output.solenoid 29 · Jackpot Flashers
- pinmame.output.solenoid 30 · Seafood Flashers
- pinmame.output.solenoid 32 · Barbecue Flashers
- pinmame.output.lamp 9 · 50K (Tiger Ramp)
- pinmame.output.lamp 10 · 100K (Tiger Ramp)
- pinmame.output.lamp 11 · 200K (Tiger Ramp)
- pinmame.output.lamp 12 · Unlimited Million (Tiger Ramp)
- pinmame.output.lamp 13 · 20,000,000 (Tiger Ramp)
- pinmame.output.lamp 17 · T (Rear Playfield Panel)
- pinmame.output.lamp 18 · O (Rear Playfield Panel)
- pinmame.output.lamp 19 · Y (Rear Playfield Panel)
- pinmame.output.lamp 20 · JACKPOT (Cntr Ramp)
- pinmame.output.lamp 32 · Seafood Arrow 2 (Fitment Unconfirmed)
