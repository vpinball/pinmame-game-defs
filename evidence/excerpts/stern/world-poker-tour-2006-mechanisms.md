# Stern World Poker Tour (2006) — manual mechanism excerpts

**Status: factory-manual transcription, cross-checked by curator on key assembly pages.** This is a bounded transcription and inventory for a high-tier curator. It does not resolve conflicts, assign VPX geometry, assign normalized coordinates, or decide runtime/emulator semantics.

## Evidence envelope

| Field | Value |
| --- | --- |
| Source / attribution | *World Poker Tour Manual* / Stern Pinball |
| PDF SHA-256 | `4cf31702805e75d37aef1c0c1624426000fec6cabf71a47e27691f5d5f8b6d01` |
| License | NOASSERTION |
| Method | Visual inspection of PDF pages and derived `tools/render_excerpt_image.py` renders; text extraction only secondarily cross-checked. |
| Transcriber / model | GPT Terra manual-research worker (Codex session 2026-09-30) |
| Review distinction | Images/pages named below were visually checked by the transcriber. Every fact remains a candidate pending high-tier curation. |
| Spatial rule | The manual’s “upper/lower,” “left/right,” “above/below P/F,” and drawing statements are kept as source language; no x/y coordinates are supplied or inferred. |

Section 4 was visually inspected from PDF pages 98–120 (printed Section 4, Chapter 2 pp. 74–94). Page 120 / printed p. 94 is a section-ending blank page. PDF p121 is the Section 5 contents (printed p. 95), not another Section 4 parts sheet.

### Render provenance

All images are in `terra-renders/assemblies/`, include source PDF one-based page in their name, derive from the original PDF, are attributed Stern Pinball / NOASSERTION, and are candidate/unreviewed. Primary outputs for p99–105, p107, p111, p114, p116, and p117 were invalid 2×2 images because a page-covering 1-pixel XObject made the primary renderer calculate 0 dpi. Their named **vector-fallback** images instead use the supplied renderer module’s `_legible_vector_dpi` type-size-derived resolution (not a fixed dpi); these were visually checked.

| PDF / printed locator | Visually checked render (SHA-256) | Scope |
| --- | --- | --- |
| 98 / Sec.4 Ch.2 p.74 | `wpt-p098-full.webp` `46b639b766cd4c2a1fc65e24961e3c28e232d08faaaf85175cf373f27dee00f5` | rails, brackets, switch gates |
| 99 / p.75 | `wpt-p099-vector-fallback.webp` `98c81aedd02fa2d950affeade1010a62b523b4ef7f700f6b4c99286c87fa1486` | pop-eject VUK |
| 100 / p.76 | `wpt-p100-vector-fallback.webp` `501dcc9fcef62b1e03842130e684b0ba92a5bbae28efefebc48d7ef249bd6f92` | shooter-lane VUK |
| 101 / p.77 | `wpt-p101-vector-fallback.webp` `d41fb207ccd6f2f1e858570ef93d54d6c44e4fa7e97472173abe3bd0ad2944c7` | shooter tube / wire ramp |
| 102 / p.78 | `wpt-p102-vector-fallback.webp` `1c0f62e9b73388992c69b03d9f6f0032f9e9c2c7624a50f50b6ae2cc57197208` | upper playfield / right wire ramp |
| 103 / p.79 | `wpt-p103-vector-fallback.webp` `eb8da5febf829abc9b424334b6e0efc289441037d04685722449f58881c0324f` | right steel and wire ramps |
| 104 / p.80 | `wpt-p104-vector-fallback.webp` `e4beba20e41baa0b5b21472c51177e3bc6bf8020fef6654ba32ac745cb386a1d` | left-ramp up post |
| 105 / p.81 | `wpt-p105-vector-fallback.webp` `8a83b1cc9491b3674dcb5b3c115585715374033a21a1a04fd15b0d944942d06f` | Reverse-O-Matic / left ramp |
| 106–107 / p.82–83 | `wpt-p106-full.webp` `099600acd579b216a2cb4fc116c0e192631ffc595d01940fe1294f9c621590c9`; `wpt-p107-parts-table-vector-fallback.webp` `31ce1ab1bb50af239639f68cfba089399fee06e675f9b0e2dcec5d8ae2b387dc` | 4-bank drop-target assemblies and whole parts table |
| 108–111 / p.82a–85 | `wpt-p108-full.webp` `9ecfed7e326e14a6a2fb852118e8444803c5ac0e21bc8d1ebf2c698f5d7a9060`; `wpt-p109-full.webp` `2f7baeca93ad857104c6cd9ef761b9a7a7aecde50a3ebbdfcb988978bbb723f7`; `wpt-p110-full.webp` `e72acf0ae82a2262edff30e307190dc88c5b29e83fad0435227e9f277949b2a8`; `wpt-p111-vector-fallback.webp` `2566ab41a9cda322b82c4d20d83931b50ec6f1d3e383e16f2430ea3e3adb49ac` | 4-/8-bank drops and 8-bank parts |
| 112–113 / p.86–87 | `wpt-p112-full.webp` `75fd281c06462a20965714e94112c09a5c85c80b952f7f2a60f0b7f745133ad6`; `wpt-p113-full.webp` `0b1cb1e3dee007b51ac41424fca2781570dcf8b7c4bc0c0a4c7380e7989d13b7` | back panel and individual parts |
| 114–115 / p.88–89 | `wpt-p114-vector-fallback.webp` `d4126e1eae1e1e85fe380af979e963aa1e9e4f0edf1a33c68b49f9c0d8183f13`; `wpt-p115-full.webp` `bddef7b23100862c888ecd2d784a80db67cdf1aadaa248d2913cd1980ec5fb88` | Ace-in-the-Hole / Mouse Trap |
| 116–117 / p.90–91 | `wpt-p116-vector-fallback.webp` `ae2cc84a30879dbf152d863a39981efc371981a2df95dc5182c5c23b2d081b4c`; `wpt-p117-vector-fallback.webp` `18f2cce5916ec1ba82ae337c13788195638fa4c2d7993d808548c3b9adce0f13` | left VUK and tube |
| 118–119 / p.92–93 | `wpt-p118-full.webp` `d80fbc90cb8b97c1afb30d497eebe9c7b07f1cd107b0cd88126174516e8152b6`; `wpt-p119-full.webp` `ccda6994f2c34556ccdf76e87aebb2405069b9de63696ad004c9ff0ff288a027` | down post / transfer trough |

