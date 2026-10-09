# Stargate (Gottlieb 1995) v2.0 (VPW): controller bindings

Source: the embedded script of the retained `Stargate (Gottlieb 1995) v2.0.vpx` (VPin Workshop, table version 2.0,
saved 2025-09-24), extracted with vpxtool as `script.vbs` (SHA-256
`eda1f035a56672f83411efe228ff98291a2bdaf9b85114d1da7dc4ab337974a1`). The pinned `sverrewl/vpxtable_scripts` corpus holds
the same script as `Stargate (Gottlieb 1995) v2.0.vbs`: compared with blank lines and whitespace ignored, the only
difference is a `Table1_exit` sub the corpus copy appends. Line numbers are the extracted file's. Leading whitespace is
dropped and a run of lines is joined with " | "; comments are kept where they say what a line is for.

## Controller

| Line | Text |
| --- | --- |
| 60 | `Const cGameName="stargat5"` |
| 75 | `Const UseSolenoids = 2 '1 = Normal Flippers, 2 = Fastflips` |
| 109 | `LoadVPM "03060000", "GTS3.VBS", 3.10` |
| 127-129 | `TournamentTimer.Interval = 3000 'If you have "switch short return 5 / 6" message at ROM startup, 'set it to 3000 and Increase it in steps of 100 untul it desapear 'between each restart of VPX` |
| 228 | `vpmMapLights AllLamps` |
| 236, 240 | `.HandleKeyboard = 0` · `.HandleMechanics = 0` |
| 261-266 | `Set SBall1 = swTrough1.CreateSizedballWithMass(...)` · `SBall2 = swTrough2...` · `SBall3 = swTrough3...` · `Set SBall4 = Drain.CreateSizedballWithMass(...)` · `Controller.Switch(34) = 1` · `Controller.Switch(24) = 1` |
| 3726-3729 | `sub TournamentTimer_Timer()` (under the banner `JLouLou SYS3 Freeplay & Tournament MOD`) · `Controller.Switch(5)=1` · `Controller.Switch(6)=1` · `TournamentTimer.Enabled = False` |

## Solenoid callbacks (lines 740-774)

| Line | Text |
| --- | --- |
| 740-746 | `'SolCallback(1)=""  'Bumper 1` · `'SolCallback(2)=""  'Bumper 2` · `'SolCallback(3)=""  'Left SlingShot` · `'SolCallback(4)=""  'Right SlingShot` · `'SolCallback(5)=""  'sw14 kickback` · `'SolCallback(6)=""  'sw15 kickback` · `'SolCallback(7)=""  'sw16 kickback` (all commented out) |
| 747 | `SolCallback(8) = "SolLeftPlunge"` |
| 748 | `SolCallback(9) = "SolAutoFire"` |
| 749 | `SolCallback(10) = "LeftPop"` |
| 750 | `SolCallback(11) = "BotPop"` |
| 751 | `SolCallback(12) = "VukTopPop"` |
| 752 | `SolCallback(13) = "SolDiv"` |
| 753 | `SolCallback(14) = "SolPivL" 'Left Pivot Target` |
| 754 | `SolCallback(15) = "SolPivR" 'Right Pivot Target` |
| 755 | `SolCallback(16) = "SolPyramid" 'Pyramid Unit` |
| 756-759 | `SolCallback(17) = "LeftDropUp"` · `SolCallback(18) = "TopDropUp"` · `SolCallback(19) = "RightDropUp"` · `SolCallback(20) = "RightDropTrip"` |
| 760 | `'SolCallback(21)=""  'Not Used` |
| 761 | `SolCallback(22) = "SolBGRopeLights"  'Rope Lights Backglass` |
| 762 | `SolCallback(23) = "SolGlid1" 'Left and Right Glide Motor` |
| 763 | `SolCallback(24) = "SolGlid2" 'Forward Glide motor` |
| 764 | `'SolCallback(25)=""  'Not Used` |
| 765 | `SolCallback(26) = "SolBBGI" 'BackBox GI used as PF GI` |
| 766 | `'SolCallback(27) = "" 'Ticket dispenser` |
| 767-769 | `SolCallback(28) = "SolRelease"` · `SolCallback(29) = "SolTrough"` · `SolCallback(30) = "SolKnocker"` |
| 770 | `SolCallback(31) = "GIState" 'Tilt Relay and PF GI` |
| 771 | `'SolCallback(32)=""  'Game Over Relay` |
| 1767-1769 | `SolCallback(sLRFlipper) = "SolRFlipper"` · `SolCallback(sLLFlipper) = "SolLFlipper"` · `SolCallback(sURFlipper) = "SolURFlipper"` |

## Solenoid handlers

