# Medusa retained runtime sources

Exact user-selected known-working table: JPSalas1.0.4, retained from
`L:/Visual Pinball/Tables Archive/Medusa (Bally 1981).vpx` after searching
Tables first. Original5894144bytes, SHA256
`35598302510b003baf68b5f9a274010b7325e639206c33203ff802f758eb7c3f`.
vpxtool `git:v0.33.3`; script35381bytes SHA256
`53cb05307a911b62104a18d0b8bbda667775071712de4a51bffec78ef60b148d`.
Full extraction836 content files10173989bytes; canonical JSON plus LF
manifest SHA256 `9754b28148f1c2661fbcd795e97b5e45bb514eadfd6715febd0ecc7c8c26021c`.
Algorithm: tools/build_external_evidence_manifest.py, case-sensitive POSIX
path order, each file path,size,SHA256, exclude only root manifest.json and
manifest.sha256. Recomputed, not an unexplained fixed digest.

## Active script regions (complete device-binding regions)

Lines79-124 initialize ball-stack switch8/BallRelease (one ball), saucer
sw19/switch19, right bank sw1-4/switch1-4 and top bank sw48..42/switch48..42.
Shield post starts pulled back, with alternate post2 dropped. Handlers
133-277 assert17 for either action key;18 from sw18/sw18a/sw18b;34-36 from
the three slings;37-40 from Bumper1-4;12-14,27,29,30 from standup targets;
20-26,28,31,32 from held triggers;33 from the spinner. Shared triggers:
25 sw25/sw25a,31 sw31/sw31a,32 sw32/sw32a. Drop-bank events hold their
target states until reset; outhole and saucer use the ball-stack helpers.

Lines283-312: ChangedSolenoids numbers1,2,3,4,5,6,8 are incremented by24
when Controller.Lamp(34) is set, then dispatched locally. Complete callbacks:

| Local callback | Action |
| --- | --- |
| 1 | knocker sound |
| 2 | right bank reset |
| 3 | top bank reset |
| 4 | top target6 knockdown |
| 5 | top target4 knockdown |
| 6 | top target2 knockdown |
| 7 | Shield post |
| 8 | outhole ball-stack out |
| 19 | game-on/GI visual helper |
| 25 | zipper open |
| 26 | zipper close |
| 27 | top target7 knockdown |
| 28 | top target5 knockdown |
| 29 | top target3 knockdown |
| 30 | top target1 knockdown |
| 32 | saucer out |
| sLRFlipper | right lower/upper flippers |
| sLLFlipper | left lower/upper flippers |

25-32 above are not public PinMAME outputs. Lines314-334 change alternate
flipper objects and write switch41=1 on open,0 on close. Lines336-351 fire
or pull back Post and switch alternate wall visibility. Lines353-453 tie GI
helpers to game-on and ball count; this does not reproduce the physical GI
wiring. Lower callbacks dim helper indices152/153, but the physical diagram
uses the upper flipper NC contacts for lower-flipper illumination.

The seven-target initialization explicitly orders sw48, sw47, sw46, sw45,
sw44, sw43, sw42, so SolHit 1 is the physical leftmost target. The callbacks
reverse this against the factory A3/identification: for example public3 with
lamp34=1 selects printed test18 / #1 target, but local callback27 calls SolHit7.
This is a retained table defect. The definition follows the factory mapping,
independently matched to public pulses by the ROM's displayed self-test number.

Complete active lamp address-to-object assignments, lines487-608:

```text
1:l1 2:l2 3:l3 4:l4,l4_1 5:l5 6:l6 7:l7 8:l8 9:l9 10:l10
11:l11(text) 12:l12 13:l13(text) 14:l14 15:l15
17:l17 18:l18 19:l19 20:l20 21:l21,l21_1 22:l22 23:l23 24:l24
25:l25 26:l26 27:l27(text) 28:l28 29:l29(text) 30:l30 31:l31
33:l33 35:l35 36:l36 37:l37,l37_1 38:l38 39:l39 40:l40 41:l41
42:l42 43:l43 44:l44 45:l45(text) 46:l46
47:l47,l47a,l47b,l47c,l47d,l47e 49:l49 51:l51 52:l52 53:l53,l53_1
54:l54 55:l55 56:l56 57:l57 58:l58 59:l59 60:l60 61:l61(text) 62:l62 63:l63
65:l65 66:l66 67:l67 68:l68 69:l69 70:l70,l70_1 71:l71,l71_1
81:l81 82:l82 83:l83 84:l84 85:l85 86:l86,l86_1 87:l87
97:l97 98:l98 99:l99 100:l100 101:l101 102:l102,l102_1 103:l103
113:l113 114:l114 115:l115 116:l116 117:l117 118:l118,l118_1 119:l119
150:lleft 151:lright
152:flipperlight1,flipperlight2,flipperlight3,flipperlight4
153:flipperlight5,flipperlight6,flipperlight7,flipperlight8
```