## Complete device / assembly inventory

| Manual device or assembly (literal) | Evidence locator | Source-address/device fitment (candidate) |
| --- | --- | --- |
| Right orbit switch gate asm. 515-6556-03A (reference 515-6556-03) | p98 / p.74 | SW.50; micro switch 180-5087-00; wire form gate and bracket are included. |
| Left orbit switch gate asm. 515-6556-03A | p98 / p.74 | SW.44; micro switch 180-5087-00. |
| One-Way Gate Asm. 515-7491-00 (Left Orbit) | p98 / p.74 | Wire gate 535-9674-00; bracket 535-9672-00. |
| 10 PT Switch Assembly 515-7492-00 | p98 / p.74 | SW.14 and SW.41; slingshot switch (standard lugs) 180-5054-00; diode 1N4004 / 112-5003-00. |
| VUK (at Eject Popper) Assembly 500-6867-01 | p99 / p.75 | SW.49; coil 26-1200 / Q21 (no diode); micro switch 180-5209-00. Manual says its 1N4001 switch diode is on a terminal strip under the playfield, not the assembly. |
| VUK (at Shooter Lane) 500-6867-01 | p100 / p.76 | SW.3; coil 26-1200 / Q3; micro 180-5209-00; 1N4001 diode statement as above. |
| Shooter Tube & Shooter Wire Ramp | p101 / p.77 | SW.51; micro switch 180-5010-01 with 1N4004; Q31 flash is drawn on this sheet. |
| Upper Playfield & Right Wire Ramp | p102 / p.78 | SW.53 source drawing; right wire ramp 515-7480-00; wire form gate (left hand style) 535-9375-00; micro 180-5010-01; protect plate 535-6539-00. |
| Right Steel Ramp & Right Wire Ramp | p103 / p.79 | SW.52 source drawing; Transceiver OPTO PCB Assembly 2, 500-6775-00. |
| Ball Deflector (Left Ramp Up Post) Assembly 500-6657-06-ND | p104 / p.80 | Q20; coil 25-1240, no diode. |
| Reverse-O-Matic Ramp & Left Wire Ramp | p105 / p.81 | Left ramp weldment 515-7479-00; Rev-O-Matic steel ramp asm. 515-7481-00; Transceiver OPTO PCB Assembly 2, 500-6775-00. |
| 4-Bank Drop Target (Mid. & Right) Assemblies 500-6946-04 (Qty. 2) | p106–109 / pp.82–83a | Middle source drawing SW.10–13; right drawing SW.7–4. Reset coils: 23-800 / Q7 and Q8, no diode. |
| 8-Bank Drop Target (Left) 500-6946-08 | p110–111 / pp.84–85 | SW.33–40; two 23-800 reset coils / Q5 and Q6, no diode. |
| Back Panel | p112–113 / pp.86–87 | Contains explicitly listed VUK (Left), VUK tube, transfer trough/optos, Ace-in-the-Hole, stand-up targets, GI and flash lamps. |
| Ace-In-The-Hole / Mouse Trap Assembly 500-6902-00 | p114–115 / pp.88–89 | Q12 26-1200 (no diode); Q19 27-880 mini coil (no diode); SW.57/SW.58/SW.63 diagrams; transmitter 520-5247-00 and receiver 520-5248-00. |
| VUK (Left) Assembly 500-6867-01 | p116–117 / pp.90–91 | Q4 26-1200; SW.55 and SW.56 on source drawing; tube/wireform details below. |
| Down Post Ball Stop 500-6969-00 | p118 / p.92 | Q32; coil 25-1240, no diode / 090-5034-ND. |
| Transfer Trough & Optos | p119 / p.93 | Transfer trough weldment 515-7483-00; two Transceiver OPTO PCB Assemblies 500-6775-00. Source drawing labels SW.54. |

