# Bally Indianapolis 500 (1995) — A-18159 10 Opto P.C.B. connector list

Source: Midway Manufacturing Company *Indianapolis 500* operations manual (152-page image-only scan,
IPDB machine 2853 file `indy500manualfull.pdf`; the untouched download is retained as
`indy500manualfull.original-scan.pdf`), PDF page 138, printed page 3-20, the connector list below
the board outline (the outline is not reproduced in the crop). Read from the native 300 dpi render.

| Pin | Printed text |
| --- | --- |
| J1-1 | Not Used |
| J1-2 | Not Used |
| J1-3 | Gray-Green to A-18617-1 (LED) J1-3 Sw #45 |
| J1-4 | Gray-Black to A-18617-1 (LED) J1-4 Sw #44 |
| J1-5 | Gray-Orange to A-18617-1 (LED) J1-5 Sw #43 |
| J1-6 | Gray-Red to A-18617-1 (LED) J1-6 Sw #42 |
| J1-7 | Gray-Brown to A-18617-1 (LED) J1-7 Sw #41 |
| J1-8 | Key |
| J1-9 | Black Ground to A-18617-1 J1-9 |
| J2-1 | Not Used |
| J2-2 | Not Used |
| J2-3 | Orange-Green to A-18618-1 (Photo) J1-7 Sw #45 |
| J2-4 | Orange-Yellow to A-18618-1 (Photo) J1-6 Sw #44 |
| J2-5 | Orange-Black to A-18618-1 (Photo) J1-5 Sw #43 |
| J2-6 | Key |
| J2-7 | Orange-Red to A-18618-1 (Photo) J1-4 Sw #42 |
| J2-8 | Orange-Brown to A-18618-1 (Photo) J1-3 Sw #41 |
| J2-9 | Gray-Yellow +12VDC to A-18618-1 (Photo) J1-1 |
| J3-1 | Black Ground from J116-3 |
| J3-2 | Gray-Yellow +12VDC from J116-2 |
| J3-3 | Green-Blue from J207-6 |
| J3-4 | Green-Yellow from J207-4 |
| J3-5 | Key |
| J3-6 | Not Used |
| J3-7 | Not Used |
| J3-8 | White-Green from J209-5 |
| J3-9 | White-Yellow from J209-4 |
| J3-10 | White-Orange from J209-3 |
| J3-11 | White-Red from J209-2 |
| J3-12 | White-Brown from J209-1 |
| J4-1 | Gray-Orange to A-16908 (LED) Sw #63 |
| J4-2 | Not Used |
| J4-3 | Not Used |
| J4-4 | Key |
| J4-5 | Orange-Black to A-16909 (Photo) Sw #63 |
| J5-1 | Gray-Red to A-16908 (LED) Sw #62 |
| J5-2 | Not Used |
| J5-3 | Key |
| J5-4 | Not Used |
| J5-5 | Orange-Red to A-16909 (Photo) Sw #62 |
| J6-1 | Gray-Brown to A-16908 (LED) Sw #61 |
| J6-2 | Key |
| J6-3 | Black Ground |
| J6-4 | Gray-Yellow +12VDC |
| J6-5 | Orange-Brown to A-16909 (Photo) Sw #61 |

Printing notes, preserved literally:

- The board takes drive columns 4 (J207-4) and 6 (J207-6) and return rows 1-5 (J209-1..J209-5), so
  it serves switches 41-45 and 61-63. Switch 66 (column 6, row 6) is not on this board; its part is
  the separate A-20047 turbo opto board (`turbo-opto-pcb.md`).
- This page prints switch 63's LED and phototransistor as `A-16908`/`A-16909`, while the handbook's
  switch-locations list and items 12c/12d of the A-20038 turbo assembly print `A-14231`/`A-14232`.
- J2's phototransistor destinations run in the opposite pin order to J1's LED destinations (J2-3
  goes to `J1-7 Sw #45`, J2-8 to `J1-3 Sw #41`).