| Lines | What the handler does |
| --- | --- |
| 782-792 | `SolDiv`: on `Flipper1.RotateToEnd` and `Controller.Switch(101)=1`, off `Flipper1.RotateToStart` and `Controller.Switch(101)=0` (sounds `S13_LowerLeftBallGateOpen`/`Close`) |
| 815-824 | `GIState(Enabled)`: `If Not Enabled Then gilvl = 1 ... Else gilvl = 0` and every light of the `GI` collection takes `gilvl` |
| 837-843 | `SolBBGI`: both branches commented out |
| 879-885 | `SolTrough`: `Drain.kick 57, 20` |
| 887-893 | `SolRelease`: `swTrough1.kick 57, 10` (sound `S28_BallRelease`) |
| 895-900 | `SolLeftPlunge`: `sw25.Kick 0, 40` (sound `S08_LowerLeftKicker`) |
| 941-949, 966-974, 991-999 | `VukTopPop` kicks the ball held at `sw33`, `BotPop` the one at `sw23`, `LeftPop` the one at `sw80`, straight up (`KickBall ..., 0, 0, 40|60|40, 0`) |
| 1003-1010 | `SolAutofire`: `APFlipper.RotateToEnd`, `PlungerIM.AutoFire` |
| 1269-1283, 1299-1313 | `SolPivL`/`SolPivR`: on, `sw116`/`sw117` and their `...a` walls stop colliding and `LeftFlipper2`/`RightFlipper2` rotate to end (`S14_LeftPivotTargetOpen`, `S15_RightPivotTargetOpen`); off, they collide again |
| 1329-1343 | `SolPyramid`: on `PyramidOpen = -1`, off `PyramidOpen = 0`, then `vpmTimer.AddTimer 500, "Controller.Switch(102)=" & PyramidOpen & "'"` (sounds `S16_TopPyramidOpen`/`Close`) |
| 1515-1523 | `SolGlid1` sets `GliderLROn`, `SolGlid2` sets `GliderFROn` |
| 1406-1416 | `GliderTimer_Timer`: `Controller.Switch(21) = 1` while `GliderY <= GliderYMin + 2`, else 0; `Controller.Switch(30) = 1` while `GliderRot > GliderRotMax - 1`, else 0. Nothing writes 20. |
| 1551-1584 | `LeftDropUp` raises 17, 27, 37; `TopDropUp` raises 26, 36; `RightDropUp` raises 35 (`S19_RollOverTargetReset`); `RightDropTrip` drops 35 (`S20_RollOverTargetTrip`) |

## Switch writers

| Lines | Text |
| --- | --- |
| 653-661, 688-697 | key down: `Controller.Switch(81) = 1` on `LeftFlipperKey`, `Controller.Switch(82) = 1` on `RightFlipperKey`; key up writes 0 |
| 673, 707 | `If keycode = RightMagnaSave Then Controller.Switch(5) = 1  'Tournament Mode` / `= 0` |
| 683, 712 | `If vpmKeyDown(keycode) Then Exit Sub` (end of `table1_KeyDown`) · `If vpmKeyUp(keycode) Then Exit Sub` (end of `table1_KeyUp`) |
| 785, 789 | `Controller.Switch(101)=1` / `=0` (in `SolDiv`) |
| 856-863 | `swTrough3_UnHit : Controller.Switch(34) = 0` · `swTrough3_Hit : Controller.Switch(34) = 1` · `Drain_UnHit : Controller.Switch(24) = 0` · `Drain_Hit : Controller.Switch(24) = 1` |
| 903-904 | `Sub sw25_Hit: Controller.Switch(25) = 1` · `Sub sw25_UnHit: Controller.Switch(25) = 0` |
| 928-939, 953-964, 978-989 | `sw33_Hit`/`UnHit` write 33, `sw23_Hit`/`UnHit` write 23, `sw80_Hit`/`UnHit` write 80 |
| 1018-1019, 1049-1050 | `Sub Bumper1_Hit` · `vpmTimer.PulseSw(10)`; `Sub Bumper2_Hit` · `vpmTimer.PulseSw(11)` |
| 1115 | `Sub sw22_Hit:vpmTimer.PulseSw 22` |
| 1118-1129 | `SW31_Hit`/`unHit` write 31; `SW111`-`SW115` `_Hit`/`_unHit` write 111-115 |
| 1189-1191 | `Sub sw90_Hit :vpmTimer.PulseSw 90` · `sw100_Hit ... 100` · `sw110_Hit ... 110` |
| 1256-1257 | `Sub sw91_Hit` · `vpmTimer.PulseSw 91` |
| 1339 | `vpmTimer.AddTimer 500, "Controller.Switch(102)=" & PyramidOpen & "'"` |
| 1407-1415 | `Controller.Switch(21) = 1` / `0`, `Controller.Switch(30) = 1` / `0` |
| 1531-1548 | `sw17_Hit: DTHit 17` · `sw27_Hit: DTHit 27` · `sw37_Hit: DTHit 37` · `sw26_Hit: DTHit 26` · `sw36_Hit: DTHit 36` · `sw35_Hit: DTHit 35` · `sw32_Hit: STHit 32` · `sw116_Hit: STHit 116` · `sw117_Hit: STHit 117` |
| 1871, 1897 | `vpmTimer.PulseSw(13) 'Sling Switch Number` (right) · `vpmTimer.PulseSw(12)` (left) |
| 2945-2947 | `Set ST32 = (new StandupTarget)(sw32, BM_ST_sw32, 32, 0)` · `Set ST116 = (new StandupTarget)(sw116, BM_GuardianL, 116, 0)` · `Set ST117 = (new StandupTarget)(sw117, BM_GuardianR, 117, 0)` |
| 3033 | `vpmTimer.PulseSw switch mod 100` (in `STAnimate`, the only place a stand-up target's switch is pulsed) |
| 3164-3169 | `Set DT17 = (new DropTarget)(sw17, sw17a, BM_DT_sw17, 17, 0, false)` and the same for 27, 37, 26, 36, 35 |
| 3342, 3398 | `controller.Switch(Switchid mod 100) = 1` when a drop target finishes dropping · `= 0` when it is raised |
| 3466-3468 | `Sub sw14_Hit: KTHit 14` · `sw15_Hit: KTHit 15` · `sw16_Hit: KTHit 16` |
| 3645, 3676 | `vpmTimer.PulseSw arr.sw` (kicking target), followed by the script's own kick of the ball and the sound `S05_LeftKickingTarget`/`S06_Center...`/`S07_Right...` |

Because `STAnimate` pulses `switch mod 100`, a hit on the left or right Horus target (116, 117) pulses 16 or 17 in this
table, not 116 or 117.
