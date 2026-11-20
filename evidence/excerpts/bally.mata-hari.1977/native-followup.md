# Mata Hari native follow-up, November 20, 2026

Raw runs, validated harness scenarios, commands, archived input metadata and initial/final state are under `review-artifacts/bally.mata-hari.1977/online-followup/native-followup/`. LibPinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450` DLL SHA-256 is `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`. Each run used a new state directory, a 25-second boot wait, binary output mode, keyboard handling off and mechanics mask 0. The initial file uses the BY17 save format and stock default DIP bytes. Its CMOS is erased (`ff`) and mechanism positions are zero, unless the run metadata explicitly specifies a CMOS change. The runner set bank bytes in the initial state before startup and checked the persisted values after shutdown. The emulator reads them through its normal NVRAM handler. Score readings below come from the ROM's displayed segment frames, with comma bits masked. The host supplied the ball contacts and target transitions.

## Stock cabinet DIP controls

The baseline used `[00,00,18,00]` in the four DIP banks and the candidate used `[00,60,38,10]`, changing S14, S15, S22 and S29 together. After coin and serve, both sent two A/B pairs, three target edges including a reclose, and four separate saucer visits. Their after-start lamp and solenoid snapshots, decoded player-one score, and per-step rising coil groups agree. The five-ball control `[00,80,18,00]` lit only left lamp 57 on the first A/B pair, then added right lamp 41 on the second. Both lamps lit on the first pair with S16 off. Conservative saucer visits each scored 3,000 and fired coil 1. The first lit 2X potential (58). The next three attained 2X, 3X and 5X (60, 44 and 28 respectively). The bounded comparison corroborates the [stock DIP read path](stock-rom-read-path.md).

## Free-play patches and display changes

- `mataharb`, S17–19 on, required an initial coin on erased CMOS. After that coin, credits stayed at 01 through Start and adding the second player. With S19 off, the same coin was spent on Start and the attempt to add a player was ignored. Player one briefly displayed revision 02 at boot.
- `matatest` showed the 07 fields at startup, required an initial coin on erased CMOS, and awarded 3,000 on the first top A closure after serve. S27 lit the credit field in the retained comparison. Both erased-CMOS runs with S27 on showed 01 after one coin and Start, including the S26-off control. The documented S25/S26 check has an independent [ROM read path](firmware-variants.md), and the erased-state comparison does not isolate its replenishment branch.
- `mataharc` required a coin with the stock settings. S18/S19 on produced an initial 9 in free play. With S17 off, it counted 9→8→7 through Start and second-player join. With S17 on, it blanked the credits at Start, held lamp 59 on and added the second player at zero. Both free-play options scored 500, 0, then 500 for target D, a reclosure of D and then C. Stock scored all three closures, including the reclosure.
- Both V22 drivers started without a host coin with S17/S18 on. The erased-CMOS probes showed a boot balance of 15 and counted down to 14 on Start. The S18-off control with the same S17 setting did not start. Both V22 variants scored 500, 0, then 500 for the same target reclosure probe. The seven-digit variant showed the full `1172400`; the six-digit variant alternated between `172400` and `117240` after scoring settled. Those modes used the same game sequences and the same public reset coils, with opposite S19 values. The seven-digit case preserved the two-digit credit and match fields.

## Spare outputs across all six drivers

This accounting uses the 26 `trace.json` files listed in the `native-followup/manifest.json` at the path above, SHA-256 `37f8d08fac0627c89c9a4657c4be4aa92a656380c172ab3ccb74c1178e746679`. A transition is one recorded binary callback event for the specified address, counting both states. A match means identical ordered `(time_s, state)` pairs for each lamp within a trace. One boot pulse is one state-1 event followed by one state-0 event, both before the first `booted` snapshot. Times are host callback times. Every run has matching sequences for lamps 4 and 20 and exactly one boot pulse per solenoid 17 and 20. Counts below are per lamp address and show the distribution across runs.

| Driver | Runs | Lamp transitions per address (runs × transitions) | Example run group |
| --- | ---: | --- | --- |
| `matahari` | 3 | 3 × 17 | `stock-baseline`, `stock-five-ball`, `stock-unassigned` |
| `mataharb` | 4 | 2 × 18, 2 × 19 | `oliver-b-*`, including the credit-enabled and credit-control pair |
| `mataharc` | 3 | 2 × 17, 1 × 22 | `user-freeplus-clear` and `-preserve` have 17 each, `-control` has 22 |
| `matahard` | 4 | 3 × 17, 1 × 18 | `quench-six*` have 17 each, `quench-control` has 18 |
| `matahard7` | 3 | 3 × 17 | `quench-seven*`, including both million-score runs |
| `matatest` | 9 | 7 × 42, 2 × 51 | `oliver-test-enabled` and `oliver-test-zero-enabled` have 51 each |

In each of the 17 traces for drivers other than `matatest`, every lamp 4/20 edge timestamp coincides with an event on at least one fitted A/B lamp (36 or 52). Some A/B events occur separately. In the nine `matatest` traces, 12 of 42 spare-edge timestamps coincide with either fitted lamp in seven runs, and 15 of 51 coincide in the other two. These counts compare host callback timestamps.

The factory [ROM paths](stock-rom-read-path.md) explain the PIA assertion and the stock whole-byte strobe writes. In `matatest`, the [revision 7 attract handler](derivative-dip-read-path.md#revision-7-first-attract-interval) complements the entire strobe byte at `$0203` via `$13c2`–`$13ca`, including the unfitted lamp bits. The [factory lamp](lamp-wiring.md) and [solenoid](solenoid-wiring.md) drawings establish that these four channels have no fitted load. Separate [stock service runs](native-runs.md) cover the operator sweeps.

| Native run directory | Driver | SHA-256 of trace.json |
| --- | --- | --- |
| stock-baseline | matahari | `8257385e51a3f776144e5ea0fb5463efc8a662eb9c936ffb5b435145c22a73c1` |
| stock-five-ball | matahari | `6ec05b796c9a34ef7d55d4a249a0c2c0e4fdf7c4860b38440ea2708a190d75e7` |
| stock-unassigned | matahari | `4f1a591732fa9f808358d90956c3187cb6a90db911feb2258aab4243428fb901` |
| oliver-b-control | mataharb | `715ea5700fa95f7976c09f634540806a7d6a0de7fb27afc4afeaefced13f32eb` |
| oliver-b-credit-control | mataharb | `d80c48121c049e8847fe66cc02ea03dabec59a9bf843c78099d2181aa63233d5` |
| oliver-b-credit-enabled | mataharb | `c6882dad41490e327ac6d05d8cdc7ce3ae62ab98eb5e358aa598ce112defd5a4` |
| oliver-b-enabled | mataharb | `38ff7dfa098f4e4d34c6cb942a3b8799625d3b39ad981df533254b24540f4732` |
| oliver-test-control | matatest | `902fa0269ef199bb76846f235689f4de1b2f86e6a47d12d9fd862e5a427e625e` |
| oliver-test-credit-control | matatest | `d6d9bb248bc7f53ffb9772d69ee8cd950b7a2ff93351de0bc991d4e0ee6c01a8` |
| oliver-test-credit-enabled | matatest | `3a51a2c717f1083800cd476726126f1fd957a516420a2844c5ef41792a88baac` |
| oliver-test-enabled | matatest | `994bc5511da7fa734b14353da93a96772f2cba9e40e2b4a33cf56c7d514e5d4a` |
| oliver-test-visible-control | matatest | `091e26c6e646e870801d0cb69d5a7f98bd2bdd2b1b706a312c939c7db066b255` |
| oliver-test-visible-enabled | matatest | `4c224e0ec3b6925a84f865b2f23678f3b58814c4793a7c7b5c695ced283b03d9` |
| oliver-test-visible-neither | matatest | `60e12bacdd85a90fa32a7d0abc7f3e884cad86caca1f7d8bc6e1733c2e2633b5` |
| oliver-test-zero-control | matatest | `290acfe31037e67894fa91397a71833c2c7c90f385cf23585e94da0ab2056bdc` |
| oliver-test-zero-enabled | matatest | `7795d9490ab5dcd510e28f4f98553740f133e001bf351b49c60aa403d020163d` |
| user-freeplus-clear | mataharc | `a299abbd97fda1e2a629468c7c04390332f062b41a1fa03391e58de22508bde9` |
| user-freeplus-control | mataharc | `4b2a78d3324fb8b7b0580e32c573b83d6bf216f38bd6e385e9abf54572502281` |
| user-freeplus-preserve | mataharc | `75941555b35cf48d612783c2b3e899eb4f928bd9da27e8b5c9308535cd76c3ff` |
| quench-control | matahard | `2c821de0a363892449c730d8df8cddb80edb9d14ef9e0e15a77748eaf95556b3` |
| quench-six | matahard | `eebf71a42528c42016bd5128dc260e2760ae61ada82abc78ff57a27204bbf424` |
| quench-seven | matahard7 | `8044a7903885cb648a931b8b37ba31fc6d8c0f96f131d2f2186e38eb02ca220d` |
| quench-six-million-idle | matahard | `02a198d7a9a5a24f64828e15d988fd2e90cc3d92022fc30c66844b584883f962` |
| quench-six-millions | matahard | `174989c467b6e1a6d09739d15d17f353832facc352a84fb4dccb7997a4531056` |
| quench-seven-million-idle | matahard7 | `8b8c436f50667610866c1414f9b8f06fb81fca8d9f8127a18a18bb9ab07673aa` |
| quench-seven-millions | matahard7 | `a55ae5f06e19a0e56128c8a1e6377aed8b8474f5de9ab93f8e9dd46037df449d` |
