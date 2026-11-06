# Radical pinned controller derivation

Line numbers are retained; trailing whitespace and final blank lines are normalized.

Pinned PinMAME revision 46e1a01a0f73dc5ce163d98db1ae435883ecc450. Source repository: https://github.com/vpinball/pinmame. Attribution and license: PinMAME contributors; source code retains its upstream project license. Exact working-tree bytes were checked at the pinned clean revision. The snippets below are read-only source excerpts, not physical construction evidence. Extraction: Python 3.13.5, source lines copied with line numbering; manually reviewed by primary curator, 2026-11-06.

The per-game GEN_S11C, mux relay12, FLIP_SWNO(58,57), S11_MUXSW2, display layout and zero extra columns are distinct facts. Public switch addresses use sequential conversion. Source read path and actual runtime/script closures determine contact normal state; source macros alone do not determine physical fitment.

## src/wpc/s11games.c

SHA256 `f7c45dafbb63cee75e485cf64ea9fff8452cb3531f68df89fad9e8ff71848b5f`.

Lines 38-48:

```c
38: #define INITGAMEFULL(name, gen, disp, mux, flip, db, gs1, gs2, sc, ss17,ss18,ss19,ss20,ss21,ss22) \
39: static core_tGameData name##GameData = { \
40:   gen, disp, {flip,0,0,0,0,db,gs1,gs2}, NULL, {{0}}, {mux,{ss17,ss18,ss19,ss20,ss21,ss22}}}; \
41: static void init_##name(void) { core_gameData = &name##GameData; hc55516_set_sample_clock(0, sc); }
42:
43: S11_INPUT_PORTS_START(s11, 1) S11_INPUT_PORTS_END
44:
45: static core_tLCDLayout disp16oneline[] = { \
46:   {0,0,0,16,CORE_SEG16},{0,33,20,16,CORE_SEG16}, {0}
47: };
48:
```

Lines 1528-1554:

```c
1528: / Radical 9/90
1529: /--------------------*/
1530: INITGAME(radcl,GEN_S11C,disp16oneline,12,FLIP_SWNO(58,57),S11_LOWALPHA|S11_DISPINV,S11_MUXSW2)
1531: S11_ROMSTART48(radcl,l1,"rad_u26.l1", CRC(84b1a125) SHA1(dd01fb9189acd2620c57149921aadb051f7a2412),
1532:                         "rad_u27.l1", CRC(6f6ca382) SHA1(a61055aab97d3fe2ecd0ed4281a9681b1d910269))
1533: S11CS_SOUNDROM008(      "rad_u4.l1",  CRC(5aafc09c) SHA1(27984bbc91dc7593e6a5b42f74dd6ddf58189bec),
1534:                         "rad_u19.l1", CRC(7c005e1f) SHA1(bdeea7517f2adf72b4b642bffb25ba5b98453127),
1535:                         "rad_u20.l1", CRC(05b96292) SHA1(7da0289cf0a0c93768c0706fdedfc3a5f2101e77))
1536: S11_ROMEND
1537: #define input_ports_radcl input_ports_s11
1538: CORE_GAMEDEF(radcl, l1, "Radical! (L-1)", 1990, "Bally", s11c_one,0)
1539:
1540: S11_ROMSTART48(radcl,g1,"rad_u26.l1", CRC(84b1a125) SHA1(dd01fb9189acd2620c57149921aadb051f7a2412),
1541:                         "u27-lg1.rom",CRC(4f2eca4b) SHA1(ff44deded1686cfa0351c4499485d6eb4561cbc1))
1542: S11CS_SOUNDROM008(      "rad_u4.l1",  CRC(5aafc09c) SHA1(27984bbc91dc7593e6a5b42f74dd6ddf58189bec),
1543:                         "rad_u19.l1", CRC(7c005e1f) SHA1(bdeea7517f2adf72b4b642bffb25ba5b98453127),
1544:                         "rad_u20.l1", CRC(05b96292) SHA1(7da0289cf0a0c93768c0706fdedfc3a5f2101e77))
1545: S11_ROMEND
1546: CORE_CLONEDEF(radcl,g1,l1, "Radical! (LG-1 German)", 1990, "Bally", s11c_one,0)
1547:
1548: S11_ROMSTART48(radcl,p3,"rad_u26.p1", CRC(7d736ae9) SHA1(4ea6945fa5cfbd33fcdf780814b0bf5cb3faa388),
1549:                         "u27-p1.rom", CRC(83b1d928) SHA1(b1bd5d8a93f1ab9fb9bf5c268d8530be438448e6))
1550: S11CS_SOUNDROM008(      "rad_u4.p3",  CRC(d31b7744) SHA1(7ebcc1503fc322909d32c7c8bda8c0b6505919b3),
1551:                         "rad_u19.l1", CRC(7c005e1f) SHA1(bdeea7517f2adf72b4b642bffb25ba5b98453127),
1552:                         "rad_u20.p3", CRC(82f8369c) SHA1(0691a80672fc11d46359f710bd211de7a59de346))
1553: S11_ROMEND
1554: CORE_CLONEDEF(radcl,p3,l1, "Radical! (P-3 Prototype)", 1990, "Bally", s11c_one,0)
```

