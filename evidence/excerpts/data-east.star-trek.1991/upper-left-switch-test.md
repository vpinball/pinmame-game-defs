# Production 2.01 upper-left hole switches

Two clean production-ROM runs used PinMAME revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450` and the authorized `trek_201.zip`. A harness adapter matched one exact visually checked 128 × 16 Switch Test title. The adapter set raw DIP bank 0 once at the first poll, after initialization, to 0 and 1 in separate runs. Both started from fresh state with a default bank readback of 0. The host changed one switch at a time, with public 18 as a reference before each candidate. The first sample was 0.3 s after closure.

Both runs returned the same visually checked frames.

| Public address and stimulus | DMD top line | DMD bottom line | Raw DMD pixel SHA-256 |
| --- | --- | --- | --- |
| 18 held at 1, both controls | SW:LEFT RETURN | GRN-ORN WHT-RED #18 | `ffc2ec9a47e28cd886ef2f467a4703a4ef8db22b8903af988d77c8cd60958758` |
| 28 held at 1 | SW:UPPER LEFT HOLE | GRN-YEL WHT-YEL #28 | `9ef4dc004b028b12181d4704998005dc3fd1ba8e2ce3fb4d4d235f6ab9ca5551` |
| 52 held at 1 | SW:UPPER LEFT HOLE | GRN-VIO WHT-YEL #52 | `3dd0cadfecbe86a0a9e9c0ced1cc164e405f2b13b4f079d650121b1391023d9b` |
| After release | SW: -SWITCH TEST- | [blank] | `9b8fca5715f25fa380e48128436349f29cb761d3050ae5a22e704783c3496682` |

The switch names disappear during the continued hold. A late snapshot would miss the recognition. The DMD uses the same name for 28 and 52 but distinguishes their switch numbers and one wire color. The factory matrix and parts charts identify 28 as Top and 52 as Bottom. The ROM output demonstrates active-high recognition at each address at both tested bank settings. The host controls the stimulus. Physical contact ordering and transit time remain unmeasured.

The 0.9 VPX `script.vbs`, embedded lines 307–315, calls `PulseSw 52` at the entrance and immediately queues `PulseSwitch 28, 1200, "bsSaucer.AddBall"`. The retained VPM v3.61 `core.vbs` timer clears the pulsed switch before waiting the requested callback delay. The 1.2 s is a simulated transfer delay after the 28 pulse, not the interval between the closures or a physical contact hold. The manual's top/bottom names are physical positions. The VPX order is a software implementation of the shot.

The complete recordings, adapter, scenario, isolated states and frames are under `review-artifacts/data-east-star-trek-1991/follow-up-inputs/switch-test-evidence/`. The manifest SHA-256 is `c88f4ab0e6dbc6b00e0fc049329a846fc1a4f7cc8dabf7ada0b9fa5368a7d500`. The scenario, hashes and exact replay command are retained in that folder.
