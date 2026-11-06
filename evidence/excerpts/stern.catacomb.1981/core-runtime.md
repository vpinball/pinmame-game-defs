# Catacomb diagnostic and synthetic-display transport

Source: PinMAME revision `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. Method: curator transcription and inspection of the pinned source. Attribution: PinMAME contributors; GPL-2.0-or-later.

`src/wpc/by35.h:230` defines `BY35_SWCPUDIAG` as `-6`. `src/wpc/by35.c:475-481` labels the block "Diagnostic buttons on CPU board" and drives the NMI line from that switch. The alternative LISY branch reads the physical S33:

```c
#ifndef LISY_SUPPORT
  cpu_set_nmi_line(0, core_getSw(BY35_SWCPUDIAG) ? ASSERT_LINE : CLEAR_LINE);
#else
  cpu_set_nmi_line(0, lisy35_get_SW_S33() ? ASSERT_LINE : CLEAR_LINE);
#endif
```

`src/libpinmame/libpinmame.cpp:875-955` enumerates the game's layouts and detects whether one is DMD or video. It reserves an additional slot, including for segment-only games. When `!hasDMDOrVideo`, it creates an additional DMD generated from segment data with `PINMAME_DISPLAY_TYPE_DMD`, width128, height32 and depth2. The update path at lines740-743 likewise describes a custom DMD generated from segment displays. This is a synthetic rendering of the score/credit/ball segment data, not a physical backbox playfield renderer or a seventh physical display.