150-153 are script-only helper array indices.34 is read as a gate and has no
lamp object assignment.50 has no binding. The top-bar assignments order
65,81,97,113,66,82,98,114,67,83,99,115,68,84,100,116,69,85,101,117,60
left-to-right. L47/l47a and l47d/l47e have identical centers, l47b/l47c differ
only0.889VPXunits. They are render doubles, not six sockets. All inspected
lights have show_bulb_mesh=false. The29-object aGiLights collection and
eight flipperlight helpers therefore never establish physical socket counts.
`evidence/spatial/bally.medusa.1981.json` retains named extractor coordinates;
they remain candidates until reconciled per-device. No hidden off-table object
is clamped into a physical position.

## Retained VPinMAME libraries

| File | SHA256 |
| --- | --- |
| Bally.vbs3.61 | d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c |
| core.vbs | a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69 |
| VPMKeys.vbs | 563f599c5d5adf22ac0f9ba8cf2ffe90491fe868b72233f7e7b4960b81e8f4c1 |

Bally.vbs explicitly writes82(right) and84(left) in key handlers. Its generic
swTilt7 and swBallRollTilt2 are not Medusa's physical labels: Medusa's table
sets nudge TiltSwitch15, and its own matrix leaves7 unused and uses2 for a
drop target. Do not import generic cabinet-port labels as machine semantics.

## Fresh-state LibPinMAME observations

DLL SHA256 `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`,
built from pinned46e1a01a; CMake cache points to that clean source, win/x64.
User ROM archive medusa.zip SHA256
`4eb0235d9855ba41e35c78518a284b2d5ace024ad16b03615950a766185f9a88`.
All five members were checked against by35games.c sizes/SHA1:
720-53_6.7324096bytes61de956a4b6e9fb9ef2b25c01bff1fb5972284ad;
845-16_2.7324096bytese876eced0c02a2b4b3c308494e8c453074d0e561;
845-01_3.5324096bytese75356a20f81a68e6b27d2fa04b8cc9b17f3976a;
845-02_4.5324096bytesfa91cef2a244d25d408585d1e14e1ed8fdc8c845;
845-05_5.7162048bytes5c7cc43e57d8e8ded1cc109aa65c4f08052899b9.
No ROM or NVRAM is committed.

Raw traces under external review-artifacts/bally.medusa.1981/harness:

| Trace | SHA256 |
| --- | --- |
| explore-solenoid-run.json | 33ac9471b831c8e938139652d467d2c4d3b43fab2ddc2b3a83f9d88e1f0097f9 |
| explore-gameplay-run.json | c8b776f3720ff1e6e4f4ab08b5f35f869b707cf9caa45258cdd02b3829da1f1c |
| explore-flippers-run.json | c512588616944d75fb3a74e21a985ec7f78429181666903d9435c6683f3cec17 |

Command template: python tools/run_pinmame_harness.py --library <pinnedDLL>
--game medusa --rom-path <read-onlyROMroot> --work-dir <newisolatedstate>
--boot-wait 20 --scenario <matchingexplore-*.json> --output <rawtrace>.
Each run uses a distinct newly created state directory and20s stabilization,
HandleMechanics0 and direct switches only. These runs were collected using
Python3.12 for exploration while the required3.13 gate environment was pending;
the emulator/library behavior and raw artifact identities are unchanged by that
host-version limitation. No host input readback is presented as ROM evidence.

Self Test4 was reached with four negative7 edges. Reconstructed segment values
0x3f,06,5b,4f,66,6d,7d,07,7f,6f encode digits0-9 (mask comma bit0x80).
For a solenoid rise, read the last score display0 update within0.3s after it,
and gate34 at the actual rise. Printed01-15 map to public1-15 with gate0.
Printed16,17,18,19,20,21,22 map to1,2,3,4,5,6,8 with gate1.
Printed23/24 describe continuous coin-lockout18/enable19 from the wiring;
they are not manufactured from the momentary sequence.

Gameplay: coin10, Start6 with outhole8 occupied, then release8. Isolated
37->12,38->11,39->10,40->9;34->15,35->14,36->13; action17->7.
Tilt15 drops19. These responses independently agree with Figure V and rebut
the table's rotated bumper-handler bindings. The synthetic column run finds
only82->45/46 and84->47/48; every other81-88 input produces no added output,
with19 held enabled as a same-run control. Negative observations alone do not
prove absence; the six-column read path and core bit logic supply that proof.
