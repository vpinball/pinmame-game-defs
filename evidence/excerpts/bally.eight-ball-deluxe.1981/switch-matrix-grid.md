# Switch matrix grid (playfield wiring schematic W-1192-28C)

Source: `Eight_Ball_Deluxe_OPS.pdf`, PDF page 41 (drawing W-1192-28C, "WIRING DIAGRAM - PLAYFIELD").
Image crop: `switch-matrix-grid.webp`, the leftmost three switch-matrix columns and the five direct
"ST 0"-"ST 4" (A4J2-1 through A4J2-5) connections at the bottom of the sheet.

This crop is a drawing (a wiring diagram), not a printed table, so it is retained as an image per
the excerpt policy rather than transcribed as prose. It independently confirms the harness-derived
switch identity and address rule recorded in `review-artifacts/eight-ball-deluxe/manual-transcription.md`:
the matrix is laid out as exactly five columns of eight rows (row returns A4J2-8 through A4J2-15,
labeled 0-7 in the margin), and reading the visible three columns column-major reproduces the
Switch Assembly Self-Test table exactly:

- Column 1 (leftmost, rows 0-7): 2X/3X/4X/5X IN LINE DROP TARGET, IN LINE BACK TARGET, [row 5 has no
  playfield switch -- self-test 06 CREDIT BUTTON is a cabinet/door switch and does not appear on
  this playfield-only sheet], TILT, OUTHOLE -- self-test 01-05, 07-08.
- Column 2 (rows 4-7 visible in this crop): "A"/"B"/"C"/"D" ROLLOVER LANE -- self-test 12-15.
- Column 3 (rightmost visible, partially cropped): 2/3/.../7 DROP TARGET through 30 POINT REBOUND --
  self-test 17-24.

This confirms `address = (column - 1) * 8 + row + 1` (columns 1-5, rows 0-7) reproduces the printed
Self-Test # for every switch on the sheet, and that self-test # equals the public controller
address (established independently by the LibPinMAME harness run, `swtest2.json`). The bottom of
the sheet additionally shows five direct, non-matrix connections (ST 0 through ST 4 at A4J2-1
through A4J2-5) that are outside the 5x8 matrix entirely; this curation did not need them, since
none of switches 1-40 fall there.
