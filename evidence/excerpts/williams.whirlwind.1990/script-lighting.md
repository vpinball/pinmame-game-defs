# Whirlwind retained script lighting bindings

Factual transcription from the embedded working `script.vbs`, SHA-256
`e478206db1045fa9e0f82668a4b78d00678b323c151245df02f9e14d096cf8d2`.
Source locations: SolCallback registrations around lines 846–875,
Sol25–Sol40 around lines 914–1037, GI handlers 1042–1070, and
UpdateLamps at lines 1802–1897. This table lists all eleven flasher
circuits; each also drives the corresponding FlSol backglass/VR proxy.

| Public solenoid | SetLamp channel | Playfield effects in UpdateLamps |
| --- | --- | --- |
| 25 | 125 | f125, f125a |
| 26 | 126 | f126 |
| 27 | 127 | f127, f127a, f127b |
| 28 | 128 | f128, f128a |
| 29 | 129 | f129, f129a, f129b |
| 30 | 130 | f130, f130a |
| 31 | 131 | f131, f131a |
| 32 | 132 | f132 |
| 37 | 137 | f137 |
| 39 | 139 | f139 |
| 40 | 140 | f140 |

The extracted Light objects are in playfield space, with
`show_bulb_mesh=false`. FlSolNN objects belong to BGArr and have backglass
coordinates. Neither object count is a physical socket count. The factory
table and construction drawing, rather than renderer proxies, establish
physical quantity and fitment.

`SolUpperGI` (11) sets UpperGI members to 0 when enabled and 1 otherwise;
it also changes bghigh/bghigh2 visibility. UpperGI has no members in the
retained extraction. `SolLowerGI` (16) similarly sets LowerGI members to
0/1 and hides/shows Flasher4. LowerGI contains only Light1. Thus a public
solenoid value of 1 commands GI darkness in this script, and a value of
0 commands light. The one modeled bulb and full-table overlay cannot
stand for the machine's complete controlled socket inventory.

UpdateLamps skips lamp 9: after FadeRm for 8 it continues with NfadeL 10.
The same extraction nevertheless contains Light.l9. That omission is a
table defect, not evidence that the physical left-outlane lamp is absent.
