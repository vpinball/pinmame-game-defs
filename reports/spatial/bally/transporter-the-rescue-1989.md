# Transporter the Rescue spatial audit

Status: partial; remaining coverage gaps are polarity and spatial placement.

Bounds: [0, 0, 952.965, 1976.52]. x / 952.965, y / 1976.52, rounded to six decimals.
Extraction manifest SHA-256: `adbdad05e280be0e58c2364cf9d0992b20624da4ad280ce1ee5001e839818165`.

Table coordinates are centres or documented mean wall drag points. Fourteen switch placements are independently checked against their own factory callout; the report records both affine residuals. Each jet switch 60-62 excludes its own Bumper object from the control fit, using the other four controls; these per-placement fits and offsets are recorded alongside the separate leave-one-out callout check. Measured factory drawing points are observed, never checked against the same page. Coils project onto their own mechanism; matrix-lamp art anchors stay candidate. Rear-panel domes project explicitly to y=0 from raw negative y values.
GI placements are show-bulb-mesh members of the retained GI collection; the table groups both factory circuits under output 9, so these do not prove physical socket count.

Recorded placements: 132.

## Omitted spatial records

- device.ball-lock-flasher
- device.single-standup-flasher
- device.ball-popper-flasher

## Blockers

- Backbox GI output 22 lamp-on/off polarity is unestablished; the source identifies its relay coil but not its load contacts, and the retained script has no independent callback.
- Factory GI socket quantity is not proved; the 33 table bulb meshes are observations only.
- Apart from six physical socket observations at lamps 1 and 4-8, playfield matrix-lamp anchors remain candidate art-effect positions; multi-bulb inserts 13/14/40 especially need individual physical socket evidence.
- Solenoid flashers 29, 30 and 31 have physical counts but no unambiguous bulb/socket centre in the retained model or location drawing; their spatial keys stay omitted.
- Factory-drawing measurements and unconfirmed table placements remain observed; the report records each checked placement's own affine residual.

## Drawing reconciliation

A placement is validated when its own callout on the factory location drawing (each callout paired with at most one placement of its label, nearest first) lands within 0.07 normalized of it under two least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements measured on a drawing are never checked against it. When a checked placement's own table object is also a control, that object is excluded and its control offset is recomputed from the other four controls; the independent fit and excluded object are recorded per placement.

Checked 14; agreeing 14.

The factory lamp drawing marks insert regions rather than individual sockets. Six socket bases at lamps 1 and 4-8 are observed on the original raised-playfield photograph; their affine photo fit and uncertainty are in the JSON report. Other retained photographs include intact plastics or partial underside views and cannot prove exhaustive GI fitment or separate the two sockets behind inserts 13/14/40. These gaps remain spatial blockers, with no invented physical-machine conflict.
