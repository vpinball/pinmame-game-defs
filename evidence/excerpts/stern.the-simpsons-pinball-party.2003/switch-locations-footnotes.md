# The Simpsons Pinball Party — Switch Matrix Grid Locations, footnotes and schematics

Transcribed from `The_Simpsons_Manual.pdf`, PDF page 31, printed page 17,
"SWITCH MATRIX GRID LOCATIONS" (playfield diagrams: Upper Playfield/Upper
Right Corner inset, plus the main lower playfield), the "Typical Switch
Wiring & Schematic" and "Dedicated Switch Schematic" boxes, and the page's
footer legend and footnotes. `method: mixed` (page located via the OCR text
layer's printed footer, all content below read from a 150 dpi render).

## Mounting-location legend

`[white box]` = Switches mounted above the Playfield. `[black box]` =
Switches mounted below the Playfield. `[gray box]` = Switches mounted in the
Cabinet. Every switch number on the playfield diagrams is stamped inside one
of these three shaded boxes; the shading is reproduced in the printed switch
number values already captured in `switch-matrix-dedicated-switches.md`'s
"Location" field (Cabinet Side / Coin Door / In Cabinet vs. Above P/F / Below
P/F), so no separate coordinate transcription from the diagram is required
for identity purposes — normalized playfield coordinates come from the
retained VPX table geometry instead (see `vpx-geometry.txt`).

## Typical Switch Wiring & Schematic

Generic switch schematic: the column wire (labelled `GRN-XXX`, "Column:
Switch Drive Wire") feeds the `N.O.` (Normally Open Switch Terminal) leg to
`COM.` (Common Switch Terminal); a blocking diode (`1N4001`/`1N4001`) routes
from `COM.` to the `N.C.` (Normally Closed Switch Terminal) leg, which
connects to the row wire (labelled `WHT-XXX`, "Row: Switch Return Wire").

## Dedicated Switch Schematic

Dedicated switch inputs (`GRY-XXX`) run `N.O.` to `COM.` to Ground (`BLK`).

## Footnotes ("LEGEND NOTE:" block at page foot)

> **Switch Part Note:** ¥ Yen Coin Switch is 180-5091-00. Part numbers which
> start with 515- or 500- include the bracket, target, and/or housing.
> Targets: See Appendix I, Stand-Up Targets, for pictorial views. Switches are
> listed again in the Pink and Blue Pages and list the assembly and securing
> hardware they're used on.
>
> **Sw. 14 & 15 Part Note:** Transmitter & Receiver OPTO PC Boards are used
> for both Switches 14 & 15. Transmitter: 515-0173-00; Receiver: 515-0174-00.
>
> **Switch 56 Part Note:** The Switch is comprised of a Hanger Bracket
> (535-5319-00) and Contact Wire (535-7563-01) located in the Cabinet.
>
> **Some Switch Diodes are located under the playfield** on Terminal Strips
> or Diode Boards and not on the assemblies.
>
> **DOTS:** Diode On Terminal Strip *or* **DODB:** Diode On Diode Board (only
> if noted in the Matrix Grid).

This is the entirety of this manual's opto-identity evidence: switches 14 and
15 are the only two positions named as opto construction anywhere in the
document. There is no shaded-cell opto legend and no separate "Opto Assembly
Part Number" column distinct from "Switch Part Number" on this manual's
switch-matrix page (contrast the Williams WPC-95 manuals used earlier in this
project, which shade optos directly on the matrix and separate the two part
columns). Every other switch part number transcribed in
`switch-matrix-dedicated-switches.md` (180-51xx-xx, 500-6227-02,
515-59xx/6027-xx, 535-xxxx) is a leaf/microswitch/standup-target contact
assembly, not an opto.
