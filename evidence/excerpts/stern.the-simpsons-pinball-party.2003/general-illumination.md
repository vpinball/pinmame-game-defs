# The Simpsons Pinball Party — General Illumination Circuit Detailed Wiring Diagram

Transcribed from `The_Simpsons_Manual.pdf`, PDF page 121, Section 5 Chapter 2,
printed page 103, "General Illumination Circuit Detailed Wiring Diagram".
`method: mixed` (page located via the printed footer in the OCR text layer;
diagram content read from a 150 dpi render). This is a schematic drawing, not
a table, so it is also captured as a rendered crop.

## Relay topology

One `G.I. RELAY` is driven from the `I-O POWER DRIVER BOARD 520-5137-01`: a
`U206 74HCT273` data latch bit feeds a `1K` resistor into `Q200 2N3904`
("RELAY DRIVER") transistor, which energizes the relay coil (`D229 1N4004`
flyback diode across it). The relay's contacts (pins 1/3/2/4, switched
together by the single coil across pins 8/5/6/7) close **all four** fused
G.I. branches simultaneously — a single-relay, multi-fuse design, not four
independently switched circuits. This matches pinned PinMAME's SE driver,
which sets `coreGlobals.nGI = 1` and exposes exactly one aggregate GI channel
(public address 0) for Whitestar hardware.

## Fused branches (secondary 5.7v AC from the transformer, via J14/J15)

| Circuit | Fuse | J15 pin | Wire | Location | Bulbs (per diagram, `*` = quantity may change) |
| --- | --- | --- | --- | --- | --- |
| 1 | F24 | P1 (BRN-WHT/WHT-BRN) | WHT-BRN | On Backpanel | 10 ea. #44 (`#10*`) |
| 2 | F25 | P2 (WHT-YEL/YEL) | WHT-YEL | Left P/F x10, Rt. Bot. x1, above P/F Rt. Return Lane Spot x1 | 11 ea. #44 + 1 ea. #555 (`#12*`) |
| 3 | F26 | P3 (WHT-GRN/GRN) | WHT-GRN | Upper Mini-P/F x7, above P/F Spotlights x5, US Coin Door x2 (Euro x1) | 7 ea. #44 + 5 ea. #555 + coin-door bulbs (`#13*`/`#14*`) |
| 4 | F27 | P4 (WHT-VIO/VIO) | WHT-VIO | Right Playfield x12 | 12 ea. #44 (`#12*`) |

Footer note: "G.I. Bulb quantities may change during production." Playfield
map callouts on the diagram itself: yellow dots (`Y`) mark circuit-2 bulbs
including "GIs above, Rt. Return Lane" and "GIs above, Rt. Return Lane Spot";
green dots (`G`) mark circuit-3 bulbs including "GI above P/F X1 Spotlight
Bart" and "GIs underneath the Upper Playfield X7 + X3 Spotlights"; violet
dots (`V`) mark circuit-4 bulbs on the right playfield; brown dots (`B`) mark
circuit-1 backpanel bulbs ("Gls above Playfield on Backpanel X10").

The retained VPX table's own `GI` collection (42 members: `GI_1`.."GI_37"
Light objects plus `spotlightright`, `spotlightright1`-`spotlightright4`) is
used as the placement set for the canonical single GI device rather than a
hand-count from this diagram's approximate, asterisked quantities; both
describe the same single-relay GI, and this diagram corroborates the general
above/below-playfield/backbox split rather than fixing an exact bulb count.

## Crop

`general-illumination.webp`: `The_Simpsons_Manual.pdf` page 121, crop box
`0.06,0.03,0.98,0.97` of the page, rendered at 150 dpi with `pdftoppm`,
reduced to 750px wide grayscale, quality 60 WebP (75,960 bytes) — the full
diagram (schematic plus playfield location map) described above.
