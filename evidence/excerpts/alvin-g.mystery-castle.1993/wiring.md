# Load-bearing wiring and physical topology

Retained MAN-019 scan, PDF 63 (DOC-000 System Wiring), 64 (DOC-003 Switch Wiring), 65 (DOC-002 Solenoid Wiring), 67 (the title block reads DOC-004 Lamp Wiring), and 44 (printed 5-5, flipper assembly). Read visually from native-resolution renders. Drawing-symbol quantities below are counted, not inferred from table code. Source wire spelling is retained; normalized public addresses are supplied by the separately pinned driver.

## DOC-002 GI and flashers (PDF 65)

| Coil/control | Diagram label | Bulbs/branches | Wiring/notes |
| --- | --- | --- | --- |
| 16 | PLAYFIELD GI RELAY #1 (SEE COIL #16) | TOP PLAYFIELD GI'S: 13 BULBS; TOP PLAYFIELD GI'S (RED): 13 BULBS | TO PWR SUPPLY CONN. PP1-10, WHT/VIO, F20 4A Slo-Blo; two drawn relay contact paths: WHT/VIO to the first branch and WHT/RED to the red branch; both return on VIO/VIO to PP1-13; controlled coil BRN/GRY A1HP6-10 |
| 26 | PLAYFIELD GI RELAY #2 (SEE COIL #26) | BOTTOM PLAYFIELD GI'S: 12 BULBS; shared fused supply also feeds COIN DOOR GI'S: 2-4 BULBS before the relay contact | TO PWR SUPPLY CONN. PP1-09, WHT/BLU, F21 4A Slo-Blo; contact output WHT/BLU feeds the bottom-playfield branch; coin-door feed taps the F21 output before that contact, with no separate printed wire color; both return on VIO/VIO to PP1-12; controlled coil BLU/BLK A1HP7-16 |
| 31 | BACKBOX GI RELAY #2 (SEE COIL #31) | INSERT GI'S (SPECIAL): dashed group labelled [4/6] BULBS (count digit uncertain), plus a separate parallel branch drawn with two unlabelled bulb symbols | TO PWR SUPPLY CONN. PP1-15, WHT/BRN; F23 4A Slo-Blo, WHT/BRN; BLU/BLU returns: dashed group to PP1-11, separate two-symbol branch to PP2-10; controlled coil BLU/ORG A1HP7-10 |
| 29 | BACKBOX GI RELAY #1 (SEE COIL #29) | INSERT GI'S: 12 BULBS; INSERT GI'S: 12 BULBS | TO PWR SUPPLY CONN. PP1-16, WHT/GRY; separate F24/F25, both 4A Slo-Blo and WHT/GRY; BLU/BLU returns: upper 12-bulb group to PP1-11, lower 12-bulb group to PP2-10; controlled coil BLU/BRN A1HP7-12 |
| 15 | FLASHER RELAY (PART OF PCA-007) | common power for all flasher branches 17-24 | RED/VIO coil feed, BRN/VIO A1HP6-11; PCA-007 relay supply/sense circuitry precedes VIO/WHT common flasher feed |
| 17 | FLASHER DUNGEON | 2 drawn bulb symbols | VIO/WHT; BLK/BRN A1HP7-08 |
| 18 | FLASHER BRIDGE | 2 drawn bulb symbols | VIO/WHT; BLK/RED A1HP7-07 |
| 19 | FLASHER TOWER | 2 drawn bulb symbols | VIO/WHT; BLK/ORG A1HP7-06 |
| 20 | FLASHER BALLROOM | 1 drawn bulb symbol | VIO/WHT; BLK/YEL A1HP7-05 |
| 21 | FLASHER SECRET DOOR | 1 drawn bulb symbol | VIO/WHT; BLK/GRN A1HP7-04 |
| 22 | FLASHER CATWALK | 2 drawn bulb symbols | VIO/WHT; BLK/BLU A1HP7-03 |
| 23 | FLASHER LOCK | 1 drawn bulb symbol | VIO/WHT; BLK/VIO A1HP7-02 |
| 24 | FLASHER BACKBOX | 4 drawn bulb symbols | VIO/WHT; BLK/GRY A1HP7-01 |

