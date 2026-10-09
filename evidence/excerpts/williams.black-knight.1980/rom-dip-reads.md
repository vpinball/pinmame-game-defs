# Black Knight L-4 game ROM: where the CPU reads the DIP-switch port

Static reading of the `bk_l4` program ROMs from the operator's authorized ROM library (archive
`bk_l4.zip`, members `ic14.716`, `ic17.532`, `ic20.716`, `ic26.716`, CRCs matching the pinned
PinMAME driver), laid out at the addresses `S7_ROMSTART8088` gives them: IC26 at `$D800`, IC14 at
`$E000`, IC20 at `$E800`, IC17 at `$F000`. No ROM bytes are reproduced beyond the short
instruction sequences quoted below.

PinMAME's `s7_dips_r` hands the CPU-board DIP banks to the ROM on PIA 3 (`$2800`) port A, and only
while Master Command Enter (public `-3`) is held. A byte search of the whole program image for
extended-mode accesses to `$2800-$2803` finds:

| Address | Instruction | Context |
| --- | --- | --- |
| `$F03E`, `$F08B`, `$FF7C` | `STAB/STAA $2800` | writes (digit select and LED) |
| `$F039`, `$F086`, `$F0CE` | `STAA $2802` | writes (BCD output) |
| `$E8C9` | `LDAA $2801` | control register A (the Advance interrupt flag) |
| `$FC6A` | `LDAB $2800` | the only read of port A data |
| `$FC71`, `$FC7C` | `LDAB $2801`, `LDAB $2803` | control registers A and B |
| `$FC75` | `LDAB $2802` | port B data |

and one `LDX #$2800` at `$FF2C`, the power-up routine `CLR 1,X; LDAA #$F0; STAA 0,X; LDAB #$3C;
STAB 1,X; STAA 0,X`, which configures the port and writes it.

The read at `$FC6A` is the start of the routine `F6 28 00 / BD EA 2F 02 / F6 28 01 / 39`
(`LDAB $2800; JSR $EA2F` with an inline argument `02`; `LDAB $2801; RTS`). `$EA2F` is the
executive's task-sleep entry: it saves the registers, B included, in the task block and resumes the
task later. The value read from port A is therefore overwritten by the control-register read before
the routine returns. Its three callers (`$FCC8`, `$FCCF`, `$FCFC`) test only the sign of the
returned control register (`BPL`/`BMI`), which is the CA1 interrupt flag that PinMAME drives from
the Advance button. The port A read is the PIA's flag-clearing dummy read, and no code path consumes
the DIP data.

IC17 (`ic17.532`, CRC `bb571a17`), which holds `$FC6A` and `$FF2C`, is the same chip in all four
Black Knight drivers (`bk_l4`, `bk_l3`, `bk_l2`, `bk_f4`).

Conclusion: the L-4 game ROM never samples the CPU-board DIP banks, which agrees with the
instruction booklet, where clearing audits, restoring factory settings and auto-cycle are all
software functions selected at Function 50 with the credit button (35 zeroes the audit totals,
45 restores factory settings, 15 starts auto-cycle) and the DIP switches are not mentioned.
