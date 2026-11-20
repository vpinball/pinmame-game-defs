# Rear-panel lamp diagnostics

The lamp-test name table in each of the four supported display programs identifies the same five addresses. The table starts at display-image offset 0x15CAD in A0.27, 0x15CB6 in A1.06 and 0x15D2E in both A1.09 and A3.00. Entry 1 is the 2X lamp. Each successive entry is a two-byte little-endian pointer to a zero-terminated name in the same 64 KiB half of the image. Read entry `n` at `table + 2 × (n − 1)`.

| Matrix address | Display diagnostic | Factory lamp matrix, printed p. 26 |
| --- | --- | --- |
| 36 | BACKBOX #5 | Backbox #5 |
| 44 | LEFT RAMP (GREEN) | Left Ramp Red |
| 45 | LEFT MILLION (RED) | Left Million Green |
| 63 | RIGHT MILLION (RED) | Right Million Green |
| 64 | RIGHT RAMP (GREEN) | Right Ramp Red |

In the original-machine photo `pf_ST-Playfield-01.jpg` (SHA-256 `702344700875c72f9188bf5ec15f99ee5a6dc1fec80bfd2983037a6b882b2dce`), the rear panel has green lenses at both outer RAMP legends and red lenses at both inner MILLION legends. The factory position drawing on printed p. 27 places 44, 45, 63 and 64 in that order from the player's left. The retained VPX script also gives 44 and 64 green covers and 45 and 63 red covers. The matrix's printed color words are reversed for these four addresses. Its function and position assignments agree with the installed legends.

All four display programs name the backbox load on 36. A test label can name a circuit with more than one bulb. The label alone cannot determine whether the playfield callout on p. 27 shares that circuit.
