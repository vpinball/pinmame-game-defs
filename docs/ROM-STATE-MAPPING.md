# Mapping a WPC ROM's own game state

A reusable procedure for recovering a WPC game's internal state layout and rule thresholds from
its ROM, using a headless emulator and a 6809 disassembler. It sits between the harness escalation
and the Ghidra escalation described in `INSTRUCTIONS.md`: cheaper and more repeatable than Ghidra,
and able to answer questions the harness cannot, because it observes CPU RAM rather than only the
public switch, lamp and solenoid addresses.

First applied to Attack From Mars (`afm_113b`) on 5 September 2026. The machine-specific results
are in `knowledge/bally/attack-from-mars-1995.md`; this file is the method.

## What it can and cannot establish

**Can:** the address of a counter, flag, timer or bitmask in CPU RAM; the code that writes and
tests it; the arithmetic of a threshold, including which operator adjustment feeds it; the legal
range of every adjustment; the operator menu's printed names.

**Cannot:** physical identity, polarity, quantity or socket location. Those rules from
`INSTRUCTIONS.md` are unchanged. A RAM address is evidence about firmware behaviour, not about
hardware. Nothing here promotes a spatial or wiring assertion.

**Evidence discipline.** The full provenance and external-retention requirements of
`INSTRUCTIONS.md` apply unchanged; an archive SHA-256 and an emulator version are the minimum, not
the whole record. A run must also retain its scenario scripts, tool versions and hashes,
initialisation conditions and replay command under the configured external roots, and commit only
compact hash-linked derived evidence. No ROM bytes enter Git, and that exclusion covers opcode-byte
columns in disassembly listings, RAM captures and NVRAM images as well as the ROM itself. Record
addresses, mnemonics and measured values. Findings begin candidate-grade and are promoted only
under the repository's normal promotion rules.

## Why CPU RAM is reachable at all

PinMAME's WPC NVRAM handler saves `wpc_ram` from 0x0000 for 0x3000 bytes on WPC-95, DCS, Security
and WPC-95-DCS generations, and 0x2000 on earlier WPC. On those generations "NVRAM" is therefore
the entire CPU RAM, audits and live game state alike. Consequences:

- A headless emulator exposes the same bytes directly.
- A VPinMAME table script can read them at play time through `Controller.NVRAM`, or receive only
  the changed rows through the `ChangedNVRAM` callback that `core.vbs` already wires when a table
  sets `UseVPMNVRAM` and assigns `NVRAMCallback`. Verified live on Attack From Mars, 847 polls
  over 93 seconds with no COM errors, the full image indexed by RAM offset.

## Procedure

### 1. Drive the ROM headlessly

`wpc-emu` (npm, MIT, version 0.36.7 used here) runs a WPC ROM in Node at roughly 18x real time and
exposes RAM, lamps, solenoids, the dot-matrix frame and the sound-command stream. Build a rig that
holds a small model of ball location, updated from the ROM's own solenoid firings: a trough eject
puts a ball in the shooter lane, the auto-plunger takes it out, a popper kick returns its held
ball, the bank motor swaps the two limit switches. Optos read closed when empty in this emulator's input model, which is an emulator-input convention rather than a polarity claim about the machine.

**Validate every scripted shot before trusting a negative result.** A shot that produces no sound
and no score is a broken sequence, not a discovered rule. Two wrong conclusions in the first
campaign came from a ramp missing its exit switch and a centre ramp routed through the wrong exit.

### 2. Measure the ROM's switch timing once

Pulse one switch repeatedly at varying widths and gaps, and count what the ROM registers. Report
the switches tested, the pulse and gap definitions, the emulator clock and the success counts. The
result bounds later scripts for the switches tested. It is not a platform constant, and an interval
that worked is a tested interval rather than a proven minimum.

### 3. Locate a byte by recording games

Record whole scripted games, sampling RAM at 50 ms alongside the sound, solenoid, lamp and switch
timeline. Then search for bytes whose value is a function of the current mode, bytes tracking a
count the script marked, and bytes decreasing monotonically inside a window. Mark generously: a mark per
jet hit is what makes a candidate identifiable. Correlation identifies a candidate; only the
controlled verification in step 4 establishes it.

### 4. Turn an address into a rule

1. **Watchpoint.** Patch the emulated CPU's memory read and write functions and record the program
   counter and active ROM bank at every access to the address. Patch the CPU's captured function
   references, not the board's handler, because the CPU binds its own copy at construction.
2. **Disassemble** the recorded site. Bank N maps to file offset `N*0x4000 + (pc-0x4000)`; the
   fixed region at and above 0x8000 is the last 32 KB of the image. The recorded PC sits just past
   the storing instruction.
3. **Predict, then confirm.** A rule is not established until a number computed from the
   disassembly appears in the emulator. On Attack From Mars the Super Jets formula predicted a
   requirement of 125 on the ball after the first collect, and the emulator showed 125.

## Patterns seen on WPC, to investigate and verify per ROM

These held on the one ROM examined so far. Treat each as a hypothesis to test on a new game rather
than a platform guarantee.

- **Per-player feature block.** One fixed-stride block per player holds that player's counters.
  Find one field and the neighbours follow, because the disassembly indexes them off one register.
- **Inline-argument far calls.** `JSR $xxxx` followed by argument bytes which the callee reads off
  the return address and then skips past. This is what derails a naive disassembler, and it is
  also the hook: scanning for one call pattern enumerates every use of that facility.
- **Operator adjustments.** Read through such a call with an inline index. The value address is
  `base + 2*(index & 0x7F) + 1`, with separate bases for the standard and game tables. Each
  adjustment carries a 12-byte ROM descriptor of default, minimum and maximum, and the getter
  clamps every read against it, so a stored byte and the effective value can differ.
- **Menu names are plain ASCII in the ROM**, in index order, one bank per supported language.
  Pairing them with the descriptors yields the complete operator menu with defaults and ranges
  without any manual. This matters where a manual's adjustment section is not retained.
- **Bitmask target banks.** One bit per target, cleared on hit, with the mode firing when the byte
  reaches zero. Three instructions, and the shape repeats across games.
- **A running-mode bit array** maintained by shared set-bits and clear-bits routines, where
  stacked modes appear as the bitwise or of their masks.

## Cautions learned

- **A field a mode arms is not always the field it uses.** Attack From Mars' final wave writes the
  ordinary wave requirement and then counts on a different byte entirely. A field that stops moving
  while its mode continues is the signal to look for the counter actually in use.
- **Read the game's own project documentation first.** In the first campaign, several facts were
  rediscovered that a table project already recorded, and one correct note was briefly contradicted
  by a wrong measurement.
- **Emulator behaviour is not hardware behaviour.** Everything here is firmware evidence. Physical
  claims still require the manual, the harness and the rules already in `INSTRUCTIONS.md`.

Record each application, and its confidence limits, in `docs/CURRENT-STATE.md`.
