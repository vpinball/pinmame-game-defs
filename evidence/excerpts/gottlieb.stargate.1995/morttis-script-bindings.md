# Stargate VPX v1.3.0 (32Assassin and JLouLoulou): controller bindings

Source: the embedded script of the retained `Stargate ( Gottlieb 1995 ) - v.1.3.0 - Led Lights - rev.1.1
[D&N][CC][FSS][DMD][10.6+][Morttis].vpx`, extracted with vpxtool as `script.vbs` (SHA-256
`113a65ebceab8ad9912eb122390302e14991cc340f1e8c49dae46bd7a931ecba`). Its header reads "STARGATE VPX V1.3.0 from
32Assassin and JLouLoulou ... All made from real Stargate scan, redraw etc etc". The retained "Original Lighs - rev.1.2"
build of the same release (script SHA-256 `110bb09404fbbf3b1e0321e1526afb9854fbcfe0250b2e7b166b68516a86fe1e`) differs
only in its lamp-overlay list, which adds `flamp113` lit from `Controller.Lamp(112)`, and its `ColoredGI` default. The
VPW v2.0 table credits this release as the one it rebuilt, so the two scripts are not independent. Line numbers are the
extracted file's; leading whitespace is dropped.

| Line | Text |
| --- | --- |
| 32 | `Const cGameName="stargat5",UseSolenoids=2,UseLamps=0,UseGI=0, SCoin="coin"` |
| 267 | `LoadVPM "01560000", "GTS3.VBS", 3.26` |
| 332-344 | `SolCallback(8) = "bsSaucer.SolOut"` · `(9) = "SolAutoFire"` · `(10) = "LeftPop"` · `(11) = "BotPop"` · `(12) = "VukTopPop"` · `(13) = "SolDiv"` · `(14) = "SolPivL" 'Left Pivot Target` · `(15) = "SolPivR" 'Right Pivot Target` · `(16) = "SolPyramid" 'Pyramid Unit` · `(17) = "dtL.SolDropUp"` · `(18) = "dtT.SolDropUp"` · `(19) = "dtR.SolDropUp"` · `(20) = "dtR.SolHit 1,"` |
| 345-360 | `'SolCallback(21) = "" 'Not Used` · `SolCallback(22) = "fnFlSol22" 'Rope Lights Backglass` · `(23) = "SolGlid1" 'Left and Right Glide Motor` · `(24) = "SolGlid2" 'Forward Glide motor` · `'SolCallback(25)="" 'Not Used` · `'SolCallback(26) = "PFGI" 'BackBox GI used as PF GI` · `'SolCallback(27) = "" 'Ticket dispenser` · `(28) = "bsTrough.SolOut"` · `(29) = "bsTrough.SolIn"` · `(30) = "vpmSolSound SoundFX(""S30_Knocker"",DOFKnocker),"` · `(31) = "PFGI" 'Tilt Relay and PF GI` · `'SolCallback(32) = "" 'Game Over Relay` |
| 538 | `.HandleMechanics=0` |
| 560-565 | `Set bsTrough = New cvpmBallStack` · `'bsTrough.InitSw 24,0,0,0,34,0,0,0` (commented) · `bsTrough.InitSw 24,34,34,34,34,0,0,0` · `bsTrough.InitKick ballrelease,90,10` · `bsTrough.Balls = 4` |
| 578-579 | `Set bsSaucer=New cvpmBallStack` · `bsSaucer.InitSaucer sw25,25,0,35` |
| 584-597 | `dtR.InitDrop sw35,35` · `dtL.InitDrop Array(sw17,sw27,sw37),Array(17,27,37)` · `dtT.InitDrop Array(sw26,sw36),Array(26,36)` |
| 771-774 | `If KeyCode=LeftFlipperKey Then Controller.Switch(81)=1` · `If KeyCode=RightFlipperKey Then Controller.Switch(82)=1` · `'If keycode=29 then controller.switch(5)=Not Controller.Switch(5) 'tournament switch` (commented) · `If keycode=207 then controller.switch(6)=Not Controller.Switch(6) 'door switch` |
| 925-926 | `Sub Bumper1_Hit : vpmTimer.PulseSw(10) : PlaySoundAtVol SoundFX("S02_BumperBottom",...)` · `Sub Bumper2_Hit : vpmTimer.PulseSw(11) : ... "S01_Bumper_Top"` |
| 929-933 | `'Kicking Stand Up Targets` · `Sub sw14_Slingshot:vpmTimer.PulseSw 14 ... "S05_LeftKickingTarget"` · `sw15_Slingshot ... PulseSw 15 ... "S06_CenterKickingTarget"` · `sw16_Slingshot ... PulseSw 16` |
| 937-939 | `'StandUp Target` · `Sub sw22_Hit:vpmTimer.PulseSw 22` · `Sub sw32_Hit:vpmTimer.PulseSw 32` |
| 943-954 | `SW31_Hit`/`unHit` write 31; `SW111`-`SW115` `_Hit`/`_unHit` write 111-115 |
| 957-962 | `Sub sw90_Hit :vpmTimer.PulseSw 90` · `sw100_Hit ... 100` · `sw110_Hit ... 110` · `Sub sw91_Hit:vpmTimer.PulseSw 91 : PlaySoundAtVol"popperball_pyramide"` |
| 970 | `Sub sw116_Hit : vpmTimer.PulseSw 116 : PlaySoundAtVol SoundFX("Target",DOFTargets)` |
| 972-982 | `Sub SolPivL(Enabled)`: on `sw116.isdropped=true` and `LeftFlipper2.RotateToEnd` (`S14_LeftPivotTargetOpen`); off `sw116.isdropped=false` (`S14_LeftPivotTargetClose`) |
| 988 | `Sub sw117_Hit : vpmTimer.PulseSw 117 : PlaySoundAtVol SoundFX("Target",DOFTargets)` |
