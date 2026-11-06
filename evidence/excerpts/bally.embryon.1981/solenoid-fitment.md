# Embryon solenoid fitment

The game's solenoid schematic `sol.tif` marks the decoded public outputs 7, 8 and 9
N/U. The separate factory diagnostic table identifies the fifteen fitted devices by
self-test number; the raw service run supplies their public PinMAME addresses.
The continuous-driver drawing (`sol.tif`; color manual PDF page 51) takes PB4/CONT.2
through Q17 to J5-7, marked N/U. This is public output 17 under the pinned
PinMAME mapping; no load is fitted. The other high-nibble lines drive coin lockout
(PB5, public 18), flipper enable (PB6, public 19) and Flipsave (PB7, public 20).

All four fresh raw runs show a boot pulse on the whole 17–20 bank: each set of
rising callbacks and each set of falling callbacks spans less than 1 ms, during
the initial wait before any scenario switch action. Exact per-address times and
raw hashes are retained in
`tools/seeds/bally/embryon-1981-solenoid-self-test.json:startup_continuous_bank`.
There are no later output-17 transitions in any of these retained runs.
They are host callback times, not measured emulated simultaneity or coil timing.
In pinned `src/wpc/by35.c:331–359`, `pia1b_w` complements the high nibble with
`data ^= 0xf0` and maps it to all four public continuous outputs via
`(data & 0xf0)<<12` (lines 357–359). Source SHA-256:
`91df5b0c8a8ba19c017fec5ea45b7a4e2b911f2a56b9a793de7ad1caddd6f6e2`.

The public behavior is thus an explained shared-bank boot pulse, including three
fitted loads. The precise firmware instruction and why the ROM initializes the
bank have not been traced. That remaining firmware question does not identify a
physical device: the game's own no-load drawing controls fitment, and the bank
mapping accounts for the observed state on 17. Together these support `unused`
for 17 without inferring fitment from activity or claiming a traced ROM routine.

The primary visually inspected the original solenoid sheet. The source drawing controls
physical fitment; the emulator trace controls observed public state.
