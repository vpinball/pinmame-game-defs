# Bounded PIA2 configuration and printer evidence

Curator independently verified the retained 23-file manifest, reproduced the
focused-code/source/input artifacts in a successor directory, and inspected the
normal setup and printer paths against pinned PinMAME. This records derived
addresses, mnemonics and values only; no opcode-byte columns or ROM data are
redistributed. CPU address equals file offset in these 64 KiB images, with
executable mapping $4000–$FFFF. This is static inference, not observed execution.

| Region | All three CPU members | Consequence within this reviewed path |
| --- | --- | --- |
| Reset / initialization | Reset vector targets $4100; its direct call $44BD reaches setup $4585 | Verified entry/call path, rather than an unqualified raw byte match |
| $4585–$4593 | Load B=$FF; write CRA=$10, DDRA=$FF, then CRA=$14 | Normal PA direction is all outputs; external PA7 is removed by the 6821 direction mask |
| $4594–$45A1 | Write CRB=$30, DDRB=$FF, then CRB=$34 | The setup write of $FF to $2802 is a DDR write, not a printer character |
| $61B6 | Read PA at $2800; immediately replace A with a read of $2803 | That PA read does not consume PA7 for a branch or game-state store |
| Fatal boot-test blink | Configure DDRA=$10; read PA, xor bit4 and write PA; overwrite A before loop tests | PA7 can enter the latch but the external callback masks output to bit4 |

Pinned `6821pia.c` reads `(out_a & ddr_a) + (in_a & ~ddr_a)` and masks output
callbacks with DDRA. Changing external PA7 therefore changes neither a normal
DDRA=$FF read nor the masked DDRA=$10 fault-blink output. Exhaustive arithmetic
checks over the 256 output-latch values verify that formula; they are not ROM runs.

The actual buffered printer code is present, and cannot be described as merely
initializing PB to zero:

| Role | wwfr_106 | wwfr_103 / wwfr_103f |
| --- | --- | --- |
| Conditional direct caller | $AEC5 | $AE40 |
| Buffer-drain entry | $B068 | $AFE3 |
| Character buffer | $0A00 | $0A00 |
| Send helper | $B098 | $B013 |
| Read CRA / test IRQ2 ($40) | $B0A2 / $B0A5 | $B01D / $B020 |
| Guarded write to PB ($2802) | $B0AE | $B029 |
| PA strobe of $03 then $00 | $B0B3 / $B0B8 | $B02E / $B033 |
| Timeout handler | $B0C3 | $B03E |

The helper reads PA (clearing pending IRQ flags), polls CRA bit6, and writes its
character to PB only when input CA2 has raised IRQ2. Stock `s11.c` PIA2 has no CA2
input callback or setter; service updates supply CA1/CB1. The 6821 core raises
IRQ2 from an input CA2 transition, while CRA writes discard bits6/7. From fresh
reset, that interface cannot supply this send helper's ready condition. It times
out before its PB write. PA7's DIP value does not supply the separate CA2 handshake.
This explains the bounded silent printer probes without identifying the physical
printer protocol or declaring public 37–44 globally unused.

The reviewed initialization/IRQ/fault regions are identical across the three
source-matching CPUs. The direct-flow index still has unresolved indexed calls
and the scheduler, assumes ordinary call returns despite inline-argument helpers,
and does not prove all indexed memory accesses. Thus it cannot establish a
whole-program unused PA7 claim, physical jumper identity, or exhaustion of every
printer-output path. DIP bank0 and printer data slots retain unknown semantics.

REA supplied archive inventories; raw M6808 was unsupported. The installed
Ghidra alias selected an incompatible 6809 language and was not used. The focused
decoder uses pinned `6800dasm.c` with its M6808 invalid-opcode mask. The retained
full analysis and ROM bytes remain external, with exact hashes in the portable
static-evidence input.
