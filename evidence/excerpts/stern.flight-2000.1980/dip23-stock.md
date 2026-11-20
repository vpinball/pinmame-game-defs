# Factory firmware DIP 23 dataflow

The authorized `flight2k` and `flightfp` archives have SHA-256 `78c865eee57bc78b366c7b81b3c243291009f295bb0c16c16ff3fe3db33c82e0` and `814f31f0d0fa629f89b98b2d499a8bec58b13a0972835b802b014494ec9df550`. Both sets' CPU member names, lengths and SHA-1 digests were checked against `stgames.c` before decoding. `ST200_ROMSTART8888` maps U1/U5/U2/U6 at `$1000/$1800/$5000/$5800` and mirrors U6 at `$F800` for the vectors. The analysis uses the M6800 opcode table from the same pinned PinMAME tree. The evidence root retains the decoder, mnemonic listings and runtime traces.

In `by35.c`, PIA U10 at `$0088` selects DIP bank 17–24 through PA7 (`$80`), and its PB read at `$008A` returns the bank. DIP 23 is bit 6 (`$40`). Both firmware sets execute the same strobe/read loop at `$1904–$1916`. X starts at `$0026` and increments once per bank. Thus the `$1910` PB read with PA7 asserted lands in `$0028` at `$1912`. The separate CB2 read at `$1923–$1925` stores bank 25–32 at `$0029`.

The boot test reads `$0026:$0027` at `$192C` and `$0028:$0029` at `$1930`. If either word is nonzero the firmware branches to `$1937`. Otherwise `$1934` jumps to the automatic service cycle at `$5968`. DIP 23 therefore participates in the combined all-off test.

| Other ROM reads of `$0028` | Bits kept or tested |
| --- | --- |
| `$1C92`, `$1E25`, `$1E41`, `$51FE`, `$5F27` | `LSRA` or `LSRB` into carry, bit 0 |
| `$5552` | `ANDB #$08`, bit 3 |
| `$556D` | `ANDB #$06`, bits 1–2 |
| `$559A` | `ANDA #$10`, bit 4 |

The `$5F2D` write clears bit 0 after testing it. `$5979` writes the service mode's `$FF`. The possible `$5876` absolute reference identified by scanning across instruction boundaries lies in table data. The analysis checked the references in both sets and the indexed bank load/store. The manual's operator-option pages and the exact VPX DIP editor list no individual stock DIP 23 option.

## Isolated runtime comparison

Four scripted LibPinMAME runs used the pinned DLL, zeroed initial CMOS, switches 33–35 held at 1, a 20-second boot wait, and no service button presses. The only within-driver change was bit 6 in bank 3 of the supplied initial state. The retained packet pins the traces, scenarios, initial-state hashes and replay commands. The decoded boot branch predicts the observed distinction. [Stock runtime evidence](../../runtime/stern/flight-2000-stock.json) · [Free-play runtime evidence](../../runtime/stern/flight-2000-free-play-dip23.json)

To replay either DIP setting, place the 302-byte initial state described in the run's `nvram_initialization` in `<work-dir>/nvram/<driver>.nv`. Use a fresh work directory per run and the portable DIP scenario with `--boot-wait 20`.

| Driver | Bank 3 | Momentary solenoid addresses observed at 1 |
| --- | --- | --- |
| `flight2k` | `$00` | 1, 3–15 |
| `flight2k` | `$40` | none |
| `flightfp` | `$00` | 1, 3–15 |
| `flightfp` | `$40` | none |

Neither all-off capture recorded public 2. The observed outputs distinguish the startup paths without exercising every step of the automatic cycle. The whole-word startup branch, the per-option masked reads and the probe establish the stock disposition. The DIP's modified-ROM rules are covered by the author's release documentation.