## Contact construction reconciliation

Primary Sol curator visually checked PDF p98 / printed p74 and p101 / printed p77 on 2026-09-30. The p98 10-point assembly drawing shows the exposed stacked leaf blades of slingshot switch 180-5054-00, fitted at SW14/SW41. The p6 chart identifies the same exact part at SW26/SW27, two contacts per slingshot; the leaf classification follows the part's drawn construction, not the slingshot label alone.

The p101 shooter-tube parts table explicitly calls 180-5010-01 a micro switch with a 1-5/8-inch flat actuator. The p6 chart identifies that same part at SW9/SW51/SW53, so all three share this construction. In contrast, p6 gives only 180-5015-04 for bumper switches SW30–32; no retained WPT assembly drawing establishes their contact construction, which stays unknown.

## Whole parts-table transcriptions

### 4-bank drop target — p107 / printed p.83

| Item | Literal part / description | Qty. | Part number / fitment |
| ---: | --- | ---: | --- |
| 1 | Frame & Pem Weldment, 4-Bank D/T | 1 | 515-7547-04-88 |
| 2 | Target Rest Ledge (Black), 4-Bank D/T | 1 | 545-6163-04 |
| 3 | Drop Target (Black Plastic) Rollover | 4 | 545-6162-00 |
| 4 | Compression (Short) Spring | 4 | 266-5029-00 |
| 5 | Reset (Long) Spring (Red Dipped) | 4 | 265-5003-02 |
| 6 | PCB, Slotted OPTO X4 | 1 | 520-5252-04; harness 036-5507-20-88 Middle; 036-5507-21-88 Right |
| 7 | Compression (Return) Spring | 1 | 266-5020-00 |
| 8 | Steel Plunger | 1 | 530-5719-00 |
| 9 | Target Lift (4-Bank) Bracket | 1 | 535-9760-04 |
| 10 | Coil Mounting Bracket | 1 | 535-9761-00 |
| 11 | Spring Washer | 1 | 269-5002-00 |
| 12 | Coil 23-800 [NO DIODE] | 1 | 090-5001-ND |
| 13 | Coil Sleeve (1.69 OAL) | 1 | 545-5411-00 |
| 14 | Bracket Plunger Stop | 1 | 515-7548-00 |

### 8-bank drop target — p111 / printed p.85

| Item | Literal part / description | Qty. | Part number / fitment |
| ---: | --- | ---: | --- |
| 1 | Frame & Pem Weldment, 8-Bank D/T | 1 | 515-7547-08-88 |
| 2 | Target Rest Ledge (Black), 8-Bank D/T | 1 | 545-6163-08 |
| 3 | Drop Target (Black Plastic) Rollover | 8 | 545-6162-00 |
| 4 | Compression (Short) Spring | 8 | 266-5029-00 |
| 5 | Reset (Long) Spring (Red Dipped) | 8 | 265-5003-02 |
| 6 | PCB, Slotted OPTO X4 | 2 | 520-5252-04; harness 036-5507-19-88 |
| 7 | Compression (Return) Spring | 2 | 266-5020-00 |
| 8 | Steel Plunger | 2 | 530-5719-00 |
| 9 | Target Lift (4-Bank) Bracket | 2 | 535-9760-04 |
| 10 | Coil Mounting Bracket | 2 | 535-9761-00 |
| 11 | Spring Washer | 2 | 269-5002-00 |
| 12 | Coil 23-800 [NO DIODE] | 2 | 090-5001-ND |
| 13 | Coil Sleeve (1.69 OAL) | 2 | 545-5411-00 |
| 14 | Bracket Plunger Stop | 2 | 515-7548-00 |

