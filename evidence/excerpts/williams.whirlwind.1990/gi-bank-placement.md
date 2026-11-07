# Whirlwind three-bank GI: two measured socket apertures

The factory `Whirlwind_OPS.pdf`, PDF 83/printed 73, shows two unfilled
round apertures between the lower jet bumpers and three-bank target slot.
The adjacent circles with floral interiors are plastic posts. Stock
photographs independently show a fitted #47 bulb in each of the two
unfilled apertures; see `gi-stock-sockets.md`. These are two physical
positions even though the supplemental Bigus renderer supplies only one
GI candidate, Light81, in this region.

Coordinate source: native 2473x3273 `hi-083.png`, SHA-256
`74d2e9fd5823471dc42a45efca2cc83aa1ff9306b7de1e1465940c8fb2cec70a`,
retained under `external:pinmame-manuals/by-machine/williams.whirlwind.1990/`
`archive-arcademanual_Whirlwind_OPS/render/hi-083.png`.
The right-hand drawing has crop origin (1384,327), size 915x1964.
The accompanying image is the native box (1630,925,1800,1120), converted
to grayscale and WebP quality 70 without resizing: 170x195, 6950 bytes,
SHA-256 `34df6f5c3236c95553d2f7431bcf71a7fc3e0179442f6f1fcbe3f7fb0b30406d`.
The repository curator visually checked both the native source and a marked 4x crop.

| Physical aperture | Full-page pixel | Normalized x,y |
| --- | --- | --- |
| Rear of the pair | 1712,1033 | .381,.364 |
| Front of the pair | 1725,1052 | .397,.375 |

The source reads have approximately 2 px uncertainty. The committed
`tools/seeds/williams/whirlwind-1990-gi-bank-callouts.json` retains all nine
independently read mechanism controls and their exact VPX object hashes.
`drawing_callouts.measured` reproduces both coordinates from those
controls. Both apertures lie inside their convex hull. The affine fit's
normalized RMS is .0106364 and maximum leave-one-out error is .0374155.
Measured coordinates are rounded to three decimals. This is the same
factory page and mechanism calibration used for the six measured
flashlamp circles; the aperture reads are separate from those circles.
The measured apertures are not checked against themselves.

For full-page pixels u,v, the fit is:

```
x = .0012246135663693367*(u-1384) - .00001182511786664532*(v-327) - .012243619630393977
y = .000014432178870973248*(u-1384) + .0005773826714006729*(v-327) - .04858408563252357
```

These are regional physical measurements. The separate reviewed
`gi-playfield-inventory.md` establishes both sockets on lower output 16 and
the complete circuit inventories from physical wiring/voltage evidence.
No output quantity or circuit membership is derived from Light81, the
pair's location, or these coordinates alone.
