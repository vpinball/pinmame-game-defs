# Independent VPX fixture register

UnclePaulie's [Mata Hari v2.0.0 release page](https://vpuniverse.com/files/file/26448-mata-hari-bally-1978/) describes object placement from scratch on a playfield scan. The retained 241,717,248-byte binary uses `matahari` and maps `AllLamps` through each object's `TimerInterval` (script lines 160 and 284–285). The `vpxtool git:v0.33.3` extraction manifest covers 2,358 files and 286,259,471 bytes. The extracted script's byte hash differs from the script in the pinned corpus. Both scripts apply 41 to both lower caps. The factory requires 41 right and 57 left.

The independent model corroborates seven 1978-frame anchor positions across five controlled circuits. Public 36 and 52 each have an upper round and a side arrow socket. The side bulb models agree with the head positions, while the two old render objects paint the head and shaft of each same insert. For potential outputs 26, 42 and 58, one bulb model lies at each arrowhead and the two script-driven lights shade its surface. The registration uses 20 round insert controls with RMS 0.729 VPU and maximum leave-one-out distance 6.793 VPU. Its side-arrow projections extrapolate from the centre controls. The production top image corroborates insert identity. The old VPX locations remain observed.

| Public lamp | Old 1978-frame anchors | Independent bulb primitives |
| --- | --- | --- |
| 26 | `Light.L26a` | `bulb26` |
| 36 | `Light.L36a`, `Light.I36b` | `bulb36`, `bulb36ar` |
| 42 | `Light.L42a` | `bulb42` |
| 52 | `Light.L52a`, `Light.I52b` | `bulb52`, `bulb52ar` |
| 58 | `Light.L58a` | `bulb58` |
| 59 | Projected `(0.162939, 0.874696)` | `Bulb_Prim_028`, below the credit lens |

The world OBJ export confirmed the chosen model XY centres within 0.000054 VPU of their primitive origins. `Bulb_Prim_028` lies at the same XY as both `l59` light objects to within 1.4 VPU and lies directly below the raised `p59` lens. Its mesh collection is `GIBulbPrims`. Its nearby powered visual lights both use address 59 in `AllLamps`, and there is no corresponding `gi_NNN` light. The original apron underside shows one nearby wired socket. Use the projected emitter centre for the feature lamp and treat the collection membership as a rendering detail.

The 27 other GI bulb primitives pair with `gi_001`–`gi_027`. Twenty-six have close counterparts in the older model. The rear-right `gi_019` and `Bulb_Prim_013` align with a large bore in the original bare board. A replacement-panel photo (`braid01.jpg`) shows an offset socket on a similar opening. `l3000` and `l3000a` are in the author's GI group, with one modeled `bulb3000` beneath the fourth upper arrow. The upper cap meshes `bumperbulb1` and `bumperbulb2` follow the hidden `b1and2` GI light. The fourth arrow, upper caps and rear-right bore remain physical-circuit candidates. Shared braid, a production opening and the virtual GI group do not establish each socket's supply or a factory total.

The full source register `newtable-objects-controls.json` retains the control coordinates, source hashes, individual GI candidate positions, VPX light and mesh bindings, transform and residuals under `review-artifacts/bally.mata-hari.1977/online-followup/`. The scene and extraction remain under `vpx-sources/bally/mata-hari-1977/unclepaulie-2.0/`. The factory schematic and parts catalog govern the physical assignments.
