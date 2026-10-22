# Baywatch controller routing

Pinned authority: PinMAME `97aa922bf8e4b6970126192ec1ac1fb0305a4f62`. Direct source read by primary curator. These are factual extracts of the named symbols, not a reconstruction from a sibling game.

- `degames.c` 1441 onward: Baywatch CPU Rev 3b, DMD Type 3, two 512K display ROMs, 64K CPU ROM. `INITGAMES11(baywatch,GEN_DEDMD64,de_192x64DMD,FLIP6364,SNDBRD_DE2S,SNDBRD_DEDMD64,S11_PRINTERLINE)`. The seven clones all reuse `init_baywatch`. `input_ports_baywatch` uses `input_ports_des112` (DE_COMPORTS2, momentary green).
- `gen.h`: GEN_DEDMD64 = `0x8000`. This is the Data East derived platform, not Whitestar.
- `degames.c` INITGAMES11: flipper fields come from FLIP6364 = FLIP_SWNO(63,64); `sxx.muxSol` is 10; `hw.swCol`, `lampCol`, `custSol` are zero; no custom getSol, no simulator, and zero inversion mask.
- `s11.c` `pia4b_w`: a Data East matrix strobe selects only its first set bit. `pia4a_r` returns `core_getSwCol(locals.swCol)` without complementing it. `core.c` default sequential conversion is n+7, making matrix numbers 1-64 column-major, not WPC decimal addresses.
- `s11.c` `setSSSol`: the Data East permutation is `{3,4,5,1,0,2}`. `pia1ca2_w` slot 0 => public 20; `pia1cb2_w` slot 1 => 21; `pia3ca2_w` slot 2 => 22; `pia3cb2_w` slot 3 => 18; `pia4ca2_w` slot 4 => 17; `pia4cb2_w` slot 5 => 19. These are active-low PIA outputs gated by ssEn. The ROM's own cycling test pairs the printed names with 17-22.
- `s11.c` `updsol`: latch2200 drives 1-8; PIA0:B drives 9-16. With mux relay 10 on, the low byte moves to 25-32. These are alternate loads behind K1, not independent power stages. `pia0cb2_w` publishes the enable at S11_GAMEONSOL=23. No state producer exists at 24.
- `s11.c` `pia2b_w`: on GEN_DEDMD64 with S11_PRINTERLINE, `extSolPulse=data`. `core_getSol` maps that byte to public 37-44, even though PWM slots use another internal numbering. The comment explicitly names bit 0 as CN3 pin 9, bit 1 as pin 8, bit 2 as pin 7 and bit 7 as pin 1. Its literal `....` elides bits 3-6: no connector-pin assignments for those bits are established here, and no skipped pin is inferred. No printed machine load is assigned here. The tried Portals printout did not move these states; non-observation is not proof of unused addresses.
- `core.c` `core_updateSw`: without FLIP_SOL, cabinet buttons from internal column 11, public 82 and 84, are copied to matrix 64 and 63 on every update. The public matrix writes are overwritten. While enable 23 is active, button 82 fabricates outputs 45 and 46 together; 84 fabricates 47 and 48 together. No independent winding timing is modelled. Without upper FLIP_SW bits or FLIP_EOS, inputs 81/83/85-88 are neither copied nor synthesized; the eight-bit row read cannot select column 11.
- `core_getSol`: Data East has no output path for 33-36; 49 is a simulator shooter slot, 50 a gap; 51+ require a custom count/getSol callback which Baywatch lacks. `pia2a_r` reads one country-jumper bit at `core_getDip(0)<<7`; its game-specific value meaning is not settled here.
- `s11.c` 1252-1257, DataEast/Sega 3b PWM branch: Baywatch matches a prefix check and models output 11 as `CORE_MODOUT_BULB_44_6_3V_AC_REV` and all eight muxed outputs 25-32 as `CORE_MODOUT_BULB_89_32V_DC_S11`. This is a uniform emulator brightness model. It does not resolve the production chart versus detailed schematic's mixed #89/#906 physical bulb populations.

## Runtime VPinMAME library

Exact `de2.vbs` SHA-256 `96fc634c7d6529a0566c753e296b287a1402636b38aa9bef63afebbf49f20b04`, retained under `review-artifacts/vpm-script-libs`. The exact table loads this library with `LoadVPM "01560000", "de2.VBS", 3.26`.

Constants: GameOnSolenoid=23; swBlack=-7; swGreen=-6; swTilt=1; swBallRollTilt=2; swStartButton=3; swCoin1=4; swCoin2=5; swCoin3=6; swSlamTilt=7; swLRFlip=82; swLLFlip=84; swURFlip=81; swULFlip=83. The generic BallRollTilt name at 2 is not this game's physical identity; Baywatch prints 4th Coin Slot.

`vpmKeyDown/vpmKeyUp` set the matching lower flipper-column switch on key press/release and call vpmFlips.FlipL/FlipR. Staged upper keys can write the library's 81/83 constants while their FlipperSolNumber is nonzero, but those positions do not reach Baywatch's CPU. Start writes 3; green writes -6; black writes -7. Service inputs are momentary in this library.

`core.vbs` (SHA-256 `a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`) defines the paired lower flipper callbacks sLRFlipper=46 and sLLFlipper=48. The table binds those hold-state callbacks; they assert with the associated power state.
