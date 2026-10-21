# Star Trek: The Next Generation — 2026-10-21 physical flasher corrections

Successor correction evidence for the Williams operations manual. The immutable external
`manual-transcription.md` remains pinned at SHA-256
`07f57792c7f405a5e59607a73ac73bb00f9b7daa91ede63477337d4a9ce8f948`; it is not
rewritten. Its earlier readings for the two items below are superseded by this reviewed
measurement record and the corrected committed manual excerpts.

The retained source record is
`external:pinmame-review-artifacts/star-trek-the-next-generation-1993/completion-2026-10-21/physical-measurements.json`,
SHA-256 `89bc8d628c9a8152a3e9f573f8a0e657ac444141381b719ced1b66a0b800d087`.
It reuses only the original 2026-09-25 page-93 affine registration (the old file's
SHA-256 is `1c7e0b9426222f0801dd2c58223ea21bd890565e3c76152bc37eab53e29dc49d`)
and explicitly supersedes that file's interpretations of solenoids 22 and 28. Coordinates
are player view: x=0 left, x=1 right, y=0 rear, y=1 front. They retain the original
fit uncertainty (RMS 0.0047, maximum 0.010; independent left-side checks reach maximum x
0.0161); new circle reads are accurate to about three page pixels.

The factory-manual scan and the two linked teardown photographs remain external. Copyright in
the photographs is retained by Robert Winter; copyright in the illustrated machine artwork is
retained by Williams Electronics Games, Inc. Rights and license are `NOASSERTION`. This excerpt
records only factual observations and hashes; it does not copy either photograph.

## Solenoid 22 — Middle Ramp Flasher

- The original manual PDF (SHA-256
  `7f626bce89556b2af4c80bf9eb1a5f74c72cbffe83a85b5142f17140bc820d86`), PDF 96,
  printed 2-44, reads `#89 (2)` in the playfield-bulb column. The previous committed
  table transcription's `#89(1)` was mistaken.
- On PDF 93 / printed 2-41, the two partially occluded circular bulb symbols behind the
  left outer-loop guide have full-page native-render centres `(1689, 559)` and `(1731, 560)`.
  The retained affine gives `(0.359, 0.054)` and `(0.400, 0.054)`.
- Robert Winter's original teardown photograph `44.jpg`,
  `https://robertwinter.com/pinball/restorations/sttng/teardown/44.jpg`, SHA-256
  `d7394b99bf22acd38ec58275098647dfc400cc7f06fce8fffdadb93543b2efd7`, shows two
  large playfield bulbs at that location. The photograph corroborates the socket identity
  and count; it supplies no coordinate.

## Solenoid 28 — Center Borg Flasher

- On PDF 93 / printed 2-41, the rear round bulb symbol has centre `(1873.3, 559.5)` and
  normalizes to `(0.536, 0.053)`; it is on the rear A-17160 board inside the Borg U.
  The front round bulb symbol has centre `(1870.0, 740.8)` and normalizes to
  `(0.533, 0.137)`; it is on the separate front A-17159 Single Flash Lamp PCB beside the
  coil/plunger.
- Robert Winter's original teardown photograph `33.jpg`,
  `https://robertwinter.com/pinball/restorations/sttng/teardown/33.jpg`, SHA-256
  `08d73a9ea758b0f8aefec2fa4c2ae7d8a85ae2e0b8432b5a8c9b1531d2c72846`, visibly shows
  the front A-17159 socket beside the coil and the rear A-17160 socket inside the U.
  It corroborates board identity and order; the manual drawing supplies both coordinates.

The factory manual remains the authority for physical construction, quantities, and drawing
coordinates. The physical photographs corroborate actual socket identity and fitment. The retained
VPX script remains runtime-binding authority and is not used to locate either flasher socket.