Lines 1565-1572:

```c
1565: // new one with additional fixes:
1566: S11_ROMSTART48(radcl,l1c,"Radical U26 game ROM rev LA-1 patch aa9e.rom", CRC(64833ec2) SHA1(8479bafd31940c901a819ca2347dadaf005aad17),
1567:                          "Radical U27 game ROM rev LA-1 patch aa9e.rom", CRC(09084b7d) SHA1(f930b215e34ccac119b49d9781adca113bf0a3d4))
1568: S11CS_SOUNDROM008(       "rad_u4.l1",  CRC(5aafc09c) SHA1(27984bbc91dc7593e6a5b42f74dd6ddf58189bec),
1569:                          "rad_u19.l1", CRC(7c005e1f) SHA1(bdeea7517f2adf72b4b642bffb25ba5b98453127),
1570:                          "rad_u20.l1", CRC(05b96292) SHA1(7da0289cf0a0c93768c0706fdedfc3a5f2101e77))
1571: S11_ROMEND
1572: CORE_CLONEDEF(radcl,l1c,l1, "Radical! (L-1C Competition MOD)", 2018, "Bally", s11c_one,0)
```

## src/wpc/s11.c

SHA256 `03784af9fe444b3da56f72192a5b04da1aa72938435f3d902d94ab47c0f8bd9e`.

Lines 537-587:

```c
537: static void setSSSol(int data, int solNo) {
538:                                     /*    WMS          DE */
539:   static const int ssSolNo[2][6] = {{5,4,1,2,0,3},{3,4,5,1,0,2}};
540:   int bit = CORE_SOLBIT(CORE_FIRSTSSSOL + ssSolNo[locals.deGame][solNo]);
541:   if (~data & 1)
542:     locals.switchedSol |= bit;
543:   else
544:     locals.switchedSol &= ~bit;
545:   if (locals.ssEn & (~data & 1))
546:   {
547:     coreGlobals.pulsedSolState |= bit;
548:     locals.solenoids |= bit;
549:     core_write_pwm_output(CORE_MODOUT_SOL0 + CORE_FIRSTSSSOL + ssSolNo[locals.deGame][solNo] - 1, 1, 1);
550:   }
551:   else
552:   {
553:     coreGlobals.pulsedSolState &= ~bit;
554:     core_write_pwm_output(CORE_MODOUT_SOL0 + CORE_FIRSTSSSOL + ssSolNo[locals.deGame][solNo] - 1, 1, 0);
555:   }
556: }
557:
558: static void updsol(void) {
559:   /* set new solenoids, preserve SSSol */
560:   coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0x00ff0000)
561:                              | (locals.solBits2 << 8)
562:                              | (locals.solBits1     );
563:
564:   /* if game has a MUX and it's active... */
565:   if ((core_gameData->sxx.muxSol) &&
566:       (coreGlobals.pulsedSolState & CORE_SOLBIT(core_gameData->sxx.muxSol))) {
567:     if (core_gameData->hw.gameSpecific1 & S11_RKMUX) /* special case WMS Road Kings */
568:       coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0x00ff8fef)      |
569:                                   ((coreGlobals.pulsedSolState & 0x00000010)<<20) |
570:                                   ((coreGlobals.pulsedSolState & 0x00007000)<<13);
571:     else
572:       coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0x00ffff00) |
573:                                    (coreGlobals.pulsedSolState << 24);
574:   }
575:
576:   // Simple implementation of modulated solenoids by pushing the pulsed state taking in account muxing to the physics emulation
577:   core_write_pwm_output_8b(CORE_MODOUT_SOL0     ,  coreGlobals.pulsedSolState        & 0x0FF); // Standard 'A'-side
578:   core_write_pwm_output_8b(CORE_MODOUT_SOL0 +  8, (coreGlobals.pulsedSolState >> 8)  & 0x0FF); // Standard
579:   // 17..22 are 6 special sol, processed either in fake VBlank if switch driven, or in setSSSol if PIA driven
580:   // 23 is GameOn, processed in pia0cb2_w (also filters out switched solenoids)
581:   core_write_pwm_output_8b(CORE_MODOUT_SOL0 + 24, (coreGlobals.pulsedSolState >> 24) & 0x0FF); // Standard 'C'-side (Muxed solenoids)
582:
583:   locals.solenoids |= coreGlobals.pulsedSolState;
584: }
585:
586: static WRITE_HANDLER(pia0b_w) {
587:   // DataEast Playboy35th needs the MUX delayed my one IRQ:
```

