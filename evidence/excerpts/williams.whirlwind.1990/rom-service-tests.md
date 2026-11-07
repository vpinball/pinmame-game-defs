# Whirlwind ROM service observations

These runs use `whirl_l3`, the native library and factory-initialized NVRAM
identified in `drop-target-levels.md`. Keyboard and mechanics are disabled.
Each run begins in a new directory containing only that initial NVRAM.
No ROM bytes or NVRAM are committed.

## Switch Levels

Scenario `tools/harness-scenarios/system-11/whirlwind-all-switch-levels.json`,
Current portable scenario SHA-256 `85f2958b98ef338964e31d45312aed40a165f2ab1e739a7e24a204d5aaafcda2`.
The retained run used scenario SHA-256
`06f98e99b80b1f1d25c6bad8fb24f02d1fd4104a796d57b4cf237c934fd48aca`; only descriptive notes differ.
Raw run `external:pinmame-review-artifacts/whirlwind-20261106/harness-all-levels.json`,
SHA-256 `8ebba45898c3b38a1ce90a9ad38cbab1bf4cc93b572bb24c8614a2da1a71495e`.

The run requires the ROM's `SWITCH LEVELS` checkpoint, then writes each
input to 1 for 1.3 seconds and 0 for 0.5 seconds. It tests exactly:

`1,3,4,5,6,7,8,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,33,34,35,36,37,38,39,40,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,59,60,61,82,84`.

For every high interval the ROM lower display identifies the corresponding
matrix number. Inputs 82/84 identify 57/58, confirming the core's flipper
mirror path. Control 15 is repeated at the end. Relay-feedback input 2 is
rewritten by the driver and is not claimed as a directly exercised switch.

The decoded display uses `O` for zero and `S` for five. The proof reads
display events between each host high and low, after the first 50 ms, and
compares the switch-number token after test number `O6`. It normalizes
only `O -> 0` and `S -> 5`. Every interval has at least one matching frame.
Some snapshots fall during a display blink or partial scan and are blank
or contain mixed letters; a single snapshot is not used as negative proof.
Examples retained literally:

| Host input 1 | ROM lower display |
| --- | --- |
| 1 | `O6 O1` |
| 5 | `O6 OS` |
| 26 | `O6 26` |
| 41 | `O6 41` |
| 82 | `O6 S7` |
| 84 | `O6 S8` |

Together with the uncomplemented `pia4a_r` read and zero per-game mask
documented in `drop-target-levels.md`, these active levels establish
normally-open matrix contacts. The beam state and a mechanism's parked
position are not used in that derivation.

## Coil Test

Scenario `tools/harness-scenarios/system-11/whirlwind-coil-test.json`, SHA-256
`ac18db5b32454f12ce5330aa58850f5f91d195dc2f56fc9cd221862edf867217`.
Raw run `external:pinmame-review-artifacts/whirlwind-20261106/harness-coils.json`,
SHA-256 `168021c8e573436e4c750805775dc99489749c5d79ae471d963362c7dddf2d39`.

The run requires `COIL TEST` and observes 110 seconds of automatic cycling.
After entry, it publishes exactly public solenoids
`1–22,25–32,37–41`. Boot-time activity is excluded from that set.
The first complete sound-overlay sequence has these callback times and
the immediately preceding ROM lower display:

| Public solenoid | Time (s) | ROM lower display | Manual item |
| --- | --- | --- | --- |
| 37 | 54.988618 | `OS 23` | 23 |
| 38 | 55.974101 | `OS 24` | 24 |
| 39 | 56.942777 | `OS 2S` | 25 |
| 40 | 57.927404 | `OS 26` | 26 |
| 41 | 58.913525 | `OS 27` | 27 |

The upper display clearly reads `BLOWER` for 38 and `SPIN WHEELS` for 41;
the flasher names have decoder gaps. These observations corroborate the
manual-item +14 mapping and working script callbacks. They do not prove
physical bulb counts, geometry, or non-fitment from an absent callback.

Both raw runs completed with `failure: null`. Derived summaries and the
full input identities remain beside the raw runs in the retained folder.