Diagram note: ALL INSERT GI LAMPS #555 BULB; ALL INSERT FLASH LAMPS #906 BULB; ALL PLAYFIELD GI LAMPS #44 BULB; ALL PLAYFIELD FLASH LAMPS #47 BULB; ALL DIODES 1N4004.

The complete GI return footer reads, in printed order:

| Printed endpoint | Wire | Printed voltage label | Branch traced to this return |
| --- | --- | --- | --- |
| TO POWER SUPPLY CONN. PP2-10 | BLU/BLU | +[5 or 6]VAC RETURN (digit uncertain) | Lower 12-bulb normal-insert group at relay 29 and the separate two-symbol special-insert branch at relay 31 |
| TO POWER SUPPLY CONN. PP1-11 | BLU/BLU | +[5 or 6]VAC RETURN (digit uncertain) | Upper 12-bulb normal-insert group at relay 29 and the dashed special-insert group at relay 31 |
| TO POWER SUPPLY CONN. PP1-12 | VIO/VIO | +[5 or 6]VAC RETURN (digit uncertain) | Bottom-playfield branch shown at relay 26 and its shared, unswitched coin-door supply branch |
| TO POWER SUPPLY CONN. PP1-13 | VIO/VIO | +[5 or 6]VAC RETURN (digit uncertain) | Both top-playfield branches shown at relay 16 |

The fourth footer line lies beyond the old compact crop; the additional gi-footer.webp crop retains all four endpoints and voltage labels from the full native 300-dpi page-65 render. Each footer label is +?VAC RETURN, but the voltage digit remains uncertain between 5 and 6 in this degraded scan. Comparisons with other printed digits do not establish a reliable reading, and no typed voltage is promoted. The coin-door first digit is 2: its descending diagonal and flat lower bar match the 2 in the adjacent 12 BULBS, unlike the rounded lower lobe of the 3 in 13 BULBS. Thus the literal variable count is 2-4 BULBS. These are unswitched cabinet lamps on the F21 supply before the relay-26 contact; they are supply context, not an additional controlled output. The drawing shows the two relay-16 contact paths together but prints no separate NO/NC contact-state labels, so this transcription makes no separate contact-state assertion. The backbox returns cross without a junction at the separate special pair's horizontal run; the two shown junction dots connect each normal-insert group to a different shared return as listed above.

For relay 31, the dashed group's count digit is uncertain between 4 and 6, followed by BULBS; the lower parallel branch contains two unlabelled bulb symbols. The annotation also does not explicitly say whether its scope includes that separate pair. This excerpt preserves the uncertain glyph, both branches and the connected returns; the definition omits a total rather than inventing a precise count. A clearer factory source or physical socket survey is needed to settle it.

The coil table says FIELD RELAY BOT at 16 and FIELD RELAY TOP at 26. DOC-002's branch labels above contradict that assignment. The ROM service labels and retained table's LowerGILights/UpperGILights bindings agree with the coil table; they do not observe physical socket wiring. Neither reading establishes the actual playfield region controlled by 16/26, so the physical assignment and per-address quantities remain conflicted. The variable 2-4 coin-door quantity is not completed by assumption or assigned to either relay's controlled load.

## Flipper circuit and parts (PDF 65 and 44)