Lines 644-654:

```c
644: static READ_HANDLER(pia4a_r)
645: {
646: #if defined(LISY_SUPPORT)
647:   //get the switches from LISY_mini
648:   lisy_w_switch_handler();
649: #endif
650:   return core_getSwCol(locals.swCol);
651: }
652:
653: /*-------
654: /  Sound
```

Lines 780-803:

```c
780: 	// Go read the switches from the P-ROC
781: 	if (coreGlobals.p_rocEn)
782: 		procGetSwitchEvents();
783: #endif
784:
785: #ifndef LISY_SUPPORT
786: //if we have LISY, all switches come from LISY (Matrix[0] has e.g. ADVANCE Button!
787:   if (inports) {
788:     coreGlobals.swMatrix[0] = (inports[S11_COMINPORT] & 0x7f00)>>8;
789:     // All the matrix switches come from the P-ROC, so we only want to read
790:     // the first column from the keyboard if we are not using the P-ROC
791: #ifndef PROC_SUPPORT
792:     coreGlobals.swMatrix[1] = inports[S11_COMINPORT];
793: #endif
794:   }
795: #endif
796:
797:   /*-- Generate interupts for diganostic keys --*/
798:   cpu_set_nmi_line(0, core_getSw(S11_SWCPUDIAG) ? ASSERT_LINE : CLEAR_LINE);
799:   sndbrd_0_diag(core_getSw(S11_SWSOUNDDIAG));
800:   if ((core_gameData->hw.gameSpecific1 & S11_MUXSW2) && core_gameData->sxx.muxSol)
801:     core_setSw(2, core_getSol(core_gameData->sxx.muxSol));
802:   if (locals.deGame) {
803:     /* Show Status of Black Advance Switch */
```

Lines 1064-1079:

```c
1064:   }
1065:   else if (strncasecmp(gn, "radcl_", 6) == 0) { // Radical!
1066:      core_set_pwm_output_type(CORE_MODOUT_SOL0 +  9 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
1067:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 10 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // Playfield GI output
1068:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 11 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // Backbox GI output
1069:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 16 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
1070:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 25 - 1, 8, CORE_MODOUT_BULB_89_25V_DC_S11); // 8 muxed flasher outputs (Mux relay is solenoid #12)
1071:   }
1072:   else if (strncasecmp(gn, "rollr_", 6) == 0) { // Rollergames
1073:      core_set_pwm_output_type(CORE_MODOUT_SOL0 +  9 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
1074:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 10 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // Playfield GI output
1075:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 11 - 1, 1, CORE_MODOUT_BULB_44_6_3V_AC_REV); // Backbox GI output
1076:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 11 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
1077:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 16 - 1, 1, CORE_MODOUT_BULB_89_25V_DC_S11);
1078:      core_set_pwm_output_type(CORE_MODOUT_SOL0 + 25 - 1, 8, CORE_MODOUT_BULB_89_25V_DC_S11); // 8 muxed flasher outputs (Mux relay is solenoid #12)
1079:   }
```

## src/wpc/core.c

SHA256 `38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00`.

Lines 1793-1847:

