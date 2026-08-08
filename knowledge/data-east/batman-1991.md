# Batman (Data East, 1991)

Coverage: **partial - manual-verified semantic I/O for the full 8x8 switch and lamp matrices with
connector, wire-colour and drive-transistor wiring, all 22 printed coil drivers including the
Left/Right relay pair, and normalized placements from one retained recreation; held below
author-ready because the Data East controller contract is not yet represented by a profile, the
W7 jumper meaning and device polarities remain incomplete, only a single recreation was retained,
and 4 source disagreements are unresolved**

## Identity

Data East Batman, 1991, `GEN_DEDMD16` - the 128x16 DMD generation, display board 520-5042-00,
sound board 520-5050-01. PinMAME roots the family at `btmn_103` with 5 drivers.
Every one shares `init_btmn` and therefore one `btmnGameData`, so all five are the same physical
machine; what differs is CPU game ROMs, plus a language display ROM on the French and German
sets, plus a ROM-layout macro on 1.01. Sound ROMs are byte-identical across all five.

**`batmanf` is Batman Forever, Sega 1995, `GEN_DEDMD64`.** It lives in the same game-table file
and shares a name prefix, and it is a completely different physical machine. Do not group them.

## Relationship to `pinmame.system-11`, and why this record does not claim it

Batman is **Data East hardware**, `GEN_DEDMD16`. It is not a Williams System 11 machine. What is
true is narrower and is a fact about PinMAME rather than about the cabinet: there is no `de.c`,
`degames.c` includes `s11.h`, and Data East games are driven by the same emulator source file as
Williams System 11 because the Data East CPU board was closely derived from it.

That makes `controllers/pinmame/system-11.json` the closest existing profile, and the two agree on
the load-bearing parts: column-major sequential switch numbering, a single DIP-style jumper bit at
public address 0, 64 lamps, the mux-relay pairing of an A-side address with A+24, address 23 as a
flipper/switched-solenoid enable with no device behind it, and no GI channel anywhere on the
platform. Those conclusions were reached here independently from source before that profile
existed, and they match.

They are not the same profile, and this record therefore keeps the `pinmame.dataeast` platform
string that nine already-committed definitions use rather than claiming a Williams one. Four
differences are established from pinned source:

- **Diagnostic buttons.** `s11.h` gives Data East only `DE_SWADVANCE` (-7) and `DE_SWUPDN` (-6).
  The -5 and -4 addresses beside them are `S11_SWCPUDIAG` and `S11_SWSOUNDDIAG`, Williams only.
- **Special-solenoid permutation.** `setSSSol` selects `ssSolNo[1] = (3, 4, 5, 1, 0, 2)` for Data East
  against `ssSolNo[0] = (5, 4, 1, 2, 0, 3)` for Williams, so the PIA-line-to-public-address map for
  17-22 differs between them.
- **Cabinet column.** Column 1 is loaded from `DE_COMPORTS`, not `S11_COMPORTS`.
- **Advance polarity.** `s11.c` reads Data East's Advance button inverted, as
  `!core_getSw(DE_SWADVANCE)`.

Authoring a Data East profile would set the address contract for all nine of those records at
once, and whether one profile should span every Data East generation - or whether Sega-era games
belong under a profile named "Data East" - are scope and naming calls for a maintainer. This
record documents the model instead of pre-empting that decision.

## The address model, and where it differs from WPC and Whitestar

Data East runs on the shared Williams System 11 core (`s11.c`); there is no `de.c`. `s11.c`
installs no switch or lamp conversion of its own, so it inherits PinMAME's sequential defaults,
`core_m2swSeq(col,row) = col*8+row-7`. **Both printed matrices are column-major**: address =
(column - 1) x 8 + row. Column 1 of the switch matrix is the cabinet/coin column, exactly as
`DE_COMPORTS` declares.

Four things will surprise anyone carrying WPC or Whitestar assumptions across.

- **There is no GI channel at all.** `coreGlobals.nGI` is never assigned anywhere in `s11.c` and
  `gi[]` is never written, so `vp_getGI` always reports zero. General illumination is **public
  solenoid 11**, which the manual prints as the "General Illumination Relay" (K-1) and which
  `s11.c:1207` comments `// GI output`. The retained script agrees, naming its own callback
  `'GI Relay`. Its runtime sense is inverted: asserted output 11 cuts the GI circuit and turns the
  playfield and backglass GI off; deasserted output 11 restores GI. The script states this in its
  own SetGI comment and implements it in `Sol11`, and the superseded legacy record preserves the
  same sense. PinMAME instead types address 11 without `_REV` while applying `_REV` to address 9;
  that discrepancy does not resolve address 9's separate bulb-type and supply conflict, so the two
  facts remain documented without inferring a causal swap.