### Back-panel individual-parts tables — p112–113 / printed pp.86–87

| Item | Literal part / description | Qty. | Part number / printed fitment |
| ---: | --- | ---: | --- |
| 1 | Back Panel Wood | 1 | 525-5643-00 |
| 2 | Down Post (Ball Stop) | 1 | 500-6969-00 |
| 3 | Cover Gray Molded Plastic NO DECALS | 1 | 545-6236-00 |
| 4 | Kit Plastics incl. 830-6052-00 | 1 | 803-5000-88 |
| 5 | Kit Decals includes -15, -16, -17 | 1 | 802-5000-88 |
| 6 | 2-Lug Staple Down Socket (for GI) | 7 | 077-5000-00 |
| 7 | #44 Bulb Heavy Filament | 7 | 165-5000-44-HF |
| 8 | 3-Lug Stand-Up Socket Med. Bracket | 4 | 077-5008-00 |
| 9 | #44 Bulb Blue Heavy Filament | 4 | 165-5053-05-HF |
| 10 | Mini-Mars Lite Cover Red Tabs | 5 | 550-5031-02 |
| 11 | #89 Bulb Clear Heavy Filament | 5 | 165-5000-89-HF |
| 12 | 2-Lug Stand-Up Short Socket | 5 | 077-5101-00 |
| 13 | Ace-In-The-Hole Asm. items 1–24 | 1 | 500-6902-00 |
| 14 | VUK (Left) Assembly items 1–11 | 1 | 500-6867-01 |
| 15 | VUK Tube Weldment Asm. items 12–20 | 1 | Individual Parts Only |
| 16 | Transfer Trough & OPTOs | 1 | Individual Parts Only |
| 17 | Stiffener Bracket Left | 1 | 535-9792-01 |
| 18 | Stiffener Bracket Right | 1 | 535-9792-00 |
| 19 | Guard Bracket (3.38x1x2.5H) | 1 | 535-9800-05 |
| 20 | Guard Bracket (8.25x1x2.5H) | 1 | 535-9800-02 |
| 21 | White S-U Target 1in Sq. Lugs Left | 1 | 515-7497-08-00 |
| 22 | Wht. Stand-Up Target 1in Sq. Lugs Rt. | 1 | 515-7497-08-01 |
| 23 | Wht. Stand-Up Target Rect. Lugs Rt. | 1 | 515-7498-08-01 |
| 24 | Switch Back Plate | 3 | 535-6452-00 |
| 25 | Foam Pads | 3 | 626-5029-00 |
| 26 | OPTO Amplifier PCB with Spacers | 2 | 520-5239-01-ASY |
| 27* | 1/2 Clamp (single) | 1 | 040-5000-06 |

### Ace-In-The-Hole / Mouse Trap parts — p115 / printed p.89

| Item | Literal part / description | Part number |
| ---: | --- | --- |
| 1 | Housing Top | 535-9659-00 |
| 2 | Housing Bottom | 535-9663-00 |
| 3 | Coil Holder Bracket | 535-9664-00 |
| 4 | Coil Retaining Bracket | 515-7489-01 |
| 5 | Spring Washer | 269-5002-00 |
| 6 | Coil 26-1200 [NO DIODE] | 500-6976-00 |
| 7 | Coil Sleeve | 545-5031-01 |
| 8 | Plunger with Knob Clevis Pin | 530-5703-00 |
| 9 | Bar Shaft Long | 530-5700-00 |
| 10 | Bar Shaft Short | 530-5700-01 |
| 11 | Grooved Clevis Pin | 530-5702-00 (Qty. 2) |
| 12 | Bar Shaft Support Block Nylon | 545-6234-00 |
| 13 | Large Return Spring | 266-5086-03 |
| 14 | Plunger Lock | 530-5701-00 |
| 15 | Latch | 535-9661-00 |
| 16 | Dowel Pin | 515-5004-00 |
| 17 | Small Return Spring | 266-5086-01 |
| 18 | Lock Spring Seat | 545-6235-00 |
| 19 | OPTO U Transmitter PCB | 520-5251-00 |
| 20 | OPTO Transceiver PCB (Top) | 520-5247-00 |
| 21 | Fiche Insulator Pad | 545-6173-00 |
| 22 | OPTO Receiver PCB (Bottom) | 520-5248-00 |
| 23 | Mini Coil Retaining Bracket | 535-9662-00 |
| 24 | Mini Coil 27-880 [NO DIODE] | 500-6976-01 (direct reference 090-5072-05) |

