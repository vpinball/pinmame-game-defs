# Mata Hari native evidence, 20 November 2026

LibPinMAME `46e1a01a0f73dc5ce163d98db1ae435883ecc450`.
`pinmame64.dll` SHA-256
`8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`.
Fresh state directories per run, binary output mode, keyboard
handling off, mechanics mask 0, factory numeric service displays.
Run JSON is under `review-artifacts/bally.mata-hari.1977/native-traces`,
with one full-file manifest built by
`tools/build_external_evidence_manifest.py`. Manifest SHA-256
`77b1e24392747e450a2cce02ec805cc1985e76024e9731206d3eb22494747f69`.
The three isolated state directories are beside it. ROM members
were verified against the pinned loader SHA-1s.

| Run | ROM archive SHA-256 | Trace SHA-256 |
| --- | --- | --- |
| native-stock-gameplay-20261120.json | 93c96382262c7624bbde461f5f3f59d5be9c876f9f0804a0fb7ee2d139259f8d | d30115b51d20431f066f9282ff249e319503e29e8490f75a40269c8cfe2112aa |
| native-stock-service-20261120.json | 93c96382262c7624bbde461f5f3f59d5be9c876f9f0804a0fb7ee2d139259f8d | b08a6111792a09ab664b44f6aac66608b56b7acd2faecf11e1b53c77b70dd663 |
| native-v22-7-layout-20261120.json | 94ab62eabd52ba20c17c6c932c509ccdf73da3466c6da95788fd4492bd7703ee | 4f8ddf494cd4e1af4647e109ce78a2dbfcbf54e8ba221aba5656c3533809b6c1 |

Stock invocation template:

```text
python -B tools/run_pinmame_harness.py --library <DLL> --game matahari --rom-path <authorized-ROM-root> --work-dir <fresh-state> --scenario tools/harness-scenarios/by17/matahari-<gameplay-or-service>.json --output <trace>
```

`matahari-gameplay.json` SHA-256
`6d255cdcacdc5ab05ef7c810bd9e160d34c4d9f6088440000aae48e3e53e507c`.
`matahari-service.json` SHA-256
`835a2ad2ffef6c80901831a00de0b61ce191cd781c6294ed94c91fbf5f3ffd2f`.
For the alternate display probe use `--game matahard7 --boot-wait 25
--observe 0` with its own fresh state, in place of `--scenario`.

## Stock service walk

The first door self-test press flashed the four sets of fifteen lamp
addresses, including electrically reachable drivers with no load.
The second press ran the segment test and the third began the coil
test. The first two complete sweeps (starting with public 7)
both were `7,6,2,3,4,5,8,9,10,11,12,14,1,13,15,18,19`.
This is FO 579 order 01 through 17. The published segments and
coil pulse timestamps pair in the same order, with brief partial
frames from display multiplexing. The fourth press entered the
stuck-switch test. It displayed 32 during the saucer hold and 12
during an isolated injected hold on unfitted matrix position 12.
An open matrix flashed 0 in the match/ball-in-play field.

## Stock gameplay

These are public output transitions from separate host inputs.
The host supplies ball movements and target-latch states.

| Action | Observed ROM or core output |
| --- | --- |
| Coin I (10) | Chime 5 and credit indicator 59 |
| Start (6), 8 held | Outhole 7, bank resets 13/15 and enable 19 |
| Right button 82 | Both 45 and 46 for one hold |
| Left button 84 | Both 47 and 48 for one hold |
| Bottom left thumper 38 | 8 and chime 3 |
| Top left thumper 40 | 9 and chime 3 |
| Top right thumper 39 | 10 and chime 3 |
| Bottom right thumper 37 | 11 and chime 3 |
| Right sling 35 | 14 and chime 2 |
| Left sling 36 | 12 and chime 2 |
| Saucer 32 held | Kicker 1, chime 4, eventual bonus 4K and 2X potential |
| Right D–A held | No bank-reset assertion for right completion alone |
| Left D–A then held | Both reset drives 13/15 and lamp 51 when the second bank completed |
| Tilt 7 | Relay 19 fell and tilt legend 61 rose |
| Right button after tilt | No flipper-pair assertion |

The two unfitted continuous load lines 17/20 pulsed during startup.
The stock gameplay trace records identical lamp 4 and 20 edges
from 8.110 to 27.485 s. During attract the regular edges are about
one second apart, or about two seconds per full blink cycle. Both
bits are on in every recorded in-play snapshot. The factory
harness marks both branches N/U. The [stock read-path follow-up](stock-rom-read-path.md) explains these transitions and the spare solenoid assertions.

## Stock A/B lane and lower bumper probe

The successor run uses the same stock ROM and DLL hashes above,
with fresh state in `state-ab-lamps-89e71fae5467`, default DIPs
(S16 off, three balls per game), keyboard handling off and mechanics
mask 0. No service inputs are sent. Repeat with the stock invocation
template using `tools/harness-scenarios/by17/matahari-ab-lamps.json`.

| Artifact | SHA-256 |
| --- | --- |
| Scenario `matahari-ab-lamps.json` | `00b2ccb1fad31699742cb46b932d3ba72c9fc9816d40a2e7f27842d1c4d72593` |
| Raw `review-artifacts/bally.mata-hari.1977/native-ab-lamps-89e71fae5467/trace.json` | `10f98b319c8dad465986fae54f86c04f22bca5496e46028c17ddd171bee7a0c1` |
| Full-file manifest in the same directory | `db88f85f45d30b59c4e12880fe02803209782d3c1ecfe566d74ff05fe9d5e2e5` |

After serve, two isolated lower hits (38 left, 37 right) each
scored 100. The top A input (31) left 41 and 57 off. The
following top B (30) completed the first pair and each lamp
reported a rising edge at 38.031 s on the host clock. Both
remained on through a second pair (28 then 29), a third pair
(29 then 30), and the final lower bumper hits. A/B value
lamps advanced to 22, 38 and 54 on the respective completions.
Each lower hit after the first pair scored 1,000.

Bally's A5/A6 wiring assigns 41 to the right cap and 57 to the
left. The trace confirms both public bits are available in
three-ball gameplay. Bally FO 579 printed page 4, section C,
describes the separate five-ball sequence with the left cap
lighting on the first pair and the right on the second. That
setting has a separate [five-ball trace](native-followup.md).

## Display callbacks

At startup stock `matahari` supplies four six-digit layouts at
indices 0–3 (type 6), plus two two-digit layouts at indices 4–5
(type 6). `matahard7` supplies four seven-digit layouts at 0–3
(type 8) and two two-digit layouts at 4–5 (type 6).
Both expose a 128×32 renderer output at index 6. It is a rasterized
view of the segment data. The factory game has five physical A1
modules, with two windows on the fifth. The alternate probe
checks callback layout at default DIPs. The [follow-up](native-followup.md) crossed one million in both configurations.
