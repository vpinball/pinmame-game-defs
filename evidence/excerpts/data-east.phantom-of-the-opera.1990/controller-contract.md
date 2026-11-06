# Phantom of the Opera controller construction

Sources: manual PDF 2 / red insert printed i, CPU Jumper Table; PDF 42 / printed 38 cabinet drawing; PDF 51 / printed 46 CPU Board Assembly Drawing; PDF 53 / printed 48 CPU logic sheet 2; pinned s11.h, s11.c and degames.c. Direct visual/code read by project curator; reviewed. The accompanying tight crop shows the entire relevant PIA11B PA7 net, including the jumper path previously omitted from the transcription.

CPU PIA11B PA7 pin 9 connects both to a +5V pull-up through RA4, 4.7K, and to two circle terminals with a dashed jumper link to ground, labelled J8. The rotated designator reads J8; the CPU Board Assembly Drawing independently labels that jumper position J8. RA3, 4.7K x8, is the neighboring port-B pull-up array, not the PA7 resistor. With J8 installed the net is grounded; with it removed RA4 pulls it high. The complete CPU Jumper Table below explicitly lists J8 installed for Phantom of the Opera, CPU Ver 2, ROMs 5B,5C. This is documented factory configuration, not a survey of every surviving board.

The inherited s11 machine driver declares one DIP-style bit, and pia2a_r returns core_getDip(0)<<7. Thus public bit 0 at value 0 supplies low PA7, corresponding to the documented grounded J8 configuration; value 1 supplies high PA7, corresponding electrically to removing J8. S11_COMPORTS declares a Country input; DE_COMPORTS used by poto does not. Neither this transport nor the jumper drawing establishes Phantom's firmware purpose. Do not rename J8 as Williams W7 or assert a Country function without game-specific evidence. The definition retains an input_semantics blocker for the unresolved firmware interpretation.

The cabinet drawing depicts open STEP and Forward/Reverse contacts into CN14 (STEP pin 4, BLU; Forward/Reverse pin 3, GRN; common ground pin 2, WHT). The CPU logic sheet 1 inverts both through LS02 gates before the PIA control inputs. The emulator presents public Advance inverted to PIA2 CA1 and Up/Down directly to CB1; consume its public states as delivered. Physical normally-open construction is separate from the maintained/toggled service convention.

## Complete CPU Jumper Table

| Game | CPU* Version | ROM Location | Jumpers Installed | Jumpers Removed |
| --- | --- | --- | --- | --- |
| Laser Wars | Ver 1 | 5C | J1b,J3,J4,J6a,J7a,&J8 | J1a,J2,J5,J6,&J7b |
|  | Ver 2 | 5C | J1b,J3,J4,J5a,J6a,J7b,&J8 | J1a,J2,J5,J5b,J6b,&J7a |
| Secret Service | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Torpedo Alley | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Time Machine | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Playboy | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| ABC M.N. Football | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Robocop | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |
| Phantom of the Opera | Ver 2 | 5B,5C | J1b,J3,J4,J5b,J6b,J7b,&J8 | J1a,J2,J5,J5a,J6a,&J7a |

The blank second Game cell belongs to the merged Laser Wars entry. Printed comma separators, ampersands, case and the unlettered J5/J6 entries are retained; surrounding table spacing is normalized.

*Version 1 has a 2K RAM which is a 24-pin IC at location 5D.

*Version 2 has an 8K RAM which is a 28-pin IC at location 5D.
