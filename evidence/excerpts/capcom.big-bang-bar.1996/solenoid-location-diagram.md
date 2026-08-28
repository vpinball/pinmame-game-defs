# Transcription: Capcom Big Bang Bar operators manual, printed page 82 (PDF page 86) — playfield location drawing callouts

Source: `manual.capcom.big-bang-bar.1996` (SHA-256 `5fc11391e3092298e31775fdff5944554fc78db2bdb9240aa39fa9eab5dabca5`),
"SOLENOIDS, MOTORS, & FLASHERS" page: the numbered location drawing printed
beside the Ref./Description/Part Number table. The companion image is the full
drawing region (backbox box above, playfield below) at native resolution — a
page-scale drawing whose callouts are spread across the whole frame.

Every numbered callout visible in the drawing, with the position its balloon
occupies (rear = top of the playfield drawing, apron = bottom):

- **Backbox box** (the wide rectangle above the playfield):
  - **21** — Backbox Left flasher: balloon at the box's left-centre.
  - **22** — Backbox Right flasher (the unnumbered row that shares solenoid 22
    with "TUBE DANCER"): balloon at the box's right-centre.
  - **3** — Knocker: balloon at the box's top-right corner.
- **Playfield drawing**:
  - **14** (Ramp Diverter 1): balloon on the left edge below callout 15, leader
    pointing at the diverter wall at the rear-left of the playfield. Balloon
    centre measures to normalized playfield space (x/952, y/2162) at
    approximately (0.133, 0.067) — see the measurement block below.
  - **15** (Ramp Diverter 2): balloon at the top-centre-left, leader pointing up
    the ramp; measures to approximately (0.258, 0.034).
  - **27** (Orbit Gate Left): balloon right of 15; measures to approximately
    (0.292, 0.050), corroborating the retained table's gate-left placement
    (0.290, 0.047) to within about 0.013 normalized units.
  - **28** (Orbit Gate Right), **16** (Alien Lock Post), **25** (Aliens flasher),
    **31** (Aliens Forward Motor), **32** (Aliens Reverse Motor): cluster at the
    top-right alien area.
  - **29** (1-Bank Reset): right of the alien figures.
  - **22** (Tube Dancer — the numbered half of the shared address) and **30**
    (Tube Dancer Motor): balloons inside the large circular feature at the
    rear-left-centre of the playfield — the physical Tube Lady assembly stands
    on the playfield here, in a clear tube. The circle measures to approximately
    (0.245, 0.139), corroborating the retained table's tube-dancer placement
    (0.252, 0.133) to within about 0.008 normalized units.
  - **18 / 20 / 19** (Star Bumper Left / Right / Middle): three balloons inside
    the three bumper rings — **18 leftmost, 20 upper-right, 19 lower-centre**,
    exactly the left/right/middle identity the definition records.
  - **23** (Dance Floor flasher): centre of the bumper cluster.
  - **13** (Island Diverter 1), **24** (Eject Hole flasher), **12** (Eject Hole),
    **11** (Upper Right Flipper): right side, mid-playfield.
  - **7** (4-Bank Reset): left edge, mid-playfield.
  - **4** (Left Slingshot) and **8** (Lower Lock Post): bottom-left sling area,
    **5** (Right Slingshot): bottom-right sling area, **26** (Lower Lock
    flasher) beside 4.
  - **9** (Left Flipper) and **10** (Right Flipper): balloons at the two flipper
    pivots; **6** (Kickback) bottom-left; **2** (Trough) bottom-right; **1**
    (Outhole) at the drain.
- No knocker, flipper, or diverter callout appears anywhere else; in particular
  the drawing places **no** flasher, motor, or solenoid hardware outside these
  positions.

## Measurement record (for the two diverter callouts)

- Source render: `Capcom_1996_Big_Bang_Bar_Manual.pdf` page 86 rendered at
  400 dpi (3307 x 4390 px full page; the page's embedded scan raster is 4960 px
  across 8.27 in, so 400 dpi is below native — sufficient for balloon centres,
  which are measured to +-10 px).
- Playfield-frame corners measured on the 400 dpi render:
  - top-left inner corner (1730, 1333)
  - top-right inner corner (2883, 1333) (right edge measured at the same height)
  - bottom-left inner corner (1762, 3860)
  - bottom-right inner corner (2883, 3860)
- Normalization formula: `x = (px_x - 1730) / 1153`, `y = (py_y - 1333) / 2527`.
- Cross-check: callout 27 measures (0.292, 0.050) against the retained table's
  gate-left object (0.290, 0.047) — agreement to ~0.005-0.013 normalized units,
  which is the honest precision of balloon-centre measurement.
- Each measured point is a **remote callout balloon centre**, not a device
  symbol; the balloon sits beside its device with a leader line, so balloon
  coordinates are corroboration evidence (declared tolerance ~0.02-0.05), never
  the primary coordinate source. The primary coordinates for every placement in
  this definition come from the retained VPX extractions.
