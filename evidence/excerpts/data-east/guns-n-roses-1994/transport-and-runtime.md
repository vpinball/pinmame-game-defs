# Exact runtime and transport contract

Pinned PinMAME8371478a7640f1896dcdf565aed340dc5df989ba:
degames.c1269-1320 declares three GnR3.00 drivers, shared gnrGameData,
GEN_DEDMD32,de_128x32DMD,FLIP6364,three custom solenoids,
zero extra switch/lamp columns,zero inverse array,S11_PRINTERLINE,mux10.
core.h300-330:ext37,custom51; gnr_getSol51/52/53 returns37/38/39.
s11.c392-410 printer byte is noninverted;205-220 publishes it.
s11.c558-584 mux10 routes1-8 to25-32.
s11.c618-625 Data East special order:
pia1ca2->20,pia1cb2->21,pia3ca2->22,pia3cb2->18,pia4ca2->17,pia4cb2->19.
s11.c628-650 eight-bit switch strobe,uncomplemented core_getSwCol.
s11.c1188-1196:11 reversed #44 6.3VAC;25-32 #89 32VDC.
core.c1700-1753:82->64,84->63;game-on23 gates synthetic45-48.
core.c2182-2224:33-36 dead for Data East,37-44 raw extension,49 simulator,
50 gap,51-53custom;greater custom returns0. No upper ROM coil36.

Exact retained Team PP embedded script sha256
d42debb0e6c30e4498e6ed77ac475a04141a799448c7fcbfff26f3a247b376a9:
script.vbs95 cGameName=gnr_300;170-250 trough/scoop/eject/VUK/magnets;
269 vpmMapLights AllLamps;436-438 and585-587 drop switches;
770-845 slings28right29left30top;914-1020 matrix Hit/UnHit;
1044-1093 kickers;1264-1334 solenoid callbacks/trap;
1346-1499 glow/flasher routines;1505-1545 reversed GI.
Not exact-match to any pinned corpus script. Three Flipper objects exist;
LeftFlipper1 is the upper-left pivot and the old script moves it with the lower-left.

Pinned VPW1.2.1 sha256
a0b37bbd036726345d89483c76e2afebec994abcc395d646b85ac79770eefe1e:
vpxtable_scripts revision0c036bb61b4b4e8c778c37559f6795df8cd1521e;
script39-40 ROM;514-586 initialization with six trough balls, captive seventh,
magnet51left52center53right;663-715callbacks;722-767trough;
1263-1407kickers/trap; staged cabinet flipper callbacks.
de.vbs and core.vbs cvpmFlips2.Init2094-2150 capture callbacks;
Flip/FlipUL call upper code directly while TiltSol/game-on23 enables it.
de.vbs sha2568858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04;
core.vbs sha256a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69.

The committed scenario and bounded DMD-header adapter use named service
keys and exact retained top-ten-row templates. After the transient test
header, wait_until_output23 proves readiness before switch stimulus.
Fresh run magnet-laser-v2-state:US3.00,boot8seconds,empty CMOS.
Expected causal results:holding Start cycles37=51,38=52,39=53;
54 pulse->14,37->4,39->5,38->6. Hostleft/right buttons produce47/48 and45/46.
Complete raw run, snapshots, ROM archive hashes, DLL identity and manifest
remain external. Compact checked observations are in runtime-summary.md.
Host switch readback alone is not evidence of ROM behavior.

Exact pinned transport files (full-file SHA256):

- src/wpc/core.h: `9d2fa69f7fa6963adc793b272bb5cbfbf94e929c0d7f6b928b1b02a8ee15b2b3`; lines 139-165,300-360; FLIP_SWNO and address bands.
- src/wpc/core.c: `84aa5ccddc077b60c1331e32ee13d3d577fd5109d4e7a90001692f737a1c7963`; lines 1700-1777,2182-2224,2591; button copies, synthetic outputs, no simData initialization.
- src/wpc/s11.c: `cd1b989ac1eec8c95126e743829a8a3726e76a9b838a29339776d4025d75d2d4`; lines 371-410,558-650,870-877,1188-1196; printer, mux, PIA and brightness models.
- src/wpc/sim.c: `20579da60adf58538d5b8c93a0bf22bd8c6d4e3ea6657234cd371293bd05c405`; lines 238; simulator-only output49.
