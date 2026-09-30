# WHO dunnit spatial blockers

Retained VPX SHA-256 `a0f18c07f98ec7dce96cc030eb11af11a0c28d0d1cffb5390744067b9221e2a9`; script `034fe6483660fbc9516aa15a4727d8dc6da0cfb3db0321b0c1357523967ccd44`; 631-file extraction manifest `0fd20d012d8219583a8222b51a0997ca4876247cc9ec19352e5a06d270d3643c`; manual `5fa08344d905c9730c86c6baee79b43e6a4a1c4e2230f67a08c2973b57bc714e`.

Bounds: `left=0 top=0 right=953 bottom=2128`. x=object_x/953; y=object_y/2128; player view, rear y=0, apron y=1; values rounded to six decimals.

141 devices have VPX candidates; 0 used devices lack even a candidate. The 46 newly projected mechanism/actuator devices remain physically unplaced: a shared assembly anchor is not a hidden contact, coil, or bulb centre. Backbox flasher branches and the complete G.I. socket census remain unmeasured.

## Retained registers and projection classes

The [VPX object register](../../../tools/seeds/bally/who-dunnit-1995-spatial.json) has SHA-256 `e6c9f386a0e7b420893cd4736b89236ef3e25c68b36067ca4b743508588bd885`; the [G.I. bulb-mesh register](../../../tools/seeds/bally/who-dunnit-1995-gi-candidates.json) has SHA-256 `feb5185273d8f36596e75ec7753a4ff1a1d962a001005593c8b14bc38ae999d1`. The [reviewed geometry register](../../../tools/seeds/bally/who-dunnit-1995-geometry.json) has SHA-256 `4ece3a02cc9b7b579c062a79a0b8d3c3fc73cfc71de691c77d1897bfccc18035` and 47 candidate records. The JSON form embeds their source hashes, world-VPU or polygon centre definitions, projection classes, and uncertainty.

- **switch (48 candidate devices):** Exact-name VPX collision object centre for matrix switch or F5 Spinner, candidate only; cabinet, EOS and always-closed positions use controlled not_applicable.
- **lamp (60 candidate devices):** Exact LNN VPX Light centre, candidate only. L16/L17/L18 glow helpers are excluded; the factory location drawing on PDF 125 still needs device-by-device socket reconciliation.
- **gi (3 candidate devices):** Script collection members GI_Left/GI_Right/GI_Top with bulb mesh; 11/10/28 retained. Other collection members are glow/reflection leads, not sockets. Factory GI socket quantity is unknown. All five strings' table wiring/bulb/location claims and backbox exclusions remain candidate: the board layout shows J120/J121, but PDF 158–159 omits J112–J127 pin destinations and supplies no branch/placement corroboration.
- **actuator (30 candidate devices):** Named VPX mechanism anchor or visible effect projection only. No projection is called a hidden winding, motor body or physical bulb centre.
- **flasher_and_coil (0 candidate devices):** 46 formerly unplaced devices now have 47 candidate VPX mechanism projections. World-transformed OBJ bounds locate collidable primitives. Cup, reel, target, ramp, post and flipper anchors are not hidden coil or sensor centres; flasher domes and named Light proxies are not proven bulb centres. Backbox branches have no invented playfield point.
- **manual_drawing (0 candidate devices):** PDF 127 switch and PDF 125 lamp plans have separate affine fits and visually checked symbol controls. Tiny residuals can reflect a VPX author tracing the manual and do not prove independent physical accuracy. The PDF 129 actuator overlay is rejected: it reused the PDF 127 frame although page 129 has a different scale/origin. No balloon centre is used as a device coordinate.

## Unresolved physical geometry

- No complete factory G.I. socket census or backbox/cabinet bulb coordinates. G.I. table locations remain candidate without J120/J121 destination corroboration; PDF 158–159 omits J112–J127 connector-list entries.
- Hidden trough optos, reel indexes, bank/ramp limit contacts, coil bodies and flipper E.O.S. contacts have only whole-mechanism or output-effect projections.
- PDF 129 actuator/flasher overlay is invalid until its own frame is fitted; candidate VPX points carry no manual-page-129 reconciliation claim.
- One derivative VPX lineage and manual diagrams do not establish all physical centres or prototype geometry.

## Missing placements

None. Every used device has a candidate or controlled non-playfield status.
