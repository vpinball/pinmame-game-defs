# Mata Hari fixture photographs and parts catalog

## 1979 Bally Parts Catalog, printed pages 40–41

The Mata Hari spread is PDF page 21 in the PinWiki-hosted scan. Page 40 draws left and right drop-reset callouts 14/15 at the outer lower ends of the banks, one on each side. It draws the panel tilt callout 07 on the player-left side rearward of the sling. Other 07 locations include the cabinet. The following is the complete printed solenoid assembly list in numerical order.

| No. | Description | Part |
| --- | --- | --- |
| 1 | Outhole Kicker | AR-26-1200 |
| 2 | Knocker | AR-26-1200 |
| 3 | Chime 10 | CN-31-2000 |
| 4 | Chime 100 | CN-31-2000 |
| 5 | Chime 1000 | CN-31-2000 |
| 6 | Chime 10,000 | CN-31-2000 |
| 7 | Bottom Left Thumper-Bumper | AN-26-1200 |
| 8 | Top Left Thumper-Bumper | AN-26-1200 |
| 9 | Top Right Thumper-Bumper | AN-26-1200 |
| 10 | Bottom Right Thumper-Bumper | AN-26-1200 |
| 11 | Left Slingshot | AN-26-1200 |
| 12 | Right Slingshot | AN-26-1200 |
| 13 | Top Saucer | AO-27-1300 |
| 14 | Left Drop Target | NO-26-1900 |
| 15 | Right Drop Target | NO-26-1900 |
| 16 | Coin Lockout Door | FO-36-7000 |
| 17 | K1 Relay (Flipper Enable) | AQ-25-500/34-5050 |

FO 579 names the outhole part AN-26-1200. Both charts identify the same load. The diagram shows K1 in the backbox as well as the flipper locations, and FO 579 associates the printed dual-winding part in row 17 with the flippers. The catalog's printed test order remains distinct from the public addresses.

## Photo observations

- Jason Charlton's `braid02.jpg` shows a distinct green 2X and yellow 3X bulb to the player's left and a colourless 5X and amber shoot-again bulb to the player's right. Their apertures map to the arrowhead-side table objects in the 1978 extraction. Registration uses independently read sockets of round inserts as controls. The replacement Braid and sockets locate the apertures. The production underside photo shows the corresponding four socket assemblies, and A5/A6 ties them to feeder circuits 60, 44, 28 and 43. The reported positions are observed VPX coordinates supported by the apertures.
- Vic Camp's IPDB photo 34409 shows the two-screw mounting point of the weighted tilt contact on the player-left side. The weight projects further toward the apron in the oblique photo. Use the screw mount for the observation and retain FO 579 and the 1979 diagram for identity. Placement is approximate because the underside is photographed obliquely.
- The same underside photo shows both reset coils at their outward ends. The centre of each visible wrapper projects to `(136.3, 857.5)` and `(723.7, 873.6)` VPU. The end-of-bank square callouts 14 and 15 in the 1979 catalog register within 17 VPU per axis of the photos. Their own fit against 15 controls has a maximum leave-one-out residual of 10.6 VPU per axis. The callouts corroborate the bank ends and the elevated coils limit the photo fit to coarse observed actuator effect anchors `(0.14, 0.44)` and `(0.76, 0.45)`. The unrounded left y lies just below the 0.445 boundary.
- Mark Clayton's bare playfield photo, IPDB 50997, shows distinct upper and side inserts for A and B. The head and shaft render objects for each side arrow correspond to one insert. Its side socket remains occluded in the available production underside photograph.
- The rebuilt underside shows the fourth arrow's 3,000 fixture. [Pinball Restorations LLC's LED-restored machine #3](https://pinball-restorations.com/product/almost-ready-1978-bally-mata-hari-3/) shows the 3,000 arrow and both upper caps lit, with the 2X/3X/5X arrows dark. The VPX models assign these same three to GI, and the factory feature routing assigns them no public address. Their exact factory feed remains an inference. [Original lit photograph](https://pinball-restorations.com/wp-content/uploads/2024/07/DSCN1111.jpg)
- The original production underside shows four wired sockets under the side guides at full-image pixels `(89,952)`, `(109,863)`, `(787,929)` and `(780,832)`. The two VPX builds and the original bare-board openings corroborate their approximate locations. These are a visible part of the GI run. The full harness and individual factory socket count remain open.

The registration seed records the control pixels, fixed matrices and target reads. `braid-register.py`, `under-fit.py`, and `top-fit.py` under `review-artifacts/bally.mata-hari.1977/online-followup` retain the original fit and overlay procedures. The 1K control sits well forward of the arrow sockets and has a 54.2 VPU leave-one-out y residual. Omitting it shifts arrow projections by up to 6.2 VPU in x and 11.6 VPU in y and selects the same VPX object for each of the four sockets. The production underside tilt fit has leave-one-out component maxima of 16.4 VPU x and 20.9 VPU y. The projected mount is approximately `(0.222, 0.578)` in player view.