- **Public solenoid 10 is the Left/Right relay and it re-routes addresses.** With it energised,
  outputs 1-8 are re-published at 25-32 and read zero at 1-8. The manual describes the same
  mechanism in prose: the relay "switch[es] +32 volts between coils or flash lamps; these sets
  are termed 'left' and 'right'", and it is why 22 drivers yield "29 regular coils". Every right
  half on this machine is a group of four flash lamps.
- **PinMAME's flasher typing is uniform and the machine is not.** `s11.c:1209` types the whole
  25-32 block as No. 89 bulbs, but the printed wiring diagram shows four of the eight right-side
  groups mixing No. 906 bulbs in. Treat the emulator's output type as a brightness model, not as
  evidence of what is fitted; the manual's per-drive composition is recorded on each address.
- **64 lamps, not 80**, and every one of the 64 is populated - the printed chart has no "Not
  Used" cell anywhere. Any address above 64 is not hardware; the superseded legacy record listed
  lamps at 109 and 111-132, and the retained script binds 71 `Lampz` slots, both of which are
  recreation-side fictions.
- **Solenoids 33-44 are permanently zero here.** `core_getSol` only serves 33-36 for
  `GEN_ALLWPC`/`GEN_SAM`, and the S11 extra block at 37-44 is written only under
  `S11_SNDOVERLAY` or `S11_PRINTERLINE`, neither of which this game sets.

## Public switches 15 and 16 belong to the emulator

The printed matrix names them Left EOS and Right EOS. Pinned PinMAME publishes something else
there. `btmnGameData` declares `FLIP_SWNO(15,16)`, and `core.c:1740-1741` - under its own comment
"set switches in matrix for non-fliptronic games" - writes the flipper **button** state into those
two addresses via `core_setSw`. Because this game declares no `FLIP_SOL`, no `FLIP_EOS` bit is
ever set and the end-of-stroke simulation at `core.c:1756-1775` never runs at all.

**A recreation must not drive public 15 or 16**, because `core_updateSw` overwrites them on every
frame. The retained known-working script never touches either address, which is the behaviour this
predicts.

## Flipper coils are synthesised, and fire in pairs

There is no `FLIP_SOL`, so `core.c:1746-1753` fabricates 45-48 from Game On plus button state:
power and hold assert and release together. They are not independently controllable and must not
be modelled as separate coils. The manual's own unnumbered "Flipper Solenoids" table lists a left
and a right flipper and nothing else - there is no upper flipper of either hand, which is
consistent with the driver setting no upper-flipper bit.

## Evidence and its limits

The retained manual has **no text layer whatsoever** (70 pages,
0 characters, `ocr_required`), so every table here was read from 400 dpi renders and
transcribed by hand. Nothing came from `pdftotext`.

Spatial placement rests on **one** retained recreation, the VPW v1.1 build, whose playfield is
**952 x 1974** - not the 2162 most WPC-era tables use. 27 of the 44
fitted switches and 54 of the 64 lamps resolved to an object; nothing resolved to an
address the manual prints "Not Used", which is the check that would have caught an invented
binding. 14 coordinates are centroids of an extended object's drag points rather
than a measured center, and are reported as such in the spatial report. Effect coordinates for
ball-handling coils, bumpers, slingshots and the ramp diverter are projections to the exact VPX
assemblies exercised by the working script; they do not pretend to locate hidden coil bodies.

4 source disagreements are recorded as unresolved conflicts rather than decided: `conflict.motor-circuit-identity` - the manual's Museum Motor terminology versus the working script's Bat Bar motor and ramp-diverter routing; `conflict.solenoid-9-bulb-type` - the bulb type and supply PinMAME assigns to solenoid 9; `conflict.matrix-position-2-naming` - whether dedicated matrix position 2 was ever fitted; `conflict.turbo-bumper-center-right-routing` - the retained script's crossed Center/Right turbo-bumper callbacks.