```c
1793: void core_updateSw(int flipEn) {
1794:   /*-- handle flippers--*/
1795:   const int flip = core_gameData->hw.flippers;
1796:   const int flipSwCol = (core_gameData->gen & (GEN_GTS3 | GEN_SPA | GEN_ALVG | GEN_ALVG_DMD2 | GEN_WICO)) ? 15 : CORE_FLIPPERSWCOL;
1797:   int inports[CORE_MAXPORTS];
1798:   UINT8 swFlip;
1799:   int ii;
1800:
1801:   if (g_fHandleKeyboard) {
1802:     const int n = CORE_COREINPORT+(coreData->coreDips+31)/16;
1803:     for (ii = 0; ii < n; ii++)
1804:       inports[ii] = readinputport(ii);
1805:
1806:     /*-- buttons --*/
1807:     swFlip = 0;
1808:     if (inports[CORE_FLIPINPORT] & CORE_LLFLIPKEY) swFlip |= CORE_SWLLFLIPBUTBIT;
1809:     if (inports[CORE_FLIPINPORT] & CORE_LRFLIPKEY) swFlip |= CORE_SWLRFLIPBUTBIT;
1810:     if (locals.flipMask & CORE_SWULFLIPBUTBIT) {    /* have UL switch */
1811:       if (flip & FLIP_BUT(FLIP_UL))
1812:         { if (inports[CORE_FLIPINPORT] & CORE_ULFLIPKEY) swFlip |= CORE_SWULFLIPBUTBIT; }
1813:       else
1814:         { if (inports[CORE_FLIPINPORT] & CORE_LLFLIPKEY) swFlip |= CORE_SWULFLIPBUTBIT; }
1815:     }
1816:     if (locals.flipMask & CORE_SWURFLIPBUTBIT) {    /* have UR switch */
1817:       if (flip & FLIP_BUT(FLIP_UR))
1818:         { if (inports[CORE_FLIPINPORT] & CORE_URFLIPKEY) swFlip |= CORE_SWURFLIPBUTBIT; }
1819:       else
1820:         { if (inports[CORE_FLIPINPORT] & CORE_LRFLIPKEY) swFlip |= CORE_SWURFLIPBUTBIT; }
1821:     }
1822:   }
1823:   else
1824:     swFlip = (coreGlobals.swMatrix[flipSwCol] ^ coreGlobals.invSw[flipSwCol]) & (CORE_SWULFLIPBUTBIT|CORE_SWURFLIPBUTBIT|CORE_SWLLFLIPBUTBIT|CORE_SWLRFLIPBUTBIT);
1825:
1826: #ifdef PROC_SUPPORT
1827:   /*-- Only handle flipper switches if we're not in a real game, otherwise they --*/
1828:   /*-- will get physically activated anyway */
1829:   if (!coreGlobals.p_rocEn) {
1830: #endif
1831:
1832:     /*-- set switches in matrix for non-fliptronic games --*/
1833:     if (FLIP_SWL(flip)) core_setSw(FLIP_SWL(flip), swFlip & CORE_SWLLFLIPBUTBIT);
1834:     if (FLIP_SWR(flip)) core_setSw(FLIP_SWR(flip), swFlip & CORE_SWLRFLIPBUTBIT);
1835: #ifdef PROC_SUPPORT
1836:   }
1837: #endif
1838:
1839:   /*-- fake solenoids if not CPU controlled --*/
1840:   if ((flip & FLIP_SOL(FLIP_L)) == 0) {
1841:     coreGlobals.solenoids2 &= 0xffffff00;
1842:     if (flipEn) {
1843:       if (swFlip & CORE_SWLLFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LLFLIPSOLBITS;
1844:       if (swFlip & CORE_SWLRFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LRFLIPSOLBITS;
1845:     }
1846:   }
1847:
```

Lines 1875-1898:

