# Scared Stiff — Lamp Matrix and Lamp Locations

Transcribed from `Scared_Stiff_OPS.pdf`, PDF pages 107-108, printed pages 2-42/2-43, the Lamp Matrix
and Lamp Locations. Produced by rendering the retained PDF at 300-600 dpi with `pdftoppm` and reading
the tables directly; this scan's text layer is garbled multi-column OCR and was never trusted.

Column wiring (Yellow-x): 1 J121-1/Q96, 2 J121-2/Q100, 3 J121-3/Q95, 4 J121-4/Q99, 5 J121-5/Q94, 6
J121-6/Q98, 7 J121-7/Q93, 8 J121-9/Q97. Row wiring (Red-x): 1 J125-1/Q104, 2 J125-2/Q108, 3
J125-4/Q103, 4 J125-5/Q107, 5 J125-6/Q102, 6 J125-7/Q106, 7 J125-8/Q101, 8 J125-9/Q105.

| Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Stiff Level 7 | 21 | Stiff Level 8 | 31 | Crate Left Eye | 41 | Left Leaper | 51 | Ramp Item | 61 | Laboratory Item | 71 | Web Award 7 | 81 | Web Award 15 |
| 12 | Stiff Level 6 | 22 | Stiff Level 9 | 32 | Crate Center Left | 42 | Left Ramp Jackpot | 52 | Coffin Multiball Item | 62 | Crate Item | 72 | Web Award 8 | 82 | Web Award 16 |
| 13 | Stiff Level 5 | 23 | Scared Stiff | 33 | Crate Center Right | 43 | Light Lock | 53 | Leaper Item | 63 | Skull Item | 73 | Web Award 9 | 83 | Web Award 1 |
| 14 | Stiff Level 4 | 24 | Center Leaper | 34 | Crate Right Eye | 44 | Ramp Right Eye | 54 | Coffin Spotlight | 64 | Web Award 2 | 74 | Web Award 10 | 84 | Left Skull Lane |
| 15 | Stiff Level 3 | 25 | Three Bank Lower | 35 | Left Outlane | 45 | Right Outlane | 55 | Shoot Again | 65 | Web Award 3 | 75 | Web Award 11 | 85 | Center Skull Lane |
| 16 | Stiff Level 2 | 26 | Three Bank Middle | 36 | Right Leaper | 46 | Skill Shot | 56 | Lock Lamp | 66 | Web Award 4 | 76 | Web Award 12 | 86 | Right Skull Lane |
| 17 | Stiff Level 1 | 27 | Three Bank Upper | 37 | Right Ramp Jackpot | 47 | Crate Jackpot | 57 | Left Loop Center | 67 | Web Award 5 | 77 | Web Award 13 | 87 | Buy In |
| 18 | Ramp Left Eye | 28 | Spider Popper | 38 | Light Spin Spider | 48 | Extra Ball | 58 | Left Loop Upper | 68 | Web Award 6 | 78 | Web Award 14 | 88 | Start Button |

Sixteen "Web Award" lamps span 64-68, 71-78, 81-83 (5 + 8 + 3 = 16), all within the ordinary 8x8
matrix — not a separate auxiliary column. Every one of them (and only these sixteen, plus none of
84-88) carries the printed `*Located in backbox` annotation on the Lamp Locations (continued) page
(PDF 108); 84/85/86 (Skull Lanes) and 87/88 (Buy-In/Start, cabinet) are not asterisked.

Bulb/assembly numbers: `24-8768` = `#555` bulb, `24-6549` = `#44` bulb (playfield inserts use
`#555`; backbox/cabinet items mostly use `#44`, per each row). No lamp in this table uses a `(2)`
suffix (unlike Monster Bash's 12/24/31/43); the LAMP MATRIX page's "STIFF LEVEL" ladder (11-17,
21-22) is nine individually addressed lamps, one per rung, not a shared multi-bulb position.

## Undocumented auxiliary lamp columns 91-98 / 101-108

Pinned `ss.c`'s `ssGameData` declares `/*lampCol*/2` (two auxiliary lamp columns beyond the standard
8x8 matrix), driven through a pair of HC4094 serial shift registers clocked by solenoids 37/38 ("Aux
Lamp Clock"/"Aux Lamp Data"). The driver's own comment calls this "2 extra lamp columns for the LEDs
of rev. 0.1" and says the matching 16-LED board "was not kept in the production build" — but the
retained production manual (part `16-50048-101`, Sept. 1996, 1.5 ROM) still prints solenoids 37/38
with real connectors and wire colors (not "NOT USED"), and the Lower Playfield Parts page (PDF 105)
still lists item 6 `A-21287-1 "16-LED Skull Driver PCB Assy."` This is recorded as an unresolved
authoring-critical gap: PinMAME's own driver enumerates public lamp addresses 91-98 and 101-108, but
no source available here can name what (if anything) is fitted there.