DOC-002 draws FLIPPER RIGHT, FLIPPER LEFT and UPPER LEFT FLIPPER on separate VIO/ORG supply branches, each with a normally-closed local EOS contact and its own two winding sections. Right returns through RIGHT FLIPPER SWITCH; lower-left returns through LEFT FLIPPER SWITCH; the upper-left return reaches the same left switch through a mechanically linked normally-open contact on the lower-left flipper assembly. RF3/CF3 shunt that normally-open contact. The coils are not in series. FLIPPER RELAY (COIL #27), BLU/VIO A1HP7-15, gates the common return.

The complete flipper-assembly parts-list region in PDF 44 / 5-5 reads:

| Item | Description | Qty | Part no. |
| --- | --- | --- | --- |
| 1 | Plunger stop bracket | 1 | BSL-027 |
| 2 | Bumper gromet | 1 | RBR-001 |
| 3 | Bushing | 1 | BRG-001 |
| 4 | E-Ring 5144-18 | 2 | HRG-001 |
| 5 | Link & plunger assembly | 1 | LAP-001 |
| 6 | Spring | 1 | SRG-001 |
| 7 | Coil mounting bracket assembly | 1 | CBA-001 |
| 8 | #8-32 X 3/8 HWH (type AB) | 6 | HTT-005 |
| 9 | Coil (Used only on lower left and right flipper assemblies.) | 1 | CLL-015 |
| dagger 9 | Coil (Used only on upper left flipper assembly.) | 1 | CLL-003 |
| 10 | Sleeve | 1 | SLC-001 |
| 11 | Stop stud assembly | 1 | ASS-002 |
| 12 | #10 SLW | 3 | HLW-010 |
| 13 | 10-32 X 3/8 BSC | 3 | HMS-026 |
| 14 | Actuator bearing | 1 | SLV-001 |
| 15-L | Pivot yoke left (Used only on left flipper assemblies.) | 1 | PYA-L01 |
| 15-R | Pivot yoke right (Used only on right flipper assemblies.) | 1 | PYA-R01 |
| 16-L | Flipper base assembly left (Used only on left flipper assemblies.) | 1 | FBA-L01 |
| 16-R | Flipper base assembly right (Used only on right flipper assemblies.) | 1 | FBA-R01 |
| 17 | Flipper shaft bushing | 1 | FSB-001 |
| 18 | #6-32 X 3/8 HWH (type F) | 3 | HTT-004 |
| 19 | Flipper bat assembly | 1 | AFT-004 |
| 20 | Capacitor T12.2K 250VDC | 1 | CAP-001 |
| 21 | Mounting bracket | 1 | BSL-032 |
| double dagger 22 | Switch normally open (Upper Flipper Activator) | 1 | FLS-002 |
| 23 | Insulator | 1 | FPN-004 |
| 24 | Switch normally closed (End Of Stroke) | 1 | FLS-002 |
| 25 | 0.1µF, 500V, Capacitor | 1 | CAP-021 |
| 26 | 100Ω, 1/2W, Resistor | 1 | RST-031 |
| 27 | #5-40 X 5/8 PPH MS | 1 | HMS-006 |
| 28 | Clamp plate | 1 | SWP-001 |

Footnote marks dagger/double dagger and the micro/ohm glyphs are normalized explicitly above. Source heading: AFF-L03, AFF-L05, AFF-R02 FLIPPER ASSEMBLY. The public controller has one left assembly callback; it does not publish the activator or either EOS contact.

## Switch/lamp construction and connector corrections

DOC-003 draws all fitted matrix contacts 1-55 normally open and labels the unpopulated cells N.U.; all cells 56-96 are N.U. It identifies the twelve strobe rows as HP4-1 through HP4-12, with 11/12 ORG/YEL and ORG/GRN, correcting HP4-13/-14 printed on the matrix page. Return 5 is HP5-4 GRN/BLK, agreeing with DOC-000 and correcting the matrix's duplicated GRN/YEL. The matrix excerpt preserves every original heading and blank.

DOC-004 Lamp Wiring (PDF 67) draws one bulb at every named circuit 1-61; 62-96 are N.U. Alternate labels include SHOOT AGAIN (1), GRID SCEPTOR (2), LOCK ARROW (20), MYSTERY ARROW (21), CATAPULT LOADED (22), TUNNEL LOCK (37), TUNNEL MYSTERY (38), BUMPER TOP/BOTTOM (39/40), CASTLE SPECIAL (46), XBAll (54), and BILLBOARD BRIDGE/DUNGEON/TOWER/BALLROOM/CATWALK (57-61). These are names for the same devices, not incompatible physical claims. Return 7 is HP2-8 on the matrix and detailed CPU board schematic, while this load drawing prints HP2-7; the return wire YEL/VIO and circuit are unchanged.

DOC-000 labels HP4 SWITCH STROBES and HP5 SWITCH RETURNS. Its dedicated-switch header HP5A labels FLASHER SENSE SW1, MENU EXIT SW2, MENU ENTER SW3, NC, EXTRA SW4; only the menu pair is fitted as a human coin-door control. The active PinMAME read block and retained service trace establish the public -7/-6 ordering; its emulator symbols do not reproduce the literal header order.