```c
1875:   /*-- update game dependent switches --*/
1876:   if (g_fHandleMechanics) {
1877:     if (core_gameData->hw.handleMech) core_gameData->hw.handleMech(g_fHandleMechanics);
1878:   }
1879:
1880:   /*-- run simulator --*/
1881:   if (coreGlobals.simAvail)
1882:     sim_run(inports, CORE_COREINPORT+(coreData->coreDips+31)/16,
1883:             (inports[CORE_SIMINPORT] & SIM_SWITCHKEY) == 0,
1884:             (SIM_BALLS(inports[CORE_SIMINPORT])));
1885:
1886:   /*-- Report changed solenoids --*/
1887:   if (coreGlobals.nSolenoids &&
1888:      ((options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_FORCE_ON)) || ((core_gameData->gen & (GEN_ALLWPC | GEN_SAM)) && (options.usemodsol & CORE_MODOUT_ENABLE_MODSOL)) ))
1889:   {
1890:     float state[CORE_MODOUT_SOL_MAX];
1891:     #if defined(VPINMAME) || defined(LIBPINMAME)
1892:     // These builds only integrate on client request (see VIDEO_UPDATE): integrate here, or a client only listening to OnSolenoid would see no change
1893:     // (serialized with the client's integrations by the lock in core_update_pwm_outputs)
1894:     core_update_pwm_solenoids();
1895:     #endif
1896:     core_getAllPhysicSols(state);
1897:     for (ii = 1; ii <= coreGlobals.nSolenoids; ii++) {
1898:       UINT8 v = saturatedByte(state[ii - 1]);
```

Lines 2208-2210:

```c
2208: int core_swSeq2m(int no) { return no+7; }
2209: int core_m2swSeq(int col, int row) { return col*8+row-7; }
2210:
```

Lines 2456-2512:

```c
2456: int core_getSol(int solNo) {
2457:   // No solenoid 0, but VPM's Solenoids/SolenoidsState arrays start at index 0
2458:   if (solNo < 1)
2459:     return 0;
2460:   // Binary states are returned as 0/1, like the changed solenoid list. The integrated value is only returned with physical solenoid outputs
2461:   // or modulated solenoids: with CORE_MODOUT_FORCE_ON alone (SAM, Capcom, pinHeck), a blinking flasher would read on for the whole sequence
2462:   // 1-32: driver board outputs, like core_getAllSol / core_getAllPhysicSols
2463:   if (solNo <= 28 || (solNo <= 32 && !(core_gameData->gen & GEN_ALLWPC)))
2464:     return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value) : ((coreGlobals.solenoids & CORE_SOLBIT(solNo)) != 0);
2465:   else if (solNo <= 32) // 29-32 WPC: remap GameOn/J111 GPIO (hacky)
2466:     // Binary state even with physical outputs, while core_getAllPhysicSols reports slots 28-30 (CORE_MODOUT_PULSE, same states) as 0/255
2467:     return (coreGlobals.solenoids2 & (1<<(solNo-29+8))) != 0;
2468:   else if (solNo <= 36) { // 33-36 driver specific sols
2469:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)))
2470:       return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value); // Fliptronics are implemented through PWM (needed as these are used to drive flashers on some games)
2471:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & CORE_MODOUT_FORCE_ON)) // Binary state of the flipper outputs, like core_getFlipSolBits
2472:       return coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value > 0.f;
2473:     if (core_gameData->gen & GEN_ALLWPC) { // WPC only: Upper flipper (note that other systems also have upper flippers, they just don't implement the legacy PinMAME flipper output mapping)
2474:       int mask;
2475:       /*-- flipper coils --*/
2476:       if      ((solNo == sURFlip) && (core_gameData->hw.flippers & FLIP_SOL(FLIP_UR)))
2477:         mask = CORE_URFLIPSOLBITS;
2478:       else if ((solNo == sULFlip) && (core_gameData->hw.flippers & FLIP_SOL(FLIP_UL)))
2479:         mask = CORE_ULFLIPSOLBITS;
2480:       else
2481:         mask = 1<<(solNo - 33 + 4);
2482:       return (coreGlobals.solenoids2 & mask) != 0;
2483:     }
2484:     else if (core_gameData->gen & (GEN_SAM | GEN_SPIKE1)) // SAM, SPIKE 1: fake GameOn solenoid for fast flips
2485:        return (coreGlobals.solenoids2 & 0x10) != 0;
2486:     else if (core_gameData->gen & GEN_ALLWS) // Whitestar: aux board outputs (magnets, ...), like core_getAllSol
2487:        return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value) : ((coreGlobals.solenoids2 & (1<<(solNo - 33 + 4))) != 0);
2488:   }
2489:   else if (solNo <= 44) { // 37-44 WPC95 & S11 extra
2490:     if (core_gameData->gen & (GEN_WPC95|GEN_WPC95DCS)) { // Duplicated in 37..40 / 41..44, so always read from 41..44 (hence the |4 in the index/mask) for solenoids, and 37..40 for PWM outputs
2491:       if (coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)))
2492:         return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + (solNo <= 40 ? solNo : (solNo - 4))-1].value);
2493:       else
2494:         return (coreGlobals.solenoids & (1<<((solNo - 13)|4))) != 0;
2495:     }
2496:     if (core_gameData->gen & (GEN_ALLS11 | GEN_PINHECK)) // S11 outputs in slots 40-47; pinHeck's GI 8-15 in 36-43, its lower flippers using 44-47
2497:       return coreGlobals.nSolenoids && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)) ? saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + ((core_gameData->gen & GEN_PINHECK) ? solNo - 1 : 32 + solNo - 37 + 8)].value) : ((coreGlobals.solenoids2 & (1<<(solNo - 37 + 8))) != 0);
2498:   }
2499:   else if (solNo <= 48) { // 45-48 Lower flippers
2500:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & (CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS | CORE_MODOUT_ENABLE_MODSOL)))
2501:       return saturatedByte(coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value); // Fliptronics are implemented through PWM
2502:     if (coreGlobals.hasModulatedFlippers && (options.usemodsol & CORE_MODOUT_FORCE_ON)) // Binary state of the flipper outputs, like core_getFlipSolBits
2503:       return coreGlobals.physicOutputState[CORE_MODOUT_SOL0 + solNo - 1].value > 0.f;
2504:     int mask = 1<<(solNo - 45);
2505:     /*-- Game must have lower flippers but for symmetry we check anyway --*/
2506:     if      /*(*/(solNo == sLRFlip) //&& (core_gameData->hw.flippers & FLIP_SOL(FLIP_LR)))
2507:       mask = CORE_LRFLIPSOLBITS;
2508:     else if /*(*/(solNo == sLLFlip) //&& (core_gameData->hw.flippers & FLIP_SOL(FLIP_LL)))
2509:       mask = CORE_LLFLIPSOLBITS;
2510:     return (coreGlobals.solenoids2 & mask) != 0;
2511:   }
2512:   else if (solNo <= 50) // 49-50 simulated
```

