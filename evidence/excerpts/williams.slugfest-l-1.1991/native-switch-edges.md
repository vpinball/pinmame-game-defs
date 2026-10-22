# Original L-1 native service observations

Fresh isolated `sf_l1` state, no checksum bypass or prior NVRAM;45s boot,
keyboard handling and built-in mechanisms disabled. Native DLL SHA-256
`2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`,
built from pinned 97aa922bf8e4b6970126192ec1ac1fb0305a4f62. Legal user archive
and exact scenario/raw-run hashes are in the derived runtime evidence.

Exact retained menu templates checkpoint MAIN MENU B. BOOKKEEPING, MAIN MENU
T. TESTS and T.1 SWITCH EDGES. A one-second released-Enter debounce precedes
starting T.1. Earlier experiment without that gap remained on the test menu;
it is retained for diagnosis but supplies no polarity assertions.

Visually checked top-line names in the actual running T.1 test:

| Public switch | At 0 | At 1 | After release to 0 |
| --- | --- | --- | --- |
| 41 | SWITCH EDGES | Target Panel-L | SWITCH EDGES |
| 23 | SWITCH EDGES | Dispenser Prize | SWITCH EDGES |
| 54 | SWITCH EDGES | Pitch Opto | SWITCH EDGES |
| 55 | SWITCH EDGES | Ramp Opto | SWITCH EDGES |
| 61 | SWITCH EDGES | L Bleacher | SWITCH EDGES |
| 62 | SWITCH EDGES | M Bleacher | SWITCH EDGES |
| 63 | SWITCH EDGES | R Bleacher | SWITCH EDGES |

LAST SW retains the previous number after release; it is not the active-name
oracle. Read the top line. All five masked optos and both unmasked controls are
active at public 1. Combined with this game's direct WPC matrix read and mask,
the five masked contacts are physically normally closed and unmasked 23/41 are
normally open. The trace alone does not establish beam clear/blocked geometry.

With game-enable 31 active, host 112=1 produces native synthetic 45/46 together;
host 114=1 produces 47/48 together. Release clears the pair. These are runtime
emulator output states even though the machine has no physical flippers, and
they are not bat windings. Host-injected switch values are recorded as stimulus,
not ROM-observed switch edges. No absence in this run proves an unobserved
J111 output or generic input unreadable/unused.

The compact evidence includes all 21 interpreted optical/control frames with
their raw-pixel hashes and native active-output snapshots. Full raw JSON/PGMs
remain under review-artifacts/williams.slugfest-l-1.1991/harness.
