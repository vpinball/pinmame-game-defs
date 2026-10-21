# Joker Poker 1.1: retained runtime bindings

Source: `extracted/script.vbs`, SHA-256
`07c82d5f27b3c49961676cd8ef6840caf5a0720ecdafe6b3910994a40bed02b1`.
The exact embedded script uses Windows-1252 encoding. Transcription method:
manual code inspection, GPT Sol, 2026-10-21. This records what
the retained implementation does; launch/play verification has not been supplied.

The table declares `cGameName="jokrpokr"`, loads `GTS1.VBS`, sets UseSolenoids=1,
UseLamps=1 and UseGI=0. It disables controller keyboard and mechanism handling.
The initial solenoid mask is zero and a 2,000 ms timer restores `&Hffffffff`.

## SolCallback assignments (complete region, lines 49-71)

| Public address | Callback behavior |
| --- | --- |
| 1 | bsTrough.SolOut |
| 2 | SolKnocker |
| 3 | vpmSolSound 10, or 10_pf according to ChimeSound |
| 4 | vpmSolSound 100, or 100_pf according to ChimeSound |
| 5 | vpmSolSound 1000, or 1000_pf according to ChimeSound |
| 6 | dtjj.SolDropUp |
| 7 | dtqq.SolDropUp |
| 8 | dtaa.SolDropUp |
| 17 | vpmNudge.SolGameOn |
| sLRFlipper | SolRFlipper: RightFlipper and RightFlipper1 move together |
| sLLFlipper | SolLFlipper: LeftFlipper moves |

ChimeSound defaults to 0. That is an audio option of the recreation, not evidence
that the production machine has electronic tones instead of chimes.

## Ball stack and targets (complete initialization, lines 204-226)

`bsTrough.InitNoTrough BallRelease,66,90,10` models a single-ball outhole with switch
66. Drain_Hit adds the ball to this stack. The 90-degree/10-speed launch values
are recreation tuning, not physical specifications.

| Instance | Objects in ordered InitDrop array | Switch array | Reset |
| --- | --- | --- | --- |
| dtjj | sw21, sw22, sw23 | 21,22,23 | solenoid 6 |
| dtqq | sw31, sw32, sw33 | 31,32,33 | solenoid 7 |
| dtkk | sw41, sw42, sw43, sw44 | 41,42,43,44 | lamp 17 rising edge calls DropSol_On |
| dtaa | sw50, sw51, sw52, sw53, sw54 | 50,51,52,53,54 | solenoid 8 |

Each corresponding hit handler calls its bank's Hit method with the 1-based
target index. Thus switches stay down through cvpmDropTarget until the bank resets.
The 10/J pair and four-target Kings bank do not share a reset output.

## Direct switch handlers (complete region, lines 295-386)

| Address | Bound object(s) | Assertion |
| --- | --- | --- |
| 10 | Bumper1, Bumper2 | PulseSw |
| 11 | sw11, sw11b | set 1 at Hit, 0 at UnHit |
| 12 | sw12, sw12b, sw12d | set 1 at Hit, 0 at UnHit |
| 13 | sw13, sw13b | set 1 at Hit, 0 at UnHit |
| 20 | sw20 | PulseSw |
| 30 | sw30 | set 1 at Hit, 0 at UnHit |
| 40 | sw40a through sw40j and LeftSlingshot | PulseSw |

The 11 contacts at address 40 comprise ten passive scoring-rubber regions plus
the powered left kicking rubber. Wall centroids are candidate interaction-region
anchors, not measured leaf-switch positions.

## Lamp region (complete assignments, lines 388-421)

Lamp 17 is read separately through LampCallback=UpdateMultipleLamps. Its rising
edge resets dtkk. The Lights array has exactly these 21 mappings, all one-to-one:
4:l4, 8:l8, 9:l9, 10:l10, 11:l11, 12:l12, 13:l13, 14:l14, 15:l15, 16:l16,
18:l18, 19:l19, 20:l20, 21:l21, 22:l22, 23:l23, 24:l24, 25:l25, 26:l26,
27:l27, 28:l28. A lamp's render region is not evidence of a physical bulb socket.
All objects in collection GI are forced on; no controller GI callback is used.

## Retained shared library

The table loads local gts1.vbs 3.61, SHA-256
`554da222cdff8080854c9bf59ad891fd8f44f2a3013deba4f6f0d62058ca3d78`.
Its cabinet constants are Test=00, Coin1=01, Coin2=02, Start=03, Tilt=04,
Slam=76, CPU diagnostic/audits reset=56, right flipper=82, left flipper=84.
KeyDown sets start/test/slam/56 and flipper buttons true; KeyUp clears them.
Coin events use a 750 ms delayed PulseSw. The library loads core.vbs and
VPMKeys.vbs; their exact bytes are retained and hash-checked by the curator.