## src/wpc/core.h

SHA256 `b6c03b20a09fbadff1ce16f9f1cfc9e5bace08857cb998b92d8f304695ec97c0`.

Lines 150-164:

```c
150: #define FLIP_LL        (0x2)
151: #define FLIP_UR        (0x4)
152: #define FLIP_UL        (0x8)
153: #define FLIP_L         (FLIP_LL | FLIP_LR)
154: #define FLIP_U         (FLIP_UL | FLIP_UR)
155:
156: /*-- definition macros --*/
157: #define FLIP_BUT(x)    ((x)<<16)
158: #define FLIP_SW(x)     ((x)<<20)
159: #define FLIP_SWNO(l,r) (((l)<<8)|(r)|FLIP_SW(FLIP_L))
160: #define FLIP_EOS(x)    ((x)<<28)
161: #define FLIP_SOL(x)    (((x)<<24)|FLIP_EOS(x))
162:
163: #define FLIP_SWL(x)    (((x)>>8)&0xff)
164: #define FLIP_SWR(x)    ((x)&0xff)
```

## src/wpc/gen.h

SHA256 `77deabc0f1ff902381e31d6d60d23b6585a27631848a1d13e64111b7205d7562`.

Lines 1-65:

```c
1: #pragma once
2:
3: #if defined(__GNUC__)
4: #define U64(x) __extension__ x##LL
5: #elif defined(_MSC_VER)
6: #define U64(x) x##ui64
7: #endif
8:
9: /*-- All Hardware Generations --*/
10: #define GEN_WPCALPHA_1  U64(0x0000000000001) /* Alpha-numeric display S11 sound, Dr Dude 10/90 */
11: #define GEN_WPCALPHA_2  U64(0x0000000000002) /* Alpha-numeric display,  - The Machine BOP 4/91*/
12: #define GEN_WPCDMD      U64(0x0000000000004) /* Dot Matrix Display, Terminator 2 7/91 - Party Zone 10/91 */
13: #define GEN_WPCFLIPTRON U64(0x0000000000008) /* Fliptronic flippers, Addams Family 2/92 - Twilight Zone 5/93 */
14: #define GEN_WPCDCS      U64(0x0000000000010) /* DCS Sound system, Indiana Jones 10/93 - Popeye 3/94 */
15: #define GEN_WPCSECURITY U64(0x0000000000020) /* Security chip, World Cup Soccer 3/94 - Jackbot 10/95 */
16: #define GEN_WPC95DCS    U64(0x0000000000040) /* Hybrid WPC95 driver + DCS sound, Who Dunnit */
17: #define GEN_WPC95       U64(0x0000000000080) /* Integrated boards, Congo 3/96 - Cactus Canyon 2/99 */
18: #define GEN_S11         U64(0x0000080000000) /* No external sound board */
19: #define GEN_S11X        U64(0x0000000000100) /* S11C sound board */
20: #define GEN_S11A        GEN_S11X
21: #define GEN_S11B        GEN_S11X
22: #define GEN_S11B2       U64(0x0000000000200) /* Jokerz! sound board */
23: #define GEN_S11C        U64(0x0000000000400) /* No CPU board sound */
24: #define GEN_S9          U64(0x0000000000800) /* S9 CPU, 4x7+1x4 */
25: #define GEN_DE          U64(0x0000000001000) /* DE AlphaSeg */
26: #define GEN_DEDMD16     U64(0x0000000002000) /* DE 128x16 */
27: #define GEN_DEDMD32     U64(0x0000000004000) /* DE 128x32 */
28: #define GEN_DEDMD64     U64(0x0000000008000) /* DE 192x64 */
29: #define GEN_S7          U64(0x0000000010000) /* S7 CPU */
30: #define GEN_S6          U64(0x0000000020000) /* S6 CPU */
31: #define GEN_S4          U64(0x0000000040000) /* S4 CPU */
32: #define GEN_S3C         U64(0x0000000080000) /* S3 CPU No Chimes */
33: #define GEN_S3          U64(0x0000000100000)
34: #define GEN_BY17        U64(0x0000000200000)
35: #define GEN_BY35        U64(0x0000000400000)
36: #define GEN_STMPU100    U64(0x0000000800000) /* Stern MPU - 100*/
37: #define GEN_STMPU200    U64(0x0000001000000) /* Stern MPU - 200*/
38: #define GEN_ASTRO       U64(0x0000002000000) /* Unknown Astro game, Stern hardware */
39: #define GEN_HNK	        U64(0x0000004000000) /* Hankin */
40: #define GEN_BYPROTO     U64(0x0000008000000) /* Bally Bow & Arrow prototype */
41: #define GEN_BY6803      U64(0x0000010000000)
42: #define GEN_BY6803A     U64(0x0000020000000)
43: #define GEN_BOWLING     U64(0x0000040000000) /* Big Ball Bowling, Stern hardware */
44:
45: #define GEN_GTS1        U64(0x0000100000000) /* GTS1 */
46: #define GEN_GTS80       U64(0x0000200000000) /* GTS80 */
47: #define GEN_GTS80A      GEN_GTS80
48: #define GEN_GTS80B      U64(0x0000400000000) /* GTS80B */
49: #define GEN_RECEL       U64(0x0000800000000) /* Recel System III */
50: #define GEN_WS          U64(0x0004000000000) /* Whitestar */
51: #define GEN_WS_1        U64(0x0008000000000) /* Whitestar with extra RAM */
52: #define GEN_WS_2        U64(0x0010000000000) /* Whitestar with extra DMD */
53: #define GEN_GTS3        U64(0x0020000000000) /* GTS3 */
54:
55: #define GEN_ZAC1        U64(0x0040000000000)
56: #define GEN_ZAC2        U64(0x0080000000000)
57:
58: #define GEN_SAM         U64(0x0100000000000) /* Stern SAM */
59:
60: #define GEN_ALVG        U64(0x0200000000000) /* Alvin G Hardware */
61: #define GEN_ALVG_DMD2   U64(0x0400000000000) /* Alvin G Hardware, with more shades */
62: #define GEN_MRGAME      U64(0x0800000000000) /* Mr.Game Hardware */
63: #define GEN_SLEIC       U64(0x1000000000000) /* Sleic Hardware */
64: #define GEN_WICO        U64(0x2000000000000) /* Wico Hardware */
65:
```
