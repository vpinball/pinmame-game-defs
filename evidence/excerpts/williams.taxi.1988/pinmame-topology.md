# Taxi pinned PinMAME topology

Managed PinMAME revision 8371478a7640f1896dcdf565aed340dc5df989ba. Canonical files src/wpc/s11games.c:644..706, src/wpc/s11.c:537..580,644..662,780..804,1100..1110, src/wpc/core.h:216, src/wpc/core.c:2173 onward and core_updateSw, src/wpc/gen.h:19..21.

All seven native drivers select init_taxi. taxi_l4 is the Lola L-4 root; L-3, LU-1 Europe, LG-1 German, P-5 prototype and the two L-5C competition revisions are clones. Firmware-year 2016 is not the machine manufacture year.

```c
static core_tLCDLayout dispTaxi[] = {
  DISP_SEG_16(0,CORE_SEG16), DISP_SEG_16(1,CORE_SEG8),
  {2,0,21,7,CORE_SEG7SCH},{0}
};
INITGAME(taxi, GEN_S11B, dispTaxi, 12, FLIP_SWNO(58,57),
         S11_LOWALPHA | S11_DISPINV, S11_MUXSW2)
```

GEN_S11B aliases GEN_S11X=0x100. DISP_SEG_16 expands to row*4, column 0, memory start row*20, length 16. Physical display index 0 has start 0/length 16; index 1 start 20/length 16; index 2 start 21/length 7 is the Jackpot/Meter. Index 3 is a synthetic 128x32 alpha-on-DMD renderer, not a fitted DMD. Overlapping segment starts are intentional layout addressing.

Taxi muxSol=12: updsol sends first-byte output bits to public 25..32 while relay 12 is on, otherwise 1..8. S11_MUXSW2 overwrites switch 2 with core_getSol(12); the manual has no switch fitted at 2. Williams setSSSol uses permutation {5,4,1,2,0,3}: PIA handler slots 0..5 drive public 22, 21, 18, 19, 17, 20. Independently, factory PDF 72 prints Sol. No. 17..22 and Solenoid Type "Special #1".."Special #6" on those same six rows. These are two literal factory fields, not PIA slot aliases. The public physical identities 17..22 agree with the factory rows and retained callbacks; they are not derived from a slot ordinal. Slot 4 drives Left Jet 17. Taxi ssSw[] is zero: no simulator-driven/direct special-solenoid override. No simulator, custom solenoid getter, or nonzero custom-output count is installed.

The matrix row PIA reads core_getSwCol directly, with zero per-game inversion mask. Public 1 is active for ordinary contacts and drop-bank sensors in the retained script and ROM switch edges. Drop sensors are optos, but their matrix contact rests open; beam rest alone does not define polarity.

FLIP_SWNO(58,57) installs cabinet-wired flippers. core_updateSw copies public 82 right cabinet button to matrix 57, public 84 left to 58. Drive 82/84; direct writes 57/58 are overwritten. Public 81/83 are EOS namespace slots, 85..88 upper-flipper slots: Taxi has no separately readable EOS or upper flipper. Synthetic outputs 45/46 right and 47/48 left are distinct public states; 46 and 48 are the compatibility callbacks used by S11.VBS. The real FL11630 dual winding/EOS loop is locally wired and enabled by 23.

Public 23 is game-enable, not a coil. 24 is unused. Taxi has no WPC/SAM flipper-output or sound-overlay route, so 33..44 read zero; 49..50 simulator outputs have no Taxi simulator. Custom 51..64 are absent from the exact Taxi contract. Output 22 can pulse in the ROM coil diagnostic although its physical load is Not Used. A test pulse never proves fitment.

Output-type initialization assigns inverse #44 GI behavior to 10/11 and #89 flasher behavior 15/16,25..32. Relay state 1 cuts GI, state 0 restores GI. This is an output effect, not permission to invert controller switch values.