### Left VUK tube parts — p117 / printed p.91

| Item | Literal part / description | Part number |
| ---: | --- | --- |
| 1–11 | VUK Assembly | 500-6867-01 |
| 12 | Wood Block Spacer | 525-5648-00 |
| 13 | Front VUK Tube Weldment | 515-7555-00 |
| 14 | Wireform for Gate & End Flapper Asm. | 535-9667-00 |
| 15 | Wireform for Lift Gate | 535-9657-00 |
| 16 | Door Bracket Pivot Flap | 535-9655-00 |
| 17 | Torsion Spring | 267-5002-00 |
| 18 | Grooved Clevis Pin | 530-5702-01 |
| 19 | Transceiver OPTO PCB | 500-6775-00 |
| 20 | Deflector Pad/Bump | 545-5428-00 |

### Transfer trough — p119 / printed p.93

| Item | Literal part / description | Qty. | Part number |
| ---: | --- | ---: | --- |
| 1 | Transfer Trough Weldment Assembly | 1 | 515-7483-00 |
| 2 | Transceiver OPTO PCB Assembly | 2 | 500-6775-00 |

## Candidate-only mechanical and ball-path statements

These are verbatim/near-verbatim source topology statements, deliberately not converted into inferred geometry or a complete graph:

- p100/p101: a ball is delivered “up into Shooter Tube”; p101 says “Ball exits Shooter Tube onto the ‘Upper Playfield’ ... via Shooter Wire Ramp.”
- p103: “Ball can enter the ‘Upper Playfield’ ... via the Right Steel Ramp and can exit from the ‘Upper Playfield’ onto the Right Wire Ramp (another exit is through the Back Panel).”
- p104: “Ball can be stopped (locked) in the Left Wire Ramp.”
- p114: “Ball can be locked” in the Ace-In-The-Hole mechanism after required hits against the bars.
- p116: the left VUK drawing says a ball is transferred from the lower playfield to the upper playfield.
- p118: “Ball can be locked before entering upper playfield via Right Ramp.”
- p119: “Ball can exit from the upper playfield through this (another exit via Right Wire Ramp).”

## Questions for the high-tier curator (no resolution made)

1. **SW.54 conflict / possible shared labeling:** DR. 4 names SW.54 “LEFT RAMP MADE,” but the p105 left-ramp diagram and p119 transfer-trough diagram both label SW.54 around 500-6775-00 opto material. Trace wiring/physical fitment before selecting a canonical device mapping.
2. **SW.53 scope:** DR. 4 names SW.53 “UPF EXIT,” while p102 labels SW.53 on the Upper Playfield & Right Wire Ramp drawing. The language may be compatible, but the exact physical trigger needs curation.
3. **Coil #21 wiring glyph:** DR. 8 prints the control-line cell as “WHITE [printed directional/slash glyph] VIO-GRN.” The Q21 step-up board schematic (PDF p168 / printed Section 5 Ch.4 p142) documents VIO-GRN at J1-P1, WHT at J1-P4, and YEL-VIO to J10-P9/10 at J1-P5; preserve the original glyph until a curator resolves how to normalize it.
4. **Optional Q24:** The exact printed power connection is visually “J16-P4>8”; source also calls it OPTIONAL COIL / Opt. 5v. Do not create a mandatory device without corroboration.
5. **GI count:** Circuit 3 is printed “9* #44 Bulb,” and the asterisk says GI quantities may change during production. Treat the count as production-variable.

## Visually unchecked or intentionally not converted

The cited Section 4 assembly pages and address-table source pages were visually checked. I did **not** transcribe every non-functional fastener/callout from drawings into this inventory, nor convert drawing placement to coordinates; those remain available in the original pages/renders. Wiring figures p123–129 and p132 were visually inspected for scope, but their full graphical wire routes have not been redrawn into an inferred netlist. No OCR was run: the installed environment has no Tesseract executable, and visual renders plus PDF text were legible for the entries recorded here.
