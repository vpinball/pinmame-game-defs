# Creature from the Black Lagoon — Solenoid/Flasher Locations parts list

Transcribed from `Creature_From_The_Black_Lagoon_OPS.pdf`, PDF page 103, printed page 2-43,
"SOLENOID/FLASHER LOCATIONS". Read directly from a 300 dpi `pdftoppm` render.

| Item | Coil/Flasher No. | Assembly No. | Description |
| --- | --- | --- | --- |
| 01 | AE-23-800 | A-15769 | Top Right Popper |
| 02 | 24-8704 / 24-8802 (2) | A-8798 | Left Subway Enter Flasher (Playfield) / (Insert) |
| 03 | AE-26-1200 | A-15842 | Bottom Right Popper |
| 04 | AE-26-1200 | B-9362-L-2 | Ball Release |
| 05 | AE-27-1200 | A-14369-R | Right Slingshot |
| 06 | AE-27-1200 | A-14369-L | Left Slingshot |
| 07 | AE-23-800 | B-10686-1 | *Knocker |
| 08 | 24-8704 / 24-8802 (2) | A-8798 | Bottom Right Flasher (Playfield) / (Insert) |
| 09 | 24-8704 (2) | A-8798 | Top Left & Right Flashers |
| 10 | 24-8704 / 24-8802 (2) | A-9359 | Bowl Flasher (Playfield) / (Insert) |
| 11 | 24-8802 (2) | --- | Hologram Creature Flasher (Insert) |
| 12 | AE-27-1200 | A-8039-3 | Outhole |
| 13 | AE-26-1200 | A-9415-2 | Top Left Jet |
| 14 | AE-26-1200 | A-9415-2 | Top Right Jet |
| 15 | AE-26-1200 | A-9415-2 | Bottom Jet |
| 16 | 24-8704 / 24-8802 (2) | A-8798 | Right Popper Slide Flasher (Playfield) / (Insert) |
| 17 | 24-8704 / 24-8802 | A-8798 | Bottom Left Flasher (Playfield) / (Insert) |
| 18 | 24-8704 / 24-8802 (2) | A-8798 | Right Ramp Flasher (Playfield) / (Insert) |
| 19 | 24-8704 / 24-8802 (2) | A-8798 | Left Ramp Flasher (Playfield) / (Insert) |
| 20 | --- | A-15541 | †Sequential G.I. #1 |
| 21 | 14-7977 | A-15988 | †Hologram Push Motor 48VAC |
| 22 | 24-8704 / 24-8802 (2) | A-8798 | Center Hole Flasher (Playfield) / (Insert) |
| 23 | SM1-2B-900-DC | A-16042 | †Up/Down Ramp (up) |
| 24 | --- | A-15541 | †Sequential G.I. #2 |
| 25 | 24-8704 (2) | A-9302 | Left & Right Start Movie Flashers |
| 26 | AE-26-1200 | A-16042 | †Up/Down Ramp (down) |
| 27 | 14-7977 | A-15988 | ΔCreature Mirror Motor 48VAC |
| 28 | 24-8826 | A-15857 | ΔHologram Light |

## General Illumination Circuits (printed on the same page)

| Item | Bulb type | Description |
| --- | --- | --- |
| *01 | 24-8829 (#86) | Sequential G.I. #1 |
| *02 | 24-8768 #555, 24-6549 #44 | Insert/Playfield Middle |
| *03 | 24-8768 #555, 24-6549 #44 | Insert/Playfield Upper |
| *04 | 24-8829 (#86) | Sequential G.I. #2 |
| *05 | 24-8768 #555, 24-6549 #44 | Insert/Playfield Lower |

## Flipper Coils (printed on the same page)

| Coil | Assembly | Description |
| --- | --- | --- |
| *FL-15411 (Orange) | A-15205-L-4 | Lower Left Flipper |
| *FL-11629 (Blue) | A-15205-R-2 | Lower Right Flipper |

Footnotes: `* Not shown` / `† Located under playfield` / `Δ Located in cabinet bottom`. Legend:
"Square indicates coil or P.C.B.", "Circle indicates flasher".

**Solenoids 20 and 24 are the same printed name ("Sequential G.I. #1"/"#2") as General Illumination
items 01 and 04**, but they are two different circuits on the same A-15541 board: GI-01/04 are the
GI-triac power buses that light the chase bulbs (see `solenoid-flasher-wiring.md` for their separate
GI-side connectors and driver transistors, Q18/Q15), while solenoids 20/24 are the board's own 2-bit
address-select lines (driven from a different pair of transistors, Q36/Q32) — the physical read-out of
pinned PinMAME's own driver comment describing "a 2 bit decoder wired on solenoid outputs 20/24" that
selects one of four physical chase-light groups powered through "GI outputs 1/4" (1-based, i.e. GI
addresses 0 and 3 zero-based). Both share assembly A-15541 and both are marked `†` (under playfield),
which is why the manual reuses one board name for two electrically distinct connector positions.

**Items 27 (Creature Mirror Motor) and 28 (Hologram Lamp) are both marked `Δ` "Located in cabinet
bottom"** — genuinely cabinet-mounted devices, not playfield hardware, even though their visible
effect (a hologram image that appears to float above the playfield) reads as a playfield feature.

**Item 11 (Hologram Creature Flasher) prints only an Insert connection, no Playfield entry at all** —
unlike every other dual-mount flasher on this page (02, 08, 09, 10, 16, 17, 18, 19, 22), which print
both Playfield and Backbox/Insert connections. This is the only single-mount, insert-only flasher on
the page, confirming it is a backbox-insert-panel device with no playfield bulb.

Item 09 ("Back Flashers", quantity 2) prints only a Playfield voltage connection (no Backbox column
entry), unlike the paired dual-mount flashers above; "Back" here reads as the rear of the playfield
itself (upper play field near the backboard), not the cabinet backbox.
