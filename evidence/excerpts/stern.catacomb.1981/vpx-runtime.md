# Retained Catacomb runtime and geometry

Source: UnclePaulie Catacomb 2.0.1 VPX, published 2024-09-27 at https://vpuniverse.com/files/file/21750-catacomb-stern-1981/ . VPX SHA-256 `aa4566613123d8e511228497715d8c0bec0e68cc2ebc5fd2fb584e9c36a4628c`; embedded script `177b7d10a092f82b8b8f00faee2c495eed5cb1353f01bccb20a529ef344055c5`. The release credits UnclePaulie, Hauntfreaks' scan, Redbone's graphics, VPW testing and prior HSM/lander code. NOASSERTION: original source retained locally, not redistributed.

Method: curator inspection of exact script handlers, collections, TimerInterval fields and exported world bounds, checked against manual tables and ROM traces. The pinned corpus script hash differs (`5a814437d836211da377be4ebfd91be242043b8f97d4897d86e32c5942de5e6b`); it is not substituted for the embedded bytes. vpxtool git:v0.33.3 extraction manifest: `e173f51a4b8c1dc3ea328b41dc6ad732307cf2ae5c13e0f2b98616b0cebc77a7`.

## Actual switch anchors

| Public | Script-bound object | Method |
| --- | --- | --- |
| 4 | Spinner sw4 | Spin pulse |
| 5 | Trigger sw5 | Hit/Unhit |
| 9 | Bumper1 | Hit pulse |
| 10 | Bumper2 | Hit pulse |
| 11 | Wall UpperSlingshot | Slingshot pulse |
| 12 | Wall LeftSlingshot | Slingshot pulse |
| 13 | Wall RightSlingshot | Slingshot pulse |
| 14-16 | Walls sw14, sw15, sw16 | Bank A drop animation; shared backbox TriggerB14-16 |
| 17 | Kicker Drain | Hit closes; output9 transfers ball and clears switch |
| 18-21 | Triggers sw18, sw19, sw20, sw21 | Hit/Unhit |
| 22-24 | Walls sw22, sw23, sw24 | Bank B drop animation; shared backbox TriggerB22-24 |
| 25,26 | Triggers sw25, sw26 | Hit/Unhit |
| 27 | HitTarget sw27 | Hit handler; paired with animated sw27p |
| 28 | Trigger sw28 | Hit pulse and star28 animation |
| 29 | Trigger sw29 | Hit/Unhit |
| 30-32 | Walls sw30, sw31, sw32 | Bank C drop animation; shared backbox TriggerB30-32 |
| 33 | Kicker BallRelease | Hit/Unhit |
| 34 | Kicker Slot1 | Hit/Unhit |
| 35 | Kicker Slot2 | Hit/Unhit |
| 36,37 | Kickers sw36, sw37 | Hit/Unhit; captive holes |
| 38-40 | Walls sw38, sw39, sw40 | Bank D drop animation; shared backbox TriggerB38-40 |

The modern 2.0.1 embedded script asserts matrix8 from `LeftFlipperKey` at lines654-659 and clears it from the same key at lines695-700, both while `BackBoxActive = True`. Its right-button handlers instead move `BFlipper`. This agrees with the manual's left button for stopping bank lights. The pinned corpus copy has the same key assignment. Only the older archive script (SHA-256 `5bfe5cf522707fa6375d4b465b91b500479c82b2d9d7818e60e962e4502cc06a`, lines1545-1563) asserts and clears8 from `RightFlipperKey`; that is an older table defect. Backbox TriggerB objects and VR mirrors are simulation/render surfaces, never main-playfield coordinates. The older archive table also has duplicate sw2_Dropped handlers where bank-B handlers belong; its geometry cannot repair those runtime bindings.

## Outputs

Callbacks6 knocker,7 left kickout,8 right kickout,9 drain reflex,10 ball release,11-14 banks A-D,19 game-on and20 backbox enable match the retained controller contract. Output20 enables the rendered bagatelle and remains enabled through button strokes. Synthetic46/48 are main right/left flipper callbacks; the core publishes paired45/47 simultaneously. Table-owned smaller yellow ball, gravity changes and animation delays do not establish physical dimensions, coil strength or timing.

## Mapped lamps and actual emitters

`vpmMapLights AllLamps` maps only collection members and takes their public number from TimerInterval. The complete mapped address set is 1-12,14-15,17-28,30-31,33-44,46-47,49-60,62. Every mapped address except2 has the pair lN/lNa; public2 has only l2. Those doubles do not add sockets. The raw fixture retains every member and timer value, so names alone cannot establish a binding.

The modeled bulbN primitive belongs to the corresponding insert and supplies its own world-space center. OBJ exported with `vpxtool export obj --units vpu`, SHA-256 `0b45efc7b8cb54f51b85f3aa541776b635e9ea653b6ddd7e99e309e4b90a84f0`. Original bounds: left/top0, right952.941, bottom1976.471. Normalize x/952.941 and y/1976.471, rounding to six decimal places, matching the repository spatial helper.

Public2 maps l2 at apron-left (156.89035,1877.9075), with no corresponding physical bulb mesh. The older script calls its proxy a backbox light. Neither proves a socket; factory Q12 routes to PLAYFIELD J1-19. Public29 has no mapped light although Q15/J2-23 exists. Both loads stay unknown. Backbox legends13,45,61,63 use callbacks/reels. Shoot Again11 also drives a backbox legend. The three spinner-1000 inserts are15,31,47, as the factory IC/code table shows.

The GI collection contains light maps and lane/top glow helpers; membership is not a socket count. The separate GIBulbPrims collection contains 21 explicit meshes: Bulb_Prim_001-011,014,017,021,025-029,031,032. Two bumperbulb meshes add two modeled lamps. lstar28 can only be projected onto its button assembly, not presented as a measured socket. Photographs show lower-post illumination not represented by those 21 meshes and do not expose all lamps under plastics/apron. Total factory GI quantity and individual hidden positions remain incomplete.

## ROM corroboration

Five fresh-state runs are retained under review-artifacts/catacomb-1981/harness; complete manifest `e6d32edeb3ed3a6e7ae4e0f0de713892a1a32e650b8a3b5a02bfebd214f32ab8`. ROM archive SHA-256 `6e133f54cb093ecb65fc2ad80346fe55c63973479a539dafea6c7c479034b48e`; every program/voice member matches pinned stgames.c SHA-1. Library SHA-256 `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`, built from46e1a01a0f73dc5ce163d98db1ae435883ecc450. Host switch readbacks are excluded from conclusions.

Original run scenarios retain their exact Windows CRLF bytes and hashes beside each raw trace. Reusable repository copies use LF. The facts fixture pins both byte hashes; evidence-enabled tests require the original bytes, the repository bytes and parsed JSON equality. The runtime evidence's scenario locator refers to the retained original, not a byte-identical claim about the normalized copy.

Coil test reads display0 at250ms after each callback: printed1-19 maps to public2,1,6,7,3,4,5,8,11,12,14,13,9,10,19,15,17,20,18 in repeated cycles. Switch test displays each address1-40 during its own public1 closure; transient multiplex glyphs are not additional switches. Gameplay9-13 fires1-5; completing banks A-D fires11-14; drain17 fires9; Start raises19. Right82 publishes45/46; left84 publishes47/48. Returning the third ball to33 with34/35occupied drops19 and raises20 in the bonus/backbox phase.20 stays enabled through the later82button probe. This proves the sustained feature state, not the physical relay-coil harness path.
